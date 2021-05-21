<template>
  <div class="main-page">
    <HeaderMenu :activename="9"></HeaderMenu>
    <Scroll :height="screenHeight">
    <Row span="24" :height="screenHeight">
        <Col :lg="3"></Col>
        <Col :lg="18">
          <h1>阅读记录</h1>
          <Divider></Divider>
          <Card style="margin-bottom: 15px;">
            <Row>
              <Col :lg="21">
                <h4>标题1</h4>
              </Col>
              <Col :lg="3">
                <p>2020-10-21 14:21</p>
              </Col>
            </Row>
          </Card>
          <Card style="margin-bottom: 15px;">
            <Row>
              <Col :lg="21">
                <h4>标题1</h4>
              </Col>
              <Col :lg="3">
                <p>2020-10-21 14:21</p>
              </Col>
            </Row>
          </Card>
          <Card style="margin-bottom: 15px;">
            <Row>
              <Col :lg="21">
                <h4>标题1</h4>
              </Col>
              <Col :lg="3">
                <p>2020-10-21 14:21</p>
              </Col>
            </Row>
          </Card>
          <Card style="margin-bottom: 15px;">
            <Row>
              <Col :lg="21">
                <h4>标题1</h4>
              </Col>
              <Col :lg="3">
                <p>2020-10-21 14:21</p>
              </Col>
            </Row>
          </Card>
        </Col>
        <Col :lg="3"></Col>
    </Row>
    </Scroll>
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu";
export default {
  name: "BrowsingHistory",
  components: {HeaderMenu},
  data() {
    return{
      screenHeight: document.documentElement.clientHeight - 65,
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
    }
  },
}
</script>

<style scoped>

</style>
