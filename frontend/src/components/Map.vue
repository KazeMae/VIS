<template>
  <div>
    <loading
        v-if="isLoading"
        :active="isLoading"
        loader="bars"
        :color="'#3498db'"
        :is-full-page="true"
        class="loading-item"
    />
    <div id="map"></div>
  </div>
</template>

<script>
import {getMapData} from "@/api/api";
import * as echarts from 'echarts'
import mapData from '@/assets/map/聊城市.json'
import {mapState} from "vuex";
import Loading from 'vue-loading-overlay';

export default {
  name: 'MapItem',
  data() {
    return {
      chartData: null,
      chart: null,
      isLoading: false,  // 控制加载动画显示
    }
  },
  components: {
    Loading
  },
  computed: {
    ...mapState({
      checkPoint: state => state.checkPoint,
    }),
    checkPoint: {
      get() {
        return this.$store.state.checkPoint;
      },
      set(value) {
        this.$store.commit("setCheckPoint", value);
      }
    }
  },
  mounted() {
    this.chart = echarts.init(document.getElementById('map'));
    this.fetchChartData();
  },
  methods: {
    async fetchChartData() {
      this.isLoading = true;
      try {
        const response = await getMapData();
        this.chartData = response;  // 获取到的数据
        // 调用渲染图表的方法
        this.renderChart();
      } catch (error) {
        console.error('Error fetching chart data:', error);
      } finally {
        this.isLoading = false;  // 加载完成后隐藏加载动画
      }
    },
    renderChart() {
      if (this.chartData) {
        echarts.registerMap('liaocheng', mapData);
        const points = this.chartData.map(function (item) {
          return [item.longitude, item.latitude];
        });
        const option = {
          title: {
            show: false
          },
          tooltip: {
            trigger: 'item',
            formatter: function (params) {
              return params.marker + params.name + '<br>' + '过往车辆：' + params.value[2];
            },
          },
          geo: {
            type: 'map',
            map: 'liaocheng',
            roam: true,
            zoom: 1.5,
            label: {show: true},
            itemStyle: {
              areaColor: '#f3f3f3',
              borderColor: '#999'
            },
            emphasis: {
              itemStyle: {
                areaColor: '#247bc7',
              },
              label: {
                color: '#fff'
              }
            }
          },
          series: [{
            name: '站点',
            type: 'effectScatter', // 修改为涟漪散点图
            coordinateSystem: 'geo', // 使用地理坐标系
            data: points.map((point, index) => {
              const checkpointName = this.chartData[index].checkpoint_name;
              const totalVehicleCount = this.chartData[index].total_vehicle_count;
              return {
                name: checkpointName,
                value: [...point, totalVehicleCount], // 将值加入坐标点
              };
            }),
            showEffectOn: 'render',
            rippleEffect: {
              brushType: 'stroke'
            },
            label: {
              show: false
            },
            itemStyle: {
              color: '#ff7f50', // 散点颜色
              shadowBlur: 10,
              shadowColor: '#333'
            },
          }]
        };
        this.chart.setOption(option);
        this.chart.on('click', (params) => {
          if (params.componentType === 'series' && params.componentSubType === 'effectScatter') {
            this.checkPoint = params.name;
          }
        });
      }
    },
  }
}
</script>

<style>
#map {
  position: absolute;
  width: 30%;
  height: 25vw;
  top: 5vw;
  left: 40vw;
}

.loading-item {
  position: absolute;
  width: 100vw;
  height: 100vh;
  left: 0;
  top: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(240, 248, 255, 0.46);
}
</style>