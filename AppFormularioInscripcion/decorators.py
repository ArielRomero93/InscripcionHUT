from django.shortcuts import redirect
from functools import wraps

def usuario_autenticado(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            return redirect('login')  # Redirige al login si no está autenticado
        return func(request, *args, **kwargs)
    return wrapper
