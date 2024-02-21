from django.contrib import admin
from AppFormularioInscripcion.models import Pais, ProvinciaEstado,FormularioInscripcionHUT

# Register your models here.

class AdminPais(admin.ModelAdmin):
    list_display = ('paisNombre',)  # Añade la coma al final para indicar una tupla
    ordering = ['paisNombre']

class AdminProvinciaEstado(admin.ModelAdmin):
    list_display = ('provinciaNombre',)
    ordering = ['provinciaNombre']

class AdminFormularioInscripcion(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ['nombre']

admin.site.site_header = 'Formulario'
admin.site.site_title = 'HUT'

admin.site.register(Pais, AdminPais)  # Registra la clase AdminPais
admin.site.register(ProvinciaEstado, AdminProvinciaEstado)  # Registra la clase AdminProvinciaEstado
admin.site.register(FormularioInscripcionHUT, AdminFormularioInscripcion)
