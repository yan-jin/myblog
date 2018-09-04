var dom4 = document.getElementById("q-word");
var myChart4 = echarts.init(dom4, 'dark');
var app = {};
option4 = null;

var dom5 = document.getElementById("word-cloud");
var myChart5 = echarts.init(dom5, 'dark');
var app = {};
option5 = null;

function get_word_cloud_data(keywords){
    var data = [];
    for (var name in keywords) {
        data.push({
            name: name,
            value: Math.sqrt(keywords[name])
        })
    }
    return data;
}

var maskImage = new Image();
var option5 = {
    textStyle: {
        color: '#eeeeee'
    },
    backgroundColor: '#222222',
    series: [ {
        type: 'wordCloud',
        sizeRange: [15, 100],
        rotationRange: [-60, 60],
        rotationStep: 45,
        gridSize: 1,
        shape: 'circle',
        maskImage: maskImage,
        textStyle: {
            normal: {
                color: function () {
                    return 'rgb(' + [
                        Math.round(Math.random() * 160 + 95),
                        Math.round(Math.random() * 160 + 95),
                        Math.round(Math.random() * 160 + 95)
                    ].join(',') + ')';
                }
            },
            emphasis: {
                            shadowBlur: 5,
                            shadowColor: '#eeeeee'
                        }
        },
        data: [],
    } ]
};

maskImage.onload = function () {
    option5.series[0].maskImage;
    myChart5.setOption(option5);
}
maskImage.src = 'data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/PjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+PHN2ZyB0PSIxNTM1OTgxMTU0NzAwIiBjbGFzcz0iaWNvbiIgc3R5bGU9IiIgdmlld0JveD0iMCAwIDEwMjQgMTAyNCIgdmVyc2lvbj0iMS4xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHAtaWQ9IjE3MzUiIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCI+PGRlZnM+PHN0eWxlIHR5cGU9InRleHQvY3NzIj48L3N0eWxlPjwvZGVmcz48cGF0aCBkPSJNMTAxMS4zMjggMTM0LjQ5NmMtMTEwLjc1Mi04My45MzYtMjgxLjE4NC0xMzQuMDQ4LTQ1NS45MDQtMTM0LjA0OC0yMTYuMTI4IDAtMzkyLjIyNCA3NS40NTYtNDgzLjE2OCAyMDcuMDA4LTQyLjcyIDYxLjc5Mi02Ni4zMzYgMTM0Ljk0NC03MC4yMDggMjE3LjQ3Mi0zLjQ1NiA3My40NzIgOC44OTYgMTU0LjcyIDM2LjY3MiAyNDIuMTQ0IDk0Ljg4LTI4NC4zODQgMzU5LjgwOC01MDcuMTA0IDY2NS4yOC01MDcuMTA0IDAgMC0yODUuODI0IDc1LjIzMi00NjUuNTM2IDMwOC4xOTItMC4wOTYgMC4xMjgtMi40OTYgMy4xMDQtNi42MjQgOC43MDQtMzYuMDk2IDQ4LjI4OC02Ny41NTIgMTAzLjE2OC05MS4wNzIgMTY1LjMxMi0zOS44NzIgOTQuODE2LTc2LjggMjI0Ljk2LTc2LjggMzgxLjc5MmwxMjggMGMwIDAtMTkuNDI0LTEyMi4yMDggMTQuMzY4LTI2Mi43ODQgNTUuOTA0IDcuNTUyIDEwNS44NTYgMTEuMjk2IDE1MC44NDggMTEuMjk2IDExNy42NjQgMCAyMDEuMzc2LTI1LjQ3MiAyNjMuMzkyLTgwLjEyOCA1NS41NTItNDguOTkyIDg2LjIwOC0xMTQuNzg0IDExOC42MjQtMTg0LjQ0OCA0OS41MzYtMTA2LjQgMTA1LjY2NC0yMjcuMDA4IDI2OC42NC0zMjAuMTYgOS4zNDQtNS4zNDQgMTUuMzYtMTQuOTc2IDE2LjA2NC0yNS43MjhzLTQuMDMyLTIxLjA4OC0xMi42MDgtMjcuNTg0eiIgcC1pZD0iMTczNiI+PC9wYXRoPjwvc3ZnPg==';

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
    if (cmt){
        url += 'cmt=1';
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
    url += '&q=' + text;
    myChart4.showLoading(
        {
          text: 'loading',
          color: '#c23531',
          textColor: '#eeeeee',
          maskColor: 'rgba(255, 255, 255, 0)',
          zlevel: 0
    });
    myChart5.showLoading(
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
        keywords = data['keywords'];
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
        var word_cloud_data = get_word_cloud_data(keywords).sort(function (a, b) {
                return b.value  - a.value;
             });
        myChart5.setOption({
            series: [ {
                data: word_cloud_data
    } ]
        });
        myChart5.hideLoading();

    });

});
$("#q-word-type2").click(function(){
    if(dates){
        myChart4.setOption({
                    series: [{
                        name: '指数',
                        data: index
                    }]
                });
        }
});
$("#q-word-type1").click(function(){
    if(dates){
        myChart4.setOption({
                    series: [{
                        name: '数量',
                        data: num
                    }]
                });
        }
});

$(function(){
    $('#q-word-text').bind('keypress',function(event){
        if(event.keyCode == "13")
        {
        	$('#q-word-btn').click();
        }
    });
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



myChart5.on('click', function (params) {
    if (params.componentType === 'series') {
        var text = params.name;
        document.getElementById('q-word-text').value = text;
        var date = new Date();
        date.setDate(date.getDate()-3);
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
        if (cmt){
            url += 'cmt=1';
        }
        if(time != 0){
            url += '&time_range=' + '[\'' + min_date + '\', \'' + max_date + '\']';
        }
        url += '&q=' + text;
       myChart4.showLoading(
        {
          text: 'loading',
          color: '#c23531',
          textColor: '#eeeeee',
          maskColor: 'rgba(255, 255, 255, 0)',
          zlevel: 0
    });
    myChart5.showLoading(
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
            keywords = data['keywords'];
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
            var word_cloud_data = get_word_cloud_data(keywords).sort(function (a, b) {
                    return b.value  - a.value;
                 });
            myChart5.setOption({
                series: [ {
                    data: word_cloud_data
                } ]
            });
            myChart5.hideLoading();

        });
    }

});