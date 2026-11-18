"""Генератор сторінок послуг, каталогу та цін з tools/content.py.
Усі тексти двомовні: <span class="l-uk">…</span><span class="l-ru">…</span>, build.py залишає потрібну мову."""
from content import SERVICES, CATS, DISCLAIMER, P, GOOGLE, GOOGLE_REVIEWS, REVIEWS_PAGE_SIZE

ICONS = {
 'face':  '<circle cx="17" cy="17" r="10"/><path d="M12 19c2 3 8 3 10 0M13 14h.01M21 14h.01"/>',
 'drop':  '<path d="M17 4c6 7 9 11 0 22-9-11-6-15 0-22z"/><path d="M12 20c1 3 4 4 6 3"/>',
 'bolt':  '<path d="M19 3 8 19h8l-2 12 11-16h-8z"/>',
 'wave':  '<path d="M3 12c4-6 7-6 11 0s7 6 11 0M3 22c4-6 7-6 11 0s7 6 11 0"/>',
 'sun':   '<circle cx="17" cy="17" r="5"/><path d="M17 4v4M17 26v4M4 17h4M26 17h4M8 8l3 3M23 23l3 3M26 8l-3 3M11 23l-3 3"/>',
 'lips':  '<path d="M4 17c4-5 8-5 13-2 5-3 9-3 13 2-4 6-8 8-13 8S8 23 4 17z"/><path d="M4 17h26"/>',
 'hand':  '<path d="M11 18V8a2 2 0 0 1 4 0v7M15 14V6a2 2 0 0 1 4 0v8M19 14V8a2 2 0 0 1 4 0v10c0 6-3 10-8 10-4 0-6-3-8-7l-2-4a2 2 0 0 1 3-2l3 4"/>',
 'leaf':  '<path d="M6 28C6 14 14 6 28 6c0 14-8 22-22 22zM6 28 18 16"/>',
}

UI = dict(
 home=('Головна', 'Главная'), services=('Послуги', 'Услуги'), book=('Записатися', 'Записаться'), prices=('Ціни', 'Цены'),
 more=('Детальніше', 'Подробнее'), from_=('від', 'от'), for_whom=('Для кого', 'Для кого'), process=('Як проходить', 'Как проходит'),
 tech=('Препарати та апарати', 'Препараты и аппараты'), contra=('Протипоказання', 'Противопоказания'), price=('Ціна', 'Цена'),
 faq=('Питання та відповіді', 'Вопросы и ответы'), related=('Також може бути цікаво', 'Также может быть интересно'),
 article=('Читати в журналі', 'Читать в журнале'), all_services=('Усі послуги', 'Все услуги'), all_=('Усі', 'Все'),
 cta_t=('Почнемо з консультації', 'Начнём с консультации'), cta_p=('Спеціаліст огляне шкіру, відповість на питання й запропонує план. Консультація не зобов\'язує до процедури.',
        'Специалист осмотрит кожу, ответит на вопросы и предложит план. Консультация не обязывает к процедуре.'),
 contra_p=('Це загальні обмеження. Повний перелік і остаточне рішення: на консультації.', 'Это общие ограничения. Полный перечень и окончательное решение: на консультации.'),
 pl_h=('Ціни та програми', 'Цены и программы'), see_prices=('Усі ціни', 'Все цены'), watch=('Відео', 'Видео'),
 cat_h=('Що ми робимо', 'Что мы делаем'),
 cat_p=('Обирайте напрямок або перегляньте всі послуги. Ціни вказані як «від», остаточну вартість визначає спеціаліст після огляду.',
        'Выбирайте направление или посмотрите все услуги. Цены указаны как «от», окончательную стоимость определяет специалист после осмотра.'),
 pr_h=('Ціни', 'Цены'), pr_p=('Ціни вказані як «від». Остаточну вартість визначає спеціаліст після огляду, залежно від зони, обсягу та плану. Оплата: [ЗАПОВНИТИ].',
        'Цены указаны как «от». Окончательную стоимость определяет специалист после осмотра, в зависимости от зоны, объёма и плана. Оплата: [ЗАПОЛНИТЬ].'),
)

def B(t, block=False, q='"'):
    tag = 'div' if block else 'span'
    return f'<{tag} class={q}l-uk{q}>{t[0]}</{tag}><{tag} class={q}l-ru{q}>{t[1]}</{tag}>'

def fill(t, block=False):
    """Якщо текст виглядає як плейсхолдер [ ... ], підсвічуємо."""
    if t is None:
        return ''
    if t[0].startswith('['):
        return B((f'<span class="fill">{t[0]}</span>', f'<span class="fill">{t[1]}</span>'), block)
    return B(t, block)

def svg(name, cls='ico'):
    return f'<svg class="{cls}" viewBox="0 0 34 34" aria-hidden="true">{ICONS[name]}</svg>'

def price_text(s):
    if s['price'] is None:
        return B((f'від <span class="fill">[ЦІНА]</span> ₴', f'от <span class="fill">[ЦЕНА]</span> ₴'))
    return B((f'від {s["price"]} ₴', f'от {s["price"]} ₴'))

def card(s, extra=''):
    media = (f'<img class="ph-img" src="{{{{A}}}}assets/{"video/massage-2.webp" if s["slug"]=="masazh" else "img/"+s["img"]+".webp"}" alt="" width="900" height="1125" loading="lazy" decoding="async">'
             if s['img'] else f'<div class="pvis pvis-sm">{svg(s["icon"], "pvis-ico")}</div>')
    cat = next(n for c, n in CATS if c == s['cat'])
    return (f'<a class="card rv scard" data-cat="{s["cat"]}" href="{{{{P}}}}poslugy/{s["slug"]}.html"{extra}><div class="frame">{media}</div>'
            f'<div class="tagl" style="margin-top:16px">{B(cat)}</div><h3>{B(s["name"])}</h3><p class="cardp">{B(s["short"])}</p>'
            f'<div class="meta"><span>{price_text(s)}</span><i>→</i></div></a>')

def head(title, desc, extra=''):
    return (f'<!doctype html>\n<html lang="uk" class="no-js">\n<head>\n<!--#include head-->\n<title>{B(title)}</title>\n'
            f'<meta name="description" content="{B(desc)}">\n<meta property="og:title" content="{B(title)}">\n<meta property="og:description" content="{B(desc)}">\n{extra}</head>\n<body>\n<!--#include header-->\n')

TAIL = '\n<!--#include footer-->\n<!--#include scripts-->\n</body>\n</html>\n'

def cta_band():
    return (f'<section class="section dark ctaband"><div class="wrap"><h2>{B(UI["cta_t"])}</h2><p class="lead">{B(UI["cta_p"])}</p>'
            f'<div class="actions"><a class="btn btn-primary" href="{{{{P}}}}kontakty.html#zapys" data-ga-event="click_book">{B(UI["book"])}</a>'
            f'<a class="btn btn-ghost" data-contact="telegram" href="#" hidden>Telegram</a><a class="btn btn-ghost" data-contact="whatsapp" href="#" hidden>WhatsApp</a></div></div></section>')

def service_page(s, i):
    name, cat = s['name'], next(n for c, n in CATS if c == s['cat'])
    from urllib.parse import quote
    book = f'{{{{P}}}}kontakty.html?service={quote(s["form"])}#zapys'
    visual = (f'<img src="{{{{A}}}}assets/{"video/massage-2.webp" if s["slug"]=="masazh" else "img/"+s["img"]+".webp"}" alt="" width="900" height="1125" decoding="async" fetchpriority="high">'
              if s['img'] else f'<div class="pvis">{svg(s["icon"], "pvis-ico")}<span class="pvis-l">[ФОТО]</span></div>')
    out = [head((f'{name[0]} в Одесі — Potapova Cosmetology', f'{name[1]} в Одессе — Potapova Cosmetology'), s['lead'],
                '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","name":"' + B(name, q="'") + '","provider":{"@type":"Organization","name":"Potapova Cosmetology"},"areaServed":"Одеса"}</script>\n')]
    out.append(f'<main id="main">\n<section class="phero dark"><div class="wrap phero-grid"><div>'
               f'<nav class="crumbs" aria-label="Breadcrumb"><a href="{{{{P}}}}index.html">{B(UI["home"])}</a><span>/</span><a href="{{{{P}}}}poslugy/index.html">{B(UI["services"])}</a><span>/</span>{B(cat)}</nav>'
               f'<h1>{B(name)}</h1><p class="lead">{B(s["lead"])}</p>'
               f'<div class="actions"><a class="btn btn-primary" href="{book}" data-ga-event="click_book">{B(UI["book"])}</a><a class="btn btn-ghost" href="#process">{B(UI["process"])}</a></div></div>'
               f'<div class="phero-vis">{visual}</div></div></section>')
    # факти
    facts = ''
    for label, val in s['facts']:
        v = price_text(s) if val is None else fill(val)
        facts += f'<div><small>{B(label)}</small><b>{v}</b></div>'
    out.append(f'<section class="facts-band"><div class="wrap"><div class="facts">{facts}</div></div></section>')
    # для кого + технологія
    whom = ''.join(f'<li>{B(w)}</li>' for w in s['whom'])
    tech = f'<div class="two-col-b"><h3>{B(UI["tech"])}</h3><p>{fill(s["tech"], False)}</p></div>' if s.get('tech') else ''
    out.append(f'<section class="section"><div class="wrap two-col"><div><div class="eyebrow"><b>01</b> {B(UI["for_whom"])}</div><h2>{B(UI["for_whom"])}</h2></div><div><ul class="ticks">{whom}</ul>{tech}</div></div></section>')
    # кроки
    steps = ''.join(f'<div data-n="{n+1:02d}"><h3>{B(t)}</h3><p>{fill(d)}</p></div>' for n, (t, d) in enumerate(s['steps']))
    out.append(f'<section class="section sand" id="process"><div class="wrap"><div class="eyebrow"><b>02</b> {B(UI["process"])}</div><h2>{B(UI["process"])}</h2><div class="steps">{steps}</div></div></section>')
    # масаж: ціни + відео
    if s.get('price_rows'):
        rows = ''.join(f'<li><span>{B(n)}</span><b>{p} ₴</b></li>' for n, p in s['price_rows'])
        out.append(f'<section class="section"><div class="wrap two-col"><div><div class="eyebrow"><b>03</b> {B(UI["prices"])}</div><h2>{B(UI["pl_h"])}</h2><ul class="pricelist">{rows}</ul></div>'
                   f'<div class="vids vids-2"><video data-lazy muted loop playsinline preload="none" poster="{{{{A}}}}assets/video/massage-2.webp" aria-label="Масаж"><source src="{{{{A}}}}assets/video/massage-2.mp4" type="video/mp4"></video>'
                   f'<video data-lazy muted loop playsinline preload="none" poster="{{{{A}}}}assets/video/massage-1.webp" aria-label="Масаж"><source src="{{{{A}}}}assets/video/massage-1.mp4" type="video/mp4"></video></div></div></section>')
    # протипоказання
    contra = ''.join(f'<li>{B(c)}</li>' for c in s['contra'])
    out.append(f'<section class="section {"" if s.get("price_rows") else "sand"}"><div class="wrap two-col"><div><div class="eyebrow"><b>04</b> {B(UI["contra"])}</div><h2>{B(UI["contra"])}</h2><p class="lead">{B(UI["contra_p"])}</p></div>'
               f'<div><ul class="ticks warn">{contra}</ul><p class="disc" style="text-align:left;margin-top:24px">{B(DISCLAIMER)}</p></div></div></section>')
    # ціна
    note = f'<p class="lead">{B(s["price_note"])}</p>' if s.get('price_note') else ''
    out.append(f'<section class="section dark"><div class="wrap two-col"><div><div class="eyebrow"><b>05</b> {B(UI["price"])}</div><h2>{price_text(s)}</h2>{note}</div>'
               f'<div class="actions" style="align-self:end"><a class="btn btn-primary" href="{book}" data-ga-event="click_book">{B(UI["book"])}</a><a class="btn btn-ghost" href="{{{{P}}}}tsiny.html">{B(UI["see_prices"])}</a></div></div></section>')
    # FAQ
    faq = ''.join(f'<details><summary>{B(q)}</summary><p>{fill(a)}</p></details>' for q, a in s['faq'])
    out.append(f'<section class="section"><div class="wrap"><div class="eyebrow"><b>06</b> FAQ</div><h2 style="margin-bottom:40px">{B(UI["faq"])}</h2><div class="faq">{faq}</div>'
               + (f'<p style="margin-top:32px"><a class="link" href="{{{{P}}}}zhurnal/{s["article"]}.html">{B(UI["article"])}</a></p>' if s.get('article') else '') + '</div></section>')
    # схожі
    others = [SERVICES[(i + k) % len(SERVICES)] for k in (1, 2, 3)]
    out.append(f'<section class="section sand"><div class="wrap"><div class="head"><div><h2>{B(UI["related"])}</h2></div><a class="link" href="{{{{P}}}}poslugy/index.html">{B(UI["all_services"])}</a></div><div class="grid3">{"".join(card(o) for o in others)}</div></div></section>')
    out.append(cta_band() + '\n</main>' + TAIL)
    # JSON-LD FAQ не додаємо для плейсхолдерів
    return ''.join(out)

def catalog():
    chips = f'<button class="chip is-on" type="button" data-filter="all">{B(UI["all_"])}</button>' + ''.join(
        f'<button class="chip" type="button" data-filter="{c}">{B(n)}</button>' for c, n in CATS)
    cards = ''.join(card(s, f' style="--i:{i % 3}"') for i, s in enumerate(SERVICES))
    return (head((f'Послуги — Potapova Cosmetology, Одеса', f'Услуги — Potapova Cosmetology, Одесса'), UI['cat_p']) +
            f'<main id="main">\n<section class="phero dark phero-text"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="{{{{P}}}}index.html">{B(UI["home"])}</a><span>/</span>{B(UI["services"])}</nav>'
            f'<h1>{B(UI["cat_h"])}</h1><p class="lead">{B(UI["cat_p"])}</p></div></section>'
            f'<section class="section"><div class="wrap"><div class="chips" role="group" aria-label="Filter">{chips}</div><div class="grid3 filterable">{cards}</div></div></section>'
            + cta_band() + '\n</main>' + TAIL)

def prices_page():
    blocks = ''
    for c, cn in CATS:
        items = [s for s in SERVICES if s['cat'] == c]
        if not items:
            continue
        rows = ''
        for s in items:
            link = f'<a class="link" href="{{{{P}}}}poslugy/{s["slug"]}.html">{B(s["name"])}</a>'
            if s.get('price_rows'):
                sub = ''.join(f'<li><span>{B(n)}</span><b>{p} ₴</b></li>' for n, p in s['price_rows'])
                rows += f'<div class="prow prow-g"><div class="prow-h">{link}</div><ul class="pricelist">{sub}</ul></div>'
            else:
                rows += f'<div class="prow"><div class="prow-h">{link}</div><b>{price_text(s)}</b></div>'
        blocks += f'<details class="pcat" open><summary>{B(cn)}</summary>{rows}</details>'
    return (head((f'Ціни — Potapova Cosmetology, Одеса', f'Цены — Potapova Cosmetology, Одесса'), UI['pr_p']) +
            f'<main id="main">\n<section class="phero dark phero-text"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="{{{{P}}}}index.html">{B(UI["home"])}</a><span>/</span>{B(UI["prices"])}</nav>'
            f'<h1>{B(UI["pr_h"])}</h1><p class="lead">{fill(UI["pr_p"])}</p></div></section>'
            f'<section class="section"><div class="wrap" style="max-width:900px">{blocks}<p class="disc" style="text-align:left;margin-top:32px">{B(DISCLAIMER)}</p></div></section>'
            + cta_band() + '\n</main>' + TAIL)

def gen_pages():
    pages = {f'poslugy/{s["slug"]}.html': service_page(s, i) for i, s in enumerate(SERVICES)}
    pages['poslugy/index.html'] = catalog()
    pages['tsiny.html'] = prices_page()
    return pages


# ---------- генеровані частини шапки (меню з переліком послуг) ----------
def gen_partials():
    mega = ''
    for c, cn in CATS:
        items = [s for s in SERVICES if s['cat'] == c]
        icon = {'face': 'face', 'inject': 'lips', 'device': 'wave', 'body': 'hand', 'care': 'leaf'}[c]
        links = ''.join(f'<li><a href="{{{{P}}}}poslugy/{s["slug"]}.html">{B(s["name"])}</a></li>' for s in items)
        mega += f'<div class="mcol">{svg(icon)}<h3>{B(cn)}</h3><ul>{links}</ul></div>'
    mega += f'<a class="mall" href="{{{{P}}}}poslugy/index.html">{B(UI["all_services"])} →</a>'
    mobile = ''
    for c, cn in CATS:
        items = [s for s in SERVICES if s['cat'] == c]
        links = ''.join(f'<li><a href="{{{{P}}}}poslugy/{s["slug"]}.html">{B(s["name"])}</a></li>' for s in items)
        mobile += f'<li class="mgroup"><small>{B(cn)}</small><ul>{links}</ul></li>'
    mobile += f'<li class="mgroup"><a class="mall" href="{{{{P}}}}poslugy/index.html">{B(UI["all_services"])} →</a></li>'
    g = GOOGLE
    gfoot = (f'<a class="gfoot" href="{{{{P}}}}vidhuky.html" aria-label="Google"><span class="g-stars" aria-hidden="true">★★★★★</span> <b>{g["rating"]}</b> '
             f'<span>{B((f"на Google · {g["count"]} відгуків", f"на Google · {g["count"]} отзывов"))}</span> →</a>')
    return {'nav_mega': mega, 'nav_mobile': mobile, 'gfoot': gfoot}


def google_card():
    g = GOOGLE
    t = lambda uk, ru: B((uk, ru))
    return (f'<div class="gcard rv"><div class="g-main"><span class="g-logo">Google</span><div class="g-row"><b class="g-num">{g["rating"]}</b>'
            f'<div class="g-meta"><span class="g-stars" role="img" aria-label="{g["rating"]} / 5">★★★★★</span>'
            f'<small>{B((f"{g['count']} відгуків", f"{g['count']} отзывов"))}</small></div></div></div>'
            f'<div class="actions" style="margin-top:0"><a class="btn btn-primary" href="{g["reviews_url"]}" target="_blank" rel="noopener noreferrer" data-ga-event="click_google_reviews">{t("Читати відгуки на Google", "Читать отзывы на Google")}</a>'
            f'<a class="btn btn-ghost" href="{g["write_url"]}" target="_blank" rel="noopener noreferrer" data-ga-event="click_google_write">{t("Залишити відгук на Google", "Оставить отзыв на Google")}</a></div>'
            f'<p class="disc" style="text-align:left;margin:0">{B((f"Рейтинг за даними Google Maps, {g["asof"][0]}. Відгуки пишуть клієнти на Google, ми їх не редагуємо.", f"Рейтинг по данным Google Maps, {g["asof"][1]}. Отзывы пишут клиенты на Google, мы их не редактируем."))}</p></div>')

def google_strip():
    g = GOOGLE
    return (f'<section class="gstrip"><div class="wrap"><a href="{{{{P}}}}vidhuky.html" class="gstrip-a"><span class="g-stars" aria-hidden="true">★★★★★</span><b>{g["rating"]}</b>'
            f'<span>{B((f"на Google · {g["count"]} відгуків", f"на Google · {g["count"]} отзывов"))}</span><span class="gstrip-go">{B(("Відгуки", "Отзывы"))} →</span></a></div></section>')


def google_reviews():
    """Відгуки Google: перші REVIEWS_PAGE_SIZE видно, решта за кнопкою «Далі»; коли ховати нічого, кнопка веде на всі відгуки в Google."""
    g = GOOGLE
    cards = ''
    for i, r in enumerate(GOOGLE_REVIEWS):
        hid = ' hidden data-more' if i >= REVIEWS_PAGE_SIZE else ''
        tail = '…' if r.get('trunc') else ''
        more = (f'<a class="rmore" href="{g["reviews_url"]}" target="_blank" rel="noopener noreferrer">{B(("Читати повністю на Google", "Читать полностью на Google"))}</a>') if r.get('trunc') else ''
        cards += (f'<figure class="review-card"{hid}><div class="stars" role="img" aria-label="{r["rating"]} / 5">{"★" * r["rating"]}</div>'
                  f'<blockquote lang="ru">«{r["text"]}{tail}»</blockquote>{more}'
                  f'<figcaption><span class="ini">{r["name"][0]}</span><span><span>{r["name"]}</span><span>Google · {B(r["when"])}</span></span></figcaption></figure>')
    hidden_n = max(0, len(GOOGLE_REVIEWS) - REVIEWS_PAGE_SIZE)
    nxt = (f'<button class="btn btn-ghost" type="button" data-more-btn data-step="{REVIEWS_PAGE_SIZE}"{"" if hidden_n else " hidden"}>{B(("Далі", "Далее"))}</button>'
           f'<a class="btn btn-ghost" data-more-link href="{g["reviews_url"]}" target="_blank" rel="noopener noreferrer" data-ga-event="click_google_reviews"{" hidden" if hidden_n else ""}>{B((f"Далі: усі {g["count"]} відгуків на Google →", f"Далее: все {g["count"]} отзывов на Google →"))}</a>')
    return (f'<div class="rev-grid" data-more-list>{cards}</div><div class="actions rev-next">{nxt}</div>'
            f'<p class="disc" style="text-align:left">{B(("Відгуки наведені з Google в оригіналі (мовою авторів). Ми їх не редагуємо.", "Отзывы приведены из Google в оригинале (на языке авторов). Мы их не редактируем."))}</p>')
