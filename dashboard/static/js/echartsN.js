function createDynamicChart(chartDom) {
    var chart = echarts.init(chartDom);

    const categories = (function () {
        let now = new Date();
        let res = [];
        let len = 10;
        while (len--) {
            res.unshift(now.toLocaleTimeString().replace(/^\D*/, ''));
            now = new Date(+now - 2000);
        }
        return res;
    })();

    const categories2 = (function () {
        let res = [];
        let len = 10;
        while (len--) {
            res.push(10 - len - 1);
        }
        return res;
    })();

    const data = (function () {
        let res = [];
        let len = 10;
        while (len--) {
            res.push(Math.round(Math.random() * 1000));
        }
        return res;
    })();

    const data2 = (function () {
        let res = [];
        let len = 0;
        while (len < 10) {
            res.push(+(Math.random() * 10 + 5).toFixed(1));
            len++;
        }
        return res;
    })();

    var option = {
        title: {
            text: 'Dynamic Data',
            textStyle: {
                color: '#000000' // Color negro para el título
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#283b56'
                }
            },
            textStyle: {
                color: '#000000' // Color negro para el texto del tooltip
            }
        },
        legend: {
            textStyle: {
                color: '#000000' // Color negro para la leyenda
            }
        },
        toolbox: {
            show: true,
            feature: {
                dataView: {
                    readOnly: false,
                    textStyle: {
                        color: '#000000' // Color negro para la vista de datos
                    }
                },
                restore: {},
                saveAsImage: {}
            }
        },
        dataZoom: {
            show: false,
            start: 0,
            end: 100
        },
        xAxis: [
            {
                type: 'category',
                boundaryGap: true,
                data: categories,
                axisLine: {
                    lineStyle: {
                        color: '#000000' // Color negro para la línea del eje X
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: '#000000' // Color negro para las etiquetas del eje X
                    }
                }
            },
            {
                type: 'category',
                boundaryGap: true,
                data: categories2,
                axisLine: {
                    lineStyle: {
                        color: '#000000' // Color negro para la línea del eje X (segundo eje)
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: '#000000' // Color negro para las etiquetas del eje X (segundo eje)
                    }
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                scale: true,
                name: 'Price',
                max: 30,
                min: 0,
                boundaryGap: [0.2, 0.2],
                axisLine: {
                    lineStyle: {
                        color: '#000000' // Color negro para la línea del eje Y
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: '#000000' // Color negro para las etiquetas del eje Y
                    }
                }
            },
            {
                type: 'value',
                scale: true,
                name: 'Order',
                max: 1200,
                min: 0,
                boundaryGap: [0.2, 0.2],
                axisLine: {
                    lineStyle: {
                        color: '#000000' // Color negro para la línea del eje Y (segundo eje)
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: '#000000' // Color negro para las etiquetas del eje Y (segundo eje)
                    }
                }
            }
        ],
        series: [
            {
                name: 'Dynamic Bar',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: data
            },
            {
                name: 'Dynamic Line',
                type: 'line',
                data: data2
            }
        ]
    };

    chart.setOption(option);

    let count = 11;
    setInterval(function () {
        let axisData = new Date().toLocaleTimeString().replace(/^\D*/, '');
        data.shift();
        data.push(Math.round(Math.random() * 1000));
        data2.shift();
        data2.push(+(Math.random() * 10 + 5).toFixed(1));
        categories.shift();
        categories.push(axisData);
        categories2.shift();
        categories2.push(count++);
        chart.setOption({
            xAxis: [
                {
                    data: categories
                },
                {
                    data: categories2
                }
            ],
            series: [
                {
                    data: data
                },
                {
                    data: data2
                }
            ]
        });
    }, 2100);
}

function createStepLineChart(chartDom) {
    var chart = echarts.init(chartDom, 'dark');

    var option = {
        backgroundColor: 'transparent',
        title: {
            text: 'Step Line',
            textStyle: {
                color: '#000'
            }
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['Step Start', 'Step Middle', 'Step End'],
            textStyle: {
                color: '#000'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            axisLine: {
                lineStyle: {
                    color: '#000'
                }
            },
            axisLabel: {
                textStyle: {
                    color: '#000'
                }
            }
        },
        yAxis: {
            type: 'value',
            axisLine: {
                lineStyle: {
                    color: '#000'
                }
            },
            axisLabel: {
                textStyle: {
                    color: '#000'
                }
            }
        },
        series: [
            {
                name: 'Step Start',
                type: 'line',
                step: 'start',
                data: [120, 132, 101, 134, 90, 230, 210]
            },
            {
                name: 'Step Middle',
                type: 'line',
                step: 'middle',
                data: [220, 282, 201, 234, 290, 430, 410]
            },
            {
                name: 'Step End',
                type: 'line',
                step: 'end',
                data: [450, 432, 401, 454, 590, 530, 510]
            }
        ]
    };

    chart.setOption(option);
}

function createLineChart(chartDom) {
    var chart = echarts.init(chartDom);

    var option = {
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['Serie 1', 'Serie 2'],
            textStyle: {
                color: '#000'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
            axisLine: {
                lineStyle: {
                    color: '#000'
                }
            },
            axisLabel: {
                color: '#000'
            }
        },
        yAxis: {
            type: 'value',
            axisLine: {
                lineStyle: {
                    color: '#000'
                }
            },
            axisLabel: {
                color: '#000'
            },
            splitLine: {
                lineStyle: {
                    color: '#444'
                }
            }
        },
        series: [
            {
                name: 'Serie 1',
                type: 'line',
                data: [120, 132, 101, 134, 90, 230, 210],
                itemStyle: {
                    color: '#ff7f50'
                }
            },
            {
                name: 'Serie 2',
                type: 'line',
                data: [220, 182, 191, 234, 290, 330, 310],
                itemStyle: {
                    color: '#87cefa'
                }
            }
        ]
    };

    chart.setOption(option);
}

// Exponer las funciones al ámbito global para poder llamarlas desde el HTML
window.createDynamicChart = createDynamicChart;
window.createStepLineChart = createStepLineChart;
window.createLineChart = createLineChart;
