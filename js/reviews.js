/* Опубліковані відгуки для каруселі на головній.
   Власник ставить позначку «Опубліковано» у Google Таблиці; Apps Script (doGet ?action=reviews) віддає такі рядки як JSON.
   Поки опублікованих відгуків немає (або запит не вдався), залишаються картки-заглушки зі сторінки.
   Щойно з'являється хоча б один справжній відгук, показуються ТІЛЬКИ справжні. */
(function () {
  'use strict';
  var track = document.getElementById('revTrack'), tpl = track && track.querySelector('figure');
  var url = window.SITE && window.SITE.reviews && window.SITE.reviews.url;
  if (!track || !tpl || !url) return;
  var LANG = (document.documentElement.lang || 'uk').slice(0, 2), CACHE = 'pcReviews', TTL = 5 * 60 * 1000, MAX = 24;

  function esc(s) { var d = document.createElement('div'); d.textContent = s; return d; }
  function parts(full) {
    var p = String(full || '').trim().split(/\s+/).filter(Boolean), first = p[0] || '';
    return { short: p.length > 1 ? first + ' ' + p[1].charAt(0).toUpperCase() + '.' : first, ini: (first.charAt(0) + (p[1] ? p[1].charAt(0) : '')).toUpperCase() };
  }
  function card(r) {
    var f = tpl.cloneNode(true), n = Math.max(1, Math.min(5, Math.round(Number(r.rating) || 5)));
    f.querySelector('.stars').textContent = '★★★★★'.slice(0, n) + '☆☆☆☆☆'.slice(0, 5 - n);
    f.querySelector('.stars').setAttribute('aria-label', n + ' / 5');
    var q = f.querySelector('blockquote'); q.className = ''; q.textContent = '«' + String(r.text) + '»'; if (r.lang) q.setAttribute('lang', r.lang);
    var nm = parts(r.name), sp = f.querySelectorAll('figcaption span');
    sp[0].textContent = nm.ini; sp[2].textContent = nm.short; sp[3].textContent = r.city || '';
    return f;
  }
  function use(d) {
    var list = (d && Array.isArray(d.reviews) ? d.reviews : []).filter(function (r) { return r && String(r.text || '').trim().length >= 10 && String(r.name || '').trim(); });
    if (!list.length) return;
    list.sort(function (a, b) { return (b.lang === LANG) - (a.lang === LANG); });
    track.innerHTML = ''; list.slice(0, MAX).forEach(function (r) { track.appendChild(card(r)); });
  }
  try { var c = JSON.parse(sessionStorage.getItem(CACHE)); if (c && Date.now() - c.t < TTL) { use(c.d); return; } } catch (e) {}
  var ctl = window.AbortController ? new AbortController() : null, timer = setTimeout(function () { if (ctl) ctl.abort(); }, 7000);
  fetch(url + (url.indexOf('?') < 0 ? '?' : '&') + 'action=reviews', ctl ? { signal: ctl.signal } : {})
    .then(function (r) { return r.json(); })
    .then(function (d) { clearTimeout(timer); try { sessionStorage.setItem(CACHE, JSON.stringify({ t: Date.now(), d: d })); } catch (e) {} use(d); })
    .catch(function () { clearTimeout(timer); });
})();
