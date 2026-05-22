"""
Vistas (controladores) de la aplicación IA.edu.

Este módulo implementa las vistas que manejan:
- Página de inicio
- Autenticación (login, registro, logout)
- Recuperación de contraseña con tokens seguros
- Rutas del dashboard educativo

Cada vista recibe una solicitud HTTP y devuelve una respuesta (HTML, redirección, etc.)
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import secrets

from .forms import LoginForm, RegisterForm, PasswordResetRequestForm, PasswordResetForm
from .models import PasswordResetToken


def home(request):
    """
    Vista de página de inicio.
    
    Renderiza la página principal con información sobre la plataforma educativa.
    No requiere autenticación (accesible para todos).
    """
    return render(request, 'home.html')


def auth_page(request):
    """
    Vista de autenticación - Login y Registro unificados.
    
    Maneja dos formularios en una misma página:
    - Formulario de LOGIN: Autenticación de usuarios existentes
    - Formulario de REGISTRO: Creación de nuevas cuentas
    
    El usuario puede cambiar entre ellos usando los tabs sin recargar la página.
    
    Flujo:
    1. GET: Muestra los formularios vacíos (modo login por defecto)
    2. POST (login): Verifica credenciales y crea sesión
    3. POST (registro): Valida datos, crea usuario y lo autentica automáticamente
    
    Parámetro GET 'mode': puede ser 'login' o 'register' (por defecto 'login')
    Parámetro POST 'form_type': indica qué formulario se envió
    """
    login_form = LoginForm()
    register_form = RegisterForm()
    mode = request.GET.get('mode', 'login')

    if request.method == 'POST':
        # Procesar registro de nueva cuenta
        if request.POST.get('form_type') == 'register':
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                # Extraer datos del formulario validado
                name = register_form.cleaned_data['name']
                email = register_form.cleaned_data['email']
                password = register_form.cleaned_data['password']
                
                # Usar email como nombre de usuario (único y fácil de recordar)
                username = email
                
                # Crear usuario en la base de datos
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = name  # Guardar nombre completo
                user.save()
                
                # Autenticar e iniciar sesión automáticamente
                login(request, user)
                request.session.set_expiry(None)  # Sesión permanente
                return redirect('dashboard')
        
        # Procesar login de usuario existente
        else:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # El formulario ya autentica el usuario
                user = login_form.cleaned_data['user']
                remember_me = login_form.cleaned_data.get('remember_me', False)
                
                # Crear sesión (opcionalmente permanente si "recordarme" está marcado)
                login(request, user)
                request.session.set_expiry(None if remember_me else 0)
                return redirect('dashboard')
        
        # Si hay error, indicar qué formulario estaba en uso
        mode = request.POST.get('form_type', 'login')

    return render(
        request,
        'login.html',
        {
            'login_form': login_form,
            'register_form': register_form,
            'mode': mode,  # Para mostrar el formulario correcto en el navegador
        },
    )


def logout_user(request):
    """
    Vista de cierre de sesión.
    
    Destruye la sesión del usuario y lo redirige a la página de inicio.
    """
    logout(request)
    return redirect('home')


@login_required  # Esta vista solo es accesible para usuarios autenticados
def dashboard_home(request):
    """
    Vista del dashboard - Módulo 01: Definición de IA.
    
    Muestra contenido educativo sobre la definición de Inteligencia Artificial.
    Requiere que el usuario esté autenticado.
    
    hide_navbar=True: Oculta la navbar superior en el dashboard
    """
    return render(request, 'dashboard/index.html', {'hide_navbar': True})


@login_required
def dashboard_tipos_de_redes(request):
    """
    Vista del dashboard - Módulo 03: Tipos de Redes Neuronales.
    
    Muestra contenido sobre diferentes arquitecturas de redes neuronales:
    - Redes Feedforward (FNN)
    - Redes Convolucionales (CNN)
    - Redes Recurrentes (RNN)
    - Redes Adversariales (GAN)
    """
    return render(request, 'dashboard/tipos_de_redes.html', {'hide_navbar': True})


@login_required
def dashboard_redes_neuronales(request):
    """
    Vista del dashboard - Módulo 02: Redes Neuronales Artificiales.
    
    Muestra conceptos fundamentales sobre redes neuronales:
    - Estructura biológica vs artificial
    - Cómo funcionan
    - Procesos de aprendizaje
    """
    return render(request, 'dashboard/redes_neuronales.html', {'hide_navbar': True})


@login_required
def dashboard_autores(request):
    """
    Vista del dashboard - Módulo 04: Autores y Pioneros de la IA.
    
    Muestra perfiles y contribuciones de científicos destacados:
    - Geoffrey Hinton
    - Yann LeCun
    - Otros pioneros en IA
    """
    return render(request, 'dashboard/autores.html', {'hide_navbar': True})


def password_reset_request(request):
    """
    Vista para solicitar recuperación de contraseña.
    
    Flujo:
    1. GET: Muestra formulario para ingresar email
    2. POST: 
       - Valida que el email exista en la BD
       - Genera token único y seguro (válido 24 horas)
       - Envía email con enlace de recuperación
       - Redirige a login con mensaje de confirmación
    
    Seguridad:
    - Los tokens se generan con secrets.token_urlsafe (criptográficamente seguros)
    - Se limpia el token anterior si existe uno vigente
    - Token expira en 24 horas
    """
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Obtener usuario por email
            user = User.objects.get(email=email)

            # Eliminar token anterior si existe (evitar múltiples tokens activos)
            PasswordResetToken.objects.filter(user=user).delete()

            # Crear nuevo token seguro
            token = secrets.token_urlsafe(32)  # Token aleatorio de 32 bytes
            expires_at = timezone.now() + timedelta(hours=24)  # Válido 24 horas
            reset_token = PasswordResetToken.objects.create(
                user=user,
                token=token,
                expires_at=expires_at,
            )

            # Construir URL del enlace de recuperación
            reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'token': token}))
            subject = 'Recuperación de contraseña — IA.edu'
            message = f"""
Hola {user.first_name or user.username},

Recibimos una solicitud para recuperar tu contraseña. 

Haz clic en el siguiente enlace para crear una nueva contraseña:
{reset_url}

Este enlace expirará en 24 horas.

Si no solicitaste este cambio, ignora este correo.

Saludos,
Equipo IA.edu
            """
            try:
                # Enviar email (en desarrollo se imprime en consola)
                send_mail(subject, message, 'noreply@ia.edu', [email])
                messages.success(request, 'Se ha enviado un enlace de recuperación a tu correo electrónico.')
                return redirect('login')
            except Exception as e:
                messages.error(request, 'Error al enviar el correo. Por favor, intenta más tarde.')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'password_reset_request.html', {'form': form})


def password_reset_confirm(request, token):
    """
    Vista para confirmar recuperación de contraseña y cambiarla.
    
    Parámetro URL:
    - token: Token único del usuario (debe ser válido y no expirado)
    
    Flujo:
    1. Verifica que el token exista y sea válido (no expirado)
    2. GET: Muestra formulario para ingresar nueva contraseña
    3. POST:
       - Valida que las contraseñas coincidan
       - Cambia la contraseña del usuario
       - Elimina el token (no se puede reutilizar)
       - Redirige a login
    
    Errores:
    - Token inválido: Redirige a solicitar nuevo token
    - Token expirado: Muestra mensaje y redirige a solicitar nuevo
    """
    # Obtener token o mostrar 404 si no existe
    reset_token = get_object_or_404(PasswordResetToken, token=token)

    # Verificar que el token aún sea válido (no haya expirado)
    if not reset_token.is_valid():
        messages.error(request, 'El enlace de recuperación ha expirado. Por favor, solicita uno nuevo.')
        return redirect('password_reset_request')

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = reset_token.user
            
            # Cambiar contraseña (hash automático)
            user.set_password(new_password)
            user.save()

            # Eliminar token (no se puede reutilizar)
            reset_token.delete()

            messages.success(request, 'Tu contraseña ha sido actualizada. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = PasswordResetForm()

    return render(request, 'password_reset_confirm.html', {'form': form, 'token': token})
