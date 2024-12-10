var myChart = echarts.init(document.getElementById('pulsochart')); // Gráfica
var eventTableBody = document.getElementById('event-table-body');

var dataPointsSeries = []; // Un array para cada serie de datos
let shouldStoreData = false;  // Variable global para controlar el almacenamiento de datos
var updateInterval = null;
// Objeto para almacenar los valores anteriores de D1, D2 y D3
let previousDatabaseValues = {
    D1: null,
    D2: null,
    D3: null
};
let isPaused = false; // Variable para controlar el estado de pausa

function fetchData() {
    const url = `/chart-data/?storeData=${shouldStoreData}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data); // Verifica si los datos recibidos son correctos
            updateConnectionStatus(data.connected);
            fetchDatabaseData();
        })
        .catch(error => console.error("Error al obtener datos:", error));
}

function fetchDatabaseData() {
    const url = `/db_data/`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data); // Verifica si los datos recibidos son correctos
            updateConnectionStatus(data.connected);
            if (data.time && Array.isArray(data.raw_data) && data.raw_data.length === 3) {
                var utcDate = new Date(data.time);
                utcDate.setMinutes(utcDate.getMinutes() - utcDate.getTimezoneOffset());

                // Verifica si los valores han cambiado
                const [currentD1, currentD2, currentD3] = data.raw_data;

                if (
                    currentD1 !== previousDatabaseValues.D1 ||
                    currentD2 !== previousDatabaseValues.D2 ||
                    currentD3 !== previousDatabaseValues.D3
                ) {
                    // Actualiza los valores anteriores
                    previousDatabaseValues.D1 = currentD1;
                    previousDatabaseValues.D2 = currentD2;
                    previousDatabaseValues.D3 = currentD3;

                    // Verifica y actualiza las series de datos
                    if (dataPointsSeries.length === 0 || dataPointsSeries.length !== data.raw_data.length) {
                        dataPointsSeries = data.raw_data.map(() => []);
                    }

                    // Agrega los nuevos datos a la serie
                    dataPointsSeries.forEach((dataPoints, index) => {
                        dataPoints.push([utcDate, data.raw_data[index]]);
                        if (dataPoints.length > 30) {
                            dataPoints.shift(); // Mantener solo los últimos 200 puntos
                        }
                    });

                    console.log("Mostrados por base de datos");

                    updateChart(); // Actualiza la gráfica
                    addDataToTable(data); // Actualiza la tabla
                } else {
                    console.log("Los datos no han cambiado, no se actualizan la gráfica ni la tabla.");
                }
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
//Actualizar grafica
function updateChart() {
    // Inicializa la visibilidad de las series
    const seriesNames = dataPointsSeries.map((_, index) => `Data ${index + 1}`);
    initializeSeriesVisibility(seriesNames);

    const seriesOptions = dataPointsSeries.map((dataPoints, index) => ({
        name: `Data ${index + 1}`,
        type: 'line', // Cambiado de 'pulse' a 'line'
        step: 'start', // Cambia 'start' a 'middle' o 'end' según sea necesario
        data: dataPoints,
        showSymbol: false,
        animation: false, // Desactivar animaciones
        lineStyle: {
            width: 2,
            color: colors[index % colors.length] // Asigna un color según el índice
        }
    }));

    const option = {
        title: {
            text: 'Gráfica de Datos',
            textStyle: { color: '#fff' }
        },
        tooltip: { trigger: 'axis' },
        legend: {
            data: seriesNames, // Usa los nombres de las series dinámicamente
            textStyle: { color: '#fff' },
            selected: seriesVisibility
        },
        xAxis: { type: 'time' }, // Mantén el tipo 'time' para datos de tiempo
        yAxis: { type: 'value' },
        series: seriesOptions
    };

    myChart.setOption(option, true);
}
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
                    updateInterval = setInterval(fetchDatabaseData, 250);
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
                updateInterval = setInterval(fetchData, 250);
                document.querySelector('button').textContent = 'Pausar';
            }
        });
}
