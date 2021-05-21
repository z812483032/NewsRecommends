<style lang="less">
@import 'style/common.less';
@import 'style/draggable-list.less';
</style>

<template>
  <div class="page" >
    <HeaderMenu></HeaderMenu>
    <div class="center_content" :height="fullHeight">
      <Scroll :height="this.fullHeight">
        <Row>
          <Col :lg="4"></Col>
          <Col :s="10" :md="10" :lg="20" style="margin-top: 10px;" >
            <Row type="flex">
              <Col :xxs="1" :xs="5" :md="10" :lg="18">
                <Card>
                  <h2 slot="title">头像</h2>
                  <Avatar shape="square" icon="ios-person" size="90"/>
                </Card>
                <Card style="margin-top: 10px;">
                  <h2 slot="title">账户详情</h2>
                  <h4 class="margin-left-10" >ID</h4>
                  <h4 class="margin-left-10" >用户名</h4>
                  <h4 class="margin-left-10" >性别</h4>
                  <Button type="primary" style="margin-top: 20px;" @click="modal1 = true">修改个人信息</Button>
                  <Modal
                    v-model="modal1"
                    title="Common Modal dialog box title"
                    @on-ok="ok"
                    @on-cancel="cancel">
                    <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="80">
                      <FormItem label="Password" prop="passwd">
                        <Input type="password" v-model="formCustom.passwd"></Input>
                      </FormItem>
                      <FormItem label="Confirm" prop="passwdCheck">
                        <Input type="password" v-model="formCustom.passwdCheck"></Input>
                      </FormItem>
                      <FormItem label="Age" prop="age">
                        <Input type="text" v-model="formCustom.age" number></Input>
                      </FormItem>
                      <FormItem>
                      </FormItem>
                    </Form>
                  </Modal>
                </Card>
                <Row style="margin-top: 10px;">
                  <Col span="24">
                    <Card>
                      <Row>
                        <Col span="12">
                          <Card dis-hover>
                            <p slot="title">
                              <Icon type="ios-list-outline"></Icon>
                              本周欲完成任务清单(拖拽到右侧删除)
                            </p>
                            <div style="height: 360px;">
                              <ul id="doList" class="iview-admin-draggable-list"></ul>
                            </div>
                          </Card>
                        </Col>
                        <Col span="12" class="padding-left-10">
                          <Card dis-hover>
                            <p slot="title">
                              <Icon type="ios-list"></Icon>
                              所剩任务清单(拖拽到左侧添加)
                            </p>
                            <div style="height: 360px;">
                              <ul id="todoList" class="iview-admin-draggable-list">
                                <li v-for="(item, index) in todoArray" :key="index" class="notwrap todolist-item" :data-index="index">
                                  {{ item.content }}
                                </li>
                              </ul>
                            </div>
                          </Card>
                        </Col>
                      </Row>
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
      </Scroll>
    </div>
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu";
import Sortable from 'sortablejs';
export default {
  name: "UserDetail",
  components: {HeaderMenu},
  data() {
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please enter your password'));
      } else {
        if (this.formCustom.passwdCheck !== '') {
          // 对第二个密码框单独验证
          this.$refs.formCustom.validateField('passwdCheck');
        }
        callback();
      }
    };
    const validatePassCheck = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please enter your password again'));
      } else if (value !== this.formCustom.passwd) {
        callback(new Error('The two input passwords do not match!'));
      } else {
        callback();
      }
    };
    const validateAge = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('Age cannot be empty'));
      }
      // 模拟异步验证效果
      setTimeout(() => {
        if (!Number.isInteger(value)) {
          callback(new Error('Please enter a numeric value'));
        } else {
          if (value < 18) {
            callback(new Error('Must be over 18 years of age'));
          } else {
            callback();
          }
        }
      }, 1000);
    };
    return{
      formCustom: {
        passwd: '',
        passwdCheck: '',
        age: ''
      },
      ruleCustom: {
        passwd: [
          { validator: validatePass, trigger: 'blur' }
        ],
        passwdCheck: [
          { validator: validatePassCheck, trigger: 'blur' }
        ],
        age: [
          { validator: validateAge, trigger: 'blur' }
        ]
      },

      modal1: false,
      doArray: [],
      fullHeight: document.documentElement.clientHeight-70,
      affordList: [],
      todoArray: [
        {
          content: '完成iview-admin基本开发'
        },
        {
          content: '对iview-admin进行性能优化'
        },
        {
          content: '对iview-admin的细节进行优化'
        },
        {
          content: '完成iview-admin开发'
        },
        {
          content: '解决发现的bug'
        },
        {
          content: '添加更多组件'
        },
        {
          content: '封装更多图表'
        },
        {
          content: '增加更多人性化功能'
        }
      ],
    }
  },
  methods: {
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.$Message.success('Success!');
        } else {
          this.$Message.error('Fail!');
        }
      })
    },
    handleReset (name) {
      this.$refs[name].resetFields();
    },
    ok() {
      this.$Message.info('Clicked ok');
    },
    cancel() {
      this.$Message.info('Clicked cancel');
    },
  },
  mounted () {
    document.body.ondrop = function (event) {
      event.preventDefault();
      event.stopPropagation();
    };
    let vm = this;
    let todoList = document.getElementById('todoList');
    Sortable.create(todoList, {
      group: {
        name: 'list',
        pull: true
      },
      animation: 120,
      ghostClass: 'placeholder-style',
      fallbackClass: 'iview-admin-cloned-item',
      onRemove (event) {
        vm.doArray.splice(event.newIndex, 0, vm.todoArray[event.item.getAttribute('data-index')]);
        console.log('doArray:', vm.doArray)
        console.log('todoArray:', vm.todoArray)
      }
    });
    let doList = document.getElementById('doList');
    Sortable.create(doList, {
      group: {
        name: 'list',
        pull: true
      },
      sort: false,
      filter: '.iview-admin-draggable-delete',
      animation: 120,
      fallbackClass: 'iview-admin-cloned-item',
      onRemove (event) {
        vm.doArray.splice(event.oldIndex, 1);
        console.log('doArray:', vm.doArray)
        console.log('todoArray:', vm.todoArray)
      }
    });
    let affordList = document.getElementById('affordList');
    Sortable.create(affordList, {
      group: {
        name: 'list',
        pull: true
      },
      sort: false,
      filter: '.iview-admin-draggable-delete',
      animation: 120,
      fallbackClass: 'iview-admin-cloned-item',
      onRemove (event) {
        vm.affordList.splice(event.oldIndex, 1);

      }
    });
  }
}
</script>

<style scoped>
.margin-left-10{
  margin-left: 10px;
  margin-top: 30px;
}
.margin-left-20{
  margin-left: 20px;
}
.margin-left-40{
  margin-left: 40px;
}
.margin-left-50{
  margin-left: 50px;
}
</style>
