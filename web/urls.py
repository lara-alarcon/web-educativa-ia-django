"""
Configuración de URLs para la aplicación 'web' (IA.edu).

Este módulo define todas las rutas disponibles en la plataforma:
- Página de inicio
- Autenticación (login, registro, logout)
- Recuperación de contraseña
- Dashboard educativo (4 módulos)

Las URLs se incluyen en iaedu/urls.py con el prefijo raíz '/'.
"""

from django.urls import path
from . import views

# Patrón de nombres de URL reutilizables con {% url 'nombre' %} en templates
urlpatterns = [
    # Página pública
    path('', views.home, name='home'),
    
    # Autenticación
    path('login/', views.auth_page, name='login'),              # Login y Registro
    path('logout/', views.logout_user, name='logout'),          # Cerrar sesión
    
    # Recuperación de contraseña
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # Dashboard - Módulos educativos
    path('dashboard/', views.dashboard_home, name='dashboard'),                          # Módulo 1: Definición IA
    path('dashboard/tipos-de-redes/', views.dashboard_tipos_de_redes, name='dashboard_tipos_de_redes'),
    path('dashboard/redes-neuronales/', views.dashboard_redes_neuronales, name='dashboard_redes_neuronales'),
    path('dashboard/autores/', views.dashboard_autores, name='dashboard_autores'),       # Módulo 4: Autores
]
