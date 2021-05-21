import Vue from 'vue'
import Router from 'vue-router'


Vue.use(Router)

const commonRoutes = [
  {
    path: '/login',
    name: 'login',
    meta: { title: '登录' },
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/register',
    name: 'register',
    meta: { title: '登录' },
    component: () => import('../views/Register.vue'),
  },
  {
    path: '/404',
    name: '404',
    meta: { title: '404' },
    component: () => import('../components/404.vue'),
  },
  {
    path: '/home',
    name: 'home',
    meta: { title: '首页' },
    redirect:'/allnews',
    children:[
      {
        path: '/allnews',
        name: 'allnews',
        component: () => import('../components/AllNews'),
      },
      {
        path: '/domesticnews/:id',
        name: 'domesticnews',
        component: () => import('../components/DomesticNews'),
      }
    ],
    component: () => import('../views/home.vue'),
  },
  {
    path: '/user',
    name: 'user',
    meta: { title: '用户' },
    component: () => import('../views/UserDetail-demo.vue'),
  },
  {
    path: '/message',
    name: 'message',
    meta: { title: '消息' },
    component: () => import('../views/UserMessage.vue'),
  },
  {
    path: '/recommend',
    name: 'recommend',
    meta: { title: '为你推荐' },
    component: () => import('../views/NewsRecommend.vue'),
  },
  {
    path: '/eventhot',
    name: 'eventhot',
    meta: { title: '时事热点' },
    component: () => import('../views/CurrentEventHotSpot.vue'),
  },
  {
    path: '/newspage/:id',
    name: 'newspage',
    meta: { title: '详情' },
    component: () => import('../views/NewsDetail.vue'),
  },
  {
    path: '/history',
    name: 'history',
    meta: { title: '浏览记录' },
    component: () => import('../views/BrowsingHistory.vue'),
  },

  { path: '/', redirect: '/home' },
]

// 本地所有的页面 需要配合后台返回的数据生成页面
export const asyncRoutes = {
}

const createRouter = () => new Router({
  routes: commonRoutes,
  mode: 'history',
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  }
})

const router = createRouter()

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher
}

export default router
