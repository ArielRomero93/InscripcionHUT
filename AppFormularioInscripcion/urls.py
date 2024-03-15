from django.urls import path
from .views import FormularioInscripcionView, obtener_provincias, InscripcionExitosaView
from django.contrib import admin

urlpatterns = [
    # Otras URL...
    path('admin/', admin.site.urls),
    path('', FormularioInscripcionView.as_view(), name='formHUT'),
    path('obtener_provincias/', obtener_provincias, name='obtener_provincias'),
    path('inscripcionExitosa/<str:nombre>/', InscripcionExitosaView.as_view(), name='inscripcion_exitosa'),  # Ajuste en la URL
]