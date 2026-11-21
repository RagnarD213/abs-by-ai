// Great Again T purchase tracking. Install once: Shopify admin > Settings > Customer events > Add custom pixel,
// name "Great Again T purchase", paste this file, Save, Connect. Permission: Marketing + Analytics. Data sale: not a sale.
// Sends one Google Ads conversion (value, currency, order id) and one PostHog event per Great Again T order.
// No name, email, address or quiz answer leaves the shop.
const AW = 'AW-18361229851';
const LABEL = 'RurWCMWDwbodEJvEqLNE';            // Google Ads conversion "Great Again T Purchase" (id 7907328453)
const PH_KEY = 'phc_s3ZXKWHRFQVqK6pYRBRBKtc2ex7LL78CFMHtCfENEQrU';

const tag = document.createElement('script');
tag.async = true;
tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + AW;
document.head.appendChild(tag);
window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', AW);

analytics.subscribe('checkout_completed', async (event) => {
  const c = event.data.checkout || {};
  const items = c.lineItems || [];
  const gat = items.filter((i) => /great again t/i.test(i.title || ''));
  if (!gat.length) return;
  const value = c.totalPrice ? Number(c.totalPrice.amount) : 0;
  const currency = c.currencyCode || 'USD';
  const orderId = String((c.order && c.order.id) || c.token || event.id);
  const option = gat.some((i) => i.sellingPlanAllocation) ? 'trial' : 'single';
  gtag('event', 'conversion', { send_to: AW + '/' + LABEL, value: value, currency: currency, transaction_id: orderId });
  let who = event.clientId || orderId;
  try {
    const raw = await browser.cookie.get('ph_' + PH_KEY + '_posthog');
    if (raw) { const j = JSON.parse(decodeURIComponent(raw)); if (j && j.distinct_id) who = j.distinct_id; }
  } catch (e) {}
  fetch('https://us.i.posthog.com/capture/', {
    method: 'POST', keepalive: true, headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ api_key: PH_KEY, event: 'gat_purchase', distinct_id: who,
      properties: { order_id: orderId, value: value, currency: currency, option: option, site: 'shop.sixpackabs.com', funnel: 'great-again-t' } }),
  }).catch(() => {});
});
