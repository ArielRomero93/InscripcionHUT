document.addEventListener('DOMContentLoaded', function() {
    const archivoInput = document.getElementById('archivoCSV');
    const submitButton = document.querySelector('button[type="submit"]');
    const form = document.getElementById('formCargaCSV');

    if (archivoInput) {
        archivoInput.addEventListener('change', function() {
            const archivo = archivoInput.files[0];

            // Resetear el estado del botón de enviar
            submitButton.disabled = false;

            if (archivo) {
                // Validar si el archivo es un CSV
                if (archivo.type !== 'text/csv') {
                    alert('Por favor, cargue un archivo CSV válido.');
                    archivoInput.value = ''; // Limpiar la selección de archivo
                    submitButton.disabled = true; // Deshabilitar el botón de enviar
                    return;
                }

                // Validar el tamaño del archivo (por ejemplo, 2MB)
                const maxSize = 2 * 1024 * 1024; // 2MB
                if (archivo.size > maxSize) {
                    alert('El archivo es demasiado grande. El tamaño máximo permitido es 2MB.');
                    archivoInput.value = ''; // Limpiar la selección de archivo
                    submitButton.disabled = true; // Deshabilitar el botón de enviar
                    return;
                }
            }
        });
    }

    // Agregar evento de submit en lugar de click
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevenir el envío del formulario de forma tradicional

        const archivo = archivoInput.files[0];
        const formData = new FormData();
        formData.append('archivoCSV', archivo);

        // Enviar archivo CSV mediante AJAX
        fetch('', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            // Mostrar la grilla de resultados con efecto fade-in
            const grilla = document.getElementById('grillaResultados');
            grilla.style.display = 'block';

            const resultadosTabla = document.getElementById('resultadosTabla');
            const tbody = resultadosTabla.querySelector('tbody');

            tbody.innerHTML = '';  // Limpiar la tabla antes de llenarla

            data.filas.forEach(fila => {
                const tr = document.createElement('tr');
                if (fila.estado === 'error') {
                    tr.classList.add('error');  // Marcar la fila con error (roja)
                }

                const tdEmail = document.createElement('td');
                tdEmail.textContent = fila.email;
                tr.appendChild(tdEmail);

                const tdNombre = document.createElement('td');
                tdNombre.textContent = fila.nombre;
                tr.appendChild(tdNombre);

                const tdfechaFinalizacion = document.createElement('td');
                tdfechaFinalizacion.textContent = fila.fechaFinalizacion;
                tr.appendChild(tdfechaFinalizacion);

                tbody.appendChild(tr);
            });
        })
        .catch(error => {
            console.log("Error en la petición AJAX:", error);
        });

    });
});
