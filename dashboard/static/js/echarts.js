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
                color: '#ffffff' // Color blanco para el título
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
                color: '#ffffff' // Color blanco para el texto del tooltip
            }
        },
        legend: {
            textStyle: {
                color: '#ffffff' // Color blanco para la leyenda
            }
        },
        toolbox: {
            show: true,
            feature: {
                dataView: {
                    readOnly: false,
                    textStyle: {
                        color: '#ffffff' // Color blanco para la vista de datos
                    }
                },
                restore: {},
                saveAsImage: {}
            }
        },
        dataZoom: {
            show: true,
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
                        color: '#ffffff' // Color blanco para la línea del eje X
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: '#ffffff' // Color blanco para las etiquetas del eje X
                    }
                }
            },
            {
                type: 'category',
                boundaryGap: true,
                data: categories2,
                axisLine: {
                    lineStyle: {
                        color: '#ffffff' // Color blanco para la línea del eje X (segundo eje)
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: '#ffffff' // Color blanco para las etiquetas del eje X (segundo eje)
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
                        color: '#ffffff' // Color blanco para la línea del eje Y
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: '#ffffff' // Color blanco para las etiquetas del eje Y
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
                        color: '#ffffff' // Color blanco para la línea del eje Y (segundo eje)
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: '#ffffff' // Color blanco para las etiquetas del eje Y (segundo eje)
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

        var maxPoints = 60; // Máximo número de puntos a mostrar
        var xAxisData = ['Dato 1']; // dato incializado
        var seriesData1 = [2]; // datos de la linea 1 random para incializarlo
        var seriesData2 = [1]; // datos de la lina 2 random para incializarlo
        var seriesData3 = [0]; // datos de la linea 3 random para incializarlo

        var option = {
            backgroundColor: 'transparent',
            title: {
                text: 'Step Line',
                textStyle: {
                    color: '#fff'
                }
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['Step Start', 'Step Middle', 'Step End'],
                textStyle: {
                    color: '#fff'
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
                data: xAxisData.slice(-maxPoints), // Muestra los últimos puntos
                axisLine: {
                    lineStyle: {
                        color: '#fff'
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: '#fff'
                    }
                }
            },
            yAxis: {
                type: 'value',
                axisLine: {
                    lineStyle: {
                        color: '#fff'
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: '#fff'
                    }
                }
            },
            dataZoom: [
                {
                    type: 'slider',  // Permite el desplazamiento horizontal
                    start: 0,
                    end: 100
                }
            ],
            series: [
                {
                    name: 'Step Start',
                    type: 'line',
                    step: 'start',
                    data: seriesData1.slice(-maxPoints) // Muestra los últimos puntos
                },
                {
                    name: 'Step Middle',
                    type: 'line',
                    step: 'middle',
                    data: seriesData2.slice(-maxPoints)
                },
                {
                    name: 'Step End',
                    type: 'line',
                    step: 'end',
                    data: seriesData3.slice(-maxPoints)
                }
            ]
        };

        chart.setOption(option);

        // Simula la recepción de datos en tiempo real
        setInterval(function () {
            var newPoint = Math.round(Math.random() * 500); // Genera nuevos puntos aleatorios
            var newCategory = 'Dato ' + (xAxisData.length + 1); // Nueva etiqueta en el eje X

            // Agregar los nuevos datos
            xAxisData.push(newCategory);
            seriesData1.push(newPoint);
            seriesData2.push(newPoint + 100);
            seriesData3.push(newPoint + 200);

            // Actualizar la gráfica mostrando solo los últimos puntos
            chart.setOption({
                xAxis: {
                    data: xAxisData.slice(-maxPoints) // Solo muestra los últimos puntos
                },
                series: [
                    {
                        data: seriesData1.slice(-maxPoints)
                    },
                    {
                        data: seriesData2.slice(-maxPoints)
                    },
                    {
                        data: seriesData3.slice(-maxPoints)
                    }
                ]
            });
        }, 200000); // Intervalo de 2 segundos para recibir nuevos datos
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
                color: '#ffffff'
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
                    color: '#ffffff'
                }
            },
            axisLabel: {
                color: '#ffffff'
            }
        },
        yAxis: {
            type: 'value',
            axisLine: {
                lineStyle: {
                    color: '#ffffff'
                }
            },
            axisLabel: {
                color: '#ffffff'
            },
            splitLine: {
                lineStyle: {
                    color: '#444444'
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
