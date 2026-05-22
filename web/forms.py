"""
Formularios de validación para la aplicación IA.edu.

Este módulo define formularios Django que validan datos de usuario para:
- Autenticación (login)
- Registro de nuevos usuarios
- Recuperación y cambio de contraseña

Los formularios incluyen validación de datos, mensajes de error personalizados
y verificaciones de seguridad como contraseñas coincidentes y emails únicos.
"""

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """
    Formulario de inicio de sesión.
    
    Campos:
    - email: Correo electrónico del usuario (se usa para buscar username)
    - password: Contraseña de la cuenta
    - remember_me: Opción para mantener sesión activa (sin expiración)
    
    Validación personalizada:
    - Verifica que exista un usuario con ese email
    - Autentica el usuario contra la base de datos
    - Devuelve el objeto 'user' si las credenciales son correctas
    """
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'usuario@email.com'}),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
    )
    remember_me = forms.BooleanField(
        required=False,  # No es obligatorio marcarlo
        label='Recordarme',
        widget=forms.CheckboxInput(),
    )

    def clean(self):
        """
        Validación personalizada del formulario completo.
        
        Se ejecuta después de validar campos individuales.
        Aquí autenticamos el usuario contra la BD.
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                # Buscar usuario por email (convertiéndolo a username)
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError('El correo o la contraseña son incorrectos.')

            # Autenticar usuario (verifica contraseña hash)
            user = authenticate(username=user.username, password=password)
            if user is None:
                raise forms.ValidationError('El correo o la contraseña son incorrectos.')

            # Guardar usuario autenticado para usarlo en la vista
            cleaned_data['user'] = user
        return cleaned_data


class RegisterForm(forms.Form):
    """
    Formulario de registro de nuevos usuarios.
    
    Campos:
    - name: Nombre completo del usuario (máx 150 caracteres)
    - email: Correo electrónico (debe ser único)
    - password: Contraseña (mínimo 6 caracteres)
    - confirm_password: Confirmación de contraseña (debe coincidir)
    
    Validaciones:
    - Email único: Verifica que no exista otro usuario con ese email
    - Contraseñas coinciden: Las dos contraseñas deben ser idénticas
    - Contraseña segura: Mínimo 6 caracteres
    """
    name = forms.CharField(
        label='Nombre completo',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'usuario@email.com'}),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
        min_length=6,
    )
    confirm_password = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
    )

    def clean_email(self):
        """
        Validación personalizada del campo email.
        
        Se ejecuta automáticamente para validar solo este campo.
        Verifica que el email sea único en la BD.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo.')
        return email

    def clean(self):
        """
        Validación del formulario completo.
        
        Verifica que las contraseñas coincidan.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned_data


class PasswordResetRequestForm(forms.Form):
    """
    Formulario para solicitar recuperación de contraseña.
    
    Campos:
    - email: Correo electrónico de la cuenta a recuperar
    
    Validación:
    - Verifica que exista una cuenta con ese email
    - Si el email no existe, muestra error
    """
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'usuario@email.com'}),
    )

    def clean_email(self):
        """
        Validación del campo email.
        
        Verifica que exista una cuenta registrada con ese email.
        """
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('No existe una cuenta con este correo.')
        return email


class PasswordResetForm(forms.Form):
    """
    Formulario para cambiar contraseña durante recuperación.
    
    Campos:
    - new_password: Nueva contraseña (mínimo 6 caracteres)
    - confirm_password: Confirmación de la nueva contraseña
    
    Validación:
    - Contraseñas coinciden: Ambos campos deben ser idénticos
    - Contraseña segura: Mínimo 6 caracteres
    
    Este formulario se usa en el flujo de recuperación de contraseña
    después de verificar el token.
    """
    new_password = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
        min_length=6,
    )
    confirm_password = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
    )

    def clean(self):
        """
        Validación del formulario.
        
        Verifica que ambas contraseñas sean idénticas.
        """
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned_data
