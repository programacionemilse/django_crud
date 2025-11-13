from django.db import models
#importamos la tabla usuario que viene con django con la cual hicimos el login
from django.contrib.auth.models import User

# Create your models here.
class Tarea(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    creada = models.DateTimeField(auto_now_add =True) #sino se pasa dato automaticamente pone fecha y hora actual
    fechora_completada = models.DateTimeField(null=True) #campo vacio inicialmente
    importante =models.BooleanField(default=False) #valor por defecto en falso
    usuario = models.ForeignKey(User, on_delete = models.CASCADE) #forenkey con la tabla usuario que viene por defecto en django

    def __str__(self):
        return self.titulo + '- por ' + self.usuario.username