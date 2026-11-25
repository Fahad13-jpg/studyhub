(() => {
  const carousel = document.querySelector('.study-carousel');
  if (!carousel) return;
  const slides = [...carousel.querySelectorAll('.hero-slide')];
  const dots = [...carousel.querySelectorAll('[data-slide]')];
  const pause = carousel.querySelector('.slider-pause');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const captions = ['A shared table', 'A quieter corner', 'A fresh perspective', 'A plan for what’s next'];
  let current = 0;
  let timer;
  let rotates = !reduced.matches;
  let hovered = false;
  let inView = true;
  let selection = 0;
  let pauseIntent = null;
  function schedule() {
    clearTimeout(timer);
    pause.setAttribute('aria-label', rotates ? 'Pause image rotation' : 'Start image rotation');
    pause.classList.toggle('is-paused', !rotates);
    if (rotates && !hovered && inView && !document.hidden) {
      timer = setTimeout(() => show(current + 1, false), 6500);
    }
  }
  async function show(index, manual = true) {
    if (manual) rotates = false;
    clearTimeout(timer);
    const next = (index + slides.length) % slides.length;
    const request = ++selection;
    const image = slides[next].querySelector('img');
    try { await image.decode(); } catch (_) {
      if (!image.complete || !image.naturalWidth) { schedule(); return; }
    }
    if (request !== selection) return;
    current = next;
    slides.forEach((slide, i) => {
      slide.classList.toggle('is-active', i === current);
      slide.setAttribute('aria-hidden', String(i !== current));
      dots[i].setAttribute('aria-pressed', String(i === current));
    });
    carousel.querySelector('#slide-number').textContent = String(current + 1).padStart(2, '0');
    carousel.querySelector('#scene-caption').textContent = captions[current];
    if (manual) carousel.querySelector('#slider-status').textContent = `Image ${current + 1} of ${slides.length}: ${captions[current]}`;
    schedule();
  }
  carousel.querySelector('.slider-prev').addEventListener('click', () => show(current - 1));
  carousel.querySelector('.slider-next').addEventListener('click', () => show(current + 1));
  dots.forEach(dot => dot.addEventListener('click', () => show(Number(dot.dataset.slide))));
  pause.addEventListener('pointerdown', () => { pauseIntent = !rotates; });
  pause.addEventListener('click', () => { rotates = pauseIntent ?? !rotates; pauseIntent = null; schedule(); });
  carousel.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault(); show(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  carousel.addEventListener('focusin', () => { rotates = false; schedule(); });
  carousel.addEventListener('pointerenter', event => { if (event.pointerType === 'mouse') { hovered = true; schedule(); } });
  carousel.addEventListener('pointerleave', () => { hovered = false; schedule(); });
  document.addEventListener('visibilitychange', schedule);
  reduced.addEventListener('change', () => { if (reduced.matches) rotates = false; schedule(); });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => { inView = entries[0].isIntersecting; schedule(); }, {threshold: 0.2}).observe(carousel);
  }
  window.addEventListener('pagehide', () => clearTimeout(timer));
  window.addEventListener('pageshow', schedule);
  schedule();
})();
