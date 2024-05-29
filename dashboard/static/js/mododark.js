// Función para cambiar el estilo y guardar la selección
function cambiarEstilo() {
    var link = document.getElementById('theme-link');
    var hrefActual = link.href;
    var urlOriginal = "{%static 'css/styleM.css' %}";
    var urlAlternativo = "{%static 'css/style.css' %}";

    if (hrefActual.includes(urlOriginal)) {
        link.href = urlAlternativo;
        localStorage.setItem('theme', 'alternativo');
    } else {
        link.href = urlOriginal;
        localStorage.setItem('theme', 'original');
    }
}

// Función para aplicar el estilo guardado al cargar la página
function aplicarEstiloGuardado() {
    var theme = localStorage.getItem('theme');
    var link = document.getElementById('theme-link');
    var urlOriginal = "{%static 'css/styleM.css' %}";
    var urlAlternativo = "{%static 'css/style.css' %}";

    if (theme === 'alternativo') {
        link.href = urlAlternativo;
    } else {
        link.href = urlOriginal;
    }
}

// Llamar a aplicarEstiloGuardado al cargar la página
window.onload = aplicarEstiloGuardado;
