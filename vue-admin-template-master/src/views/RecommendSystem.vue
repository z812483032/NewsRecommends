<template>
    <div style="background:#eee;width: 100%; height: 100%; overflow: scroll;" >
        <Row>
            <Col span="8"  >
                <div style="background:#eee; padding: 20px;" :style="styObj" >
                    <Card :bordered="false">
                        <h3 slot="title">数据分析配置</h3>
                        <span>
                                <span style="margin-left: 5px; font-size: larger;">定时</span>
                                <span style="display: inline-block; float: right;">
                                    <TimePicker v-model="analysistime"
                                                :steps="[1, 3, 60]" placeholder="Time" style="width: 112px"></TimePicker>
                                </span><br/><br/><br/>
                                <span style="margin-left: 5px; font-size: larger;" >启动/关闭数据分析</span>
                                <span style="display: inline-block; float: right;">
                                    <i-switch v-model="analysisstate" @click.native="BeginAnalysis" />
                                </span>
                            </span>
                    </Card>
                    <Card :bordered="false" style="margin-top: 10px;">
                        <h3 slot="title">推荐配置</h3>
                        <span>
                                <span style="margin-left: 5px; font-size: larger;">定时推荐</span>
                                <span style="display: inline-block; float: right;">
                                    <TimePicker v-model="recommendtime"
                                                :steps="[1, 5, 60]" placeholder="Time" style="width: 112px"></TimePicker>
                                </span><br/><br/><br/>
                                <span style="margin-left: 5px; font-size: larger;" >启动/关闭推荐</span>
                                <span style="display: inline-block; float: right;">
                                    <i-switch v-model="recommendstate" @click.native="BeginRecommend" />
                                </span>
                            </span>
                    </Card>
                    <Card :bordered="false" style="margin-top: 10px;">
                        <h3 slot="title">运行情况</h3>
                        <ChartLint ref="chart_line_one" style="display: inline-block;"></ChartLint>
                    </Card>
                </div>
            </Col>
            <Col span="16">
                <div style="background:#eee;padding: 20px;" :style="styObj" >
                    <Card :bordered="false" style=" height: auto">
                        <h3 slot="title">新闻推荐日志</h3>
                        <Table style="height: auto" height="200" :columns="RecommendColumns"
                               :data="RecommendData" @on-row-click="downloadLog"></Table>
                    </Card>
                    <Card :bordered="false" style="margin-top: 10px;  height: auto;">
                        <h3 slot="title">数据分析日志</h3>
                        <Table style="height: auto" height="200" :columns="AnalysisColumns"
                               :data="AnalysisData" @on-row-click="downloadLog"></Table>
                    </Card>
                </div>
            </Col>
        </Row>
    </div>
</template>

<script>
import ChartLint from '../components/RecommendChartLint.vue'
import { recommendOff, recommendOn, analysisOn, analysisOff, getRecommendPageData } from '@/api'

export default {
    name: 'RecommendSystem',
    components: { ChartLint },
    mounted() {
        const {
            name,
            xData,
            yData,
        } = this
        console.log(this.$refs)
        this.$refs.chart_line_one.initChart(this.name, this.xData, this.yData)
        window.onresize = () => {
            this.screenHeight = document.body.clientHeight
            this.tableHeight = this.screenHeight - 10
            // this.circleWidth = window.innerHeight / 100 * 6.2
        }
    },
    data() {
        return {
            analysistime: '',
            analysisstate: false,
            recommendtime: '',
            recommendstate: false,
            name: '推荐量',
            xData: [],
            yData: [],
            RecommendColumns: [
                {
                    title: '日志名',
                    key: 'name',
                },
                {
                    title: '时间',
                    key: 'date',
                },
            ],
            RecommendData: [],
            AnalysisColumns: [
                {
                    title: '日志名',
                    key: 'name',
                },
                {
                    title: '时间',
                    key: 'date',
                },
            ],
            AnalysisData: [],
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
        BeginRecommend() {
            if (this.recommendstate === true) {
                let gettime = this.recommendtime
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
                    this.recommendstate = false
                } else {
                    recommendOn(time, gettime)
                    .then(res => {
                    })
                    this.$Message.info('推荐系统状态：打开')
                }
            } else if (this.recommendstate === false) {
                this.recommendstate = false
                recommendOff()
                .then(res => {
                    if (res.message === 'Success.') {
                        this.$Message.info('推荐系统状态：关闭')
                    }
                })
            }
        },
        BeginAnalysis() {
            if (this.analysisstate === true) {
                let gettime = this.analysistime
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
                    this.analysisstate = false
                } else {
                    analysisOn(time, gettime)
                    .then(res => {
                    })
                    this.$Message.info('推荐系统状态：打开')
                }
            } else if (this.analysisstate === false) {
                this.analysisstate = false
                analysisOff()
                .then(res => {
                    if (res.message === 'Success.') {
                        this.$Message.info('推荐系统状态：关闭')
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
        getRecommendPageData()
        .then(res => {
            console.log(res)
            if (Number(res.message.spiderstatelist[3][0]) === 1) {
                this.recommendstate = true
            }
            if (Number(res.message.spiderstatelist[4][0]) === 1) {
                this.analysisstate = true
            }
            this.recommendtime = res.message.spiderstatelist[3][1]
            this.analysistime = res.message.spiderstatelist[4][1]
            // eslint-disable-next-line no-unused-expressions,no-restricted-syntax,no-empty,guard-for-in
            for (let i in res.message.statistical) {
                this.xData.push(i)
                this.yData.push(res.message.statistical[i])
            }
            this.$refs.chart_line_one.initChart(this.name, this.xData, this.yData)
            // eslint-disable-next-line guard-for-in,no-restricted-syntax
            for (let i in res.message.reclist) {
                // console.log(i)
                if (String(i) === 'clg.log' || String(i) === 'hlg.log' || String(i) === 'rlg.log' || String(i) === 'log.log') continue
                let data = {
                    name: i,
                    date: res.message.reclist[i].time,
                    downloadlurl: res.message.reclist[i].filepath,
                }
                this.RecommendData.push(data)
            }
            // eslint-disable-next-line guard-for-in,no-restricted-syntax
            for (let i in res.message.analysisloglist) {
                // console.log(i)
                if (String(i) === 'ccg.log' || String(i) === 'hvg.log' || String(i) === 'hwg.log'
                    || String(i) === 'log.log' || String(i) === 'kwg.log') continue
                let data = {
                    name: i,
                    date: res.message.analysisloglist[i].time,
                    downloadlurl: res.message.analysisloglist[i].filepath,
                }
                this.AnalysisData.push(data)
            }
        })
    },
}
</script>

<style scoped>

</style>
