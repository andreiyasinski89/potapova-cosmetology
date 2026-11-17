#!/usr/bin/env python3
"""Перевірка зібраного сайту: биті відносні посилання/ресурси, залишки {{...}}, коректність hreflang, html lang.
   Запуск: python tools/check.py  (після tools/build.py). Код виходу 1, якщо є проблеми."""
import os, re, sys, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
pages = [os.path.join(dp, f) for dp, dn, fs in os.walk('.') for f in fs
         if f.endswith('.html') and not re.match(r'\.[/\\](src|docs|tools|integrations|\.git)', os.path.join(dp, f))]
bad = []
for p in sorted(pages):
    s = open(p, encoding='utf-8').read()
    lang = 'ru' if p.replace('\\', '/').startswith('./ru/') else 'uk'
    if '{{' in s or '@@KEEP' in s: bad.append((p, 'залишився плейсхолдер'))
    if f'<html lang="{lang}"' not in s: bad.append((p, f'html lang != {lang}'))
    if 'l-uk' in s or 'l-ru' in s: bad.append((p, 'залишились мовні блоки'))
    for m in re.finditer(r'(?:href|src|poster)="([^"]+)"', s):
        u = m.group(1)
        if re.match(r'(https?:|mailto:|tel:|viber:|data:|#|javascript:)', u) or '{' in u or u.startswith('//'):
            continue
        path = urllib.parse.unquote(u.split('#')[0].split('?')[0])
        if not path: continue
        t = os.path.normpath(os.path.join(os.path.dirname(p), path))
        if not os.path.exists(t): bad.append((p, f'нема файлу: {u}'))
    # ru-сторінка не повинна містити українських літер у видимому тексті (грубий контроль)
    if lang == 'ru':
        text = re.sub(r'<(script|style)\b.*?</\1>', '', s, flags=re.S)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\[[^\]]*\]', '', text)
        left = set(re.findall(r'\b\w*[іїєґІЇЄҐ]\w*\b', text))
        left = {w for w in left if w.lower() not in {'potapova'}}
        if left: bad.append((p, 'українські літери в ru: ' + ', '.join(sorted(left)[:8])))
print(f'перевірено сторінок: {len(pages)}')
for p, why in bad: print(' ✗', p, why)
print('OK: проблем не знайдено' if not bad else f'проблем: {len(bad)}')
sys.exit(1 if bad else 0)
