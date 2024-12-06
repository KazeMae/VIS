<template>
  <div class="timeline">
    <div v-for="(year, index) in allYears" :key="index" class="timeline-year">
      <label :for="'year' + year" class="timeline-label">
        <input
            type="checkbox"
            :id="'year' + year"
            v-model="selectedYears"
            :value="year"
            class="checkbox-input"
            @change="updateSelectedYears"
        />
        <span class="timeline-text">{{ year }}</span>
      </label>
    </div>
  </div>
</template>

<script>
import {getTimeLine} from "@/api/api";
import {mapState, mapMutations} from 'vuex';

export default {
  name: 'TimeLine',
  data() {

    return {
      allYears: [],
      selectedYears: []
    };
  },
  computed: {
    ...mapState({
      years: state => state.years  // 从 Vuex 获取年份
    })
  },
  watch: {
    selectedYears: function (newYears) {
      this.updateSelectedYears(newYears);  // 监听 selectedYears 的变化
    }
  },
  mounted() {
    // 获取所有年份数据
    this.fetchTimelineData();
    this.selectedYears = [...this.years];
  },
  methods: {
    ...mapMutations(['setYears']),  // 引入 setYears mutation
    updateSelectedYears() {
      this.setYears(this.selectedYears);  // 更新 Vuex store 中的 years
    },
    // 获取所有年份
    async fetchTimelineData() {
      try {
        const resp = await getTimeLine()
        this.allYears = resp.years
      } catch (error) {
        console.error('Error fetching timeline data:', error);
      }
    },
  }
};
</script>

<style scoped>
.timeline {
  display: flex;
  position: relative;
  justify-content: space-around;
  list-style-type: none;
  padding: 0;

  .timeline-year {
    position: relative;
  }

  .timeline-label {
    cursor: pointer;
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-items: center;

    span {
      color: #abb0b3;
      font-size: 1vw;
    }

    input[type="checkbox"] {
      -webkit-appearance: none;
      vertical-align: middle;
      margin-top: 0;
      background: #fafeff;
      border: #e8edf0 solid 0.7vw;
      border-radius: 50%;
      min-height: 2vw;
      min-width: 2vw;
      position: relative;
      cursor: pointer;
      transition-duration: .3s;
    }

    input[type="checkbox"]:checked {
      background: #8aacda;
      border: #4b69b3 solid 0.4vw;
    }

  }
}

.timeline::before {
  content: '';
  position: absolute;
  top: 1vw;
  left: 0;
  right: 0;
  height: 0.185vw;
  background-color: #e9eef2;
  z-index: -1;
}

</style>
