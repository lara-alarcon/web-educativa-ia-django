"""
Configuración principal de URLs del proyecto Django.

Este módulo es el punto de entrada para el enrutamiento de URLs.
Aquí se definen:
- Panel de administración de Django
- Inclusión de URLs de la app 'web'
- Servir archivos estáticos en desarrollo

Todas las URLs de 'web' se sirven directamente en la raíz '/'
(no están bajo prefijo como /api/ o /web/)
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración de Django (manejo de BD y usuarios)
    # Accesible en /admin/ con credenciales de superusuario
    path('admin/', admin.site.urls),
    
    # Incluir todas las URLs de la app 'web' con prefijo raíz
    # Esto hace disponibles todas las rutas definidas en web/urls.py
    path('', include('web.urls')),
]

# En desarrollo, Django sirve archivos estáticos (CSS, JS, imágenes)
# En producción, esto debe ser manejado por un servidor web como Nginx
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
