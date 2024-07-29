from AppFormularioInscripcion.models import FormularioInscripcionHUT, FormularioDeDecision


def ValidarNumeroTelefono(telefono):
    telefono_ultimos_seis = telefono[-6:]
    if FormularioInscripcionHUT.objects.filter(telefono__endswith=telefono_ultimos_seis).exists():
        return True
    else:
        return False


def ValidarEmail(email):
    if FormularioInscripcionHUT.objects.filter(email__endswith=email).exists():
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
    return form