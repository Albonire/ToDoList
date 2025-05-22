from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'estado', 'prioridad', 'fecha_vencimiento')
    list_filter = ('estado', 'prioridad', 'usuario')
    search_fields = ('nombre', 'descripcion')

# Register your models here.
