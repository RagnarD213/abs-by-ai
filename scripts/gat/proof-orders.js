// API-level proof in Stripe TEST mode against the module directly (no browser): both options, a decline, Shopify order, emails.
const path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const { env } = require('./env.js');
process.env.DATABASE_URL = env.DATABASE_URL;
const { pool: db, initDb } = require(ROOT + '/db.js');
const express = require(ROOT + '/node_modules/express'), rateLimit = require(ROOT + '/node_modules/express-rate-limit');
const { createGatCheckout } = require(ROOT + '/gat-checkout.js');
const stripe = require(ROOT + '/node_modules/stripe')(env.GAT_STRIPE_SECRET_KEY);
const gat = createGatCheckout({ db, dbReady: Promise.resolve(), express, rateLimit, env: Object.assign({}, env, { GAT_FROM: process.env.GAT_FROM || env.GAT_FROM || 'SixPackAbs.com <orders@absbyai.com>' }) });
const I = gat.internals;
const buyer = (option, extra) => Object.assign({ option, firstName: 'Testy', lastName: 'McTest', email: process.env.TEST_TO || 'delivered@resend.dev', phone: '512-555-0100',
  shipping: { address1: '100 Test Lane', address2: 'Apt 2', city: 'Austin', state: 'TX', zip: '78701' }, agree: option === 'trial', sms: false }, extra || {});
(async () => {
  console.log('mode', gat.mode);
  for (const option of (process.env.ONLY ? [process.env.ONLY] : ['trial', 'single'])) {
    const o = await I.createOrder(buyer(option), { ip: '127.0.0.1', ua: 't1' });
    const piId = o.clientSecret.split('_secret_')[0];
    console.log(option, 'order', o.orderId, 'amount', o.amount);
    // a declined card first, then a good one on the SAME order
    const bad = await stripe.paymentIntents.confirm(piId, { payment_method: 'pm_card_chargeDeclined' }).catch(e => ({ declined: e.code + ' / ' + e.message }));
    console.log('  decline ->', bad.declined || bad.status);
    const again = await I.createOrder(buyer(option, { orderId: o.orderId }), { ip: '127.0.0.1', ua: 't1' });
    console.log('  retry reuses the same order and payment:', again.orderId === o.orderId && again.clientSecret === o.clientSecret);
    const pending = await I.summary(o.orderId, true);
    console.log('  before payment status:', pending.status, pending.orderName);
    const ok = await stripe.paymentIntents.confirm(piId, { payment_method: 'pm_card_visa' });
    const ch = await stripe.charges.retrieve(ok.latest_charge);
    console.log('  paid ->', ok.status, ok.amount, 'statement:', ch.calculated_statement_descriptor);
    const sum = await I.summary(o.orderId, true);
    console.log('  summary', JSON.stringify(sum));
    const sum2 = await I.summary(o.orderId, true);
    console.log('  second call makes no second order:', sum2.orderName === sum.orderName);
    console.log('  account link', I.accountLink(o.orderId).replace(/k=.*/, 'k=...'));
  }
  const rows = await db.query(`SELECT c.kind, c.amount_cents, c.state, c.shopify_order_name, c.email_sent_at IS NOT NULL AS emailed, c.last_error FROM gat_charges c ORDER BY c.created_at DESC LIMIT 4`);
  console.table(rows.rows);
  await db.end();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
