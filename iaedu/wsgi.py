"""
Punto de entrada WSGI (Web Server Gateway Interface) para el proyecto.

WSGI es el estándar Python para servir aplicaciones web. Este archivo
se usa cuando se despliega la aplicación en un servidor de producción
como Gunicorn, uWSGI, ou Apache.

Flujo:
1. El servidor web importa 'application' desde este módulo
2. Configura el módulo de configuración de Django
3. Obtiene la aplicación WSGI de Django
4. El servidor delega solicitudes HTTP a través de esta aplicación

En desarrollo, se usa 'python manage.py runserver' (no requiere WSGI).
"""

import os
from django.core.wsgi import get_wsgi_application

# Indicar a Django qué módulo de configuración usar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iaedu.settings')

# --- MIGRACIONES EN VERCEL ---
from django.core.management import call_command

# Obtener la aplicación WSGI configurada
application = get_wsgi_application()

# Ejecuta las migraciones automáticamente en la carpeta /tmp de Vercel
try:
    call_command('migrate', interactive=False)
except Exception as e:
    print(f"Error al correr las migraciones: {e}")
