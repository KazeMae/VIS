<!--气象参数折线图-->
<template>
  <div id="chart4">

  </div>
</template>

<script>
import {chart4Data} from "@/api/api";
import * as echarts from 'echarts'
import {mapState} from "vuex";

export default {

  name: 'ChartFour',
  data() {
    return {
      hours: [],
      temperature: [],
      wind_direction: [],
      wind_speed: [],
      precipitation: []
    }
  },
  computed: {
    ...mapState({
      years: state => state.years,  // 从 Vuex 获取 years
    }),
    years() {
      return this.$store.state.years.length > 0 ? this.$store.state.years : [2020];
    }
  },
  watch: {
    years: 'fetchChartData',
  },
  mounted() {
    // 在组件挂载后请求数据并渲染图表
    this.fetchChartData();
  },
  methods: {
    async fetchChartData() {
      try {
        const response = await chart4Data(this.years);
        this.hours = response.hours;
        this.temperature = response.temperature;
        this.wind_direction = response.wind_direction;
        this.wind_speed = response.wind_speed;
        this.precipitation = response.precipitation;
        // 调用渲染图表的方法
        this.renderChart();
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    },
    renderChart() {
      // 获取 DOM 容器并初始化 ECharts 实例
      const chart = echarts.init(document.getElementById('chart4'));
      // 配置图表选项
      const option = {
        title: {
          text: `{title| ${this.years} 气温、风向、风速、降水量变化}`,
          textStyle: {
            fontSize: 14,
            fontWeight: 'bold',
            rich: {
              title: {
                backgroundColor: '#87888c',
                padding: 5, // 文字边界扩充
                color: '#ffffff', // 文字颜色
                shadowBlur: 5, // 阴影模糊等级
                shadowColor: 'rgba(84,112,198,0.42)', // 阴影颜色
                shadowOffsetX: 4, // 阴影x轴偏移
                shadowOffsetY: 4 // 阴影y轴偏移
              }
            }
          },
          top: '2%',
          left: 'center'
        },
        tooltip: {
          axisPointer: {
            type: 'cross',
          },
          trigger: 'axis'
        },
        dataZoom: {
          type: 'slider',
          start: 0,
          end: 1
        },
        legend: {
          data: ['气温', '风向', '风速', '降水量'],
          orient: 'horizontal',
          left: 'center',
          top: '15%'
        },
        grid: {
          top: '23%',
          left: '2%',
          right: '5%',
          bottom: '5%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: this.hours
        },
        yAxis: [
          {
            type: 'value',
            name: '气温',
            position: "left",
            splitLine: {
              show: false
            }
          },
          {
            type: 'value',
            position: 'left',
            offset: 25,
            splitLine: {
              show: false
            }
          },
          {
            type: 'value',
            position: 'right',
            splitLine: {
              show: false
            }
          },
          {
            type: 'value',
            name: '降水量',
            position: 'right',
            offset: 30,
            splitLine: {
              show: false
            }
          }
        ],
        series: [
          {
            name: '气温',
            type: 'line',
            data: this.temperature,
            yAxisIndex: 0,
            symbol: 'none'
          },
          {
            name: '风向',
            type: 'line',
            data: this.wind_direction,
            yAxisIndex: 1,
            symbol: 'none'

          },
          {
            name: '风速',
            type: 'line',
            data: this.wind_speed,
            yAxisIndex: 2,
            symbol: 'none'

          },
          {
            name: '降水量',
            type: 'line',
            data: this.precipitation,
            yAxisIndex: 3,
            symbol: 'none'
          }
        ]
      };
      chart.setOption(option);
    }
  }
}
</script>

<style scoped>
#chart4 {
  width: 100%;
  height: 100%;
}

</style>