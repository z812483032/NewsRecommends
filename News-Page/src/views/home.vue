<template>
  <div :height="this.screenHeight">
<!--    <Scroll :height="this.screenHeight" :width="this.screenWidth">-->
    <HeaderMenu :activename='2' :userImg="imgs"></HeaderMenu>
    <HeaderPicture></HeaderPicture>
    <ContentPage></ContentPage>
    <footer>
      <div style="text-align: center; background: #656565">
        <span style="color: white">Copyright © 2021 News| 京ICP备xxxxxxx号-1 </span>
      </div>
    </footer>
<!--    </Scroll>-->
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu";
import HeaderPicture from "../components/HeaderPicture";
import ContentPage from "../components/ContentPage";
export default {
  name: "home",
  created() {
    let token = sessionStorage.getItem('token')
    this.openFullScreen()
    // console.log(token)
    if(token === null || token ===''){
      this.$router.push({ name: 'login' })
      this.$Message.info('请登录！！')
    }

    this.imgs = sessionStorage.getItem('userImg');
    // console.log(this.imgs);
  },
  components: {ContentPage, HeaderPicture, HeaderMenu},
  mounted() {
    window.onresize = () => {
      this.screenHeight = document.body.clientHeight
    }
  },
  methods: {
    openFullScreen() {
      const loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading',
        background: 'rgba(45,45,45,0.7)'
      });
      setTimeout(() => {
        loading.close();
      }, 500);
    },
  },
  data() {

    return {
      activename: 1,
      screenHeight: document.body.clientHeight ,
      screenWidth: document.body.clientWidth,
      // imgs: JSON.parse(localStorage.getItem('userImg'))
      imgs: '',
    }
  }
}
</script>

<style scoped>



</style>
