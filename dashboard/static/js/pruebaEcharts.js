var myChart = echarts.init(document.getElementById('graficalineal')); // Gráfica 2

var dataPointsTemperature = [];
var dataPointsVoltage = [];
var dataPointsHumidity = [];
let shouldStoreData = false;  // Variable global para controlar el almacenamiento de datos

            function fetchData() {
                const url = `/chart-data/?store=${shouldStoreData}`;  // Envía la variable global en la URL
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        /*var connectionStatus = document.getElementById('connection-status');
                        if (data.connected) {
                            connectionStatus.textContent = 'Conectado el Arduino';
                            connectionStatus.classList.remove('text-danger');
                            connectionStatus.classList.add('text-success');
                        } else {
                            connectionStatus.textContent = 'Desconectado';
                            connectionStatus.classList.remove('text-success');
                            connectionStatus.classList.add('text-danger');
                        }*/

                        if (data.time && data.temperature !== null && data.voltage !== null && data.humidity !== null) {
                            var utcDate = new Date(data.time);
                            var offset = utcDate.getTimezoneOffset();
                            utcDate.setMinutes(utcDate.getMinutes() - offset);

                            dataPointsTemperature.push([utcDate, data.temperature]);
                            dataPointsVoltage.push([utcDate, data.voltage]);
                            dataPointsHumidity.push([utcDate, data.humidity]);
                           
                            if (dataPointsTemperature.length > 50) {
                                dataPointsTemperature.shift();
                        
                            }
                            if (dataPointsVoltage.length > 50) {
                                dataPointsVoltage.shift();
                
                            }
                            if (dataPointsHumidity.length > 50) {  
                                dataPointsHumidity.shift();
                            }
            

                            var option = {
                                title: {
                                    text: 'Gráfica Lineal',
                                    top: '20px',       // Aplica un margen superior de 20px
                                    bottom: '20px',
                                    textStyle: {
                                        color: '#FFFF', // Cambia el color del texto del título a blanco
                                        fontSize: 18,     // Ajusta el tamaño de la fuente
                                        fontWeight: 'bold'// Hace el texto en negrita
                                    }
                                },
                                tooltip: {
                                    trigger: 'axis'
                                },
                                legend: {
                                    data: ['Temperature', 'Voltage','Humidity'],
                                    textStyle: {
                                        color: '#FFFF' // Cambia el color del texto de la leyenda a rojo
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
                                    type: 'time',
                                    boundaryGap: false
                                },
                                yAxis: {
                                    type: 'value'
                                },
                                series: [
                                    {
                                        name: 'Temperature',
                                        type: 'line',
                                        data: dataPointsTemperature,
                                        showSymbol: false,
                                        animation: false
                                    },
                                    {
                                        name: 'Voltage',
                                        type: 'line',
                                        data: dataPointsVoltage,
                                        showSymbol: false,
                                        animation: false,
                                        lineStyle: {
                                            color: 'green'
                                        }
                                    },
                                    {
                                        name: 'Humidity',  
                                        type: 'line',
                                        data: dataPointsHumidity,
                                        showSymbol: false,
                                        animation: false,
                                    }
                                ]
                            };
                            myChart.setOption(option);
                            
                        }
                    });
            }

            // Función para iniciar/pausar la actualización
            function toggleUpdate() {
                if (updateInterval) {
                    clearInterval(updateInterval);
                    updateInterval = null;
                    document.querySelector('button').textContent = 'Iniciar';
                } else {
                    openModal();
                }
            }

            // Función para mostrar el modal
            function openModal() {
                document.getElementById('myModal').style.display = 'block';
            }

            // Función para cerrar el modal
            function closeModal() {
                document.getElementById('myModal').style.display = 'none';
            }

            // Función para almacenar los datos
            function storeData() {
                // Lógica para almacenar los datos
                shouldStoreData = true;  // Establece la variable global a true
                connectArduino();
                closeModal(); // Cierra el modal
            }

            function notStoreData() {
                // Lógica para almacenar los datos
                shouldStoreData = false;  // Establece la variable global a false
                connectArduino();
                closeModal(); // Cierra el modal 
            }

            function connectArduino() {
                fetch('/connect-arduino/')
                    .then(response => response.json())
                    .then(data => {
                        var connectionStatus = document.getElementById('connection-status');
                        if (data.connected) {
                            connectionStatus.textContent = 'Conectado el Arduino';
                            connectionStatus.classList.remove('text-danger');
                            connectionStatus.classList.add('text-success');
                            fetchData();
                            updateInterval = setInterval(fetchData, 1000);
                            document.querySelector('button').textContent = 'Pausar';
                        } else {
                            connectionStatus.textContent = 'Desconectado';
                            connectionStatus.classList.remove('text-success');
                            connectionStatus.classList.add('text-danger');
                        }
                    });
            }