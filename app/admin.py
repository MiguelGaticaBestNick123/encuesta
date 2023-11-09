from django.contrib import admin
from .models import Encuesta, Alternativa, Pregunta, Respuesta, Voto, Like, Comentario, Notificacion, PerfilUsuario, Reporte

admin.site.register(Encuesta)
admin.site.register(Alternativa)
admin.site.register(Pregunta)
admin.site.register(Respuesta)
admin.site.register(Voto)
admin.site.register(Like)
admin.site.register(Comentario)
admin.site.register(Notificacion)
admin.site.register(PerfilUsuario)
admin.site.register(Reporte)
