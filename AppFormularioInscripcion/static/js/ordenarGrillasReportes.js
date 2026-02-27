//ordenarGrillasReportes.js


function sortTable(columnIndex) {
    const table = document.getElementById("tablaReporte");
    const rows = Array.from(table.rows).slice(1); // Omitir el encabezado
    let sortedRows;

    // Alternar entre orden ascendente y descendente
    const isAscending = table.getAttribute("data-sort-order") !== "asc";
    table.setAttribute("data-sort-order", isAscending ? "asc" : "desc");

    sortedRows = rows.sort((a, b) => {
        const aText = a.cells[columnIndex].innerText.toLowerCase();
        const bText = b.cells[columnIndex].innerText.toLowerCase();

        return isAscending
            ? aText.localeCompare(bText)
            : bText.localeCompare(aText);
    });

    // Remover filas actuales y agregar las ordenadas
    for (const row of rows) {
        table.tBodies[0].removeChild(row);
    }
    for (const row of sortedRows) {
        table.tBodies[0].appendChild(row);
    }
}
