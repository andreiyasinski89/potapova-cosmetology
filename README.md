# Potapova Cosmetology: сайт

Статический сайт (HTML/CSS/JS), без сервера и базы данных. Две языковые версии: `/` (укр) и `/ru/` (рус). Хостится бесплатно на GitHub Pages.

## Структура

```
src/            исходные страницы (украинский текст) и шаблоны шапки/подвала (src/partials)
i18n/           русский перевод (ru.json, ru.extra.json)
tools/build.py  собирает src/ → корень сайта и ru/, sitemap.xml, robots.txt, CNAME
tools/build-assets.py   сжимает оригиналы фото/видео из папки клиента в assets/
js/config.js    ВСЕ ссылки на чаты, ключи, аналитика, куда слать заявки
js/             contacts.js (чаты), forms.js (заявки, отзывы), consent.js (cookie, аналитика), reviews.js
css/            tokens.css (цвета, шрифты), styles.css, media.css, connect.css
assets/         сжатые фото, видео, логотип, фавикон
integrations/   код для Telegram-воркера и Google Apps Script (отзывы)
docs/INTEGRATIONS.md   пошаговая настройка каждого канала
```

Готовые страницы (`index.html`, `ru/…` и т.д.) лежат в репозитории и отдаются как есть. Редактировать их руками не нужно: правьте `src/` и запускайте сборку.

## Что делать, чтобы запустить

1. **Выгрузить на GitHub.** Создайте репозиторий, затем:
   ```bash
   git remote add origin https://github.com/andreiyasinski89/potapova-cosmetology.git
   git push -u origin main
   ```
2. **Включить Pages:** репозиторий → Settings → Pages → Source: `Deploy from a branch`, ветка `main`, папка `/ (root)`.
3. **Подключить домен:**
   * В `site.json` впишите `{"domain": "https://ваш-домен.com"}`, затем `python tools/build.py` и коммит. Сборка пропишет `canonical`, `hreflang`, `og:url`, создаст `sitemap.xml`, `robots.txt`, `CNAME`. (Пока домена нет, `robots.txt` закрывает сайт от индексации.)
   * У регистратора домена создайте записи: для основного домена четыре `A` на `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; для `www` запись `CNAME` на `andreiyasinski89.github.io`.
   * Settings → Pages → Custom domain → ваш домен → включите **Enforce HTTPS**.
4. **Вписать ссылки** в `js/config.js` (см. [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md)): Telegram, WhatsApp, Viber, телефон, куда слать заявки, ID аналитики. Закоммитить и запушить: сайт обновится за минуту.
5. **Заполнить `[ЗАПОЛНИТЬ]`**: список материалов в [MISSING.md](MISSING.md). Тексты правятся в `src/`, затем `python tools/build.py`.

## Ежедневная работа

```bash
python tools/build.py        # после правки src/ или i18n/
git add -A && git commit -m "..." && git push
```
Для локального просмотра: `python -m http.server 5173`, затем http://localhost:5173.
Сборка выводит список строк, которых нет в русском переводе: добавьте их в `i18n/ru.extra.json`.
Нужен Python 3.9+ без сторонних библиотек (для сжатия медиа ещё `Pillow`, `PyMuPDF`, `ffmpeg`).

## Перед публикацией
* Юристу: `privacy.html`, `terms.html`, `contraindications.html`, `cookies.html` (это черновики), формулировки про инъекции.
* Врачу: статьи журнала, противопоказания, данные об образовании и сертификатах.
* Реквизиты ФОП/ТОВ и лицензия: в подвале (`src/partials/footer.html`).
