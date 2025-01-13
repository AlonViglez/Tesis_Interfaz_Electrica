// Configuración inicial
const datosPorPagina = 15; // Número de datos por página
const filas = document.querySelectorAll("#data-table tbody tr");
const totalDatos = filas.length;
const totalPages = Math.ceil(totalDatos / datosPorPagina);
const maxVisiblePages = Math.min(5, totalPages);
let currentPage = 1;

// Elementos del DOM
const pageNumbersContainer = document.getElementById("page-numbers");
const prevPageButton = document.getElementById("prev-page");
const nextPageButton = document.getElementById("next-page");

// Mostrar las filas de la página actual
function mostrarPagina(page) {
    filas.forEach((fila, index) => {
        const inicio = (page - 1) * datosPorPagina;
        const fin = page * datosPorPagina;
        fila.style.display = index >= inicio && index < fin ? "table-row" : "none";
    });
}

// Renderizar los números de página
function renderizarPaginacion() {
    pageNumbersContainer.innerHTML = "";

    // Calcular rango dinámico de páginas visibles
    let startPage = Math.max(currentPage - Math.floor(maxVisiblePages / 2), 1);
    let endPage = startPage + maxVisiblePages - 1;

    if (endPage > totalPages) {
        endPage = totalPages;
        startPage = Math.max(endPage - maxVisiblePages + 1, 1);
    }

    // Generar los números de página
    for (let i = startPage; i <= endPage; i++) {
        const pageSpan = document.createElement("span");
        pageSpan.classList.add("page");
        if (i === currentPage) {
            pageSpan.classList.add("active");
        }
        pageSpan.textContent = i;
        pageSpan.addEventListener("click", () => {
            currentPage = i;
            mostrarPagina(currentPage);
            renderizarPaginacion();
        });
        pageNumbersContainer.appendChild(pageSpan);
    }

    // Mostrar/ocultar botones "Anterior" y "Siguiente"
    prevPageButton.style.display = currentPage === 1 ? "none" : "inline-block";
    nextPageButton.style.display = currentPage === totalPages ? "none" : "inline-block";
}

// Botones de navegación
prevPageButton.addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        mostrarPagina(currentPage);
        renderizarPaginacion();
    }
});

nextPageButton.addEventListener("click", () => {
    if (currentPage < totalPages) {
        currentPage++;
        mostrarPagina(currentPage);
        renderizarPaginacion();
    }
});

// Inicialización
mostrarPagina(currentPage);
renderizarPaginacion();

