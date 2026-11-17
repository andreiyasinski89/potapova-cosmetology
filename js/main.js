/* Інтерфейс: меню (десктоп і мобільне), «вгору», індикатор прокручування, поява блоків, відео, фільтр каталогу, слайдер «до/після». */
(() => {
  'use strict';
  const root = document.documentElement;
  root.classList.remove('no-js');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* ---------- шапка: стискається при прокрутці, ховається вниз, показується вгору ---------- */
  const hdr = $('header.site'), bar = $('.progress i'), toTop = $('.totop');
  let lastY = scrollY, ticking = false;
  function onScroll() {
    const y = scrollY, max = root.scrollHeight - innerHeight;
    if (hdr) {
      hdr.classList.toggle('compact', y > 80);
      hdr.classList.toggle('hide', y > lastY + 4 && y > 420 && !document.body.classList.contains('menu-open'));
      if (y < lastY - 4) hdr.classList.remove('hide');
    }
    if (bar) bar.style.transform = `scaleX(${max > 0 ? Math.min(1, y / max) : 0})`;
    if (toTop) toTop.hidden = y < 700;
    lastY = y; ticking = false;
  }
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  toTop && toTop.addEventListener('click', () => scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }));

  /* ---------- мобільне меню ---------- */
  const burger = $('.burger'), mnav = $('#mnav');
  function setMenu(open) {
    if (!burger || !mnav) return;
    mnav.hidden = !open;
    burger.setAttribute('aria-expanded', String(open));
    burger.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
    if (open) hdr && hdr.classList.remove('hide');
  }
  if (burger && mnav) {
    burger.addEventListener('click', () => setMenu(mnav.hidden));
    mnav.addEventListener('click', e => {
      const a = e.target.closest('a');
      if (a) { setMenu(false); return; }                     // після переходу меню прибирається
      const sub = e.target.closest('.msub');
      if (sub) {                                              // акордеон «Послуги» / «Про нас»
        const open = sub.getAttribute('aria-expanded') !== 'true';
        $$('.msub', mnav).forEach(b => b.setAttribute('aria-expanded', 'false'));
        sub.setAttribute('aria-expanded', String(open));
      }
    });
    addEventListener('keydown', e => { if (e.key === 'Escape' && !mnav.hidden) { setMenu(false); burger.focus(); } });
    addEventListener('resize', () => { if (innerWidth > 1000 && !mnav.hidden) setMenu(false); });
    addEventListener('pageshow', () => setMenu(false));       // повернення кнопкою «назад»
  }
  /* якір на цій самій сторінці теж закриває меню */
  addEventListener('hashchange', () => setMenu(false));

  /* ---------- поява блоків ---------- */
  const els = $$('.rv, .steps');
  if (reduce || !('IntersectionObserver' in window)) els.forEach(e => e.classList.add('in'));
  else {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { threshold: .12, rootMargin: '0px 0px -5% 0px' });
    els.forEach(e => io.observe(e));
  }

  /* ---------- фільтр каталогу послуг ---------- */
  $$('.chips').forEach(box => {
    const cards = $$('.scard', box.parentElement);
    const apply = f => {
      cards.forEach(c => { c.hidden = !(f === 'all' || c.dataset.cat === f); });
      $$('.chip', box).forEach(b => { const on = b.dataset.filter === f; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', String(on)); });
      try { history.replaceState(null, '', f === 'all' ? location.pathname : '#' + f); } catch (e) {}
    };
    box.addEventListener('click', e => { const b = e.target.closest('.chip'); if (b) apply(b.dataset.filter); });
    const h = location.hash.slice(1);
    if (h && $(`.chip[data-filter="${h}"]`, box)) apply(h); else apply('all');
  });

  /* ---------- слайдер «до/після» ---------- */
  $$('.ba').forEach(ba => {
    const r = $('input', ba), set = () => ba.style.setProperty('--pos', r.value + '%');
    r.addEventListener('input', set); set();
  });

  /* ---------- відео: hero зупиняється при reduced-motion, решта грає лише у видимій зоні ---------- */
  const vids = $$('video');
  if (reduce) vids.forEach(v => { v.removeAttribute('autoplay'); v.pause(); v.preload = 'none'; });
  else if ('IntersectionObserver' in window) {
    const vo = new IntersectionObserver(es => es.forEach(e => {
      const v = e.target; if (v.dataset.lazy === undefined) return;
      if (e.isIntersecting) v.play().catch(() => {}); else v.pause();
    }), { threshold: .35 });
    vids.forEach(v => vo.observe(v));
  }

  /* ---------- лічильники (необов'язково: [data-count]) ---------- */
  const counters = $$('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    const co = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return; co.unobserve(e.target);
      const end = parseFloat(e.target.dataset.count), suf = e.target.dataset.suffix || '', t0 = performance.now(), dur = reduce ? 1 : 1400;
      (function tick(t) { const p = Math.min(1, (t - t0) / dur); e.target.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))).toLocaleString('uk') + suf; if (p < 1) requestAnimationFrame(tick); })(t0);
    }), { threshold: .4 });
    counters.forEach(c => co.observe(c));
  }
})();
