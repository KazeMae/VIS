<!--车流量环状图-->
<template>
  <div id="chart6">
    <!-- Chart will be rendered here -->
  </div>
</template>

<script>
import {chart6Data} from "@/api/api";
import * as echarts from 'echarts';
import {mapState} from 'vuex';

export default {
  name: 'ChartSix',
  data() {
    return {
      chartData: []
    };
  },
  computed: {
    ...mapState({
      checkPoint: state => state.checkPoint || '黄河10', // 从 Vuex 获取 checkPoint，默认值为 '黄河10'
    }),
  },
  mounted() {
    // 在组件挂载后请求数据并渲染图表
    this.fetchChartData();
  },
  watch: {
    checkPoint: 'fetchChartData'
  },
  methods: {
    async fetchChartData() {
      try {
        const response = await chart6Data(this.checkPoint);  // 传递 checkPoint 给后端
        this.chartData = response;
        this.renderChart();
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    },
    renderChart() {
      // 获取 DOM 容器并初始化 ECharts 实例
      const chart = echarts.init(document.getElementById('chart6'));

      // 配置图表选项
      const option = {
        title: {
          text: `{title| ${this.checkPoint}车辆类型分布}`,
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
        legend: {
          orient: 'horizontal',
          left: 'center',
          top: '10%',
          type: 'scroll',
          width: '80%'
        },
        series: [
          {
            name: '车辆类型',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '60%'],
            data: this.chartData,
            padAngle: 3,
            minAngle: 2,
            itemStyle: {
              borderRadius: 10
            },
            label: {
              show: false,
              position: 'center'
            },
            labelLine: {
              show: false
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              },
              label: {
                show: true,
                fontSize: 30,
                fontWeight: 'bold'
              }
            }
          }
        ]
      };

      chart.setOption(option);
    }
  }
};
</script>

<style scoped>
#chart6 {
  width: 100%;
  height: 100%;
}
</style>
