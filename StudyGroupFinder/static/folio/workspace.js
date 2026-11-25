(() => {
  if (!document.body.classList.contains('workspace-page')) return;
  function avatarFallback(image) {
    if (!image.isConnected) return;
    const fallback = document.createElement('span');
    const name = image.alt.trim() || 'Student';
    const size = Math.max(32, Math.min(160, image.width || 40));
    fallback.className = 'avatar-fallback';
    fallback.setAttribute('role', 'img');
    fallback.setAttribute('aria-label', name);
    fallback.textContent = name.split(/\s+/).slice(0, 2).map(word => word[0]).join('').toUpperCase();
    fallback.style.width = `${size}px`; fallback.style.height = `${size}px`;
    fallback.style.fontSize = `${Math.min(40, Math.max(14, Math.round(size * 0.32)))}px`;
    image.replaceWith(fallback);
  }
  document.addEventListener('error', event => { if (event.target instanceof HTMLImageElement) avatarFallback(event.target); }, true);
  document.querySelectorAll('img').forEach(image => { if (image.complete && !image.naturalWidth) avatarFallback(image); });
  document.querySelectorAll('.workspace-field').forEach(field => {
    const control = field.querySelector('input, select, textarea');
    if (!control) return;
    const help = field.querySelector('.form-text');
    const error = field.querySelector('.field-feedback');
    const ids = [];
    if (help) { help.id = `${control.id}_help`; ids.push(help.id); }
    if (error) { error.id = `${control.id}_errors`; ids.push(error.id); control.setAttribute('aria-invalid', 'true'); }
    if (ids.length) control.setAttribute('aria-describedby', ids.join(' '));
  });
  document.querySelectorAll('.workspace-form, .preferences-form').forEach(form => {
    const button = form.querySelector('button[type=submit]');
    if (!button) return;
    const original = button.textContent;
    form.addEventListener('submit', event => {
      if (event.defaultPrevented || !form.checkValidity()) return;
      button.disabled = true; button.setAttribute('aria-busy', 'true'); button.textContent = 'Saving…';
    });
    window.addEventListener('pageshow', () => {button.disabled = false;button.removeAttribute('aria-busy');button.textContent = original;});
  });
})();
