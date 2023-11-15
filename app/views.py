from django.shortcuts import render
from .models import Encuesta, Voto, Pregunta, PerfilUsuario
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count



def home(request):
    # Esto obtendrá  la fecha y hora actuales
    now = timezone.now()
    # Esto calcula la fecha y hora de hace una semana
    week_ago = now - timedelta(weeks=1)
    # Mes 
    month_ago = now - timedelta(weeks=4)
    # Obtener los perfiles y ordenarlos por el número de puntos
    perfil_usuario = PerfilUsuario.objects.order_by('-reward_points')
    # Obtiene los 10 primeros perfiles más votados
    top_users = perfil_usuario[:10]
    # Obtén todas las encuestas de la última semana y anota cada una con el número total de votos
    encuestas = Encuesta.objects.filter(created_at__gte=week_ago).annotate(num_votos=Count('alternativa__voto'))
    # Ordena las encuestas por el número     de votos
    encuestas = encuestas.order_by('-num_votos')
    # Llamará a la  encuesta más votada
    encuesta_mas_votada = encuestas.first()
    # Obtén todas las preguntas de la última semana y anota cada una con el número total de votos
    preguntas = Pregunta.objects.filter(created_at__gte=week_ago).annotate(num_votos=Count('respuesta__voto'))
    # Ordena las preguntas por el número de votos
    preguntas = preguntas.order_by('-num_votos')
    # Llamará a la pregunta más votada
    pregunta_mas_votada = preguntas.first()
    return render(request, 'home.html', {'encuesta_mas_votada': encuesta_mas_votada, 'pregunta_mas_votada': pregunta_mas_votada, 'top_users': top_users})
