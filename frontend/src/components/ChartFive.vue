<template>
  <div id="chart5">

  </div>
</template>

<script>
import {chart5Data} from "@/api/api";
import * as echarts from 'echarts'
import {mapState} from "vuex";

export default {

  name: 'ChartFive',
  data() {
    return {
      chartData: []
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
  mounted() {
    // 在组件挂载后请求数据并渲染图表
    this.fetchChartData();
  },
  watch: {
    years: 'fetchChartData',
  },
  methods: {
    async fetchChartData() {
      try {
        const response = await chart5Data(this.years);
        this.chartData = response
        // 调用渲染图表的方法
        this.renderChart();
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    },
    renderChart() {
      // 获取 DOM 容器并初始化 ECharts 实例
      const chart = echarts.init(document.getElementById('chart5'));
      // 配置图表选项
      const option = {
        title: {
          text: `{title| ${this.years} 空气质量等级分布}`,
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
          trigger: 'item'
        },
        legend: {
          orient: 'horizontal',
          left: 'center',
          top: '10%'
        },
        series: [
          {
            name: '质量等级',
            type: 'pie',
            radius: '50%',
            center: ['50%', '60%'],
            data: this.chartData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };
      chart.setOption(option);
    }
  }
}
</script>

<style scoped>
#chart5 {
  width: 100%;
  height: 100%;
}

</style>