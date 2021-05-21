<template>
    <div class="home-main" style="width: 100%; height: 100%; position: absolute; overflow: scroll;">
        <Row :gutter="10">
            <Col :md="24" :lg="10">
                <Row :gutter="10" style="margin-top: 20px;">
                    <Col :xs="24" :sm="12" :md="8" :style="{marginBottom: '10px'}">
                        <infor-card
                            id-name="usernum_count"
                            :end-val="count.usernum"
                            iconType="md-person-add"
                            color="#2d8cf0"
                            intro-text="平台总用户"
                        ></infor-card>
                    </Col>
                    <Col :xs="24" :sm="12" :md="8" :style="{marginBottom: '10px'}">
                        <infor-card
                            id-name="readnum_count"
                            :end-val="count.readnum"
                            iconType="ios-eye"
                            color="#64d572"
                            :iconSize="50"
                            intro-text="浏览量"
                        ></infor-card>
                    </Col>
                    <Col :xs="24" :sm="12" :md="8" :style="{marginBottom: '10px'}">
                        <infor-card
                            id-name="newsnum_count"
                            :end-val="count.newsnum"
                            iconType="md-cloud-upload"
                            color="#ffd572"
                            intro-text="新闻采集总量"
                        ></infor-card>
                    </Col>
                </Row>
                <Row :gutter="10" style="margin-top: 20px;">
                    <Col :xs="24" :sm="12" :md="8" :style="{marginBottom: '10px'}">
                        <infor-card
                            id-name="recnum_count"
                            :end-val="count.recnum"
                            iconType="ios-color-filter"
                            color="#2d8cf0"
                            intro-text="推荐总量"
                        ></infor-card>
                    </Col>
                    <Col :xs="24" :sm="12" :md="8" :style="{marginBottom: '10px'}">
                        <infor-card
                            id-name="comnum_count"
                            :end-val="count.comnum"
                            iconType="ios-eye"
                            color="#64d572"
                            :iconSize="50"
                            intro-text="评论总量"
                        ></infor-card>
                    </Col>
                    <Col :xs="24" :sm="12" :md="8" :style="{marginBottom: '10px'}">
                        <infor-card
                            id-name="likenum_count"
                            :end-val="count.likenum"
                            iconType="md-thumbs-up"
                            color="#ffd572"
                            intro-text="点赞总量"
                        ></infor-card>
                    </Col>
                </Row>
            </Col>
            <Col :md="24" :lg="14">
                <ChartLint ref="chart_line_one"></ChartLint>
            </Col>
        </Row>
        <Divider></Divider>
        <Row>
            <Col :md="24" :lg="24">
                <Row>
                    <Card :padding="0">
                        <p slot="title" class="card-title">
                            <Icon type="map"></Icon>
                            用户分布情况
                        </p>
                        <div class="map-con">
                            <Col span="10">
                                <map-data-table :cityData="cityData" height="281" :style-obj="{margin: '12px 0 0 11px'}"></map-data-table>
                            </Col>
                            <Col span="14" class="map-incon">
                                <Row type="flex" justify="center" align="middle">
                                    <home-map :city-data="cityData"></home-map>
                                </Row>
                            </Col>
                        </div>
                    </Card>
                </Row>
            </Col>
        </Row>
    </div>
</template>

<script>
import * as echarts from 'echarts'
import ChartLint from '../../components/MainPageChartLint'
import inforCard from './components/inforCard.vue'
import countUp from './components/countUp'
import homeMap from './components/map.vue'
import mapDataTable from './components/mapDataTable.vue'
import { getData } from '@/api'

export default {
    name: 'home',
    created() {},
    // eslint-disable-next-line vue/no-unused-components
    components: { ChartLint, inforCard, countUp, homeMap, mapDataTable },
    mounted() {
        getData().then(res => {
            console.log(res)
            this.count.usernum = res.message.usernum
            this.count.readnum = res.message.readnum
            this.count.newsnum = res.message.newsnum
            this.count.recnum = res.message.recnum
            this.count.comnum = res.message.comnum
            this.count.likenum = res.message.likenum
            // eslint-disable-next-line guard-for-in,no-restricted-syntax
            for (let i in res.message.statistical) {
                this.xData.push(i)
                this.yData.push(res.message.statistical[i])
            }
            // eslint-disable-next-line guard-for-in,no-restricted-syntax
            for (let i in res.message.regionlist) {
                if (i === '') {
                    let data = {
                        name: '未知',
                        value: res.message.regionlist[i],
                    }
                    this.cityData.push(data)
                    continue
                }
                let data = {
                    name: i,
                    value: res.message.regionlist[i],
                }
                console.log(data)
                this.cityData.push(data)
            }
            let map = echarts.init(document.getElementById('home_page_map'))
            // eslint-disable-next-line import/no-unresolved
            const chinaJson = require('./components/map-data/china.json')
            echarts.registerMap('china', chinaJson)
            map.setOption({
                visualMap: { // 地图图例
                    show: true,
                    pieces: [ // 根据数据大小，各省显示不同颜色
                        {
                            gte: 100,
                            label: '>= 100',
                            color: '#ef2929',
                        },
                        {
                            gte: 70,
                            lt: 99,
                            label: '70 - 99',
                            color: '#ff5c5c',
                        },
                        {
                            gte: 50,
                            lt: 69,
                            label: '50 - 69',
                            color: '#ff9090',
                        },
                        {
                            gte: 10,
                            lt: 49,
                            label: '10 - 49',
                            color: '#ffc8c8',
                        },
                        {
                            lt: 10,
                            label: '<10',
                            color: '#e3b7b7',
                        },
                    ],
                },
                geo: { // 中国地图设置
                    map: 'china',
                    scaleLimit: {
                        min: 1,
                        max: 5,
                    },
                    zoom: 1,
                    itemStyle: {
                        normal: {
                            borderColor: 'rgba(0, 0, 0, 0.2)',
                        },
                        emphasis: {
                            areaColor: '#a0d8e8',
                            shadowOffsetX: 0,
                            shadowOffsetY: 0,
                            borderWidth: 0,
                        },
                    },
                },
                series: [
                    {
                        name: '突发事件',
                        type: 'map',
                        geoIndex: 0,
                        data: this.cityData,
                    },
                ],
            })
            this.$refs.chart_line_one.initChart(this.name, this.xData, this.yData)
        })
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
            cityData: [],
            count: {
                usernum: 496,
                readnum: 3264,
                newsnum: 24389305,
                recnum: 39503498,
                comnum: 1111,
                likenum: 22222,
            },
            name: '推荐访问量',
            xData: [],
            yData: [],
            // circleWidth: window.innerHeight / 100 * 6.2,
            screenHeight: document.body.clientHeight,
        }
    },
    computed: {
        color() {
            let color = '#2db7f5'
            if (this.percent == 100) {
                color = '#5cb85c'
            }
            return color
        },
    },
}
</script>

<style scoped>
.home-container {
    padding: 10px;
    padding-top: 5px;
}

.home-content {
    padding: 10px;
    border-radius: 5px;
    background: #fff;
}
</style>
<style lang="less">
.demo-Circle-custom {
    & h1 {
        color: #3f414d;
        font-size: 28px;
        font-weight: normal;
    }

    & p {
        color: #657180;
        font-size: 14px;
        margin: 10px 0 15px;
    }

    & span {
        display: block;
        padding-top: 15px;
        color: #657180;
        font-size: 14px;

        &:before {
            content: '';
            display: block;
            width: 50px;
            height: 1px;
            margin: 0 auto;
            background: #e0e3e6;
            position: relative;
            top: -15px;
        }
    ;
    }

    & span i {
        font-style: normal;
        color: #3f414d;
    }
}
</style>
