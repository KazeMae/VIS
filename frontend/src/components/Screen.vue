<template>
  <div class="screen">
    <div class="title">
      <div class="title-left">{{ title }}</div>
      <div class="title-right">
        <span v-for="(item, index) in auth" :key="index">{{ item }}</span>
        <button @click="goBack">复位</button> <!-- 添加按钮，并绑定点击事件 -->
      </div>
    </div>
    <div class="container">
      <div class="left">
        <div class="left-top">
          <div class="top-left">
            <div class="chart">
              <chart-one :year="selectedYear"/>
            </div>
            <div class="chart">
              <chart-two/>
            </div>
          </div>
          <div class="top-right">
            <div class="main-left">
              <div class="top">
                <choose-area/>
              </div>
              <div class="bottom">
                <div class="chart">
                  <chart-eleven/>
                </div>
              </div>
            </div>
            <div class="main-right">
              <time-line :selectedYear="selectedYear" @update-year="updateYear"/>
              <map-item/>
            </div>
          </div>
        </div>
        <div class="left-bottom">
          <div class="bottom-left">
            <div class="chart">
              <chart-three/>
            </div>
          </div>
          <div class="bottom-right">
            <div class="chart">
              <chart-four/>
            </div>
          </div>
        </div>
      </div>
      <div class="right">
        <div class="right-top">
          <div class="chart">
            <chart-five/>
          </div>
        </div>
        <div class="right-bottom">
          <div class="chart">
            <chart-six/>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import ChartOne from "@/components/ChartOne.vue";
import ChartTwo from "@/components/ChartTwo.vue";
import ChartThree from "@/components/ChartThree.vue";
import ChartFour from "@/components/ChartFour.vue";
import ChartFive from "@/components/ChartFive.vue";
import ChartSix from "@/components/ChartSix.vue";
import TimeLine from "@/components/TimeLine.vue";
import ChooseArea from "@/components/ChooseArea.vue";
import ChartEleven from "@/components/ChartEleven.vue";
import MapItem from "@/components/Map.vue";

export default {
  name: 'ScreenPage',
  components: {
    MapItem,
    ChartEleven, ChooseArea, TimeLine, ChartSix, ChartFive, ChartFour, ChartThree, ChartTwo, ChartOne
  },
  data() {
    return {
      title: '大气污染可视化平台',
      // auth: ['name', 'name', 'name', 'name', 'name', 'name'],
      selectedYear: 2020,
    }
  },
  methods: {
    updateYear(newYear) {
      this.selectedYear = newYear; // 更新选中的年份
    },
    goBack() {
      location.reload();
    }
  }
}
</script>

<style scoped>
@font-face {
  font-family: "hyxbsh";
  src: url("@/assets/fonts/hyxbsh.ttf");
}

.screen {
  width: 100vw;
  height: 100vh;
}

.title {
  width: 100vw;
  height: 8%;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .title-left {
    flex: 1;
    text-align: center;
    font-size: 2vw;
    font-weight: bold;
    color: #247bc7;
    letter-spacing: 0.278vw;
    font-family: 'hyxbsh', serif
  }

  .title-right {
    width: 12%;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5vw;
    justify-content: center;;
    font-size: 1vw;
    font-weight: normal;
    color: #247bc7;
    letter-spacing: 0.093vw;
    font-family: 'hyxbsh', serif
  }

  .title-right span {
    padding: 0.463vw;
    white-space: normal;
    word-wrap: break-word;
  }
  .title-right button {
    background-color: #f5fafd;
    color: #333;
    border: none;
    padding: 0.463vw 0.926vw;
    border-radius: 0.2315vw;
    cursor: pointer;
    font-size: 1vw;
    font-family: 'hyxbsh', serif;
    margin-left: 0.463vw;
    transition: background-color 0.3s ease;
  }

  .title-right button:hover {
    background-color: #e0e0e0;
  }

}


.container {
  width: 100vw;
  height: 92%;
  margin-bottom: 1.389vw;
  display: flex;
  flex-direction: row;
  justify-content: space-around;

  .left {
    width: 72%;
    height: 100%;
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;


    .left-top {
      width: 100%;
      height: 60%;
      display: flex;
      flex-direction: row;
      justify-content: space-between;

      .top-left {
        width: 32%;
        height: 100%;

        display: flex;
        flex-direction: column;
        flex-wrap: nowrap;
        justify-content: space-evenly;

        .chart {
          width: 100%;
          height: 46%;
        }


      }

      .top-right {
        width: 66%;
        height: 100%;
        display: flex;


        .main-left {
          width: 30%;
          height: 100%;
          display: flex;
          flex-direction: column;
          flex-wrap: nowrap;
          justify-content: space-evenly;

          .top, .bottom {
            width: 100%;
            height: 46%;

            .chart {
              width: 100%;
              height: 100%;
            }
          }

        }

        .main-right {
          width: 70%;
          height: 100%;

          .timeline {
            width: 100%;
            height: 15%;
          }

          .map {
            width: 100%;
            height: 85%;
          }

        }

      }

    }

    .left-bottom {
      width: 100%;
      height: 38%;

      display: flex;
      justify-content: space-between;

      .bottom-left, .bottom-right {
        width: 49%;
        height: 100%;

        .chart {
          width: 100%;
          height: 100%;
        }

      }


    }

  }

  .right {
    width: 25%;
    height: 100%;
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    justify-content: space-around;

    .right-top, .right-bottom {
      width: 100%;
      height: 48%;

      .chart {
        width: 100%;
        height: 98%;
      }
    }


  }

  .chart {
    border-radius: 0.463vw;
    background-color: #fff;
    box-shadow: 0 0.463vw 0.926vw rgba(204, 204, 204, 0.35);
  }

}
</style>
