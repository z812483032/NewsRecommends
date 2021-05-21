import Vue from 'vue'
import axios from 'axios'
import ViewUI from 'view-design'
import App from './App'
import store from './store'
import router from './router'
import 'view-design/dist/styles/iview.css'
import './permission'
// eslint-disable-next-line import/order
import echarts from 'echarts'

Vue.config.productionTip = false
Vue.use(ViewUI)
Vue.prototype.$echarts = echarts
Vue.prototype.$axios = axios

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App),
})
