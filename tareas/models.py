from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
    ]

    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    hora_inicio = models.TimeField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Create your models here.
