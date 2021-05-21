// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import 'view-design/dist/styles/iview.css'
import ViewUI from 'view-design'
import vuescroll from "vuescroll";//引入vuescroll
import "vuescroll/dist/vuescroll.css";//引入vuescroll样式
import VideoPlayer from 'vue-video-player'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
require('video.js/dist/video-js.css')
require('vue-video-player/src/custom-theme.css')
Vue.use(VideoPlayer)
Vue.use(ElementUI);
Vue.use(vuescroll);//使用
Vue.config.productionTip = false
Vue.use(ViewUI)
Vue.prototype.$axios = axios

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
