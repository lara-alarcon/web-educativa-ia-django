/**
 * Funcionalidades JavaScript para página de autenticación (login/registro).
 * 
 * Este script maneja:
 * - Cambio de tabs entre formularios de login y registro
 * - Toggle de visibilidad de contraseñas (mostrar/ocultar)
 * - Cambio dinámico de estilos de botones
 */

document.addEventListener('DOMContentLoaded', function () {
  // ===== Elementos del DOM =====
  var tabs = document.querySelectorAll('[data-auth-mode]');
  var loginForm = document.getElementById('login-form');
  var registerForm = document.getElementById('register-form');
  var loginSubmit = document.getElementById('login-submit');
  var registerSubmit = document.getElementById('register-submit');

  /**
   * Cambia entre modo login y registro
   * @param {string} mode - 'login' o 'register'
   */
  function setMode(mode) {
    // Actualizar estado activo de los tabs
    tabs.forEach(function (tab) {
      if (tab.dataset.authMode === mode) {
        tab.classList.add('active');
      } else {
        tab.classList.remove('active');
      }
    });
    
    // Mostrar/ocultar formularios
    if (mode === 'register') {
      if (loginForm) loginForm.classList.add('hidden');
      if (registerForm) registerForm.classList.remove('hidden');
      
      // Cambiar estilos de botones
      if (loginSubmit) {
        loginSubmit.classList.remove('glow-green');
        loginSubmit.classList.remove('button-primary');
        loginSubmit.classList.add('button-secondary');
      }
      if (registerSubmit) {
        registerSubmit.classList.remove('button-secondary');
        registerSubmit.classList.add('button-primary', 'glow-green');
      }
    } else {
      if (loginForm) loginForm.classList.remove('hidden');
      if (registerForm) registerForm.classList.add('hidden');
      
      // Cambiar estilos de botones
      if (loginSubmit) {
        loginSubmit.classList.remove('button-secondary');
        loginSubmit.classList.add('button-primary', 'glow-green');
      }
      if (registerSubmit) {
        registerSubmit.classList.remove('glow-green');
        registerSubmit.classList.remove('button-primary');
        registerSubmit.classList.add('button-secondary');
      }
    }
  }

  // Agregar listeners a cada tab
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      setMode(tab.dataset.authMode);
    });
  });

  // Inicializar estilos: detectar formulario visible
  var initialMode = 'login';
  if (registerForm && !registerForm.classList.contains('hidden')) {
    initialMode = 'register';
  }
  if (loginForm && !loginForm.classList.contains('hidden')) {
    initialMode = 'login';
  }
  
  // Aplicar modo inicial
  setMode(initialMode);

  // ===== Toggle Visibilidad de Contraseñas =====
  document.querySelectorAll('.password-toggle').forEach(function (button) {
    button.addEventListener('click', function () {
      var target = document.querySelector(button.dataset.toggleTarget);
      if (!target) return;
      
      if (target.type === 'password') {
        target.type = 'text';
        button.textContent = '🙈';
      } else {
        target.type = 'password';
        button.textContent = '👁';
      }
    });
  });
});
