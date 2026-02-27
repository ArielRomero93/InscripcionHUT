from datetime import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
<<<<<<< HEAD
import os
from django.utils import timezone  # Importa timezone desde django.utils, no desde datetime
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError


class Usuario(models.Model):
    ROLES = (
        (1001, 'Super'),
        (2002, 'Directivo'),
        (3003, 'Coordinador'),
        (111111, 'Desautorizado'),
    )
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Guardaremos la contraseña hasheada
    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=ROLES)
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    ultimoIngreso = models.DateTimeField(default=timezone.now)
    intentos_fallidos = models.IntegerField(default=0)  # Contador de intentos fallidos
    bloqueado_hasta = models.DateTimeField(blank=True, null=True)  # Tiempo hasta que puede intentar nuevamente

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.ultimoIngreso = timezone.now()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class OpcionesMenu(models.Model):
    TIPOS_OPCION = (
        (1, 'Reportes'),
        (2, 'Formulario'),
        (3, 'Gráficos'),
    )
    Codigo = models.CharField(max_length=50, unique=True)
    Descripcion = models.CharField(max_length=100)
    Icono = models.CharField(max_length=100)  # Almacena el nombre de la clase de Bootstrap para el ícono.
    TipoOpcion = models.IntegerField(choices=TIPOS_OPCION)
    ruta = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.Descripcion


=======
from django.utils import timezone  # Importa timezone desde django.utils, no desde datetime
import pytz  # Importa pytz para trabajar con zonas horarias
>>>>>>> 67d304ea4b40605ad550d744c4b268d28871bcf7

class Pais(models.Model):
    paisNombre = models.CharField(max_length=100)

    def __str__(self):
        return self.paisNombre

    class Meta:
        ordering = ['paisNombre']

class ProvinciaEstado(models.Model):
    idPais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    provinciaNombre = models.CharField(max_length=100)
    def __str__(self):
        return self.provinciaNombre

class FormularioInscripcionHUT(models.Model):
    ESTADO = (
        ('Soltera/o', 'Soltera/o'),
        ('Casada/o', 'Casada/o'),
    )
    nombre = models.CharField(max_length= 30)
    apellido = models.CharField(max_length= 25)
    edad = models.IntegerField(
        validators=[
            MaxValueValidator(99),  # Ajusta el valor según tu necesidad
            MinValueValidator(13),
        ]
    )
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    provincia = models.ForeignKey(ProvinciaEstado, on_delete=models.CASCADE)
    ciudad = models.CharField(max_length= 50)

    telefono = models.CharField(max_length= 15)
    congregacion = models.CharField(max_length= 50)
    pastor = models.CharField(max_length= 50)
    email = models.EmailField()
    estadoCivil = models.CharField(choices=ESTADO, verbose_name='EstadoCivil', max_length=9)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    abandonado = models.BooleanField(default=False)
    fecha_abandono = models.DateTimeField(blank=True, null=True)
<<<<<<< HEAD
    fecha_finalizacion = models.DateField(blank=True, null=True)
=======
>>>>>>> 67d304ea4b40605ad550d744c4b268d28871bcf7

    def __str__(self):
        return self.nombre

class FormularioDeDecision(models.Model):
    OPORTUNIDAD_SERVICIO = (
        ('Voluntariado de Base', 'Voluntariado de Base'),
        ('Candidato a salir al campo', 'Candidato a salir al campo'),
        ('Intercesion', 'Intercesion'),
        ('Futuros tutores de HUT', 'Futuros tutores de HUT'),
        ('Movilizador', 'Movilizador')
    )
    nombre = models.CharField(max_length= 30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()
    profesionOcupacion = models.CharField(max_length = 30)
<<<<<<< HEAD
    servicioElegido = models.CharField(choices=OPORTUNIDAD_SERVICIO, max_length = 30)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    telefono = models.CharField(max_length= 15, blank=True, null=True)


#Voluntarios
SI_NO = [
    ('SI', 'Sí'),
    ('NO', 'No'),
]

SI_NO_TALVEZ = [
    ('SI', 'Sí'),
    ('NO', 'No'),
    ('NO_POR_AHORA', 'No por ahora'),
    ('CORTO_PLAZO', 'Por corto plazo'),
]

REALIZO_HUT = [
    ('SI', 'Sí'),
    ('TODAVIA_NO', 'Todavía no'),
]

REALIZO_REACCIONA = [
    ('SI', 'Sí'),
    ('TODAVIA_NO', 'Todavía no'),
]

NIVEL_ESTUDIO = [
    ('PRIMARIA_COMPLETA', 'Primaria completa'),
    ('SECUNDARIA_INCOMPLETA', 'Secundaria incompleta'),
    ('SECUNDARIA_COMPLETA', 'Secundaria completa'),
    ('TERCIARIO_INCOMPLETO', 'Terciario incompleto'),
    ('TERCIARIO_COMPLETO', 'Terciario completo'),
    ('UNIVERSITARIO_INCOMPLETO', 'Universitario incompleto'),
    ('UNIVERSITARIO_COMPLETO', 'Universitario completo'),
]

AREAS_INTERES = [
    ('DISENO', 'Diseño'),
    ('CONTENIDO', 'Contenido en redes'),
    ('SISTEMAS', 'Sistemas'),
    ('MOVILIZADOR', 'Movilizador de Reacciona'),
    ('STAND', 'Stand'),
    ('EDICION_VIDEO', 'Editor/a, productor/a de videos'),
    ('TRADUCCION', 'Traducción'),
    ('HUT', 'HUT'),
    ('PROFESIONAL_CAMPO', 'Profesional al Servicio del campo'),
    ('REVISION', 'Revisión de textos y documentos'),
    ('SECRETARIA', 'Secretaría'),
]

# --- Validación para imagen ---
def validar_extension_imagen(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Solo se permiten imágenes JPG o PNG.')

# --- Modelo principal ---
class Voluntario(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    pais_origen = models.CharField(max_length=100)
    pais_residencia = models.CharField(max_length=100)
    provincia_residencia = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    barrio = models.CharField(max_length=100)

    miembro_iglesia = models.CharField(max_length=10, choices=SI_NO)
    cual_iglesia = models.CharField(max_length=255, blank=True)

    sirve_en_iglesia = models.CharField(max_length=10, choices=SI_NO)
    cual_servicio = models.CharField(max_length=255, blank=True)

    tiempo_asistiendo = models.CharField(max_length=100, blank=True)
    contacto_lider = models.CharField(max_length=255, blank=True)
    contacto_lider_telefono = models.CharField(max_length=255, blank=True)

    voluntario_otra_org = models.CharField(max_length=10, choices=SI_NO)
    cual_org = models.CharField(max_length=255, blank=True)

    hizo_hut = models.CharField(max_length=20, choices=REALIZO_HUT)
    hizo_hut_anio = models.CharField(max_length=100, blank=True)

    hizo_reacciona = models.CharField(max_length=20, choices=REALIZO_REACCIONA)
    cuando_reacciona = models.CharField(max_length=100, blank=True)

    deseo_salir_campo = models.CharField(max_length=30, choices=SI_NO_TALVEZ)

    nivel_estudio = models.CharField(max_length=30, choices=NIVEL_ESTUDIO)
    titulo_universitario = models.CharField(max_length=255, blank=True)

    cursos_formacion = models.TextField(blank=True)
    experiencia_profesional = models.TextField(blank=True)

    habla_idioma = models.CharField(max_length=10, choices=SI_NO)
    cual_idioma = models.CharField(max_length=255, blank=True)

    lee_escribe_idioma = models.CharField(max_length=10, choices=SI_NO)

    areas_interes = models.ManyToManyField('AreaInteres', blank=True)
    otras_propuestas = models.TextField(blank=True)

    foto_rostro = models.ImageField(upload_to='fotos_rostro/', validators=[validar_extension_imagen])

    def __str__(self):
        return self.nombre_completo


# Opcional: tabla separada para áreas de interés, para usar ManyToMany
class AreaInteres(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


=======
    servicioElegido = models.CharField(choices=OPORTUNIDAD_SERVICIO, max_length = 30)
>>>>>>> 67d304ea4b40605ad550d744c4b268d28871bcf7
