from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import date, time, timedelta
from .models import Task
from django.contrib.auth.models import User

class TaskViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.now = timezone.now()

    def test_create_task_with_times(self):
        response = self.client.post(reverse('task-create'), {
            'nombre': 'Test Task with Times',
            'descripcion': 'Test Description',
            'fecha_vencimiento': self.now.date(),
            'hora_inicio': '09:00',
            'hora_fin': '17:00',
            'estado': 'pendiente',
            'prioridad': 'media',
        })
        self.assertEqual(response.status_code, 302) # Should redirect after successful creation
        task = Task.objects.get(nombre='Test Task with Times')
        self.assertEqual(task.hora_inicio, time(9, 0))
        self.assertEqual(task.hora_fin, time(17, 0))
        self.assertEqual(task.usuario, self.user)

    def test_update_task_with_times(self):
        task = Task.objects.create(
            usuario=self.user,
            nombre='Initial Task',
            descripcion='Initial Description',
            fecha_vencimiento=self.now.date(),
            estado='pendiente',
            prioridad='media'
        )
        response = self.client.post(reverse('task-update', args=[task.pk]), {
            'nombre': 'Updated Task with Times',
            'descripcion': 'Updated Description',
            'fecha_vencimiento': self.now.date() + timedelta(days=1),
            'hora_inicio': '10:00',
            'hora_fin': '18:00',
            'estado': 'en_progreso',
            'prioridad': 'alta',
        })
        self.assertEqual(response.status_code, 302) # Should redirect after successful update
        updated_task = Task.objects.get(pk=task.pk)
        self.assertEqual(updated_task.nombre, 'Updated Task with Times')
        self.assertEqual(updated_task.hora_inicio, time(10, 0))
        self.assertEqual(updated_task.hora_fin, time(18, 0))
        self.assertEqual(updated_task.fecha_vencimiento, self.now.date() + timedelta(days=1))
        self.assertEqual(updated_task.estado, 'en_progreso')
        self.assertEqual(updated_task.prioridad, 'alta')

class TaskOverdueTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.now = timezone.now()

    def test_overdue_task_past_date(self):
        Task.objects.create(
            usuario=self.user,
            nombre='Past Task',
            descripcion='Test',
            fecha_vencimiento=self.now.date() - timedelta(days=1),
            hora_fin=time(10, 0) 
        )
        response = self.client.get(reverse('task-list'))
        self.assertContains(response, 'task-overdue') 
        self.assertContains(response, '¡Vencida!')

    def test_overdue_task_today_past_time(self):
        Task.objects.create(
            usuario=self.user,
            nombre='Today Past Task',
            descripcion='Test',
            fecha_vencimiento=self.now.date(),
            hora_fin=(self.now - timedelta(hours=1)).time()
        )
        response = self.client.get(reverse('task-list'))
        self.assertContains(response, 'task-overdue')
        self.assertContains(response, '¡Vencida!')

    def test_not_overdue_task_today_future_time(self):
        Task.objects.create(
            usuario=self.user,
            nombre='Today Future Task',
            descripcion='Test',
            fecha_vencimiento=self.now.date(),
            hora_fin=(self.now + timedelta(hours=1)).time()
        )
        response = self.client.get(reverse('task-list'))
        self.assertNotContains(response, 'task-overdue')
        self.assertNotContains(response, '¡Vencida!')
    
    def test_not_overdue_task_future_date(self):
        Task.objects.create(
            usuario=self.user,
            nombre='Future Task',
            descripcion='Test',
            fecha_vencimiento=self.now.date() + timedelta(days=1),
            hora_fin=time(10,0)
        )
        response = self.client.get(reverse('task-list'))
        self.assertNotContains(response, 'task-overdue')
        self.assertNotContains(response, '¡Vencida!')

    def test_task_not_overdue_today_no_end_time(self):
        Task.objects.create(
            usuario=self.user,
            nombre='Today No End Time Task',
            descripcion='Test',
            fecha_vencimiento=self.now.date(),
            hora_fin=None 
        )
        response = self.client.get(reverse('task-list'))
        self.assertNotContains(response, 'task-overdue')
        self.assertNotContains(response, '¡Vencida!')
