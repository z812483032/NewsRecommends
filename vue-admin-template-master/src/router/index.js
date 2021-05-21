import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const commonRoutes = [
    {
        path: '/login',
        name: 'login',
        meta: { title: '登录' },
        component: () => import('../components/Login.vue'),
    },
    {
        path: '/other', // 点击侧边栏跳到一个单独的路由页面，需要定义，层级和其他顶级路由一样
        name: 'other',
        meta: { title: '单独的路由' },
        component: () => import('../views/Other.vue'),
    },
    {
        path: '/404',
        name: '404',
        meta: { title: '404' },
        component: () => import('../components/404.vue'),
    },
    { path: '/', redirect: '/home' },
]

// 本地所有的页面 需要配合后台返回的数据生成页面
export const asyncRoutes = {
    home: {
        path: 'home',
        name: 'home',
        meta: { title: '主页' },
        component: () => import('../views/home/Home.vue'),
    },
    user: {
        path: 'user',
        name: 'user',
        meta: { title: '用户数据' },
        component: () => import('../views/user.vue'),
    },
    news: {
        path: 'news',
        name: 'news',
        meta: { title: '新闻数据' },
        component: () => import('../views/news.vue'),
    },
    password: {
        path: 'password',
        name: 'password',
        meta: { title: '修改密码' },
        component: () => import('../views/Password.vue'),
    },
    msg: {
        path: 'msg',
        name: 'msg',
        meta: { title: '通知消息' },
        component: () => import('../views/Msg.vue'),
    },
    userinfo: {
        path: 'userinfo',
        name: 'userinfo',
        meta: { title: '用户信息' },
        component: () => import('../views/UserInfo.vue'),
    },
    Spider: {
        path: 'Spider',
        name: 'Spider',
        meta: { title: '爬虫系统' },
        component: () => import('../views/Spider.vue'),
    },
    Recommend: {
        path: 'Recommend',
        name: 'Recommend',
        meta: { title: '推荐系统' },
        component: () => import('../views/RecommendSystem.vue'),
    },
    comments: {
        path: 'comments',
        name: 'comments',
        meta: { title: '推荐系统' },
        component: () => import('../views/Comments.vue'),
    },
}

const createRouter = () => new Router({
    routes: commonRoutes,
})

const router = createRouter()

export function resetRouter() {
    const newRouter = createRouter()
    router.matcher = newRouter.matcher
}

export default router
