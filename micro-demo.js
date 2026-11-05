/* Recorded-result illustration. No backend, analytics or persistence. */
(() => {
  const deck = document.querySelector('.deck');
  const scenes = [...deck.querySelectorAll('.scene')];
  const buttons = [...document.querySelectorAll('[data-scene]')];
  const play = document.querySelector('#play');
  const previous = document.querySelector('#previous');
  const next = document.querySelector('#next');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const labels = ['The request', 'Operator denied', 'Operator permitted', 'Evidence'];
  let current = 0, timer = null, playing = false;
  const stop = () => {
    clearTimeout(timer); playing = false;
    play.textContent = 'Play walkthrough'; play.setAttribute('aria-pressed', 'false');
  };
  const render = () => {
    scenes.forEach((scene, i) => { scene.hidden = i !== current; });
    buttons.forEach((button, i) => button.setAttribute('aria-current', String(i === current)));
    previous.disabled = current === 0; next.disabled = current === scenes.length - 1;
    document.querySelector('#scene-status').textContent = `Scene ${current + 1} of 4 · ${labels[current]}`;
    deck.classList.toggle('motion-enabled', !reduced.matches && !document.hidden);
  };
  const schedule = () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      if (!playing) return;
      if (current === scenes.length - 1) { stop(); return; }
      current += 1; render(); schedule();
    }, 7000);
  };
  const go = (index) => { stop(); current = index; render(); };
  buttons.forEach((button, i) => button.addEventListener('click', () => go(i)));
  previous.addEventListener('click', () => go(Math.max(0, current - 1)));
  next.addEventListener('click', () => go(Math.min(3, current + 1)));
  play.addEventListener('click', () => {
    if (playing) { stop(); deck.classList.remove('motion-enabled'); return; }
    if (reduced.matches) return;
    if (current === 3) current = 0;
    playing = true; render(); play.textContent = 'Pause walkthrough';
    play.setAttribute('aria-pressed', 'true'); schedule();
  });
  const preferences = () => { stop(); play.hidden = reduced.matches; render(); };
  reduced.addEventListener('change', preferences);
  document.addEventListener('visibilitychange', () => { if (document.hidden) { stop(); deck.classList.remove('motion-enabled'); } });
  if ('IntersectionObserver' in window) new IntersectionObserver(entries => {
    if (!entries[0].isIntersecting) { stop(); deck.classList.remove('motion-enabled'); }
  }).observe(deck);
  document.querySelector('.deck-controls').hidden = false;
  preferences();
})();
