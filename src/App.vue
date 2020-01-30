<template>
    <div id="app">
        <div class="container">
            <img class="background-img" :src="randomBackground" alt="">
            <transition name="pop">
                <div v-if="!noticeIsClosed" class="notice">
                    <div class="msgbox">
                        <img @click="noticeIsClosed = true" src="./assets/close.png" alt="关闭" class="close">
                        <div class="msgbox-title">公告</div>
                        <p>由于挖掘机女神的粉丝数涨幅已经趋于稳定，截止到{{lastUpdateTime}}，微博粉丝抓取脚本停止抓取，该页面的数据不会再有更新。为避免造成服务器资源浪费，预计该页面将于2月份关闭。</p>
                        <p>如果你想保存这些数据，请点击右上角的下载，为了避免兼容性问题，推荐使用PC或手机端的Chrome或FireFox浏览器。为提高数据自由度，下载的数据是未进行格式化的csv格式的原始表格数据，时间为标准美国时间格式，上涨率都是小数形式，按需自行格式化。仅供学习使用，请勿将数据用于商业用途。</p>
                        <p>新年快乐！在家追大力，少出门哦～</p>
                    </div>
                </div>
            </transition>
            <div class="top-bar">
                <div class="totalbar">
                  <span class="round-text">
                    挖掘机女神{{parseInt(timeSpan / 1000 / 60 / 60)}}小时内的涨粉趋势
                  </span>
                </div>
                <span class="copyright round-text" @click="changeDataSet">{{toChange}}</span>
                <span class="downloadcsv round-text" @click="downloadTable">
                    <img src="./assets/download.png" alt="">
                </span>
            </div>
            <ve-line style="border-radius:10px;background: #fff;opacity: .7;margin-top: 40px" :data="lineGraphData"
                     width="740"></ve-line>
            <FansIncrTable :structured-data="reverseStructuredData"></FansIncrTable>
        </div>
    </div>
</template>

<script>
    import FansIncrTable from "@/components/FansIncrTable";

    export default {
        name: 'app',
        components: {
            FansIncrTable,
        },
        methods: {
            changeDataSet : function () {
                if (this.toChange == '切换到全部'){
                    this.changeToAll()
                    this.toChange = '切换到24小时'
                }else{
                    this.changeTo24Hours()
                    this.toChange = '切换到全部'
                }
            },
            changeDataSetByUrl: function(url){
                var that = this
                this.$axios.get(url).then((resp) => {
                    that.structuredData = []
                    that.lineGraphData.rows = []
                    that.rawData = resp.data
                    that.rawData.split('\n').forEach((lineData, index) => {
                        let timeAndCount = lineData.split('-')
                        let time = timeAndCount[0].substring(0, timeAndCount[0].length - 3)
                        time = new Date(time)
                        let count = parseInt(timeAndCount[1])
                        let incrCount = index == 0 ? 0 : count - that.structuredData[index - 1]['count']
                        let incrRateByLast = incrCount / count
                        let totalIncrCount = index == 0 ? 0 : count - that.structuredData[0]['count']
                        let totalIncrRate = totalIncrCount / count
                        that.lineGraphData.rows.push({
                            "日期": time.getDate() + "日" + time.getHours() + ":" + time.getMinutes(),
                            "上涨人数(较上一次)": incrCount,
                        })
                        that.structuredData.push({
                            time: time,
                            count: count,
                            incrCount: incrCount,
                            incrRateByLast: incrRateByLast,
                            totalIncrCount: totalIncrCount,
                            totalIncrRate: totalIncrRate
                        })
                    })
                    this.structuredData.pop()
                    this.lineGraphData.rows.pop()
                    this.lastData = this.structuredData[this.structuredData.length - 1]
                    this.timeSpan = this.lastData.time - this.structuredData[0].time
                }).catch((err) => {
                    window.console.log(err)
                })
            },
            changeToAll: function () {
                this.changeDataSetByUrl('http://106.54.85.24:3000/follower_analyse_all')
            },
            changeTo24Hours: function () {
                this.changeDataSetByUrl('http://106.54.85.24:3000/follower_analyse')
            },
            downloadTable: function () {
                var str = "时间,粉丝数,上涨数量(距上次),上涨率(距上次),上涨数量(距第一次),上涨率(距第一次)\n"
                for (var i = 0 ; i < this.reverseStructuredData.length ; i++){
                    var item = this.reverseStructuredData[i]
                    str+=item.time+','+item.count+','+item.incrCount+','+item.incrRateByLast+
                            ','+item.totalIncrCount+','+item.totalIncrRate+'\n'
                }
                window.console.log(str)
                var aLink = document.createElement('a')
                var blob = new Blob([str],{
                    type: 'text/csv'
                })
                new Event('click')
                aLink.download = 'table.csv'
                aLink.href = URL.createObjectURL(blob)
                aLink.click()
                URL.revokeObjectURL(blob)
            }
        },
        data() {
            return {
                rawData: '',
                structuredData: [],
                lineGraphData: {
                    columns: ["日期", "上涨人数(较上一次)"],
                    rows: []
                },
                toChange: "切换到全部",
                lastData: {},
                backgrounds: [
                    "http://nsimg.cn-bj.ufileos.com/1578905970954150-453136459.jpg",
                    "http://nsimg.cn-bj.ufileos.com/1578905970954150-453136459.jpg",
                    "http://nsimg.cn-bj.ufileos.com/1578905970957064-690658643.jpg",
                    "http://nsimg.cn-bj.ufileos.com/1578905971204032-926086450.jpg",
                    "http://nsimg.cn-bj.ufileos.com/1578905971204032-926086450.jpg",
                    "http://nsimg.cn-bj.ufileos.com/1578906006071548-421975814.jpg"
                ],
                randomBackground: "",
                timeSpan: null,
                noticeIsClosed: true,
            }
        },
        mounted() {
            this.changeTo24Hours()
            this.randomBackground = this.backgrounds[parseInt(this.backgrounds.length * Math.random())]
            setTimeout(()=>{
                this.noticeIsClosed = false
            },1000)
        },
        computed: {
            reverseStructuredData() {
                // eslint-disable-next-line vue/no-side-effects-in-computed-properties
                return this.structuredData.reverse()
            },
            lastUpdateTime(){
                var time = this.reverseStructuredData[0] == undefined ? undefined : this.reverseStructuredData[0].time
                return time == undefined ? undefined : time.getFullYear()+"年" + (time.getMonth()+1) + "月" + time.getDate() +"日" +time.getHours()+"时" + time.getMinutes()+"分"

            }
        },
    }
</script>

<style>
    @font-face {
        font-family: Montserrat;
        src: url("./assets/Montserrat-Regular.otf");
    }

    #app {
        font-family: Helvetica, Tahoma, Arial, STXihei, '华文细黑', 'Microsoft YaHei', '微软雅黑', sans-serif;
        color: #2c3e50;
    }

    .container {
        margin: 40px auto;
        width: max-content;
        max-width: 1000px;
        text-align: left;
    }

    .top-bar {
        display: flex;
        flex-direction: row;
        margin-top: 40px;
        align-items: center;
    }
    .totalbar{
        flex-grow: 1;
    }
    .round-text{
        padding: 1.2em 1em;
        background: #fff;
        opacity: .7;
        font-weight: bold;
        border-radius: 10em;
    }

    a,a:visited,a:active , a:visited, a:link{
        color: #333;
    }

    table {
        margin-top: 25px;
    }

    .title {
        margin: .6em;
        font-size: 1.4em;
    }

    .background-img {
        object-fit: cover;
        filter: brightness(60%);
        z-index: -1;
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
    }
    .notice{
        position: fixed;
        z-index: 99;
        top: 0;left: 0;right: 0;bottom: 0;
        background: rgba(.2,.2,.2,.5);
    }
    .msgbox{
        display: block;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 100;
        width: 70%;
        max-width: 1000px;
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 20px 20px 20px rgba(.2,.2,.2,.2);
    }
    .msgbox-title{
        font-size: 1.4em;
        font-weight: bold;
    }
    .close{
        display: inline-block;
        width: 16px;
        position: absolute;
        right: 20px;
    }

    .downloadcsv{
        margin-left: 20px;
    }

    .downloadcsv img{
        display: inline-block;
        width: 20px;
    }
    .pop-enter-active, .pop-leave-active {
        opacity: 1;
        transition: opacity .5s;
    }
    .pop-enter, .pop-leave-to /* .fade-leave-active below version 2.1.8 */ {
        opacity: 0;
    }
</style>
