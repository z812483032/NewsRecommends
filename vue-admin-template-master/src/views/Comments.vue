<template>
    <div style="padding: 10px">
        <div style="background: #fff; border-radius: 8px; padding: 20px;">
            <div class="query-c">
                查询：
                <Input search v-model="keyword"
                       @on-change="searchComments"
                       placeholder="评论内容/用户ID/新闻ID检索" style="width: auto" />
            </div>
            <br>
            <Table max-height="400" border stripe :columns="columns1" :data="nowData"></Table>
            <br>
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
            <div>
                <div>
                    <Modal
                        v-model="modal1"
                        title="确认中......."
                        @on-ok="delok"
                        @on-cancel="delcancel">
                        <h3>确认封禁当前评论吗？？</h3>
                    </Modal>
                    <Modal
                        v-model="modal2"
                        title="确认中......."
                        @on-ok="Unlockok"
                        @on-cancel="Unlockcancel">
                        <h3>确认解封当前评论吗？？</h3>
                    </Modal>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import { delCommentData, fetchCommentsData, getSearchCommentsResult } from '@/api'

export default {
    name: 'comments',
    inject: ['reload'],
    data() {
        return {
            delcommentsid: '',
            modal1: false,
            modal2: false,
            temp: {},
            line: {
                userid: '',
                username: '',
                gender: '',
                ip: '',
                tags: '',
            },
            pStyle: {
                fontSize: '16px',
                color: 'rgba(0,0,0,0.85)',
                lineHeight: '24px',
                display: 'block',
                marginBottom: '16px',
            },
            styles: {
                height: 'calc(100% - 55px)',
                overflow: 'auto',
                paddingBottom: '53px',
                position: 'static',
            },
            totalPage: 0,
            pageSize: 10,
            dataCount: 0,
            pageCurrent: 1,
            columns1: [
                {
                    title: 'ID',
                    key: 'id',
                    align: 'center',
                },
                {
                    title: '新闻ID',
                    key: 'newsid',
                    align: 'center',
                },
                {
                    title: '评论内容',
                    key: 'comments',
                    align: 'center',
                },
                {
                    title: '发送用户ID',
                    key: 'userid',
                    align: 'center',
                },
                {
                    title: '被评论用户ID',
                    key: 'touserid',
                    align: 'center',
                },
                {
                    title: '时间',
                    key: 'time',
                    align: 'center',
                },
                {
                    title: '评论状态',
                    key: 'status',
                    align: 'center',
                },
                {
                    title: '操作',
                    key: 'action',
                    width: 150,
                    align: 'center',
                    // eslint-disable-next-line no-return-assign
                    render: (h, params) => h('div', [
                        (params.row.status === '正常') && h('Button', {
                            props: {
                                type: 'error',
                                size: 'small',
                            },
                            style: {
                                marginRight: '5px',
                            },
                            on: {
                                click: () => {
                                    this.delcommentsid = params.row.id
                                    this.temp = params.row
                                    this.modal1 = true
                                },
                            },
                        }, '封禁'),
                        (params.row.status === '封禁') && h('Button', {
                            props: {
                                type: 'primary',
                                size: 'small',
                            },
                            style: {
                                marginRight: '5px',
                            },
                            on: {
                                click: () => {
                                    this.delcommentsid = params.row.id
                                    this.temp = params.row
                                    this.modal2 = true
                                },
                            },
                        }, '解封'),
                    ]),
                },
            ],
            data1: [],
            nowData: [],
            user: '',
            keyword: '',
            value3: false,
        }
    },
    methods: {
        searchComments() {
            getSearchCommentsResult(this.keyword).then(res => {
                let listjson = JSON.parse(res.commentslist)
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
                    dict.id = listjsonKey.pk
                    dict.newsid = listjsonKey.fields.newsid
                    dict.comments = listjsonKey.fields.comments
                    dict.userid = listjsonKey.fields.userid
                    dict.touserid = listjsonKey.fields.touserid
                    dict.time = listjsonKey.fields.time
                    dict.status = listjsonKey.fields.status
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
        changepage(index) {
            console.log('index:', index)
            // eslint-disable-next-line no-underscore-dangle
            let _start = (index - 1) * this.pageSize
            // eslint-disable-next-line no-underscore-dangle
            let _end = index * this.pageSize
            console.log(_start)
            console.log(_end)
            this.nowData = this.data1.slice(_start, _end)
            this.pageCurrent = index
        },
        nowPageSize(index) {
            this.pageSize = index
        },
        delok() {
            delCommentData(this.delcommentsid, this.temp.userid, this.temp.newsid, 1).then(res => {
                console.log(res)
                if (res.message == 'Success.') {
                    this.$Message.info('封禁成功')
                    this.temp.status = '封禁'
                } else {
                    this.$Message.info('出错！请重试！')
                }
            })
        },
        delcancel() {
            this.$Message.info('取消')
        },
        Unlockok() {
            delCommentData(this.delcommentsid, this.temp.userid, this.temp.newsid, 0).then(res => {
                console.log(res)
                if (res.message == 'Success.') {
                    this.$Message.info('解封成功')
                    this.temp.status = '正常'
                } else {
                    this.$Message.info('出错！请重试！')
                }
            })
        },
        Unlockcancel() {
            this.$Message.info('取消')
        },
    },
    created() {
        fetchCommentsData()
        .then(res => {
            console.log(res)
            let listjson = JSON.parse(res.commentslist)
            console.log('sss', listjson)
            let a = []
            this.totalPage = listjson.length
            console.log(this.totalPage)
            this.dataCount = Math.ceil(listjson.length / this.pageSize)
            console.log('dataCount:', this.dataCount)
            for (let i = 0; i < listjson.length; i++) {
                let listjsonKey = listjson[i]
                let dict = {}
                // console.log('listjsonkey:', listjsonKey)
                dict.id = listjsonKey.pk
                dict.newsid = listjsonKey.fields.newsid
                dict.comments = listjsonKey.fields.comments
                dict.userid = listjsonKey.fields.userid
                dict.touserid = listjsonKey.fields.touserid
                dict.time = listjsonKey.fields.time
                dict.status = listjsonKey.fields.status
                a.push(dict)
            }
            this.data1 = a
            console.log('data1:', this.data1)
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
