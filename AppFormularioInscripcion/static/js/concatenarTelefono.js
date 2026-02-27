$(document).ready(function() {
    // Escuchar el evento de cambio en los campos de código de país, código de área y número de teléfono
    $(document).on('input', '#id_codigo_pais, #id_codigo_area, #id_numero_telefono', function() {
        // Obtener los valores de los campos
        var codigoPais = $('#id_codigo_pais').val();
        var codigoArea = $('#id_codigo_area').val();
        var numeroTelefono = $('#id_numero_telefono').val();

        // Concatenar los valores
        var telefono = '+' + codigoPais + codigoArea + numeroTelefono;

        // Actualizar el valor del campo de teléfono oculto
        $('#id_telefono').val(telefono);
        console.log('Teléfono actualizado: ' + telefono);
    });
});
