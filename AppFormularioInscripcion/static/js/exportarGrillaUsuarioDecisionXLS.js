document.getElementById("export-button").addEventListener("click", function() {
    var exportFormat = document.querySelector('input[name="export-format"]:checked').value;
    if (exportFormat === 'xls') {
        exportToXLS();
    } else if (exportFormat === 'csv') {
        exportToCSV();
    }
});

function exportToXLS() {
// Obtener los datos de la tabla
    var table = document.getElementById("dataTable");
    var tableData = [];
    var headers = [];

    // Obtener los encabezados de la tabla
    var headerRow = table.rows[0];
    for (var i = 0; i < headerRow.cells.length; i++) {
        headers.push(headerRow.cells[i].innerText);
    }

    // Obtener los datos de cada fila de la tabla
    for (var i = 1; i < table.rows.length; i++) {
        var rowData = [];
        for (var j = 0; j < table.rows[i].cells.length; j++) {
            rowData.push(table.rows[i].cells[j].innerText);
        }
        tableData.push(rowData);
    }

    // Crear un nuevo libro de trabajo de Excel
    var workbook = XLSX.utils.book_new();
    var sheet = XLSX.utils.aoa_to_sheet([headers].concat(tableData));

    // Agregar la hoja al libro de trabajo
    XLSX.utils.book_append_sheet(workbook, sheet, "Hoja1");

    // Descargar el archivo XLS
    XLSX.writeFile(workbook, "formulario_de_decision.xls");
}

function exportToCSV() {
 // Obtener los datos de la tabla
    var table = document.getElementById("dataTable");
    var csv = [];

    // Obtener los encabezados de la tabla
    var headerRow = table.rows[0];
    var headers = [];
    for (var i = 0; i < headerRow.cells.length; i++) {
        headers.push(headerRow.cells[i].innerText);
    }
    csv.push(headers.join(","));

    // Obtener los datos de cada fila de la tabla
    for (var i = 1; i < table.rows.length; i++) {
        var rowData = [];
        for (var j = 0; j < table.rows[i].cells.length; j++) {
            rowData.push(table.rows[i].cells[j].innerText);
        }
        csv.push(rowData.join(","));
    }

    // Convertir el array CSV en una cadena
    var csvString = csv.join("\n");

    // Crear un objeto Blob para el CSV
    var blob = new Blob([csvString], { type: "text/csv;charset=utf-8" });

    // Crear un enlace de descarga y simular clic para descargar el archivo
    var link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.setAttribute("download", "formulario_de_decision.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}