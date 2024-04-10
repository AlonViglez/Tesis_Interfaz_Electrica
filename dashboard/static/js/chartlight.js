document.addEventListener('DOMContentLoaded', () => {
  // Obtener el contexto del lienzo (canvas)
  const canvas = document.getElementById('pulso-chart').getContext('2d');

  // Inicializar la gráfica con Chart.js
  const chart = new Chart(canvas, {
      type: 'line',
      data: {
          labels: [], // etiquetas para el eje x (tiempo)
          datasets: [{
              label: 'Pulso en Tiempo Real',
              borderColor: 'rgb(75, 192, 192)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              data: [], // datos para el eje y (pulso)
              fill: false
          }]
      },
      options: {
          scales: {
              x: {
                  type: 'realtime',
                  realtime: {
                      duration: 20000, // actualización en milisegundos
                      delay: 1000, // retardo inicial
                      refresh: 1000, // frecuencia de actualización
                      ttl: undefined // tiempo de vida de los datos en caché
                  }
              }
          }
      }
  });

  // Generar datos aleatorios y agregarlos a la gráfica
  setInterval(() => {
      const randomPulse = Math.floor(Math.random() * 100) + 60; // Generar un pulso aleatorio
      const now = new Date().toLocaleTimeString(); // Obtener la hora actual

      // Agregar el pulso y el tiempo actual a la gráfica
      chart.data.labels.push(now);
      chart.data.datasets[0].data.push(randomPulse);

      // Limitar el historial de datos a 20 puntos
      if (chart.data.labels.length > 20) {
          chart.data.labels.shift();
          chart.data.datasets[0].data.shift();
      }

      // Actualizar la gráfica
      chart.update();
  }, 1000); // Actualizar cada segundo
});
