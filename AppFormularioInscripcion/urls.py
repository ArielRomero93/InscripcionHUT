from django.urls import path
<<<<<<< HEAD
from .views import FormularioInscripcionView, obtener_provincias, InscripcionExitosaView \
    , FormularioDecicionView, decisionProcesadaExitosamenteView, UsuarioDecision, InscripcionCerradaView, inicio, \
    mostrar_opcionesMenu, ReporteInscriptosHUT, ReporteDecisiones,login_view, logout_view ,register_view, \
    password_reset_request, password_reset_confirm, exportarInscriptosExcel, ver_inscripto, ver_interesado, formulario_voluntario
=======
from .views import FormularioInscripcionView, obtener_provincias, InscripcionExitosaView, FormularioDecicionView, decisionProcesadaExitosamenteView, UsuarioDecision, InscripcionCerradaView
>>>>>>> 67d304ea4b40605ad550d744c4b268d28871bcf7

from django.contrib import admin

urlpatterns = [
    # Otras URL...
<<<<<<< HEAD
    path('home/', inicio, name='inicio'),
    path('regsUsMios/', register_view, name='register'),  # Agrega esta línea
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),  # Añade esta línea

    path('admin/', admin.site.urls),
    path('opciones/<int:tipo_opcion>/', mostrar_opcionesMenu, name='mostrar_opciones'),

    path('reportes/inscriptosHUT/', ReporteInscriptosHUT, name='ReporteInscriptosHUT'),
    path('inscripto/ver/<int:id>/', ver_inscripto, name='ver_inscripto'),
    path('exportar/excel/', exportarInscriptosExcel, name='exportarInscriptosExcel'),


    path('reportes/reporteDecisiones/', ReporteDecisiones, name='ReporteDecisiones'),
    path('interesado/ver/<int:id>/', ver_interesado, name='ver_interesado'),


    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset_confirm/<str:token>/', password_reset_confirm, name='password_reset_confirm'),



    #FORMULARIOS
    #path('inscripcionHUT/formHUT/', FormularioInscripcionView.as_view(), name='formHUT'),
    path('inscripcionHUT/formHUT/', InscripcionCerradaView.as_view(), name = 'inscripcionHutCerrada'),
    path('voluntario/', formulario_voluntario, name='formulario_voluntario'),

    path('obtener_provincias/', obtener_provincias, name='obtener_provincias'),
    path('inscripcionHUT/inscripcionExitosa/<str:nombre>/', InscripcionExitosaView.as_view(), name='inscripcion_exitosa'),
=======
    path('admin/', admin.site.urls),
    #path('', FormularioInscripcionView.as_view(), name='formHUT'),
    path('', InscripcionCerradaView.as_view(), name = 'inscripcionHutCerrada'),

    path('obtener_provincias/', obtener_provincias, name='obtener_provincias'),
    path('inscripcionExitosa/<str:nombre>/', InscripcionExitosaView.as_view(), name='inscripcion_exitosa'),
>>>>>>> 67d304ea4b40605ad550d744c4b268d28871bcf7
    path('formDecisionHUT/', FormularioDecicionView.as_view(), name='formDecisionHUT'),
    path('decisionProcesadaExitosamente/<str:nombre>/', decisionProcesadaExitosamenteView.as_view(), name='decisionProcesadaExitosamente'),
    path('formularioDecisionGrilla/', UsuarioDecision, name='formularioDecisionGrilla'),
]