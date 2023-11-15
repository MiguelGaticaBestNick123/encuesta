from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver




class Eliminable(models.Model):
    deleted = models.BooleanField(default=False)
    deleted_at = models.IntegerField(null=True, blank=True)
    delete_reason = models.TextField(null=True, blank=True)

    def mark_as_deleted(self):
        self.deleted = True
        self.deleted_at = int(datetime.datetime.now().timestamp())
        self.save()

    class Meta:
        abstract = True

class Encuesta(Eliminable):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    allow_extra_options = models.BooleanField(default=False)
    show_option_author = models.BooleanField(default=False)
    reward_points = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=[('Dr', 'Borrador'), ('PB', 'Publicada'), ('CL', 'Cerrada')])

class Alternativa(Eliminable):
    survey = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    text = models.CharField(max_length=100) #Eliminar
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    votes = models.IntegerField(default=0)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Pregunta(Eliminable): #No se implementará aún
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    question_text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Dr', 'Borrador'), ('PB', 'Publicada'), ('CL', 'Cerrada')])

class Respuesta(Eliminable): #No se usará ya que comentario es recursivo
    question = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Voto(models.Model): #Intersección entre Alternativa y Usuario
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)
    registered_user = models.BooleanField(default=True)
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comentario', on_delete=models.CASCADE)

class Comentario(Eliminable):
    survey = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    question = models.ForeignKey(Pregunta, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User, through=Like, related_name='liked_comments')

class Notificacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

class PerfilUsuario(Eliminable):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    theme = models.CharField(max_length=20, default='basic')
    description = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    profile_filter = models.CharField(max_length=20, default='none')
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfilusuario.save()

class Reporte(models.Model):
    REPORT_CHOICES = [
        ('SP', 'Spam'),
        ('VI', 'Violencia'),
        ('NS', 'Contenido sexual'),
        ('DI', 'Discriminación'),
        ('OT', 'Otro'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Encuesta, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Pregunta, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Alternativa, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comentario, on_delete=models.CASCADE, null=True, blank=True)
    report_type = models.CharField(max_length=2, choices=REPORT_CHOICES)
    description = models.TextField()
    reviewed = models.BooleanField(default=False, verbose_name="Revisado")