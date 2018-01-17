$(document).ready(function() {
            var namespace = '/socket';
            var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
            socket.emit('on_connect');
            socket.emit('on_message_predict');
            socket.emit('on_message_history');
            var chart_predict;
            load_photo();
            //全局
            Highcharts.setOptions({
                        chart: {
                            backgroundColor: '#0000'
                        },
                         credits: {
                            enabled: false
                        },
                        exporting:{
                            enabled:false
                        },
                        colors: ['#F62366', '#9DFF02', '#0CCDD6'],
                        title: {
                            style: {
                                color: 'black'
                            }
                        },
                        tooltip: {
                            style: {
                                color: 'black'
                            }
                        }
                    });
            //预测-定义图形
           chart_predict =  Highcharts.chart({
             chart: {
              renderTo: 'predict_div',
              defaultSeriesType: 'spline',
              events: {
                load: load_predict
                }
             },
            title: {
              text: '预测数据'
             },
            tooltip: {
              formatter: function() {
                return 'cycle:' + this.x + ', rul:' + this.y;
                 }
                },
            xAxis: {
             allowDecimals: false,
             title: {
                text: 'cycle'
              }

              },
            yAxis: {
              minPadding: 0.2,
              maxPadding: 0.2,
              title: {
                text: 'rul',
                margin: 20
              }
            },
            series: [{
              name: 'rul',
              data: [ ]
             }]
         });

//预测-绘图
chart_predict.showLoading();

function load_photo(){
  socket.on('message_response_status', function(msg) {
     var status_light=msg.status_light;
     var status_buzzer=msg.status_buzzer;
     if(status_light==1){
      document.getElementById("preload-01").innerHTML='<img src="../static/images/1.1.png" height="100" width="100" />';
     }
     else{
     document.getElementById("preload-01").innerHTML='<img src="../static/images/1.0.png" height="100" width="100" />';
     }
     if(status_buzzer==1){
      document.getElementById("preload-02").innerHTML='<img src="../static/images/2.1.png" height="100" width="100" />';
     }
     else{
     document.getElementById("preload-02").innerHTML='<img src="../static/images/2.0.png" height="100" width="100" />';
     }
  })
}
//预测-数据加载
function load_predict(){
  socket.on('message_response_predict', function(msg) {
  chart_predict.hideLoading();
    chart_predict.series[0].addPoint([msg.cycle, msg.rul], true, false);
    chart_predict.series[1].addPoint([msg.cycle, Math.random()], true, false);
 })
}


 //温度图形绘制
temperature_chart= Highcharts.chart('temperature',{
        chart: {
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false
        },
        title: {
            text: '温度测量仪'
        },
        pane: {
            startAngle: -150,
            endAngle: 150,
            background: [{
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                    ]
                },
                borderWidth: 0,
                outerRadius: '109%'
            }, {
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#333'],
                        [1, '#FFF']
                    ]
                },
                borderWidth: 1,
                outerRadius: '107%'
            }, {
                // default background
            }, {
                backgroundColor: '#DDD',
                borderWidth: 0,
                outerRadius: '105%',
                innerRadius: '103%'
            }]
        },
        // the value axis
        yAxis: {
            min: 0,
            max: 200,
            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',
            tickPixelInterval: 30,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            labels: {
                step: 2,
                rotation: 'auto'
            },
            title: {
                text: 'db'
            },
            plotBands: [{
                from: 0,
                to: 120,
                color: '#55BF3B' // green
            }, {
                from: 120,
                to: 160,
                color: '#DDDF0D' // yellow
            }, {
                from: 160,
                to: 200,
                color: '#DF5353' // red
            }]
        },
        series: [{
            name: 'Speed',
            data: [],
            tooltip: {
                valueSuffix: ' db'
            }
        }]
    });


//湿度图形绘制
humidity_chart= Highcharts.chart('humidity',{
        chart: {
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false
        },
        title: {
            text: '湿度测量仪'
        },
        pane: {
            startAngle: -150,
            endAngle: 150,
            background: [{
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                    ]
                },
                borderWidth: 0,
                outerRadius: '109%'
            }, {
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#333'],
                        [1, '#FFF']
                    ]
                },
                borderWidth: 1,
                outerRadius: '107%'
            }, {
                // default background
            }, {
                backgroundColor: '#DDD',
                borderWidth: 0,
                outerRadius: '105%',
                innerRadius: '103%'
            }]
        },
        // the value axis
        yAxis: {
            min: 0,
            max: 200,
            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',
            tickPixelInterval: 30,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            labels: {
                step: 2,
                rotation: 'auto'
            },
            title: {
                text: '%rh'
            },
            plotBands: [{
                from: 0,
                to: 120,
                color: '#55BF3B' // green
            }, {
                from: 120,
                to: 160,
                color: '#DDDF0D' // yellow
            }, {
                from: 160,
                to: 200,
                color: '#DF5353' // red
            }]
        },
        series: [{
            name: 'Speed',
            data: [],
            tooltip: {
                valueSuffix: ' %rh'
            }
        }]
    });

//噪音图形绘制
sound_chart= Highcharts.chart('sound',{
        chart: {
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false
        },
        title: {
            text: '风速测量仪'
        },
        pane: {
            startAngle: -150,
            endAngle: 150,
            background: [{
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                    ]
                },
                borderWidth: 0,
                outerRadius: '109%'
            }, {
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#333'],
                        [1, '#FFF']
                    ]
                },
                borderWidth: 1,
                outerRadius: '107%'
            }, {
                // default background
            }, {
                backgroundColor: '#DDD',
                borderWidth: 0,
                outerRadius: '105%',
                innerRadius: '103%'
            }]
        },
        // the value axis
        yAxis: {
            min: 0,
            max: 200,
            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',
            tickPixelInterval: 30,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            labels: {
                step: 2,
                rotation: 'auto'
            },
            title: {
                text: 'db'
            },
            plotBands: [{
                from: 0,
                to: 120,
                color: '#55BF3B' // green
            }, {
                from: 120,
                to: 160,
                color: '#DDDF0D' // yellow
            }, {
                from: 160,
                to: 200,
                color: '#DF5353' // red
            }]
        },
        series: [{
            name: 'Speed',
            data: [],
            tooltip: {
                valueSuffix: ' db'
            }
        }]
    });
//PM2.5图形绘制
pm_chart= Highcharts.chart('pm',{
        chart: {
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false
        },
        title: {
            text: 'PM2.5测量仪'
        },
        pane: {
            startAngle: -150,
            endAngle: 150,
            background: [{
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                    ]
                },
                borderWidth: 0,
                outerRadius: '109%'
            }, {
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#333'],
                        [1, '#FFF']
                    ]
                },
                borderWidth: 1,
                outerRadius: '107%'
            }, {
                // default background
            }, {
                backgroundColor: '#DDD',
                borderWidth: 0,
                outerRadius: '105%',
                innerRadius: '103%'
            }]
        },
        // the value axis
        yAxis: {
            min: 0,
            max: 200,
            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',
            tickPixelInterval: 30,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            labels: {
                step: 2,
                rotation: 'auto'
            },
            title: {
                text: 'μg/m3'
            },
            plotBands: [{
                from: 0,
                to: 120,
                color: '#55BF3B' // green
            }, {
                from: 120,
                to: 160,
                color: '#DDDF0D' // yellow
            }, {
                from: 160,
                to: 200,
                color: '#DF5353' // red
            }]
        },
        series: [{
            name: 'Speed',
            data: [],
            tooltip: {
                valueSuffix: ' μg/m3'
            }
        }]
    });
	//加载数据
	function load_temperature(){
		socket.on('message_response_history', function(msg) {
			temperature_chart.series[0].update({data:[msg.temperature]});
			humidity_chart.series[0].update({data:[msg.humidity]});
			sound_chart.series[0].update({data:[msg.sound]});
			pm_chart.series[0].update({data:[msg.pm]});
		})
	}
   //on close page.
  $(window).on("beforeunload", function() {
    socket.emit('on_disconnect');
})

});