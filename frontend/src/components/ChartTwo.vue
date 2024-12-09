<!-- 热力图 -->
<template>
  <div id="chart2">

  </div>
</template>

<script>
import {chart2Data} from "@/api/api";
import * as echarts from 'echarts'
import {mapState} from "vuex";

export default {

  name: 'ChartTwo',
  data() {
    return {
      chartData: {
        columns: [],
        data: []
      }
    }
  },
  computed: {
    ...mapState({
      years: state => state.years,  // 从 Vuex 获取 years
      area: state => state.area,  // 从 Vuex 获取 area
    }),
    years() {
      return this.$store.state.years.length > 0 ? this.$store.state.years : [2020];
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
    formatDataForHeatmap(matrix) {
      let formattedData = [];
      for (let i = 0; i < matrix.length; i++) {
        for (let j = 0; j < matrix[i].length; j++) {
          formattedData.push([i, j, matrix[i][j]]);
        }
      }
      // console.log(formattedData)
      return formattedData;
    },
    async fetchChartData() {
      try {
        const response = await chart2Data(this.area, this.years);
        this.chartData = response;  // 获取到的数据
        // console.log(this.chartData)
        // 调用渲染图表的方法
        this.renderChart();
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    },
    renderChart() {
      if (this.chartData) {
        // 获取 DOM 容器并初始化 ECharts 实例
        const chart = echarts.init(document.getElementById('chart2'));
        const {columns, data} = this.chartData;
        // console.log(this.chartData)
        // 配置图表选项
        const option = {
          title: {
            text: `{title| ${this.years}年${this.area} 污染物与气象变量相关性}`,
            textStyle: {
              fontSize: 14,
              fontWeight: 'bold',
              rich: {
                title: {
                  backgroundColor: '#87888c',
                  padding: 5, // 文字边界扩充
                  color: '#ffffff', // 文字颜色
                  shadowBlur: 5, // 阴影模糊等级
                  shadowColor: 'rgba(84,112,198,0.47)', // 阴影颜色
                  shadowOffsetX: 4, // 阴影x轴偏移
                  shadowOffsetY: 4 // 阴影y轴偏移
                }
              }
            },
            top: '5%',
            left: 'center'
          },
          tooltip: {
            position: 'top'
          },
          grid: {
            top: 30,
            left: '2%',
            right: '5%',
            bottom: '5%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: columns,
          },
          yAxis: {
            type: 'category',
            data: columns,
          },
          visualMap: {
            min: -1,
            max: 1,
            calculable: true,
            inRange: {
              color: ['#FFFFFF', '#FF4500']  // 设置颜色范围
            },
            show: false,
            // height: 5,
            // top: 15,
            // left: 'center',
            // orient: 'horizontal'
          },
          series: [{
            name: '相关性',
            type: 'heatmap',
            data: this.formatDataForHeatmap(data),
            label: {
              show: false,
            },
            emphasis: {
              itemStyle: {
                color: '#ff3333'
              }
            }
          }]
        };
        chart.setOption(option);
      }
    }
  }
}
</script>

<style scoped>
#chart2 {
  width: 100%;
  height: 100%;
}

</style>