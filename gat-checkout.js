// Great Again T one-page order form (shop.sixpackabs.com/pages/great-again-t-order).
//
// The buyer pays on our own page: card fields are Stripe Elements, so card numbers never reach this server.
// Every paid charge (the first order and each monthly refill) then becomes a paid order in Shopify through the
// Admin API, so Supliful ships it and Shopify stays the order record.
//
//   free month  = a Stripe subscription at $67 every 30 days with a 30-day trial, plus a $9.99 shipping line on the
//                 first invoice. Charged today: $9.99. First $67 charge: 30 days later.
//   one bottle  = a single $97 invoice.
//
// Both go through Stripe invoices on purpose: an invoice charge takes its card-statement text from the product
// (SIXPACKABS.COM), where a bare PaymentIntent would read "<account name>* SIXPACKABS." on a shared Stripe account.
//
// Configuration (Railway variables; nothing is read from the Abs By AI Stripe settings):
//   GAT_STRIPE_SECRET_KEY, GAT_STRIPE_PUBLISHABLE_KEY, GAT_STRIPE_WEBHOOK_SECRET   test keys = test mode
//   GAT_SHOPIFY_SHOP, GAT_SHOPIFY_CLIENT_ID, GAT_SHOPIFY_CLIENT_SECRET             app "gat-order-sync"
//   GAT_RESEND_API_KEY (falls back to RESEND_API_KEY), GAT_FROM, GAT_ALERT_FROM
//   GAT_LINK_SECRET       signs the account-page links in emails
//   GAT_TEST_KEY          test mode only: lets the proof scripts attach a Stripe test clock
//   GAT_TEST_REAL_VARIANT test mode only: "1" puts the real variant on the Shopify test order
//   GAT_ALLOWED_ORIGINS   comma list, default https://shop.sixpackabs.com
'use strict';
const crypto = require('crypto');

const PRICE = { single: 9700, ship: 999, monthly: 6700 };
const TRIAL_DAYS = 30;
const CYCLE_DAYS = 30;
const DESCRIPTOR = 'SIXPACKABS.COM';
const SUPPORT = 'support@sixpackabs.com';
const SHOP_URL = 'https://shop.sixpackabs.com';
const PAGES = {
  order: SHOP_URL + '/pages/great-again-t-order',
  account: SHOP_URL + '/pages/great-again-t-account',
  terms: SHOP_URL + '/pages/great-again-t-terms',
  how: SHOP_URL + '/pages/great-again-t-how-it-works',
  returns: SHOP_URL + '/pages/great-again-t-shipping-and-returns',
};
const STATES = ('AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD '
  + 'TN TX UT VT VA WA WV WI WY').split(' ');
const TERMS_VERSION = 'free-trial-2026-11-18';
const API_VERSION_SHOPIFY = '2026-10';

const money = c => '$' + (c / 100).toFixed(2);
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]));
const clean = (v, max) => String(v == null ? '' : v).replace(/[\u0000-\u001f\u007f]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, max);
const longDate = d => new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'America/Chicago' });

class GatError extends Error {
  constructor(status, message, field) { super(message); this.status = status; this.field = field; }
}

function createGatCheckout({ db, dbReady, express, rateLimit, env = process.env, fetchImpl = fetch, log = console, stripeFactory }) {
  const SK = env.GAT_STRIPE_SECRET_KEY || '';
  const PK = env.GAT_STRIPE_PUBLISHABLE_KEY || '';
  const WH = env.GAT_STRIPE_WEBHOOK_SECRET || '';
  const MODE = SK.startsWith('sk_live_') ? 'live' : SK.startsWith('sk_test_') ? 'test' : 'off';
  const SHOP = env.GAT_SHOPIFY_SHOP || '';
  const VARIANT = env.GAT_SHOPIFY_VARIANT_ID || '68049477796162';
  const ORIGINS = (env.GAT_ALLOWED_ORIGINS || SHOP_URL).split(',').map(s => s.trim()).filter(Boolean);
  const RESEND = env.GAT_RESEND_API_KEY || env.RESEND_API_KEY || '';
  const FROM = env.GAT_FROM || 'SixPackAbs.com <orders@sixpackabs.com>';
  const ALERT_FROM = env.GAT_ALERT_FROM || env.RESET_FROM || FROM;
  const LINK_SECRET = env.GAT_LINK_SECRET || (WH ? crypto.createHash('sha256').update('gat-link:' + WH).digest('hex') : '');
  const TEST_KEY = MODE === 'test' ? (env.GAT_TEST_KEY || '') : '';

  let stripeClient = null;
  const stripe = () => {
    if (!SK) throw new GatError(503, 'Ordering is not open yet.');
    if (!stripeClient) stripeClient = (stripeFactory || require('stripe'))(SK);
    return stripeClient;
  };

  // ------------------------------------------------------------------ database
  let tablesReady = null;
  function ready() {
    if (!db) return Promise.reject(new GatError(503, 'Ordering is not available right now.'));
    if (!tablesReady) {
      tablesReady = Promise.resolve(dbReady).then(() => db.query(`
        CREATE TABLE IF NOT EXISTS gat_orders (
          id TEXT PRIMARY KEY, mode TEXT NOT NULL, option TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'pending',
          email TEXT NOT NULL, first_name TEXT NOT NULL, last_name TEXT NOT NULL, phone TEXT, sms_opt_in BOOLEAN NOT NULL DEFAULT false,
          ship JSONB NOT NULL, bill JSONB, agreed_at TIMESTAMPTZ, agreed_terms TEXT, ip TEXT, user_agent TEXT, attribution JSONB,
          stripe_customer_id TEXT, stripe_subscription_id TEXT, stripe_invoice_id TEXT, stripe_payment_intent_id TEXT,
          amount_cents INTEGER NOT NULL, tracked_at TIMESTAMPTZ, paid_at TIMESTAMPTZ, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
        CREATE TABLE IF NOT EXISTS gat_subscriptions (
          stripe_subscription_id TEXT PRIMARY KEY, order_id TEXT NOT NULL, mode TEXT NOT NULL, status TEXT NOT NULL,
          first_charge_at TIMESTAMPTZ, next_charge_at TIMESTAMPTZ, reminder_sent_at TIMESTAMPTZ, canceled_at TIMESTAMPTZ,
          cancel_email_sent_at TIMESTAMPTZ, failed_email_invoice TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
        CREATE TABLE IF NOT EXISTS gat_charges (
          stripe_invoice_id TEXT PRIMARY KEY, order_id TEXT NOT NULL, kind TEXT NOT NULL, amount_cents INTEGER NOT NULL,
          state TEXT NOT NULL DEFAULT 'creating', shopify_order_id TEXT, shopify_order_name TEXT, email_sent_at TIMESTAMPTZ,
          last_error TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT now(), updated_at TIMESTAMPTZ NOT NULL DEFAULT now());
        CREATE INDEX IF NOT EXISTS gat_orders_sub ON gat_orders (stripe_subscription_id);
        CREATE INDEX IF NOT EXISTS gat_orders_invoice ON gat_orders (stripe_invoice_id);
      `)).catch(e => { tablesReady = null; throw e; });
    }
    return tablesReady;
  }
  const one = async (sql, args) => (await db.query(sql, args)).rows[0] || null;

  // ------------------------------------------------------------------ Stripe catalog (found or made once per account and mode)
  let catalog = null;
  async function prices() {
    if (catalog) return catalog;
    const s = stripe();
    const find = async key => (await s.prices.list({ lookup_keys: [key], active: true, limit: 1, expand: ['data.product'] })).data[0];
    let monthly = await find('gat_monthly_6700');
    let single = await find('gat_single_9700');
    let ship = await find('gat_ship_999');
    if (!monthly || !single) {
      const product = (monthly && monthly.product.id) || (single && single.product.id)
        || (await s.products.create({ name: 'Great Again T', statement_descriptor: DESCRIPTOR, metadata: { funnel: 'gat' } })).id;
      if (!monthly) monthly = await s.prices.create({ product, currency: 'usd', unit_amount: PRICE.monthly, lookup_key: 'gat_monthly_6700',
        nickname: 'Monthly supply, shipping included', recurring: { interval: 'day', interval_count: CYCLE_DAYS } });
      if (!single) single = await s.prices.create({ product, currency: 'usd', unit_amount: PRICE.single, lookup_key: 'gat_single_9700', nickname: 'One bottle, one time' });
    }
    if (!ship) {
      const product = (await s.products.create({ name: 'Shipping and handling', statement_descriptor: DESCRIPTOR, metadata: { funnel: 'gat' } })).id;
      ship = await s.prices.create({ product, currency: 'usd', unit_amount: PRICE.ship, lookup_key: 'gat_ship_999' });
    }
    if (monthly.unit_amount !== PRICE.monthly || single.unit_amount !== PRICE.single || ship.unit_amount !== PRICE.ship) throw new Error('GAT price mismatch at Stripe');
    catalog = { monthly: monthly.id, single: single.id, ship: ship.id };
    return catalog;
  }

  // ------------------------------------------------------------------ input
  function address(a, what) {
    const out = {
      address1: clean(a && a.address1, 120), address2: clean(a && a.address2, 120), city: clean(a && a.city, 80),
      state: clean(a && a.state, 2).toUpperCase(), zip: clean(a && a.zip, 10), country: 'US',
    };
    if (out.address1.length < 3) throw new GatError(400, `Please enter your ${what} address.`, what + '.address1');
    if (out.city.length < 2) throw new GatError(400, `Please enter your ${what} city.`, what + '.city');
    if (!STATES.includes(out.state)) throw new GatError(400, `Please choose your ${what} state.`, what + '.state');
    if (!/^\d{5}(-\d{4})?$/.test(out.zip)) throw new GatError(400, `Please enter a 5 digit ${what} ZIP code.`, what + '.zip');
    return out;
  }
  function parse(body) {
    const b = body || {};
    const option = b.option === 'single' ? 'single' : b.option === 'trial' ? 'trial' : null;
    if (!option) throw new GatError(400, 'Please choose an option.', 'option');
    const firstName = clean(b.firstName, 60), lastName = clean(b.lastName, 60);
    const email = clean(b.email, 160).toLowerCase(), phone = clean(b.phone, 30);
    if (!firstName) throw new GatError(400, 'Please enter your first name.', 'firstName');
    if (!lastName) throw new GatError(400, 'Please enter your last name.', 'lastName');
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) throw new GatError(400, 'Please enter a valid email address.', 'email');
    if (phone.replace(/\D/g, '').length < 10) throw new GatError(400, 'Please enter your phone number.', 'phone');
    const ship = address(b.shipping, 'shipping');
    const bill = b.billing ? Object.assign(address(b.billing, 'billing'), {
      firstName: clean(b.billing.firstName, 60) || firstName, lastName: clean(b.billing.lastName, 60) || lastName }) : null;
    if (option === 'trial' && b.agree !== true) throw new GatError(400, 'Please tick the box to agree to the terms of the offer.', 'agree');
    const at = b.attribution && typeof b.attribution === 'object' ? b.attribution : {};
    const attribution = {};
    for (const k of ['ph', 'gclid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']) if (at[k]) attribution[k] = clean(at[k], 200);
    return { option, firstName, lastName, email, phone, ship, bill, agree: b.agree === true, sms: b.sms === true, attribution, orderId: clean(b.orderId, 40) };
  }
  const stripeAddress = a => ({ line1: a.address1, line2: a.address2 || undefined, city: a.city, state: a.state, postal_code: a.zip, country: 'US' });

  // ------------------------------------------------------------------ create (or reuse) the order and its first payment
  async function createOrder(body, meta) {
    await ready();
    const s = stripe(), p = parse(body), cat = await prices();
    const name = `${p.firstName} ${p.lastName}`;
    const customerFields = {
      email: p.email, name, phone: p.phone,
      shipping: { name, phone: p.phone, address: stripeAddress(p.ship) },
      address: stripeAddress(p.bill || p.ship),
    };
    const amount = p.option === 'trial' ? PRICE.ship : PRICE.single;

    // A second press after a declined card reuses the same order and payment instead of piling up new ones.
    if (p.orderId) {
      const row = await one('SELECT * FROM gat_orders WHERE id = $1 AND mode = $2', [p.orderId, MODE]);
      if (row && row.status === 'pending' && row.option === p.option && row.stripe_payment_intent_id) {
        const pi = await s.paymentIntents.retrieve(row.stripe_payment_intent_id);
        if (['requires_payment_method', 'requires_confirmation', 'requires_action'].includes(pi.status)) {
          await s.customers.update(row.stripe_customer_id, customerFields);
          await db.query(`UPDATE gat_orders SET email=$2, first_name=$3, last_name=$4, phone=$5, sms_opt_in=$6, ship=$7, bill=$8,
            agreed_at = CASE WHEN $9 THEN now() ELSE agreed_at END WHERE id=$1`,
            [row.id, p.email, p.firstName, p.lastName, p.phone, p.sms, p.ship, p.bill, p.agree]);
          return { orderId: row.id, clientSecret: pi.client_secret, amount, mode: MODE };
        }
      }
    }

    const id = crypto.randomBytes(12).toString('hex');
    const md = { funnel: 'gat', gat_order: id, gat_option: p.option };
    const clock = TEST_KEY && meta.testKey === TEST_KEY && body.testClock ? clean(body.testClock, 60) : undefined;
    const customer = await s.customers.create(Object.assign({ metadata: md, test_clock: clock }, customerFields));
    let subId = null, invoice;
    if (p.option === 'trial') {
      const sub = await s.subscriptions.create({
        customer: customer.id,
        items: [{ price: cat.monthly }],
        trial_period_days: TRIAL_DAYS,
        add_invoice_items: [{ price: cat.ship }],
        payment_behavior: 'default_incomplete',
        payment_settings: { save_default_payment_method: 'on_subscription', payment_method_types: ['card'] },
        metadata: md,
        expand: ['latest_invoice.payment_intent'],
      });
      subId = sub.id; invoice = sub.latest_invoice;
    } else {
      const draft = await s.invoices.create({
        customer: customer.id, collection_method: 'charge_automatically', auto_advance: false, statement_descriptor: DESCRIPTOR,
        pending_invoice_items_behavior: 'exclude', payment_settings: { payment_method_types: ['card'] }, metadata: md,
      });
      await s.invoiceItems.create({ customer: customer.id, invoice: draft.id, price: cat.single });
      invoice = await s.invoices.finalizeInvoice(draft.id, { auto_advance: false, expand: ['payment_intent'] });
      // Keeps the card on the customer, so a later one-click upsell can charge it (the upsell pages are not built yet).
      await s.paymentIntents.update(invoice.payment_intent.id, { setup_future_usage: 'off_session' });
    }
    const pi = invoice.payment_intent;
    if (!pi || invoice.amount_due !== amount) throw new Error(`GAT first invoice is ${invoice.amount_due}, expected ${amount}`);
    await db.query(`INSERT INTO gat_orders (id, mode, option, email, first_name, last_name, phone, sms_opt_in, ship, bill, agreed_at, agreed_terms,
        ip, user_agent, attribution, stripe_customer_id, stripe_subscription_id, stripe_invoice_id, stripe_payment_intent_id, amount_cents)
      VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10, CASE WHEN $11 THEN now() END, $12,$13,$14,$15,$16,$17,$18,$19,$20)`,
      [id, MODE, p.option, p.email, p.firstName, p.lastName, p.phone, p.sms, p.ship, p.bill, p.agree, p.agree ? TERMS_VERSION : null,
        clean(meta.ip, 60), clean(meta.ua, 300), p.attribution, customer.id, subId, invoice.id, pi.id, amount]);
    return { orderId: id, clientSecret: pi.client_secret, amount, mode: MODE };
  }

  // ------------------------------------------------------------------ Shopify
  let shopToken = null;
  async function shopifyToken(force) {
    if (!force && shopToken && shopToken.until > Date.now()) return shopToken.value;
    if (!SHOP || !env.GAT_SHOPIFY_CLIENT_ID || !env.GAT_SHOPIFY_CLIENT_SECRET) throw new Error('Shopify app is not configured');
    const r = await fetchImpl(`https://${SHOP}/admin/oauth/access_token`, {
      method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ grant_type: 'client_credentials', client_id: env.GAT_SHOPIFY_CLIENT_ID, client_secret: env.GAT_SHOPIFY_CLIENT_SECRET }),
    });
    if (!r.ok) throw new Error('Shopify token ' + r.status);
    const j = await r.json();
    shopToken = { value: j.access_token, until: Date.now() + Math.max(60, (j.expires_in || 3600) - 600) * 1000 };
    return shopToken.value;
  }
  async function shopify(query, variables, retried) {
    const r = await fetchImpl(`https://${SHOP}/admin/api/${API_VERSION_SHOPIFY}/graphql.json`, {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Shopify-Access-Token': await shopifyToken(retried) },
      body: JSON.stringify({ query, variables }),
    });
    if (r.status === 401 && !retried) return shopify(query, variables, true);
    const j = await r.json().catch(() => ({}));
    if (!r.ok || j.errors) throw new Error('Shopify ' + r.status + ' ' + JSON.stringify(j.errors || j).slice(0, 400));
    return j.data;
  }
  const usd = cents => ({ shopMoney: { amount: (cents / 100).toFixed(2), currencyCode: 'USD' } });

  async function createShopifyOrder(order, kind, invoice) {
    const tag = 'gat-inv-' + invoice.id;
    const found = await shopify('query($q: String!) { orders(first: 1, query: $q) { nodes { id name } } }', { q: `tag:'${tag}'` });
    if (found.orders.nodes[0]) return found.orders.nodes[0];     // made on an earlier attempt whose database write failed
    const ship = order.ship, bill = order.bill;
    const product = kind === 'first' ? 0 : kind === 'renewal' ? PRICE.monthly : PRICE.single;
    const shipping = kind === 'first' ? PRICE.ship : 0;
    const total = product + shipping;
    if (total !== invoice.amount_paid) throw new Error(`invoice ${invoice.id} paid ${invoice.amount_paid}, order would be ${total}`);
    const testOrder = MODE !== 'live';
    const line = testOrder && env.GAT_TEST_REAL_VARIANT !== '1'
      ? { title: 'Great Again T (TEST ORDER, do not ship)', quantity: 1, priceSet: usd(product), requiresShipping: true }
      : { variantId: 'gid://shopify/ProductVariant/' + VARIANT, quantity: 1, priceSet: usd(product) };
    const addr = (a, first, last) => ({ firstName: first, lastName: last, address1: a.address1, address2: a.address2 || null, city: a.city,
      provinceCode: a.state, countryCode: 'US', zip: a.zip, phone: order.phone || null });
    const label = { first: 'Free month (first order)', renewal: 'Monthly refill', single: 'One bottle, one time' }[kind];
    const input = {
      email: order.email,
      customer: { toUpsert: { email: order.email, firstName: order.first_name, lastName: order.last_name } },
      lineItems: [line],
      shippingAddress: addr(ship, order.first_name, order.last_name),
      billingAddress: bill ? addr(bill, bill.firstName || order.first_name, bill.lastName || order.last_name) : addr(ship, order.first_name, order.last_name),
      shippingLines: [{ title: shipping ? 'Standard' : 'Standard (free)', code: 'Standard', priceSet: usd(shipping) }],
      transactions: [{ kind: 'SALE', status: 'SUCCESS', gateway: 'Stripe (one-page order form)', amountSet: usd(total), test: testOrder }],
      financialStatus: 'PAID',
      currency: 'USD',
      test: testOrder,
      tags: ['Great Again T', 'gat-one-page', 'gat-' + kind, tag].concat(testOrder ? ['gat-test'] : [], kind !== 'single' ? ['Subscription'] : []),
      note: `${label}. Paid on the one-page order form through Stripe.` + (testOrder ? ' TEST MODE: no real money, do not ship.' : ''),
      customAttributes: [
        { key: 'Order form', value: label }, { key: 'Stripe invoice', value: invoice.id },
        { key: 'Stripe customer', value: order.stripe_customer_id || '' }, { key: 'Order form id', value: order.id },
        { key: 'Text updates', value: order.sms_opt_in ? 'yes' : 'no' },
      ],
    };
    const data = await shopify(`mutation($order: OrderCreateOrderInput!, $options: OrderCreateOptionsInput) {
      orderCreate(order: $order, options: $options) { order { id name } userErrors { field message } } }`,
      { order: input, options: { sendReceipt: false, sendFulfillmentReceipt: false, inventoryBehaviour: 'BYPASS' } });
    const res = data.orderCreate;
    if (res.userErrors && res.userErrors.length) throw new Error('Shopify orderCreate: ' + JSON.stringify(res.userErrors).slice(0, 400));
    return res.order;
  }

  // ------------------------------------------------------------------ email
  async function send(to, subject, html, from) {
    if (!RESEND) { log.warn('GAT email skipped (no key):', subject); return false; }
    const r = await fetchImpl('https://api.resend.com/emails', {
      method: 'POST', headers: { Authorization: 'Bearer ' + RESEND, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: from || FROM, to: [to], reply_to: SUPPORT, subject: (MODE === 'test' ? '[TEST] ' : '') + subject, html }),
    });
    if (!r.ok) { log.error('GAT email failed:', r.status, (await r.text()).slice(0, 200)); return false; }
    return true;
  }
  const alert = (subject, text) => send(SUPPORT, 'Order form alert: ' + subject, `<p>${esc(text)}</p>`, ALERT_FROM).catch(() => false);

  const sign = id => crypto.createHmac('sha256', LINK_SECRET).update('acct:' + id).digest('hex').slice(0, 32);
  const accountLink = id => `${PAGES.account}?o=${id}&k=${sign(id)}`;
  const linkOk = (id, k) => !!LINK_SECRET && typeof k === 'string' && k.length === 32 && crypto.timingSafeEqual(Buffer.from(k), Buffer.from(sign(id)));

  function shell(title, inner) {
    return `<div style="font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:1.55;color:#1f2a27;max-width:560px;margin:0 auto;padding:8px 4px">
<p style="font-size:13px;letter-spacing:.08em;font-weight:700;color:#8a7440;margin:0 0 14px">SIXPACKABS.COM</p>
<h1 style="font-size:22px;line-height:1.3;margin:0 0 14px;color:#14201d">${title}</h1>${inner}
<p style="margin-top:26px;font-size:13px;color:#69706c;border-top:1px solid #e3e5df;padding-top:14px">Questions? Reply to this email or write to ${SUPPORT}.<br>
SixPackAbs.com is owned and operated by Rose Digital Holdings LLC, 3520 Cavu Rd, Georgetown, TX 78628.</p></div>`;
  }
  const button = (href, text) => `<p style="margin:20px 0"><a href="${href}" style="display:inline-block;background:#14201d;color:#ffffff;text-decoration:none;font-weight:700;padding:13px 22px;border-radius:6px">${text}</a></p>`;
  const shipTo = o => `${esc(o.first_name)} ${esc(o.last_name)}<br>${esc(o.ship.address1)}${o.ship.address2 ? ', ' + esc(o.ship.address2) : ''}<br>${esc(o.ship.city)}, ${esc(o.ship.state)} ${esc(o.ship.zip)}`;
  const rows = list => '<table style="width:100%;border-collapse:collapse;margin:14px 0">' + list.map(([a, b, bold]) =>
    `<tr><td style="padding:7px 0;border-bottom:1px solid #e3e5df${bold ? ';font-weight:700' : ''}">${a}</td><td style="padding:7px 0;border-bottom:1px solid #e3e5df;text-align:right${bold ? ';font-weight:700' : ''}">${b}</td></tr>`).join('') + '</table>';

  function confirmationEmail(o, kind, orderName, firstCharge) {
    const link = accountLink(o.id);
    if (kind === 'single') {
      return ['Your Great Again T order ' + orderName, shell(`Thank you, ${esc(o.first_name)}. Your order is confirmed.`,
        `<p>Order ${esc(orderName)}</p>` + rows([['Great Again T, one bottle (60 tablets)', money(PRICE.single)], ['Shipping and handling', '$0.00'], ['Total charged today', money(PRICE.single), true]])
        + `<p>This is a one time order. There are no monthly shipments and you will not be charged again.</p>
<p><b>Shipping to</b><br>${shipTo(o)}</p>
<p>Your bottle ships within 2 to 5 business days. We will email you a tracking link when it leaves.</p>
<p>The charge appears on your statement as ${DESCRIPTOR}.</p>
<p>You are covered by our one year money back guarantee on unopened bottles. Details: <a href="${PAGES.returns}">Shipping and Returns</a>.</p>`)];
    }
    return ['Your free bottle of Great Again T is on the way (order ' + orderName + ')', shell(`Thank you, ${esc(o.first_name)}. Your free bottle is confirmed.`,
      `<p>Order ${esc(orderName)}</p>` + rows([['Great Again T, free month’s supply (60 tablets)', '$0.00'], ['Shipping and handling', money(PRICE.ship)], ['Total charged today', money(PRICE.ship), true]])
      + `<p><b>Shipping to</b><br>${shipTo(o)}</p>
<p>Your bottle ships within 2 to 5 business days. We will email you a tracking link when it leaves.</p>
<h2 style="font-size:18px;margin:22px 0 8px;color:#14201d">How your monthly delivery works</h2>
<p>You have 30 days to try Great Again T. If you continue, we ship you a fresh bottle every 30 days and charge your card ${money(PRICE.monthly)} per bottle, shipping included, until you cancel.</p>
<p><b>Your first ${money(PRICE.monthly)} charge is on ${longDate(firstCharge)}.</b> We will email you a reminder at least 7 days before it.</p>
<p>You can cancel, skip a month or update your card at any time on your account page. If you cancel before ${longDate(firstCharge)}, you keep your free bottle and you are not billed again.</p>`
      + button(link, 'Open My Account Page')
      + `<p>You can also cancel by emailing ${SUPPORT}. Charges appear on your statement as ${DESCRIPTOR}. Full terms: <a href="${PAGES.terms}">Terms and Conditions</a>.</p>`)];
  }
  function reminderEmail(o, chargeAt) {
    return [`Reminder: your first ${money(PRICE.monthly)} Great Again T refill is on ${longDate(chargeAt)}`, shell(`${esc(o.first_name)}, your first monthly refill is coming up.`,
      `<p>On <b>${longDate(chargeAt)}</b> we will charge your card <b>${money(PRICE.monthly)}</b>, shipping included, and ship your next bottle of Great Again T.</p>
<p>After that, a fresh bottle ships every 30 days at ${money(PRICE.monthly)} until you cancel. There is no minimum number of months and no cancellation fee.</p>
<p><b>Want to keep going?</b> You do not need to do anything.</p>
<p><b>Want to cancel or skip a month?</b> Use your account page before ${longDate(chargeAt)} and you will not be charged. You keep your free bottle.</p>`
      + button(accountLink(o.id), 'Cancel, Skip Or Update My Card')
      + `<p>You can also cancel by emailing ${SUPPORT}. The charge will appear on your statement as ${DESCRIPTOR}.</p>`)];
  }
  function renewalEmail(o, orderName, nextAt) {
    return ['Your Great Again T refill is on the way (order ' + orderName + ')', shell(`${esc(o.first_name)}, your next bottle is on the way.`,
      `<p>Order ${esc(orderName)}</p>` + rows([['Great Again T, monthly supply (60 tablets)', money(PRICE.monthly)], ['Shipping and handling', 'Included'], ['Total charged today', money(PRICE.monthly), true]])
      + `<p><b>Shipping to</b><br>${shipTo(o)}</p><p>Your bottle ships within 2 to 5 business days. We will email you a tracking link when it leaves.</p>`
      + (nextAt ? `<p>Your next refill is on ${longDate(nextAt)}. You can cancel, skip a month or update your card at any time.</p>` : '')
      + button(accountLink(o.id), 'Open My Account Page') + `<p>The charge appears on your statement as ${DESCRIPTOR}.</p>`)];
  }
  function cancelEmail(o) {
    return ['Your Great Again T monthly delivery is cancelled', shell(`${esc(o.first_name)}, your monthly delivery is cancelled.`,
      `<p>This confirms that your Great Again T monthly delivery is cancelled. You will not be charged again and no more bottles will ship.</p>
<p>Any order that was already charged will still ship, and it is covered by our one year money back guarantee on unopened bottles.</p>
<p>If you did not ask for this, or you want to start again, reply to this email.</p>`)];
  }
  function failedEmail(o) {
    return ['Action needed: we could not charge your card for Great Again T', shell(`${esc(o.first_name)}, your card was declined.`,
      `<p>We tried to charge ${money(PRICE.monthly)} for your next bottle of Great Again T and the payment did not go through. Your bottle has not shipped.</p>
<p>We will try again over the next few days. To avoid a delay, update your card on your account page.</p>`
      + button(accountLink(o.id), 'Update My Card') + `<p>If you would rather stop your monthly delivery, you can cancel on the same page.</p>`)];
  }

  // ------------------------------------------------------------------ a paid invoice becomes a Shopify order (once)
  async function orderForInvoice(invoice) {
    const md = invoice.metadata || {}, smd = (invoice.subscription_details && invoice.subscription_details.metadata) || {};
    const id = md.gat_order || smd.gat_order;
    if (id) return one('SELECT * FROM gat_orders WHERE id = $1 AND mode = $2', [id, MODE]);
    const subId = typeof invoice.subscription === 'string' ? invoice.subscription : invoice.subscription && invoice.subscription.id;
    if (subId) return one('SELECT * FROM gat_orders WHERE stripe_subscription_id = $1 AND mode = $2', [subId, MODE]);
    return one('SELECT * FROM gat_orders WHERE stripe_invoice_id = $1 AND mode = $2', [invoice.id, MODE]);
  }

  async function processPaidInvoice(invoice) {
    await ready();
    const order = await orderForInvoice(invoice);
    if (!order) return { skipped: 'not a Great Again T invoice' };
    if (!(invoice.amount_paid > 0)) return { skipped: 'nothing paid' };
    const kind = order.option === 'single' ? 'single' : invoice.id === order.stripe_invoice_id ? 'first' : 'renewal';
    const claim = await db.query(`INSERT INTO gat_charges (stripe_invoice_id, order_id, kind, amount_cents) VALUES ($1,$2,$3,$4)
      ON CONFLICT (stripe_invoice_id) DO UPDATE SET state='creating', updated_at=now()
        WHERE gat_charges.state='error' OR (gat_charges.state='creating' AND gat_charges.updated_at < now() - interval '3 minutes')
      RETURNING stripe_invoice_id`, [invoice.id, order.id, kind, invoice.amount_paid]);
    if (!claim.rowCount) return { duplicate: true, charge: await one('SELECT * FROM gat_charges WHERE stripe_invoice_id=$1', [invoice.id]) };
    try {
      let sub = null;
      if (order.stripe_subscription_id) {
        sub = await stripe().subscriptions.retrieve(order.stripe_subscription_id);
        const next = sub.status === 'canceled' ? null : new Date((sub.trial_end && sub.status === 'trialing' ? sub.trial_end : sub.current_period_end) * 1000);
        await db.query(`INSERT INTO gat_subscriptions (stripe_subscription_id, order_id, mode, status, first_charge_at, next_charge_at)
          VALUES ($1,$2,$3,$4,$5,$6) ON CONFLICT (stripe_subscription_id) DO UPDATE SET status=$4, next_charge_at=$6`,
          [sub.id, order.id, MODE, sub.status, sub.trial_end ? new Date(sub.trial_end * 1000) : next, next]);
      }
      if (kind !== 'renewal') await db.query(`UPDATE gat_orders SET status='paid', paid_at=COALESCE(paid_at, now()) WHERE id=$1`, [order.id]);
      const made = await createShopifyOrder(order, kind, invoice);
      await db.query(`UPDATE gat_charges SET state='done', shopify_order_id=$2, shopify_order_name=$3, last_error=NULL, updated_at=now() WHERE stripe_invoice_id=$1`,
        [invoice.id, made.id, made.name]);
      await sendOrderEmail(invoice.id).catch(e => log.error('GAT order email failed:', e.message));
      return { ok: true, kind, shopify: made };
    } catch (e) {
      await db.query(`UPDATE gat_charges SET state='error', last_error=$2, updated_at=now() WHERE stripe_invoice_id=$1`, [invoice.id, String(e.message).slice(0, 500)]).catch(() => {});
      alert('a paid order was not created in Shopify', `Stripe invoice ${invoice.id} (${money(invoice.amount_paid)}, ${MODE} mode) is paid but the Shopify order failed: ${e.message}. Stripe will retry the webhook; if this repeats, create the order by hand.`);
      throw e;
    }
  }

  async function sendOrderEmail(invoiceId) {
    const charge = await one('SELECT * FROM gat_charges WHERE stripe_invoice_id=$1', [invoiceId]);
    if (!charge || charge.state !== 'done' || charge.email_sent_at) return false;
    const order = await one('SELECT * FROM gat_orders WHERE id=$1', [charge.order_id]);
    const sub = order.stripe_subscription_id ? await one('SELECT * FROM gat_subscriptions WHERE stripe_subscription_id=$1', [order.stripe_subscription_id]) : null;
    const mail = charge.kind === 'renewal' ? renewalEmail(order, charge.shopify_order_name, sub && !sub.canceled_at ? sub.next_charge_at : null)
      : confirmationEmail(order, charge.kind, charge.shopify_order_name, sub && sub.first_charge_at);
    const claim = await db.query('UPDATE gat_charges SET email_sent_at=now() WHERE stripe_invoice_id=$1 AND email_sent_at IS NULL RETURNING order_id', [invoiceId]);
    if (!claim.rowCount) return false;
    if (await send(order.email, mail[0], mail[1])) return true;
    await db.query('UPDATE gat_charges SET email_sent_at=NULL WHERE stripe_invoice_id=$1', [invoiceId]);
    return false;
  }

  // ------------------------------------------------------------------ reminder, 7 days before the first $67 charge
  async function sendReminder(subId, chargeAt) {
    const claim = await db.query(`UPDATE gat_subscriptions SET reminder_sent_at=now() WHERE stripe_subscription_id=$1 AND reminder_sent_at IS NULL
      AND canceled_at IS NULL RETURNING order_id`, [subId]);
    if (!claim.rowCount) return false;
    const order = await one('SELECT * FROM gat_orders WHERE id=$1', [claim.rows[0].order_id]);
    const mail = reminderEmail(order, chargeAt);
    if (await send(order.email, mail[0], mail[1])) return true;
    await db.query('UPDATE gat_subscriptions SET reminder_sent_at=NULL WHERE stripe_subscription_id=$1', [subId]);   // try again on the next sweep
    return false;
  }
  // Runs from the server's hourly timer. `now` can be passed in by the proof scripts (Stripe test clocks live in the future).
  async function sweep(now = new Date()) {
    if (MODE === 'off' || !db) return { skipped: true };
    await ready();
    const due = await db.query(`SELECT stripe_subscription_id, first_charge_at FROM gat_subscriptions WHERE mode=$1 AND status='trialing'
      AND reminder_sent_at IS NULL AND canceled_at IS NULL AND first_charge_at > $2 AND first_charge_at <= $2::timestamptz + interval '8 days'`, [MODE, now]);
    let sent = 0;
    for (const r of due.rows) {
      try {
        const sub = await stripe().subscriptions.retrieve(r.stripe_subscription_id);
        if (sub.status !== 'trialing' || sub.cancel_at_period_end) { await syncSubscription(sub); continue; }
        if (await sendReminder(sub.id, new Date(sub.trial_end * 1000))) sent++;
      } catch (e) { log.error('GAT reminder failed:', r.stripe_subscription_id, e.message); }
    }
    // An order email that did not go out (mail provider down) is sent on a later pass.
    const unsent = await db.query(`SELECT c.stripe_invoice_id FROM gat_charges c JOIN gat_orders o ON o.id = c.order_id
      WHERE o.mode=$1 AND c.state='done' AND c.email_sent_at IS NULL AND c.created_at > now() - interval '3 days' LIMIT 20`, [MODE]);
    let resent = 0;
    for (const r of unsent.rows) {
      try { if (await sendOrderEmail(r.stripe_invoice_id)) resent++; } catch (e) { log.error('GAT order email retry failed:', e.message); }
    }
    // A one-bottle invoice that was never paid stays open at Stripe for ever unless it is voided.
    const stale = await db.query(`UPDATE gat_orders SET status='expired' WHERE mode=$1 AND status='pending' AND created_at < now() - interval '24 hours'
      RETURNING option, stripe_invoice_id`, [MODE]);
    for (const r of stale.rows) {
      if (r.option === 'single') await stripe().invoices.voidInvoice(r.stripe_invoice_id).catch(() => {});
    }
    return { due: due.rowCount, sent, resent, expired: stale.rowCount };
  }

  async function syncSubscription(sub) {
    const row = await one('SELECT * FROM gat_subscriptions WHERE stripe_subscription_id=$1', [sub.id]);
    if (!row) return false;
    const gone = sub.status === 'canceled' || sub.status === 'incomplete_expired' || sub.cancel_at_period_end === true;
    const next = gone ? null : new Date((sub.status === 'trialing' && sub.trial_end ? sub.trial_end : sub.current_period_end) * 1000);
    await db.query(`UPDATE gat_subscriptions SET status=$2, next_charge_at=$3, canceled_at = CASE WHEN $4 THEN COALESCE(canceled_at, now()) ELSE NULL END,
      first_charge_at = CASE WHEN reminder_sent_at IS NULL AND $5::timestamptz IS NOT NULL
        AND NOT EXISTS (SELECT 1 FROM gat_charges c WHERE c.order_id = gat_subscriptions.order_id AND c.kind = 'renewal') THEN $5 ELSE first_charge_at END
      WHERE stripe_subscription_id=$1`, [sub.id, sub.status, next, gone, !gone && sub.status === 'trialing' && sub.trial_end ? new Date(sub.trial_end * 1000) : null]);
    if (gone && !row.cancel_email_sent_at) {
      const claim = await db.query('UPDATE gat_subscriptions SET cancel_email_sent_at=now() WHERE stripe_subscription_id=$1 AND cancel_email_sent_at IS NULL RETURNING order_id', [sub.id]);
      if (claim.rowCount) {
        const order = await one('SELECT * FROM gat_orders WHERE id=$1', [row.order_id]);
        const mail = cancelEmail(order);
        await send(order.email, mail[0], mail[1]);
      }
    }
    return true;
  }

  // Stripe sends each event in the shape of the webhook's API version, which is not always this package's. Only ids are
  // taken from the event; the invoice or subscription itself is read again from Stripe, so the fields are always the same.
  const invoiceSubId = inv => (typeof inv.subscription === 'string' && inv.subscription) || (inv.subscription && inv.subscription.id)
    || (inv.parent && inv.parent.subscription_details && inv.parent.subscription_details.subscription) || null;
  async function handleEvent(event) {
    const obj = event.data.object, s = stripe();
    await ready();
    if (event.type === 'invoice.paid') return processPaidInvoice(await s.invoices.retrieve(obj.id));
    if (event.type === 'customer.subscription.updated' || event.type === 'customer.subscription.deleted') {
      if (!await one('SELECT 1 FROM gat_subscriptions WHERE stripe_subscription_id=$1', [obj.id])) return false;
      return syncSubscription(await s.subscriptions.retrieve(obj.id));
    }
    if (event.type === 'invoice.upcoming') {
      const subId = invoiceSubId(obj);
      const row = subId && await one('SELECT * FROM gat_subscriptions WHERE stripe_subscription_id=$1', [subId]);
      if (!row || row.reminder_sent_at) return false;
      const sub = await s.subscriptions.retrieve(subId);
      if (sub.status === 'trialing' && !sub.cancel_at_period_end && new Date(sub.trial_end * 1000).getTime() === new Date(row.first_charge_at).getTime()) {
        return sendReminder(subId, new Date(sub.trial_end * 1000));
      }
      return false;
    }
    if (event.type === 'invoice.payment_failed') {
      const inv = await s.invoices.retrieve(obj.id);
      const subId = invoiceSubId(inv);
      const row = subId && await one('SELECT * FROM gat_subscriptions WHERE stripe_subscription_id=$1', [subId]);
      if (!row || inv.billing_reason !== 'subscription_cycle') return false;
      const claim = await db.query(`UPDATE gat_subscriptions SET failed_email_invoice=$2 WHERE stripe_subscription_id=$1
        AND failed_email_invoice IS DISTINCT FROM $2 RETURNING order_id`, [subId, inv.id]);
      if (!claim.rowCount) return false;
      const order = await one('SELECT * FROM gat_orders WHERE id=$1', [row.order_id]);
      const mail = failedEmail(order);
      return send(order.email, mail[0], mail[1]);
    }
    return false;
  }

  // ------------------------------------------------------------------ what the thank-you and account pages show
  async function summary(id, allowFinish) {
    await ready();
    let order = await one('SELECT * FROM gat_orders WHERE id=$1 AND mode=$2', [id, MODE]);
    if (!order) throw new GatError(404, 'We could not find that order.');
    let charge = await one(`SELECT * FROM gat_charges WHERE stripe_invoice_id=$1`, [order.stripe_invoice_id]);
    // The webhook normally gets here first. If it is late, the thank-you page finishes the order itself.
    if (allowFinish && (!charge || charge.state !== 'done')) {
      const inv = await stripe().invoices.retrieve(order.stripe_invoice_id);
      if (inv.status === 'paid') {
        try { await processPaidInvoice(inv); } catch (e) { log.error('GAT finish on return failed:', e.message); }
        order = await one('SELECT * FROM gat_orders WHERE id=$1', [id]);
        charge = await one(`SELECT * FROM gat_charges WHERE stripe_invoice_id=$1`, [order.stripe_invoice_id]);
      }
    }
    const sub = order.stripe_subscription_id ? await one('SELECT * FROM gat_subscriptions WHERE stripe_subscription_id=$1', [order.stripe_subscription_id]) : null;
    return {
      mode: MODE, status: order.status, option: order.option, total: order.amount_cents / 100, currency: 'USD', firstName: order.first_name,
      orderName: charge && charge.shopify_order_name || null, tracked: !!order.tracked_at,
      firstCharge: sub && sub.first_charge_at ? longDate(sub.first_charge_at) : null,
      monthly: order.option === 'trial' ? PRICE.monthly / 100 : null,
    };
  }

  async function account(id) {
    const order = await one('SELECT * FROM gat_orders WHERE id=$1 AND mode=$2', [id, MODE]);
    if (!order) throw new GatError(404, 'We could not find that order.');
    const out = { mode: MODE, firstName: order.first_name, option: order.option, monthly: PRICE.monthly / 100, active: false, canSkip: false, nextCharge: null, status: 'none' };
    if (!order.stripe_subscription_id) return { order, out };
    const sub = await stripe().subscriptions.retrieve(order.stripe_subscription_id);
    await syncSubscription(sub).catch(() => {});
    const live = ['trialing', 'active', 'past_due'].includes(sub.status) && !sub.cancel_at_period_end;
    out.status = live ? sub.status : 'cancelled';
    out.active = live;
    if (live) {
      const at = (sub.status === 'trialing' && sub.trial_end ? sub.trial_end : sub.current_period_end) * 1000;
      out.nextCharge = longDate(at);
      out.nextChargeIfSkipped = longDate(at + CYCLE_DAYS * 86400000);
      out.canSkip = sub.status !== 'past_due';
    }
    return { order, sub, out };
  }

  let portalId = null;
  async function portalConfig() {
    if (portalId) return portalId;
    const s = stripe();
    const list = await s.billingPortal.configurations.list({ limit: 100 });
    const mine = list.data.find(c => c.metadata && c.metadata.funnel === 'gat' && c.active);
    portalId = mine ? mine.id : (await s.billingPortal.configurations.create({
      metadata: { funnel: 'gat' },
      business_profile: { headline: 'SixPackAbs.com: update the card for your Great Again T monthly delivery', privacy_policy_url: SHOP_URL + '/pages/great-again-t-privacy-policy', terms_of_service_url: PAGES.terms },
      features: { payment_method_update: { enabled: true }, invoice_history: { enabled: true }, customer_update: { enabled: false },
        subscription_cancel: { enabled: false } },
    })).id;
    return portalId;
  }

  // ------------------------------------------------------------------ routes
  function router() {
    const r = express.Router();
    const json = express.json({ limit: '20kb' });
    const limiter = (max, minutes) => rateLimit({ windowMs: minutes * 60000, max, standardHeaders: true, legacyHeaders: false,
      message: { error: 'Too many tries. Please wait a few minutes and try again.' } });
    const origin = (req, res, next) => {
      const o = req.headers.origin;
      if (o && !ORIGINS.includes(o)) return res.status(403).json({ error: 'Not allowed.' });
      next();
    };
    const fail = (res, e, what) => {
      if (e instanceof GatError) return res.status(e.status).json({ error: e.message, field: e.field });
      if (e && e.type === 'StripeCardError') return res.status(402).json({ error: e.message });
      log.error(`GAT ${what} failed:`, e && e.message);
      res.status(500).json({ error: `Something went wrong and your order was not placed. Please try again, or email ${SUPPORT}.` });
    };

    r.post('/api/gat/stripe-webhook', express.raw({ type: 'application/json' }), async (req, res) => {
      if (MODE === 'off' || !WH) return res.status(503).send('not configured');
      let event;
      try { event = stripe().webhooks.constructEvent(req.body, req.headers['stripe-signature'], WH); }
      catch (e) { return res.status(400).send('bad signature'); }
      try { await handleEvent(event); res.json({ received: true }); }
      catch (e) { log.error('GAT webhook', event.type, e.message); res.status(500).send('retry'); }
    });

    r.get('/api/gat/config', (req, res) => {
      res.set('Cache-Control', 'no-store');
      res.json({ mode: MODE, open: MODE !== 'off' && !!PK, publishableKey: PK || null,
        prices: { single: PRICE.single, shipping: PRICE.ship, monthly: PRICE.monthly }, states: STATES });
    });

    r.post('/api/gat/order', origin, limiter(20, 10), json, async (req, res) => {
      try {
        if (MODE === 'off' || !PK) throw new GatError(503, `Ordering is not open yet. Please email ${SUPPORT} and we will let you know when it is.`);
        res.json(await createOrder(req.body, { ip: req.ip, ua: req.headers['user-agent'], testKey: req.headers['x-gat-test-key'] }));
      } catch (e) { fail(res, e, 'order'); }
    });

    r.get('/api/gat/order/:id', limiter(60, 10), async (req, res) => {
      try { res.set('Cache-Control', 'no-store'); res.json(await summary(clean(req.params.id, 40), true)); }
      catch (e) { fail(res, e, 'summary'); }
    });

    // The thank-you page asks before it reports the sale, so a reload or a second device never counts it twice.
    r.post('/api/gat/order/:id/tracked', origin, limiter(60, 10), async (req, res) => {
      try {
        await ready();
        const q = await db.query(`UPDATE gat_orders SET tracked_at=now() WHERE id=$1 AND mode=$2 AND status='paid' AND tracked_at IS NULL RETURNING id`,
          [clean(req.params.id, 40), MODE]);
        res.json({ first: q.rowCount === 1 });
      } catch (e) { fail(res, e, 'tracked'); }
    });

    const guard = (req, res) => {
      const id = clean(req.params.id, 40), k = String(req.query.k || (req.body && req.body.k) || '');
      if (!linkOk(id, k)) { res.status(403).json({ error: 'This link is not valid. Please use the link in your order email.' }); return null; }
      return id;
    };
    r.get('/api/gat/account/:id', limiter(60, 10), async (req, res) => {
      try { await ready(); const id = guard(req, res); if (!id) return; res.set('Cache-Control', 'no-store'); res.json((await account(id)).out); }
      catch (e) { fail(res, e, 'account'); }
    });
    r.post('/api/gat/account/:id/:action', origin, limiter(20, 10), json, async (req, res) => {
      try {
        await ready();
        const id = guard(req, res); if (!id) return;
        const { order, sub, out } = await account(id);
        const action = req.params.action;
        if (action === 'card') {
          const configuration = await portalConfig();
          const portal = await stripe().billingPortal.sessions.create({ customer: order.stripe_customer_id, return_url: accountLink(id), configuration,
            flow_data: { type: 'payment_method_update' } }).catch(() => stripe().billingPortal.sessions.create({ customer: order.stripe_customer_id, return_url: accountLink(id), configuration }));
          return res.json({ url: portal.url });
        }
        if (!sub || !out.active) throw new GatError(400, 'Your monthly delivery is already cancelled.');
        if (action === 'cancel') {
          const done = await stripe().subscriptions.cancel(sub.id);
          await syncSubscription(done);
        } else if (action === 'skip') {
          if (!out.canSkip) throw new GatError(400, 'Please update your card first.');
          const base = sub.status === 'trialing' && sub.trial_end ? sub.trial_end : sub.current_period_end;
          const moved = await stripe().subscriptions.update(sub.id, { trial_end: base + CYCLE_DAYS * 86400, proration_behavior: 'none' });
          await syncSubscription(moved);
        } else throw new GatError(404, 'Not found.');
        res.json((await account(id)).out);
      } catch (e) { fail(res, e, 'account action'); }
    });

    // Test mode only: the proof scripts run the reminder sweep at a Stripe test clock's date.
    r.post('/api/gat/test/sweep', json, async (req, res) => {
      if (!TEST_KEY || req.headers['x-gat-test-key'] !== TEST_KEY) return res.status(404).end();
      try { res.json(await sweep(new Date(req.body && req.body.now ? req.body.now : Date.now()))); } catch (e) { fail(res, e, 'sweep'); }
    });
    return r;
  }

  return { router, sweep, mode: MODE, internals: { createOrder, processPaidInvoice, handleEvent, summary, account, accountLink, prices, createShopifyOrder,
    confirmationEmail, reminderEmail, renewalEmail, cancelEmail, failedEmail } };
}

module.exports = { createGatCheckout, PRICE, STATES };
