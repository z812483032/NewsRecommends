<template>
  <Col span="5" >
    <div  class="bjdiv" >
      <h3  style="margin-top: 20px; margin-left: 50px; font-size: 20px;" >浏览记录</h3>
      <Timeline v-show="show3"  v-for="(item, index) in this.historylist.slice(0,10)" :key="'his-'+index" style="margin-top: 20px; margin-left: 30px;cursor: pointer;color: #181818">
        <TimelineItem @click.native="toNewsPage(item.newsid)" >
          <p class="time" style="font-size:18px; font-weight: bold">{{ item.title }}</p>
          <p class="content" >{{ item.time }}</p>
        </TimelineItem>
      </Timeline>
    </div>

  </Col>
</template>

<script>
import {getUserHistory} from '@/api'
export default {
  name: "History",
  data() {
    return{
      show3: true,
      test: 'aaaaa',
      historylist:[],
    }
  },
  created() {
    if (sessionStorage.getItem('userId') !== null)
      getUserHistory(sessionStorage.getItem('userId')).then(res => {
      // console.log('history', res.newslist['1'])
      // for (let i = 0; i < res.newslist.length; i++){
      //   let news = res.newslist[i]
      //   let data = {
      //     'newsid' : news.newsid,
      //     'title' : res.newslist[news].title.slice(0,10) + '...',
      //     'time' : res.newslist[news].time,
      //   }
      //   console.log('id:', news )
      //   this.historylist.push(data)
      // }
      for(let news in res.newslist){
        let data = {
          'title' : news.slice(0,13) + '...',
          'newsid' : res.newslist[news].newsid,
          'time' : res.newslist[news].time,
        }
        // console.log('id:', news )
        this.historylist.push(data)
        // res.newslist[news]
      }
    })
    // console.log(this.historylist)
  },
  methods: {
    toNewsPage(newsid){
      this.$router.push('/newspage/'+newsid)
    }
  }
}
</script>

<style scoped>
.bjdiv{
  background:transparent;
  color:#fff;
  background-color:rgba(28,49,78,0.25);
  border-radius: 20px;
}
.banner_bg{
  width:100%;
  background-repeat:no-repeat;
  background-size:cover;
  -webkit-filter:blur(15px);
  -moz-filter:blur(15px);
  -o-filter:blur(15px);
  -ms-filter:blur(15px);
  filter:blur(15px);
  position:absolute;
  left:0;
  top:0;
}
</style>
