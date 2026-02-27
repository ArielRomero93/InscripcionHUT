
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import  OpcionesMenu, Usuario
from .forms import RegistroForm, PasswordResetRequestForm, PasswordResetForm

from .utils import enviar_correo_recuperacion

from django.urls import reverse
from django.utils.crypto import get_random_string
from .decorators import usuario_autenticado
from django.utils import timezone
from datetime import timedelta


#Importaciones de otras clases
from .exportaciones import exportarInscriptosExcel

from .formulariosVarios import FormularioInscripcionView, FormularioDecicionView, InscripcionForm, DecisionForm, \
    InscripcionExitosaView, InscripcionCerradaView, decisionProcesadaExitosamenteView, obtener_provincias, formulario_voluntario, csrf_protect

from .reportes import ReporteInscriptosHUT, ReporteDecisiones, ver_inscripto, ver_interesado, UsuarioDecision

@usuario_autenticado
def inicio(request):
    return render(request, 'home.html')

@usuario_autenticado
def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()  # Esto guardará el usuario con el rol y la contraseña hasheada
            messages.success(request, "Usuario registrado con éxito.")
            return redirect('login')  # Redirige a la página de login
        else:
            messages.error(request, "Hubo un error al registrar el usuario.")

    else:
        form = RegistroForm()

    return render(request, 'regsUsMios.html', {'form': form})

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            try:
                user = Usuario.objects.get(username=username, email=email)
                # Generar un token
                token = get_random_string(length=32)
                # Guardar el token temporalmente (puedes guardarlo en el usuario o en otra tabla)
                user.reset_token = token
                user.save()

                # Crear la URL de restablecimiento
                reset_url = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'token': token})
                )

                # Enviar correo de recuperación
                enviar_correo_recuperacion(user.email, user.username, reset_url)
                messages.success(request, 'Se ha enviado un correo electrónico con las instrucciones para restablecer tu contraseña.')
                return redirect('login')
            except Usuario.DoesNotExist:
                messages.error(request, 'El usuario o correo electrónico no son correctos.')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'password_reset_request.html', {'form': form})


def password_reset_confirm(request, token):
    try:
        user = get_object_or_404(Usuario, reset_token=token)  # Busca el usuario por el token
    except Usuario.DoesNotExist:
        messages.error(request, 'Token inválido o usuario no encontrado.')
        return redirect('login')

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.reset_token = ''  # Borra el token después de usarlo
            user.save()
            messages.success(request, 'Tu contraseña ha sido restablecida correctamente.')
            return redirect('login')
    else:
        form = PasswordResetForm()  # Crea una nueva instancia del formulario

    return render(request, 'password_reset_confirm.html', {'form': form})  # Renderiza el template con el formulario


@usuario_autenticado
def password_update_view(request):
    # Obtén al usuario actual desde la sesión
    usuario_id = request.session.get('usuario_id')  # Obtén el id del usuario desde la sesión
    if not usuario_id:
        messages.error(request, "No estás autenticado.")
        return redirect('login')

    user = get_object_or_404(Usuario, id=usuario_id)  # Busca al usuario en la base de datos

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.password_last_updated = timezone.now()  # Actualiza la fecha de actualización de la contraseña
            user.save()
            messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
            return redirect('inicio')
    else:
        form = PasswordResetForm()

    return render(request, 'password_update.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(username=username)

            if usuario.bloqueado_hasta and timezone.now() < usuario.bloqueado_hasta:
                messages.error(request, "Tu cuenta está bloqueada. Intenta nuevamente más tarde.")
                return render(request, 'login.html')  # Muestra la página de login

            if check_password(password, usuario.password):  # Verifica la contraseña
                usuario.intentos_fallidos = 0
                usuario.bloqueado_hasta = None  # Desbloquea al usuario
                usuario.ultimoIngreso = timezone.now() # Actualiza el último ingreso
                usuario.save()  # Guarda los cambios

                time_since_update = timezone.now() - usuario.ultimoIngreso
                if time_since_update > timedelta(days=90):
                    messages.warning(request,
                                     "Han pasado más de 3 meses desde que actualizaste tu contraseña. Por favor, cámbiala.")
                    request.session['usuario_id'] = usuario.id  # Almacena el ID del usuario en la sesión
                    return redirect('password_update')

                request.session['usuario_id'] = usuario.id  # Guarda el ID del usuario en la sesión
                request.session['username'] = usuario.username  # Guarda el nombre de usuario en la sesión
                request.session['role'] = usuario.role  # Guarda el rol del usuario en la sesión
                print("Rol almacenado en la sesión:", request.session['role'])
                return redirect('inicio')  # Redirige a la página principal
            else:

                usuario.intentos_fallidos += 1

                # Si alcanza los 3 intentos fallidos, bloquea la cuenta por 10 minutos
                if usuario.intentos_fallidos >= 3:
                    usuario.bloqueado_hasta = timezone.now() + timedelta(minutes=10)
                    messages.error(request,
                                   "Has superado el número máximo de intentos. Tu cuenta ha sido bloqueada por 10 minutos.")
                else:
                    messages.error(request, "Contraseña incorrecta. Te quedan {} intentos.".format(
                        3 - usuario.intentos_fallidos))

                usuario.save()  # Guarda los cambios en el usuario

        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")


    return render(request, 'login.html')  # Renderiza la página de login

def logout_view(request):
    try:
        del request.session['usuario_id']  # Elimina el ID del usuario de la sesión
    except KeyError:
        pass  # No hace nada si no está en la sesión

    return redirect('login')  # Redirige al LOGIN


def mostrar_opcionesMenu(request, tipo_opcion):
    # Filtrar las opciones según el tipo_opcion
    opciones = OpcionesMenu.objects.filter(TipoOpcion=tipo_opcion)
    # Pasar 'opciones' y 'tipo_opcion' al template
    return render(request, 'opcionesMenu.html', {'opciones': opciones, 'tipo_opcion': tipo_opcion})

