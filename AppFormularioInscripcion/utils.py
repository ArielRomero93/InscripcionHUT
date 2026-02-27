from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def enviar_correo(destinatario, asunto, mensaje, html=False):
    msg = EmailMultiAlternatives(
        asunto,
        mensaje,
        settings.EMAIL_HOST_USER,
        [destinatario]
    )

    if html:
        msg.attach_alternative(mensaje, "text/html")

    msg.send()

def enviar_correo_recuperacion(destinatario, nombre_usuario, reset_url):
    asunto = 'Restablecer tu contraseña'
    mensaje_html = render_to_string('registroLogueo/password_reset_email_template.html', {
        'nombre': nombre_usuario,
        'reset_url': reset_url,
    })

    enviar_correo(destinatario, asunto, mensaje_html, html=True)




#Ejemplo para el futuro


# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.conf import settings
#
# def enviar_correo(destinatario, asunto, mensaje, html=False, tipo_correo):
#     # Elegir la configuración de correo según el tipo de correo
#     if tipo_correo == 'recuperacion':
#         email_host_user = settings.EMAIL_HOST_USER_SENDGRID
#         email_host_password = settings.EMAIL_HOST_PASSWORD_SENDGRID
#         email_backend = settings.EMAIL_BACKEND_SENDGRID
#     else:
#         email_host_user = settings.EMAIL_HOST_USER_GMAIL
#         email_host_password = settings.EMAIL_HOST_PASSWORD_GMAIL
#         email_backend = settings.EMAIL_BACKEND_GMAIL
#
#     # Crear el mensaje
#     msg = EmailMultiAlternatives(
#         asunto,
#         mensaje,
#         email_host_user,
#         [destinatario]
#     )
#
#     if html:
#         msg.attach_alternative(mensaje, "text/html")
#
#     msg.send()
#
# def enviar_correo_inscripcion(destinatario, nombre_usuario):
#     asunto = 'Bienvenido a nuestra plataforma'
#     mensaje_html = render_to_string('registroLogueo/inscripcion_email_template.html', {
#         'nombre': nombre_usuario,
#     })
#     enviar_correo(destinatario, asunto, mensaje_html, html=True, tipo_correo='inscripcion')
#
# def enviar_correo_recuperacion(destinatario, nombre_usuario, reset_url):
#     asunto = 'Restablecer tu contraseña'
#     mensaje_html = render_to_string('registroLogueo/password_reset_email_template.html', {
#         'nombre': nombre_usuario,
#         'reset_url': reset_url,
#     })
#     enviar_correo(destinatario, asunto, mensaje_html, html=True, tipo_correo='recuperacion')
