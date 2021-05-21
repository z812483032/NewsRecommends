<style lang="less">
@import 'style/common.less';
@import 'style/draggable-list.less';
</style>

<template>
  <div class="page">
    <HeaderMenu></HeaderMenu>
    <div class="center_content" :height="fullHeight">
<!--      <Scroll :height="this.fullHeight">-->
        <Row>
          <Col :lg="4"></Col>
          <Col :s="10" :md="10" :lg="20" style="margin-top: 10px;">
            <Row type="flex">
              <Col :xxs="1" :xs="5" :md="10" :lg="18" >
                <Card >
                  <h2 slot="title">修改头像</h2>
                  <el-upload
                    name="image"
                    :data="{apiType:'ali', token:'f77bc648180a3838b1a01326bf358db6'}"
                    class="avatar-uploader"
                    action="https://www.hualigs.cn/api/upload"
                    :show-file-list="false"
                    :on-success="handleAvatarSuccess"
                    :before-upload="beforeAvatarUpload">
                    <img v-if="userdetail.headportrait" :src="userdetail.headportrait" class="avatar">
                    <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                  </el-upload>
<!--                  <Avatar  icon="ios-person" size="90" :src="userdetail.headportrait"></Avatar>-->

                </Card>
                <Card style="margin-top: 10px;">
                  <h2 slot="title">账户详情</h2>
                  <h3 class="margin-left-10">ID:&nbsp;&nbsp;{{ userdetail.userid }}</h3>
                  <h3 class="margin-left-10">用户名:&nbsp;&nbsp;{{ userdetail.username }}</h3>
                  <h3 class="margin-left-10">性别:&nbsp;&nbsp;{{ userdetail.gender }}</h3>
                  <Button type="primary" style="margin-top: 20px;" @click="modal1 = true">修改个人信息</Button>
                  <Modal
                    v-model="modal1"
                    title="修改用户信息"
                    @on-ok="ok"
                    @on-cancel="cancel">
                    <Form ref="formCustom" :model="userdetail" :rules="ruleCustom" :label-width="80">
                      <FormItem label="ID" prop="passwd">
                        <Input type="text" v-model="userdetail.userid" v-if="!displayornot" disabled></Input>
                        <Input type="text" v-model="userdetail.userid" v-if="displayornot" ></Input>
                      </FormItem>
                      <FormItem label="用户名" prop="passwdCheck">
                        <Input type="text" v-model="userdetail.username"  v-if="!displayornot" disabled></Input>
                        <Input type="text" v-model="userdetail.username"  v-if="displayornot" ></Input>
                      </FormItem>
                      <FormItem label="性别" prop="age">
                        <Select v-model="userdetail.gender"  v-if="!displayornot" disabled>
                          <Option value="男" >男</Option>
                          <Option value="女"> 女</Option>
                        </Select>
                        <Select v-model="userdetail.gender"  v-if="displayornot">
                          <Option value="男" >男</Option>
                          <Option value="女"> 女</Option>
                        </Select>
<!--                        <Input type="text" v-model="formCustom.age" number></Input>-->
                      </FormItem>
                    </Form>
                  </Modal>
                </Card>
                <Row style="margin-top: 10px;">
                  <Col span="24">
                    <Card>
                      <Row>
                        <Col span="24" style="width:100%;height: 100%;">
                          <Card dis-hover>
                            <div slot="title">
                              <div style="vertical-align: center;overflow: hidden;">
                                <span style="float: left;margin-top: 8px;font-weight: bold;font-size: 18px;">我的兴趣(点击标签删除）</span>
                                <Button icon="md-add" style="float: right; cursor: pointer;" @click="modal2 = true">自定义标签</Button>
                              </div>
                            </div>
                            <Modal
                              v-model="modal2"
                              title="添加自定义标签"
                              @on-ok="addTagok"
                              @on-cancel="cancelTagok">
                              <Form ref="formCustom" :rules="ruleCustom" :label-width="80">
                                <FormItem label="标签" prop="tagsword">
                                  <Input type="text" v-model="newtag"></Input>
                                  <!--                        <Input type="text" v-model="formCustom.age" number></Input>-->
                                </FormItem>
                              </Form>
                            </Modal>
<!--                            <div style="height: 360px;">-->
<!--                              <ul id="myTags" class="iview-admin-draggable-list">-->
<!--                                <li v-for="(item, index) in myTags" :key="'do-'+index" class="notwrap todolist-item"-->
<!--                                    :data-index="index">-->
<!--                                  {{ item.content}}-->
<!--                                </li>-->
<!--                              </ul>-->
<!--                            </div>-->
                            <div class="wordcloud" id="mycloud" style="height: 550px; background: #ffffff; margin: auto;">
                            </div>
                          </Card>
                        </Col>
                      </Row>
                    </Card>
                  </Col>
                </Row>
                <Row>
                  <Col span="15" style="margin-top: 10px;width:100%;height: 100%;">
                    <Card>
                      <h2 slot="title">热词库</h2>
                    <div class="wordcloud" id="wordcloud" style="height: 450px; background: #ffffff; margin: auto;">
                    </div>
                    </Card>
                  </Col>
                  <Col span="9" style="margin-top: 10px;">
                    <Card>
                      <div slot="title">
                        <h2 style="display: inline-block;">
                          点击右侧添加到我的标签
                        </h2>
                        <h2 style="float: right; display: inline; cursor: pointer;"><Icon  slot="title"  type="md-cloud-upload" @click.native="updateuserTags"/></h2>
                      </div>
                      <div class="tagspace" style="height:450px;" >
                        <Tag v-for="(item,index) in taglist" :key="index" :name="item" type="border" closable size="large" @on-close="deleteTags(item)" :color="item.color">
                          {{ item.name }}
                          <Button slot="title" >更新</Button>
                        </Tag>
                      </div>
                    </Card>
                  </Col>
                </Row>
              </Col>
            </Row>
            <Row>
            </Row>
            <Row>
            </Row>
          </Col>
        </Row>
<!--      </Scroll>-->
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import HeaderMenu from "../components/HeaderMenu";
import 'echarts-wordcloud'
import Sortable from 'sortablejs';
import {getUserdetail, updateUser, getTags, updateTags, updateUserHeadportrait} from '@/api'
import GLOBAL from '@/api/global_variable'

export default {
  name: "UserDetail",
  components: {HeaderMenu},
  data() {
    const validateUserid = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please enter your password'));
      } else {
        if (this.formCustom.username !== '') {
          // 对第二个密码框单独验证
          this.$refs.formCustom.validateField('passwdCheck');
        }
        callback();
      }
    };
    const validateUsername = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please enter your password again'));
      } else if (value !== this.formCustom.userid) {
        callback(new Error('The two input passwords do not match!'));
      } else {
        callback();
      }
    };
    return {
      displayornot: Number(sessionStorage.getItem('userId')) !== 100000,
      tagpage: 0,
      modal2: false,
      newtag: '',
      imageUrl: '',
      cloud: [],
      // userdetail: {},
      hotword: [],
      userdetail: {
        userid: '',
        username: '',
        gender: '',
      },
      ruleCustom: {
        userid: [
          {validator: validateUserid, trigger: 'blur'}
        ],
        username: [
          {validator: validateUsername, trigger: 'blur'}
        ],
      },

      modal1: false,
      taglist: [],
      myTags: [],
      hotTags: [],
      resTags: [],
      fullHeight: document.documentElement.clientHeight - 70,

    }
  },
  methods: {
    handleAvatarSuccess(res, file) {
      this.userdetail.headportrait = res.data.url['ali']
      console.log(res);
      updateUserHeadportrait(sessionStorage.getItem('userId'),res.data.url['ali'])
      sessionStorage.setItem("userImg", res.data.url['ali'])
      this.$Message.info("修改头像成功！！")
      this.$Loading.finish()
      this.$router.go(0)
    },
    beforeAvatarUpload(file) {
      this.$Loading.start()
      const isJPG = file.type === 'image/jpeg' || file.type === 'image/png';
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!');
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!');
      }
      return isJPG && isLt2M;
    },
    updateuserTags() {
      let tags = []
      for(let temp in this.myTags){
        tags.push(this.myTags[temp].name)
      }
      for (let i in this.taglist){
        tags.push(this.taglist[i].name)
        this.myTags.push({name:this.taglist[i].name, value:Math.random()*30})
      }
      console.log(tags)
      updateTags(sessionStorage.getItem('userId'),tags).then(res => {
        console.log(res)
        if (Number(res.status) === 100){
          this.$Message.info('添加成功！！')
          this.taglist = []
        }
      })
      this.$router.go(0)
      document.querySelector('#mycloud').scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"})
    },
    deleteTags(item){
      for (let i in this.taglist){
        if (this.taglist[i] === item){
          this.taglist.splice(i, 1)
        }
      }
      console.log(this.taglist)
    },
    getRandomIntInclusive(min, max) {
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min + 1)) + min; //含最大值，含最小值
    },
    randcolor() {
      let color = ['default', 'primary', 'success', 'error', 'warning', 'magenta', 'volcano', 'orange', 'gold', 'yellow',
      'lime', 'green', 'cyan', 'blue', 'geekblue', 'purple']
      let randint = this.getRandomIntInclusive(0, color.length-1)
      return color[randint]
    },
    refreshTags(param) {
      let maskImage = new Image();
      let image = GLOBAL.pic64
      console.log(param)
      if (typeof param.seriesIndex != 'undefined') {
        console.log(param.name)
        let data = {
          name:param.name,
          color:this.randcolor(),
        }
        this.taglist.push(data)
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
          backgroundColor: '#ffffff',
          tooltip: {
            show: true
          },
          series: [{
            name: '热词库',
            type: 'wordCloud',
            right: null,
            bottom: null,
            sizeRange: [10, 20],
            rotationRange: [0, 0],
            rotationStep: 90,
            // If perform layout animation.
            // NOTE disable it will lead to UI blocking when there is lots of words.
            layoutAnimation: true,
            gridSize: 3,
            // shape: 'circle',
            textPadding: 2,
            autoSize: {
              enable: true,
              minSize: 10
            },
            maskImage: maskImage,
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
            drawOutOfBound: false,
            data: this.cloud,
          }]
        }
        maskImage.src = image
        let chart = echarts.init(document.getElementById('wordcloud'))
        maskImage.onload  = function () {chart.setOption(option,true)}
      }
    },
    deleteUsertags(param) {
      let maskImage = new Image();
      if (String(this.userdetail['gender']) === '男' ){
        maskImage.src = GLOBAL.pic64_boy
      } else {
        maskImage.src = GLOBAL.pic64_girl
      }
      console.log(param)
      if (typeof param.seriesIndex != 'undefined') {
        console.log(param.name)
        // console.log(this.charts)
        for (let i in this.myTags){
          // console.log(i)
          if (this.myTags[i].name === param.name){
            this.myTags.splice(i,1)
            // console.log(this.cloud[i])
          }
        }
        let tags = []
        for(let temp in this.myTags){
          tags.push(this.myTags[temp].name)
        }
        updateTags(sessionStorage.getItem('userId'),tags).then(res => {
          console.log(res)
          if (Number(res.status) === 100){
            this.$Message.info('更新成功！！')
          }
        })
        console.log(this.myTags)
        let option = {
          backgroundColor: '#ffffff',
          tooltip: {
            show: true
          },
          series: [{
            name: '热词库',
            type: 'wordCloud',
            right: null,
            bottom: null,
            sizeRange: [10, 20],
            rotationRange: [0, 0],
            rotationStep: 90,
            // If perform layout animation.
            // NOTE disable it will lead to UI blocking when there is lots of words.
            layoutAnimation: true,
            gridSize: 3,
            // shape: 'circle',
            textPadding: 2,
            autoSize: {
              enable: true,
              minSize: 10
            },
            maskImage: maskImage,
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
            drawOutOfBound: false,
            data: this.myTags,
          }]
        }
        let chart = echarts.init(document.getElementById('mycloud'))
        maskImage.onload  = function () {chart.setOption(option,true)}
      }
    },
    handleSubmit(name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.$Message.success('Success!');
        } else {
          this.$Message.error('Fail!');
        }
      })
    },
    handleReset(name) {
      this.$refs[name].resetFields();
    },
    ok() {
      this.$Loading.start()
      updateUser(this.userdetail.userid, this.userdetail.username, this.userdetail.gender).then(res => {
        if(res.message == 'Success.')
          this.$Message.info('修改成功')
        else{
          this.$Message.error('修改失败')
        }
      })
      this.$Loading.finish()
    },
    addTagok() {
      if(this.newtag !== ''){
        let tags = []
        for(let temp in this.myTags){
          tags.push(this.myTags[temp].name)
        }
        this.myTags.push({name:this.newtag, value:Math.random()*30})
        tags.push(this.newtag)
        updateTags(sessionStorage.getItem('userId'),tags).then(res => {
          console.log(res)
          if (Number(res.status) === 100){
            this.$Message.info('添加成功！！')
          }
        })
        let maskImage = new Image();
        if (String(this.userdetail['gender']) === '男' ){
          maskImage.src = GLOBAL.pic64_boy
        } else {
          maskImage.src = GLOBAL.pic64_girl
        }
        let option = {
          backgroundColor: '#ffffff',
          tooltip: {
            show: true
          },
          series: [{
            name: '热词库',
            type: 'wordCloud',
            right: null,
            bottom: null,
            sizeRange: [10, 20],
            rotationRange: [0, 0],
            rotationStep: 90,
            // If perform layout animation.
            // NOTE disable it will lead to UI blocking when there is lots of words.
            layoutAnimation: true,
            gridSize: 3,
            // shape: 'circle',
            textPadding: 2,
            autoSize: {
              enable: true,
              minSize: 10
            },
            maskImage: maskImage,
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
            drawOutOfBound: false,
            data: this.myTags,
          }]
        }
        let chart = echarts.init(document.getElementById('mycloud'))
        maskImage.onload  = function () {chart.setOption(option,true)}
        document.querySelector('#mycloud').scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"})
      } else {
        this.$Message.error("标签不能为空！请重新添加！")
      }
    },
    cancel() {
      this.$Message.info('取消修改');
    },
    cancelTagok (){
      this.$Message.info('取消添加');
    },
  },
  mounted() {
    document.body.ondrop = function (event) {
      event.preventDefault();
      event.stopPropagation();
    };
    // let vm = this;
    // let todoList = document.getElementById('hotTags')
    // Sortable.create(hotTags, {
    //   group: {
    //     name: 'Tags',
    //     pull: true
    //   },
    //   animation: 150,
    //   ghostClass: 'placeholder-style',
    //   fallbackClass: 'iview-admin-cloned-item',
    //   onRemove(event) {
    //     let temptext = {
    //       content: vm.hotTags[event.item.getAttribute('data-index')].content
    //     }
    //     // vm.myTags.splice(event.newIndex,0, vm.hotTags[event.item.getAttribute('data-index')])
    //     vm.hotTags.splice(event.oldIndex,1)
    //     // console.log('temptext:', temptext)
    //     vm.myTags.push(temptext)
    //     console.log("vm.myTags：", vm.myTags)
    //     console.log("vm.hotTags：", vm.hotTags)
    //     // // console.log("添加时：", vm.myTags)
    //     // let tags = []
    //     // for(let temp in vm.myTags){
    //     //   tags.push(vm.myTags[temp].content)
    //     // }
    //     // // console.log(tags)
    //     // updateTags(sessionStorage.getItem('userId'),tags).then(res => {
    //     //   console.log(res)
    //     // })
    //   }
    // })
    // let doList = document.getElementById('myTags')
    // Sortable.create(myTags, {
    //   group: {
    //     name: 'Tags',
    //     pull: true
    //   },
    //   sort: false,
    //   filter: '.iview-admin-draggable-delete',
    //   animation: 150,
    //   fallbackClass: 'iview-admin-cloned-item',
    //   onRemove(event) {
    //     console.log()
    //     // vm.resTags.splice(event.oldIndex,1)
    //     // vm.myTags.splice(event.oldIndex,1)
    //     console.log("删除时：", vm.resTags)
    //     // let tags = []
    //     // for(let temp in vm.resTags){
    //     //   tags.push(vm.resTags[temp].content)
    //     // }
    //     // console.log(tags)
    //     // updateTags(sessionStorage.getItem('userId'),tags).then(res => {
    //     //   console.log(res)
    //     // })
    //   }
    // })
    // let maskImage = new Image();
    // let image = GLOBAL.pic64
    // maskImage.src = image
    // let chart = echarts.init(document.getElementById('wordcloud'))
    // maskImage.onload  = function () {chart.setOption({
    //   title: {
    //     text: '热词库',
    //     x: 'center',
    //     textStyle: {
    //       fontSize: 23
    //     }
    //   },
    //   backgroundColor: '#ffffff',
    //   tooltip: {
    //     show: true
    //   },
    //   series: [{
    //     name: '热词库',
    //     type: 'wordCloud',
    //     sizeRange: [15, 30],//value与图像像素的映射的最大值与最小值
    //     rotationRange: [-45, 90],
    //     // shape: 'circle',
    //     textPadding: 0,
    //     autoSize: {
    //       enable: true,
    //       minSize: 10
    //     },
    //     gridSize :10 ,
    //     maskImage: maskImage,
    //     textStyle: {
    //       normal: {
    //         color: function () {
    //           return 'rgb(' + [
    //             Math.round(Math.random() * 160),
    //             Math.round(Math.random() * 160),
    //             Math.round(Math.random() * 160)
    //           ].join(',') + ')';
    //         }
    //       },
    //       emphasis: {
    //         shadowBlur: 10,
    //         shadowColor: '#333'
    //       }
    //     },
    //     drawOutOfBound: false,
    //     data: []
    //   }]
    // })};

    getUserdetail(sessionStorage.getItem('userId')).then(res => {
      let tags =res.userdetail.hotword
      for (let i in tags){
        if (i !== ''){
          let content = {
            'content': tags[i],
          }
          this.hotTags.push(content)
        }
      }
      tags = eval(res.userdetail.tags)
      for (let i in tags){
        if (tags[i] !== '') {
          let content = {
            name: tags[i],
            value: this.getRandomIntInclusive(20,30),
          }
          this.myTags.push(content)
          this.resTags.push(content)
        }
      }
      console.log(this.myTags)
      this.userdetail['userid']=sessionStorage.getItem('userId')
      this.userdetail['username']=res.userdetail.username
      this.userdetail['gender']=res.userdetail.gender
      this.userdetail['headportrait']=res.userdetail.headportrait
    })


    getTags().then(res => {
      let vm = this
      this.wordlist = res.message
      for (let i in res.message){
        let data = {
          name:res.message[i],
          value: this.getRandomIntInclusive(20,30),
        }
        this.cloud.push(data)
      }
      let maskImage = new Image();
      let image = GLOBAL.pic64
      maskImage.src = image
      let chart = echarts.init(document.getElementById('wordcloud'))
      chart.on('click', this.refreshTags);
      maskImage.onload  = function () { chart.setOption({
        backgroundColor: '#ffffff',
        tooltip: {
          show: true
        },
        series: [{
          type: 'wordCloud',
          shape: 'circle',
          left: 'center',
          top: 'center',
          right: null,
          bottom: null,
          sizeRange: [10, 20],
          autoSize: {
            enable: true,
            minSize: 10
          },
          maskImage: maskImage,
          rotationRange: [0, 0],
          rotationStep: 90,
          gridSize: 3,
          drawOutOfBound: false,
          layoutAnimation: true,
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
          data: vm.cloud,
        }]
      })
      }

      let myImage = new Image()
      if (String(this.userdetail['gender']) === '男' ){
        myImage.src = GLOBAL.pic64_boy
      } else {
        myImage.src = GLOBAL.pic64_girl
      }
      let mycloud = echarts.init(document.getElementById('mycloud'));
      mycloud.on('click', this.deleteUsertags);
      myImage.onload = function () {mycloud.setOption({
        backgroundColor: '#ffffff',
        tooltip: {
          show: true
        },
        series: [{
          name: '热词库',
          type: 'wordCloud',
          sizeRange: [10, 20],//value与图像像素的映射的最大值与最小值
          rotationRange: [0, 0],
          // shape: 'circle',
          textPadding: 0,
          autoSize: {
            enable: true,
            minSize: 10
          },
          rotationStep: 90,
          gridSize: 3,
          layoutAnimation: true,
          maskImage: myImage,
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
          drawOutOfBound: false,
          data: vm.myTags,
        }]
      })}
      this.charts = chart
    })
  }
}
</script>

<style scoped>
.el-icon-plus {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.el-icon-plus:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
.page{
  min-width:1200px;
}
.margin-left-10 {
  margin-left: 10px;
  margin-top: 30px;
}
</style>
