var dom4 = document.getElementById("q-word");
var myChart4 = echarts.init(dom4, 'dark');
var app = {};
option4 = null;

function date_trans(date){
    var nowMonth = date.getMonth() + 1;
    var strDate = date.getDate();
    var seperator = "-";
    if (nowMonth >= 1 && nowMonth <= 9) {
    nowMonth = "0" + nowMonth;
    }
    if (strDate >= 0 && strDate <= 9) {
    strDate = "0" + strDate;
    }
    var nowDate = date.getFullYear() + seperator + nowMonth + seperator + strDate;
    return nowDate;
}

$("#q-word-btn").click(function(){
    var date = new Date();
    date.setDate(date.getDate()-3);
    var text = $("#q-word-text").val();
    var cmt = document.getElementById('q-word-cmt').checked;
    var times = document.getElementsByName('q-word-time');
    var time;
    for(var i = 0; i < times.length; i++){
        if(times[i].checked){
            time = i;
            break;
        }
    }
    var types = document.getElementsByName('q-word-type');
    var type;
    for(var i = 0; i < types.length; i++){
        if(types[i].checked){
            type = i;
            break;
        }
    }
    var url = 'http://127.0.0.1:8000/hole/api/q-word/?';
        url += 'q=' + text;
    if (cmt){
        url += '&' + 'cmt=1';
    }
    max_date = date_trans(date);
    switch(time){
        case 0:break;
        case 1:
            date.setDate(date.getDate()-7);
            min_date = date_trans(date);
            break;
        case 2:
            date.setMonth(date.getMonth()-1);
            min_date = date_trans(date);
            break;
        case 3:
            date.setMonth(date.getMonth()-3);
            min_date = date_trans(date);
            break;
        case 4:
            date.setMonth(date.getMonth()-6);
            min_date = date_trans(date);
            break;
        case 5:
            date.setFullYear(date.getFullYear()-1);
            min_date = date_trans(date);
            break;
    }
    if(time != 0){
        url += '&time_range=' + '[\'' + min_date + '\', \'' + max_date + '\']';
    }
    myChart4.showLoading(
        {
          text: 'loading',
          color: '#c23531',
          textColor: '#eeeeee',
          maskColor: 'rgba(255, 255, 255, 0)',
          zlevel: 0
    });
    $.get(url).done(function(data){
        dates = data['date'];
        num = data['num'];
        index = data['index'];
        myChart4.hideLoading();
        switch(type){
            case 0: d = num;break;
            case 1: d = index;break;
        }
        myChart4.setOption({
            title: {
            text: '树洞指数: ' + text,
        },
            xAxis: {
                  data: dates,
            },
            series: [{
                name: type==0?'数量':'指数',
                data: d
            }]
        });

    });
});
$("#q-word-type1").click(function(){
    if(dates){
        myChart4.setOption({
                    series: [{
                        name: '指数',
                        data: index
                    }]
                });
        }
});
$("#q-word-type2").click(function(){
    if(dates){
        myChart4.setOption({
                    series: [{
                        name: '数量',
                        data: num
                    }]
                });
        }
});
option4 = {
    textStyle: {
        color: '#eeeeee'
    },
    backgroundColor: '#222222',
    tooltip: {
        trigger: 'axis',
        position: function (pt) {
            return [pt[0], '10%'];
        }
    },
    title: {
        left: 'center',
        text: '树洞指数',
    },
    toolbox: {
        feature: {
            dataZoom: {
                yAxisIndex: 'none'
            },
            restore: {},
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: []
    },
    yAxis: {
        type: 'value',
        boundaryGap: [0, '100%']
    },
    dataZoom: [{
        type: 'inside',
        start: 0,
        end: 100
    }, {
        start: 0,
        end: 10,
        handleSize: '80%',
        handleStyle: {
            color: '#fff',
            shadowBlur: 3,
            shadowColor: 'rgba(0, 0, 0, 0.6)',
            shadowOffsetX: 2,
            shadowOffsetY: 2
        }
    }],
    series: [
        {
            name:'指数',
            type:'line',
            smooth:true,
            symbol: 'none',
            sampling: 'average',
            itemStyle: {
                normal: {
                    color: 'rgb(255, 70, 131)'
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgb(255, 158, 68)'
                    }, {
                        offset: 1,
                        color: 'rgb(255, 70, 131)'
                    }])
                }
            },
            data: []
        }
    ]
};
myChart4.setOption(option4, true);




