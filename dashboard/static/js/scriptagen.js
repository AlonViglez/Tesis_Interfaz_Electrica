// Espera a que el DOM esté completamente cargado antes de ejecutar el código
document.addEventListener("DOMContentLoaded", () => {
    // Selecciona elementos del DOM necesarios
    const currentDate = document.querySelector(".current-date"); // Elemento que muestra la fecha actual
    const daysTag = document.querySelector(".days"); // Contenedor de los días del calendario
    const prevNextIcon = document.querySelectorAll(".icons span"); // Iconos para navegar por el calendario
    const selectedDayElement = document.getElementById("selected-day"); // Elemento que muestra el día seleccionado
    const fullDateElement = document.getElementById("full-date"); // Elemento que muestra la fecha completa seleccionada
    const generateKeyButton = document.getElementById("generate-key"); // Botón para generar clave aleatoria
    const randomKeyElement = document.getElementById("random-key"); // Elemento que muestra la clave aleatoria generada

    // Obtiene la fecha actual
    let date = new Date(),
        currYear = date.getFullYear(),
        currMonth = date.getMonth();

    // Array de nombres de meses
    const months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

    // Función para renderizar el calendario
    const renderCalendar = () => {
        // Obtiene información sobre el primer y último día del mes actual
        let firstDayofMonth = new Date(currYear, currMonth, 1).getDay(),
            lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate(),
            lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay(),
            lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate();
        
        let liTag = "";

        // Agrega días del mes anterior
        for (let i = firstDayofMonth; i > 0; i--) {
            liTag += `<li class="inactive">${lastDateofLastMonth - i + 1}</li>`;
        }

        // Agrega días del mes actual
        for (let i = 1; i <= lastDateofMonth; i++) {
            let isToday = i === date.getDate() && currMonth === new Date().getMonth()
                    && currYear === new Date().getFullYear() ? "active" : "";
            liTag += `<li class="${isToday}" data-day="${i}">${i}</li>`;
        }

        // Agrega días del siguiente mes
        for (let i = lastDayofMonth; i < 6; i++) {
            liTag += `<li class="inactive">${i - lastDayofMonth + 1}</li>`;
        }

        // Actualiza la fecha actual mostrada en el calendario
        currentDate.innerText = `${months[currMonth]} ${currYear}`;
        // Inserta los días en el calendario
        daysTag.innerHTML = liTag;
    };
    renderCalendar();

    // Función para guardar la fecha seleccionada
    const saveSelectedDate = (year, month, day) => {
        // Forma la fecha completa
        const selectedDate = `${year}-${month + 1}-${day}`;
        // Actualiza el elemento de la fecha completa en el formulario
        fullDateElement.innerText = selectedDate;
    };

    // Evento click en el calendario para seleccionar día
    daysTag.addEventListener("click", (e) => {
        if (e.target.tagName === "LI" && !e.target.classList.contains("inactive")) {
            const selectedDay = e.target.dataset.day;
            // Muestra el día seleccionado en el elemento correspondiente
            selectedDayElement.innerText = selectedDay;
            // Guarda la fecha seleccionada
            saveSelectedDate(currYear, currMonth, selectedDay);
        }
    });

    // Evento click en los botones de navegación del calendario
    prevNextIcon.forEach(icon => {
        icon.addEventListener("click", () => {
            // Actualiza el mes según el botón clickeado
            currMonth = icon.id === "prev" ? currMonth - 1 : currMonth + 1;
            // Verifica si el mes está dentro del rango
            if (currMonth < 0 || currMonth > 11) {
                date = new Date(currYear, currMonth);
                currYear = date.getFullYear();
                currMonth = date.getMonth();
            } else {
                date = new Date();
            }
            // Vuelve a renderizar el calendario con el nuevo mes
            renderCalendar();
        });
    });

    // Evento click en el botón para generar clave aleatoria
    generateKeyButton.addEventListener("click", () => {
        // Genera una clave aleatoria
        const randomKey = Math.random().toString(36).substring(2, 10);
        // Muestra la clave generada en el elemento correspondiente
        randomKeyElement.innerText = randomKey;
    });

    // Evento submit del formulario
    document.querySelector("form").addEventListener("submit", (e) => {
        e.preventDefault();
        // Aquí puedes agregar cualquier lógica adicional de validación o procesamiento del formulario
        alert('Formulario enviado con éxito');
    });
});
