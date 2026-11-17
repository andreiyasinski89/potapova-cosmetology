/**
 * Cloudflare Worker: пересилає заявки з сайту в Telegram (адміністратору або в групу).
 * Токен бота НІКОЛИ не кладеться в код сайту: він живе тут, як секрет Worker.
 *
 * Налаштування (докладно в docs/INTEGRATIONS.md):
 *   Секрети:   TELEGRAM_BOT_TOKEN   (від @BotFather)
 *              TELEGRAM_CHAT_ID     (ID чату/групи, куди слати)
 *   Змінна:    ALLOWED_ORIGINS      (через кому: https://your-domain.com,https://www.your-domain.com)
 * URL воркера вписується в js/config.js → forms.telegramRelay
 */
const esc = (s) => String(s ?? '').replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const allowed = (env.ALLOWED_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean);
    const cors = {
      'Access-Control-Allow-Origin': allowed.includes(origin) ? origin : allowed[0] || 'null',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Vary': 'Origin',
    };
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (request.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: cors });
    if (allowed.length && !allowed.includes(origin)) return new Response('Forbidden', { status: 403, headers: cors });

    let d;
    try { d = await request.json(); } catch { return new Response('Bad JSON', { status: 400, headers: cors }); }
    if (!d || !d.name || !d.contact || d.consent !== 'yes') return new Response('Invalid', { status: 422, headers: cors });

    const lines = [
      '🆕 <b>Нова заявка з сайту</b>',
      `👤 ${esc(d.name)}`,
      `📞 ${esc(d.contact)}`,
      d.service ? `💆 ${esc(d.service)}` : '',
      d.channel && d.channel !== 'Будь-як' ? `💬 Зручний канал: ${esc(d.channel)}` : '',
      d.message ? `📝 ${esc(String(d.message).slice(0, 800))}` : '',
      `🌐 ${esc(d.lang || '')} · ${esc(d.page || '')}`,
      d.utm_source ? `📈 ${esc(d.utm_source)}${d.utm_campaign ? ' / ' + esc(d.utm_campaign) : ''}` : '',
    ].filter(Boolean).join('\n');

    const tg = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID, text: lines, parse_mode: 'HTML', disable_web_page_preview: true }),
    });
    return new Response(JSON.stringify({ ok: tg.ok }), { status: tg.ok ? 200 : 502, headers: { ...cors, 'Content-Type': 'application/json' } });
  },
};
