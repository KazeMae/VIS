<!--污染物分析折线图-->
<template>
  <div id="chart1">

  </div>
</template>

<script>
import {chart1Data} from "@/api/api";
import * as echarts from 'echarts'
import {mapState} from "vuex";

export default {

  name: 'LineChart',
  computed: {
    ...mapState({
      years: state => state.years,  // 从 Vuex 获取 years
      area: state => state.area,  // 从 Vuex 获取 area
    }),
    years() {
      return this.$store.state.years.length > 0 ? this.$store.state.years : [2020];
    }
  },
  data() {
    return {
      chartData: null,
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
        const response = await chart1Data(this.area, this.years);
        this.chartData = response;  // 获取到的数据
        // 调用渲染图表的方法
        this.renderChart();
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    },
    renderChart() {
      if (this.chartData) {
        // 获取 DOM 容器并初始化 ECharts 实例
        const chart = echarts.init(document.getElementById('chart1'));

        // 配置图表选项
        const option = {
          title: {
            text: `{title| ${this.years}年${this.area} 区域污染物分析}`,
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
            left: 'center',
            padding: [0, 10, 0, 0],
          },
          grid: {
            top: 35,
            left: '2%',
            right: '25%',
            bottom: '5%',
            containLabel: true
          },
          tooltip: {
            show: true,
            trigger: 'axis',
          },
          legend: {
            type: 'scroll',
            data: ['SO2', 'NO2', 'CO', 'O3', 'PM10', 'PM25'],
            orient: 'vertical',
            top: 'center',
            right: '0%',
            height: '70%',

          },
          xAxis: {
            type: 'category',
            data: this.chartData.months  // 使用后端返回的月份数据
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {name: 'SO2', type: 'line', data: this.chartData.so2},
            {name: 'NO2', type: 'line', data: this.chartData.no2},
            {name: 'CO', type: 'line', data: this.chartData.co},
            {name: 'O3', type: 'line', data: this.chartData.o3},
            {name: 'PM10', type: 'line', data: this.chartData.pm10},
            {name: 'PM25', type: 'line', data: this.chartData.pm25}
          ]
        };
        chart.setOption(option);
      }
    }
  }
}
</script>

<style scoped>
#chart1 {
  width: 100%;
  height: 100%;
}

</style>