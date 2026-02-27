document.addEventListener("DOMContentLoaded", function() {
    const fechaHasta = document.getElementById("fechaHasta");
    const fechaDesde = document.getElementById("fechaDesde");

    // Fecha actual (hoy)
    const hoy = new Date();
    const hoyISO = hoy.toISOString().split("T")[0];
    fechaHasta.value = hoyISO;

    // Fecha de hace 6 meses
    const seisMesesAtras = new Date(hoy);
    seisMesesAtras.setMonth(hoy.getMonth() - 6);
    const seisMesesAtrasISO = seisMesesAtras.toISOString().split("T")[0];
    fechaDesde.value = seisMesesAtrasISO;
});

function applyDateFilter() {
    const fechaDesde = document.getElementById("fechaDesde").value;
    const fechaHasta = document.getElementById("fechaHasta").value;

    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('fechaDesde', fechaDesde);
    urlParams.set('fechaHasta', fechaHasta);
    window.location.search = urlParams.toString(); // Actualiza la URL para aplicar el filtro
}
