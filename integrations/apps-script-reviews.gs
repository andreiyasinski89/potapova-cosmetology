/**
 * Відгуки для сайту: Google Таблиця + Google Apps Script.
 *
 * Як підключити (докладно в docs/INTEGRATIONS.md):
 *  1. Створіть Google Таблицю, на першому аркуші назвіть аркуш "Reviews".
 *  2. У рядку 1 впишіть заголовки A..H:
 *       Дата | Ім'я | Місто | Оцінка | Текст | Мова | Опубліковано | Згода
 *     Стовпець G «Опубліковано»: Вставка → Прапорець (галочка). Відгук з'явиться на сайті, коли власник ставить галочку.
 *  3. Розширення → Apps Script → вставте цей файл → Розгорнути → Веб-застосунок:
 *       Виконувати від імені: Я,  Доступ: Усі.
 *  4. Скопіюйте URL розгортання (закінчується на /exec) у js/config.js → reviews.url
 *
 * GET  ?action=reviews   -> {"reviews":[{name,city,rating,text,lang}, ...]}   (лише рядки з галочкою)
 * POST action=review     -> додає новий відгук з галочкою FALSE (чекає на перевірку)
 */
var SHEET_NAME = 'Reviews';
var NOTIFY_EMAIL = '';          // необов'язково: на цю пошту прийде лист про новий відгук
var MAX_TEXT = 1200;

function doGet(e) {
  var action = (e && e.parameter && e.parameter.action) || '';
  if (action === 'reviews') return json_({ reviews: published_() });
  return json_({ ok: true });
}

function doPost(e) {
  var p = (e && e.parameter) || {};
  if (p.action !== 'review') return json_({ ok: false, error: 'bad action' });
  var name = clean_(p.name, 80), text = clean_(p.text, MAX_TEXT);
  var rating = Math.max(1, Math.min(5, parseInt(p.rating, 10) || 5));
  if (!name || text.length < 10 || p.consent !== 'yes') return json_({ ok: false, error: 'invalid' });
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    sheet_().appendRow([new Date(), name, clean_(p.city, 80), rating, text, clean_(p.lang, 5), false, 'yes']);
  } finally { lock.release(); }
  if (NOTIFY_EMAIL) {
    MailApp.sendEmail(NOTIFY_EMAIL, 'Новий відгук на сайті (чекає на перевірку)', name + ' (' + rating + '/5)\n\n' + text);
  }
  return json_({ ok: true });
}

function published_() {
  var cache = CacheService.getScriptCache(), hit = cache.get('reviews');
  if (hit) return JSON.parse(hit);
  var rows = sheet_().getDataRange().getValues().slice(1), out = [];
  rows.forEach(function (r) {
    if (r[6] === true && r[1] && r[4]) out.push({ name: String(r[1]), city: String(r[2] || ''), rating: Number(r[3]) || 5, text: String(r[4]), lang: String(r[5] || '') });
  });
  out.reverse();                         // нові зверху
  cache.put('reviews', JSON.stringify(out), 120);
  return out;
}

function sheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  return ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
}
function clean_(v, max) { return String(v || '').replace(/[\u0000-\u001f]/g, ' ').trim().slice(0, max); }
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
