<template>
  <div class="login-vue" :style="bg">
    <div class="container">
      <p class="title">新闻中心</p>
      <div class="input-c">
        <Input prefix="ios-contact" v-model="account" placeholder="用户名" clearable @on-blur="verifyAccount" />
        <p class="error">{{accountError}}</p>
      </div>
      <div class="input-c">
        <Input type="password" v-model="pwd" prefix="md-lock" placeholder="密码" clearable @on-blur="verifyPwd"
               @keyup.enter.native="submit" />
        <p class="error">{{pwdError}}</p>
      </div>
      <Button :loading="isShowLoading" class="submit" type="primary" @click="submit">登陆</Button>
      <p class="account"><span @click="register">注册账号</span> | <span @click="forgetPwd">忘记密码 </span>| <span @click="tourists">游客模式</span></p>
    </div>
  </div>
</template>

<script>
import { login, getTourists } from '@/api'

export default {
  name: "Login",
  data() {
    return {
      account: '',
      pwd: '',
      accountError: '',
      pwdError: '',
      isShowLoading: false,
      bg: {},
    }
  },
  created() {
    //token存在直接跳转
    let token = sessionStorage.getItem('token')
    if(token !== null && token !=='' )
      this.$router.push({ name: 'home' })
    this.bg.backgroundImage = 'url(' + require('../assets/imgs/bg0' + new Date().getDay() + '.jpg') + ')'
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
    tourists() {
      getTourists().then(res => {
        sessionStorage.setItem('userImg', res.data.headPortrait)
        sessionStorage.setItem('userName', res.data.username)
        sessionStorage.setItem('userId', res.data.userid)
        sessionStorage.setItem('gender', res.data.gender)
        sessionStorage.setItem('token', 'i_am_token')
        this.$router.push({ path: this.redirect || '/' })
        this.$Message.info('欢迎游客！！完整功能请注册并登录账号！！')
      })
    },
    verifyAccount() {
      if (this.account === '') {
        this.accountError = '账号不能为空'
      } else {
        this.accountError = ''
      }
    },
    verifyPwd() {
      if (this.pwd === '') {
        this.pwdError = '密码不能为空'
      } else {
        this.pwdError = ''
      }
    },
    register() {
      this.$router.push({ name: 'register' })
    },
    forgetPwd() {

    },
    submit() {
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
            this.$Message.info('登录成功！！')
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
  },
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
