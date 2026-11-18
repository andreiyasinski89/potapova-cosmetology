/* ============================================================
   НАЛАШТУВАННЯ САЙТУ — єдине місце, де вписуються всі посилання та ключі.
   Порожнє значення = функція вимкнена (кнопка/посилання автоматично ховається).
   Тут НЕМАЄ паролів і токенів: усі значення публічні за своєю природою.
   Секретні токени (бот Telegram) живуть лише у Cloudflare Worker, див. docs/INTEGRATIONS.md
   ============================================================ */
window.SITE = {
  brand: 'Potapova Cosmetology',

  /* ---------- Контакти й чати ---------- */
  contacts: {
    phone: '+380953231032',            // міжнародний формат: '+380XXXXXXXXX'
    email: '',            // 'info@domain.com'
    telegram: 'potapova_anastaisha',         // нік БЕЗ @: 'potapova_cosmetology'   (профіль або бот)
    whatsapp: '+380953231032',         // номер: '+380XXXXXXXXX'
    viber: '',            // номер: '+380XXXXXXXXX'
    instagram: 'potapova.cosmetology',   // нік БЕЗ @, для DM відкривається ig.me
    facebook: '',         // повне посилання на сторінку
    tiktok: '',           // повне посилання
    address: 'вул. Академіка Філатова, 2А, ЖК «Манхеттен», Одеса',
    addressRu: 'ул. Академика Филатова, 2А, ЖК «Манхэттен», Одесса',
    mapEmbed: 'https://maps.google.com/maps?q=46.4313051,30.7265503(Potapova%20Cosmetology)&z=17&hl=uk&output=embed',   // карта на сторінці «Контакти»; координати з Google Maps
    mapUrl: 'https://www.google.com/maps/place/?q=place_id:ChIJv6nXS2QzxkAR7weqnZd8A8g',           // посилання «Прокласти маршрут» (Google Maps share link)
    hours: ''             // 'Пн–Сб 10:00–20:00'
  },

  /* Порядок каналів у плаваючій кнопці «Написати» */
  chatOrder: ['telegram', 'whatsapp', 'viber', 'instagram', 'phone'],

  /* Тексти-заготовки для WhatsApp (підставляються у повідомлення автоматично) */
  messages: {
    uk: 'Вітаю! Хочу записатися на консультацію.',
    ru: 'Здравствуйте! Хочу записаться на консультацию.'
  },

  /* ---------- Куди надходять заявки з форм (можна кілька одразу) ---------- */
  forms: {
    // 1) Email через FormSubmit.co. Вкажіть пошту. Після першої заявки прийде лист-активація, натисніть кнопку в ньому.
    formsubmitEmail: '',
    // 2) CRM (публічний ключ форми у CRM; це не пароль). Приклад MLM CRM: url 'https://mlmcrm.app/api/public/leads/', key '...'
    crm: { url: '', key: '' },
    // 3) Telegram-бот через Cloudflare Worker (миттєва сповіщення лікарю). URL воркера з integrations/telegram-relay-worker.js
    telegramRelay: '',
    // Скільки секунд між відправками з одного браузера (антиспам)
    cooldownSec: 30
  },

  /* ---------- Відгуки (Google Таблиця + Apps Script, див. integrations/apps-script-reviews.gs) ---------- */
  reviews: { url: '' },

  /* ---------- Аналітика. Вмикається лише після згоди відвідувача ---------- */
  analytics: {
    ga4: '',        // 'G-XXXXXXXXXX'
    metaPixel: '',  // числовий ID піксела Meta
    clarity: ''     // ID Microsoft Clarity
  },

  /* Пропонувати іншу мову за мовою браузера */
  langSuggest: true
};
