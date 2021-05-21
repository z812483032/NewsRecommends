<template>
    <div style="background:#eee; width: 100%; height: 100%; overflow: scroll;">
        <Row>
            <Col span="8">
                <div style="background:#eee;padding: 20px;" :style="styObj">
                    <Card :bordered="false">
                        <h3 slot="title">URL采集配置</h3>
                        <span>
                                <span style="margin-left: 5px; font-size: larger;">时间间隔</span>
                                <span style="display: inline-block; float: right;">
                                    <TimePicker v-model="urltime" :steps="[1, 1, 30]" placeholder="Time"
                                                style="width: 112px"></TimePicker>
                                </span>
                                <br/><br/><br/>
                                <span style="margin-left: 5px; font-size: larger;">启动爬虫</span>
                                <span style="display: inline-block; float: right;">
                                    <i-switch v-model="urlstate" @click.native="BeginUrlSpider"/></span>
                            </span>
                    </Card>
                    <Card :bordered="false" style="margin-top: 20px;">
                        <h3 slot="title">新闻详情采集配置</h3>
                        <span>
                                <span style="margin-left: 5px; font-size: larger;">时间间隔</span>
                                <span style="display: inline-block; float: right;">
                                    <TimePicker v-model="detailtime" :steps="[1, 1, 30]"
                                                placeholder="Time" style="width: 112px"></TimePicker>
                                </span>
                                <br/><br/><br/>
                                <span style="margin-left: 5px; font-size: larger;">启动爬虫</span>
                                <span style="display: inline-block; float: right;">
                                    <i-switch v-model="detailstate" @click.native="BeginDetailSpider"/></span>
                            </span>
                    </Card>
                    <Card :bordered="false" style="margin-top: 20px;">
                        <h3 slot="title">运行情况</h3>
                        <ChartLint ref="chart_line_one" style="display: inline-block;"></ChartLint>
                    </Card>
                </div>
            </Col>
            <Col span="16">
                <div style="background:#eee;padding: 20px; " :style="styObj">
                    <Card :bordered="false">
                        <h3 slot="title">URL采集日志</h3>
                        <Table height="200"
                               :columns="UrlColumns" :data="UrlData" @on-row-click="downloadLog"></Table>
                    </Card>
                    <Card :bordered="false" style="margin-top: 10px;">
                        <h3 slot="title">详情采集日志</h3>
                        <Table height="200" :columns="DetailColumns" :data="DetailData"
                               @on-row-click="downloadLog"></Table>
                    </Card>
                    <Card :bordered="false" style="margin-top: 10px;">
                        <h3 slot="title">注意事项</h3>
                        <Collapse height="200">
                            <Panel name="1">
                                重启爬虫
                                <p slot="content">爬虫重启为强制性重启，该操作可能会造成之前采集未来得及存入数据库的内容丢失请注意！尽量在空闲时使用该功能，避免数据丢失</p>
                            </Panel>
                            <Panel name="2">
                                关闭爬虫
                                <p slot="content">关闭爬虫意味着近期将无法获取到最新的新闻内容，请酌情使用该功能</p>
                            </Panel>
                        </Collapse>
                    </Card>
                </div>
            </Col>
        </Row>
    </div>
</template>

<script>
import ChartLint from '../components/SpiderChartLint'
import { urlspider, getSpiderPageData, closeurlspider, closedetailspider, detailspider, download } from '@/api'

export default {
    components: { ChartLint },
    name: 'Spider',
    mounted() {
        const {
            name,
            xData,
            yData,
        } = this
        window.onresize = () => {
            this.screenHeight = document.body.clientHeight
            this.tableHeight = this.screenHeight - 10
            // this.circleWidth = window.innerHeight / 100 * 6.2
        }
    },
    data() {
        return {
            urlstate: false,
            detailstate: false,
            urltime: '',
            detailtime: '',
            name: '新闻采集量',
            xData: [],
            yData: [],
            UrlColumns: [
                {
                    title: '日志文件名',
                    key: 'name',
                },
                {
                    title: '时间',
                    key: 'date',
                },
            ],
            UrlData: [],
            DetailColumns: [
                {
                    title: '日志文件名',
                    key: 'name',
                },
                {
                    title: '时间',
                    key: 'date',
                },
            ],
            DetailData: [],
            styObj: {
                height: 0,
            },
            switch1: false,
        }
    },
    methods: {
        downloadLog(render) {
            this.$Loading.start()
            let url = 'http://localhost:8000/download/logs/?filepath=' + render.downloadlurl
            window.location.href = url
            this.$Loading.finish()
        },
        BeginDetailSpider() {
            if (this.detailstate === true) {
                let gettime = this.detailtime
                let temp = gettime.split(':')
                let time = 0
                if (temp.length !== 1 && temp[0] !== '00') {
                    // console.log('temp[0]:', Number(temp[0]))
                    time += Number(temp[0]) * 60 * 60
                }
                if (temp.length !== 1 && temp[1] !== '00') {
                    // console.log('temp[0]:', Number(temp[0]))
                    time += Number(temp[1]) * 60
                }
                if (temp.length !== 1 && temp[2] !== '00') {
                    // console.log('temp[0]:', Number(temp[0]))
                    time += Number(temp[2])
                }
                // eslint-disable-next-line use-isnan
                if (time === 0) {
                    // this.urlstate = Object.assign({}, this.urlstate)
                    this.$Message.error('请选择间隔时间')
                    this.detailstate = false
                } else {
                    detailspider(time, gettime)
                    .then(res => {
                    })
                    this.$Message.info('详情爬虫状态：打开')
                }
            } else if (this.detailstate === false) {
                this.detailstate = false
                closedetailspider()
                .then(res => {
                    if (res.message === 'Success.') {
                        this.$Message.info('详情爬虫状态：关闭')
                    }
                })
            }
        },
        BeginUrlSpider() {
            if (this.urlstate === true) {
                let gettime = this.urltime
                let temp = gettime.split(':')
                let time = 0
                if (temp.length !== 1 && temp[0] !== '00') {
                    // console.log('temp[0]:', Number(temp[0]))
                    time += Number(temp[0]) * 60 * 60
                }
                if (temp.length !== 1 && temp[1] !== '00') {
                    // console.log('temp[0]:', Number(temp[0]))
                    time += Number(temp[1]) * 60
                }
                if (temp.length !== 1 && temp[2] !== '00') {
                    // console.log('temp[0]:', Number(temp[0]))
                    time += Number(temp[2])
                }
                // eslint-disable-next-line use-isnan
                if (time === 0) {
                    // this.urlstate = Object.assign({}, this.urlstate)
                    this.$Message.error('请选择间隔时间')
                    this.urlstate = false
                } else {
                    urlspider(time, gettime)
                    .then(res => {
                    })
                    this.$Message.info('Url爬虫状态：打开')
                }
            } else if (this.urlstate === false) {
                this.urlstate = false
                closeurlspider()
                .then(res => {
                    if (res.message === 'Success.') {
                        this.$Message.info('Url爬虫状态：关闭')
                    }
                })
            }
        },
        change(status) {
            this.$Message.info('开关状态：' + status)
        },
        changeHeight() {
            this.styObj.height = window.innerHeight - 0 + 'px'
        },
    },
    created() {
        window.addEventListener('resize', this.changeHeight)
        this.changeHeight()
        getSpiderPageData()
        .then(res => {
            if (Number(res.message.spiderstatelist[1][0]) === 1) {
                this.urlstate = true
            }
            if (Number(res.message.spiderstatelist[2][0]) === 1) {
                this.detailstate = true
            }
            this.urltime = res.message.spiderstatelist[1][1]
            this.detailtime = res.message.spiderstatelist[2][1]
            // eslint-disable-next-line no-unused-expressions,no-restricted-syntax,no-empty,guard-for-in
            for (let i in res.message.statistical) {
                this.xData.push(i)
                this.yData.push(res.message.statistical[i])
            }
            this.$refs.chart_line_one.initChart(this.name, this.xData, this.yData)
            // eslint-disable-next-line guard-for-in,no-restricted-syntax
            for (let i in res.message.urlloglist) {
                // console.log(i)
                if (String(i) === 'clg.log' || String(i) === 'hlg.log' || String(i) === 'rlg.log' || String(i) === 'log.log') continue
                let data = {
                    name: i,
                    date: res.message.urlloglist[i].time,
                    downloadlurl: res.message.urlloglist[i].filepath,
                }
                this.UrlData.push(data)
            }
            // eslint-disable-next-line guard-for-in,no-restricted-syntax
            for (let i in res.message.detaillist) {
                // console.log(i)
                if (String(i) === 'clg.log' || String(i) === 'hlg.log' || String(i) === 'rlg.log' || String(i) === 'log.log') continue
                let data = {
                    name: i,
                    date: res.message.detaillist[i].time,
                    downloadlurl: res.message.detaillist[i].filepath,
                }
                this.DetailData.push(data)
            }
        })
    },
}
</script>

<style scoped>

</style>
