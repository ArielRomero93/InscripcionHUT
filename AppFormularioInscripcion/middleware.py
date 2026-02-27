from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Tiempo de inactividad permitido en segundos (15 minutos)
        timeout = 15 * 60

        # Verifica si el usuario está autenticado
        if request.user.is_authenticated:
            # Obtén la última actividad registrada
            last_activity_str = request.session.get('last_activity')

            # Verifica el tiempo actual
            current_time = timezone.now()

            # Si hay una última actividad registrada, conviértela de nuevo a datetime
            if last_activity_str:
                last_activity = timezone.datetime.fromisoformat(last_activity_str)

                # Calcula el tiempo transcurrido desde la última actividad
                if (current_time - last_activity).total_seconds() > timeout:
                    # Cerrar sesión si se superó el tiempo de inactividad
                    logout(request)
                    return redirect('login')

            # Actualiza la última actividad a la hora actual (convertida a string)
            request.session['last_activity'] = current_time.isoformat()

        # Continua con la respuesta
        response = self.get_response(request)
        return response