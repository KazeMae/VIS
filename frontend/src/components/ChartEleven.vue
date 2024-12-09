<!--PM2.5浓度变化面积图-->
<template>
  <div id="chart7">

  </div>
</template>

<script>
import {chart7Data} from "@/api/api";
import * as echarts from 'echarts'

export default {

  name: 'ChartEleven',
  data() {
    return {
      chartData: [],
      yearList: [],
      avgPm25: []
    }
  },
  mounted() {
    // 在组件挂载后请求数据并渲染图表
    this.fetchChartData();
  },
  methods: {
    async fetchChartData() {
      try {
        const response = await chart7Data();
        this.chartData = response
        this.yearList = response.map(item => item.year);
        this.avgPm25 = response.map(item => item.avg_pm25);
        // 调用渲染图表的方法
        this.renderChart();
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    },
    renderChart() {
      // 获取 DOM 容器并初始化 ECharts 实例
      const chart = echarts.init(document.getElementById('chart7'));
      // 配置图表选项
      const option = {
        title: {
          text: '{title| 每年PM2.5平均浓度变化}',
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
        grid: {
          top: '23%',
          left: '2%',
          right: '5%',
          bottom: '5%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: this.yearList
        },
        yAxis: {
          type: 'value',
          min: 56
        },
        series: [{
          data: this.avgPm25,
          type: 'line',
          smooth: true,
          areaStyle: {
            color: '#247bc7'
          }
        }]
      };
      chart.setOption(option);
    }
  }
}
</script>

<style scoped>
#chart7 {
  width: 100%;
  height: 100%;
}

</style>