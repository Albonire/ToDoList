from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Task
from .forms import TaskForm

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
        from datetime import date, timedelta
        try:
            print("Obteniendo contexto...")  # Mensaje de depuración
            context = super().get_context_data(**kwargs)
            print(f"Contexto base: {context}")  # Mensaje de depuración
            
            # Asegurarse de que Task tenga los atributos necesarios
            print(f"Task.ESTADO_CHOICES: {hasattr(Task, 'ESTADO_CHOICES')}")
            print(f"Task.PRIORIDAD_CHOICES: {hasattr(Task, 'PRIORIDAD_CHOICES')}")
            
            context['estados'] = Task.ESTADO_CHOICES
            context['prioridades'] = Task.PRIORIDAD_CHOICES
            context['estado_actual'] = self.request.GET.get('estado', '')
            context['prioridad_actual'] = self.request.GET.get('prioridad', '')
            context['now'] = timezone.now()
            
            print(f"Contexto final: {context}")  # Mensaje de depuración
            return context
        except Exception as e:
            print(f"Error en get_context_data: {str(e)}")  # Mensaje de error
            raise  # Vuelve a lanzar la excepción para ver el error completo

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tareas/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(usuario=self.request.user)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tareas/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tareas/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

    def get_queryset(self):
        return Task.objects.filter(usuario=self.request.user)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tareas/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    def get_queryset(self):
        return Task.objects.filter(usuario=self.request.user)
