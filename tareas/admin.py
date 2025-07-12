from django.contrib import admin
from .models import Task, TaskEvent

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'estado', 'prioridad')
    list_filter = ('estado', 'prioridad', 'usuario')
    search_fields = ('nombre', 'descripcion')

@admin.register(TaskEvent)
class TaskEventAdmin(admin.ModelAdmin):
    list_display = ('task', 'fecha', 'hora_inicio', 'hora_fin')
    list_filter = ('fecha', 'task__usuario')
    search_fields = ('task__nombre',)

# Register your models here.
