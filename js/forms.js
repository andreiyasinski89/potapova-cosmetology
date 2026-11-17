/* Форми заявки та відгуку.
   Принцип (той самий, що на clever-travel.club): заявка летить у ВСІ підключені канали одночасно
   (email через FormSubmit, CRM, Telegram-бот через воркер). Заявка вважається прийнятою, якщо спрацював хоча б один.
   Якщо не спрацював жоден (або жоден не підключений) — відкриваємо месенджер/пошту з уже готовим текстом.
   Захист: приховане поле-пастка, мінімальний час заповнення, пауза між відправками, обов'язкова згода. */
(function () {
  'use strict';
  var S = window.SITE || {}, F = S.forms || {}, C = S.contacts || {};
  var LANG = (document.documentElement.lang || 'uk').slice(0, 2);
  var T = function (uk, ru) { return LANG === 'ru' ? ru : uk; };
  var safe = function (fn) { try { return fn(); } catch (e) { return null; } };

  /* ---------- UTM: запам'ятовуємо перше джерело візиту (Instagram, реклама тощо) ---------- */
  var UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'fbclid', 'ref'];
  (function captureUtm() {
    var q = new URLSearchParams(location.search), got = {};
    UTM_KEYS.forEach(function (k) { var v = q.get(k); if (v) got[k] = v.slice(0, 100); });
    if (Object.keys(got).length) safe(function () { sessionStorage.setItem('pcUtm', JSON.stringify(got)); });
  })();
  function utm() { return safe(function () { return JSON.parse(sessionStorage.getItem('pcUtm')) || {}; }) || {}; }

  /* ---------- Канали доставки ---------- */
  function toFormSubmit(p) {
    if (!F.formsubmitEmail) return Promise.resolve(false);
    var body = { 'Ім\'я': p.name, 'Контакт': p.contact, 'Послуга': p.service, 'Зручний канал': p.channel, 'Коментар': p.message || '—', 'Мова сайту': p.lang, 'Сторінка': p.page, 'Джерело': p.utm_source || '—', _subject: 'Заявка з сайту Potapova Cosmetology', _template: 'table', _captcha: 'false' };
    return fetch('https://formsubmit.co/ajax/' + encodeURIComponent(F.formsubmitEmail), { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (j) { return r.ok && String(j.success) !== 'false'; }, function () { return r.ok; }); })
      .catch(function () { return false; });
  }
  function toCrm(p) {
    var c = F.crm || {};
    if (!c.url || !c.key) return Promise.resolve(false);
    var body = new URLSearchParams();
    Object.keys(p).forEach(function (k) { if (p[k]) body.append(k, String(p[k])); });
    return fetch(c.url.replace(/\/$/, '') + '/' + c.key, { method: 'POST', body: body, credentials: 'omit', keepalive: true })
      .then(function (r) { return r.ok; }).catch(function () { return false; });
  }
  function toTelegram(p) {
    if (!F.telegramRelay) return Promise.resolve(false);
    return fetch(F.telegramRelay, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(p), keepalive: true })
      .then(function (r) { return r.ok; }).catch(function () { return false; });
  }
  function anyConfigured() { return !!(F.formsubmitEmail || (F.crm && F.crm.url && F.crm.key) || F.telegramRelay); }

  /* ---------- Запасний варіант: месенджер/пошта з готовим текстом ---------- */
  function fallbackLinks(p) {
    var text = [T('Заявка з сайту', 'Заявка с сайта'), T("Ім'я", 'Имя') + ': ' + p.name, T('Контакт', 'Контакт') + ': ' + p.contact, T('Послуга', 'Услуга') + ': ' + p.service, p.message ? T('Коментар', 'Комментарий') + ': ' + p.message : ''].filter(Boolean).join('\n');
    var d = function (v) { return String(v || '').replace(/\D/g, ''); }, out = [];
    if (C.whatsapp) out.push(['WhatsApp', 'https://wa.me/' + d(C.whatsapp) + '?text=' + encodeURIComponent(text)]);
    if (C.telegram) out.push(['Telegram', 'https://t.me/' + String(C.telegram).replace(/^@/, '')]);
    if (C.viber) out.push(['Viber', 'viber://chat?number=%2B' + d(C.viber)]);
    if (C.email) out.push(['Email', 'mailto:' + C.email + '?subject=' + encodeURIComponent(T('Заявка з сайту', 'Заявка с сайта')) + '&body=' + encodeURIComponent(text)]);
    return out;
  }

  /* ---------- Валідація ---------- */
  function validContact(v) {
    v = String(v || '').trim();
    if (/^@[A-Za-z0-9_]{4,}$/.test(v)) return true;                    // Telegram
    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) return true;             // email
    return v.replace(/\D/g, '').length >= 9;                           // телефон
  }

  function track(name, params) { if (window.siteTrack) window.siteTrack(name, params || {}); }

  /* ---------- Форма заявки ---------- */
  document.querySelectorAll('form[data-lead]').forEach(function (f) {
    var opened = Date.now(), formId = f.getAttribute('data-form-id') || 'lead';
    var err = f.querySelector('[data-err]'), ok = f.querySelector('[data-ok]'), fb = f.querySelector('[data-fallback]'), btn = f.querySelector('button[type=submit]');
    var svc = new URLSearchParams(location.search).get('service');
    if (svc && f.service) [].some.call(f.service.options, function (o) { if (o.value.toLowerCase() === svc.toLowerCase()) { f.service.value = o.value; return true; } });
    f.addEventListener('focusin', function once() { track('form_start', { form_id: formId }); f.removeEventListener('focusin', once); });

    f.addEventListener('submit', function (e) {
      e.preventDefault();
      ok.hidden = true; fb.hidden = true;
      var name = f.name.value.trim(), contact = f.contact.value.trim();
      if (!name || !validContact(contact) || (f.consent && !f.consent.checked)) { err.hidden = false; (!name ? f.name : f.contact).focus(); return; }
      err.hidden = true;
      if (f._honey && f._honey.value) return;                                             // пастка для ботів
      if (Date.now() - opened < 2500) return;                                             // людина так швидко не заповнює
      var last = +safe(function () { return localStorage.getItem('pcLastSend'); }) || 0;
      if (Date.now() - last < (F.cooldownSec || 30) * 1000) { err.textContent = T('Заявку щойно надіслано. Спробуйте за хвилину.', 'Заявка только что отправлена. Попробуйте через минуту.'); err.hidden = false; return; }

      var u = utm();
      var payload = Object.assign({
        name: name, contact: contact, service: f.service ? f.service.value : '', channel: f.channel ? f.channel.value : '',
        message: f.msg ? f.msg.value.trim() : '', consent: 'yes', form: formId, lang: LANG.toUpperCase(), page: location.pathname, ts: new Date().toISOString()
      }, u);
      var label = btn.textContent; btn.disabled = true; btn.textContent = T('Надсилаємо…', 'Отправляем…');

      Promise.all([toFormSubmit(payload), toCrm(payload), toTelegram(payload)]).then(function (r) {
        var sent = r.some(Boolean);
        btn.disabled = false; btn.textContent = label;
        if (sent) {
          safe(function () { localStorage.setItem('pcLastSend', String(Date.now())); });
          ok.hidden = false; f.reset();
          track('generate_lead', { form_id: formId, service: payload.service, method: ['formsubmit', 'crm', 'telegram'].filter(function (m, i) { return r[i]; }).join('+') });
        } else {
          var links = fallbackLinks(payload);
          fb.hidden = false;
          fb.innerHTML = (anyConfigured() ? T('Не вдалося надіслати автоматично. Напишіть нам напряму:', 'Не удалось отправить автоматически. Напишите нам напрямую:') : T('Напишіть нам напряму:', 'Напишите нам напрямую:'));
          if (links.length) {
            var ul = document.createElement('span'); ul.className = 'fb-links';
            links.forEach(function (l) { var a = document.createElement('a'); a.href = l[1]; a.textContent = l[0]; a.className = 'btn btn-ghost'; if (/^https/.test(l[1])) { a.target = '_blank'; a.rel = 'noopener noreferrer'; } ul.appendChild(a); });
            fb.appendChild(ul);
            track('generate_lead', { form_id: formId, service: payload.service, method: 'fallback' });
            window.open(links[0][1], '_blank', 'noopener');
          } else {
            fb.textContent += ' ' + T('(контакти будуть додані найближчим часом)', '(контакты будут добавлены в ближайшее время)');
          }
        }
      });
    });
  });

  /* ---------- Форма відгуку (потрапляє в Google Таблицю; публікується лише після схвалення) ---------- */
  document.querySelectorAll('form[data-review]').forEach(function (f) {
    var url = (S.reviews && S.reviews.url) || '', err = f.querySelector('[data-err]'), ok = f.querySelector('[data-ok]'), btn = f.querySelector('button[type=submit]');
    f.addEventListener('submit', function (e) {
      e.preventDefault(); ok.hidden = true;
      var name = f.name.value.trim(), text = f.text.value.trim();
      if (!name || text.length < 10 || !f.consent.checked) { err.hidden = false; return; }
      err.hidden = true; if (f._honey && f._honey.value) return;
      var body = new URLSearchParams({ action: 'review', name: name, city: f.city ? f.city.value.trim() : '', rating: f.rating ? f.rating.value : '5', text: text, lang: LANG, consent: 'yes' });
      var label = btn.textContent; btn.disabled = true; btn.textContent = T('Надсилаємо…', 'Отправляем…');
      var done = function (good) {
        btn.disabled = false; btn.textContent = label;
        if (good) { ok.textContent = T('Дякуємо! Відгук з’явиться на сайті після перевірки.', 'Спасибо! Отзыв появится на сайте после проверки.'); ok.hidden = false; f.reset(); track('review_submit', {}); }
        else { err.textContent = T('Не вдалося надіслати. Напишіть нам у месенджер.', 'Не удалось отправить. Напишите нам в мессенджер.'); err.hidden = false; }
      };
      if (!url) return done(false);
      fetch(url, { method: 'POST', body: body, mode: 'no-cors' }).then(function () { done(true); }).catch(function () { done(false); });   // Apps Script відповідає без CORS: no-cors достатньо
    });
  });
})();
