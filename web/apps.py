"""
Configuración de la aplicación 'web' dentro del proyecto Django.

Este módulo define la configuración de metadatos de la aplicación
incluyendo el nombre, etiqueta, y tipo de campo automático para
claves primarias.
"""

from django.apps import AppConfig


class WebConfig(AppConfig):
    """
    Configuración de la aplicación 'web' (IA.edu).
    
    Atributos:
        default_auto_field: Tipo de campo para claves primarias automáticas
                           (BigAutoField para soportar IDs muy grandes)
        name: Nombre técnico de la aplicación (debe coincidir con carpeta)
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web'

