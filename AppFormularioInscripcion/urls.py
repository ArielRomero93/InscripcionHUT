from django.urls import path
from .views import (
    FormularioInscripcionView,
    obtener_provincias,
    InscripcionExitosaView,
    FormularioDecicionView,
    decisionProcesadaExitosamenteView,
    UsuarioDecision,
    InscripcionCerradaView,
    inicio,
    mostrar_opcionesMenu,
    ReporteInscriptosHUT,
    ReporteDecisiones,
    login_view,
    logout_view,
    register_view,
    password_reset_request,
    password_reset_confirm,
    exportarInscriptosExcel,
    ver_inscripto,
    ver_interesado,
    formulario_voluntario
)

from django.contrib import admin

urlpatterns = [

    # LOGIN
    path('', login_view, name='login'),
    path('home/', inicio, name='inicio'),
    path('logout/', logout_view, name='logout'),
    path('regsUsMios/', register_view, name='register'),

    # ADMIN
    path('admin/', admin.site.urls),

    # MENÚ
    path('opciones/<int:tipo_opcion>/', mostrar_opcionesMenu, name='mostrar_opciones'),

    # REPORTES
    path('reportes/inscriptosHUT/', ReporteInscriptosHUT, name='ReporteInscriptosHUT'),
    path('inscripto/ver/<int:id>/', ver_inscripto, name='ver_inscripto'),
    path('exportar/excel/', exportarInscriptosExcel, name='exportarInscriptosExcel'),

    path('reportes/reporteDecisiones/', ReporteDecisiones, name='ReporteDecisiones'),
    path('interesado/ver/<int:id>/', ver_interesado, name='ver_interesado'),

    # PASSWORD RESET
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset_confirm/<str:token>/', password_reset_confirm, name='password_reset_confirm'),

    # FORMULARIOS
    path('inscripcionHUT/formHUT/', InscripcionCerradaView.as_view(), name='inscripcionHutCerrada'),
    path('voluntario/', formulario_voluntario, name='formulario_voluntario'),

    path('obtener_provincias/', obtener_provincias, name='obtener_provincias'),
    path(
        'inscripcionHUT/inscripcionExitosa/<str:nombre>/',
        InscripcionExitosaView.as_view(),
        name='inscripcion_exitosa'
    ),

    path('formDecisionHUT/', FormularioDecicionView.as_view(), name='formDecisionHUT'),
    path(
        'decisionProcesadaExitosamente/<str:nombre>/',
        decisionProcesadaExitosamenteView.as_view(),
        name='decisionProcesadaExitosamente'
    ),
    path('formularioDecisionGrilla/', UsuarioDecision, name='formularioDecisionGrilla'),
]