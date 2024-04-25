
const currentDate = document.querySelector(".current-date");
daysTag = document.querySelector(".days"),
prevNextIcon = document.querySelectorAll(".icons span")
const selectedDayElement = document.getElementById("selected-day");
//obitene new fecha, fecha y mes 
let date = new Date(),
currYear = date.getFullYear(),
currMonth = date.getMonth();

const months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

const renderCalendar = () => {
    let firstDayofMonth = new Date(currYear, currMonth, 1).getDay(),//obtiene el primer dia del mes
    lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate(),//obtiene la utltima fecha del dia
    lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay(),//obtiene la utltima fecha del dia del mes siguiente
    lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate(); //obtiene el ultimo dia previo del mes
    let liTag = ""; 

    for (let i = firstDayofMonth; i > 0; i--) { //muestra los dias del mes anterios
        liTag += `<li class="inactive">${lastDateofLastMonth - i + 1}</li>`;
    }
    //muestra todos los dias del mes que esta
    for (let i = 1; i <= lastDateofMonth; i++) {
        // adding la clase activa para indicar el dia actual, mes y año marcados
        let isToday = i === date.getDate() && currMonth === new Date().getMonth()
                && currYear === new Date().getFullYear() ? "active" : "";
        liTag += `<li class="${isToday}">${i}</li>`;
    }

    for (let i = lastDayofMonth; i < 6; i++) {
        liTag += `<li class="inactive">${i - lastDayofMonth + 1}</li>`;
    }

    currentDate.innerText = `${months[currMonth]} ${currYear}`;
    daysTag.innerHTML = liTag;
}
renderCalendar();

daysTag.addEventListener("click", (e) => {
    if (e.target.tagName === "LI") {
        const selectedDay = e.target.dataset.day;
        selectedDayElement.innerText = selectedDay;
    }
});

prevNextIcon.forEach(icon =>{
    icon.addEventListener("click", () =>{ //agregar click al evento en los botones 
        //si es clickeado previamente se decrementara por mes y tambien ascendera
        currMonth = icon.id === "prev" ? currMonth - 1 : currMonth + 1;
        if (currMonth < 0 || currMonth > 11) { //si mes es menos que 0 o mayor que 11
            //crea una nueva fecha de año actual y el mes pasado es evaluado
            date = new Date(currYear, currMonth);
            currYear = date.getFullYear();
            currMonth = date.getMonth();
        }else{
            date = new Date();
        }
        renderCalendar();
    });
});