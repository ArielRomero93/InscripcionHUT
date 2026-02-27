document.getElementById('exportButton').addEventListener('click', function() {
    const reportTitle = document.getElementById('reportTitle').textContent.trim();
    const table = document.getElementById('tablaReporte');
    const wb = XLS.utils.table_to_book(table, { sheet: reportTitle });
    XLS.writeFile(wb, `${reportTitle}.xls`);
});