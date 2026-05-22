# ARQUITECTURA DEL PROYECTO — IA.edu

## Diagrama de Flujo General

```
Cliente (Navegador)
        ↓
    [Frontend: HTML/CSS/JS]
        ↓
HTTP Request → Django Router (urls.py)
        ↓
  Middleware (CSRF, Auth, Security)
        ↓
  Vista (View) → Modelo (Model) ↔ Base de Datos
        ↓
    Template Engine
        ↓
HTML Response → Cliente
```

---

## Patrones de Diseño

### Patrón MTV (Model-Template-View)
Django implementa MTV, similar a MVC:

```
Model  → Capa de datos (web/models.py)
         Define estructura de BD
         Relaciones entre datos

Template → Capa de presentación (templates/)
           HTML con lógica de plantilla
           Renderiza datos dinámicamente

View   → Capa de lógica de negocio (web/views.py)
         Procesa solicitudes HTTP
         Interactúa con modelos
         Retorna respuestas
```

---

## Flujo de Autenticación

### Registro de Usuario

```
1. Usuario accede a /login/?mode=register
   ↓
2. Muestra formulario RegisterForm
   ↓
3. Usuario completa: nombre, email, contraseña
   ↓
4. POST a /login/ con form_type=register
   ↓
5. Validaciones en RegisterForm:
   - Email único (no existe en BD)
   - Contraseñas coinciden
   - Contraseña mínimo 6 caracteres
   ↓
6. Si válido:
   - Crea User en BD con email como username
   - Guarda nombre en first_name
   - Crea sesión automáticamente
   ↓
7. Redirige a /dashboard/
```

### Login de Usuario

```
1. Usuario accede a /login/?mode=login
   ↓
2. Muestra formulario LoginForm
   ↓
3. Usuario ingresa: email, contraseña
   ↓
4. POST a /login/ con form_type=login
   ↓
5. Validaciones en LoginForm:
   - Email existe en BD
   - Contraseña es correcta (hash)
   ↓
6. Si válido:
   - Crea sesión de usuario
   - Si "recordarme": sesión indefinida
   - Si no: sesión de navegador (se cierra al salir)
   ↓
7. Redirige a /dashboard/
```

### Recuperación de Contraseña

```
1. Usuario accede a /password-reset/
   ↓
2. Ingresa email registrado
   ↓
3. Backend genera token seguro:
   - token = secrets.token_urlsafe(32)
   - Válido 24 horas
   - Único por usuario
   ↓
4. Construye URL: /password-reset/<token>/
   ↓
5. Envía email con enlace
   ↓
6. Usuario hace click en enlace
   ↓
7. GET /password-reset/<token>/:
   - Verifica token existe
   - Verifica token no expiró
   - Muestra formulario cambio contraseña
   ↓
8. Usuario ingresa nueva contraseña
   ↓
9. POST /password-reset/<token>/:
   - Valida contraseñas coincidan
   - Cambia contraseña (hash)
   - Elimina token (no reutilizable)
   ↓
10. Redirige a /login/
```

---

## Capas de Seguridad

### Nivel 1: Middleware
```python
SecurityMiddleware      → Headers de seguridad HTTP
SessionMiddleware       → Gestión de sesiones
CsrfViewMiddleware      → Protección contra CSRF
AuthenticationMiddleware → Autenticación de usuario
```

### Nivel 2: Vistas
```python
@login_required  # Solo usuarios autenticados
def dashboard_home(request):
    # Si no autenticado → redirige a /login/
    ...
```

### Nivel 3: Formularios
```python
class LoginForm:
    def clean(self):
        # Valida email existe
        # Valida contraseña correcta
        # Autentica contra BD
```

### Nivel 4: Modelos
```python
class PasswordResetToken:
    def is_valid(self):
        # Verifica expiración
        return timezone.now() < self.expires_at
```

---

## Modelo de Datos

### Diagrama de Entidades

```
User (Django Built-in)
├── id (PK)
├── username
├── email (UNIQUE)
├── password (hash)
├── first_name
├── last_name
├── is_active
├── is_staff
└── date_joined

PasswordResetToken
├── id (PK)
├── user (FK → User, OneToOne)
├── token (UNIQUE, CharField)
├── created_at (auto_now_add)
└── expires_at (DateTime)
```

### Relaciones
- User → PasswordResetToken: **1 a 1** (un usuario, un token activo)
- Token se elimina al crear nuevo (evita múltiples tokens)

---

## Rutas y Vistas

### Rutas Públicas (sin autenticación)

```
GET  /                          → home()
     │ Página inicio con info
     
GET/POST /login/                → auth_page()
     │ Login y Registro
     
GET  /password-reset/           → password_reset_request()
POST /password-reset/           │ Solicitar recuperación
     │ 
GET/POST /password-reset/<token>/ → password_reset_confirm()
     │ Cambiar contraseña
     
GET  /logout/                   → logout_user()
     │ Cerrar sesión
```

### Rutas Protegidas (requieren login)

```
@login_required

GET  /dashboard/                → dashboard_home()
     │ Módulo 1: Definición IA
     
GET  /dashboard/tipos-de-redes/    → dashboard_tipos_de_redes()
     │ Módulo 3: Tipos Redes
     
GET  /dashboard/redes-neuronales/  → dashboard_redes_neuronales()
     │ Módulo 2: Redes Neuronales
     
GET  /dashboard/autores/           → dashboard_autores()
     │ Módulo 4: Autores
```

---

## Contexto de Templates

### Contexto Disponible en Todos los Templates

```python
{
    'request': request,              # Objeto HTTP request
    'user': request.user,            # Usuario actual
    'hide_navbar': True/False,       # Mostrar/ocultar navbar
}
```

### Contexto de Vistas de Autenticación

```python
# auth_page()
{
    'login_form': LoginForm(),
    'register_form': RegisterForm(),
    'mode': 'login',  # o 'register'
}
```

### Contexto de Password Reset

```python
# password_reset_confirm()
{
    'form': PasswordResetForm(),
    'token': '<token_único>',
}
```

---

## Responsividad

### Breakpoints (definidos en CSS media queries)

```css
/* Mobile-first approach */

/* Hasta 768px: Móvil */
.mobile-menu { display: block; }
.desktop-nav { display: none; }

/* 768px+: Tablet */
@media (min-width: 768px) {
    .mobile-menu { display: none; }
    .desktop-nav { display: flex; }
}

/* 1024px+: Desktop */
@media (min-width: 1024px) {
    .container { max-width: 1024px; }
}
```

### Componentes Responsivos

- **Navbar**: Menú hamburguesa en móvil, nav horizontal en desktop
- **Dashboard**: Sidebar colapsable en móvil
- **Formularios**: Ancho completo en móvil, ancho limitado en desktop
- **Imágenes**: `max-width: 100%` (escalan con contenedor)

---

## Ciclo de Vida de una Solicitud

### Request HTTP

```
1. Cliente envía GET/POST a URL
   ↓
2. Django Router (urls.py) busca coincidencia
   ↓
3. Middleware procesa request:
   - SecurityMiddleware (headers)
   - SessionMiddleware (sesión)
   - AuthenticationMiddleware (usuario)
   - CsrfViewMiddleware (tokens CSRF)
   ↓
4. Vista se ejecuta:
   - @login_required verifica autenticación
   - Accede a request.user
   - Interactúa con modelos (BD)
   - Prepara contexto
   ↓
5. Template Engine renderiza:
   - Lee template
   - Sustituye variables {{ variable }}
   - Ejecuta lógica {% if %}, {% for %}
   ↓
6. Middleware procesa response:
   - Agrega headers de seguridad
   ↓
7. Response HTML se envía al navegador
```

---

## Migraciones de Base de Datos

### Crear Migración
```bash
python manage.py makemigrations
# Detecta cambios en models.py
# Crea archivo de migración
```

### Aplicar Migración
```bash
python manage.py migrate
# Ejecuta migraciones
# Actualiza esquema BD
```

### Historial
```
0001_initial.py
├── Create User (Django built-in)
├── Create PasswordResetToken
└── Create indexes
```
---

## Referencias

### Django
- [Django Docs](https://docs.djangoproject.com/)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [Django ORM](https://docs.djangoproject.com/en/stable/topics/db/models/)

### Python
- [PEP 8 Style Guide](https://pep8.org/)
- [Python Docstrings](https://www.python.org/dev/peps/pep-0257/)

### Web
- [HTML Standards](https://html.spec.whatwg.org/)
- [CSS Specs](https://www.w3.org/Style/CSS/)
- [MDN Web Docs](https://developer.mozilla.org/)

---

**Documento generado**: Mayo 2026  
**Versión**: 1.0.0  
**Estado**: Completado
