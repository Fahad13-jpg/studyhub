/* Small progressive enhancements. Core navigation and forms work without this file. */
(() => {
  const links = document.querySelectorAll('.folio-nav a.nav-link');
  for (const link of links) {
    if (new URL(link.href).pathname === location.pathname) link.setAttribute('aria-current', 'page');
  }
  // Bootstrap ships deferred. Templates may initialize it on DOMContentLoaded.
  const badge = document.getElementById('notificationBadge');
  if (!badge) return;
  let timer;
  let pending = false;
  async function updateCount() {
    if (document.hidden || pending) return;
    pending = true;
    try {
      const response = await fetch('/notifications/api/unread-count/', {headers: {'Accept': 'application/json'}});
      if (!response.ok) return;
      const data = await response.json();
      const count = Math.max(0, Number(data.count) || 0);
      badge.textContent = count > 99 ? '99+' : String(count);
      badge.hidden = count === 0;
    } catch (_) { /* Keep the last known count when offline. */ }
    finally { pending = false; }
  }
  function schedule() {
    clearInterval(timer);
    if (!document.hidden) {
      updateCount();
      timer = setInterval(updateCount, 60000);
    }
  }
  document.addEventListener('visibilitychange', schedule);
  window.addEventListener('pagehide', () => clearInterval(timer));
  schedule();
})();
