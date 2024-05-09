from datetime import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone  # Importa timezone desde django.utils, no desde datetime
import pytz  # Importa pytz para trabajar con zonas horarias

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

    def __str__(self):
        return self.nombre