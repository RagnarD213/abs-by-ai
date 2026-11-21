# Great Again T one-page order form: build receipt (2026-11-18, Claude Fable 5.2)

Handoff executed up to the live step: `Handoffs/handoff-20261118-gat-one-page-checkout.md`. Website and payment build, no edit slot. Spend: $0 (Stripe test mode, no real charges, no AI generation).

**State (2026-11-20, 8:55 AM Central): LIVE FOR EVERYONE on the order page (Stripe live mode, `CFG['onePage'] = 'on'`). `?classic=1` brings back the two-step Shopify checkout. The funnel is still not launched (noindex, no ads). Open: the two real test orders are only partly undone (monthly plan cancelled; Shopify shows both refunded but Stripe has NOT returned the money; Supliful declined to cancel, so both bottles are still set to ship), and Stripe sends its own receipt in the Abs By AI name. See "Go live" at the bottom.**

- Live order page: https://shop.sixpackabs.com/pages/great-again-t-order (REAL charges since 2026-11-18 5:56 PM Central; never type a test card there). Two-step fallback: add `?classic=1`.
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

## Go live (2026-11-18, Claude Fable 5.2, its own task)

Dan split the go-live handoff: Claude does everything except the two real card orders, which are Grokbot's (`Handoffs/handoff-20261118-gat-real-test-orders-grokbot.md`).

### Part A, done before any real order

| What | Result |
|---|---|
| Stripe live keys | Railway `GAT_STRIPE_SECRET_KEY` and `GAT_STRIPE_PUBLISHABLE_KEY` now hold the live keys of the existing account (`acct_1TemLD...`, the same values as `STRIPE_SECRET_KEY` / `STRIPE_PUBLISHABLE_KEY`). `GAT_TEST_KEY` deleted. |
| Live webhook | `we_1UdIfSAC3gM1rghl4GUmOvKc` to `https://absbyai.com/api/gat/stripe-webhook`, API version 2023-10-16, the five events. Its signing secret is in Railway `GAT_STRIPE_WEBHOOK_SECRET` and in the local cache as `GAT_STRIPE_WEBHOOK_SECRET_LIVE` (the test secret keeps its old name there). The test-mode webhook `we_1UdHnW...` still exists in test mode and is harmless. |
| Live mode confirmed | `https://absbyai.com/api/gat/config` said `"mode":"live"` with a `pk_live` key at 5:56 PM Central. An unsigned call to the webhook is refused (400), an order from another website is refused. |
| Live page, look only | `GAT_PROOF=look` at phone, tablet and desktop: `?onepage=1` shows the form with three card fields and no TEST MODE bar; without it the page is the two-step flow; no sideways scroll; still `noindex`. |
| The two webhooks on one Stripe account | Checked in code: the Abs By AI webhook ignores Great Again T invoices and subscriptions (it looks them up in the members table), and the Great Again T webhook ignores Abs By AI ones (it looks them up in `gat_orders` / `gat_subscriptions`). Neither can touch the other's customers. |
| Stripe's own customer emails (read in the dashboard, nothing changed) | Settings > Business > Customer emails: **Successful payments ON, Refunds ON.** Billing > Subscriptions and emails: trial reminder OFF, upcoming renewals OFF, **expiring cards ON, failed card payments ON**, failed bank debits OFF, "manage subscription" link ON (Stripe customer portal). Abs By AI members rely on Stripe's receipts (the app does not send its own), so nothing was turned off. |

Open from Part A:

1. **Stripe receipts in the Abs By AI name.** Because "Successful payments" is on, a Great Again T buyer will get Stripe's receipt (headed Abs By AI) next to our own order email, and Stripe's failed-payment and expiring-card emails too. The two real orders will show exactly what arrives. Fix that leaves Abs By AI members alone: keep the buyer's email off the Stripe customer record (our own emails already cover the receipt, the reminder and the failed-payment notice), or a separate Stripe account for SixPackAbs. Do before launch; it does not block the test orders.
2. **Order emails still come from `orders@absbyai.com`.** Resend is not signed in in Dan's Chrome (resend.com/login), and the Railway mail key cannot add domains. Once signed in: add `sixpackabs.com`, add its DNS records at WordPress.com (root MX untouched), verify, make a sending key for that domain, set `GAT_RESEND_API_KEY` and `GAT_FROM`.
3. The server running at the moment of the switch to live was commit `2ac3eda`, one behind the card-update page fix `c4c137d`, which was still in Railway's queue (about 40 minutes behind). Only the "update my card" button on the account page is affected until it lands.

Part A items 2 and 3 above are closed: see the sender row below; the card-update fix `c4c137d` deployed overnight.

### Part B, 2026-11-19: the two real orders, the sender, the switch

**The two real orders (Grokbot, 2026-11-18 about 6:21 and 6:25 PM Central), checked from the records, not from a report:**

| | Free month | One bottle |
|---|---|---|
| Shopify order | #1030 | #1031 |
| Stripe charge | $9.99, statement text `SIXPACKABS.COM` | $97.00, statement text `SIXPACKABS.COM` |
| Stripe invoice | `in_1UdJ6MAC3gM1rghlbdYK2AvP` (shipping $9.99 + trial line $0) | `in_1UdJA2AC3gM1rghlG7m6CavM` |
| Monthly plan | $67.00 every 30 days (`gat_monthly_6700`), in trial, first charge December 18, 2026 | none |
| Shopify | Paid, not a test order, real variant `68049477796162`, bottle $0.00 + shipping $9.99, tags `gat-one-page`, `gat-first` | Paid, not a test order, real variant, $97.00, free shipping, tags `gat-one-page`, `gat-single` |
| Supliful | Shopify timeline: "Fulfillment of 1 item was requested from Supliful Fulfillment", then "Supliful accepted the request" two seconds later. Status In progress | Same, accepted one second later. Status In progress |
| `gat_charges` | `first`, 999, `done`, emailed | `single`, 9700, `done`, emailed |
| Order email | Arrived in the inbox, "Your free bottle of Great Again T is on the way (order #1030)", from orders@absbyai.com (the sender at the time) | Arrived, "Your Great Again T order #1031", same sender |
| PostHog | one `gat_purchase`, flow `one-page`, 9.99 | one `gat_purchase`, flow `one-page`, 97 |

**Supliful receiving an order made this way is now proven** (the one thing test mode could not show). Supliful's own dashboard was not seen by Claude; the proof is Shopify's timeline entry that Supliful accepted each request.

Not as planned:

1. **The undo is PARTLY done (checked from the records 2026-11-20 8:52 AM Central).** Done on 2026-11-19: the $67 monthly plan was cancelled at 1:29 PM Central (Stripe subscription `canceled`, cancel email sent, no December charge will happen). At 5:02 PM Central someone in the Shopify admin asked Supliful to cancel both orders and **Supliful declined both requests**, then recorded a refund on each Shopify order ($9.99 on #1030, $97.00 on #1031). **Those Shopify refunds are bookkeeping only**: the orders were paid outside Shopify (Stripe, through `gat-order-sync`), so Shopify cannot send the money back. In Stripe both charges still read `succeeded`, refunded $0.00. Still open: refund $9.99 and $97.00 in the Stripe dashboard (so Stripe matches Shopify and the money returns to Dan's card); both orders are still "In progress" with Supliful and no shipment is recorded yet, so two bottles will ship unless Supliful support stops them. Lesson for real refunds later: a refund on a one-page order must be made in Stripe; a refund pressed in Shopify moves no money. Prompts for what is left: `Handoffs/handoff-20261118-gat-real-test-orders-grokbot.md`.
2. No declined-card attempt shows in Stripe for either customer, so the wrong-CVV check was probably skipped on the live page (it passed in test mode).
3. **Stripe's own receipt went out for both orders**, "Your receipt from Abs By AI #2844-6305" and "#2996-2191", from Stripe's invoice address with the sender name Abs By AI. A real buyer would get it next to our order email. Pre-launch fix (not done, needs Dan's yes because it changes payment code): keep the buyer's email off the Stripe customer record, or a separate Stripe account.

**Order emails from orders@sixpackabs.com (done 2026-11-19):**

- Resend: domain `sixpackabs.com` added (North Virginia, us-east-1) and Verified. Codex added it and read the records through Dan's signed-in Chrome; Claude added the DNS at WordPress.com: TXT `resend._domainkey`, CNAME `send` to `send.forge.rmta.net`, CNAME `rsend` to `rsend.forge.rmta.net`. Root MX, root SPF, `_dmarc` and every other record untouched.
- Key: `gat-orders-sixpackabs`, Sending access, sixpackabs.com only. Dan pressed Add himself (Codex's computer use will not create a key without a person's confirmation, and it refused a Full access key outright; plan around that). The value is in Railway `GAT_RESEND_API_KEY` and the local cache under the same name.
- Railway `GAT_FROM` is `SixPackAbs.com <orders@sixpackabs.com>`. Proof: a setup test sent with the new key from orders@sixpackabs.com to support@sixpackabs.com arrived in the inbox. The old absbyai.com key is refused for sixpackabs.com (403), so the new key is required. No real order has gone out with the new sender yet.

**The switch (2026-11-19, about 1:00 PM Central):**

- `CFG['onePage'] = 'on'` in `refine/build_live.py`, `python3 build_live.py --no-export` (PASS: 14 pages, copy checks), `gen.py`, `page.css`, `letterdoc.py`, `infodoc.py` matched the gat-letter copies, `./deploy_live.sh`. Only three generated files changed (`assets/gat.js`, `assets/gat-pay.js`, `layout/gat.liquid`); theme repo commit `499449a`. `build_live.py` copied to the gat-letter folder.
- Live, look only, at phone, tablet and desktop: `/pages/great-again-t-order` shows the form with three card fields and no TEST MODE bar; `?classic=1` shows the two-step flow; `?option=single` shows the form; no sideways scroll; still `noindex`. `LAUNCHED` is still False.

Trap found on the way: the Claude Chrome extension in this task was attached to a different Chrome than the one on Dan's screen, so a sign-in Dan did could not be used and he could not see "the tab". Check which Chrome the extension drives (open a marked address, look for it with `osascript` in Dan's Chrome) before asking him to sign in anywhere.
