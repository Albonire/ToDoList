from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path('horario/', views.ScheduleView.as_view(), name='task-schedule'),
    path('tarea/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tarea/<int:pk>/add-event/', views.AddEventView.as_view(), name='task-add-event'),
    path('tarea/nueva/', views.TaskCreateView.as_view(), name='task-create'),
    path('tarea/<int:pk>/editar/', views.TaskUpdateView.as_view(), name='task-update'),
    path('tarea/<int:pk>/eliminar/', views.TaskDeleteView.as_view(), name='task-delete'),
]
