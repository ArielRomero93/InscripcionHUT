from django.shortcuts import render, get_object_or_404
from datetime import timedelta, datetime, date
from .models import FormularioInscripcionHUT, FormularioDeDecision

def ReporteInscriptosHUT(request):
    # Obtener la fecha actual
    fecha_desde_str = request.GET.get('fechaDesde')
    fecha_hasta_str = request.GET.get('fechaHasta')

    # Convertir las fechas a objetos datetime
    if fecha_desde_str:
        fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d')
    else:
        fecha_desde = datetime.now() - timedelta(days=180)

    if fecha_hasta_str:
        fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d')
    else:
        fecha_hasta = datetime.now()

    # Ajustar fecha_desde a las 00:00:00 y fecha_hasta a las 23:59:59
    fecha_desde = fecha_desde.replace(hour=0, minute=0, second=0)
    fecha_hasta = fecha_hasta.replace(hour=23, minute=59, second=59)

    # Filtrar formularios según las fechas con rango de horas correcto
    formularios = FormularioInscripcionHUT.objects.filter(
        fecha_creacion__gte=fecha_desde,
        fecha_creacion__lte=fecha_hasta
    ).order_by('-fecha_creacion')

    # Formatear las fechas para mostrarlas en la plantilla
    for formulario in formularios:
        if formulario.fecha_creacion:
            formulario.fecha_creacion = formulario.fecha_creacion.strftime("%d/%m/%Y %H:%M:%S")

    context = {
        'formularios': formularios,
        'fecha_desde': fecha_desde.strftime('%Y-%m-%d'),  # Enviar solo la fecha
        'fecha_hasta': fecha_hasta.strftime('%Y-%m-%d'),  # Enviar solo la fecha
    }
    return render(request, 'reportes/inscriptosHUT.html', context)



def ReporteDecisiones(request):
    formularios = FormularioDeDecision.objects.all()  # Obtiene todos los registros
    for formulario in formularios:
        if formulario.fecha_creacion:
            formulario.fecha_creacion = formulario.fecha_creacion.strftime("%d/%m/%Y")

    return render(request, 'reportes/reporteDecisiones.html', {'formularios': formularios})


def ver_inscripto(request, id):
    inscripto = get_object_or_404(FormularioInscripcionHUT, id=id)
    return render(request, 'reportes/ver_inscripto.html', {'inscripto': inscripto})

def ver_interesado(request, id):
    interesado = get_object_or_404(FormularioDeDecision, id=id)
    return render(request, 'reportes/ver_interesado.html', {'interesado': interesado})



def UsuarioDecision(request):
    usuariosDecisiones = FormularioDeDecision.objects.order_by('nombre')
    return render(request, 'formularioDecisionGrilla.html', {'usuarios': usuariosDecisiones})

def GrillaInscripion(request):
    usuariosRegistrados = FormularioInscripcionHUT.objects.order_by('nombre')
    return render(request,"html", {'usuarios': usuariosRegistrados})
