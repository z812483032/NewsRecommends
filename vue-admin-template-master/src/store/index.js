import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        isShowLoading: false, // 全局 loading
        // 左侧菜单栏数据
        menuItems: [
            {
                name: 'home', // 要跳转的路由名称 不是路径
                size: 18, // icon大小
                type: 'md-home', // icon类型
                text: '概况', // 文本内容
            },
            // {
            //     name: 'other', // 要跳转的路由名称 不是路径
            //     size: 18, // icon大小
            //     type: 'ios-egg-outline', // icon类型
            //     text: '单独的路由', // 点击侧边栏跳到一个单独的路由页面，需要提前在 router.js 定义
            // },
            {
                size: 18, // icon大小
                type: 'md-arrow-forward', // icon类型
                text: '新闻中心',
                url: 'http://localhost:8080/#/home',
                isExternal: true, // 外链 跳到一个外部的 URL 页面
            },
            {
                text: '控制中心',
                type: 'ios-cube',
                children: [
                    {
                        type: 'ios-bug-outline',
                        name: 'Spider',
                        text: '爬虫系统',
                        // hidden 属性 隐藏此菜单 可以通过在地址栏上输入对应的 URL 来显示页面
                        // hidden: true,
                    },
                    {
                        type: 'ios-git-network',
                        name: 'Recommend',
                        text: '推荐系统',
                        // hidden 属性 隐藏此菜单 可以通过在地址栏上输入对应的 URL 来显示页面
                        // hidden: true,
                    },
                ],
            },
            {
                text: '数据中心',
                type: 'ios-paper',
                children: [
                    {
                        type: 'ios-grid',
                        name: 'news',
                        text: '新闻数据',
                        // hidden 属性 隐藏此菜单 可以通过在地址栏上输入对应的 URL 来显示页面
                        // hidden: true,
                    },
                    {
                        type: 'md-people',
                        name: 'user',
                        text: '用户数据',
                        // hidden 属性 隐藏此菜单 可以通过在地址栏上输入对应的 URL 来显示页面
                        // hidden: true,
                    },
                    {
                        type: 'ios-chatbubbles-outline',
                        name: 'comments',
                        text: '评论数据',
                        // hidden 属性 隐藏此菜单 可以通过在地址栏上输入对应的 URL 来显示页面
                        // hidden: true,
                    },
                ],
            },
            {
                text: '账户中心',
                type: 'ios-contact',
                children: [
                    {
                        type: 'md-lock',
                        name: 'password',
                        text: '修改密码',
                    },
                    // {
                    //     size: 18, // icon大小
                    //     type: 'md-arrow-forward', // icon类型
                    //     text: '外链',
                    //     url: 'https://www.baidu.com',
                    //     isExternal: true, // 外链 跳到一个外部的 URL 页面
                    // },
                ],
            },
        ],
    },
    mutations: {
        setMenus(state, items) {
            state.menuItems = [...items]
        },
        setLoading(state, isShowLoading) {
            state.isShowLoading = isShowLoading
        },
    },
})

export default store
