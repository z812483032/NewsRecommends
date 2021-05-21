<template>
  <div class="mian-page">
    <HeaderMenu class="headmenu" :activename="7"></HeaderMenu>
    <div class="middle-page">
        <Row :height="screenHeight">
          <Col :md="3"></Col>
          <Col :md="18">
            <Row style="margin-top: 10px;">
              <Col id="anchor1">
                <a :href="'/domesticnews/'+this.category">{{ this.sort }}</a> &nbsp; > &nbsp; 正文
              </Col>
            </Row>
            <Row style="margin-top: 15px;">
              <h1 style="font-size: xxx-large">{{ this.title }}</h1>
            </Row>
            <Row style="float: right;vertical-align: middle;">
              感兴趣：
              <Rate  @on-change="upGivelike(1)"   v-model="value" :count="1" icon="ios-thumbs-up" :clearable="true" style="margin-top: -10px; font-size: 25px;"/>
<!--              <Rate v-else  v-model="value" @on-change="upGivelike" :count="1" icon="ios-thumbs-up" :clearable="true" style="margin-top: -10px; font-size: 25px;"/>-->
              不感兴趣：
<!--              <Rate @on-change="upGivelike" disabled v-model="value"  :count="1" icon="ios-thumbs-down" :clearable="true" style="margin-top: -10px; font-size: 25px"/>-->
              <Rate  @on-change="upGivelike(0)"  v-model="value1"  :count="1" icon="ios-thumbs-down" :clearable="true" style="margin-top: -10px; font-size: 25px"/>
<!--              <Rate v-else  v-model="value1" @on-change="upGivelike"  :count="1" icon="ios-thumbs-down" :clearable="true" style="margin-top: -10px; font-size: 25px"/>-->

              阅读量：<a style="color: #bbbbbb; margin-right: 20px;" >{{ this.readnum }}</a>
              评论：<a style="color: #bbbbbb; margin-right: 20px;" @click="toComments">{{ this.comments }}</a>
              <p style="color: #bbbbbb; margin-right: 20px;">发表时间：{{ this.date }}</p>
            </Row>
            <Divider v-if="this.pic_url !== '[]'"></Divider>
            <Row style="font-size: large">
                <div v-for="(item,index) in this.pic_url" :key="'pic-'+index"  style="margin: auto;">
                <img width="500px" style=""  class="pict"  :src="item" alt
                        :onerror="defaultImg">
                </div>
              <Row>
                  <div class="mainpage" >
                    <p class="pageitem" v-for="(item,index) in this.origin" :key="'info2-'+index">{{ item }}</p>
                  </div>
              </Row>
              <Divider></Divider>
              <Card style="height: 620px;width: 800px; margin: auto;"
                     v-if="videoshow">
<!--                v-if="this.playerOptions.sources[0].src !== 'None'"-->
                <video-player class="video-player vjs-custom-skin"
                              ref="videoPlayer"
                              :playsinline="true"
                              :options="playerOptions" v-if="videoshow">
                </video-player>
              </Card>
              <Divider>为你推荐</Divider>
              <Row></Row>
            </Row>
            <Row v-if="this.recsimilarlist.length !== 0">
              <Col :lg="12">
                <Carousel radius-dot dots="outside" autoplay :autoplay-speed="9000" v-model="Carouselvalue1" loop  >
                  <CarouselItem v-for="(item, index) in this.recsimilarlist" :key="'recsim-'+index" >
                    <Card v-if="item.pic_url === ''" style="height: 300px; width: 500px; margin: auto;cursor: pointer;" @click.native="toNewsDetail(item.newsid)">
                      <p slot="title" >{{item.title}}</p>
                      <p>
                        {{item.mainpage}}
                      </p>
                    </Card>
                    <div v-if="item.pic_url !== ''" style="text-align: center; cursor: pointer;" class="pic_item">
                      <img :src="item.pic_url[0]" class="images" @click="toNewsDetail(item.newsid)">
                      <h2 >{{ item.title.slice(0,20) }}</h2>
                    </div>
                  </CarouselItem>
                </Carousel>
              </Col>
              <Col :lg="12">
                <Carousel radius-dot dots="outside"  loop autoplay :autoplay-speed="10000" v-model="Carouselvalue2" loop >
                  <CarouselItem  v-for="(item, index) in this.rechotlist" :key="'rechot-'+index">
                    <Card v-if="item.pic_url === ''" style="height: 300px; width: 500px; margin: auto;cursor: pointer;" @click.native="toNewsDetail(item.newsid)">
                      <p slot="title">{{item.title}}</p>
                      <p>
                        {{item.mainpage}}
                      </p>
                    </Card>
                    <div v-if="item.pic_url !== ''" style="text-align: center;cursor: pointer;" class="pic_item">
                      <img style="object-fit: contain;" :src="item.pic_url[0]" class="images" @click="toNewsDetail(item.newsid)">
                      <h2 >{{ item.title.slice(0,20) }}</h2>
                    </div>
                  </CarouselItem>
                </Carousel>
              </Col>
            </Row>
            <Row v-if="this.recsimilarlist.length === 0" >
              <Col :lg="6"></Col>
              <Col :lg="12">
                <Carousel radius-dot dots="outside"  loop autoplay :autoplay-speed="9000" v-model="Carouselvalue2" loop >
                  <CarouselItem  v-for="(item, index) in this.rechotlist" :key="'rechot-'+index">
                    <Card v-if="item.pic_url === ''" style="height: 300px; width: 500px; margin: auto;cursor: pointer;" @click.native="toNewsDetail(item.newsid)">
                      <p slot="title">{{item.title}}</p>
                      <p>
                        {{item.mainpage}}
                      </p>
                    </Card>
                    <div v-if="item.pic_url !== ''" style="text-align: center;cursor: pointer;" class="pic_item">
                      <img :src="item.pic_url[0]" class="images" @click="toNewsDetail(item.newsid)">
                      <h2 >{{ item.title.slice(0,20) }}</h2>
                    </div>
                  </CarouselItem>
                </Carousel>
              </Col>
              <Col :lg="6"></Col>
            </Row>
            <Divider></Divider>
            <Row>
              <Col :lg="24">
                <Card>
                  <h4 slot="title">发表评论</h4>
                  <Row style="text-align: center;">
                    <Input show-word-limit maxlength="500" v-model="comment"
                           type="textarea" :autosize="{minRows: 5,maxRows: 60}"
                           placeholder="有什么想说的....."/>
                  </Row>
                  <Row style="margin-top: 20px;">
                    <Button size="large" type="primary" @click="submitComment" style="margin-left: 10px; ">确认</Button>
                  </Row>
                </Card>
              </Col>
            </Row>
            <Row style="margin-top: 10px;">
              <Col span="24">
                <Card id="comments" >
                  <h4 slot="title">评论</h4>
                  <h5 v-if="this.commentlists.length === 0">暂时没有小伙伴评论！！</h5>
                  <Row v-for="(item,index) in this.commentlists"  :key="'comm-'+index">
                      <Col :lg="24" >
                        <Avatar icon="ios-person" :src="item.userheadPortrait" size="large"/>
                        {{ item.username }}
                        <div style="text-indent: 4em;">
                          <p style="display: inline;font-weight: bold;color: #409eff" v-if="item.tousername !== null"><a>@{{ item.tousername }}</a></p>
                          <p style="display: inline;">{{ item.comments }}</p>
                        </div>
                        <span v-if="Number(item.userid) !== Number(userid)" :id="'com'+item.userid">
                          <Collapse style="background: #ffffff; border: white" >
                          <Panel name="1" >
                            回复
                            <p slot="content"><Input v-model="toUserComment" type="textarea" show-word-limit maxlength="500" :autosize="{minRows: 5,maxRows: 60}" placeholder="有什么想说的....."></Input>
                              <Button size="large" type="primary" @click="submitCommenttoUser(item.userid)" style="margin-left: 10px; margin-top: 10px;">确认</Button></p>
                          </Panel>
                        </Collapse>
                        </span>
                      </Col>
                    <Divider>{{ item.time.replace('T', ' ') }}</Divider>
                  </Row>
                </Card>
              </Col>
            </Row>
          </Col>
          <Col :md="3"></Col>
        </Row>
    </div>
    <el-backtop target=".headmenu"></el-backtop>
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu";
import { getNewsDetail, updateHistory, getSimilarnews, getHotNews, getComments, updateGiveLike, submitComments, submitCommentsToUser } from '@/api'
import { videoPlayer } from 'vue-video-player'

export default {
  name: "NewsDetail",
  components: {HeaderMenu, videoPlayer},
  computed: {
    defaultImg() {
      return 'this.src="' + require('@/assets/imgs/404.jpg') + '"'
    }
  },
  created() {
    this.openFullScreen()
    let self = this
    self.fetchData()
    self.userid = sessionStorage.getItem('userId')
  },

  data()  {
    return {
      fullscreenLoading: false,
      videoshow: false,
      isShowLoading: true,
      userid: '',
      toUserComment: '',
      commentlists:[],
      recsimilarlist: [],
      rechotlist: [],
      sort: '',
      newsdetail: '',
      newsid: '',
      title: '',
      readnum: '',
      comments: '',
      category: '',
      origin: [],
      videourl: '',
      date: '',
      pic_url: '',
      Carouselvalue1: 1,
      Carouselvalue2: 2,
      comment: '',
      value: 0,
      value1: 0,
      screenHeight: document.documentElement.clientHeight - 70,
      screenWidth: document.documentElement.clientWidth,
      playerOptions: {
        playbackRates: [0.7, 1.0, 1.5, 2.0], //播放速度
        autoplay: false, // 如果true,浏览器准备好时开始回放。
        muted: false, // 默认情况下将会消除任何音频。
        loop: false, // 导致视频一结束就重新开始。
        preload: 'auto', // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
        language: 'zh-CN',
        aspectRatio: '4:3', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
        fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
        sources: [{
          type: "",
          src: "", //url地址
        }],
        poster: "../../static/images/test.jpg", // 你的封面地址
        // width: document.documentElement.clientWidth,
        notSupportedMessage: '此视频暂无法播放，请稍后再试', // 允许覆盖Video.js无法播放媒体源时显示的默认信息。
        controlBar: {
          timeDivider: true,
          durationDisplay: true,
          remainingTimeDisplay: false,
          fullscreenToggle: true,  // 全屏按钮
        }
      }
    }
  },
  mounted() {
    const that = this
    window.onresize = () => {
      return (() => {
        window.screenHeight = document.body.clientHeight
        that.screenHeight = window.screenHeight - 70
      })()
    }
  },
  watch: {
    screenHeight(val) {
      // 为了避免频繁触发resize函数导致页面卡顿，使用定时器
      if (!this.timer) {
        // 一旦监听到的screenWidth值改变，就将其重新赋给data里的screenWidth
        this.screenHeight = val
        this.timer = true
        let that = this
        setTimeout(function () {
          // 打印screenWidth变化的值
          // console.log(that.screenHeight)
          that.timer = false
        }, 400)
      }
    },
    '$route':'fetchData'
  },
  methods: {
    openFullScreen() {
      const loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading',
        background: 'rgba(206,206,206,0.7)'
      });
      setTimeout(() => {
        loading.close();
      }, 1000);
    },
    submitComment() {
      submitComments(sessionStorage.getItem('userId'), this.newsid, this.comment)
      this.$router.go(0);
    },
    submitCommenttoUser(touserid) {
      submitCommentsToUser(sessionStorage.getItem('userId'), this.newsid, this.toUserComment, touserid)
      console.log(this.toUserComment)
      this.$router.go(0);
    },
    upGivelike(type){
      // console.log('newsid',this.newsid)
      if (type === 1){
        if (this.value === 0){
          this.value = 0
          updateGiveLike(sessionStorage.getItem('userId'), this.newsid, 0)
        } else {
          if (this.value1 === 1){
            this.value1 = 0
          }
          this.value = 1
          updateGiveLike(sessionStorage.getItem('userId'), this.newsid, 1)
        }
      }else {
        if (this.value1 === 1){
          this.value = 0
          updateGiveLike(sessionStorage.getItem('userId'), this.newsid, 2)
        }else {
          if(this.value === 1){
            this.value = 0
          }
          this.value1 = 1
          updateGiveLike(sessionStorage.getItem('userId'), this.newsid, 0)
        }
      }
      // if (this.value1 === 0 && this.value === 1){
      //   updateGiveLike(sessionStorage.getItem('userId'), this.newsid, 1)
      // }else if (this.value1 === 0 && this.value === 0){
      //   updateGiveLike(sessionStorage.getItem('userId'), this.newsid, 0)
      // }else {
      //   updateGiveLike(sessionStorage.getItem('userId'), this.newsid, 2)
      // }
    },
    toNewsDetail(newsid) {
      this.$router.push('/newspage/'+newsid)
    },
    toComments() {
      document.querySelector('#comments').scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"})
    },
    fetchData(){
      this.isShowLoading = true
      //清空所有数据
      Object.assign(this.$data, this.$options.data())

      // console.log('路由发送变化doing...');
      //加载数据
      this.newsid = this.$route.params.id
      getNewsDetail(this.newsid, sessionStorage.getItem('userId')).then(res => {
        this.newsid = res.message.newsid
        this.date = res.message.date
        this.pic_url = eval(res.message.pic_url)
        // console.log('pic',this.pic_url)
        this.playerOptions.sources[0].src = res.message.videourl
        if (String(res.message.videourl) !== 'None' && res.message.videourl !== '[]'){
          this.videoshow = true
        }
        this.comments = res.message.comments
        this.newsdetail = res.message
        this.category = res.message.category
        // console.log(this.category)
        this.title = res.message.title
        this.readnum = res.message.readnum
        if(res.message.givelike === 1){
          this.value = 1
        }
        if(res.message.givelike === 2){
          this.value1 = 1
        }
        this.origin = eval(res.message.origin)
        switch (this.category) {
          case 0:
            this.sort = '美股'
            break
          case 1:
            this.sort = '国内'
            break
          case 2:
            this.sort = '国际'
            break
          case 3:
            this.sort = '社会'
            break
          case 4:
            this.sort = '体育'
            break
          case 5:
            this.sort = '娱乐'
            break
          case 6:
            this.sort = '军事'
            break
          case 7:
            this.sort = '科技'
            break
          case 8:
            this.sort = '财经'
            break
          case 9:
            this.sort = '股市'
            break
          case 10:
            this.sort = '全部'
            break
          default:
            break
        }
        document.querySelector('#anchor1').scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"})
        setTimeout(function () {
          this.isShowLoading = false
        }, 3000)

      })
      updateHistory(sessionStorage.getItem('userId'), this.newsid)
      getSimilarnews(this.newsid).then(res => {
        // console.log(res.newslist)
        for (let i = 0; i < res.newslist.length; i++) {
          let news = res.newslist[i]
          let pic_url = ''
          if(news.pic_url === '[]')
            pic_url= ''
          else
            pic_url = eval(news.pic_url)
          let data = {
            'newsid': news.newsid,
            'title': news.title,
            'pic_url': pic_url,
            'mainpage': news.mainpage.slice(0,50)+'...'
          }
          this.recsimilarlist.push(data)
        }
        // console.log(this.recsimilarlist)
      })
      getHotNews().then(res => {
        // console.log(res.newslist)
        for (let i = 0; i < res.newslist.length; i++) {
          let news = res.newslist[i]
          let pic_url = ''
          if(news.pic_url === '[]')
            pic_url= ''
          else
            pic_url = eval(news.pic_url)
          let data = {
            'newsid': news.newsid,
            'title': news.title,
            'pic_url': pic_url,
            'mainpage': news.mainpage.slice(0,50)+'...'
          }
          this.rechotlist.push(data)
        }
        // console.log('rechotlist', this.rechotlist)
      })
      getComments(this.newsid).then(res => {
        let commentlist = res.commentlist
        let commentlists = []
        for(let i=0;i<commentlist.length;i++){
          let comment = commentlist[i]
          let data = {
            'userid':comment.userid,
            'touserid':comment.touserid,
            'comments':comment.comments,
            'time':comment.time,
            'username':comment.username,
            'userheadPortrait':comment.userheadPortrait,
            'tousername':comment.tousername,
            'toUserHeadPortrait':comment.toUserHeadPortrait,
          }
          commentlists.push(data)

        }
        this.commentlists = commentlists
      })
      this.$Loading.finish()
    },

  },
}
</script>

<style scoped>
.pageitem{
  margin-top: 10px;
  margin-bottom: 7px;
  text-indent: 2em;
  font-size: 18px;
}
.mainpage {

}
.images{
  width: 500px;
  height: 300px;
  object-fit: cover;
  position: relative;
}
.pict {
  margin: auto;
}
.pic_item h2 {
  margin: auto;
  /*position: absolute;*/
  color: #070707;
  bottom: 3rem;
}
.top{
  padding: 10px;
  background: rgba(0, 153, 229, .7);
  color: #fff;
  text-align: center;
  border-radius: 2px;
}
.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(255,255,255,.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
