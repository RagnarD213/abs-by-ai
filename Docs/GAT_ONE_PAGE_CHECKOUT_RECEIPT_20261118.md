# Great Again T one-page order form: build receipt (2026-11-18, Claude Fable 5.2)

Handoff executed up to the live step: `Handoffs/handoff-20261118-gat-one-page-checkout.md`. Website and payment build, no edit slot. Spend: $0 (Stripe test mode, no real charges, no AI generation).

**State: built, deployed and proven end to end in Stripe TEST mode. Hidden from visitors. Dan has not reviewed it yet. No live key is set.**
The two-step flow (our page, then Shopify checkout with `FREEMONTH`) is untouched and is what every visitor still gets.

- Test page: https://shop.sixpackabs.com/pages/great-again-t-order?onepage=1 (test card 4242 4242 4242 4242, any future date, any CVV)
- Review page (phone, tablet, desktop, the six emails): https://claude.ai/artifact/13HpHVHTeBsqDZCz7t11qn (built by `scripts/gat/build-review.py`)
- What is left (sender domain, live keys, two real card orders, switch over): `Handoffs/handoff-20261118-gat-one-page-checkout-go-live.md`

## What the buyer gets

One page, Healthy Back's layout: the two options, 1 Shipping information, 2 Order summary, 3 Payment information (card fields from Stripe Elements, inside our page), the "How this FREE Trial Offer Works" box, the required tick box, one button ("Complete My Order"), the three policy links. Then our own thank-you page, an order email, and an account page (cancel, skip a month, update card).

- Free month: $9.99 today, then $67.00 every 30 days, first $67 charge 30 days after the order. Stripe subscription with a 30-day trial and a $9.99 shipping line on the first invoice.
- One bottle: $97.00 once (a single Stripe invoice). The card is kept on the Stripe customer, so the four upsells can charge it with one click later.
- Card statement text is exactly `SIXPACKABS.COM` for every charge, verified on the test charges. This needed the charges to go through Stripe invoices: a plain charge on the shared Stripe account reads `ABS BY AI* SIXPACKABS.`.
- No sales tax, as the shop does today.

## How it is built

| Piece | Where |
|---|---|
| Payment server | `gat-checkout.js` (repo root), mounted in `server.js`, on Railway service `abs-by-ai`. Routes under `https://absbyai.com/api/gat/`: `config`, `order`, `order/:id`, `order/:id/tracked`, `account/:id` and its actions, `stripe-webhook`. Tables `gat_orders`, `gat_subscriptions`, `gat_charges` (made on first use). |
| Settings (Railway, names only) | `GAT_STRIPE_SECRET_KEY`, `GAT_STRIPE_PUBLISHABLE_KEY`, `GAT_STRIPE_WEBHOOK_SECRET` (TEST values today), `GAT_SHOPIFY_SHOP`, `GAT_SHOPIFY_CLIENT_ID`, `GAT_SHOPIFY_CLIENT_SECRET`, `GAT_LINK_SECRET`, `GAT_TEST_KEY`, `GAT_FROM`. Unset Stripe keys switch the whole thing off. Local copies: `~/.absbyai-secrets.env`. |
| Stripe (test mode, account `acct_1TemLD...`) | Webhook `we_1UdHnWAC3gM1rghl3EvW52VS` to `/api/gat/stripe-webhook`, API version 2023-10-16, five events. Prices found by lookup key: `gat_monthly_6700`, `gat_single_9700`, `gat_ship_999` (the server makes them if missing, in test and in live). |
| Shopify orders | App `gat-order-sync` (Dev Dashboard, org SixPackAbs 245324494, client id `fb4d0a71bc30debeec1473fef99d4b93`), installed on the shop 2026-11-18 with orders, customers, products and pages access. Project folder on the M2: `~/Projects/Claude/Projects/shopify-apps/gat-order-sync`. The server asks Shopify for a fresh 24-hour token as needed. |
| Pages | `refine/onepage.py` (order form, thank-you, account) and `refine/live/gat-pay.js`, hooked into `refine/build_live.py`. Versioned copy: `.claude/skills/design-sales-page/reference/gat-letter/`. New Shopify pages: `/pages/great-again-t-thank-you` (template `gat-thanks`) and `/pages/great-again-t-account` (template `gat-account`). The live funnel is now 14 pages. |
| The switch | `CFG['onePage']` in `build_live.py`: `'preview'` today (form only at `?onepage=1`), `'on'` at go-live (form for everyone, `?classic=1` brings back the two-step flow), `'off'`. |
| Proofs | `scripts/gat/`: `proof-orders.js`, `proof-renewal.js`, `proof-deployed.js`, `browser-proof.mjs`, `local-proof-server.js` (preview name `gat-order-form-test`), `build-review.py`. All Stripe test mode. |

Every paid Stripe invoice becomes one Shopify order, once: the first order (bottle $0.00, shipping $9.99), each refill ($67.00, free shipping), or the one bottle ($97.00, free shipping). The Stripe webhook does it; if the webhook is late, the thank-you page finishes the order itself. Orders are tagged `gat-one-page`, `gat-first` / `gat-renewal` / `gat-single` and `gat-inv-<Stripe invoice>`, and carry the Stripe ids as order details. If Shopify refuses an order, Stripe retries the webhook and an alert email goes to support@sixpackabs.com.

## Facts found on the way (they change how to test)

1. **The shop sends every paid order to Supliful the moment it is paid.** Test-mode orders made by the proofs were marked fulfilled within seconds. So in test mode the Shopify order is flagged test and uses a line called "Great Again T (TEST ORDER, do not ship)" instead of the real variant. The real variant `68049477796162` is used only in live mode. **Supliful receiving an order made this way is therefore proven only by the first real order** (evidence it will work: order #1005, made as a draft order in the admin, went to Supliful the same way).
2. Stripe sends webhook events in the account's default API shape, not this app's. The server reads only ids from an event and fetches the invoice or subscription again, so the shape cannot break it. Found by the renewal proof.
3. The Railway mail key can only send from absbyai.com. Until the sixpackabs.com sending domain is added in Resend (needs a sign-in: go-live handoff, step 1), test emails come from `orders@absbyai.com` with `[TEST]` in the subject.
4. On the shared Stripe account, Stripe's own card-update page shows the account name (Abs By AI). Cancel and skip are on our own account page, so the buyer only sees Stripe's page when changing a card. A separate Stripe account for SixPackAbs would remove this; it needs Dan's ID details (Codex or Grokbot).
5. Unrelated, fixed in passing: `server.js` had Dan's personal email hard-coded as the web push contact fallback (public repo). It is now the business address `dan@absbyai.com`. Web push is not switched on, so nothing changed for users.

## Proven in test mode (2026-11-18)

| What | Result |
|---|---|
| Free month, through the form in a phone-size browser | Declined card (4000 0000 0000 0002) shows "Your card has been declined."; the retry with 4242 pays $9.99 on the same order; thank-you page shows the order number and "first $67 charge is on December 18, 2026" |
| One bottle, through the form (tablet and phone sizes) | $97.00, thank-you page, no subscription |
| Free month with a separate billing address (desktop size) | Paid, order created |
| Field checks | Empty form refused field by field; free month refused until the box is ticked; an order sent from another website is refused |
| Statement text | `SIXPACKABS.COM` on the $9.99, $97.00 and $67.00 test charges |
| Shopify | A paid order for every charge, right totals and address, made once even when asked twice. 22 test orders, #1008 to #1029 (all flagged test, tagged `gat-test`; none with the real variant, none sent to Supliful). The test subscriptions and Stripe test clocks were cancelled and deleted afterwards |
| Hosted server and real webhook | Orders sent through `https://absbyai.com/api/gat/order`; the Stripe webhook made the Shopify orders (#1027 one bottle, #1028 first order, #1029 refill, and #1024 to #1026 on the first run) with no help from the thank-you page. `scripts/gat/proof-deployed.js` passes end to end |
| Renewal (Stripe test clock) | Day 30: exactly $67.00 charged, refill order made in Shopify, refill email sent |
| Reminder | Sent once, 8 days before the first $67 charge, with the amount, the date and the account page button. Nothing sent earlier, nothing sent twice |
| Skip a month | Next charge moves 30 days; no charge in the skipped month |
| Declined refill | Stripe marks it past due and the "update your card" email goes out once |
| Cancel | From the account page: subscription cancelled at once, cancel email sent, no charge 70 days later |
| Purchase tracking | The thank-you page asks the server before reporting; the first ask says yes, every later one says no. In test mode it sends `gat_purchase_test` to PostHog and nothing to Google Ads. In live mode it sends `gat_purchase` and the Google Ads conversion `AW-18361229851/RurWCMWDwbodEJvEqLNE` with value and order number. Orders made this way never pass through Shopify checkout, so the Shopify pixel does not fire for them: no double count. |
| Live shop pages | `?onepage=1` shows the form with three Stripe card fields and the red TEST MODE bar at 390, 768 and 1440 wide, no sideways scroll; without it the page is the two-step flow as before; all pages still `noindex` |
| Copy checks | `build_live.py check`: 14 pages free of Google Ads words and dashes; order page still shows both options, the terms box, the tick box and the three policy links |

Not proven, on purpose: a real card, a real Shopify order with the real variant, Supliful receiving it, and emails from @sixpackabs.com. Those are the go-live handoff.

## Defaults I picked (Dan can change)

- The order emails, thank-you page and account page wording are new and written by me (the terms box and order page wording are unchanged).
- The "Text me order updates" switch is on the form as in the mockup, off by default; the answer is saved on the Shopify order. No texts are sent by anything.
- Cancel on the account page stops the monthly delivery at once (the pages say "Canceling stops all future orders").
- United States addresses only (50 states and DC).
- The reminder goes out by our own hourly check, 8 days before the first $67 charge, so it does not depend on a Stripe setting.

## Undo

Set `CFG['onePage'] = 'off'`, build, deploy (the form disappears; nothing else changes). Remove the `GAT_STRIPE_*` settings on Railway to switch the server off. Delete the two Shopify pages, uninstall the app `gat-order-sync`, delete the Stripe test webhook, drop the three `gat_` tables.
