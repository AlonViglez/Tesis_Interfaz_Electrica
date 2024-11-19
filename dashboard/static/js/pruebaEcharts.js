var myChart = echarts.init(document.getElementById('graficalineal')); // Gráfica 2
var eventTableBody = document.getElementById('event-table-body');

var dataPointsSeries = []; // Un array para cada serie de datos
let shouldStoreData = false;  // Variable global para controlar el almacenamiento de datos
var updateInterval = null;

let isPaused = false; // Variable para controlar el estado de pausa

// Función para agregar datos a la tabla
function addDataToTable(data) {
    if (Array.isArray(data.raw_data) && !isPaused) {
        data.raw_data.forEach((value) => {
            // Crear una nueva fila y celdas
            var newRow = document.createElement('tr');
            var dataCell = document.createElement('td');
            var timeCell = document.createElement('td');

            // Establecer el contenido de las celdas
            dataCell.textContent = value;
            timeCell.textContent = new Date(data.time).toLocaleString();

            // Agregar celdas a la fila
            newRow.appendChild(dataCell);
            newRow.appendChild(timeCell);

            // Agregar la fila al cuerpo de la tabla
            eventTableBody.appendChild(newRow);

            // Mantener solo las últimas 50 filas
            if (eventTableBody.rows.length > 50) {
                eventTableBody.removeChild(eventTableBody.firstChild);
            }
        });
    }
}

//LIMPIAR TABLA
function TableClean() {
    eventTableBody.innerHTML = ''; // LAS FILAS
}

//PAUSAR TABLA
function TablePause() {
    isPaused = !isPaused; // ALTERNAR 
}

//GRAFICA LINEAL
function fetchData() {
    const url = `/chart-data/?store=${shouldStoreData}`;  // Envía la variable global en la URL
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data); // Verifica si los datos recibidos son correctos
            var connectionStatus = document.getElementById('connection-status');
            if (data.connected) {
                connectionStatus.textContent = 'Conectado el Arduino';
                connectionStatus.classList.remove('text-danger');
                connectionStatus.classList.add('text-success');
            } else {
                connectionStatus.textContent = 'Desconectado';
                connectionStatus.classList.remove('text-success');
                connectionStatus.classList.add('text-danger');
            }
            
            if (data.time) {
                var utcDate = new Date(data.time);
                var offset = utcDate.getTimezoneOffset();
                utcDate.setMinutes(utcDate.getMinutes() - offset);

                // Asegúrate de que data.raw_data sea un array válido
                if (Array.isArray(data.raw_data)) {
                    // Verifica si la cantidad de datos ha cambiado (cuántas series esperas)
                    if (dataPointsSeries.length === 0 || dataPointsSeries.length !== data.raw_data.length) {
                        dataPointsSeries = data.raw_data.map(() => []);
                    }

                    // Agrega los nuevos datos a cada serie
                    data.raw_data.forEach((value, index) => {
                        dataPointsSeries[index].push([utcDate, value]);

                        // Mantén solo los últimos 50 puntos de datos
                        if (dataPointsSeries[index].length > 500) {
                            dataPointsSeries[index].shift();
                        }
                    });

                    // Configura las series para el gráfico (una por cada dato crudo)
                    var seriesOptions = dataPointsSeries.map((dataPoints, index) => ({
                        name: `Data ${index + 1}`, // Nombre dinámico para cada serie
                        type: 'line',
                        data: dataPoints,
                        showSymbol: false,
                        animation: false
                    }));

                    var option = {
                        title: {
                            text: 'Tiempo real',
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
                            data: seriesOptions.map(series => series.name),
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
                        series: seriesOptions // Aplica todas las series al gráfico
                    };
                    myChart.setOption(option, true);
                } else {
                    console.warn("raw_data no es un array válido:", data.raw_data);
                }

                addDataToTable(data); //ACTUALIZAR LA TABLA
            }
        })
        .catch(error => console.error("Error al obtener datos:", error));
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
                updateInterval = setInterval(fetchData, 500);
                document.querySelector('button').textContent = 'Pausar';
            } else {
                connectionStatus.textContent = 'Desconectado';
                connectionStatus.classList.remove('text-success');
                connectionStatus.classList.add('text-danger');
            }
        });
}


/*
function fetchData() {
    const url = `/chart-data/?store=${shouldStoreData}`;  // Envía la variable global en la URL
    fetch(url)
        .then(response => response.json())
        .then(data => {
            var connectionStatus = document.getElementById('connection-status');
            if (data.connected) {
                connectionStatus.textContent = 'Conectado el Arduino';
                connectionStatus.classList.remove('text-danger');
                connectionStatus.classList.add('text-success');
            } else {
                connectionStatus.textContent = 'Desconectado';
                connectionStatus.classList.remove('text-success');
                connectionStatus.classList.add('text-danger');
            }

            if (data.time && data.temperature !== null && data.voltage !== null && data.humidity !== null) {
                var utcDate = new Date(data.time);
                var offset = utcDate.getTimezoneOffset();
                utcDate.setMinutes(utcDate.getMinutes() - offset);

                dataPointsTemperature.push([utcDate, data.temperature]);
                dataPointsVoltage.push([utcDate, data.voltage]);
                dataPointsHumidity.push([utcDate, data.humidity]);
               
                if (dataPointsTemperature.length > 500) {
                    dataPointsTemperature.shift();
            
                }
                if (dataPointsVoltage.length > 500) {
                    dataPointsVoltage.shift();
    
                }
                if (dataPointsHumidity.length > 500) {  
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
                        data: ['Temperature', 'Voltage','ValorA0'],
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
                            name: 'ValorA0',  
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
}*/