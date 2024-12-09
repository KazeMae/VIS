<!--雷达图-->
<template>
  <div id="chart3">

  </div>
</template>

<script>
import {chart3Data} from "@/api/api";
import * as echarts from 'echarts'
import {mapState} from "vuex";

export default {
  name: 'ChartThree',
  computed: {
   ...mapState({
      area: state => state.area,
      years: state => state.years
    }),
    // 处理years为空时的默认情况（可根据实际需求调整默认值）
    years() {
      return this.$store.state.years.length > 0? this.$store.state.years : [2020];
    }
  },
  data() {
    return {
      // 这里area初始值可以移除，因为从Vuex获取，或者根据实际情况保留作为本地临时默认值等使用
      so2: [],
      no2: [],
      co: [],
      o3: [],
      pm10: [],
      pm25: []
    }
  },
  mounted() {
    // 在组件挂载后请求数据并渲染图表
    this.fetchChartData();
  },
  watch: {
    years: 'fetchChartData',
    area: 'fetchChartData'
  },
  methods: {
    async fetchChartData() {
      try {
        const response = await chart3Data(this.area, this.years);
        // console.log(response)
        this.so2 = response.so2;
        this.no2 = response.no2;
        this.co = response.co;
        this.o3 = response.o3;
        this.pm10 = response.pm10;
        this.pm25 = response.pm25;
        // 调用渲染图表的方法
        this.renderChart();
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    },
    renderChart() {
      // 获取 DOM 容器并初始化 ECharts 实例
      const chart = echarts.init(document.getElementById('chart3'));
      // 配置图表选项（修改图例位置，并更换为低饱和度颜色）
      const option = {
        title: {
          text: `{title| ${this.years}年${this.area}区域污染物变化}`,
          textStyle: {
            fontSize: 14,
            fontWeight: 'bold',
            rich: {
              title: {
                backgroundColor: '#87888c',
                padding: 5, // 文字边界扩充
                color: '#ffffff',
                shadowBlur: 5, // 阴影模糊等级
                shadowColor: 'rgba(84,112,198,0.47)',
                shadowOffsetX: 4, // 阴影x轴偏移
                shadowOffsetY: 4 // 阴影y轴偏移
              }
            }
          },
          top: '2%',
          left: 'center'
        },
        tooltip: {
          trigger: 'item' // 对于雷达图，触发提示框的方式通常设为'item'
        },
        legend: {
          data: ['2020', '2021', '2022'],
          orient: 'vertical',
          right: '5%', // 靠右对齐，距离右边 5% 的位置
          top: '50%', // 垂直方向上大致在中间靠下一点的位置，可根据实际微调
          itemGap: 8, // 图例项之间的间隔，可根据实际调整
          textStyle: {
            fontSize: 12 // 图例文字大小，可按需调整
          }
        },
        radar: {
          // 雷达图的指示器配置，对应各个维度（这里对应不同污染物指标）
          indicator: [
            {name: 'SO2', max: Math.max(...this.so2)},
            {name: 'NO2', max: Math.max(...this.no2)},
            {name: 'CO', max: Math.max(...this.co)},
            {name: 'O3', max: Math.max(...this.o3)},
            {name: 'PM10', max: Math.max(...this.pm10)},
            {name: 'PM2.5', max: Math.max(...this.pm25)}
          ]
        },
        series: []
      };
      const yearsLength = this.years.length;
      for (let i = 0; i < yearsLength; i++) {
        const yearData = {
          value: [
            this.so2[i],
            this.no2[i],
            this.co[i],
            this.o3[i],
            this.pm10[i],
            this.pm25[i]
          ],
          name: this.years[i]
        };
        const seriesItem = {
          name: this.years[i], // 设置数据系列名称为对应年份，用于图例显示
          type: 'radar',
          data: [yearData]
        };
        option.series.push(seriesItem);
      }
      option.legend.data = option.legend.data.concat(['SO2', 'NO2', 'CO', 'O3', 'PM10', 'PM2.5']); // 添加污染物指标名称到图例数据源
      chart.setOption(option);
    }
  }
}
</script>

<style scoped>
#chart3 {
  width: 100%;
  height: 100%;
}
</style>