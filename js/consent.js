/* Cookie-згода та аналітика для всіх сторінок (один файл).
   - Google Analytics 4 у режимі Google Consent Mode v2: усе "denied", поки відвідувач не обрав.
   - Meta Pixel вантажиться лише після згоди на маркетинг; Microsoft Clarity лише після згоди на аналітику.
   - Якщо в js/config.js не вказано жодного ID, банер НЕ показується (сайт не ставить ніяких cookie).
   - Вибір зберігається у localStorage ("pcConsent") на 12 місяців.
   - Події: click_telegram / click_whatsapp / click_viber / click_instagram / click_phone / click_email / click_book,
     form_start, generate_lead (заявка), review_submit, language_switch. */
(function () {
  'use strict';
  if (window.__pcConsent) return; window.__pcConsent = true;
  var A = (window.SITE && window.SITE.analytics) || {};
  var LANG = (document.documentElement.lang || 'uk').slice(0, 2);
  var KEY = 'pcConsent', VERSION = 1, MAX_AGE = 365 * 24 * 60 * 60 * 1000;
  var enabled = !!(A.ga4 || A.metaPixel || A.clarity);

  var TXT = {
    uk: { aria: 'Налаштування cookie', title: 'Ми цінуємо вашу приватність', desc: 'Необхідні технології потрібні для роботи сайту. Аналітичні та маркетингові вмикаються лише за вашої згоди. Подробиці: ', cookiePolicy: 'політика cookie', and: 'і', privacy: 'політика конфіденційності', nec: 'Необхідні', necD: 'Робота сайту та збереження вашого вибору. Завжди ввімкнені.', an: 'Аналітичні', anD: 'Google Analytics і Microsoft Clarity: статистика відвідувань, кліки та прокручування.', mk: 'Маркетингові', mkD: 'Meta Pixel і сигнали згоди для Google: вимірювання реклами.', accept: 'Прийняти', decline: 'Відхилити', more: 'Налаштувати', save: 'Зберегти вибір' },
    ru: { aria: 'Настройки cookie', title: 'Мы ценим вашу приватность', desc: 'Необходимые технологии нужны для работы сайта. Аналитические и маркетинговые включаются только с вашего согласия. Подробности: ', cookiePolicy: 'политика cookie', and: 'и', privacy: 'политика конфиденциальности', nec: 'Необходимые', necD: 'Работа сайта и сохранение вашего выбора. Всегда включены.', an: 'Аналитические', anD: 'Google Analytics и Microsoft Clarity: статистика посещений, клики и прокрутка.', mk: 'Маркетинговые', mkD: 'Meta Pixel и сигналы согласия для Google: измерение рекламы.', accept: 'Принять', decline: 'Отклонить', more: 'Настроить', save: 'Сохранить выбор' }
  }[LANG] || null;
  var t = TXT || {};
  function read() {
    try { var o = JSON.parse(localStorage.getItem(KEY)); if (o && o.v === VERSION && Date.now() - o.t < MAX_AGE) return o; } catch (e) {}
    return null;
  }
  function write(an, mk) { try { localStorage.setItem(KEY, JSON.stringify({ v: VERSION, t: Date.now(), analytics: !!an, marketing: !!mk })); } catch (e) {} }
  var state = read();

  /* ---------- Google Consent Mode v2 ---------- */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  if (A.ga4) {
    gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', wait_for_update: 500 });
    gtag('set', 'ads_data_redaction', true);
    gtag('js', new Date()); gtag('config', A.ga4);
    var ga = document.createElement('script'); ga.async = true; ga.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(A.ga4); document.head.appendChild(ga);
  }
  var pixelOn = false, clarityOn = false;
  function loadPixel() {
    if (!A.metaPixel || pixelOn) return; pixelOn = true;
    !function (f, b, e, v, n, tt, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; tt = b.createElement(e); tt.async = !0; tt.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(tt, s); }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', A.metaPixel); window.fbq('track', 'PageView');
  }
  function loadClarity() {
    if (!A.clarity || clarityOn) return; clarityOn = true;
    (function (c, l, a, r, i, tt, y) { c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); }; tt = l.createElement(r); tt.async = 1; tt.src = 'https://www.clarity.ms/tag/' + i; y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(tt, y); })(window, document, 'clarity', 'script', A.clarity);
  }
  function apply(st) {
    var an = st && st.analytics ? 'granted' : 'denied', mk = st && st.marketing ? 'granted' : 'denied';
    if (A.ga4) gtag('consent', 'update', { analytics_storage: an, ad_storage: mk, ad_user_data: mk, ad_personalization: mk });
    if (st && st.analytics) loadClarity();
    if (st && st.marketing) loadPixel();
  }
  if (state) apply(state);

  /* ---------- Банер ---------- */
  var box = null;
  function closeBanner() { if (box) { box.remove(); box = null; } }
  function openBanner() {
    if (!enabled || !TXT || box) return;
    var ex = state || { analytics: false, marketing: false };
    box = document.createElement('div'); box.className = 'consent-banner'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-label', t.aria);
    var P = function (p) { return (document.querySelector('footer a[href$="' + p + '"]') || {}).href || p; };
    box.innerHTML = '<h2>' + t.title + '</h2><p>' + t.desc + '<a class="link" href="' + P('cookies.html') + '">' + t.cookiePolicy + '</a> ' + t.and + ' <a class="link" href="' + P('privacy.html') + '">' + t.privacy + '</a>.</p>' +
      '<div class="cb-more" hidden>' +
      '<label><input type="checkbox" checked disabled> <b>' + t.nec + '</b><small>' + t.necD + '</small></label>' +
      '<label><input type="checkbox" data-an ' + (ex.analytics ? 'checked' : '') + '> <b>' + t.an + '</b><small>' + t.anD + '</small></label>' +
      '<label><input type="checkbox" data-mk ' + (ex.marketing ? 'checked' : '') + '> <b>' + t.mk + '</b><small>' + t.mkD + '</small></label></div>' +
      '<div class="cb-actions"><button type="button" class="btn btn-ghost" data-decline>' + t.decline + '</button><button type="button" class="btn btn-ghost" data-more>' + t.more + '</button><button type="button" class="btn btn-primary" data-accept>' + t.accept + '</button></div>';
    document.body.appendChild(box);
    var more = box.querySelector('.cb-more'), moreBtn = box.querySelector('[data-more]');
    function save(an, mk) { state = { analytics: an, marketing: mk }; write(an, mk); apply(state); closeBanner(); }
    box.querySelector('[data-accept]').onclick = function () { save(true, true); };
    box.querySelector('[data-decline]').onclick = function () { save(false, false); };
    moreBtn.onclick = function () {
      if (more.hidden) { more.hidden = false; moreBtn.textContent = t.save; }
      else save(box.querySelector('[data-an]').checked, box.querySelector('[data-mk]').checked);
    };
    box.addEventListener('keydown', function (e) { if (e.key === 'Escape' && state) closeBanner(); });
  }
  document.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('[data-cookie-settings]')) { if (!enabled) return; closeBanner(); openBanner(); } });
  function first() { if (!state) setTimeout(openBanner, 600); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', first); else first();
  if (!enabled) document.querySelectorAll('[data-cookie-settings]').forEach(function (b) { b.hidden = true; });

  /* ---------- Події ---------- */
  var FB = { generate_lead: 'Lead', click_telegram: 'Contact', click_whatsapp: 'Contact', click_viber: 'Contact', click_instagram: 'Contact', click_phone: 'Contact', review_submit: 'SubmitApplication' };
  function track(name, params) {
    params = params || {}; params.page_language = LANG; params.transport_type = 'beacon';
    try { if (A.ga4) gtag('event', name, params); } catch (e) {}
    try { if (window.fbq && FB[name]) window.fbq('track', FB[name], { content_name: params.service || params.link_location || name }); } catch (e) {}
    try { if (window.clarity) window.clarity('event', name); } catch (e) {}
  }
  window.siteTrack = track;
  function where(a) { if (a.closest('footer')) return 'footer'; if (a.closest('header')) return 'header'; if (a.closest('.chat')) return 'chat_button'; if (a.closest('.mbar')) return 'mobile_bar'; if (a.closest('.topbar')) return 'topbar'; return 'page'; }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]'); if (!a) return;
    var href = a.getAttribute('href') || '', low = href.toLowerCase(), name = null, host = '';
    if (low.indexOf('tel:') === 0) name = 'click_phone';
    else if (low.indexOf('mailto:') === 0) name = 'click_email';
    else if (low.indexOf('viber:') === 0) name = 'click_viber';
    else { try { host = new URL(a.href, location.href).hostname.toLowerCase(); } catch (x) {}
      if (host === 't.me' || host === 'telegram.me') name = 'click_telegram';
      else if (host === 'wa.me' || /(^|\.)whatsapp\.com$/.test(host)) name = 'click_whatsapp';
      else if (host === 'ig.me' || /(^|\.)instagram\.com$/.test(host)) name = 'click_instagram'; }
    if (name) track(name, { link_url: String(a.href).slice(0, 200), link_location: where(a) });
    var ge = a.closest('[data-ga-event]'); if (ge) track(ge.getAttribute('data-ga-event'), { link_location: where(ge) });
    var to = a.getAttribute('hreflang');
    if (to && to !== LANG) track('language_switch', { language_from: LANG, language_to: to });
  }, true);
})();
