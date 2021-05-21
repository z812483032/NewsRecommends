<template>
  <div>
    <el-menu style="text-align: center" background-color="" :default-active="this.category" class="el-menu-demo" mode="horizontal">
      <el-menu-item index="0" class="menuitem">
        <router-link to="/allnews">
          <Icon type="ios-book" size="20"/>全部
        </router-link>
      </el-menu-item>
      <el-menu-item index="1" class="menuitem">
        <router-link to="/domesticnews/1">
          <Icon type="md-home" size="20"/>国内
        </router-link>
      </el-menu-item>
      <el-menu-item index="2" class="menuitem">
        <router-link to="/domesticnews/2">
          <Icon type="ios-planet" size="20"/>国际
        </router-link>
      </el-menu-item>
      <el-menu-item index="3" class="menuitem">
        <router-link to="/domesticnews/3">
          <Icon type="md-people" size="20"/>社会
        </router-link>
      </el-menu-item>
      <el-menu-item index="5" class="menuitem">
        <router-link to="/domesticnews/4">
          <Icon type="md-basketball" size="20"/>体育
        </router-link>
      </el-menu-item>
      <el-menu-item index="4" class="menuitem">
        <router-link to="/domesticnews/5">
          <Icon type="md-headset" size="20"/>娱乐
        </router-link>
      </el-menu-item>
      <el-menu-item index="6" class="menuitem">
        <router-link to="/domesticnews/6">
          <Icon type="ios-jet" size="20"/>军事
        </router-link>
      </el-menu-item>
      <el-menu-item index="7" class="menuitem">
        <router-link to="/domesticnews/7">
          <Icon type="ios-ionitron" size="20"/>科技
        </router-link>
      </el-menu-item>
      <el-menu-item index="8" class="menuitem">
        <router-link to="/domesticnews/8">
          <Icon type="md-pulse" size="20"/>财经
        </router-link>
      </el-menu-item>
      <el-menu-item index="9" class="menuitem">
        <router-link to="/domesticnews/9">
          <Icon type="ios-trending-up" size="20"/>股市
        </router-link>
      </el-menu-item>
      <el-menu-item index="10" class="menuitem">
        <router-link to="/domesticnews/10">
          <Icon type="md-cash" size="20"/>美股
        </router-link>
      </el-menu-item>
    </el-menu>
    <router-view  :key="$route.name + ($route.params.id || '')"></router-view>
  </div>
</template>

<script>
export default {
  name: "ContentPage",
  data() {
    return {
      category: '1',
    }
  },
  created() {
    if (this.$route.params.id === undefined)
      this.category='0'
    else
     this.category=this.$route.params.id
  }
}
</script>

<style scoped>
.menuitem {
  width: 9%;
  font-size: 20px;
  text-align: center;
}


</style>
