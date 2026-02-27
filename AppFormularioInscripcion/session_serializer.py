from django.contrib.sessions.serializers import JSONSerializer
from datetime import datetime

class CustomSessionSerializer(JSONSerializer):
    def default(self, obj):
        # Si el objeto es un datetime, lo convertimos a un formato de cadena
        if isinstance(obj, datetime):
            return obj.isoformat()  # Cambiar el formato si lo necesitas
        # Para otros tipos que no sean serializables, llamamos al serializer por defecto
        return super().default(obj)
