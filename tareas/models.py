from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    """
    Representa la idea general de una tarea o hábito, sin información de tiempo.
    Ej: 'Estudiar Inglés', 'Hacer ejercicio'.
    """
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

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')

    def __str__(self):
        return self.nombre

class TaskEvent(models.Model):
    """
    Representa una ocurrencia específica de una Tarea en el calendario.
    Una Tarea puede tener muchos TaskEvents.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='events')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        ordering = ['fecha', 'hora_inicio']

    def __str__(self):
        return f"{self.task.nombre} - {self.fecha.strftime('%Y-%m-%d')} de {self.hora_inicio.strftime('%H:%M')} a {self.hora_fin.strftime('%H:%M')}"