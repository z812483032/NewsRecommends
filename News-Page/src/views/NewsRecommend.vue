<template>
  <div class="home-main" style="background: url('https://ae01.alicdn.com/kf/Uaef3584e1df843bcab561b344d38f6e73.jpg'); background-attachment: fixed;" >
<!--    <Scroll :height="this.screenHeight">-->
      <HeaderMenu activename="3"></HeaderMenu>
      <Row>
        <Col span="4"></Col>
        <Col span="12" style="height: auto; padding: 10px; cursor: pointer;">
          <Card :bordered="false" class="newsitem" v-for="(item, index) in this.newslist.slice(0,a)" :key="'news'+index"
               @click.native="updRec(item.newsid)" style="border-radius: 12px;">
            <p slot="title" style="font-weight: 700;font-size: larger;">{{ item.title }}</p>
            <Row :lg="24" v-if="item.pic_url !== null">
              <Col :lg="9" style="text-align: center">
                <img class="images" style="width: 210px;height: 110px;" :src="item.pic_url">
              </Col>
              <Col :lg="1"></Col>
              <Col :lg="14">
                {{ item.mainpage }}
              </Col>
            </Row>
            <Row :lg="24" v-if="item.pic_url === null">
              <Col :lg="1"></Col>
              <Col :lg="22"><p>{{ item.mainpage }}</p></Col>
              <Col :lg="1"></Col>
            </Row>
            <Row style="margin-top: 10px;">
              <Col :lg="24" style="text-align: right;">
                <div>{{item.date}}</div>
              </Col>
            </Row>
            <Row>
              <Col :lg="7" style="color: #a8a8a8" ><Icon size="20" type="ios-people" />{{item.readnum}} &nbsp;&nbsp; <Icon size="18" type="ios-megaphone-outline" />{{item.comments}}</Col>
              <Col :lg="17" style="text-align: right;">推荐By：{{ item.species }}</Col>
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
<!--    </Scroll>-->
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu";
import History from "../components/History";
import { getRecNewsDetail, updateRec } from '@/api'
export default {
  name: "NewsRecommend",
  components: {History, HeaderMenu},
  data() {
    return{
      active : 1,
      screenHeight: document.body.clientHeight,
      a:6,
      newslist: [],
    }
  },
  methods: {
    openFullScreen() {
      const loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading',
        background: 'rgba(255,255,255,0.7)'
      });
      setTimeout(() => {
        loading.close();
        this.$Message.info("更多的阅读，能带来更加准确的推荐喔！！！");
      }, 1000);
    },
    updRec (newsid){
      updateRec(newsid, sessionStorage.getItem('userId'), newsid)
      this.$router.push('/newspage/'+newsid)
    },
    loadMore:function(){
      this.a+=6;
    }
  },
  created() {
    this.openFullScreen()
    getRecNewsDetail(sessionStorage.getItem('userId')).then(res => {
      let newslist = eval(res.newslist)
      // console.log(newslist)
      for (let i = 0; i < newslist.length; i++) {
        let id = newslist[i].newsid
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
        let species = newslist[i].species
        switch (species){
          case 0:
            species = '兴趣'
            break
          case 1:
            species = '地区'
            break
          case 2:
            species = '热点'
            break
        }
        let data = {
          'newsid': id,
          'title': title,
          'pic_url': pic_url,
          'mainpage': mainpage,
          'date': date,
          'species': species,
          'readnum': readnum,
          'comments': comments,
        }
        this.newslist.push(data)
        // console.log(this.newslist)
      }
    })

  }
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
