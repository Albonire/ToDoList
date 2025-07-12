from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['nombre', 'descripcion', 'fecha_vencimiento', 'hora_inicio', 'estado', 'prioridad']
        widgets = {
            'fecha_vencimiento': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'hora_inicio': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Título de la Tarea',
            'descripcion': 'Descripción Detallada',
            'fecha_vencimiento': 'Fecha de Vencimiento',
            'hora_inicio': 'Hora de Inicio (Opcional)',
        }
