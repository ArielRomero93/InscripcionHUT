from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from AppFormularioInscripcion.models import Pais, ProvinciaEstado,FormularioInscripcionHUT

# Register your models here.

class AdminResource(resources.ModelResource):
    class Meta:
        model = FormularioInscripcionHUT

class AdminPais(admin.ModelAdmin):
    list_display = ('paisNombre',)  # Añade la coma al final para indicar una tupla
    ordering = ['paisNombre']

class AdminProvinciaEstado(admin.ModelAdmin):
    list_display = ('provinciaNombre',)
    ordering = ['provinciaNombre']

class AdminFormularioInscripcion(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'pais')
    # search_fields = ('nombre', 'pais')
    resource_class = AdminResource
    ordering = ['nombre']

admin.site.site_header = 'Formulario'
admin.site.site_title = 'HUT'

admin.site.register(Pais, AdminPais)  # Registra la clase AdminPais
admin.site.register(ProvinciaEstado, AdminProvinciaEstado)  # Registra la clase AdminProvinciaEstado
admin.site.register(FormularioInscripcionHUT, AdminFormularioInscripcion)
