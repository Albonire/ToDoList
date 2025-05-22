# ToDoList

## Description

This is a simple web-based ToDo list application built with Django. It allows users to create, view, update, and delete tasks. Users can also register and log in to manage their own tasks.

## Project Structure

The project follows a standard Django project structure:

- `manage.py`: Django's command-line utility for administrative tasks.
- `gestor_tareas/`: The main project directory.
    - `__init__.py`: Marks the directory as a Python package.
    - `asgi.py`: ASGI entry point for the project.
    - `settings.py`: Project settings.
    - `urls.py`: Project-level URL configurations.
    - `wsgi.py`: WSGI entry point for the project.
- `tareas/`: The main application directory for ToDo list functionality.
    - `__init__.py`: Marks the directory as a Python package.
    - `admin.py`: Django admin configurations for the app.
    - `apps.py`: Application configuration.
    - `forms.py`: Django forms for task creation and updates.
    - `models.py`: Database models for tasks.
    - `tests.py`: Application tests.
    - `urls.py`: Application-level URL configurations.
    - `views.py`: Views that handle request logic.
- `templates/`: Directory for HTML templates.
    - `base.html`: Base template for consistent site structure.
    - `registration/`: Templates for user authentication.
        - `login.html`: Login page template.
        - `logout.html`: Logout confirmation page template.
        - `register.html`: User registration page template.
    - `tareas/`: Templates specific to the tasks application.
        - `task_confirm_delete.html`: Template for confirming task deletion.
        - `task_detail.html`: Template for displaying a single task.
        - `task_form.html`: Template for creating and updating tasks.
        - `task_list.html`: Template for displaying the list of tasks.
- `static/`: Directory for static files (CSS, JavaScript, images).
    - `css/estilos.css`: Custom CSS file.
- `staticfiles/`: Directory where static files are collected (managed by Django).
- `tareas/migrations/`: Directory for database schema migrations.
- `.idx/`: Directory for indexing (likely related to development environment setup).
- `.vscode/`: Directory for VS Code editor settings.

## Setup Instructions

1. **Clone the repository:**
