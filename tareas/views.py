from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import TaskForm
from .models import Task


class FormSuccessMessageMixin:
    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


class DeleteSuccessMessageMixin:
    success_message = ''

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tareas/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(usuario=self.request.user)
        estado = self.request.GET.get('estado')
        prioridad = self.request.GET.get('prioridad')
        if estado:
            queryset = queryset.filter(estado=estado)
        if prioridad:
            queryset = queryset.filter(prioridad=prioridad)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # El queryset base (context['tasks']) ya está filtrado por usuario en get_queryset
        
        # Contar tareas que NO están completadas
        context['count'] = context['tasks'].exclude(estado='completada').count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            # Filtrar por el campo 'nombre' que existe en el modelo
            context['tasks'] = context['tasks'].filter(
                nombre__icontains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tareas/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(usuario=self.request.user)


class TaskCreateView(LoginRequiredMixin, FormSuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tareas/task_form.html'
    success_url = reverse_lazy('task-list')
    success_message = "Tarea creada con éxito."

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, FormSuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'tareas/task_form.html'
    fields = ['nombre', 'descripcion', 'fecha_vencimiento', 'hora_inicio', 'estado', 'prioridad']
    success_url = reverse_lazy('task-list')
    success_message = "Tarea actualizada con éxito."

    def get_queryset(self):
        return Task.objects.filter(usuario=self.request.user)


class TaskDeleteView(LoginRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tareas/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')
    success_message = "Tarea eliminada con éxito."

    def get_queryset(self):
        return Task.objects.filter(usuario=self.request.user)


from datetime import timedelta

class ScheduleView(LoginRequiredMixin, ListView):
    template_name = 'tareas/schedule.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # No necesitamos un queryset principal aquí, lo manejaremos en get_context_data
        return Task.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Obtener tareas de la semana que tienen una hora de inicio asignada
        tasks_this_week = Task.objects.filter(
            usuario=self.request.user,
            fecha_vencimiento__range=[start_of_week, end_of_week],
            hora_inicio__isnull=False
        )

        # Organizar tareas por día
        schedule = {i: [] for i in range(7)}
        for task in tasks_this_week:
            day_index = task.fecha_vencimiento.weekday()
            schedule[day_index].append(task)

        # Ordenar las tareas de cada día por hora
        for day_tasks in schedule.values():
            day_tasks.sort(key=lambda x: x.hora_inicio)

        context['schedule'] = schedule
        context['week_dates'] = [start_of_week + timedelta(days=i) for i in range(7)]
        context['week_days'] = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        context['start_of_week'] = start_of_week
        context['end_of_week'] = end_of_week
        
        return context
