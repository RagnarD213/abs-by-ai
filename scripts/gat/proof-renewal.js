// Renewal, reminder, skip, failed card and cancel on a Stripe TEST CLOCK (time is simulated; no real waiting, no real money).
const path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const { env } = require('./env.js');
process.env.DATABASE_URL = env.DATABASE_URL;
const { pool: db } = require(ROOT + '/db.js');
const express = require(ROOT + '/node_modules/express'), rateLimit = require(ROOT + '/node_modules/express-rate-limit');
const stripe = require(ROOT + '/node_modules/stripe')(env.GAT_STRIPE_SECRET_KEY);
const gat = require(ROOT + '/gat-checkout.js').createGatCheckout({ db, dbReady: Promise.resolve(), express, rateLimit, env: Object.assign({}, env, { GAT_FROM: process.env.GAT_FROM || env.GAT_FROM || 'SixPackAbs.com <orders@absbyai.com>' }) });
const I = gat.internals, DAY = 86400;
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function advance(clock, to) {
  await stripe.testHelpers.testClocks.advance(clock, { frozen_time: to });
  for (;;) { const c = await stripe.testHelpers.testClocks.retrieve(clock); if (c.status === 'ready') return; if (c.status === 'internal_failure') throw new Error('clock failed'); await sleep(2500); }
}
// What the deployed webhook does for each event, replayed here from Stripe's own event log for this customer.
async function replay(customer, seen) {
  const types = ['invoice.paid', 'invoice.upcoming', 'invoice.payment_failed', 'customer.subscription.updated', 'customer.subscription.deleted'];
  const evs = (await stripe.events.list({ limit: 100, types })).data.filter(e => (e.data.object.customer === customer) && !seen.has(e.id)).reverse();
  for (const e of evs) { seen.add(e.id); const r = await I.handleEvent(e).catch(x => 'ERROR ' + x.message); console.log('    event', e.type, '->', JSON.stringify(r === true || r === false ? r : (r && (r.kind || r.skipped || (r.duplicate && 'duplicate'))) || r)); }
}
(async () => {
  const t0 = Math.floor(Date.now() / 1000);
  const clock = (await stripe.testHelpers.testClocks.create({ frozen_time: t0, name: 'gat-renewal-proof' })).id;
  const body = { option: 'trial', firstName: 'Clock', lastName: 'Tester', email: process.env.TEST_TO || 'delivered@resend.dev', phone: '512-555-0101',
    shipping: { address1: '200 Clock St', city: 'Georgetown', state: 'TX', zip: '78628' }, agree: true, testClock: clock };
  const o = await I.createOrder(body, { ip: '127.0.0.1', ua: 't2', testKey: env.GAT_TEST_KEY });
  const piId = o.clientSecret.split('_secret_')[0];
  await stripe.paymentIntents.confirm(piId, { payment_method: 'pm_card_visa' });
  const seen = new Set();
  const row = async () => (await db.query('SELECT s.status, s.first_charge_at, s.next_charge_at, s.reminder_sent_at IS NOT NULL AS reminded, s.canceled_at IS NOT NULL AS cancelled, o.stripe_subscription_id AS sub, o.stripe_customer_id AS cus FROM gat_orders o LEFT JOIN gat_subscriptions s ON s.stripe_subscription_id=o.stripe_subscription_id WHERE o.id=$1', [o.orderId])).rows[0];
  console.log('DAY 0: first order', JSON.stringify(await I.summary(o.orderId, true)));
  let r = await row(); const cus = r.cus, sub = r.sub;
  await replay(cus, seen);
  console.log('  day 20 sweep (too early):', JSON.stringify(await gat.sweep(new Date((t0 + 20 * DAY) * 1000))));
  await advance(clock, t0 + 24 * DAY);
  await replay(cus, seen);
  console.log('DAY 24 sweep (6 days before the first $67):', JSON.stringify(await gat.sweep(new Date((t0 + 24 * DAY) * 1000))), 'reminded:', (await row()).reminded);
  console.log('  second sweep sends nothing:', JSON.stringify(await gat.sweep(new Date((t0 + 24 * DAY) * 1000))));
  await advance(clock, t0 + 30 * DAY + 2 * 3600);
  await replay(cus, seen);
  let invs = (await stripe.invoices.list({ subscription: sub, limit: 10 })).data;
  console.log('DAY 30: invoices', invs.map(i => `${i.billing_reason} ${i.amount_paid} ${i.status}`).join(' | '));
  const ren = invs.find(i => i.billing_reason === 'subscription_cycle');
  const ch = await stripe.charges.retrieve(ren.charge);
  console.log('  renewal charged', ren.amount_paid, 'statement:', ch.calculated_statement_descriptor, 'row:', JSON.stringify(await row()));
  // skip a month on the account page
  const acct = await I.account(o.orderId);
  console.log('  account page shows:', JSON.stringify(acct.out));
  const moved = await stripe.subscriptions.update(sub, { trial_end: acct.sub.current_period_end + 30 * DAY, proration_behavior: 'none' });
  await replay(cus, seen);
  console.log('SKIP: next charge moved to day', Math.round((moved.trial_end - t0) / DAY), 'row next:', (await row()).next_charge_at);
  await advance(clock, t0 + 61 * DAY);
  await replay(cus, seen);
  invs = (await stripe.invoices.list({ subscription: sub, limit: 10 })).data;
  console.log('DAY 61 (skipped month): invoices', invs.map(i => `${i.billing_reason} ${i.amount_paid} ${i.status}`).join(' | '));
  // the card starts failing, then day 90 renewal
  const cust = await stripe.customers.retrieve(cus);
  const badPm = await stripe.paymentMethods.attach('pm_card_chargeCustomerFail', { customer: cus });
  await stripe.subscriptions.update(sub, { default_payment_method: badPm.id });
  await advance(clock, t0 + 90 * DAY + 2 * 3600);
  await replay(cus, seen);
  invs = (await stripe.invoices.list({ subscription: sub, limit: 10 })).data;
  console.log('DAY 90 (declined renewal): invoices', invs.map(i => `${i.billing_reason} ${i.amount_due} ${i.status}`).join(' | '), 'sub:', (await stripe.subscriptions.retrieve(sub)).status);
  // cancel from the account page
  const done = await stripe.subscriptions.cancel(sub);
  await replay(cus, seen);
  console.log('CANCEL:', done.status, 'row:', JSON.stringify(await row()), 'account:', JSON.stringify((await I.account(o.orderId)).out));
  await advance(clock, t0 + 125 * DAY);
  await replay(cus, seen);
  invs = (await stripe.invoices.list({ customer: cus, limit: 10 })).data;
  console.log('DAY 125 after cancel: paid invoices', invs.filter(i => i.status === 'paid').map(i => i.amount_paid).join(', '), '(no new charge)');
  console.table((await db.query('SELECT kind, amount_cents, state, shopify_order_name, email_sent_at IS NOT NULL AS emailed FROM gat_charges WHERE order_id=$1 ORDER BY created_at', [o.orderId])).rows);
  console.log(JSON.stringify({ clock, cus, sub, order: o.orderId }));
  await db.end();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
