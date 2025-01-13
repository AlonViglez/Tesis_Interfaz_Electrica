const tableBody = document.getElementById('event-body');
// Variables globales
let updateInterval = null; // Almacena el intervalo
let chart; // Gráfica de líneas
let justGauge; // Gauge de JustGage
let justGauge2;
let justGauge3;
let chartOptions; // Opciones de configuración de la gráfica de líneas
let tableData = []; // Almacena los datos para la tabla
let isPaused = false; // Variable para controlar el estado de pausa

// Inicializamos el gráfico
function initializeChart() {
    chart = echarts.init(document.getElementById('graficalineal'));

    chartOptions = {
        title: {
            text: 'Gráfica Lineal',
            textStyle: {
                color: '#ffffff', // Color del título
                fontWeight: 'bold', // Texto en negritas
                fontSize: 20,
            },
        },
        tooltip: {
            trigger: 'axis',
        },
        legend: {
            data: ['Dato 1', 'Dato 2', 'Dato 3'], // Títulos personalizados en la leyenda
            top: '10%', // Posición de la leyenda
            textStyle: {
                color: '#ffffff', // Color del texto de la leyenda
            },
        },
        toolbox: {
            feature: {
                saveAsImage: {
                    show: true,
                    title: 'Guardar como imagen', // Título del botón
                    name: 'grafica_barras', // Nombre del archivo
                    backgroundColor: '#314255', // Fondo del archivo exportado
                },
            },
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: [],
            axisLine: {
                lineStyle: {
                    color: '#ffffff', // Color del eje X
                },
            },
            axisLabel: {
                color: '#ffffff', // Color de las etiquetas del eje X
            },
        },
        yAxis: {
            type: 'value',
            axisLine: {
                lineStyle: {
                    color: '#ffffff', // Color del eje Y
                },
            },
            axisLabel: {
                color: '#ffffff', // Color de las etiquetas del eje Y
            },
        },
        series: [
            {
                name: 'Dato 1', // Nombre para la leyenda
                type: 'line',
                data: [],
                color: '#ff0000', // Color de la línea
            },
            {
                name: 'Dato 2', // Nombre para la leyenda
                type: 'line',
                data: [],
                color: '#00ff00', // Color de la línea
            },
            {
                name: 'Dato 3', // Nombre para la leyenda
                type: 'line',
                data: [],
                color: '#0000ff', // Color de la línea
            },
        ],
        dataZoom: [
            {
                type: 'slider', // Control deslizante
                show: true, // Mostrar el control
                xAxisIndex: 0, // Se aplica al eje X
                start: 0, // Empieza mostrando el 0% de los datos
                end: 100, // Muestra el 100% de los datos
                textStyle: {
                    color: '#ffffff', // Color del texto en el control
                },
            },
        ],
    };

    chart.setOption(chartOptions);
}

// Inicializamos los gauges de JustGage
function initializeGauge() {
    justGauge = new JustGage({
        id: 'gauge3',
        value: 0,
        min: 0,
        max: 1023,
        title: 'Dato 1',
        label: 'Valor',
        gaugeWidthScale: 0.6,
        pointer: true,
        levelColors: ['#90ee90', '#ffa500', '#ff4500'],
    });
}

function initializeGauge2() {
    justGauge2 = new JustGage({
        id: 'gauge4',
        value: 0,
        min: 0,
        max: 1023,
        title: 'Dato 2',
        label: 'Valor',
        gaugeWidthScale: 0.6,
        pointer: true,
        levelColors: ['#90ee90', '#ffa500', '#ff4500'],
    });
}

function initializeGauge3() {
    justGauge3 = new JustGage({
        id: 'gauge5',
        value: 0,
        min: 0,
        max: 1023,
        title: 'Dato 3',
        label: 'Valor',
        gaugeWidthScale: 0.6,
        pointer: true,
        levelColors: ['#90ee90', '#ffa500', '#ff4500'],
    });
}

// Inicializamos la tabla
function initializeTable() {
    tableBody.innerHTML = ''; // Limpiamos la tabla
}
// Función para limpiar la tabla
function TableClean() {
    tableBody.innerHTML = ''; // Borra todas las filas
}

function TablePause() {
    isPaused = true; // Cambiar a modo pausa
    document.getElementById('pause-button').style.display = 'none'; // Ocultar botón de pausa
    document.getElementById('start-button').style.display = 'inline-block'; // Mostrar botón de inicio
}

function TableResume() {
    isPaused = false; // Cambiar a modo reanudar
    document.getElementById('start-button').style.display = 'none'; // Ocultar botón de inicio
    document.getElementById('pause-button').style.display = 'inline-block'; // Mostrar botón de pausa
}

// Función para actualizar la tabla
function updateTable(data) {
    const tableBody = document.getElementById('event-body');
    // Crear una nueva fila
    const row = document.createElement('tr');
    // Crear celdas y añadir los datos
    row.innerHTML = `
        <td>${tableBody.rows.length + 1}</td> <!-- Número de registro -->
        <td>${data.fecha}</td> <!-- Fecha -->
        <td>${data.d1}</td> <!-- Dato 1 -->
        <td>${data.d2}</td> <!-- Dato 2 -->
        <td>${data.d3}</td> <!-- Dato 3 -->
    `;

    // Añadir la fila al principio del cuerpo de la tabla
    tableBody.insertBefore(row, tableBody.firstChild);
}

// Función para obtener datos y actualizar las gráficas y la tabla
async function fetchData() {
    try {
        const response = await fetch('/dato-reciente/');
        const data = await response.json();
        if (data.error) {
            console.error(data.error);
            return;
        }

        const { fecha, d1, d2, d3 } = data;

        // Actualizamos los datos de la gráfica de líneas
        const xAxisData = chartOptions.xAxis.data;
        const d1Data = chartOptions.series[0].data;
        const d2Data = chartOptions.series[1].data;
        const d3Data = chartOptions.series[2].data;

        xAxisData.push(fecha);
        d1Data.push(d1);
        d2Data.push(d2);
        d3Data.push(d3);

        chart.setOption({
            xAxis: { data: xAxisData },
            series: [
                { data: d1Data },
                { data: d2Data },
                { data: d3Data },
            ],
        });

        // Actualizamos los gauges
        justGauge.refresh(d1);
        justGauge2.refresh(d2);
        justGauge3.refresh(d3);

        if(isPaused === false){
            // Actualizamos la tabla
            updateTable({ fecha, d1, d2, d3 });
        }    
    } catch (error) {
        console.error('Error al obtener los datos:', error);
    }
}

// Función para iniciar/pausar la actualización
function toggleUpdate() {
    const button = document.getElementById('toggle-btn');

    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
        button.textContent = 'Iniciar';
    } else {
        fetchData();
        updateInterval = setInterval(fetchData, 500);
        button.textContent = 'Pausar';
    }
}

// Inicialización
initializeChart();
initializeGauge();
initializeGauge2();
initializeGauge3();
initializeTable();
