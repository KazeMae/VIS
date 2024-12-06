<template>
  <div id="chart3">

  </div>
</template>

<script>
import {chart3Data} from "@/api/api";
import * as echarts from 'echarts'

export default {

  name: 'ChartThree',
  data() {
    return {
      area: '东昌府区',
      years: [],
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
  methods: {
    async fetchChartData() {
      try {
        const response = await chart3Data(this.area);
        // console.log(response)
        this.years = response.years;
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
      // 配置图表选项
      const option = {
        title: {
          text: '{title| 各年份污染物变化}',
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
          top: '2%',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['SO2', 'NO2', 'CO', 'O3', 'PM10', 'PM2.5'],
          orient: 'horizontal',
          left: 'center',
          top: '15%'
        },
        xAxis: {
          type: 'category',
          data: this.years  // X轴为年份
        },
        yAxis: {
          type: 'value'
        },
        grid: {
          top: '23%',
          left: '2%',
          right: '5%',
          bottom: '5%',
          containLabel: true
        },
        series: [
          {
            name: 'SO2',
            type: 'bar',
            data: this.so2
          },
          {
            name: 'NO2',
            type: 'bar',
            data: this.no2
          },
          {
            name: 'CO',
            type: 'bar',
            data: this.co
          },
          {
            name: 'O3',
            type: 'bar',
            data: this.o3
          },
          {
            name: 'PM10',
            type: 'bar',
            data: this.pm10
          },
          {
            name: 'PM2.5',
            type: 'bar',
            data: this.pm25
          }
        ]
      };
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