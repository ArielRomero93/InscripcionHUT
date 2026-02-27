//$(document).ready(function() {
//    var table = $('#dataTable').DataTable();
//
//    $('#busqueda').on('keyup', function() {
//        table.search($(this).val()).draw();
//         "searching": false // Habilitar función de búsqueda
//    });
//});

$(document).ready(function() {
    $("#busqueda").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("table tbody tr").each(function() {
            var rowText = $(this).text().toLowerCase();
            if (rowText.indexOf(value) === -1) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    });
});
