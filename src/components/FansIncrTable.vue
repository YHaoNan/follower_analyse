<template>
    <table cellpadding="0" cellspacing="0" class="fans-incr-table">
        <thead>
        <tr>
            <th>时间</th>
            <th>粉丝数</th>
            <th>上涨数量(距上次)</th>
            <th>上涨率(距上次)</th>
            <th>上涨数量(距第一次)</th>
            <th>上涨率(距第一次)</th>
        </tr>
        </thead>
        <tbody>
        <tr :key="line.count" v-for="line in structuredData">
            <td>{{line.time.getDate() + "日"  + line.time.getHours() +":"+formatMinutes(line.time.getMinutes())}}</td>
            <td>{{NaNCheck(line.count)}}</td>
            <td :class="{nan: isNaN(line.incrCount),negative: line.incrCount < 0, zero: line.incrCount == 0, positive: line.incrCount > 0}"><span v-if="line.incrCount > 0">+</span>{{NaNCheck(line.incrCount)}}</td>
            <td :class="{nan: isNaN(line.incrRateByLast),negative: line.incrRateByLast < 0, zero: line.incrRateByLast == 0, positive: line.incrRateByLast > 0}"><span v-if="line.incrRateByLast > 0">+</span>{{NaNCheck((line.incrRateByLast * 100).toFixed(2)).toString() + "%"}}</td>
            <td :class="{nan: isNaN(line.totalIncrCount),negative: line.totalIncrCount < 0, zero: line.totalIncrCount == 0, positive: line.totalIncrCount > 0}"><span v-if="line.totalIncrCount > 0">+</span>{{NaNCheck(line.totalIncrCount)}}</td>
            <td :class="{nan: isNaN(line.totalIncrRate),negative: line.totalIncrRate < 0, zero: line.totalIncrRate == 0, positive: line.totalIncrRate > 0}"><span v-if="line.totalIncrRate > 0">+</span>{{NaNCheck((line.totalIncrRate * 100).toFixed(2)).toString() + "%"}}</td>
        </tr>
        </tbody>
    </table>
</template>

<script>
    export default {
        name: "FansIncrTable",
        props: ["structuredData"],
        methods: {
            formatMinutes: function (min) {
                if (min < 10){
                    return "0"+min
                }
                return min.toString()
            },
            NaNCheck: function (num) {
                if (isNaN(num)){
                    return "数据缺失"
                }
                return num
            }
        },
    }
</script>

<style scoped>
.fans-incr-table{
    opacity: .8;
    display: inline-block;
}
.fans-incr-table td , .fans-incr-table th{
    border: 1px solid #ddd;
    padding: .2em .4em;
    margin: 0;
}
.fans-incr-table th:first-child{
    border-top-left-radius: 10px;
}
.fans-incr-table th:last-child{
    border-top-right-radius: 10px;
}
.fans-incr-table tr:last-child td:first-child{
    border-bottom-left-radius: 10px;
}
.fans-incr-table tr:last-child td:last-child{
    border-bottom-right-radius: 10px;
}
.fans-incr-table tr{
    background: #fff;
}
.fans-incr-table tr:nth-child(odd){
    background: #eee;
}
.zero{

}
.positive{
    color: crimson;
}
.negative{
    color: #42b983;
}
.nan{
    color: darkslategrey;
    font-weight: lighter;
}
</style>
