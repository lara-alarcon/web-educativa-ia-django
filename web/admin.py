"""
Configuración del panel de administración de Django.

Este módulo registra los modelos personalizados de la aplicación en el panel
administrativo de Django (/admin/), permitiendo que administradores gestionen
datos a través de una interfaz gráfica.

Modelos registrados:
- PasswordResetToken: Administración de tokens de recuperación de contraseña

NOTA: Los modelos de usuario (User, Group) ya están registrados por Django
      y se gestionan automáticamente en el admin.
"""

from django.contrib import admin
from .models import PasswordResetToken


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Interfaz de administración para tokens de recuperación de contraseña.
    
    Funcionalidades:
    - Visualizar lista de tokens activos/expirados
    - Buscar tokens por email o username del usuario
    - Ver fecha de creación y expiración
    - Verificar estado (válido/expirado) del token
    
    Campos de solo lectura (readonly_fields):
    - created_at: Fecha automática de creación
    - token: Token único (no se modifica tras creación)
    
    Columnas mostradas (list_display):
    - user: Usuario propietario del token
    - created_at: Cuándo se generó el token
    - expires_at: Cuándo expira (24 horas después)
    - is_valid(): Estado del token (método personalizado)
    
    Campos de búsqueda (search_fields):
    - Buscar por email o username del usuario
    """
    readonly_fields = ('created_at', 'token')  # No permitir edición de estos campos
    list_display = ('user', 'created_at', 'expires_at', 'is_valid')
    search_fields = ('user__email', 'user__username')

