<template>
  <div >
    <Menu mode="horizontal" :active-name="activename" >
      <MenuItem name="1">
        <img src="../assets/imgs/logo4.png" width="90px" style="margin-top: 10px;">
      </MenuItem>
      <MenuItem name="2" to="/home" >
        <Icon type="md-home"/>
        首页
      </MenuItem>
      <MenuItem name="3" to="/recommend" v-if="displayornot">
        <Icon type="ios-star"/>
        为你推荐
      </MenuItem>
      <MenuItem name="4" to="/eventhot">
        <Icon type="md-clock"/>
        时事热点
      </MenuItem>
      <!--        <Badge dot style="display: inline-block; float: right; margin-right: 70px; margin-top: 4px;">-->
      <!--          <Icon type="ios-notifications-outline" size="30" ></Icon>-->
      <!--        </Badge>-->
      <Dropdown style="display: inline-block; float: right; margin-right: 2%; cursor: pointer;" trigger="click"  @on-click="userOperate" >
        <Badge v-if="this.tip === 1" dot  :offset=[12,8]>
          <Avatar :src="userImg" icon="ios-person" size="large"></Avatar>
        </Badge>
        <Badge v-if="this.tip === 0"  :offset=[12,8]>
          <Avatar :src="userImg" icon="ios-person" size="large"></Avatar>
        </Badge>
        <DropdownMenu slot="list">
          <DropdownItem name="1" @click.native="toMessage">查看消息</DropdownItem>
          <DropdownItem name="2" @click.native="toUser">个人中心</DropdownItem>
          <DropdownItem divided name="3">退出登录</DropdownItem>
        </DropdownMenu>
      </Dropdown>
    </Menu>
  </div>
</template>

<script>
import { resetTokenAndClearUser } from '../utils'
import { getTip } from '@/api'
export default {
  name: "HeaderMenu",
  created() {
    this.userImg = sessionStorage.getItem('userImg')
    if (sessionStorage.getItem('userId') !== null)
      getTip(sessionStorage.getItem('userId')).then(res => {
        // console.log(res)
        this.tip = res.message
        // console.log('tip',this.tip)
      })
  },
  data() {
    return{
      displayornot: Number(sessionStorage.getItem('userId')) !== 100000,
      tip: 0,
      userImg:'',
    }
  },
  props: {
    'activename' : Number,
  },
  methods:{
    toUser() {
      this.$router.push('/user')
    },
    toMessage() {
      this.$router.push('/message')
    },
    userOperate(name) {
      switch (name) {
        case '1':
          // 基本资料
          // this.gotoPage('user')
          break
        case '2':
          // 消息
          // this.gotoPage('message')
          break
        case '3':
          resetTokenAndClearUser()
          this.$router.push({ name: 'login' })
          this.$Message.info('退出成功！！')
          break
      }
    },
  }
}
</script>

<style scoped>

</style>
