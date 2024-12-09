<!--地区选择-->
<template>
  <div class="choose-area">
    <select v-model="area" class="area-select">
      <option v-for="a in allAreas" :key="a" :value="a">{{ a }}</option>
    </select>
  </div>
</template>

<script>

import {getArea} from "@/api/api";
import {mapState} from "vuex";

export default {
  name: "ChooseArea",
  data() {
    return {
      allAreas: []
    }
  },
  computed: {
    ...mapState({
      area: state => state.area,  // 从 Vuex 获取 area
    }),
    area: {
      get() {
        return this.$store.state.area;
      },
      set(value) {
        this.$store.commit("setArea", value);
      }
    }
  },
  mounted() {
    this.fetchAreaData()
  },
  methods: {
    async fetchAreaData() {
      try {
        const resp = await getArea()
        this.allAreas = resp.areas
      } catch (error) {
        console.error('Error fetching area data:', error);
      }
    },
  },
}

</script>

<style scoped>
.area-select {
  border: none;
  border-radius: 0.463vw;
  padding: .6vw !important;
  user-select: none;
  font-size: .9vw;
  box-shadow: 0 0.463vw 0.926vw rgba(204, 204, 204, 0.35);
}
</style>