from django.core.exceptions import ValidationError
import csv
from AppFormularioInscripcion.models import FormularioInscripcionHUT, FormularioDeDecision


def ValidarNumeroTelefono(modelo, telefono):
    telefono_ultimos_seis = telefono[-6:]
    if modelo.objects.filter(telefono__endswith=telefono_ultimos_seis).exists():
        return True
    else:
        return False


def ValidarEmail(modelo, email):
    if modelo.objects.filter(email__endswith=email).exists():
        return True
    else:
        return False


def ValidarEmailDesdeFormularioDeDecision(email):
    if FormularioDeDecision.objects.filter(email__endswith=email).exists():
        return True
    else:
        return False


def QuitarEspacios(form):
    campos_excluidos = ['pais', 'provincia']

    for field_name, field in form.fields.items():
        if (
            field_name in form.cleaned_data
            and isinstance(form.cleaned_data[field_name], str)
            and field_name not in campos_excluidos
        ):
            form.cleaned_data[field_name] = form.cleaned_data[field_name].strip()

    return form


def validar_archivo_csv(archivo):
    """
    Validaciones de archivo CSV.
    """

    if not archivo.name.endswith('.csv'):
        raise ValidationError('El archivo debe ser un archivo CSV.')

    archivo.seek(0)
    reader = csv.reader(archivo.read().decode('utf-8').splitlines())
    cabecera = next(reader)

    if cabecera != ['email', 'nombre', 'apellido']:
        raise ValidationError('El archivo CSV no tiene el formato esperado.')

    if archivo.size > 2 * 1024 * 1024:
        raise ValidationError('El archivo es demasiado grande. El tamaño máximo permitido es 2MB.')