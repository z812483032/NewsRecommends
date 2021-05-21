<template>
  <el-carousel :interval="8000" type="card" height="400px" style="vertical-align: auto;">
    <el-carousel-item v-for="(item, index) in newsdetail"  :key="'info2-'+index" :label="item.title" >
      <img class="carouselpic" ref="bannerHeight" alt="" :onerror="defaultImg" :src="item.pic_url" @click="toNewsDetail(item.newsid)">
    </el-carousel-item>
  </el-carousel>
</template>

<script>
import {getPicture} from '@/api'
export default {
  name: "HeaderPicture",
  computed: {
    defaultImg () {
      return 'this.src="' + require('@/assets/imgs/404.jpg') + '"'
    }
  },
  created() {
    getPicture().then(res => {
      this.$Loading.start()
      // console.log('res', res)
      this.newsdetail = res.message
      this.$Loading.finish()
    })
  },
  data() {
    return {
      newsdetail: '',
      value2: 0,
    }
  },
  methods: {
    toNewsDetail(newsid) {
      // console.log(newsid)
      this.$router.push({path:'/newspage/'+newsid})
    }
  }
}
</script>

<style scoped>
.carouselpic{
  position: absolute;
  width: 100%;
}
.el-carousel__item h3 {
  position: absolute;
  color: #cbcfd7;
  font-size: 14px;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #ffffff;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #ffffff;
}
.imgaes {
  position: fixed;
  text-align: center;
  vert-align: middle;
  width: 100%;
  height: 100%;
}
.pic_item h2 {
  position: absolute;
  color: #ffffff;
  /*bottom:2rem;*/
}
</style>
