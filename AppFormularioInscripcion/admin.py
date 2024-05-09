# from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
# from AppFormularioInscripcion.models import Pais, ProvinciaEstado,FormularioInscripcionHUT

# # Register your models here.

# class AdminResource(resources.ModelResource):
#     class Meta:
#         model = FormularioInscripcionHUT

# class AdminPais(admin.ModelAdmin):
#     list_display = ('paisNombre',)  # Añade la coma al final para indicar una tupla
#     ordering = ['paisNombre']

# class AdminProvinciaEstado(admin.ModelAdmin):
#     list_display = ('provinciaNombre',)
#     ordering = ['provinciaNombre']

# class AdminFormularioInscripcion(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = ('nombre', 'pais')
#     # search_fields = ('nombre', 'pais')
#     resource_class = AdminResource
#     ordering = ['nombre']

# admin.site.site_header = 'Formulario'
# admin.site.site_title = 'HUT'

# admin.site.register(Pais, AdminPais)  # Registra la clase AdminPais
# admin.site.register(ProvinciaEstado, AdminProvinciaEstado)  # Registra la clase AdminProvinciaEstado
# admin.site.register(FormularioInscripcionHUT, AdminFormularioInscripcion)

from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from AppFormularioInscripcion.models import Pais, ProvinciaEstado, FormularioInscripcionHUT

# Custom field to get paisNombre
class PaisNombreField(fields.Field):
    def get_attribute(self, instance):
        return instance.pais.paisNombre if instance.pais else None

    def export(self, instance, obj=None):
        return self.get_attribute(instance)

# Custom field to get provinciaNombre
class ProvinciaNombreField(fields.Field):
    def get_attribute(self, instance):
        return instance.provincia.provinciaNombre if instance.provincia else None

    def export(self, instance, obj=None):
        return self.get_attribute(instance)

# Resource class with custom fields
class AdminResource(resources.ModelResource):
    pais_nombre = PaisNombreField(attribute='pais', column_name='Pais')
    provincia_nombre = ProvinciaNombreField(attribute='provincia', column_name='Provincia')

    class Meta:
        model = FormularioInscripcionHUT
        fields = ('nombre','apellido', 'edad', 'pais_nombre', 'provincia_nombre', 'ciudad', 'telefono', 'congregacion', 'pastor', 'email', 'estadoCivil', 'fecha_creacion', 'abandonado', 'fecha_abandono')

class AdminPais(admin.ModelAdmin):
    list_display = ('paisNombre',)
    ordering = ['paisNombre']

class AdminProvinciaEstado(admin.ModelAdmin):
    list_display = ('provinciaNombre',)
    ordering = ['provinciaNombre']

class AdminFormularioInscripcion(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AdminResource
    ordering = ['nombre']

admin.site.site_header = 'Formulario'
admin.site.site_title = 'HUT'

admin.site.register(Pais, AdminPais)
admin.site.register(ProvinciaEstado, AdminProvinciaEstado)
admin.site.register(FormularioInscripcionHUT, AdminFormularioInscripcion)
