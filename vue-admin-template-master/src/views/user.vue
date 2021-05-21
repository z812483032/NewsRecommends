<template>
    <div style="padding: 10px">
        <div style="background: #fff; border-radius: 8px; padding: 20px;">
            <div class="query-c">
                查询：
                <Input search v-model="keyword"
                       @on-change="searchUser"
                       placeholder="用户ID/用户名/标签检索" style="width: auto" />
            </div>
            <br>
            <Table max-height="400" border stripe :columns="columns1" :data="nowData"></Table>
            <br>
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
            <div>
                <Drawer
                    title="修改用户信息"
                    v-model="value3"
                    width="720"
                    :mask-closable="false"
                    :styles="styles">
                    <Form :model="this.line">
                        <Row :gutter="32">
                            <Col span="12">
                                <FormItem label="用户名" label-position="top">
                                    <Input v-model="line.username" placeholder="修改用户名" />
                                </FormItem>
                            </Col>
                            <Col span="12">
                                <FormItem label="ID" label-position="top">
                                    <Input v-model="line.userid" placeholder="修改ID" disabled></Input>
                                </FormItem>
                            </Col>
                        </Row>
                        <Row :gutter="32">
                            <Col span="12">
                                <FormItem label="标签" label-position="top">
                                    <Input v-model="line.tags" placeholder="修改标签"></Input>
                                </FormItem>
                            </Col>
                            <Col span="12">
                                <FormItem label="性别" label-position="top">
                                    <Select v-model="line.gender" placeholder="修改性别">
                                        <Option value="男">男</Option>
                                        <Option value="女">女</Option>
                                    </Select>
                                </FormItem>
                            </Col>
                        </Row>
                        <Row :gutter="32">
                            <Col span="12">
                                <FormItem label="IP地址" label-position="top">
                                    <Input v-model="line.ip" placeholder="更改IP"></Input>
                                </FormItem>
                            </Col>
                        </Row>
                        <FormItem>
                            <div class="demo-drawer-footer">
                                <Button style="margin-right: 8px" @click="value3 = false">返回</Button>
                                <Button type="primary" @click="userupdate(line)">提交</Button>
                            </div>
                        </FormItem>
                    </Form>
                    <Divider />
                </Drawer>
                <div>
<!--                    <Button type="primary" @click="modal1 = true">Display dialog box</Button>-->
                    <Modal
                        v-model="modal1"
                        title="确认中......."
                        @on-ok="delok"
                        @on-cancel="delcancel">
                        <h3>确认删除当前用户吗？？</h3>
                    </Modal>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import { delUserData, fetchUserData, getSearchUserResult, updateUserData } from '@/api'

export default {
    name: 't1',
    inject: ['reload'],
    data() {
        return {
            deluserid: '',
            modal1: false,
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
                    key: 'userid',
                    align: 'center',
                },
                {
                    title: '用户名',
                    key: 'username',
                    align: 'center',
                },
                {
                    title: '性别',
                    key: 'gender',
                    align: 'center',
                },
                {
                    title: 'IP地址',
                    key: 'ip',
                    align: 'center',
                },
                {
                    title: '标签',
                    key: 'tags',
                    align: 'center',
                },
                {
                    title: '操作',
                    key: 'action',
                    width: 150,
                    align: 'center',
                    // eslint-disable-next-line no-return-assign
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
                                    let username = params.row.username
                                    let userid = params.row.userid
                                    let tags = params.row.tags
                                    let gender = params.row.gender
                                    let ip = params.row.ip
                                    this.line.gender = gender
                                    this.line.userid = userid
                                    this.line.username = username
                                    this.line.tags = tags
                                    this.line.ip = ip
                                    console.log(this.line.gender)
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
                                    let userid = params.row.userid
                                    // eslint-disable-next-line no-undef
                                    this.deluserid = userid
                                    console.log('userid:', this.deluserid)
                                },
                            },
                        }, '删除'),
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
        searchUser() {
            getSearchUserResult(this.keyword).then(res => {
                let listjson = JSON.parse(res.userlist)
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
                    dict.userid = listjsonKey.pk
                    dict.username = listjsonKey.fields.username
                    if (listjsonKey.fields.gender == 1) {
                        dict.gender = '男'
                    } else {
                        dict.gender = '女'
                    }
                    dict.ip = listjsonKey.fields.ip
                    dict.tags = listjsonKey.fields.tags
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
        userupdate(line) {
            console.log('line:', line.userid)
            this.value3 = false
            let userid = line.userid
            let username = line.username
            let gender = line.gender
            let ip = line.ip
            let tags = line.tags
            updateUserData(userid, username, gender, ip, tags).then(res => {
                if (res.message == 'Success.') {
                    this.$Message.info('修改成功')
                } else {
                    this.$Message.info('出错！请重试！')
                }
            })
            this.reload()
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
            delUserData(this.deluserid).then(res => {
                console.log(res)
                if (res.message == 'Success.') {
                    this.$Message.info('删除成功')
                } else {
                    this.$Message.info('出错！请重试！')
                }
            })
        },
        delcancel() {
            this.$Message.info('取消')
        },
    },
    created() {
        fetchUserData()
        .then(res => {
            let listjson = JSON.parse(res.userlist)
            console.log(listjson)
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
                dict.userid = listjsonKey.pk
                dict.username = listjsonKey.fields.username
                if (listjsonKey.fields.gender == 1) {
                    dict.gender = '男'
                } else {
                    dict.gender = '女'
                }
                dict.ip = listjsonKey.fields.ip
                dict.tags = listjsonKey.fields.tags
                a.push(dict)
            }
            this.data1 = a
            console.log('data1:', this.data1)
            for (let i = 0; i < this.pageSize; i++) {
                if (a[i] != null) {
                    this.nowData.push(a[i])
                }
            }
            console.log('nowData:', this.nowData)
            // this.data1 =
            // console.log(this.data1)
        })
    },
}
</script>

<style scoped>

</style>
