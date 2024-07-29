from django.urls import path
from .views import FormularioInscripcionView, obtener_provincias, InscripcionExitosaView, FormularioDecicionView, decisionProcesadaExitosamenteView, UsuarioDecision, InscripcionCerradaView

from django.contrib import admin

urlpatterns = [
    # Otras URL...
    path('admin/', admin.site.urls),
    #path('', FormularioInscripcionView.as_view(), name='formHUT'),
    path('', InscripcionCerradaView.as_view(), name = 'inscripcionHutCerrada'),

    path('obtener_provincias/', obtener_provincias, name='obtener_provincias'),
    path('inscripcionExitosa/<str:nombre>/', InscripcionExitosaView.as_view(), name='inscripcion_exitosa'),
    path('formDecisionHUT/', FormularioDecicionView.as_view(), name='formDecisionHUT'),
    path('decisionProcesadaExitosamente/<str:nombre>/', decisionProcesadaExitosamenteView.as_view(), name='decisionProcesadaExitosamente'),
    path('formularioDecisionGrilla/', UsuarioDecision, name='formularioDecisionGrilla'),
]