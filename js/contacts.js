/* Контакти та чати: підставляє посилання з js/config.js у всі елементи [data-contact],
   будує плаваючу кнопку «Написати», підказує мову за мовою браузера.
   Якщо канал не вказаний у config.js, його посилання ховається автоматично. */
(function () {
  'use strict';
  var C = (window.SITE && window.SITE.contacts) || {};
  var LANG = (document.documentElement.lang || 'uk').slice(0, 2);
  var T = function (uk, ru) { return LANG === 'ru' ? ru : uk; };
  var digits = function (v) { return String(v || '').replace(/\D/g, ''); };
  var pretty = function (v) { var d = digits(v); return /^380\d{9}$/.test(d) ? '+380 ' + d.slice(3, 5) + ' ' + d.slice(5, 8) + ' ' + d.slice(8, 10) + ' ' + d.slice(10) : String(v || ''); };
  var handle = function (v) { return String(v || '').trim().replace(/^@/, '').replace(/^https?:\/\/(t\.me|instagram\.com)\//, '').replace(/\/$/, ''); };

  function message(extra) {
    var m = (window.SITE.messages && (window.SITE.messages[LANG] || window.SITE.messages.uk)) || '';
    return extra ? m + ' ' + extra : m;
  }

  /* Одна точка, де з даних config.js робиться посилання на кожен канал */
  var CHANNEL = {
    phone:     function () { return C.phone ? 'tel:+' + digits(C.phone) : ''; },
    email:     function () { return C.email ? 'mailto:' + C.email : ''; },
    telegram:  function () { var h = handle(C.telegram); return h ? 'https://t.me/' + h : ''; },
    whatsapp:  function (x) { var d = digits(C.whatsapp); return d ? 'https://wa.me/' + d + '?text=' + encodeURIComponent(message(x)) : ''; },
    viber:     function () { var d = digits(C.viber); return d ? 'viber://chat?number=%2B' + d : ''; },
    instagram: function () { var h = handle(C.instagram); return h ? 'https://ig.me/m/' + h : ''; },
    facebook:  function () { return C.facebook || ''; },
    tiktok:    function () { return C.tiktok || ''; },
    map:       function () { return C.mapUrl || (C.address ? 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(C.address) : ''); }
  };
  var LABEL = { telegram: 'Telegram', whatsapp: 'WhatsApp', viber: 'Viber', instagram: 'Instagram', phone: T('Зателефонувати', 'Позвонить') };
  var ICON = {
    telegram: '<path d="M21.5 3.5 2.8 10.7c-.9.4-.9 1.1-.2 1.3l4.8 1.5 1.8 5.6c.2.6.4.8.9.8.4 0 .6-.2.9-.5l2.3-2.2 4.7 3.5c.9.5 1.5.2 1.7-.8l3.1-14.8c.3-1.2-.5-1.8-1.5-1.5Z" fill="currentColor"/>',
    whatsapp: '<path d="M3 21l1.6-4.8A9 9 0 1 1 8 19.5Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 8.5c0 3.5 3 6.5 6.5 6.5l1-1.5-2-1-1 .8c-1-.4-2-1.4-2.4-2.4l.8-1-1-2Z" fill="currentColor"/>',
    viber: '<path d="M12 3c-5 0-8 2.5-8 7.3 0 3 1 5 3 6.2V21l3.3-2.5c.6.1 1.2.1 1.7.1 5 0 8-2.5 8-7.3S17 3 12 3Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
    instagram: '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.3" cy="6.7" r="1.2" fill="currentColor"/>',
    phone: '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>'
  };

  /* 1. Заповнити всі [data-contact] */
  var configured = {};
  document.querySelectorAll('[data-contact]').forEach(function (a) {
    var ch = a.getAttribute('data-contact'), fn = CHANNEL[ch], href = fn ? fn(a.getAttribute('data-msg')) : '';
    var li = a.parentElement && a.parentElement.tagName === 'LI' ? a.parentElement : null;
    if (!href) { a.hidden = true; if (li) li.hidden = true; return; }
    if (li) li.hidden = false;
    configured[ch] = true;
    a.href = href; a.hidden = false;
    if (/^https?:/.test(href) && ch !== 'map') { a.target = '_blank'; a.rel = 'noopener noreferrer'; }
    var t = a.getAttribute('data-contact-text');
    if (t === 'phone') a.textContent = pretty(C.phone);
    else if (t === 'email') a.textContent = C.email;
    else if (t === 'address') a.textContent = (LANG === 'ru' && C.addressRu) || C.address || '';
  });
  document.querySelectorAll('[data-contact-fallback]').forEach(function (el) { if (configured.map) el.hidden = true; });
  var any = Object.keys(configured).some(function (k) { return k !== 'map'; });
  document.querySelectorAll('[data-contact-empty]').forEach(function (el) { if (any) el.hidden = true; });
  document.querySelectorAll('[data-fill="hours"]').forEach(function (el) { if (C.hours) { el.textContent = C.hours; el.classList.remove('fill'); } });
  window.SITE_CONFIGURED = configured;

  /* 2. Плаваюча кнопка «Написати» з меню каналів */
  var order = (window.SITE.chatOrder || []).filter(function (c) { return CHANNEL[c] && CHANNEL[c](); });
  function openPanel(open) {
    var p = document.getElementById('chatPanel'), b = document.getElementById('chatBtn');
    if (!p) return;
    p.hidden = !open; b.setAttribute('aria-expanded', String(open));
    if (open) p.querySelector('a').focus();
  }
  if (order.length) {
    var box = document.createElement('div'); box.className = 'chat';
    var items = order.map(function (c) {
      return '<li><a href="' + CHANNEL[c]() + '"' + (c === 'phone' ? '' : ' target="_blank" rel="noopener noreferrer"') + ' data-chat="' + c + '"><svg viewBox="0 0 24 24" aria-hidden="true">' + ICON[c] + '</svg>' + LABEL[c] + '</a></li>';
    }).join('');
    box.innerHTML = '<div id="chatPanel" class="chat-panel" role="dialog" aria-label="' + T('Написати нам', 'Написать нам') + '" hidden><p>' + T('Відповідаємо у зручному для вас месенджері', 'Отвечаем в удобном для вас мессенджере') + '</p><ul>' + items + '</ul></div>' +
      '<button id="chatBtn" class="chat-btn" type="button" aria-expanded="false" aria-controls="chatPanel" data-chat-open><span class="chat-pulse"></span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v11H9l-5 4Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg><span class="chat-label">' + T('Написати', 'Написать') + '</span></button>';
    document.body.appendChild(box);
    document.getElementById('chatBtn').addEventListener('click', function () { openPanel(document.getElementById('chatPanel').hidden); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') openPanel(false); });
    document.addEventListener('click', function (e) { if (!e.target.closest('.chat') && !e.target.closest('.mbar')) openPanel(false); });
  }
  /* «Написати» на мобільній панелі відкриває те саме меню; якщо каналів немає — веде до форми */
  document.querySelectorAll('.mbar [data-chat-open]').forEach(function (b) {
    b.addEventListener('click', function () {
      if (!order.length) { location.href = (document.querySelector('.fab') || {}).href || '#zapys'; return; }
      openPanel(document.getElementById('chatPanel').hidden);
    });
  });

  /* 3. Підказка мови за мовою браузера: один раз, без нав'язування */
  (function langSuggest() {
    if (!window.SITE.langSuggest) return;
    var KEY = 'pcLang';
    function store(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
    try { if (localStorage.getItem(KEY)) return; } catch (e) {}
    if (/bot|crawl|spider|slurp|lighthouse/i.test(navigator.userAgent || '')) return;
    var list = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ''];
    var target = null;
    for (var i = 0; i < list.length; i++) { var p = String(list[i]).toLowerCase().slice(0, 2); if (p === 'uk' || p === 'ru') { target = p; break; } }
    document.querySelectorAll('[data-lang]').forEach(function (a) {
      a.addEventListener('click', function () { store(a.getAttribute('data-lang')); });
    });
    if (!target || target === LANG) { if (target) store(LANG); return; }
    var link = document.querySelector('a[data-lang="' + target + '"]');
    if (!link) return;
    var S = { uk: ['Переглянути сайт українською?', 'Перейти на українську', 'Залишитися тут'], ru: ['Открыть сайт на русском?', 'Перейти на русский', 'Остаться здесь'] }[target];
    setTimeout(function () {
      var box = document.createElement('div'); box.className = 'langbox'; box.setAttribute('role', 'region'); box.setAttribute('lang', target);
      box.innerHTML = '<p>' + S[0] + '</p><div><a class="btn btn-primary" data-lang-go href="' + link.getAttribute('href') + '" hreflang="' + target + '">' + S[1] + '</a><button class="btn btn-ghost" type="button" data-lang-stay>' + S[2] + '</button></div>';
      document.body.appendChild(box);
      box.querySelector('[data-lang-go]').addEventListener('click', function () { store(target); });
      var stay = function () { store(LANG); box.remove(); };
      box.querySelector('[data-lang-stay]').addEventListener('click', stay);
      box.addEventListener('keydown', function (e) { if (e.key === 'Escape') stay(); });
    }, 900);
  })();
})();
