# Gestor de Tareas Avanzado

Este es un proyecto Django que implementa una aplicación de lista de tareas (To-Do list) con funcionalidades avanzadas, incluyendo autenticación de usuarios, gestión de tareas personales, y una interfaz limpia y moderna.

## Características

- **Autenticación de Usuarios:** Sistema completo de registro, inicio de sesión y cierre de sesión.
- **Gestión de Tareas (CRUD):** Los usuarios pueden crear, ver, actualizar y eliminar sus propias tareas.
- **Seguridad:** Cada usuario solo puede acceder a sus propias tareas. Las vistas están protegidas y requieren inicio de sesión.
- **Filtrado y Búsqueda:** Permite buscar tareas por título y filtrar por estado o prioridad.
- **Notificaciones:** Feedback visual para el usuario al crear, actualizar o eliminar tareas.
- **Diseño Responsivo:** Interfaz adaptable a diferentes tamaños de pantalla.

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación y Puesta en Marcha

1.  **Clona el repositorio:**
    ```bash
    git clone <URL-del-repositorio>
    cd ToDoList
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crea un archivo `.env`:**
    Copia el contenido de `.env.example` (o créalo desde cero) en un nuevo archivo llamado `.env` en la raíz del proyecto. Este archivo contendrá la `SECRET_KEY` y la configuración de `DEBUG`.
    ```
    SECRET_KEY='tu-clave-secreta-aqui'
    DEBUG=True
    ```

5.  **Aplica las migraciones de la base de datos:**
    ```bash
    python manage.py migrate
    ```

6.  **Crea un superusuario (opcional):**
    Esto te permitirá acceder al panel de administración de Django.
    ```bash
    python manage.py createsuperuser
    ```

7.  **Ejecuta el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```

¡La aplicación estará disponible en `http://127.0.0.1:8000/`!