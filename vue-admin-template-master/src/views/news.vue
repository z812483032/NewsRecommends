<template>
    <div style="padding: 10px">
        <div style="background: #fff; border-radius: 8px; padding: 20px;">
            <div class="query-c">
                查询：
                <Input v-model="keyword" @on-change="searchNews" search placeholder="标题/新闻内容检索" style="width: auto" />
            </div>
            <br/>
            <div>
                <!--            <table v-for="item in news" :key="item.pk">{{item.pk}}</table>-->
                <Table :height="tableHeight"  border stripe :columns="columns1" :data="nowData" size="small" @mouseup="longText"></Table>
                <br/>
                <div class="pageBox" v-if="data1.length" >
                    <Page :total="parseInt(totalPage)"
                          :page-size="pageSize"
                          :page-size-opts="[10 ,20 ,30]"
                          show-elevator
                          show-total
                          show-sizer
                          @on-change="changepage"
                          @on-page-size-change="nowPageSize">
                    </Page>
                    <p>总共{{dataCount}}页</p>
                </div>
                <Drawer :closable="false" width="640" v-model="value3">
                    <h2 :style="pStyle">新闻详情</h2>
                    <p :style="pStyle">基本信息</p>
                    <div :model="news">
                        <div class="demo-drawer-profile">
                            <Row>
                                <Col span="12">
                                    <h5>标题:</h5> {{ this.news.title }}
                                </Col>
                            </Row>
                            <Divider />
                            <Row>
                                <Col span="12">
                                    <h5>发表日期:</h5> {{ this.news.date }}
                                </Col>
                                <Col span="12">
                                    <h5>类别:</h5> {{ this.news.category }}
                                </Col>
                            </Row>
                            <Divider />
                            <Row>
                                <Col span="30">
                                    <h5>原链接:</h5> <a v-bind:href=this.news.url target="_blank">{{ this.news.url }}</a>
                                </Col>
                            </Row>
                        </div>
                        <Divider />
                        <p :style="pStyle">图片素材</p>
                        <div class="demo-drawer-profile">
                            <Row>
                                <Col span="30">
                                    <p v-for="(item,index) in this.news.pic_url" :key="index">
                                        <a v-bind:href=item>{{item}}</a><br></p>
<!--                                    <a v-for="(item,index) in this.news.pic_url" :key="index" v-bind:href=item>{{ item }}</a><br>-->
                                </Col>
                            </Row>
                        </div>
                        <Divider />
                        <p :style="pStyle">视频素材</p>
                        <div class="demo-drawer-profile">
                        <Row>
                            <Col span="12">
                               {{ this.news.videourl }}
                            </Col>
                        </Row>

                    </div>
                    </div>
                </Drawer>
                <Modal
                    v-model="modal1"
                    title="确认中......."
                    @on-ok="delok"
                    @on-cancel="delcancel">
                    <h3>确认删除当前新闻吗？？</h3>
                </Modal>
            </div>
        </div>
    </div>
</template>

<script>


import { fetchNewsData, delNewsData, getSearchNewsResult } from '@/api'

export default {
    name: 'newslist',
    inject: ['reload'],
    mounted() {
        window.onresize = () => {
            this.screenHeight = document.body.clientHeight
            this.tableHeight = this.screenHeight - 300
        }
    },
    data() {
        return {
            keyword: '',
            tableHeight: window.innerHeight - 250,
            screenHeight: document.body.clientHeight,
            delnewsurl: '',
            modal1: false,
            pStyle: {
                fontSize: '16px',
                color: 'rgba(0,0,0,0.85)',
                lineHeight: '24px',
                display: 'block',
                marginBottom: '16px',
            },
            news: {
                title: '',
                url: '',
                date: '',
                category: '',
                pic_url: [],
                videourl: '',
                mainpage: '',
            },
            styles: {
                height: 'calc(100% - 55px)',
                overflow: 'auto',
                paddingBottom: '53px',
                position: 'static',
            },
            value3: false,
            totalPage: 0,
            pageSize: 10,
            dataCount: 0,
            pageCurrent: 1,
            nowData: [],
            columns1: [
                {
                    title: '标题',
                    key: 'title',
                    align: 'center',
                    render: (h, params) => {
                        let texts = params.row.title
                        if (params.row.title != null) {
                            if (params.row.title.length > 9) {
                                texts = params.row.title.slice(0, 8) + '...' // 进行数字截取
                            } else {
                                texts = params.row.title
                            }
                        }
                        return h('div', [
                            h('Tooltip', {
                                props: {
                                    placement: 'top',
                                    transfer: true,
                                },
                            }, [texts, h('span', {
                                slot: 'content',
                                style: {
                                    whiteSpace: 'normal',
                                },
                            }, params.row.title),
                            ]),
                        ])
                    },
                },
                {
                    title: '发布日期',
                    key: 'date',
                    align: 'center',
                },
                {
                    title: '原始链接',
                    key: 'url',
                    align: 'center',
                    render: (h, params) => {
                        let texts = params.row.url
                        if (params.row.url != null) {
                            if (params.row.url.length > 9) {
                                texts = params.row.url.slice(0, 15) + '...' // 进行数字截取
                            } else {
                                texts = params.row.url
                            }
                        }
                        return h('div', [
                            h('Tooltip', {
                                props: {
                                    placement: 'top',
                                    transfer: true,
                                },
                            }, [texts, h('span', {
                                slot: 'content',
                                style: {
                                    whiteSpace: 'normal',
                                },
                            }, params.row.url),
                            ]),
                        ])
                    },
                },
                {
                    title: '类别',
                    key: 'category',
                    align: 'center',
                    filters: [
                        {
                            label: '国内',
                            value: 1,
                        },
                        {
                            label: '财经',
                            value: 2,
                        },
                    ],
                    filterMultiple: false,
                    filterMethod(value, row) {
                        if (value === 1) {
                            return row.category == '国内'
                        } if (value === 2) {
                            return row.category == '财经'
                        }
                    },
                },
                {
                    title: '评论量',
                    key: 'comments',
                    align: 'center',
                },
                {
                    title: '阅读量',
                    key: 'readnum',
                    align: 'center',
                },
                {
                    title: '操作',
                    key: 'action',
                    width: 150,
                    align: 'center',
                    render: (h, params) => h('div', [
                        h('Button', {
                            props: {
                                type: 'primary',
                                size: 'small',
                            },
                            style: {
                                marginRight: '5px',
                            },
                            on: {
                                click: () => {
                                    let title = params.row.title
                                    let date = params.row.date
                                    // eslint-disable-next-line camelcase
                                    let pic_url = params.row.pic_url
                                    // eslint-disable-next-line no-eval,camelcase
                                    let pic_list = eval(pic_url)
                                    // console.log('pic_list', pic_list)
                                    let url = params.row.url
                                    let videourl = params.row.videourl
                                    let mainpage = params.row.mainpage
                                    let category = params.row.category
                                    if (videourl == 'None') {
                                        this.news.videourl = ''
                                    } else {
                                        this.news.videourl = videourl
                                    }
                                    this.news.title = title
                                    this.news.date = date
                                    // eslint-disable-next-line camelcase
                                    if (pic_url == '[]') {
                                        this.news.pic_url = ''
                                    } else {
                                        // eslint-disable-next-line camelcase
                                        this.news.pic_url = pic_list
                                        console.log('pic_url:', this.news.pic_url)
                                    }
                                    this.news.url = url
                                    this.news.mainpage = mainpage
                                    this.news.category = category
                                    console.log('params:', params)
                                    this.value3 = true
                                },
                            },
                        }, '详情'),
                        h('Button', {
                            props: {
                                type: 'error',
                                size: 'small',
                            },
                            on: {
                                click: () => {
                                    this.modal1 = true
                                    let url = params.row.url
                                    this.delnewsurl = url
                                },
                            },
                        }, '删除'),
                    ]),
                },

            ],
            data1: [],
            userInfo: '',
        }
    },
    methods: {
        searchNews() {
            getSearchNewsResult(this.keyword).then(res => {
                let listjson = JSON.parse(res.newslist)
                // console.log(listjson[1].fields)
                let a = []
                this.totalPage = listjson.length
                this.dataCount = Math.ceil(listjson.length / this.pageSize)
                // console.log('dataCount:', this.dataCount)
                // eslint-disable-next-line guard-for-in,no-restricted-syntax
                for (let i = 0; i < listjson.length; i++) {
                    let listjsonKey = listjson[i]
                    let dict = {}
                    // console.log('listjsonkey:', listjsonKey)
                    dict.title = listjsonKey.fields.title
                    dict.date = listjsonKey.fields.date
                    dict.mainpage = listjsonKey.fields.mainpage
                    dict.pic_url = listjsonKey.fields.pic_url
                    dict.videourl = listjsonKey.fields.videourl
                    let category = ''
                    let temp = listjsonKey.fields.category
                    switch (temp) {
                        case 0:
                            category = '美股'
                            break
                        case 1:
                            category = '国内'
                            break
                        case 2:
                            category = '国际'
                            break
                        case 3:
                            category = '社会'
                            break
                        case 4:
                            category = '体育'
                            break
                        case 5:
                            category = '娱乐'
                            break
                        case 6:
                            category = '军事'
                            break
                        case 7:
                            category = '科技'
                            break
                        case 8:
                            category = '财经'
                            break
                        case 9:
                            category = '股市'
                            break
                        default:
                            break
                    }
                    dict.category = category
                    dict.readnum = listjsonKey.fields.readnum
                    dict.url = listjsonKey.fields.url
                    dict.comments = listjsonKey.fields.comments
                    a.push(dict)
                }
                this.data1 = a
                this.nowData = []
                for (let i = 0; i < this.pageSize; i++) {
                    if (a[i] != null) {
                        this.nowData.push(a[i])
                    }
                }
            })
        },
        delok() {
            // eslint-disable-next-line no-undef
            delNewsData(this.delnewsurl).then(res => {
                console.log(res)
                if (res.message == 'Success.') {
                    this.$Message.info('删除成功')
                    this.reload()
                } else {
                    this.$Message.info('出错！请重试！')
                }
            })
        },
        delcancel() {
            this.$Message.info('取消')
        },
        longText(item) {
            item.render = (h, params) => {
                // 处理文字，溢出用点代替
                let txt = params.row[params.column.key]
                let tableTxt = null
                if (txt) {
                    if (txt.length > item.longText) {
                        tableTxt = txt.substring(0, item.longText) + '.....'
                    } else {
                        tableTxt = txt
                    }
                }

                return h('Tooltip', {
                    props: {
                        placement: 'top',
                    },
                }, [
                    tableTxt,
                    h('span', { slot: 'content', style: { whiteSpace: 'normal', wordBreak: 'break-all' } }, txt),
                ])
            }
            return item
        },
        changepage(index) {
            // console.log('index:', index)
            // eslint-disable-next-line no-underscore-dangle
            let _start = (index - 1) * this.pageSize
            // eslint-disable-next-line no-underscore-dangle
            let _end = index * this.pageSize
            this.nowData = this.data1.slice(_start, _end)
            this.pageCurrent = index
        },
        nowPageSize(index) {
            this.pageSize = index
        },
    },
    created() {
        fetchNewsData()
        .then(res => {
            let listjson = JSON.parse(res.newslist)
            // console.log(listjson[1].fields)
            let a = []
            this.totalPage = listjson.length
            this.dataCount = Math.ceil(listjson.length / this.pageSize)
            // console.log('dataCount:', this.dataCount)
            // eslint-disable-next-line guard-for-in,no-restricted-syntax
            for (let i = 0; i < listjson.length; i++) {
                let listjsonKey = listjson[i]
                let dict = {}
                // console.log('listjsonkey:', listjsonKey)
                dict.title = listjsonKey.fields.title
                dict.date = listjsonKey.fields.date
                dict.mainpage = listjsonKey.fields.mainpage
                dict.pic_url = listjsonKey.fields.pic_url
                dict.videourl = listjsonKey.fields.videourl
                let category = ''
                let temp = listjsonKey.fields.category
                switch (temp) {
                    case 0:
                        category = '美股'
                        break
                    case 1:
                        category = '国内'
                        break
                    case 2:
                        category = '国际'
                        break
                    case 3:
                        category = '社会'
                        break
                    case 4:
                        category = '体育'
                        break
                    case 5:
                        category = '娱乐'
                        break
                    case 6:
                        category = '军事'
                        break
                    case 7:
                        category = '科技'
                        break
                    case 8:
                        category = '财经'
                        break
                    case 9:
                        category = '股市'
                        break
                    default:
                        break
                }
                dict.category = category
                dict.readnum = listjsonKey.fields.readnum
                dict.url = listjsonKey.fields.url
                dict.comments = listjsonKey.fields.comments
                a.push(dict)
            }
            this.data1 = a
            for (let i = 0; i < this.pageSize; i++) {
                if (a[i] != null) {
                    this.nowData.push(a[i])
                }
            }
        })
    },
}


</script>

<style scoped>

</style>
