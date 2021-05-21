<template>
  <div class="home-main" style="background: url('https://ae01.alicdn.com/kf/Ue1cf333248e943a185ce61da03bde50eS.jpg'); background-attachment: fixed;">
      <HeaderMenu activename="4"></HeaderMenu>
    <Row>
      <Col span="4" ></Col>
      <Col span="12" style="height: auto; padding: 10px; cursor: pointer;">
        <Card :bordered="false" class="newsitem" v-for="(item, index) in this.newslist.slice(0,a)"
              :key="'news'+index" :to="'/newspage/'+ item.newsid" style="border-radius: 12px;">
          <p slot="title" style="font-weight: 700;font-size: larger;">{{ item.title }}</p>
          <Row :lg="24" v-if="item.pic_url !== null">
            <Col :lg="9" style="text-align: center">
              <img class="images" style="width: 210px;height: 120px;" :src="item.pic_url">
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
            <Col :lg="24" style="text-align: right;">
              <div>{{item.date}}</div>
            </Col>
          </Row>
          <Row>
            <Col :lg="7" style="color: #a8a8a8" ><Icon size="20" type="ios-people" />{{item.readnum}} &nbsp;&nbsp; <Icon size="18" type="ios-megaphone-outline" />{{item.comments}}</Col>
            <Col :lg="17" style="text-align: right; color: red;font-weight: bold"><Icon size="22" type="md-bonfire" />{{ item.hotvalue }}</Col>
          </Row>
        </Card>
        <div align="center">
          <div class="load-more mr-bottom"  v-if="a<this.newslist.length"  @click='loadMore'
               style="text-align: center;margin-top: 20px;cursor: pointer;">点击加载更多
          </div>
          <div class="load-more" v-else style="text-align: center;margin-top: 20px;cursor: pointer;">没有更多了</div>
        </div>
      </Col>
      <History></History>
    </Row>
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu";
import History from "../components/History";
import {getHotSpot} from '@/api'
export default {
  name: "CurrentEventHotSpot",
  components: { HeaderMenu, History },
  data() {
    return{
      active : 1,
      screenHeight: document.body.clientHeight,
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
    getHotSpot(sessionStorage.getItem('userId')).then(res => {
      let newslist = eval(res.newslist)
      // console.log(newslist)
      for (let i = 0; i < newslist.length; i++) {let id = newslist[i].newsid
        let title = newslist[i].title
        let pic_url = null
        if (newslist[i].pic_url !== '[]')
          pic_url = eval(newslist[i].pic_url)[0]
        let mainpage = ''
        // console.log('length:', newslist[i].fields.mainpage.length)
        if (newslist[i].mainpage.length > 101)
          mainpage = newslist[i].mainpage.slice(0, 100) + '...'
        else
          mainpage = newslist[i].mainpage
        let date = newslist[i].date
        let readnum = newslist[i].readnum
        let comments = newslist[i].comments
        let hotvalue = newslist[i].hotvalue
        let data = {
          'newsid': id,
          'title': title,
          'pic_url': pic_url,
          'mainpage': mainpage,
          'date': date,
          'readnum': readnum,
          'comments': comments,
          'hotvalue': hotvalue,
        }
        this.newslist.push(data)
      }
    })
  },
}
</script>

<style scoped>
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
.images{
  width: 100px;
  height: 120px;
  object-fit: cover;
}
</style>
