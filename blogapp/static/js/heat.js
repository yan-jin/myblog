
var dom = document.getElementById("heat-calender-plot");
var myChart = echarts.init(dom);
option = {
    textStyle: {
        color: '#ffffff'
    },
    //backgroundColor: 'rgba(255,255,255,0)',
    tooltip : {
       position: 'top',
        formatter: function (p) {
            var format = echarts.format.formatTime('yyyy-MM-dd', p.data[0]);
            return format + ': ' + p.data[1];
        }
    },
    visualMap: {
        min: 0,
        max: 1200,
        //type: 'piecewise',
        orient: 'vertical',
        right: '10%',
        top: 'center',
        caculable: true,
    },
    calendar: [{
        top: '16%',
        width: '10%',
        height: 550,
        bottom: '5%',
        left: '5%',
        cellSize: ['20', 'auto'],
        range: ['2014'],
        itemStyle: {
            normal: {borderWidth: 0.5},
        },
        yearLabel: {show: true},
        orient: 'vertical',
        dayLabel: {
        color: '#ffffff'
        },
        monthLabel: {
        color: '#ffffff',
        show: false
        }
    },
    {
        top: '16%',
        width: '10%',
        height: 550,
        bottom: '5%',
        left: '20%',
        cellSize: ['20', 'auto'],
        range: ['2015'],
        itemStyle: {
            normal: {borderWidth: 0.5}
        },
        yearLabel: {show: true},
        orient: 'vertical',
        dayLabel: {
        color: '#ffffff'
        },
        monthLabel: {
        color: '#ffffff',
        show: false
        }
    },
    {
        top: '16%',
        width: '10%',
        height: 550,
        bottom: '5%',
        left: '35%',
        cellSize: ['20', 'auto'],
        range: ['2016'],
        itemStyle: {
            normal: {borderWidth: 0.5}
        },
        yearLabel: {show: true},
        orient: 'vertical',
        dayLabel: {
        color: '#ffffff'
        },
        monthLabel: {
        color: '#ffffff',
        show: false
        }
    },
    {
        top: '16%',
        width: '10%',
        height: 550,
        bottom: '5%',
        left: '50%',
        cellSize: ['20', 'auto'],
        range: ['2017'],
        itemStyle: {
            normal: {borderWidth: 0.5}
        },
        yearLabel: {show: true},
        orient: 'vertical',
        dayLabel: {
        color: '#ffffff'
        },
        monthLabel: {
        color: '#ffffff',
        show: false
        }
    },
    {
        top: '16%',
        width: '10%',
        height: 550,
        bottom: '5%',
        left: '65%',
        cellSize: ['20', 'auto'],
        range: ['2018'],
        itemStyle: {
            normal: {borderWidth: 0.5}
        },
        yearLabel: {show: true},
        orient: 'vertical',
        dayLabel: {
        color: '#ffffff'
        },
        monthLabel: {
        color: '#ffffff',
        show: false
        }
    }],
    series: [
    {
        name: '1',
        type: 'heatmap',
        coordinateSystem: 'calendar',
        calendarIndex: 0,
        data: []

    },
    {
        name: '2',
        type: 'heatmap',
        coordinateSystem: 'calendar',
        calendarIndex: 1,
        data: []
    },
    {
        name: '3',
        type: 'heatmap',
        coordinateSystem: 'calendar',
        calendarIndex: 2,
        data: []
    },
    {
        name: '4',
        type: 'heatmap',
        coordinateSystem: 'calendar',
        calendarIndex: 3,
        data: []
    },
    {
        name: '5',
        type: 'heatmap',
        coordinateSystem: 'calendar',
        calendarIndex: 4,
        data: []
    }]
};
myChart.setOption(option);
myChart.showLoading(
    {
      text: 'loading',
      color: '#c23531',
      textColor: '#ffffff',
      maskColor: 'rgba(255, 255, 255, 0)',
      zlevel: 0
});
$.get('http://127.0.0.1:8000/hole/api/heat-plot').done(function(json_data){
    data = JSON.parse(json_data);
    myChart.hideLoading();
    myChart.setOption({
        series: [{
            name: '1',
            data: data['2014']
        },
        {
            name: '2',
            data: data['2015']
        },
        {
            name: '3',
            data: data['2016']
        },
        {
            name: '4',
            data: data['2017']
        },
        {
            name: '5',
            data: data['2018']
            },
        ]
    });

});

//CHART 2

var dom2 = document.getElementById("heat-bar-plot");
var myChart2 = echarts.init(dom2);
var app2 = {};

option2 = {
    textStyle: {
        color: '#ffffff'
    },
    //backgroundColor: 'rgba(255,255,255,0)',
    toolbox: {
        feature: {
            dataZoom: {
                yAxisIndex: false
            },
            saveAsImage: {
                pixelRatio: 2
            }
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        bottom: 90
    },
    dataZoom: [{
        type: 'inside'
    }, {
        type: 'slider'
    }],
    xAxis: {
        data: [],
        silent: false,
        splitLine: {
            show: false
        },
        splitArea: {
            show: false
        }
    },
    yAxis: {
        splitArea: {
            show: false
        }
    },
    series: [{
        name: 'Num',
        type: 'bar',
        data: [],
        large: true
    }]
};

myChart2.setOption(option2);

myChart2.showLoading(
    {
      text: 'loading',
      color: '#c23531',
      textColor: '#ffffff',
      maskColor: 'rgba(255, 255, 255, 0)',
      zlevel: 0
});
$.get('http://127.0.0.1:8000/hole/api/heat-plot').done(function(json_data){
    data = JSON.parse(json_data);
    date_ = [];
    date_cnt = [];
    for(var y = 2014; y <= 2018; ++y){
        for(var d = 0; d < data[y].length; ++d){
            date_.push(data[y][d][0]);
            date_cnt.push(data[y][d][1]);
        }
    }
    myChart2.hideLoading();
    myChart2.setOption({
        xAxis: {
        data: date_,
        },
        series: [{
            data: date_cnt,
        },
        ]
    });

});

//CHART 3

var dom3 = document.getElementById("week-heat");
var myChart3 = echarts.init(dom3);
var app3 = {};

option3 = {
    textStyle: {
        color: '#ffffff'
    },
    //backgroundColor: 'rgba(255,255,255,0)',

    visualMap: {
        max: 120,
        inRange: {
            color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
        }
    },
    xAxis3D: {
        name: 'Time',
        type: 'category',
        data: [],
        nameTextStyle: {color: '#ffffff'},
        axisLabel:{textStyle: {color: '#ffffff'}},

    },
    yAxis3D: {
        name: 'Date',
        type: 'category',
        data: [],
        nameTextStyle: {color: '#ffffff'},
        axisLabel:{textStyle: {color: '#ffffff'}},

    },
    zAxis3D: {
        name: 'Num',
        type: 'value',
        nameTextStyle: {color: '#ffffff'},
        axisLabel:{textStyle: {color: '#ffffff'}},
    },
    grid3D: {
        boxWidth: 200,
        boxDepth: 80,
        light: {
            main: {
                intensity: 1.2
            },
            ambient: {
                intensity: 0.3
            }
        }
    },
    series: [{
        name: 'Num',
        type: 'bar3D',
        data: [],
        shading: 'color',

        label: {
            show: false,
            textStyle: {
                fontSize: 16,
                borderWidth: 1,
                color: '#ffffff'
            }
        },

        itemStyle: {
            opacity: 0.4
        },

        emphasis: {
            label: {
                textStyle: {
                    fontSize: 20,
                    color: '#900'
                }
            },
            itemStyle: {
                color: '#900'
            }
        }
    }]
};
myChart3.setOption(option3, true);
myChart3.showLoading(
    {
      text: 'loading',
      color: '#c23531',
      textColor: '#ffffff',
      maskColor: 'rgba(255, 255, 255, 0)',
      zlevel: 0
});

$.get('http://127.0.0.1:8000/hole/api/week-heat').done(function(json_data){
    data = JSON.parse(json_data);
    hours = data['xAxis'];
    dates = data['yAxis'];
    num = data['data'];
    myChart3.hideLoading();
    myChart3.setOption({
        xAxis3D: {
              data: hours,
        },
        yAxis3D: {
              data: dates,
        },
        series: [{
            data: num.map(function (item) {
            return {
                value: [item[1], item[0], item[2]]
            }
        }),
        }]
    });

});

//用于使chart自适应高度和宽度,通过窗体高宽计算容器高宽
var resizeContainer = function () {
    dom.style.width = window.innerWidth+'px';
    dom.style.height = window.innerHeight * 0.8+'px';
    dom2.style.width = window.innerWidth+'px';
    dom2.style.height = window.innerHeight * 0.8+'px';
    //dom3.style.width = window.innerWidth+'px';
    dom3.style.height = window.innerHeight * 0.8+'px';
    dom4.style.width = window.innerWidth+'px';
    dom4.style.height = window.innerHeight * 0.8+'px';
    dom5.style.width = window.innerWidth+'px';
    dom5.style.height = window.innerHeight * 0.8+'px';
};
//用于使chart自适应高度和宽度
window.onresize = function () {
    //重置容器高宽
    resizeContainer();
    myChart.resize();
    myChart2.resize();
    myChart3.resize();
    myChart4.resize();
    myChart5.resize();
};
