<template>
  <div id="app">
    <router-view></router-view>
    <el-backtop style="background-color: #f2f5f6;
        box-shadow: 0 0 6px rgba(0,0,0, .12);"></el-backtop>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
body {
  min-width:1200px;
  overflow: scroll;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
li, ul, p, div, body, html, table {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html, body {
  height: 100%;
}
li {
  list-style: none;
}
#app {
  height: 100%;
}
</style>
