import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    area: '东昌府区',
    years: [2020],
    checkPoint: '黄河10'
  },
  mutations: {
    setArea(state, area) {
      state.area = area;
    },
    setYears(state, years) {
      state.years = years;
    },
    setCheckPoint(state, checkPoint) {
      state.checkPoint = checkPoint;
    }
  },
  getters: {
    getYears: (state) => state.years,
    getArea: (state) => state.area,
    getCheckPoint: (state) => state.checkPoint
  }
});