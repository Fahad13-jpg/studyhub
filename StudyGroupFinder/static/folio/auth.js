(() => {
  document.querySelectorAll('.auth-field.has-error input').forEach(input => input.setAttribute('aria-invalid', 'true'));
  document.querySelectorAll('.password-toggle').forEach(button => {
    const input = document.getElementById(button.getAttribute('aria-controls'));
    if (!input) return;
    button.hidden = false;
    input.setAttribute('data-password', 'true');
    const original = button.getAttribute('aria-label').replace(/^Show /, '');
    button.addEventListener('click', () => {
      const show = input.type === 'password';
      input.type = show ? 'text' : 'password';
      button.setAttribute('aria-pressed', String(show));
      button.setAttribute('aria-label', `${show ? 'Hide' : 'Show'} ${original}`);
    });
    const caps = input.closest('.auth-field').querySelector('.caps-warning');
    input.addEventListener('keyup', event => { if (caps) caps.hidden = !event.getModifierState('CapsLock'); });
    input.addEventListener('blur', () => { if (caps) caps.hidden = true; });
  });
  document.querySelectorAll('.auth-form').forEach(form => {
    const button = form.querySelector('.auth-submit');
    const label = button?.querySelector('.submit-label');
    if (!button || !label) return;
    const original = label.textContent;
    form.addEventListener('submit', event => {
      if (event.defaultPrevented || !form.checkValidity()) return;
      button.disabled = true;
      button.setAttribute('aria-busy', 'true');
      label.textContent = form.dataset.busyLabel || original;
    });
    window.addEventListener('pageshow', () => {
      button.disabled = false; button.removeAttribute('aria-busy'); label.textContent = original;
    });
  });
})();
