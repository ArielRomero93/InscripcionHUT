from collections import defaultdict

from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.cell import MergedCell
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from .models import FormularioInscripcionHUT


def exportarInscriptosExcel(request):
    fecha_desde = request.GET.get('fechaDesde')
    fecha_hasta = request.GET.get('fechaHasta')
    agrupacion = request.GET.get('agrupacion', 'sin agrupar')  # Por defecto, sin agrupar

    # Obtener los inscriptos dentro del rango de fechas
    formularios = FormularioInscripcionHUT.objects.filter(
        fecha_creacion__range=[fecha_desde, fecha_hasta]
    )

    # Crear el contenedor de agrupaciones
    agrupados = defaultdict(list)

    # Agrupar según el criterio seleccionado
    for formulario in formularios:
        fecha = formulario.fecha_creacion
        if agrupacion == 'mensual':
            clave = fecha.strftime("%B %Y")  # Ejemplo: "Enero 2024"
        elif agrupacion == 'trimestral':
            trimestre = (fecha.month - 1) // 3 + 1
            clave = f"Trimestre {trimestre} {fecha.year}"  # Ejemplo: "Trimestre 1 2024"
        elif agrupacion == 'semestral':
            semestre = 1 if fecha.month <= 6 else 2
            clave = f"Semestre {semestre} {fecha.year}"  # Ejemplo: "Semestre 1 2024"
        elif agrupacion == 'anual':
            clave = f"Año {fecha.year}"  # Ejemplo: "Año 2024"
        else:  # Sin agrupar
            clave = None  # Sin clave para agregar directamente

        agrupados[clave].append(formulario)

    # Crear archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Inscriptos.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Inscriptos"

    row = 1  # Inicializamos la fila

    for key, items in agrupados.items():
        if key:  # Agregar fila de agrupación si hay clave
            # Combinar celdas para la agrupación
            ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=10)
            cell = ws.cell(row=row, column=1)
            cell.value = key
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.fill = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")
            row += 1

        # Fila de encabezados
        headers = ['Nombre', 'Apellido', 'Edad', 'País', 'Provincia', 'Ciudad', 'Teléfono', 'Email', 'Estado Civil', 'Fecha de Creación']
        for col_num, header in enumerate(headers, start=1):
            cell = ws.cell(row=row, column=col_num)
            cell.value = header
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        row += 1

        # Datos de los inscriptos
        for item in items:
            ws.append([
                item.nombre, item.apellido, item.edad, item.pais.paisNombre, item.provincia.provinciaNombre,
                item.ciudad, item.telefono, item.email, item.estadoCivil, item.fecha_creacion.strftime("%d/%m/%Y")
            ])
            row += 1

    # Configurar el ancho de las columnas automáticamente
    for column_cells in ws.columns:
        # Filtrar celdas para evitar errores con celdas combinadas
        filtered_cells = [cell for cell in column_cells if not isinstance(cell, MergedCell) and cell.value]
        if filtered_cells:  # Solo ajustar si hay celdas válidas en la columna
            length = max(len(str(cell.value)) for cell in filtered_cells)
            column_letter = get_column_letter(filtered_cells[0].column)  # Convertir el índice en letra
            ws.column_dimensions[column_letter].width = length + 2

    wb.save(response)
    return response