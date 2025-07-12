from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.task = Task.objects.create(
            usuario=self.user,
            nombre='Tarea de prueba',
            descripcion='Descripción de prueba',
            fecha_vencimiento='2025-12-31',
            estado='pendiente',
            prioridad='media'
        )

    def test_task_creation(self):
        """Prueba que una tarea se crea correctamente con todos sus campos."""
        self.assertEqual(self.task.nombre, 'Tarea de prueba')
        self.assertEqual(self.task.usuario.username, 'testuser')
        self.assertEqual(str(self.task), 'Tarea de prueba')

class TaskViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.task = Task.objects.create(
            usuario=self.user,
            nombre='Mi tarea personal',
            descripcion='Descripción',
            fecha_vencimiento='2025-12-31'
        )

    def test_task_list_view(self):
        """Prueba que la lista de tareas es accesible y muestra la tarea."""
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tareas/task_list.html')
        self.assertContains(response, 'Mi tarea personal')

    def test_task_detail_view(self):
        """Prueba que la vista de detalle de una tarea es accesible."""
        response = self.client.get(reverse('task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tareas/task_detail.html')
        self.assertContains(response, 'Mi tarea personal')

    def test_task_create_view(self):
        """Prueba que la página de creación de tareas es accesible."""
        response = self.client.get(reverse('task-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tareas/task_form.html')

    def test_unauthenticated_user_cannot_access_tasks(self):
        """Prueba que un usuario no autenticado es redirigido al login."""
        self.client.logout()
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_user_cannot_see_other_users_tasks(self):
        """Prueba que un usuario no puede ver las tareas de otro."""
        other_user = User.objects.create_user(username='otheruser', password='password')
        other_task = Task.objects.create(
            usuario=other_user,
            nombre='Tarea de otro usuario',
            descripcion='No deberías ver esto',
            fecha_vencimiento='2025-12-31'
        )
        response = self.client.get(reverse('task-list'))
        self.assertContains(response, 'Mi tarea personal')
        self.assertNotContains(response, 'Tarea de otro usuario')

# Para ejecutar estas pruebas, usa el comando: python manage.py test tareas