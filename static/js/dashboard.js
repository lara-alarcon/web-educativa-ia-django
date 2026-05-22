/**
 * Funcionalidades JavaScript para el dashboard.
 * 
 * Este script maneja:
 * - Toggle de la barra lateral (sidebar) en versión móvil
 * - Toggle entre tema claro y oscuro (light/dark mode)
 * - Persistencia de preferencia de tema en localStorage
 * - Actualización de íconos de tema usando biblioteca Lucide
 */

document.addEventListener('DOMContentLoaded', function () {
  // Elementos del dashboard
  var toggle = document.getElementById('sidebar-toggle');    // Botón para abrir/cerrar sidebar
  var sidebar = document.getElementById('dashboard-sidebar'); // Barra lateral
  var themeToggle = document.getElementById('theme-toggle');  // Botón cambiar tema

  // ===== Toggle Sidebar (Menú móvil) =====
  if (toggle && sidebar) {
    toggle.addEventListener('click', function () {
      // Alternar clase que muestra/oculta la barra lateral
      sidebar.classList.toggle('sidebar-open');
    });
  }

  // ===== Tema Claro/Oscuro (Dark Mode) =====
  
  /**
   * Actualiza el ícono del botón de tema según el tema actual
   * - Tema oscuro: Muestra ícono de sol (para cambiar a claro)
   * - Tema claro: Muestra ícono de luna (para cambiar a oscuro)
   */
  function updateThemeButton() {
    if (!themeToggle) return;
    
    // Verificar si el tema oscuro está activo
    var isDark = document.body.classList.contains('dark');
    
    // Elegir ícono según el tema (opuesto al tema actual)
    var iconName = isDark ? 'sun' : 'moon';
    
    // Actualizar HTML del botón con el ícono de Lucide
    themeToggle.innerHTML = '<i data-lucide="' + iconName + '"></i>';
    
    // Texto alternativo para accesibilidad
    themeToggle.setAttribute('aria-label', isDark ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro');
    
    // Actualizar íconos de Lucide en el documento
    if (window.lucide && typeof lucide.createIcons === 'function') {
      lucide.createIcons();
    }
  }

  // Aplicar tema guardado o tema por defecto
  if (themeToggle) {
    // Obtener preferencia de tema guardada en navegador
    var storedTheme = localStorage.getItem('dashboardTheme');
    
    // Si no hay tema guardado, usar 'dark' por defecto
    if (storedTheme === null) {
      storedTheme = 'dark';
      localStorage.setItem('dashboardTheme', 'dark');
    }
    
    // Aplicar tema oscuro si está guardado como 'dark'
    if (storedTheme === 'dark') {
      document.body.classList.add('dark');
    }
    
    // Actualizar botón con el ícono correcto
    updateThemeButton();

    /**
     * Listener para cambiar tema
     * Alterna entre claro y oscuro y guarda en localStorage
     */
    themeToggle.addEventListener('click', function () {
      // Alternar clase 'dark' en el cuerpo del documento
      document.body.classList.toggle('dark');
      
      // Guardar preferencia de tema en localStorage (persiste entre sesiones)
      localStorage.setItem(
        'dashboardTheme',
        document.body.classList.contains('dark') ? 'dark' : 'light'
      );
      
      // Actualizar ícono del botón
      updateThemeButton();
    });
  }
});
