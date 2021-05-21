<style lang="less">
@import './style/common.less';
@import './style/table.less';
</style>
<template>
  <div class="center_content" :height="fullHeight">
    <HeaderMenu></HeaderMenu>
    <Row :gutter="10">
      <Col span="24">
        <Card>
          <p slot="title">
            <Icon type="mouse"></Icon>
            消息
          </p>
          <Row>
            <Table :height="fullHeight" @on-row-click="chooseMessage" :columns="columns1" :data="data3"
                   :style="{width: fullWidth+'px'}"></Table>
            <Modal
              v-if="Number(modaldata.hadread) === 0"
              v-model="modal1"
              cancel-text="返回"
              :title="modaldata.topic"
              @on-cancel="cancel">
              <div v-if="Number(modaldata.newsid) === 0">{{ modaldata.message }}</div>
              <a v-if="modaldata.newsid !== null"
                 :href="'newspage/'+modaldata.newsid">{{ modaldata.message }}</a>
              <div slot="footer"></div>
            </Modal>
            <Modal
              v-if="modaldata.hadread === 1"
              v-model="modal1"
              :title="this.modaldata.topic"
              @on-cancel="cancel">
              <div v-if="this.modaldata.newsid === null">{{ this.modaldata.message }}</div>
              <a v-if="this.modaldata.newsid !== null"
                 :href="'newspage/'+this.modaldata.newsid">{{ this.modaldata.message }}</a>
            </Modal>
          </Row>
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu";
import * as table from './data/search';
import {getMessage, setHadRead} from '@/api'

export default {
  name: "UserMessage",
  components: {HeaderMenu},
  created() {
    getMessage(sessionStorage.getItem('userId')).then(res => {
      // console.log('res:', res)
      let orimessage = res.message
      table.searchTable3.length = 0
      for (let i = 0; i < orimessage.length; i++) {
        let temp = orimessage[i]
        let reading
        if (Number(temp.hadread) === 1){
          reading = '已读'
        }else {
          reading = '未读'
        }
        let test = {
          'id': temp.id,
          'topic': temp.title,
          'time': temp.time,
          'message': temp.message,
          'newsid': temp.newsid,
          'hadread': temp.hadread,
          'state': reading,
        }
        table.searchTable3.push(test)
      }
    })
  },
  data() {
    return {
      modaldata: {
        temp: {},
        message: '',
        topic: '',
        newsid: '',
        hadread: '',
        time: '',
      },
      modal1: false,
      fullHeight: document.documentElement.clientHeight - 70,
      fullWidth: document.documentElement.clientWidth,
      searchConName3: '',
      columns1: table.columns1,
      data3: [],
      initTable3: [],
      messagelist: [],
    };
  },
  methods: {
    chooseMessage(params) {
      console.log(params)
      this.modal1 = true
      this.modaldata = {
        id: '',
        message: '',
        topic: '',
        newsid: '',
        hadread: '',
        time: '',
      }
      this.modaldata.topic = params.topic
      this.modaldata.newsid = params.newsid
      this.modaldata.time = params.time
      this.modaldata.message = params.message
      setHadRead(params.id)
    },
    cancel() {
      this.$Message.info('Clicked cancel');
      this.$router.go(0)
    },
    init() {
      this.data3 = this.initTable3 = table.searchTable3;
    },
  },
  mounted() {
    this.init();
  }
}
</script>

<style scoped>

</style>
