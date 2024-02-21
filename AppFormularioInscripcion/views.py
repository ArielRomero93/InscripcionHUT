from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from AppFormularioInscripcion import validaciones
from .models import FormularioInscripcionHUT, ProvinciaEstado, Pais
from .forms import InscripcionForm
from django.http import JsonResponse

from django.urls import reverse


class FormularioInscripcionView(View):
    template_name = 'formHUT.html'  # Reemplaza con el nombre de tu template

    def get(self, request):
        form = InscripcionForm()
        return render(request, self.template_name, {'formulario': form})

    def post(self, request):
        form = InscripcionForm(request.POST)

        if form.is_valid():
            form = validaciones.QuitarEspacios(form)
            telefono = form.cleaned_data['telefono']
            email = form.cleaned_data['email']

            if validaciones.ValidarNumeroTelefono(telefono):
                # Mostrar mensaje de error y no guardar el formulario
                messages.error(request, 'Ya existe alguien registrado con ese número de teléfono.',
                               extra_tags='telefono')
                return render(request, self.template_name, {'formulario': form})
            if validaciones.ValidarEmail(email):
                messages.error(request, 'Ya existe alguien registrado con ese correo electrónico.', extra_tags='email')
                return render(request, self.template_name, {'formulario': form})

            # Obtener el nombre completo del usuario
            nombre_completo = form.cleaned_data['nombre']

            # Dividir el nombre completo en nombre y apellido
            nombre, _, apellido = nombre_completo.partition(' ')

            # Guardar el nombre y apellido por separado
            form.cleaned_data['nombre'] = nombre
            form.cleaned_data['apellido'] = apellido

            form.save()

            # Redirigir a la página de éxito con el nombre del usuario como parámetro
            url = reverse('inscripcion_exitosa', kwargs={'nombre': nombre})
            return redirect(url)

        return render(request, self.template_name, {'formulario': form})


class InscripcionExitosaView(View):
    template_name = 'inscripcionExitosa.html'  # Reemplaza con el nombre de tu template de éxito

    def get(self, request, *args, **kwargs):
        # Obtener el nombre del usuario del parámetro en la URL
        nombre_usuario = kwargs.get('nombre', 'Usuario')

        # Pasar el nombre del usuario al template
        return render(request, self.template_name, {'nombre': nombre_usuario})



def obtener_provincias(request):
    pais_id = request.GET.get('pais_id')

    if pais_id:
        provincias = ProvinciaEstado.objects.filter(idPais_id=pais_id)
        opciones_provincias = [{'id': provincia.id, 'nombre': provincia.provinciaNombre} for provincia in provincias]
        print(opciones_provincias)
        return JsonResponse(opciones_provincias, safe=False)

    return JsonResponse([], safe=False)
