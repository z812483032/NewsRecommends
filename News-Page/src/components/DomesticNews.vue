<template>
  <Row style="background:url('https://www.hualigs.cn/image/60821cdb3c769.jpg');background-attachment: fixed;">
    <Col span="4" ></Col>
    <Col span="12" style=" height: auto; padding: 10px">
      <Card :bordered="false" class="newsitem" v-for="(item, index) in this.newslist.slice(0,a)" :key="'news'+index"
            :to="'/newspage/'+ item.newsid" style="border-radius: 12px;">
        <p slot="title" style="font-weight: 700;font-size: larger;">{{ item.title }}</p>
        <Row :lg="24" v-if="item.pic_url !== null">
          <Col :lg="9" style="text-align: center">
            <img class="images" style="width: 200px; " alt :onerror="defaultImg" :src="item.pic_url">
          </Col>
          <Col :lg="1"></Col>
          <Col :lg="14" style="color: #181818">
            {{ item.mainpage }}
          </Col>
        </Row>
        <Row :lg="24" v-if="item.pic_url === null">
          <Col :lg="1"></Col>
          <Col :lg="22"><p style="color: #181818">{{ item.mainpage }}</p></Col>
          <Col :lg="1"></Col>
        </Row>
        <Row style="margin-top: 10px; color: #a8a8a8">
          <Col :lg="1"></Col>
          <Col :lg="5">
            <Icon size="20" type="ios-people"/>
            {{ item.readnum }} &nbsp;&nbsp;
            <Icon size="18" type="ios-megaphone-outline"/>
            {{ item.comments }}
          </Col>
          <Col :lg="11"></Col>
          <Col :lg="6" style="text-align: right;">
            <div>{{ item.date }}</div>
          </Col>
        </Row>
      </Card>
      <div align="center">
        <div class="load-more mr-bottom" v-if="a<this.newslist.length" @click='loadMore'
             style="text-align: center;margin-top: 20px;cursor: pointer;" v-show="spinShow" >点击加载更多
        </div>
        <div class="load-more" v-else style="text-align: center;margin-top: 20px;cursor: pointer;" v-show="spinShow">没有更多了</div>
      </div>
    </Col>
    <History></History>
  </Row>
</template>

<script>
import {getTypeNewsDetail} from '@/api'
import History from "./History";
export default {
  name: "DomesticNews",
  components: {History},
  computed: {
    defaultImg () {
      return 'this.src="' + require('@/assets/imgs/404.jpg') + '"'
    }
  },
  data() {
    return {
      spinShow: false,
      a:6,
      newslist: [],
    }
  },
  methods: {
    loadMore:function(){
      this.a+=6;
    }
  },
  created() {
    this.$Loading.start()
    getTypeNewsDetail(this.$route.params.id).then(res => {
      let newslist = eval(res.newslist)
      // console.log('newslist:', newslist)
      for (let i = 0; i < newslist.length; i++) {
        let detail = eval(newslist[i])[0]
        if(undefined === detail)
          continue
        // console.log(detail)
        let id = detail.pk
        let title = detail.fields.title
        let pic_url = null
        if (detail.fields.pic_url !== '[]')
          pic_url = eval(detail.fields.pic_url)[0]
        let mainpage = ''
        // console.log('length:', newslist[i].fields.mainpage.length)
        if (detail.fields.mainpage.length > 101)
          mainpage = detail.fields.mainpage.slice(0, 100) + '...'
        else
          mainpage = detail.fields.mainpage
        let date = detail.fields.date
        let readnum = detail.fields.readnum
        let comments = detail.fields.comments
        let data = {
          'newsid': id,
          'title': title,
          'pic_url': pic_url,
          'mainpage': mainpage,
          'date': date,
          'readnum': readnum,
          'comments': comments,
        }
        this.newslist.push(data)
        // console.log(this.newslist)
      }
    })
    this.$Loading.finish()
    this.spinShow = true
  },
}
</script>

<style scoped>
.images{
  width: 100px;
  height: 80px;
  object-fit: cover;
}
.load-more{
  width: 200px;
  border-radius: 50px;
  background: linear-gradient(45deg, #c2e7e8, #a3c2c3);

  font-weight: bold;
  font-size: 19px;
}
.load-more:hover{
  width: 200px;
  border-radius: 50px;
  background: #e0e0e0;
  background: linear-gradient(45deg, #a3c2c3, #c2e7e8);

}
.newsitem {
  margin-top: 10px;
}
</style>
