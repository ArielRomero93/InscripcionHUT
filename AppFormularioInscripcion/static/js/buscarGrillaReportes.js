document.getElementById('searchInput').addEventListener('keyup', function () {
    // Obtener el valor de búsqueda y convertirlo a minúsculas
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll('#tablaReporte tbody tr');

    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        let matchFound = false;

        // Verificar si alguna celda coincide con el filtro
        for (let i = 0; i < cells.length; i++) {
            if (cells[i].textContent.toLowerCase().includes(filter)) {
                matchFound = true;
                break;
            }
        }

        // Mostrar u ocultar la fila según la coincidencia
        row.style.display = matchFound ? '' : 'none';
    });

    // Actualizar el contador de registros visibles
    actualizarContador();
});

// Función para actualizar el contador de registros
function actualizarContador() {
    const totalRegistrosLabel = document.getElementById('totalRegistros');
    const filasVisibles = document.querySelectorAll('#tablaReporte tbody tr:not([style*="display: none"])');

    if (totalRegistrosLabel) {
        totalRegistrosLabel.textContent = `Total de registros: ${filasVisibles.length}`;
    }
}

// Actualizar el contador al cargar la página
actualizarContador();
