"""
Modelos de base de datos para la aplicación IA.edu.

Este módulo define los modelos de Django utilizados para almacenar datos
persistentes, incluyendo tokens de recuperación de contraseña.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets


class PasswordResetToken(models.Model):
    """
    Modelo para almacenar tokens de recuperación de contraseña.
    
    Cada usuario que solicita recuperar su contraseña recibe un token único
    y seguro que expira después de 24 horas.
    
    Atributos:
        user: Relación OneToOne con el usuario (se elimina al eliminar usuario)
        token: Token único generado de forma segura
        created_at: Marca de tiempo de creación (automática)
        expires_at: Marca de tiempo de expiración (24 horas después de creación)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reset_token')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        """Verifica si el token sigue siendo válido (no ha expirado)."""
        return timezone.now() < self.expires_at

    def __str__(self):
        """Representación en texto del token para el panel admin."""
        return f"Token de recuperación para {self.user.email}"

