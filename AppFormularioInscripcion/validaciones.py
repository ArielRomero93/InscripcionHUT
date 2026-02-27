<<<<<<< HEAD
from django.core.exceptions import ValidationError
import csv
from AppFormularioInscripcion.models import FormularioInscripcionHUT, FormularioDeDecision


def ValidarNumeroTelefono(modelo, telefono):
    telefono_ultimos_seis = telefono[-6:]
    if modelo.objects.filter(telefono__endswith=telefono_ultimos_seis).exists():
=======
from AppFormularioInscripcion.models import FormularioInscripcionHUT, FormularioDeDecision


def ValidarNumeroTelefono(telefono):
    telefono_ultimos_seis = telefono[-6:]
    if FormularioInscripcionHUT.objects.filter(telefono__endswith=telefono_ultimos_seis).exists():
>>>>>>> 67d304ea4b40605ad550d744c4b268d28871bcf7
        return True
    else:
        return False


<<<<<<< HEAD
def ValidarEmail(modelo, email):
    if modelo.objects.filter(email__endswith=email).exists():
=======
def ValidarEmail(email):
    if FormularioInscripcionHUT.objects.filter(email__endswith=email).exists():
>>>>>>> 67d304ea4b40605ad550d744c4b268d28871bcf7
        return True
    else:
        return False

def ValidarEmailDesdeFormularioDeDecision(email):
    if FormularioDeDecision.objects.filter(email__endswith=email).exists():
        return True
    else:
        return False

def QuitarEspacios(form):
    campos_excluidos = ['pais', 'provincia']  # Agrega los nombres de los campos que no deseas limpiar

    for field_name, field in form.fields.items():
        if field_name in form.cleaned_data and isinstance(form.cleaned_data[field_name], str) and field_name not in campos_excluidos:
            form.cleaned_data[field_name] = form.cleaned_data[field_name].strip()
<<<<<<< HEAD
    return form


def validar_archivo_csv(archivo):
    """
    Validaciones de archivo CSV.
    """
    if not archivo.name.endswith('.csv'):
        raise ValidationError('El archivo debe ser un archivo CSV.')

    # Aquí podrías agregar más validaciones, como asegurarte de que el CSV tenga el formato correcto.
    # Por ejemplo, si el archivo CSV tiene una cabecera, validar que tenga las columnas esperadas:
    # ['email', 'nombre', 'apellido']
    archivo.seek(0)
    reader = csv.reader(archivo.read().decode('utf-8').splitlines())
    cabecera = next(reader)  # Lee la primera fila (cabecera)

    if cabecera != ['email', 'nombre', 'apellido']:  # Ajusta según las columnas de tu archivo CSV
        raise ValidationError('El archivo CSV no tiene el formato esperado.')

    # Validación de tamaño (puedes ajustarlo según tus necesidades)
    if archivo.size > 2 * 1024 * 1024:  # Limitar a 2MB
        raise ValidationError('El archivo es demasiado grande. El tamaño máximo permitido es 2MB.')
=======
    return form
>>>>>>> 67d304ea4b40605ad550d744c4b268d28871bcf7
