(() => {
  const root = document.documentElement;
  root.classList.remove('no-js');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const safe = (fn) => { try { return fn(); } catch (e) { return null; } };

  // Sticky header: стискається та ховається при скролі вниз
  const hdr = document.querySelector('header.site');
  let lastY = scrollY;
  addEventListener('scroll', () => {
    const y = scrollY;
    hdr.classList.toggle('compact', y > 80);
    hdr.classList.toggle('hide', y > lastY && y > 400);
    lastY = y;
  }, { passive: true });

  // Burger
  const burger = document.querySelector('.burger'), nav = document.querySelector('.nav');
  burger && burger.addEventListener('click', () => {
    const o = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', o);
  });

  // Reveal
  const els = document.querySelectorAll('.rv, .steps');
  if (reduce || !('IntersectionObserver' in window)) els.forEach(e => e.classList.add('in'));
  else {
    const io = new IntersectionObserver((es) => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { threshold: .15, rootMargin: '0px 0px -6% 0px' });
    els.forEach(e => io.observe(e));
  }

  // Before/after (drag + клавіатура через input[type=range])
  document.querySelectorAll('.ba').forEach(ba => {
    const r = ba.querySelector('input');
    const set = () => ba.style.setProperty('--pos', r.value + '%');
    r.addEventListener('input', set); set();
  });

  // Відео: hero зупиняється при reduced-motion, решта грає лише у видимій зоні
  const vids = document.querySelectorAll('video');
  if (reduce) vids.forEach(v => { v.removeAttribute('autoplay'); v.pause(); v.preload = 'none'; });
  else if ('IntersectionObserver' in window) {
    const vo = new IntersectionObserver((es) => es.forEach(e => {
      const v = e.target; if (v.dataset.lazy === undefined) return;
      if (e.isIntersecting) { v.play().catch(() => {}); } else { v.pause(); }
    }), { threshold: .35 });
    vids.forEach(v => vo.observe(v));
  }
})();
