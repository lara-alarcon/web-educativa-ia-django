"""
Configuración centralizada del proyecto Django 'IA.edu'.

Este módulo contiene la configuración de Django para la aplicación educativa
sobre Inteligencia Artificial, incluyendo:
- Base de datos (SQLite para desarrollo)
- Aplicaciones instaladas
- Middleware de seguridad
- Templates y autenticación
- Configuración de email para recuperación de contraseña

NOTA IMPORTANTE: En producción, cambiar:
- SECRET_KEY: Usar una clave segura aleatoria
- DEBUG = False: Desactivar modo debug
- ALLOWED_HOSTS: Agregar dominios permitidos
- EMAIL_BACKEND: Configurar SMTP real
"""

from pathlib import Path

# Directorio base del proyecto (carpeta padre de este archivo)
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================================
# SEGURIDAD - Configuración crítica para producción
# ============================================================================
# ADVERTENCIA: Cambiar estos valores antes de desplegar
SECRET_KEY = 'django-insecure-replace-this-with-a-secure-key'  # Clave secreta para firmar sesiones
DEBUG = True  # CAMBIAR A False EN PRODUCCIÓN
ALLOWED_HOSTS = ['.vercel.app', '127.0.0.1', 'localhost']  # AGREGAR DOMINIOS EN PRODUCCIÓN (ej: ['ia.edu', 'www.ia.edu'])

# ============================================================================
# APLICACIONES INSTALADAS
# ============================================================================
INSTALLED_APPS = [
    # Apps de Django (autenticación, admin panel, manejo de sesiones)
    'django.contrib.admin',           # Panel de administración
    'django.contrib.auth',            # Sistema de autenticación de usuarios
    'django.contrib.contenttypes',    # Framework de tipos de contenido
    'django.contrib.sessions',        # Gestión de sesiones de usuario
    'django.contrib.messages',        # Sistema de mensajes (notificaciones)
    'django.contrib.staticfiles',     # Servir archivos estáticos (CSS, JS, imágenes)
    
    # App personalizada
    'web',                            # Aplicación principal de IA.edu
]

# ============================================================================
# MIDDLEWARE - Capas de procesamiento de solicitudes/respuestas
# ============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',        # Encabezados de seguridad HTTP
    'django.contrib.sessions.middleware.SessionMiddleware', # Gestión de sesiones
    'django.middleware.common.CommonMiddleware',            # Validación de métodos HTTP y normalización de URLs
    'django.middleware.csrf.CsrfViewMiddleware',           # Protección contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Autenticación de usuarios
    'django.contrib.messages.middleware.MessageMiddleware', # Sistema de mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Protección contra clickjacking
]

# ============================================================================
# CONFIGURACIÓN DE URLS Y TEMPLATES
# ============================================================================
ROOT_URLCONF = 'iaedu.urls'  # Punto de entrada para enrutamiento

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Directorio de templates globales
        'APP_DIRS': True,                   # Buscar templates en carpetas de apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',     # Variable 'debug' en templates
                'django.template.context_processors.request',   # Variable 'request' en templates
                'django.contrib.auth.context_processors.auth',  # Variable 'user' en templates
                'django.contrib.messages.context_processors.messages',  # Variable 'messages' en templates
            ],
        },
    },
]

# ============================================================================
# WSGI - Interfaz Web Server Gateway Interface
# ============================================================================
WSGI_APPLICATION = 'iaedu.wsgi.application'

# ============================================================================
# BASE DE DATOS
# ============================================================================
# SQLite es suficiente para desarrollo. En producción usar PostgreSQL o MySQL

import os

if "VERCEL" in os.environ:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "/tmp/db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",  # Motor de base de datos
            "NAME": BASE_DIR / "db.sqlite3",         # Ruta del archivo de BD
        }
    }


# ============================================================================
# VALIDACIÓN DE CONTRASEÑAS
# ============================================================================
# Validadores que se aplican al crear/cambiar contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================================================
# INTERNACIONALIZACIÓN Y ZONA HORARIA
# ============================================================================
LANGUAGE_CODE = 'es'  # Idioma español
TIME_ZONE = 'UTC'     # Zona horaria universal
USE_I18N = True       # Habilitar internacionalización
USE_TZ = True         # Usar zonas horarias conscientes

# ============================================================================
# ARCHIVOS ESTÁTICOS (CSS, JS, Imágenes)
# ============================================================================
STATIC_URL = '/static/'  # URL para acceder a archivos estáticos
STATICFILES_DIRS = [     # Directorios adicionales para archivos estáticos
    BASE_DIR / 'static',  # Carpeta de archivos estáticos personalizados
    BASE_DIR / 'public'   # Carpeta de activos públicos
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Donde se copian archivos estáticos en producción

# ============================================================================
# CONFIGURACIÓN DE MODELOS Y CAMPOS
# ============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Tipo de campo ID por defecto

# ============================================================================
# AUTENTICACIÓN Y REDIRECCIONES
# ============================================================================
LOGIN_URL = '/login/'                  # URL para redirigir si no está autenticado
LOGIN_REDIRECT_URL = '/dashboard/'     # URL después de iniciar sesión exitosamente
LOGOUT_REDIRECT_URL = '/'              # URL después de cerrar sesión

# ============================================================================
# CONFIGURACIÓN DE EMAIL - Recuperación de contraseña
# ============================================================================
# En desarrollo: envía emails a la consola (no a servidor SMTP real)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Para producción, descomentar y configurar con SMTP real:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'                    # Servidor SMTP
# EMAIL_PORT = 587                                 # Puerto SMTP (TLS)
# EMAIL_USE_TLS = True                             # Usar encriptación TLS
# EMAIL_HOST_USER = 'tu-email@gmail.com'           # Email del remitente
# EMAIL_HOST_PASSWORD = 'tu-contraseña-aplicacion' # Contraseña de aplicación (NO la contraseña personal)
