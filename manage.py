#!/usr/bin/env python
"""
Utilidad de línea de comandos para tareas administrativas de Django.

Este es el punto de entrada para ejecutar comandos de Django durante desarrollo:
- python manage.py runserver    # Inicia servidor de desarrollo
- python manage.py migrate      # Aplica migraciones a la BD
- python manage.py createsuperuser  # Crea usuario administrador
- python manage.py shell        # Abre shell interactivo de Python
- python manage.py collectstatic    # Recopila archivos estáticos

El script busca el módulo de configuración (settings.py) y ejecuta
el comando solicitado.
"""

import os
import sys


def main():
    """Punto de entrada principal para manage.py."""
    # Indicar a Django dónde encontrar la configuración
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iaedu.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. Asegúrate de que esté instalado en el entorno de Python."
        ) from exc
    
    # Ejecutar el comando de Django
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
