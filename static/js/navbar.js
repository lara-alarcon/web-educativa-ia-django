/**
 * Funcionalidades JavaScript para la navegación (navbar).
 * 
 * Este script maneja:
 * - Toggle del menú móvil (hamburguesa)
 * - Cerrar menú al hacer clic en un enlace
 * - Accesibilidad (atributos aria-expanded y aria-hidden)
 */

document.addEventListener('DOMContentLoaded', function () {
  // Elementos del navbar
  const button = document.getElementById('navbar-toggle');      // Botón hamburguesa
  const menu = document.getElementById('navbar-menu');          // Menú desplegable

  // Si alguno no existe, salir (página sin navbar)
  if (!button || !menu) {
    return;
  }

  /**
   * Toggle: Abre/cierra el menú móvil
   * También actualiza atributos de accesibilidad (a11y)
   */
  button.addEventListener('click', function () {
    // Alternar clase 'navbar-open' en el menú
    const isOpen = menu.classList.toggle('navbar-open');
    
    // Actualizar atributos ARIA para screen readers
    button.setAttribute('aria-expanded', String(isOpen));
    menu.setAttribute('aria-hidden', String(!isOpen));
  });

  /**
   * Cerrar menú: Cuando el usuario hace clic en un enlace del menú
   * El menú se cierra automáticamente
   */
  menu.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      // Remover clase de menú abierto
      menu.classList.remove('navbar-open');
      
      // Actualizar atributos de accesibilidad
      button.setAttribute('aria-expanded', 'false');
      menu.setAttribute('aria-hidden', 'true');
    });
  });
});
