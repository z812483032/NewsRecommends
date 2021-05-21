<template>
    <div class="echart" id="echart-line" style="white-space: nowrap;" :style="{  width: '100%', height: '160%' } "></div>
</template>

<script>
import * as echarts from 'echarts'

export default {
    name: 'chartLint',

    methods: {

        initChart(name, xData, yData) {
            let getchart = echarts.init(document.getElementById('echart-line'))
            let option = {
                tooltip: {
                    trigger: 'axis',
                },
                legend: {
                    data: [name],
                    bottom: '0%',
                },
                grid: { // 调整图表上下左右位置
                    top: '10%',
                    left: '3%',
                    right: '8%',
                    bottom: '11%',
                    containLabel: true,
                },

                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: xData,
                    axisLine: {
                        lineStyle: {
                            color: 'rgba(12,102,173,.5)',
                        },
                    },
                },
                yAxis: {
                    type: 'value',
                },
                series: [
                    {
                        name,
                        type: 'line',
                        stack: '总量',
                        data: yData,
                        smooth: true,
                        lineStyle: {
                            width: 0,
                        },
                        showSymbol: false,
                        areaStyle: {
                            opacity: 0.8,
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(128, 255, 165)',
                            }, {
                                offset: 1,
                                color: 'rgba(1, 191, 236)',
                            }]),
                        },
                        emphasis: {
                            focus: 'series',
                        },
                    },
                ],
            }

            getchart.setOption(option)
            window.addEventListener('resize', () => {
                getchart.resize()
            })
        },

    },
}
</script>

<style scoped>

</style>
