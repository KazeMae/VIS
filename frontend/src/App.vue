<template>
  <div id="app">
    <Screen/>
  </div>
</template>

<script>
import Screen from './components/Screen.vue'

export default {
  name: 'App',
  components: {
    Screen
  }
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
  background-color: #f5fafd;
}

#app {
  * {
    margin: 0;
    padding: 0;
  }

}
</style>
