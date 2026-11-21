# Great Again T one-page order form: go live (sender setup, live keys, two real card orders, switch over)

Written 2026-11-18 by Claude (Fable 5.2). Website and payment work, not video: no edit slot.
For **Codex (newest Sol, high) and Grokbot**: it needs a sign-in to Resend and two real card payments, which Claude cannot type.

**Fire after Dan has looked at the test-mode page** (he has not reviewed it yet). Once he says go, Dan authorizes whoever runs this to do every step: sign in, create the sending domain and its key, set the live keys, pay for the two test orders with his card, refund and cancel them, and switch the page over. Do not stop to ask him. No secret value goes into a repo file (the repo is public); keys live in Railway and in `~/.absbyai-secrets.env`.

Read first: `Docs/GAT_ONE_PAGE_CHECKOUT_RECEIPT_20261118.md` (what is built, how it was proven, every ID).

## Where things stand

- The one-page form is built and proven end to end in Stripe TEST mode. It is on the live shop but hidden: it only shows at
  https://shop.sixpackabs.com/pages/great-again-t-order?onepage=1 . Without `?onepage=1` the page is still the two-step flow (Shopify checkout), unchanged.
- Server: `gat-checkout.js` in the Abs By AI app on Railway (service `abs-by-ai`), settings named `GAT_*`. Today they hold Stripe TEST keys.
- Shopify orders are made by the app `gat-order-sync` (already installed). In test mode the Shopify order is flagged test and uses a line called "Great Again T (TEST ORDER, do not ship)", because this shop sends every paid order to Supliful the moment it is paid. In live mode the order uses the real Great Again T variant `68049477796162`.

## Steps

1. **Order emails from @sixpackabs.com (Resend).** The Railway mail key can only send from absbyai.com, so test emails currently come from `orders@absbyai.com`. Sign in at resend.com (Dan's account), Domains > Add domain `sixpackabs.com`. Add the DNS records Resend shows (DKIM `resend._domainkey` TXT, and the MX and SPF TXT on the `send` subdomain) at WordPress.com, where the domain's DNS lives. Do not touch the existing root MX records (they forward support@ to Dan). Verify the domain, create an API key with Sending access limited to sixpackabs.com, then on Railway set `GAT_RESEND_API_KEY` to it and `GAT_FROM` to `SixPackAbs.com <orders@sixpackabs.com>`. Check: `TEST_TO=support@sixpackabs.com node scripts/gat/proof-deployed.js` and confirm the emails arrive from orders@sixpackabs.com.
2. **Stripe live keys.** On Railway set `GAT_STRIPE_SECRET_KEY` and `GAT_STRIPE_PUBLISHABLE_KEY` to the live keys of the Stripe account Dan picks (default: the existing Rose Digital Holdings account, the same values as `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY`). In that account's LIVE mode add a webhook endpoint `https://absbyai.com/api/gat/stripe-webhook`, API version `2023-10-16`, events `invoice.paid`, `invoice.upcoming`, `invoice.payment_failed`, `customer.subscription.updated`, `customer.subscription.deleted`; put its signing secret in `GAT_STRIPE_WEBHOOK_SECRET`. Delete `GAT_TEST_KEY`. After the deploy, `https://absbyai.com/api/gat/config` must say `"mode":"live"`. The products and prices are created by the server on the first order.
3. **Stripe's own customer emails.** In Stripe > Settings > Billing > Subscriptions and emails, and Settings > Customer emails: if "successful payments" or "upcoming renewals" emails are on, they would go to Great Again T buyers under the Abs By AI name. Report what is on; turn them off only if they are not needed by Abs By AI members (the app sends its own).
4. **Two real orders** at `...great-again-t-order?onepage=1`, on a phone-size window:
   - Free month: expect $9.99 today. Confirm: thank-you page with the order number and the first $67 date; Stripe shows a $9.99 charge with statement text `SIXPACKABS.COM` and a subscription in trial at $67 every 30 days; Shopify shows a paid, non-test order (bottle $0.00, shipping $9.99) and its fulfilment goes "In progress" (sent to Supliful); Supliful's dashboard shows the order; the confirmation email arrives with the account page link; PostHog has one `gat_purchase` event (flow `one-page`) and Google Ads shows the conversion `Great Again T Purchase`. Reload the thank-you page: no second event.
   - One bottle: expect $97.00, no subscription, Shopify order paid with free shipping.
   - Also try one declined card (any card with a wrong CVV): the page must show the bank's message and let the next try go through on the same order.
5. **Undo the test orders.** Open the account link from the free-month email and press Cancel My Monthly Delivery (check the cancel email). Refund both charges in Stripe. Cancel both Shopify orders and stop them in Supliful unless Dan wants the bottles (default: cancel both).
6. **Switch over.** In `Media/research/gat-sales-page-contest-20261117/refine/build_live.py` set `CFG['onePage'] = 'on'`, run `python3 build_live.py --no-export`, then `./deploy_live.sh`. Now everyone gets the one-page form, and `?classic=1` brings back the two-step Shopify checkout (the fallback; keep discount `FREEMONTH`, the $57.01 plan and the Shopify pixel in place). Copy the changed files to `.claude/skills/design-sales-page/reference/gat-letter/` and push.
7. Add the results to `Docs/GAT_ONE_PAGE_CHECKOUT_RECEIPT_20261118.md`, and mark this handoff and `handoff-20261118-gat-one-page-checkout.md` executed in `Handoffs/README.md`.

## Limits

No ads turned on. No marketing email. Do not change the other five products, the page copy or the prices. Real charges only in step 4, and they are refunded in step 5.

## Done looks like

Both real orders are in the receipt with their totals and Shopify order numbers, Supliful received them, the monthly plan reads $67 every 30 days, the test subscription is cancelled and both charges are refunded, emails come from orders@sixpackabs.com, and the order page shows the one-page form to everyone with `?classic=1` as the fallback.

## Starter prompts

**Codex (GPT-6.2 Sol, high):**

> Read and execute `Handoffs/handoff-20261118-gat-one-page-checkout-go-live.md` in the Abs By AI project. Dan has reviewed the test-mode order page and authorizes every step, including signing in to Resend, creating the sending domain and key, setting the live Stripe keys on Railway, paying for the two real test orders with his card, refunding and cancelling them, and switching the page over. Do not stop to ask him. Keep secrets out of repo files.

**Grokbot (self-contained):**

> Finish the Great Again T one-page order form for Dan Rose (SixPackAbs.com, Shopify store 1yar3v-ie). Dan authorizes every step below, including sign-ins and card payments; do not stop to ask him. (1) In Resend (Dan's account) add the sending domain sixpackabs.com, add the DNS records it shows at WordPress.com without touching the root MX records, verify it, create a Sending-access API key limited to that domain, and on Railway (project invigorating-liberation, service abs-by-ai) set GAT_RESEND_API_KEY to the key and GAT_FROM to "SixPackAbs.com <orders@sixpackabs.com>". (2) In Stripe (Rose Digital Holdings account, live mode) add a webhook endpoint https://absbyai.com/api/gat/stripe-webhook with API version 2023-10-16 and events invoice.paid, invoice.upcoming, invoice.payment_failed, customer.subscription.updated, customer.subscription.deleted; on Railway set GAT_STRIPE_SECRET_KEY and GAT_STRIPE_PUBLISHABLE_KEY to the live keys and GAT_STRIPE_WEBHOOK_SECRET to the endpoint's signing secret, and delete GAT_TEST_KEY. Wait for the deploy; https://absbyai.com/api/gat/config must say mode live. (3) At https://shop.sixpackabs.com/pages/great-again-t-order?onepage=1 place two real orders with Dan's card: the free month ($9.99 today, then $67 every 30 days) and one bottle ($97). For each confirm the thank-you page shows an order number, Stripe shows the charge with statement text SIXPACKABS.COM, Shopify shows a paid order that goes to "In progress", Supliful received it, and the confirmation email arrived. (4) Cancel the monthly delivery from the account link in the free-month email, refund both charges in Stripe, cancel both Shopify orders and stop them in Supliful. (5) Report every total, order number and anything that failed. Do not turn on ads, send marketing email, or change prices or page copy.
