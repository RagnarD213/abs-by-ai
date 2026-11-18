// Great Again T one-page order form: proof against the DEPLOYED server (https://absbyai.com), Stripe TEST mode only.
// Unlike proof-orders.js and proof-renewal.js this never calls the module directly: orders go in through the public
// API the shop page uses, and the Shopify orders must be made by the real Stripe webhook. Time is a Stripe test clock.
//   node scripts/gat/proof-deployed.js            emails go to Resend's test inbox
//   TEST_TO=you@example.com node scripts/gat/proof-deployed.js     send the test emails to a real inbox instead
const crypto = require('crypto');
const path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const { env } = require('./env.js');
process.env.DATABASE_URL = env.DATABASE_URL;
const { pool: db } = require(ROOT + '/db.js');
const stripe = require(ROOT + '/node_modules/stripe')(env.GAT_STRIPE_SECRET_KEY);
const BASE = process.env.GAT_BASE || 'https://absbyai.com', DAY = 86400;
const TO = process.env.TEST_TO || 'delivered@resend.dev';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const key = id => crypto.createHmac('sha256', env.GAT_LINK_SECRET).update('acct:' + id).digest('hex').slice(0, 32);
async function call(p, body, headers) {
  const r = await fetch(BASE + p, body === undefined ? {} : { method: 'POST', headers: Object.assign({ 'Content-Type': 'application/json', Origin: 'https://shop.sixpackabs.com' }, headers || {}), body: JSON.stringify(body) });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`${p} -> ${r.status} ${j.error || ''}`);
  return j;
}
async function advance(clock, to) {
  await stripe.testHelpers.testClocks.advance(clock, { frozen_time: to });
  for (;;) { const c = await stripe.testHelpers.testClocks.retrieve(clock); if (c.status === 'ready') return; if (c.status === 'internal_failure') throw new Error('clock failed'); await sleep(2500); }
}
// Waits for the WEBHOOK to finish a charge. Reads the database only, so nothing here can do the webhook's work for it.
async function charge(orderId, kind, seconds = 120) {
  for (let i = 0; i < seconds / 3; i++) {
    const r = (await db.query(`SELECT kind, amount_cents, state, shopify_order_name, email_sent_at IS NOT NULL AS emailed, last_error FROM gat_charges WHERE order_id=$1 AND kind=$2`, [orderId, kind])).rows[0];
    if (r && r.state === 'done') return r;
    await sleep(3000);
  }
  return (await db.query(`SELECT kind, state, last_error FROM gat_charges WHERE order_id=$1 AND kind=$2`, [orderId, kind])).rows[0] || { state: 'webhook never arrived' };
}
const buyer = (option, extra) => Object.assign({ option, firstName: 'Deployed', lastName: 'Proof', email: TO, phone: '512-555-0103',
  shipping: { address1: '400 Hosted Ave', city: 'Georgetown', state: 'TX', zip: '78628' }, agree: option === 'trial' }, extra || {});

(async () => {
  const cfg = await call('/api/gat/config');
  if (cfg.mode !== 'test') throw new Error('the deployed server is in ' + cfg.mode + ' mode: this proof is for test mode only');
  console.log('deployed server:', BASE, '| mode', cfg.mode, '| prices', JSON.stringify(cfg.prices));
  const wrong = await fetch(BASE + '/api/gat/order', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: 'https://not-our-shop.example' }, body: '{}' });
  console.log('order from another website is refused:', wrong.status === 403);
  const noTick = await call('/api/gat/order', buyer('trial', { agree: false })).catch(e => e.message);
  console.log('free month without the tick box is refused:', String(noTick).includes('400'));

  // ---- one bottle, with a declined card first
  const single = await call('/api/gat/order', buyer('single'));
  const sPi = single.clientSecret.split('_secret_')[0];
  const dec = await stripe.paymentIntents.confirm(sPi, { payment_method: 'pm_card_chargeDeclined' }).catch(e => e.code);
  await stripe.paymentIntents.confirm(sPi, { payment_method: 'pm_card_visa' });
  console.log('ONE BOTTLE: declined first (' + dec + '), then paid', single.amount, '->', JSON.stringify(await charge(single.orderId, 'single')));

  // ---- free month on a test clock
  const t0 = Math.floor(Date.now() / 1000);
  const clock = (await stripe.testHelpers.testClocks.create({ frozen_time: t0, name: 'gat-deployed-proof' })).id;
  const trial = await call('/api/gat/order', buyer('trial', { testClock: clock }), { 'X-GAT-Test-Key': env.GAT_TEST_KEY });
  await stripe.paymentIntents.confirm(trial.clientSecret.split('_secret_')[0], { payment_method: 'pm_card_visa' });
  console.log('FREE MONTH day 0: paid', trial.amount, '->', JSON.stringify(await charge(trial.orderId, 'first')));
  console.log('  thank-you page data:', JSON.stringify(await call('/api/gat/order/' + trial.orderId)));
  console.log('  reported once:', (await call('/api/gat/order/' + trial.orderId + '/tracked', {})).first, 'then', (await call('/api/gat/order/' + trial.orderId + '/tracked', {})).first);
  const sub = (await db.query('SELECT stripe_subscription_id AS s FROM gat_orders WHERE id=$1', [trial.orderId])).rows[0].s;
  const row = async () => (await db.query('SELECT status, first_charge_at, next_charge_at, reminder_sent_at IS NOT NULL AS reminded, canceled_at IS NOT NULL AS cancelled FROM gat_subscriptions WHERE stripe_subscription_id=$1', [sub])).rows[0];

  await advance(clock, t0 + 22 * DAY);
  console.log('  day 22 sweep:', JSON.stringify(await call('/api/gat/test/sweep', { now: new Date((t0 + 22 * DAY) * 1000).toISOString() }, { 'X-GAT-Test-Key': env.GAT_TEST_KEY })), '| reminded:', (await row()).reminded, '(8 days before the first $67 charge)');
  await sleep(4000);
  console.log('  reminder on record:', (await row()).reminded);
  await advance(clock, t0 + 30 * DAY + 2 * 3600);
  const ren = await charge(trial.orderId, 'renewal', 180);
  const inv = (await stripe.invoices.list({ subscription: sub, limit: 5 })).data.find(i => i.billing_reason === 'subscription_cycle');
  console.log('FREE MONTH day 30: Stripe charged', inv && inv.amount_paid, '->', JSON.stringify(ren));

  // ---- the account page's server side
  const k = key(trial.orderId);
  console.log('ACCOUNT:', JSON.stringify(await call(`/api/gat/account/${trial.orderId}?k=${k}`)));
  const bad = await fetch(`${BASE}/api/gat/account/${trial.orderId}?k=${'0'.repeat(32)}`);
  console.log('  a wrong link is refused:', bad.status === 403);
  console.log('  skip a month ->', (await call(`/api/gat/account/${trial.orderId}/skip`, { k })).nextCharge);
  console.log('  update card -> Stripe page opens:', /^https:\/\/billing\.stripe\.com\//.test((await call(`/api/gat/account/${trial.orderId}/card`, { k })).url));
  console.log('  cancel ->', JSON.stringify(await call(`/api/gat/account/${trial.orderId}/cancel`, { k })));
  await advance(clock, t0 + 100 * DAY);
  const paid = (await stripe.invoices.list({ subscription: sub, limit: 10, status: 'paid' })).data.map(i => i.amount_paid).filter(Boolean);
  console.log('  70 days after cancelling: charges ever made', paid.join(' + '), '| record:', JSON.stringify(await row()));
  console.log(JSON.stringify({ clock, trialOrder: trial.orderId, singleOrder: single.orderId }));
  await db.end();
})().catch(e => { console.error('FAILED', e.message); process.exit(1); });
