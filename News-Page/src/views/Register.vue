<template>
  <div class="login-vue" :style="bg">
    <div class="container">
      <p class="title">注册账号</p>
      <div class="input-c">
        <Input prefix="ios-contact" v-model="account" placeholder="用户ID" clearable @on-blur="verifyUserid" />
        <p class="error">{{accountError}}</p>
      </div>
      <div class="input-c">
        <Input  v-model="username" prefix="md-lock" placeholder="用户名" clearable @on-blur="verifyUsername"
               @keyup.enter.native="submit" />
        <p class="error">{{pwdError}}</p>
      </div>
      <div class="input-c">
        <Input type="password" v-model="pwd" prefix="md-lock" placeholder="密码" clearable @on-blur="verifyPwd"
               @keyup.enter.native="submit" />
        <p class="error">{{pwdError}}</p>
      </div>
      <div class="input-c">
        <Select v-model="gender" style="width:200px" placeholder="请选择性别">
          <Option v-for="item in genderlist" :value="item.value" :key="item.value" >{{ item.label }}</Option>
        </Select>
        <p class="error">{{pwdError}}</p>
      </div>
      <Button :loading="isShowLoading" class="submit" type="primary" @click="submit">注册</Button>
      <p class="account"><span @click="tologin">已有账号？</span></p>
    </div>
    <Modal v-model="word" title="请选择热门标签"  @on-ok="ok"
           @on-cancel="cancel" cancel-text="跳过">
      <div class="tagspace">
        <Tag v-for="(item,index) in taglist" :key="index" :name="item" closable size="large" @on-close="deleteTags(item)">{{ item }}</Tag>
      </div>
      <div class="wordcloud" id="wordcloud" style="width:500px;height:500px;background: #ffffff; "></div>
    </Modal>

  </div>
</template>

<script>
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import { getTags, register } from '@/api'
export default {
  name: "register",
  created() {
    this.bg.backgroundImage = 'url(' + require('../assets/imgs/bg0' + new Date().getDay() + '.jpg') + ')'
  },
  data() {
    return {
      username: '',
      updata: '',
      gender: '',
      genderlist: [
        {
          value: "男",
          label: "男"
        },
        {
          value: "女",
          label: "女"
        },
      ],
      wordlist: [],
      word: false,
      charts: '',
      cloud: [],
      taglist: [],
      account: '',
      pwd: '',
      accountError: '',
      pwdError: '',
      isShowLoading: false,
      bg: {},
    }
  },
  watch: {
    $route: {
      handler(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true,
    },
  },
  methods: {
    ok() {
      if (this.account !== '' && this.pwd !== '' && this.gender !== '' && this.username !== ''){
        this.isShowLoading = true
        register(this.account, this.pwd, this.username, String(this.taglist.join()), this.gender).then(res => {
          if (res.message === 'Success.'){
            sessionStorage.setItem('userImg', '')
            sessionStorage.setItem('userName', this.username)
            sessionStorage.setItem('userId', this.account)
            sessionStorage.setItem('gender', this.gender)
            sessionStorage.setItem('token', 'i_am_token')
            this.$router.push({ path: this.redirect || '/' })
            this.$Message.info('成功注册！！')
          }else {
            this.accountError = '账号或密码错误'
            this.pwdError = ''
            this.isShowLoading = false
          }
        })
      }else {
        this.accountError = '账号不能为空'
        this.pwdError = '密码不能为空'
      }
    },
    cancel() {
      if (this.account !== '' && this.pwd !== ''){
        this.isShowLoading = true
        login(this.account, this.pwd).then(res => {
          if (res.message === 'Success.'){
            sessionStorage.setItem('userImg', res.data.headPortrait)
            sessionStorage.setItem('userName', res.data.username)
            sessionStorage.setItem('userId', res.data.userid)
            sessionStorage.setItem('gender', res.data.gender)
            sessionStorage.setItem('token', 'i_am_token')
            this.$router.push({ path: this.redirect || '/' })
            this.$Message.info('登录成功Register！！')
          }else {
            this.accountError = '账号或密码错误'
            this.pwdError = ''
            this.isShowLoading = false
          }
        })
      }else {
        this.accountError = '账号不能为空'
        this.pwdError = '密码不能为空'
      }
    },
    deleteTags(item){
      for (let i in this.taglist){
        if (this.taglist[i] === item){
          this.taglist.splice(i, 1)
        }
      }
      console.log(this.taglist)
    },
    eConsole(param) {
      console.log(param)
      if (typeof param.seriesIndex != 'undefined') {
        console.log(param.name)
        this.taglist.push(param.name)
        // console.log(this.charts)
        for (let i in this.cloud){
          // console.log(i)
          if (this.cloud[i].name === param.name){
            this.cloud.splice(i,1)
            // console.log(this.cloud[i])
          }
        }
        console.log(this.cloud)
        let option = {
          series: [{
            type: 'wordCloud',
            shape: 'circle',
            left: 'center',
            top: 'center',
            width: '70%',
            height: '80%',
            right: null,
            bottom: null,
            // clickable : true,
            // Text size range which the value in data will be mapped to.
            // Default to have minimum 12px and maximum 60px size.

            sizeRange: [12, 60],

            // Text rotation range and step in degree. Text will be rotated randomly in range [-90, 90] by rotationStep 45

            rotationRange: [0, 0],
            rotationStep: 90,

            // size of the grid in pixels for marking the availability of the canvas
            // the larger the grid size, the bigger the gap between words.

            gridSize: 8,

            // set to true to allow word being draw partly outside of the canvas.
            // Allow word bigger than the size of the canvas to be drawn
            drawOutOfBound: false,

            // If perform layout animation.
            // NOTE disable it will lead to UI blocking when there is lots of words.
            layoutAnimation: true,

            // Global text style
            textStyle: {
              fontFamily: 'sans-serif',
              fontWeight: 'bold',
              // Color can be a callback function or a color string
              color: function () {
                // Random color
                return 'rgb(' + [
                  Math.round(Math.random() * 160),
                  Math.round(Math.random() * 160),
                  Math.round(Math.random() * 160)
                ].join(',') + ')';
              }
            },
            emphasis: {
              focus: 'self',

              textStyle: {
                shadowBlur: 10,
                shadowColor: '#333'
              }
            },

            // Data is an array. Each array item must have name and value property.
            data: this.cloud,

          }]
        }
        this.charts.setOption(option,true)
      }
    },
    verifyUserid() {
      if (this.account === '') {
        this.accountError = '账号不能为空'
      }
    },
    verifyPwd() {
      if (this.pwd === '') {
        this.pwdError = '密码不能为空'
      }
    },
    tologin() {
      this.$router.push({ name: 'login' })
    },
    submit() {
      this.word=true
    },
  },
  mounted() {
    getTags().then(res => {
      this.wordlist = res.message
      for (let i in res.message){
        let data = {
          name:res.message[i],
          value: Math.random()*50
        }
        this.cloud.push(data)
      }
      let chart = echarts.init(document.getElementById('wordcloud'))
      chart.on('click', this.eConsole);
      chart.setOption({
        series: [{
          type: 'wordCloud',
          shape: 'circle',
          left: 'center',
          top: 'center',
          width: '70%',
          height: '80%',
          right: null,
          bottom: null,
          // clickable : true,
          // Text size range which the value in data will be mapped to.
          // Default to have minimum 12px and maximum 60px size.

          sizeRange: [12, 60],

          // Text rotation range and step in degree. Text will be rotated randomly in range [-90, 90] by rotationStep 45

          rotationRange: [0, 0],
          rotationStep: 90,

          // size of the grid in pixels for marking the availability of the canvas
          // the larger the grid size, the bigger the gap between words.

          gridSize: 8,

          // set to true to allow word being draw partly outside of the canvas.
          // Allow word bigger than the size of the canvas to be drawn
          drawOutOfBound: false,

          // If perform layout animation.
          // NOTE disable it will lead to UI blocking when there is lots of words.
          layoutAnimation: true,

          // Global text style
          textStyle: {
            fontFamily: 'sans-serif',
            fontWeight: 'bold',
            // Color can be a callback function or a color string
            color: function () {
              // Random color
              return 'rgb(' + [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160)
              ].join(',') + ')';
            }
          },
          emphasis: {
            focus: 'self',

            textStyle: {
              shadowBlur: 10,
              shadowColor: '#333'
            }
          },

          // Data is an array. Each array item must have name and value property.
          data: this.cloud,

        }]
      })
      this.charts = chart
    })
  }
}
</script>

<style>
.login-vue {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
}
.wordcloud {
  background: rgba(255, 255, 255, .5);
  border-radius: 10px;
  padding: 30px;
}
.login-vue .container {
  background: rgba(255, 255, 255, .5);
  width: 300px;
  text-align: center;
  border-radius: 10px;
  padding: 30px;
}
.login-vue .ivu-input {
  background-color: transparent;
  color: #fff;
  outline: #fff;
  border-color: #fff;
}
.login-vue ::-webkit-input-placeholder { /* WebKit, Blink, Edge */
  color: rgba(255, 255, 255, .8);
}
.login-vue :-moz-placeholder { /* Mozilla Firefox 4 to 18 */
  color: rgba(255, 255, 255, .8);
}
.login-vue ::-moz-placeholder { /* Mozilla Firefox 19+ */
  color: rgba(255, 255, 255, .8);
}
.login-vue :-ms-input-placeholder { /* Internet Explorer 10-11 */
  color: rgba(255, 255, 255, .8);
}
.login-vue .title {
  font-size: 16px;
  margin-bottom: 20px;
}
.login-vue .input-c {
  margin: auto;
  width: 200px;
}
.login-vue .error {
  color: red;
  text-align: left;
  margin: 5px auto;
  font-size: 12px;
  padding-left: 30px;
  height: 20px;
}
.login-vue .submit {
  width: 200px;
}
.login-vue .account {
  margin-top: 30px;
}
.login-vue .account span {
  cursor: pointer;
}
.login-vue .ivu-icon {
  color: #eee;
}
.login-vue .ivu-icon-ios-close-circle {
  color: #777;
}
</style>
