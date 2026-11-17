"""Одноразове розміщення матеріалів у index.html (історія: див. git)."""
import re
p = 'index.html'
s = open(p, encoding='utf-8').read()

def im(f, alt, w, h, cls='ph-img'):
    return f'<img class="{cls}" src="assets/img/{f}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">'

s = s.replace('<link rel="stylesheet" href="css/styles.css">',
              '<link rel="stylesheet" href="css/styles.css">\n<link rel="stylesheet" href="css/media.css">\n<link rel="icon" type="image/png" href="assets/favicon.png">\n<meta property="og:image" content="https://[ДОМЕН]/assets/img/og.jpg">', 1)
s = s.replace('<a class="logo" href="/" aria-label="Potapova Cosmetology, на головну">Potapova<small>Cosmetology</small></a>',
              '<a class="logo" href="/" aria-label="Potapova Cosmetology, на головну"><img class="bear" src="assets/img/bear.webp" alt="" width="62" height="34"><span>Potapova<small>Cosmetology</small></span></a>', 1)
s = re.sub(r'<div class="hero-media ph"[^>]*></div>',
           '<video class="hero-media" autoplay muted loop playsinline preload="auto" poster="assets/video/hero.webp" aria-hidden="true"><source src="assets/video/hero.mp4" type="video/mp4"></video>', s, count=1)

rep = {
 '[ФОТО] чистка': im('dmk-cleanser', 'Очищення DMK', 900, 1200),
 '[ФОТО] мікротоки': im('shelf-hydraderm', 'Косметика Hydraderm', 1000, 1500),
 '[ФОТО] масаж': '<img class="ph-img" src="assets/video/massage-2.webp" alt="Масаж" width="720" height="1280" loading="lazy" decoding="async">',
 '[ФОТО] DMK': im('dmk', 'Ферментні маски DMK', 1000, 1500),
}
for k, v in rep.items():
    s = s.replace(f'<div class="ph" data-label="{k}"></div>', v, 1)

s = s.replace('<div class="ph light rv" data-label="[ФОТО] портрет лікаря" role="img" aria-label="Портрет Анастасії Потапової"></div>',
              '<img class="rv" src="assets/img/doctor.webp" alt="Портрет у кабінеті Potapova Cosmetology" width="1200" height="1800" loading="lazy" decoding="async">', 1)

tiles = [('decor', 1000, 1500), ('shelf-back', 1000, 1500), ('originals', 1000, 1500), ('image-peel', 900, 1200)]
it = iter(tiles)
def tile(m):
    f, w, h = next(it)
    return f'<img class="ph" src="assets/img/{f}.webp" alt="" width="{w}" height="{h}" loading="lazy" decoding="async">'
a = s.index('Світ Potapova</div>'); b = s.index('</section>', a)
s = s[:a] + re.sub(r'<div class="ph" data-label="\[ФОТО\]"></div>', tile, s[a:b]) + s[b:]

old = s[s.index('<div class="brands"'):s.index('<a class="link" href="#">Усі технології</a>')]
fig = lambda f, alt, w, h, t, sub, i=0: f'<figure class="rv"{f" style=\"--i:{i}\"" if i else ""}><img src="assets/img/{f}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"><figcaption>{t}<small>{sub}</small></figcaption></figure>'
newb = ('<div class="brands" aria-label="Бренди-партнери"><span>DMK</span><span>IMAGE Skincare</span><span>ZO Skin Health</span><span>Rejuran</span><span>Thalgo</span><span>Guinot</span><span>Hydraderm</span></div>\n    <div class="brandgrid">\n      '
        + '\n      '.join([
            fig('dmk-cleanser', 'DMK MD Enbioment Cleanser', 900, 1200, 'DMK', 'Ферментотерапія та догляд'),
            fig('image-iluma', 'IMAGE Skincare', 900, 1200, 'IMAGE Skincare', 'Anti-age та пілінги', 1),
            fig('zo', 'ZO Skin Health', 1000, 1000, 'ZO Skin Health', 'Лікарська косметика', 2),
            fig('thalgo', 'Thalgo Hyalu-Procollagène', 626, 624, 'Thalgo', 'Морський догляд'),
            fig('guinot', 'Guinot', 1000, 679, 'Guinot', 'Професійний догляд', 1),
            '<figure class="rv" style="--i:2"><video class="vid" data-lazy muted loop playsinline preload="none" poster="assets/video/rejuran.webp" aria-label="Rejuran"><source src="assets/video/rejuran.mp4" type="video/mp4"></video><figcaption>Rejuran<small>Skinglow, полінуклеотиди</small></figcaption></figure>',
        ]) + '\n    </div>\n    ')
s = s.replace(old, newb, 1)

gal = ''.join(f'\n      <img src="assets/img/{f}.webp" alt="" width="1000" height="1500" loading="lazy" decoding="async">' for f in ['logo-wall', 'team', 'doctor-shelf', 'decor', 'shelf-back', 'doctor-sit'])
s = s.replace('<a class="link" href="#">Усі технології</a>',
              '<a class="link" href="#">Усі технології</a>\n    <div class="eyebrow" style="margin-top:96px"><b>·</b> Простір клініки</div>\n    <div class="rail gal">' + gal + '\n    </div>', 1)

s = s.replace('      </div>\n    </div>\n  </div>\n</section>\n\n<!-- 5. ЛІКАР',
              '      </div>\n      <div class="vids">\n        <video data-lazy muted loop playsinline preload="none" poster="assets/video/massage-2.webp" aria-label="Масаж спини"><source src="assets/video/massage-2.mp4" type="video/mp4"></video>\n        <video data-lazy muted loop playsinline preload="none" poster="assets/video/massage-1.webp" aria-label="Масаж тіла"><source src="assets/video/massage-1.mp4" type="video/mp4"></video>\n      </div>\n    </div>\n  </div>\n</section>\n\n<!-- 5. ЛІКАР', 1)

j = iter([im('dmk', 'Ферментні маски DMK', 1000, 1500), im('shelf-hydraderm', 'Косметика Hydraderm', 1000, 1500)])
def jr(m):
    return next(j, m.group(0))
a = s.index('id="zhurnal"'); b = s.index('</section>', a)
s = s[:a] + re.sub(r'<div class="ph" data-label="\[ФОТО\]"></div>', jr, s[a:b]) + s[b:]

s = s.replace('<p class="lead" style="margin-top:32px">Адреса:',
              '<img class="consult-img" src="assets/img/consult.webp" alt="Консультація в кабінеті" width="1200" height="1800" loading="lazy" decoding="async">\n      <p class="lead" style="margin-top:32px">Адреса:', 1)
s = s.replace('<div class="logo" style="color:#fff">Potapova<small>Cosmetology</small></div>',
              '<img class="flogo" src="assets/img/logo-white.png" alt="Potapova Cosmetology" width="800" height="334" loading="lazy">', 1)
open(p, 'w', encoding='utf-8').write(s)
print('залишилось плейсхолдерів фото:', re.findall(r'data-label="([^"]+)"', s))
