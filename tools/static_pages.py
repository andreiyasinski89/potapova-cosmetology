"""Головна та інформаційні сторінки (двомовні), які генеруються так само, як сторінки послуг."""
from content import SERVICES, CATS, DISCLAIMER, by_slug
from pages import B, fill, svg, head, TAIL, cta_band, card, UI, price_text, google_card, google_strip, google_reviews

PP, AA = '{{P}}', '{{A}}'

def ph(t):  # плейсхолдер у двох мовах, підсвічений
    return B((f'<span class="fill">{t[0]}</span>', f'<span class="fill">{t[1]}</span>'))

def crumbs(here):
    return f'<nav class="crumbs" aria-label="Breadcrumb"><a href="{PP}index.html">{B(UI["home"])}</a><span>/</span>{B(here)}</nav>'

def phero(here, title, lead=None, extra=''):
    lead_html = f'<p class="lead">{B(lead)}</p>' if lead else ''
    return f'<section class="phero dark phero-text"><div class="wrap">{crumbs(here)}<h1>{B(title)}</h1>{lead_html}{extra}</div></section>'

def page(title, desc, body, extra_head=''):
    return head(title, desc, extra_head) + f'<main id="main">\n{body}\n' + cta_band() + '\n</main>' + TAIL

IMG = lambda f, alt='', w=1000, h=1500, cls='': f'<img{" class=" + chr(34) + cls + chr(34) if cls else ""} src="{AA}assets/img/{f}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">'

# ---------------------------------------------------------------- Про нас
def pro_nas():
    vals = [(('Точність', 'Точность'), ('Спочатку діагностика, потім план. Не пропонуємо зайвого й не обіцяємо чудес.', 'Сначала диагностика, потом план. Не предлагаем лишнего и не обещаем чудес.')),
            (('Природність', 'Естественность'), ('Підкреслюємо, а не змінюємо. Мінімально необхідне втручання заради результату, який виглядає як ви.', 'Подчёркиваем, а не меняем. Минимально необходимое вмешательство ради результата, который выглядит как вы.')),
            (('Безпека', 'Безопасность'), ('Стерильність, сертифіковані препарати та чесна розмова про протипоказання до кожної процедури.', 'Стерильность, сертифицированные препараты и честный разговор о противопоказаниях к каждой процедуре.'))]
    v = ''.join(f'<div class="rv" style="--i:{i}"><h3>{B(t)}</h3><p>{B(d)}</p></div>' for i, (t, d) in enumerate(vals))
    proc = [(('Консультація', 'Консультация'), ('Огляд, розмова про цілі та історію здоров\'я. Без тиску й обов\'язків.', 'Осмотр, разговор о целях и истории здоровья. Без давления и обязательств.')),
            (('План', 'План'), ('Пояснюємо, що, навіщо та в якій послідовності. Називаємо орієнтовну вартість.', 'Объясняем, что, зачем и в какой последовательности. Называем ориентировочную стоимость.')),
            (('Процедура та догляд', 'Процедура и уход'), ('Проводимо процедуру, даємо рекомендації й залишаємося на зв\'язку після візиту.', 'Проводим процедуру, даём рекомендации и остаёмся на связи после визита.'))]
    pr = ''.join(f'<div class="rv" style="--i:{i}"><h3>{B(t)}</h3><p>{B(d)}</p></div>' for i, (t, d) in enumerate(proc))
    gal = ''.join([IMG('logo-wall-wide', '', 1600, 1400, 'wide'), IMG('decor'), IMG('team'), IMG('doctor-shelf'), IMG('shelf-back'), IMG('doctor-sit')])
    body = (phero(('Про клініку', 'О клинике'), ('Не змінюємо. Підкреслюємо.', 'Не меняем. Подчёркиваем.'),
                  ('Potapova Cosmetology: косметологія та ін\'єкційна естетика в Одесі. Ми працюємо тихо, точно й без поспіху.', 'Potapova Cosmetology: косметология и инъекционная эстетика в Одессе. Мы работаем тихо, точно и без спешки.')) +
        f'<section class="section"><div class="wrap"><div class="eyebrow"><b>01</b> {B(("Принципи", "Принципы"))}</div><h2>{B(("Три слова, на яких стоїть клініка", "Три слова, на которых стоит клиника"))}</h2><div class="values">{v}</div>'
        f'<div class="big-num"><div><b class="fill">[N]</b><span>{B(("років практики", "лет практики"))}</span></div><div><b class="fill">[N]</b><span>{B(("проведених процедур", "проведённых процедур"))}</span></div><div><b class="fill">[N]</b><span>{B(("спеціалістів у команді", "специалистов в команде"))}</span></div></div></div></section>'
        f'<section class="section sand"><div class="wrap"><div class="eyebrow"><b>02</b> {B(("Як ми працюємо", "Как мы работаем"))}</div><h2>{B(("Від першої розмови до догляду вдома", "От первого разговора до ухода дома"))}</h2><div class="proc">{pr}</div></div></section>'
        f'<section class="section"><div class="wrap"><div class="eyebrow"><b>03</b> {B(("Простір", "Пространство"))}</div><h2 style="margin-bottom:40px">{B(("Кабінет, у якому спокійно", "Кабинет, в котором спокойно"))}</h2><div class="gal-grid">{gal}</div></div></section>'
        f'<section class="section dark"><div class="wrap two-col"><div><div class="eyebrow"><b>04</b> {B(("Безпека", "Безопасность"))}</div><h2>{B(("Стерильність і оригінальні препарати", "Стерильность и оригинальные препараты"))}</h2></div>'
        f'<div><ul class="ticks"><li>{B(("Одноразові розхідники та обробка інструментів за протоколом", "Одноразовые расходники и обработка инструментов по протоколу"))}</li><li>{B(("Сертифіковані оригінальні препарати від перевірених виробників", "Сертифицированные оригинальные препараты от проверенных производителей"))}</li><li>{B(("Інформована згода й анкета перед кожною процедурою", "Информированное согласие и анкета перед каждой процедурой"))}</li><li>{ph(("підтвердити пункти з клієнтом, додати ліцензію та документи", "подтвердить пункты с клиентом, добавить лицензию и документы"))}</li></ul>'
        f'<div class="actions"><a class="btn btn-ghost" href="{PP}tekhnolohii.html">{B(("Технології та бренди", "Технологии и бренды"))}</a><a class="btn btn-ghost" href="{PP}komanda.html">{B(("Наша команда", "Наша команда"))}</a></div></div></div></section>')
    return page(('Про клініку — Potapova Cosmetology, Одеса', 'О клинике — Potapova Cosmetology, Одесса'),
                ('Potapova Cosmetology: косметологія в Одесі, де не змінюють, а підкреслюють красу. Принципи, процес роботи, простір клініки.', 'Potapova Cosmetology: косметология в Одессе, где не меняют, а подчёркивают красоту. Принципы, процесс работы, пространство клиники.'), body)

# ---------------------------------------------------------------- Команда
def komanda():
    roles = [(('Косметолог', 'Косметолог'), ('Фото спеціаліста', 'Фото специалиста'), ('[ЗАПОВНИТИ: напрямки, освіта, сертифікати]', '[ЗАПОЛНИТЬ: направления, образование, сертификаты]')),
             (('Косметолог', 'Косметолог'), ('Фото спеціаліста', 'Фото специалиста'), ('[ЗАПОВНИТИ: напрямки, освіта, сертифікати]', '[ЗАПОЛНИТЬ: направления, образование, сертификаты]')),
             (('Майстер лазерної епіляції', 'Мастер лазерной эпиляции'), ('Фото майстра', 'Фото мастера'), ('[ЗАПОВНИТИ: досвід, апарати, сертифікати]', '[ЗАПОЛНИТЬ: опыт, аппараты, сертификаты]')),
             (('Адміністратор', 'Администратор'), ('Фото адміністратора', 'Фото администратора'), ('Допоможе обрати зручний час, відповість на питання про запис і підготовку до візиту.', 'Поможет выбрать удобное время, ответит на вопросы о записи и подготовке к визиту.'))]
    cards = ''.join(f'<article class="member rv" style="--i:{i}"><div class="ph light" data-label="[ФОТО]" role="img" aria-label="{B(al)}"></div><h4>{ph(("Ім\'я Прізвище", "Имя Фамилия")) if i < 3 else ph(("Ім\'я", "Имя"))}</h4><p class="role">{B(r)}</p><p class="bio">{fill(bio)}</p></article>'
                    for i, (r, al, bio) in enumerate(roles))
    body = (phero(('Команда', 'Команда'), ('Люди, які працюють з вашою шкірою', 'Люди, которые работают с вашей кожей'),
                  ('Кожен спеціаліст відповідає за свій напрямок. А вам не потрібно вгадувати, до кого йти: адміністратор допоможе обрати.', 'Каждый специалист отвечает за своё направление. А вам не нужно угадывать, к кому идти: администратор поможет выбрать.')) +
        f'<section class="section sand"><div class="wrap teaser-split"><img class="rv" src="{AA}assets/img/doctor.webp" alt="Анастасія Потапова" width="1200" height="1800" loading="lazy" decoding="async">'
        f'<div class="rv" style="--i:1"><div class="eyebrow"><b>01</b> {B(("Засновниця", "Основательница"))}</div><h2>{B(("Анастасія Потапова", "Анастасия Потапова"))}</h2><p class="role">{B(("Засновниця Potapova Cosmetology", "Основательница Potapova Cosmetology"))}</p>'
        f'<p class="lead">{B(("Принцип клініки: підкреслювати природну красу, а не змінювати обличчя. Ми працюємо командою, і кожен спеціаліст відповідає за свій напрямок.", "Принцип клиники: подчёркивать естественную красоту, а не менять лицо. Мы работаем командой, и каждый специалист отвечает за своё направление."))} {ph(("освіта, спеціальність, сертифікати Анастасії", "образование, специальность, сертификаты Анастасии"))}</p>'
        f'<ul class="principles"><li><b>I</b><span>{B(("Спочатку діагностика, потім план.", "Сначала диагностика, потом план."))}</span></li><li><b>II</b><span>{B(("Мінімально необхідне втручання.", "Минимально необходимое вмешательство."))}</span></li><li><b>III</b><span>{B(("Стерильність і сертифіковані препарати.", "Стерильность и сертифицированные препараты."))}</span></li></ul></div></div></section>'
        f'<section class="section"><div class="wrap"><div class="eyebrow"><b>02</b> {B(("Спеціалісти", "Специалисты"))}</div><h2 style="margin-bottom:40px">{B(("Команда клініки", "Команда клиники"))}</h2><div class="team">{cards}</div></div></section>')
    return page(('Команда — Potapova Cosmetology, Одеса', 'Команда — Potapova Cosmetology, Одесса'),
                ('Засновниця Анастасія Потапова, косметологи, майстер лазерної епіляції та адміністратор Potapova Cosmetology.', 'Основательница Анастасия Потапова, косметологи, мастер лазерной эпиляции и администратор Potapova Cosmetology.'), body)

# ---------------------------------------------------------------- Результати
def rezultaty():
    def ba(i):
        return (f'<div class="rv" style="--i:{i}"><div class="ba"><div class="ph" data-label="[ФОТО] до"></div><div class="ph after" data-label="[ФОТО] після"></div><span class="tag" style="left:16px">{B(("До", "До"))}</span><span class="tag" style="right:16px">{B(("Після", "После"))}</span>'
                f'<div class="handle"></div><input type="range" min="0" max="100" value="50" aria-label="{B(("Порівняти до і після", "Сравнить до и после"))}"></div>'
                f'<p class="disc" style="text-align:left;margin-top:12px">{ph(("процедура, кількість візитів, дата", "процедура, количество визитов, дата"))}</p></div>')
    rules = [(('Лише зі згодою', 'Только с согласия'), ('Кожне фото публікуємо за письмовою згодою пацієнта.', 'Каждое фото публикуем с письменного согласия пациента.')),
             (('Без надмірної ретуші', 'Без чрезмерной ретуши'), ('Однакове освітлення та ракурс до і після. Не обробляємо фото.', 'Одинаковое освещение и ракурс до и после. Не обрабатываем фото.')),
             (('Результат індивідуальний', 'Результат индивидуален'), ('Те, що вийшло в одного пацієнта, не гарантує такого самого в іншого.', 'То, что получилось у одного пациента, не гарантирует такого же у другого.'))]
    pr = ''.join(f'<div class="rv" style="--i:{i}"><h3>{B(t)}</h3><p>{B(d)}</p></div>' for i, (t, d) in enumerate(rules))
    body = (phero(('Результати', 'Результаты'), ('До та після', 'До и после'),
                  ('Реальні роботи без фільтрів. Тягніть повзунок, щоб порівняти.', 'Реальные работы без фильтров. Двигайте ползунок, чтобы сравнить.')) +
        f'<section class="section"><div class="wrap"><div class="res-grid">{ba(0)}{ba(1)}</div><p class="disc">{B(("Індивідуальний досвід, результат може відрізнятися. Публікація: за письмовою згодою пацієнта, без надмірної ретуші.", "Индивидуальный опыт, результат может отличаться. Публикация: с письменного согласия пациента, без чрезмерной ретуши."))}</p></div></section>'
        f'<section class="section sand"><div class="wrap"><div class="eyebrow"><b>·</b> {B(("Наші правила", "Наши правила"))}</div><h2>{B(("Як ми показуємо результати", "Как мы показываем результаты"))}</h2><div class="proc">{pr}</div></div></section>')
    return page(('Результати — Potapova Cosmetology, Одеса', 'Результаты — Potapova Cosmetology, Одесса'),
                ('Фото до і після процедур у Potapova Cosmetology: лише за згодою пацієнтів, без надмірної ретуші.', 'Фото до и после процедур в Potapova Cosmetology: только с согласия пациентов, без чрезмерной ретуши.'), body)

# ---------------------------------------------------------------- Технології та бренди
def tekhnolohii():
    B_ = [
     ('DMK', 'dmk', ('Ферментотерапія та догляд', 'Ферментотерапия и уход'), ('Американський метод ферментотерапії від Danné Montague-King: професійні ферментні маски та домашній догляд. Основа нашої роботи з тьмяною, «втомленою» шкірою.', 'Американский метод ферментотерапии от Danné Montague-King: профессиональные ферментные маски и домашний уход. Основа нашей работы с тусклой, «уставшей» кожей.'), 'fermentoterapiya-dmk'),
     ('Hydraderm', 'shelf-hydraderm', ('Мікрострумова терапія', 'Микротоковая терапия'), ('Апаратна мікрострумова терапія для тонусу, контуру й свіжості обличчя без інвазивних методик.', 'Аппаратная микротоковая терапия для тонуса, контура и свежести лица без инвазивных методик.'), 'mikrostrumy-hydraderm'),
     ('IMAGE Skincare', 'image-iluma', ('Anti-age та пілінги', 'Anti-age и пилинги'), ('Американська професійна лінія для догляду та пілінгів. Підбираємо засоби під конкретну шкіру та поєднуємо з домашнім доглядом.', 'Американская профессиональная линия для ухода и пилингов. Подбираем средства под конкретную кожу и сочетаем с домашним уходом.'), 'domashniy-doglyad'),
     ('ZO Skin Health', 'zo', ('Лікарська косметика', 'Врачебная косметика'), ('Лінія Zein Obagi для корекції стану шкіри під наглядом спеціаліста: від очищення до нічного відновлення.', 'Линия Zein Obagi для коррекции состояния кожи под наблюдением специалиста: от очищения до ночного восстановления.'), 'domashniy-doglyad'),
     ('Thalgo', 'thalgo', ('Морський догляд', 'Морской уход'), ('Французький бренд морської косметики: зволоження та ефект ліфтингу у професійних програмах і для догляду вдома.', 'Французский бренд морской косметики: увлажнение и эффект лифтинга в профессиональных программах и для ухода дома.'), 'domashniy-doglyad'),
     ('Guinot', 'guinot', ('Професійний догляд', 'Профессиональный уход'), ('Французький професійний догляд: від очищення й зволоження до програм проти ознак старіння.', 'Французский профессиональный уход: от очищения и увлажнения до программ против признаков старения.'), 'domashniy-doglyad'),
    ]
    rows = ''
    for name, img, tag, text, svc in B_:
        rows += (f'<div class="brow rv"><div class="brow-m"><img src="{AA}assets/img/{img}.webp" alt="{name}" width="900" height="1125" loading="lazy" decoding="async"></div>'
                 f'<div><div class="tagl">{B(tag)}</div><h3>{name}</h3><p>{B(text)}</p><p><a class="link" href="{PP}poslugy/{svc}.html">{B(("Де застосовуємо", "Где применяем"))}</a></p></div></div>')
    rows += (f'<div class="brow rv"><div class="brow-m"><video class="vid" data-lazy muted loop playsinline preload="none" poster="{AA}assets/video/rejuran.webp" aria-label="Rejuran"><source src="{AA}assets/video/rejuran.mp4" type="video/mp4"></video></div>'
             f'<div><div class="tagl">{B(("Skinglow", "Skinglow"))}</div><h3>Rejuran</h3><p>{B(("Корейський бренд, у якому ми працюємо з лінійкою для сяяння та захисту шкіри, зокрема Skinglow Cushion SPF50+.", "Корейский бренд, в котором мы работаем с линейкой для сияния и защиты кожи, в том числе Skinglow Cushion SPF50+."))}</p></div></div>')
    rows += (f'<div class="brow rv"><div class="brow-m"><div class="pvis">{svg("wave", "pvis-ico")}<span class="pvis-l">[ФОТО]</span></div></div>'
             f'<div><div class="tagl">STYX · MANTIS</div><h3>STYX, MANTIS</h3><p>{ph(("опис брендів і апаратів", "описание брендов и аппаратов"))}</p></div></div>')
    body = (phero(('Технології та бренди', 'Технологии и бренды'), ('Апарати й препарати, яким ми довіряємо', 'Аппараты и препараты, которым мы доверяем'),
                  ('Працюємо з професійними лініями та апаратами від перевірених виробників. Назва бренду не замінює консультацію: що підійде саме вам, вирішує спеціаліст.', 'Работаем с профессиональными линиями и аппаратами от проверенных производителей. Название бренда не заменяет консультацию: что подойдёт именно вам, решает специалист.')) +
        f'<section class="section"><div class="wrap">{rows}</div></section>')
    return page(('Технології та бренди — Potapova Cosmetology', 'Технологии и бренды — Potapova Cosmetology'),
                ('DMK, Hydraderm, IMAGE Skincare, ZO Skin Health, Thalgo, Guinot, Rejuran: професійні лінії та апарати Potapova Cosmetology.', 'DMK, Hydraderm, IMAGE Skincare, ZO Skin Health, Thalgo, Guinot, Rejuran: профессиональные линии и аппараты Potapova Cosmetology.'), body)

# ---------------------------------------------------------------- Відгуки
def vidhuky():
    def rc(l):
        return (f'<figure class="review-card"><div class="stars" role="img" aria-label="5 / 5">★★★★★</div><blockquote class="fill">«[ВІДГУК ПАЦІЄНТА, ЗА ЗГОДОЮ]»</blockquote>'
                f'<figcaption><span class="ini">{l}</span><span><span>[Ім\'я]</span><span>[Місто]</span></span></figcaption></figure>')
    form = (f'<form class="book" data-review novalidate style="margin-top:40px;max-width:680px"><input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">'
            f'<div class="field"><label for="rv-name">{B(("Ім\'я", "Имя"))}</label><input id="rv-name" name="name" autocomplete="given-name" required></div>'
            f'<div class="field"><label for="rv-city">{B(("Місто (необов\'язково)", "Город (необязательно)"))}</label><input id="rv-city" name="city" autocomplete="address-level2"></div>'
            f'<div class="field"><span class="lbl" style="font-size:var(--fs-small);letter-spacing:.1em;text-transform:uppercase;color:var(--fg-soft)">{B(("Оцінка", "Оценка"))}</span><div class="rating" role="radiogroup" aria-label="Rating">'
            + ''.join(f'<input type="radio" name="rating" id="r{n}" value="{n}"{" checked" if n == 5 else ""}><label for="r{n}" title="{n}">★</label>' for n in (5, 4, 3, 2, 1)) + '</div></div>'
            f'<div class="field"><label for="rv-text">{B(("Ваш відгук", "Ваш отзыв"))}</label><textarea id="rv-text" name="text" rows="5" required minlength="10"></textarea></div>'
            f'<label class="consent"><input type="checkbox" name="consent" required> <span>{B(("Погоджуюся на публікацію відгуку на сайті та на обробку даних згідно з", "Соглашаюсь на публикацию отзыва на сайте и на обработку данных согласно"))} <a class="link" href="{PP}privacy.html">{B(("політикою конфіденційності", "политикой конфиденциальности"))}</a></span></label>'
            f'<p class="form-err" data-err role="alert" hidden>{B(("Вкажіть ім\'я, напишіть відгук (від 10 символів) і підтвердьте згоду.", "Укажите имя, напишите отзыв (от 10 символов) и подтвердите согласие."))}</p>'
            f'<button class="btn btn-primary" type="submit">{B(("Надіслати відгук", "Отправить отзыв"))}</button><p class="ok" data-ok role="status" hidden></p></form>')
    body = (phero(('Відгуки', 'Отзывы'), ('Що кажуть пацієнти', 'Что говорят пациенты'),
                  ('Рейтинг і відгуки наших клієнтів на Google, а також ті, що залишені на сайті.', 'Рейтинг и отзывы наших клиентов на Google, а также те, что оставлены на сайте.')) +
        f'<section class="section" style="padding-bottom:0"><div class="wrap">{google_card()}</div></section>'
        f'<section class="section"><div class="wrap"><div class="eyebrow"><b>01</b> Google</div><h2 style="margin-bottom:40px">{B(("Відгуки клієнтів на Google", "Отзывы клиентов на Google"))}</h2>{google_reviews()}</div></section>'
        f'<section class="section" data-site-reviews hidden><div class="wrap"><div class="eyebrow"><b>02</b> {B(("На сайті", "На сайте"))}</div><h2 style="margin-bottom:40px">{B(("Відгуки, залишені на сайті", "Отзывы, оставленные на сайте"))}</h2>'
        f'<div class="rev-grid" id="revTrack"><figure class="review-card" hidden><div class="stars" role="img" aria-label="5 / 5">★★★★★</div><blockquote></blockquote><figcaption><span class="ini"></span><span><span></span><span></span></span></figcaption></figure></div></div></section>'
        f'<section class="section sand" id="review"><div class="wrap" style="max-width:780px"><div class="eyebrow"><b>·</b> {B(("Відгук", "Отзыв"))}</div><h2>{B(("Поділіться враженням", "Поделитесь впечатлением"))}</h2>'
        f'<p class="lead">{B(("Відгук з\'явиться на сайті після перевірки. Ми публікуємо лише ім\'я, місто й текст, без контактів.", "Отзыв появится на сайте после проверки. Мы публикуем только имя, город и текст, без контактов."))}</p>{form}</div></section>')
    return page(('Відгуки — Potapova Cosmetology, Одеса', 'Отзывы — Potapova Cosmetology, Одесса'),
                ('Відгуки пацієнтів Potapova Cosmetology в Одесі та форма, щоб залишити власний.', 'Отзывы пациентов Potapova Cosmetology в Одессе и форма, чтобы оставить собственный.'), body)

# ---------------------------------------------------------------- Журнал (список)
ARTICLES = [  # slug, послуга, зображення, тег
    ('dmk', 'fermentoterapiya-dmk', 'dmk', ('Догляд', 'Уход')),
    ('hydraderm', 'mikrostrumy-hydraderm', 'shelf-hydraderm', ('Технології', 'Технологии')),
    ('gubi', 'gubi', None, ('Губи', 'Губы')),
    ('masazh', 'masazh', 'massage', ('Масаж', 'Массаж')),
    ('zahar', 'trostynnyi-zahar', None, ('Тіло', 'Тело')),
]
TITLES = {  # назви статей (з src/zhurnal/*.html)
    'dmk': ('Ферментотерапія DMK: чому це не просто маска', 'Ферментотерапия DMK: почему это не просто маска'),
    'hydraderm': ('Мікроструми Hydraderm: чотири ефекти за одну процедуру', 'Микротоки Hydraderm: четыре эффекта за одну процедуру'),
    'gubi': ('М\'яка корекція губ без ефекту «перекачаних»', 'Мягкая коррекция губ без эффекта «перекачанных»'),
    'masazh': ('Час для релаксу: масаж обличчя, голови та стоп', 'Время для релакса: массаж лица, головы и стоп'),
    'zahar': ('Тростинний засмаг: як отримати рівний колір і зберегти його', 'Тростниковый загар: как получить ровный цвет и сохранить его'),
}
def post_card(slug, i=0):
    s, svc, img, tag = next(a for a in ARTICLES if a[0] == slug)
    media = (f'<img class="ph-img" src="{AA}assets/{"video/massage-1.webp" if img == "massage" else "img/" + img + ".webp"}" alt="" width="900" height="600" loading="lazy" decoding="async">' if img
             else f'<div class="pvis pvis-sm">{svg(by_slug(svc)["icon"], "pvis-ico")}</div>')
    return (f'<a class="card post rv" style="--i:{i}" href="{PP}zhurnal/{slug}.html"><div class="frame">{media}</div><div class="tagl" style="margin-top:16px">{B(tag)}</div>'
            f'<h3>{B(TITLES[slug])}</h3><div class="meta"><span>{B(("Читати", "Читать"))}</span><i>→</i></div></a>')

def zhurnal():
    cards = ''.join(post_card(a[0], i % 3) for i, a in enumerate(ARTICLES))
    body = (phero(('Журнал', 'Журнал'), ('Читати', 'Читать'), ('Про процедури та догляд простою мовою: що це, кому підходить і чого очікувати.', 'О процедурах и уходе простым языком: что это, кому подходит и чего ожидать.')) +
            f'<section class="section"><div class="wrap"><div class="grid3">{cards}</div></div></section>')
    return page(('Журнал — Potapova Cosmetology', 'Журнал — Potapova Cosmetology'),
                ('Статті про процедури та догляд від Potapova Cosmetology, Одеса.', 'Статьи о процедурах и уходе от Potapova Cosmetology, Одесса.'), body)

# ---------------------------------------------------------------- Головна
def index():
    feats = ['chystky', 'fermentoterapiya-dmk', 'mikrostrumy-hydraderm', 'gubi', 'lazerna-epilyatsiya', 'masazh']
    cards = ''.join(card(by_slug(s), f' style="--i:{i % 3}"') for i, s in enumerate(feats))
    cat_links = ''.join(f'<a class="chip" href="{PP}poslugy/index.html#{c}">{B(n)}</a>' for c, n in CATS)
    ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"MedicalBusiness","name":"Potapova Cosmetology","description":"' + B(('Косметологія та ін\'єкційна естетика в Одесі', 'Косметология и инъекционная эстетика в Одессе'), q="'") +
          '","telephone":"+380953231032","openingHours":"Mo-Su 09:00-21:00","address":{"@type":"PostalAddress","addressLocality":"Одеса","addressCountry":"UA","streetAddress":"вул. Академіка Філатова, 2, корпус 2 (ЖК «Манхеттен»)"},"sameAs":["https://www.instagram.com/potapova.cosmetology"],"founder":{"@type":"Person","name":"' + B(('Анастасія Потапова', 'Анастасия Потапова'), q="'") + '"}}</script>\n')
    faqs = [(('Як проходить перша консультація?', 'Как проходит первая консультация?'), ('Спеціаліст оглядає шкіру, уточнює побажання та історію здоров\'я і пропонує план. Консультація не зобов\'язує до процедури.', 'Специалист осматривает кожу, уточняет пожелания и историю здоровья и предлагает план. Консультация не обязывает к процедуре.')),
            (('Чи боляче на лазері?', 'Больно ли на лазере?'), ('Ми працюємо так, щоб процедура була максимально комфортною. Відчуття залежать від зони та індивідуальної чутливості.', 'Мы работаем так, чтобы процедура была максимально комфортной. Ощущения зависят от зоны и индивидуальной чувствительности.')),
            (('Скільки коштують процедури?', 'Сколько стоят процедуры?'), ('Орієнтовні ціни вказані на сторінці цін. Остаточна вартість залежить від зони та плану, який визначає спеціаліст.', 'Ориентировочные цены указаны на странице цен. Окончательная стоимость зависит от зоны и плана, который определяет специалист.'))]
    ld += ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + ','.join(
        '{"@type":"Question","name":"' + B(q, q="'") + '","acceptedAnswer":{"@type":"Answer","text":"' + B(a, q="'") + '"}}' for q, a in faqs) + ']}</script>\n')
    faq = ''.join(f'<details><summary>{B(q)}</summary><p>{B(a)}</p></details>' for q, a in faqs)
    hero = (f'<section class="hero" aria-label="Intro"><video class="hero-media" autoplay muted loop playsinline preload="auto" poster="{AA}assets/video/hero.webp" aria-hidden="true"><source src="{AA}assets/video/hero-loop.mp4" type="video/mp4"></video>'
            f'<div class="wrap"><h1 class="hin">{B(("Не змінюємо. <em>Підкреслюємо.</em>", "Не меняем. <em>Подчёркиваем.</em>"))}</h1>'
            f'<p class="sub hin" style="--i:1">{B(("Косметологія та ін\'єкційна естетика в Одесі", "Косметология и инъекционная эстетика в Одессе"))}</p>'
            f'<div class="cta hin" style="--i:2"><a class="btn btn-primary" href="{PP}kontakty.html#zapys" data-ga-event="click_book">{B(("Записатися на консультацію", "Записаться на консультацию"))}</a><a class="btn btn-ghost" href="{PP}poslugy/index.html">{B(("Послуги", "Услуги"))}</a></div>'
            f'<nav class="quick hin" style="--i:3" aria-label="Quick links"><a href="{PP}poslugy/index.html">{B(("Послуги", "Услуги"))}</a><a href="{PP}komanda.html">{B(("Команда", "Команда"))}</a><a href="{PP}tsiny.html">{B(("Ціни", "Цены"))}</a><a href="{PP}vidhuky.html">{B(("Відгуки", "Отзывы"))}</a><a href="{PP}kontakty.html">{B(("Контакти", "Контакты"))}</a></nav></div></section>')
    trust = ('<div class="trust-band"><div class="wrap"><div class="trust" aria-label="Facts">' + ''.join(
        f'<div class="rv" style="--i:{i}"><strong class="fill">{n}</strong><span>{B(t)}</span></div>' for i, (n, t) in enumerate([
            ('[N]', ('років практики', 'лет практики')), ('[N]', ('проведених процедур', 'проведённых процедур')),
            ('№ [ЛІЦЕНЗІЯ]', ('ліцензія МОЗ', 'лицензия МЗ')), ('[100%]', ('сертифіковані препарати', 'сертифицированные препараты'))])) + '</div></div></div>')
    manifest = (f'<section class="section dark manifest"><div class="wrap"><div class="eyebrow"><b>01</b> {B(("Філософія", "Философия"))}</div>'
                f'<p class="rv">{B(("Ми не обіцяємо чудес. Ми працюємо з вашою шкірою — <span>уважно, точно і без поспіху.</span>", "Мы не обещаем чудес. Мы работаем с вашей кожей — <span>внимательно, точно и без спешки.</span>"))}</p>'
                f'<div class="three"><div>{B(("Точність", "Точность"))}</div><div>{B(("Природність", "Естественность"))}</div><div>{B(("Безпека", "Безопасность"))}</div></div>'
                f'<p style="margin-top:40px"><a class="link" href="{PP}pro-nas.html">{B(("Про клініку", "О клинике"))}</a></p></div></section>')
    services = (f'<section class="section"><div class="wrap"><div class="head"><div><div class="eyebrow"><b>02</b> {B(("Послуги", "Услуги"))}</div><h2>{B(("Що ми робимо", "Что мы делаем"))}</h2></div><a class="link" href="{PP}poslugy/index.html">{B(UI["all_services"])}</a></div>'
                f'<div class="grid3">{cards}</div><div class="chips" style="margin:48px 0 0">{cat_links}</div></div></section>')
    team = (f'<section class="section sand"><div class="wrap teaser-split"><img class="rv" src="{AA}assets/img/doctor.webp" alt="Анастасія Потапова, засновниця Potapova Cosmetology" width="1200" height="1800" loading="lazy" decoding="async">'
            f'<div class="rv" style="--i:1"><div class="eyebrow"><b>03</b> {B(("Команда", "Команда"))}</div><h2>{B(("Анастасія Потапова", "Анастасия Потапова"))}</h2><p class="role">{B(("Засновниця Potapova Cosmetology", "Основательница Potapova Cosmetology"))}</p>'
            f'<p class="lead">{B(("Принцип клініки: підкреслювати природну красу, а не змінювати обличчя. Ми працюємо командою: косметологи, майстер лазерної епіляції та адміністратор.", "Принцип клиники: подчёркивать естественную красоту, а не менять лицо. Мы работаем командой: косметологи, мастер лазерной эпиляции и администратор."))}</p>'
            f'<ul class="principles"><li><b>I</b><span>{B(("Спочатку діагностика, потім план.", "Сначала диагностика, потом план."))}</span></li><li><b>II</b><span>{B(("Мінімально необхідне втручання.", "Минимально необходимое вмешательство."))}</span></li><li><b>III</b><span>{B(("Стерильність і сертифіковані препарати.", "Стерильность и сертифицированные препараты."))}</span></li></ul>'
            f'<a class="btn btn-ghost" href="{PP}komanda.html">{B(("Уся команда", "Вся команда"))}</a></div></div></section>')
    results = (f'<section class="section"><div class="wrap"><div class="head"><div><div class="eyebrow"><b>04</b> {B(("Результати", "Результаты"))}</div><h2>{B(("До та після", "До и после"))}</h2></div><a class="link" href="{PP}rezultaty.html">{B(("Усі результати", "Все результаты"))}</a></div>'
               f'<div class="ba rv"><div class="ph" data-label="[ФОТО] до"></div><div class="ph after" data-label="[ФОТО] після"></div><span class="tag" style="left:16px">{B(("До", "До"))}</span><span class="tag" style="right:16px">{B(("Після", "После"))}</span><div class="handle"></div><input type="range" min="0" max="100" value="50" aria-label="{B(("Порівняти до і після", "Сравнить до и после"))}"></div>'
               f'<p class="disc">{B(("Індивідуальний досвід, результат може відрізнятися. Публікація: за письмовою згодою пацієнта, без надмірної ретуші.", "Индивидуальный опыт, результат может отличаться. Публикация: с письменного согласия пациента, без чрезмерной ретуши."))}</p></div></section>')
    brands = (f'<section class="section dark"><div class="wrap"><div class="eyebrow"><b>05</b> {B(("Технології та бренди", "Технологии и бренды"))}</div><h2>{B(("Апарати та препарати", "Аппараты и препараты"))}</h2>'
              f'<div class="brands" aria-label="Brands"><span>DMK</span><span>IMAGE Skincare</span><span>ZO Skin Health</span><span>Rejuran</span><span>Thalgo</span><span>Guinot</span><span>Hydraderm</span></div>'
              f'<a class="link" href="{PP}tekhnolohii.html">{B(("Усі технології та бренди", "Все технологии и бренды"))}</a></div></section>')
    reviews = (f'<section class="section sand"><div class="wrap"><div class="head"><div><div class="eyebrow"><b>06</b> {B(("Відгуки", "Отзывы"))}</div><h2>{B(("Що кажуть пацієнти", "Что говорят пациенты"))}</h2></div><a class="link" href="{PP}vidhuky.html">{B(("Усі відгуки", "Все отзывы"))}</a></div>'
               f'<div class="rail" id="revTrack" tabindex="0" aria-label="Reviews">' + ''.join(
                   f'<figure class="review-card"><div class="stars" role="img" aria-label="5 / 5">★★★★★</div><blockquote class="fill">«[ВІДГУК ПАЦІЄНТА, ЗА ЗГОДОЮ]»</blockquote><figcaption><span class="ini">{l}</span><span><span>[Ім\'я]</span><span>[Місто]</span></span></figcaption></figure>' for l in 'АБВ')
               + f'</div><p class="disc" style="text-align:left">{B(("Індивідуальний досвід, результат може відрізнятися.", "Индивидуальный опыт, результат может отличаться."))}</p></div></section>')
    journal = (f'<section class="section"><div class="wrap"><div class="head"><div><div class="eyebrow"><b>07</b> {B(("Журнал", "Журнал"))}</div><h2>{B(("Читати", "Читать"))}</h2></div><a class="link" href="{PP}zhurnal.html">{B(("Усі статті", "Все статьи"))}</a></div>'
               f'<div class="grid3">{"".join(post_card(a[0], i) for i, a in enumerate(ARTICLES[:3]))}</div></div></section>')
    faq_s = f'<section class="section sand"><div class="wrap"><div class="eyebrow"><b>08</b> FAQ</div><h2 style="margin-bottom:40px">{B(("Часті питання", "Частые вопросы"))}</h2><div class="faq">{faq}</div></div></section>'
    final = (f'<section class="section dark" id="zapys"><div class="wrap final"><div><div class="eyebrow"><b>09</b> {B(("Запис", "Запись"))}</div><h2>{B(("Почнемо з розмови", "Начнём с разговора"))}</h2>'
             f'<p class="lead">{B(("Перша консультація: огляд, план, відповіді на питання. Візьміть із собою список препаратів і процедур, які ви вже проходили.", "Первая консультация: осмотр, план, ответы на вопросы. Возьмите с собой список препаратов и процедур, которые вы уже проходили."))}</p>'
             '<div class="msgrs"><a data-contact="telegram" href="#" rel="noopener" hidden>Telegram</a><a data-contact="whatsapp" href="#" rel="noopener" hidden>WhatsApp</a><a data-contact="instagram" href="#" rel="noopener" hidden>Instagram DM</a>'
             f'<a data-contact="phone" href="#" hidden>{B(("Зателефонувати", "Позвонить"))}</a><span class="fill" data-contact-empty>[ЗАПОВНИТИ: месенджери у js/config.js]</span></div>'
             f'<img class="consult-img" src="{AA}assets/img/consult.webp" alt="" width="1200" height="1800" loading="lazy" decoding="async">'
             f'<p class="lead" style="margin-top:32px">{B(("Адреса: вул. Академіка Філатова, 2, корпус 2 (ЖК «Манхеттен»), Одеса", "Адрес: ул. Академика Филатова, 2, корпус 2 (ЖК «Манхэттен»), Одесса"))}<br>{B(("Години:", "Часы:"))} <span class="fill" data-fill="hours">[ГОДИНИ РОБОТИ]</span></p></div>'
             '<!--#include leadform form=home--></div></section>')
    body = hero + trust + manifest + services + team + results + brands + journal + faq_s + final + google_strip()
    title = ('Potapova Cosmetology — косметологія в Одесі', 'Potapova Cosmetology — косметология в Одессе')
    desc = ('Не змінюємо, а підкреслюємо красу. Косметологія та ін\'єкційна естетика в Одесі. Засновниця Анастасія Потапова і команда спеціалістів.', 'Не меняем, а подчёркиваем красоту. Косметология и инъекционная эстетика в Одессе. Основательница Анастасия Потапова и команда специалистов.')
    return head(title, desc, ld) + f'<main id="main">\n{body}\n</main>' + TAIL

def gen_static():
    return {'index.html': index(), 'pro-nas.html': pro_nas(), 'komanda.html': komanda(), 'rezultaty.html': rezultaty(),
            'tekhnolohii.html': tekhnolohii(), 'vidhuky.html': vidhuky(), 'zhurnal.html': zhurnal()}
