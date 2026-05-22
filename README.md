# IA.edu — Plataforma Educativa sobre Inteligencia Artificial (Parte 2: Django Full-Stack)

Este repositorio contiene el desarrollo definitivo, funcional y auto-hospedado de **IA.edu**. Representa la **fase de producción y backend**, donde se tomó el prototipo estático de alta fidelidad diseñado inicialmente con herramientas No-Code de IA (v0 de Vercel) y se migró de manera nativa al stack **Django/Python Full-Stack** para superar las limitaciones de flexibilidad y personalización del software sin código.

*Nota: Para ver la fase de diseño inicial, la ingeniería de prompts arquitectónicos y la simulación estática del cliente, visite la [PARTE 1: Prototipado No-Code con IA](https://github.com/lara-alarcon/prototipo-pagina-web-django-v0).*

---


## Descripción General

**IA.edu** es una plataforma educativa web desarrollada con **Django** que enseña conceptos fundamentales sobre Inteligencia Artificial, redes neuronales y los pioneros en el campo.

La aplicación incluye:
- Sistema de autenticación de usuarios (registro, login)
- Recuperación segura de contraseñas con tokens
- Dashboard educativo con 4 módulos de contenido
- Tema claro/oscuro (dark mode)
- Interfaz responsive (móvil y escritorio)

---

## Arquitectura y Tecnologías (Patrón MVT)

Para garantizar una experiencia segura y escalable, la aplicación fue estructurada utilizando el patrón **Modelo-Vista-Plantilla (MVT)** de Django:

### 1. Persistencia de Datos (Modelos)
El archivo `models.py` gestiona la estructura de la base de datos de manera dinámica:
* **User Model (Nativo):** Administra las credenciales.
* **PasswordResetToken:** Modelo personalizado que almacena tokens únicos y controla los tiempos de expiración para el restablecimiento de contraseñas de forma segura.

### 2. Lógica de Control y Seguridad (Vistas)
Las peticiones del cliente son procesadas de forma estricta en `views.py`:
* **Control de Acceso:** Uso exhaustivo del decorador `@login_required` para bloquear el acceso al Dashboard a usuarios no autenticados.

### 3. Motor de Renderizado Dinámico (Plantillas)
La interfaz visual estructurada originalmente con Tailwind CSS fue fragmentada en bloques heredables de Django para evitar la duplicación de código:
* `base.html`: Esqueleto global que unifica las tipografías (Geist), barras de navegación y pies de página heredables.
* `login.html`: Contenedor seguro con alternancia dinámica mediante JavaScript vanilla para Login y Registro en una misma vista.
* `dashboard/`: Subcarpeta modularizada que utiliza bucles e iteradores de Django para renderizar los 4 bloques temáticos.

---

## Estructura del Proyecto

```
v0/
├── manage.py                    # Utilidad de gestión de Django
├── requirements.txt             # Dependencias Python
├── db.sqlite3                  # Base de datos (desarrollo)
│
├── iaedu/                      # Paquete principal del proyecto
│   ├── __init__.py
│   ├── settings.py             # Configuración de Django (BD, apps, emails, etc.)
│   ├── urls.py                 # Enrutamiento principal
│   ├── wsgi.py                 # Punto de entrada WSGI (producción)
│
├── web/                        # Aplicación principal de Django
│   ├── __init__.py
│   ├── apps.py                 # Configuración de la app
│   ├── models.py               # Modelos de BD (PasswordResetToken)
│   ├── views.py                # Vistas/Controladores
│   ├── forms.py                # Formularios de validación
│   ├── urls.py                 # URLs de la app
│   ├── admin.py                # Configuración del panel admin
│   ├── migrations/             # Migraciones de BD
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│
├── templates/                  # Templates HTML
│   ├── base.html               # Template base (herencia)
│   ├── home.html               # Página de inicio
│   ├── login.html              # Login y registro
│   ├── password_reset_request.html    # Solicitar recuperación
│   ├── password_reset_confirm.html    # Cambiar contraseña
│   ├── includes/
│   │   ├── navbar.html         # Barra de navegación
│   │   └── footer.html         # Pie de página
│   └── dashboard/              # Templates del dashboard
│       ├── base.html           # Layout del dashboard
│       ├── index.html          # Módulo 1: Definición de IA
│       ├── redes_neuronales.html
│       ├── tipos_de_redes.html
│       └── autores.html        # Módulo 4: Pioneros
│
├── static/                     # Archivos estáticos
│   ├── css/
│   │   └── styles.css          # Estilos principales (variables CSS, temas)
│   ├── js/
│   │   ├── auth.js             # Funcionalidades de login/registro
│   │   ├── navbar.js           # Menú responsivo
│   │   └── dashboard.js        # Toggle de tema y sidebar
│   └── img/                    # Imágenes
│
└── public/                     # Activos públicos adicionales
```

---

## Inicio Rápido

### 1. Requisitos
- Python 3.10+
- pip (gestor de paquetes)

### 2. Instalación

```bash
# Clonar o descargar el proyecto
cd v0

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones a la base de datos
python manage.py migrate

# Crear usuario administrador
python manage.py createsuperuser

# Iniciar servidor de desarrollo
python manage.py runserver
```

Acceder a:
- Sitio: http://localhost:8000
---

## Autenticación

### Registro
1. Click en "Registrarse" en la página de inicio
2. Ingresar nombre, email y contraseña (mínimo 6 caracteres)
3. Se crea la cuenta automáticamente

### Login
1. Ingresar email y contraseña
2. Opcionalmente marcar "Recordarme" para sesión persistente
3. Se redirige al dashboard

### Recuperación de Contraseña
1. Click en "¿Olvidaste tu contraseña?" en login
2. Ingresar email registrado
3. Se envía enlace seguro por email (en desarrollo aparece en consola)
4. Click en enlace para cambiar contraseña
5. **Nota**: El token expira en 24 horas

---

## Módulos Educativos (Dashboard)

Después de iniciar sesión, el usuario accede a 4 módulos educativos:

### 1. Definición de Inteligencia Artificial
- Concepto de IA
- Perspectivas de pioneros (Turing, McCarthy, Minsky)
- Diferencias entre IA débil y fuerte

### 2. Redes Neuronales Artificiales
- Estructura y funcionamiento
- Analogía biológica vs artificial
- Proceso de aprendizaje
- Retropropagación (backpropagation)

### 3. Tipos de Redes Neuronales
- FNN (Feedforward Neural Networks)
- CNN (Convolutional Neural Networks)
- RNN (Recurrent Neural Networks)
- GAN (Generative Adversarial Networks)

### 4. Autores y Pioneros
- Geoffrey Hinton
- Yann LeCun
- Yoshua Bengio
- Otras contribuciones históricas

---

## Características Técnicas

### Backend (Django)
| Característica | Detalles |
|---|---|
| **Framework** | Django 4.2+ |
| **Base de Datos** | SQLite |
| **Autenticación** | Django User model + tokens personalizados |
| **Formularios** | Validación personalizada con Django Forms |
| **Email** | Console backend (desarrollo), SMTP (producción) |

### Frontend
| Característica | Detalles |
|---|---|
| **Tipografía** | Geist (sans-serif), Geist Mono |
| **Colores** | Sistema OKLCH (mejor perceptibilidad) |
| **Temas** | Claro y Oscuro (localStorage) |
| **Iconos** | Lucide icons |
| **Responsividad** | Mobile-first design |

### JavaScript
- Cambio de tabs (Login/Registro)
- Toggle de visibilidad de contraseñas
- Menú hamburguesa responsivo
- Toggle de tema oscuro (persistente)
- Sin dependencias externas (vanilla JS)

---

## Variables CSS Principales

### Colores de Marca
```css
--primary: oklch(0.72 0.22 150);  /* Verde cian */
--primary-foreground: oklch(0.985 0 0);  /* Blanco */
```

### Temas
- **Tema Claro**: Fondo blanco, texto oscuro
- **Tema Oscuro**: Fondo negro, texto blanco (automático)

La preferencia se guarda en `localStorage.dashboardTheme`

---

## Rutas principales

```
GET  /                                  # Página inicio
GET  /login/?mode=login                # Login
GET  /login/?mode=register              # Registro
POST /login/                            # Enviar login/registro
GET  /logout/                           # Cerrar sesión
GET  /password-reset/                   # Solicitar recuperación
POST /password-reset/                   # Enviar email recuperación
GET  /password-reset/<token>/           # Cambiar contraseña
POST /password-reset/<token>/           # Guardar nueva contraseña
GET  /admin/                            # Panel administrativo
GET  /dashboard/                        # Inicio dashboard (requiere login)
GET  /dashboard/tipos-de-redes/
GET  /dashboard/redes-neuronales/
GET  /dashboard/autores/
```

---

## Modelos de Base de Datos

### PasswordResetToken
```python
user              → OneToOneField(User)  # Usuario que solicita recuperación
token             → CharField(unique)     # Token criptográfico
created_at        → DateTimeField(auto)   # Fecha creación (automática)
expires_at        → DateTimeField()       # Fecha expiración (24h)
is_valid()        → Method               # Verifica si no expiró
```

---

## Dependencias

Ver `requirements.txt`:
```
Django>=4.2,<5.0
```

**Otras librerías usadas** (CDN/Frontend):
- Lucide Icons (CDN)
- Geist Font (importada en CSS)

---

## Documentación de Código

Cada archivo Python tiene:
- Docstring del módulo (qué hace)
- Docstrings de clases (propósito)
- Docstrings de funciones (parámetros, retorno)
- Comentarios de líneas importantes

Cada archivo JavaScript tiene:
- Comentarios de bloques funcionales
- Explicación de listeners
- Propósito de cada función

CSS tiene:
- Comentarios de secciones (colores, tipografía, etc.)
- Explicación de variables
- Separación por temas (claro/oscuro)

---

## Licencia

Este proyecto es de código educativo. Desarrollado como parte de **Práctica Profesionalizante 1** en ESIM - 2026.

**Autor**: Alarcón, Lara

---

## Soporte

Para reportar bugs o solicitar features, abrir un issue en el repositorio.

---

**Última actualización**: Mayo 2026  
**Versión**: 1.0.0  
**Estado**: Producción
