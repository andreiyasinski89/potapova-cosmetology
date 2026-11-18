#!/usr/bin/env python3
"""Збирає сайт: src/*.html (українська мова + шматки включень) -> корінь (uk) і ru/ (російська).
   Запуск:  python tools/build.py
   Домен та інші параметри: site.json  ({"domain": "https://example.com"}).
   Українські тексти беруться зі src/, російські з i18n/ru.json + i18n/ru.extra.json.
   Блоки <div class="l-uk">/<div class="l-ru"> (довгі статті, юр. тексти) вибираються за мовою сторінки.
   Результат (HTML, sitemap.xml, robots.txt, CNAME) комітиться: GitHub Pages віддає корінь репозиторію."""
import json, os, re, sys, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SRC = 'src'
site = json.load(open('site.json', encoding='utf-8')) if os.path.exists('site.json') else {}
DOMAIN = (site.get('domain') or '').rstrip('/')
DOMAIN_OR_PLACEHOLDER = DOMAIN or 'https://[ДОМЕН]'

RU = json.load(open('i18n/ru.json', encoding='utf-8'))
if os.path.exists('i18n/ru.extra.json'):
    RU.update(json.load(open('i18n/ru.extra.json', encoding='utf-8')))
norm = lambda s: ' '.join(s.split())
RU = {norm(k): v for k, v in RU.items()}

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages import gen_pages, gen_partials
from static_pages import gen_static          # сторінки послуг, каталог, ціни (tools/content.py)

SOURCES = {}
for dp, _, fs in os.walk(SRC):
    if 'partials' in dp.replace(os.sep, '/').split('/'):
        continue
    for f in fs:
        if f.endswith('.html'):
            rel = os.path.relpath(os.path.join(dp, f), SRC).replace(os.sep, '/')
            SOURCES[rel] = open(os.path.join(dp, f), encoding='utf-8').read()
SOURCES.update(gen_pages())
SOURCES.update(gen_static())
GEN_PARTIALS = gen_partials()
PAGES = sorted(SOURCES)
NOINDEX = {'404.html'}
import datetime
TODAY = datetime.date.today().isoformat()

# ---------- включення ----------
def include(html, depth=0):
    def rep(m):
        name, args = m.group(1), m.group(2) or ''
        part = GEN_PARTIALS[name] if name in GEN_PARTIALS else open(f'{SRC}/partials/{name}.html', encoding='utf-8').read()
        for k, v in re.findall(r'(\w+)=(\S+)', args):
            part = part.replace('{{' + k + '}}', v)
        return include(part, depth + 1)
    return re.sub(r'<!--#include (\w+)([^>]*?)-->', rep, html)

# ---------- мовні блоки ----------
def find_close(html, start, tag):
    """індекс кінця елемента <tag ...> що починається в start (з урахуванням вкладених однойменних)."""
    pat = re.compile(rf'<(/?){tag}\b[^>]*>')
    depth = 0
    for m in pat.finditer(html, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.start(), m.end()
    raise ValueError('unbalanced ' + tag)

KEEP = {}
def lang_blocks(html, keep):
    """Видаляє блоки іншої мови; вміст блоку потрібної мови ховає під токен (відновлюється після перекладу)."""
    drop = 'ru' if keep == 'uk' else 'uk'
    for lang, action in ((drop, 'remove'), (keep, 'unwrap')):
        while True:
            m = re.search(rf'<(div|span) class=["\x27]l-{lang}["\x27]>', html)
            if not m:
                break
            cs, ce = find_close(html, m.start(), m.group(1))
            inner = html[m.end():cs]
            if action == 'unwrap':
                tok = f'@@KEEP{len(KEEP)}@@'; KEEP[tok] = inner; inner = tok
            else:
                inner = ''
            html = html[:m.start()] + inner + html[ce:]
    return html

def restore(html):
    for _ in range(3):
        html = re.sub(r'@@KEEP\d+@@', lambda m: KEEP[m.group(0)], html)
    return html

# ---------- переклад ----------
MISSING = {}
PH = [('ЗАПОВНИТИ', 'ЗАПОЛНИТЬ'), ('ЦІНА', 'ЦЕНА'), ('ГОДИНИ РОБОТИ', 'ЧАСЫ РАБОТЫ'), ('ЛІЦЕНЗІЯ', 'ЛИЦЕНЗИЯ'), ('ТРИВАЛІСТЬ', 'ДЛИТЕЛЬНОСТЬ'),
      ('УТОЧНИТИ', 'УТОЧНИТЬ'), ('КОНТАКТИ', 'КОНТАКТЫ'), ('ФОП/ТОВ', 'ФЛП/ООО'), ('РЕКВІЗИТИ', 'РЕКВИЗИТЫ'), ('№ ТА ДАТА', '№ И ДАТА'),
      ('ВІДГУК ПАЦІЄНТА, ЗА ЗГОДОЮ', 'ОТЗЫВ ПАЦИЕНТА, С СОГЛАСИЯ'), ("Ім'я", 'Имя'), ('Місто', 'Город'), ('ІНШІ', 'ДРУГИЕ'), ('АДРЕСА', 'АДРЕС'),
      ('ТЕЛЕФОН', 'ТЕЛЕФОН'), ('ЗАГОЛОВОК СТАТТІ', 'ЗАГОЛОВОК СТАТЬИ'), ('ФОТО', 'ФОТО'), ('ВІДЕО', 'ВИДЕО'), ('Лікар', 'Врач'), ('Юрист: без назв рецептурних препаратів у рекламних заголовках', 'Юрист: без названий рецептурных препаратов в рекламных заголовках'),
      ('освіта, спеціальність, сертифікати', 'образование, специальность, сертификаты'), ('месенджери у js/config.js', 'мессенджеры в js/config.js'),
      ('для кого процедура, які задачі вирішує', 'для кого процедура, какие задачи решает'), ('препарат/виробник', 'препарат/производитель'),
      ('протипоказання, реабілітація', 'противопоказания, реабилитация'), ('заголовок статті', 'заголовок статьи'),
      ("Telegram, WhatsApp, Viber, телефон у js/config.js, і картки з'являться автоматично", 'Telegram, WhatsApp, Viber, телефон в js/config.js, и карточки появятся автоматически'),
      ('вставте посилання на карту у js/config.js, поле mapEmbed', 'вставьте ссылку на карту в js/config.js, поле mapEmbed'), ('ЗАПОВНИТИ відповіддю лікаря', 'ЗАПОЛНИТЬ ответом врача'), ('УТОЧНИТИ', 'УТОЧНИТЬ')]
def tr(text, page):
    n = norm(text)
    if not n or len(n) <= 2:
        return text
    lead = re.match(r'\s*', text).group(0); trail = re.search(r'\s*$', text).group(0)
    if n in RU:
        return lead + RU[n] + trail
    if n.startswith('«') and n.endswith('»'):   # цитата-оригінал (відгуки Google мовою автора)
        return text
    if '[' in n:                       # плейсхолдери [ЗАПОВНИТИ ...]
        out = n
        for a, b in PH:
            out = out.replace(a, b)
        return lead + out + trail
    if re.search(r'[А-Яа-яІіЇїЄєҐґ]', n) and not re.fullmatch(r'[\W\d_]*', n):
        MISSING.setdefault(n, set()).add(page)
    return text

def translate_json(obj, page):
    if isinstance(obj, str):
        return RU.get(norm(obj), obj)
    if isinstance(obj, list):
        return [translate_json(x, page) for x in obj]
    if isinstance(obj, dict):
        return {k: translate_json(v, page) for k, v in obj.items()}
    return obj

ATTRS = ('alt', 'aria-label', 'title', 'placeholder')
def translate_html(html, page):
    # JSON-LD
    def ld(m):
        try:
            d = translate_json(json.loads(m.group(2)), page)
            if isinstance(d, dict) and d.get('@type') in ('MedicalBusiness', 'MedicalProcedure', 'FAQPage'):
                d['inLanguage'] = 'ru'
            return m.group(1) + json.dumps(d, ensure_ascii=False) + m.group(3)
        except Exception:
            return m.group(0)
    html = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', ld, html, flags=re.S)
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', html, flags=re.S)
    out = []
    for p in parts:
        if p.startswith('<script') or p.startswith('<style'):
            out.append(p); continue
        p = re.sub(r'>([^<>]+)<', lambda m: '>' + tr(m.group(1), page) + '<', p)
        for a in ATTRS:
            p = re.sub(rf'(\s{a}=")([^"]*)(")', lambda m: m.group(1) + tr(m.group(2), page) + m.group(3), p)
        p = re.sub(r'(<meta (?:name="description"|property="og:(?:title|description)") content=")([^"]*)(")',
                   lambda m: m.group(1) + tr(m.group(2), page) + m.group(3), p)
        out.append(p)
    return ''.join(out)

# ---------- збірка ----------
import hashlib
_HASH = {}
def bust(html):
    """css/js?v=<хеш вмісту>: після кожної зміни файлу браузери й телефони беруть свіжу версію."""
    def rep(m):
        path = m.group(2)
        if path not in _HASH:
            _HASH[path] = hashlib.md5(open(path, 'rb').read()).hexdigest()[:8] if os.path.exists(path) else '0'
        return f'{m.group(1)}{m.group(2)}?v={_HASH[path]}"'
    return re.sub(r'((?:href|src)=")(?:\.\./)*((?:css|js)/[A-Za-z0-9_.-]+\.(?:css|js))"', lambda m: (m.group(1) + m.group(0)[len(m.group(1)):].split('"')[0] + f'?v=' + _HASH.setdefault(m.group(2), hashlib.md5(open(m.group(2), 'rb').read()).hexdigest()[:8]) + '"'), html)

def build_page(rel, lang):
    html = include(SOURCES[rel])
    html = re.sub(r'<!--(?!#).*?-->', '', html, flags=re.S)
    KEEP.clear()
    html = lang_blocks(html, lang)
    d = rel.count('/')
    P = '../' * d
    A = P if lang == 'uk' else P + '../'
    base = os.path.basename(rel)
    lang_uk = base if lang == 'uk' else A + rel
    lang_ru = base if lang == 'ru' else P + 'ru/' + rel
    if lang == 'ru':
        html = translate_html(html, rel)
    html = restore(html)
    html = (html.replace('{{A}}', A).replace('{{P}}', P).replace('{{LANG_UK}}', lang_uk).replace('{{LANG_RU}}', lang_ru)
                .replace('{{DOMAIN}}', DOMAIN_OR_PLACEHOLDER).replace('{{LANG_CUR}}', 'УКР' if lang == 'uk' else 'РУС').replace('{{URLP}}', '' if lang == 'uk' else 'ru/'))
    html = bust(html)
    html = re.sub(r'<html lang="\w+"', f'<html lang="{lang}"', html, count=1)
    # посилання логотипа/«головна» у ru залишаються відносними (index.html), тож додаткових правок не потрібно
    if site.get('googleVerification') and rel not in NOINDEX:
        html = html.replace('</head>', f'<meta name="google-site-verification" content="{site["googleVerification"]}">\n</head>', 1)
    if not DOMAIN and rel not in NOINDEX:   # поки домену немає, не даємо пошуковикам індексувати github.io-адресу
        html = html.replace('</head>', '<meta name="robots" content="noindex, nofollow">\n</head>', 1)
    if rel not in NOINDEX:
        url = lambda l: f'{DOMAIN_OR_PLACEHOLDER}/' + ('' if l == 'uk' else 'ru/') + ('' if rel == 'index.html' else rel)
        head = (f'<link rel="canonical" href="{url(lang)}">\n'
                f'<link rel="alternate" hreflang="uk" href="{url("uk")}">\n<link rel="alternate" hreflang="ru" href="{url("ru")}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{url("uk")}">\n'
                f'<meta property="og:url" content="{url(lang)}">\n<meta property="og:locale" content="{"uk_UA" if lang == "uk" else "ru_UA"}">\n')
        html = html.replace('</head>', head + '</head>', 1)
    out = rel if lang == 'uk' else 'ru/' + rel
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    open(out, 'w', encoding='utf-8', newline='\n').write(html)
    return out

def main():
    shutil.rmtree('ru', ignore_errors=True)
    built = []
    for rel in PAGES:
        for lang in ('uk', 'ru'):
            built.append((rel, lang, build_page(rel, lang)))
    # sitemap / robots / CNAME / .nojekyll
    open('.nojekyll', 'w').close()
    if DOMAIN:
        urls = []
        for rel in PAGES:
            if rel in NOINDEX:
                continue
            u = lambda l: f'{DOMAIN}/' + ('' if l == 'uk' else 'ru/') + ('' if rel == 'index.html' else rel)
            for lang in ('uk', 'ru'):
                urls.append(f'  <url><loc>{u(lang)}</loc><lastmod>{TODAY}</lastmod>'
                            f'<xhtml:link rel="alternate" hreflang="uk" href="{u("uk")}"/><xhtml:link rel="alternate" hreflang="ru" href="{u("ru")}"/></url>')
        open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write(
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(urls) + '\n</urlset>\n')
        open('robots.txt', 'w', newline='\n').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
        open('CNAME', 'w', newline='\n').write(re.sub(r'^https?://', '', DOMAIN) + '\n')
    else:
        open('robots.txt', 'w', newline='\n').write('User-agent: *\nDisallow: /\n# Домен не вказано в site.json: сайт закрито від індексації до запуску. Після збірки з доменом файл оновиться.\n')
        for f in ('sitemap.xml', 'CNAME'):
            if os.path.exists(f): os.remove(f)
    print(f'зібрано сторінок: {len(built)}  (домен: {DOMAIN or "не вказано"})')
    if MISSING:
        print(f'\nНЕперекладено на російську: {len(MISSING)} рядків. Додайте їх до i18n/ru.extra.json:')
        for k in sorted(MISSING):
            print('  -', k[:110], '  [', ', '.join(sorted(MISSING[k])), ']')

if __name__ == '__main__':
    main()
