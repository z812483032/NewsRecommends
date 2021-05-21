<template>
    <div style="width:calc(100% - 10px);height:305px;background: #ffffff; " id="home_page_map"></div>
</template>

<script>
import * as echarts from 'echarts'
import geoData from './map-data/get-geography-value.js'

export default {
    name: 'homeMap',
    props: {
        cityData: Array,
    },
    mounted() {
        let convertData = function (data) {
            let res = []
            let len = data.length
            for (let i = 0; i < len; i++) {
                let geoCoord = geoData[data[i].name]
                if (geoCoord) {
                    res.push({
                        name: data[i].name,
                        value: geoCoord.concat(data[i].value),
                    })
                }
            }
            return res
        }

        let map = echarts.init(document.getElementById('home_page_map'))
        const chinaJson = require('./map-data/china.json')
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
                // top: 120,
                // label: {
                //     normal: {
                //         // show: true,
                //         fontSize: '14',
                //         color: 'rgba(0,0,0,0.7)',
                //     },
                // },
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
        window.addEventListener('resize', () => {
            map.resize()
        })
    },
}
</script>
