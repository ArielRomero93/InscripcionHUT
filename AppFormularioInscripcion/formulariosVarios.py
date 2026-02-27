from django.views import View
from AppFormularioInscripcion import validaciones
from django.template.loader import render_to_string
from .models import ProvinciaEstado, FormularioInscripcionHUT
from .forms import InscripcionForm, DecisionForm, VoluntarioForm, Voluntario
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from .utils import enviar_correo
from django.views.decorators.csrf import csrf_protect

class FormularioInscripcionView(View):
    template_name = 'inscripcionHUT/formHUT.html'  # Reemplaza con el nombre de tu template

    def get(self, request):
        form = InscripcionForm()
        return render(request, self.template_name, {'formulario': form})

    def post(self, request):
        form = InscripcionForm(request.POST)

        if form.is_valid():
            form = validaciones.QuitarEspacios(form)
            telefono = form.cleaned_data['telefono']
            email = form.cleaned_data['email']
            nombre = form.cleaned_data['nombre']

            if validaciones.ValidarNumeroTelefono(FormularioInscripcionHUT, telefono):
                # Mostrar mensaje de error y no guardar el formulario
                messages.error(request, 'Ya existe alguien registrado con ese número de teléfono.',
                               extra_tags='telefono')
                return render(request, self.template_name, {'formulario': form})
            if validaciones.ValidarEmail(FormularioInscripcionHUT, email):
                messages.error(request, 'Ya existe alguien registrado con ese correo electrónico.', extra_tags='email')
                return render(request, self.template_name, {'formulario': form})

            try:
                # Generar el contenido HTML del correo
                asunto = 'Confirmación de inscripción'
                mensaje_html = render_to_string('inscripcionHUT/email_template.html', {'nombre': nombre})

                # Enviar correo electrónico con contenido HTML
                enviar_correo(email, asunto, mensaje_html, html=True)
            except Exception as e:
                print(f"Error al enviar el correo: {e}")

            form.save()

            # Redirigir a la página de éxito con el nombre del usuario como parámetro
            url = reverse('inscripcion_exitosa', kwargs={'nombre': nombre})
            return redirect(url)

        return render(request, self.template_name, {'formulario': form})


class InscripcionExitosaView(View):
    template_name = 'inscripcionHUT/inscripcionExitosa.html'

    def get(self, request, *args, **kwargs):
        # Obtener el nombre del usuario del parámetro en la URL
        nombre_usuario = kwargs.get('nombre', 'Usuario')

        # Pasar el nombre del usuario al template
        return render(request, self.template_name, {'nombre': nombre_usuario})

class InscripcionCerradaView(View):
    template_name = 'inscripcionHUT/inscripcionHutCerrada.html'

    def get(self, request):

        return render(request, self.template_name)


class FormularioDecicionView(View):
    template_name = 'formDecisionHUT.html'

    def get(self, request):
        form = DecisionForm()
        return render(request, self.template_name, {'formulario': form})

    def post(self, request):
        form = DecisionForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            nombre = form.cleaned_data['nombre']
            if validaciones.ValidarEmailDesdeFormularioDeDecision(email):
                messages.error(request, 'Ya existe alguien que usó ese correo electrónico.', extra_tags='email')
                return render(request, self.template_name, {'formulario': form})

            form.save()

            # Redirigir a la página de éxito con el nombre del usuario como parámetro
            url = reverse('decisionProcesadaExitosamente', kwargs={'nombre': nombre})
            return redirect(url)

        return render(request, self.template_name, {'formulario': form})

class decisionProcesadaExitosamenteView(View):
    template_name = 'decisionProcesadaExitosamente.html'

    def get(self, request, *args, **kwargs):
        # Obtener el nombre del usuario del parámetro en la URL
        nombre_usuario = kwargs.get('nombre', 'Usuario')

        # Pasar el nombre del usuario al template
        return render(request, self.template_name, {'nombre': nombre_usuario})



def obtener_provincias(request):
    pais_id = request.GET.get('pais_id')

    if pais_id:
        provincias = ProvinciaEstado.objects.filter(idPais_id=pais_id).order_by('provinciaNombre')
        opciones_provincias = [{'id': provincia.id, 'nombre': provincia.provinciaNombre} for provincia in provincias]
        print(opciones_provincias)
        return JsonResponse(opciones_provincias, safe=False)

    return JsonResponse([], safe=False)

@csrf_protect
def formulario_voluntario(request):
    if request.method == 'POST':
        form = VoluntarioForm(request.POST, request.FILES)

        if form.is_valid():
            form = validaciones.QuitarEspacios(form)
            telefono = form.cleaned_data['telefono']
            email = form.cleaned_data['email']
            nombre = form.cleaned_data['nombre']

            if validaciones.ValidarNumeroTelefono(Voluntario, telefono):
                form.add_error('telefono', 'Ya existe alguien registrado con ese número de teléfono.')
            if validaciones.ValidarEmail(Voluntario, email):
                form.add_error('email', 'Ya existe alguien registrado con ese correo electrónico.')

            if form.errors:
                # Vuelve a mostrar el formulario con los errores asignados
                return render(request, 'formulario_voluntario.html', {'form': form})

            form.save()
            return render(request, 'formulario_exito.html', {'nombre': nombre})
        else:
            print("Errores del formulario:")
            print(form.errors)

    else:
        form = VoluntarioForm()

    return render(request, 'formulario_voluntario.html', {'form': form})

