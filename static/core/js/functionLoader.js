// OPEN LOADER
mostrarLoader();

// CLOSE LOADER
window.onload = function () {
    ocultarLoader();
};

// FAIL-SAFE: Ocultar si tarda más de 3 segundos (por si recursos externos bloquean onload)
setTimeout(function () {
    ocultarLoader();
}, 3000);

// OPEN LOADER
function mostrarLoader() {
    $('#overlay').show();
    $('#loader').show();
}

// CLOSE LOADER
function ocultarLoader() {
    $('#overlay').hide();
    $('#loader').hide();
}

// Aquí puedes llamar a la función mostrarLoader cuando sea necesario, por ejemplo, cuando se hace clic en un enlace que debe activar el loader.
$('.btnload').click(function () {
    mostrarLoader();
});