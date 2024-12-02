var myChart = echarts.init(document.getElementById('graficalineal')); // Gráfica
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

// Función para limpiar la tabla
function TableClean() {
    eventTableBody.innerHTML = ''; // Borra todas las filas
}

// Función para pausar/reanudar la tabla
function TablePause() {
    isPaused = !isPaused; // Alterna entre pausado y no pausado
}

// Función para obtener datos y actualizar la gráfica
function fetchData() {
    const url = `/chart-data/?store=${shouldStoreData}`; // Envía la variable global en la URL
    fetch(url)
        .then(response => response.json())
        .then(data => {
            //console.log(data); // Verifica si los datos recibidos son correctos
            updateConnectionStatus(data.connected);
            
            if (data.time && Array.isArray(data.raw_data)) {
                var utcDate = new Date(data.time);
                utcDate.setMinutes(utcDate.getMinutes() - utcDate.getTimezoneOffset());

                // Verifica y actualiza las series de datos
                if (dataPointsSeries.length === 0 || dataPointsSeries.length !== data.raw_data.length) {
                    dataPointsSeries = data.raw_data.map(() => []);
                }

                data.raw_data.forEach((value, index) => {
                    dataPointsSeries[index].push([utcDate, value]);
                    if (dataPointsSeries[index].length > 200) {
                        dataPointsSeries[index].shift();
                    }
                });

                updateChart();
                addDataToTable(data);
            }
        })
        .catch(error => console.error("Error al obtener datos:", error));
}

// Actualiza el estado de conexión del Arduino
function updateConnectionStatus(isConnected) {
    var connectionStatus = document.getElementById('connection-status');
    if (isConnected) {
        connectionStatus.textContent = 'Conectado el Arduino';
        connectionStatus.classList.remove('text-danger');
        connectionStatus.classList.add('text-success');
    } else {
        connectionStatus.textContent = 'Desconectado';
        connectionStatus.classList.remove('text-success');
        connectionStatus.classList.add('text-danger');
    }
}
// Lista de colores predefinidos para las series
const colors = ['#FF0000', '#00FF00', '#FFFF00'];

// Estado de visibilidad de las series (inicializado con 'true', todas visibles)
let seriesVisibility = {};

// Inicializa la visibilidad de las series
function initializeSeriesVisibility(seriesNames) {
    seriesNames.forEach(name => {
        if (seriesVisibility[name] === undefined) {
            seriesVisibility[name] = true; // Todas las series visibles por defecto
        }
    });
}

function updateChart() {
    // Inicializa la visibilidad de las series
    const seriesNames = dataPointsSeries.map((_, index) => `Data ${index + 1}`);
    initializeSeriesVisibility(seriesNames);

    // Configura las series con los datos y colores
    var seriesOptions = dataPointsSeries.map((dataPoints, index) => ({
        name: `Data ${index + 1}`,
        type: 'line', // Sigue siendo una línea
        data: dataPoints,
        showSymbol: false,
        animation: true, // Habilita animaciones
        lineStyle: {
            type: 'solid', // Línea sólida
            width: 2,
            color: colors[index % colors.length] // Asigna un color según el índice
        },
    }));

    // Configuración del gráfico
    var option = {
        title: {
            text: 'Grafica lineal',
            textStyle: {
                color: '#FFFF',
                fontSize: 18,
                fontWeight: 'bold'
            }
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: seriesNames,
            textStyle: {
                color: '#FFFF'
            },
            selected: seriesVisibility // Usa el estado de visibilidad de las series
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
        series: seriesOptions
    };

    // Actualiza la gráfica sin eliminar la configuración
    myChart.setOption(option, true);
}

// Escucha el evento de cambio de selección en la leyenda
myChart.on('legendselectchanged', function (event) {
    const selected = event.selected;
    for (let key in selected) {
        seriesVisibility[key] = selected[key]; // Actualiza el estado de visibilidad
    }
});
// Función para iniciar/pausar la actualización
function toggleUpdate() {
    const button = document.getElementById('toggle-btn');
    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
        button.textContent = 'Iniciar';
        actualizarEstadoBoton(false); // Notifica al servidor que se desactivó
    } else {
        openModal(); // Abre el modal antes de activar
    }
}

// Función para abrir el modal
function openModal() {
    document.getElementById('myModal').style.display = 'block';
}

// Función para cerrar el modal
function closeModal() {
    document.getElementById('myModal').style.display = 'none';
}

// Función para almacenar los datos y activar el botón
function storeData() {
    shouldStoreData = true;
    connectArduino(); // Función que conecta y obtiene los datos
    closeModal();
    document.getElementById('toggle-btn').textContent = 'Detener';
    actualizarEstadoBoton(true); // Activa el botón en el servidor
}

// Función para no almacenar los datos
function notStoreData() {
    shouldStoreData = false;
    connectArduino();
    closeModal();
    document.getElementById('toggle-btn').textContent = 'Iniciar';
    actualizarEstadoBoton(true); // Desactiva el botón en el servidor
}

// Función para obtener el estado del botón desde el servidor
function obtenerEstadoBoton() {
    fetch('/obtener_estado_boton/')
        .then(response => response.json())
        .then(data => {
            const button = document.getElementById('toggle-btn');
            if (data.estado !== undefined) {
                button.textContent = data.estado ? 'Detener' : 'Iniciar';
                if (data.estado) {
                    // Si el estado es activado, reconectar el Arduino
                    connectArduino();
                } else if (updateInterval) {
                    // Si el estado es desactivado, detener la actualización
                    clearInterval(updateInterval);
                    updateInterval = null;
                }
            }
        })
        .catch(error => console.error('Error al obtener el estado:', error));
}

// Función para actualizar el estado del botón en el servidor
function actualizarEstadoBoton(estado) {
    fetch('/actualizar_estado_boton/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        },
        body: `estado=${estado}`
    })
        .then(response => response.json())
        .then(data => console.log('Estado del botón actualizado:', data))
        .catch(error => console.error('Error al actualizar el estado:', error));
}

// Función para obtener el token CSRF
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
// Llamar a obtener el estado del botón al cargar la página
document.addEventListener('DOMContentLoaded', obtenerEstadoBoton);
// Función para conectar el Arduino
function connectArduino() {
    fetch('/connect-arduino/')
        .then(response => response.json())
        .then(data => {
            updateConnectionStatus(data.connected);
            if (data.connected) {
                fetchData();
                updateInterval = setInterval(fetchData, 150);
                document.querySelector('button').textContent = 'Pausar';
            }
        });
}
