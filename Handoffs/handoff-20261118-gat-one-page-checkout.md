# Great Again T: one-page checkout (pay on our order page, no second Shopify step)

Written 2026-11-18 by Claude (Fable 5.2). Website and payment build, not video: no edit slot.
**Recommended: Claude Fable 5.2, high effort, fresh session on the M6** (AGENTS.md: payment and shop builds are Fable's). This session's context is too long to build it safely.

## What Dan asked (2026-11-18)

"I want to build a page where they could pay all on one page. I don't want to have this secondary Shopify checkout, which I think isn't going to convert... eliminate the two-step checkout, just all in one step here."

## Why it needs a build

Shopify only takes card details on its own checkout page (anything else needs Shopify Plus). So paying on our page means taking the payment ourselves and telling Shopify about each paid order so Supliful still ships it. The approved mockup already shows this page: `refine/4-checkout.html` (Healthy Back's one-page order form: options, shipping, order summary, card, terms box, tick box, one button). Build that, for real.

## Goal

On https://shop.sixpackabs.com/pages/great-again-t-order the buyer picks an option, types shipping and card details, ticks the box and pays, all on that page. No Shopify checkout step. Free month: $9.99 today, then $67 every month until cancelled. One bottle: $97 once.

## Recommended design (change it if you find a better way)

1. **Payment: Stripe**, card fields from Stripe Elements placed inside our page (card numbers never touch our server). Start in Stripe **test mode** with the test keys already in `~/.absbyai-secrets.env` (`STRIPE_TEST_*`), and prove the whole flow there before any live key.
2. **Billing:** free month = a Stripe subscription at $67 a month whose first invoice is $9.99 (shipping), next charge 30 days later. One bottle = a single $97 payment. Statement text `SIXPACKABS.COM`.
3. **Fulfilment:** every paid charge (first order and each monthly renewal, from Stripe's webhook) creates a paid order in Shopify through the Admin API, so Supliful ships it and Shopify stays the order record. Use the Great Again T variant `68049477796162`. This needs a Shopify custom app token (Settings > Apps > Develop apps: orders, customers, products). Check first that Supliful fulfils orders created by API; if it does not, ask Supliful support in their chat.
4. **Server:** a few endpoints on the existing Railway app (`server.js` already runs Stripe, webhooks, Postgres and Resend): create the payment, the Stripe webhook, cancel. The order page on the shop calls them (allow `shop.sixpackabs.com` only).
5. **Page:** generate it from `refine/build_live.py` `order_body()` (never hand-edit the theme). Bring back the shipping and payment sections from `gen.checkout()`. Keep the terms box, the required tick box, the three policy links and both option rows. Works on a phone first.
6. **After payment:** our own thank-you page. This is also where the four upsell videos (GAT Upsell 1 to 4, WV-04 to WV-07) can be offered with one click on the saved card later. Leave a clean hook for that; do not build the upsells now.
7. **Emails:** order confirmation, and the reminder 7 days before the first $67 charge (Stripe's upcoming-invoice webhook; the compliance pages promise this email). Send through Resend from the sixpackabs.com domain. These are order emails to the buyer, not marketing.
8. **Cancel and manage:** Stripe's customer portal link in every order email, plus email to support@sixpackabs.com. The compliance pages say "cancel online from your account page": the portal is that page.
9. **Tracking:** fire the same events as now (`gat_checkout_start`, `gat_purchase`) and the Google Ads conversion `AW-18361229851/RurWCMWDwbodEJvEqLNE` on the thank-you page, value and order id included. The Shopify pixel then no longer fires for these orders; do not double count.

## Decisions already made (do not reopen)

Prices, the terms box wording, the tick box, support@sixpackabs.com everywhere, the Google Ads word list, and the design of the page. The current two-step flow (our page, then Shopify checkout with code `FREEMONTH`, plan $57.01 + $9.99 shipping) stays live and working until the new page is proven; then switch the page over and keep the old flow as the fallback.

## Defaults Claude picked for Dan to change

- **Which Stripe account for live:** the existing Rose Digital Holdings account, with the statement text above. A separate Stripe account for SixPackAbs would keep the two businesses' card processing apart; opening one needs Dan's ID details (Codex or Grokbot).
- Monthly billing every 30 days from the order date.
- Sales tax: none collected, as the shop does today.

## Steps

1. Read `Docs/GAT_SALES_PAGE_BUILD_RECEIPT_20261117.md` and the generator (`refine/gen.py`, `build_live.py`, `live/gat.js`).
2. Build in Stripe test mode end to end: both options, declined card, webhook, Shopify order created (use a Shopify test or draft order first), emails, cancel, a renewal (advance Stripe's test clock 30 days), the 7-day reminder.
3. Verify on phone, tablet and desktop. Show Dan the test-mode page before going live.
4. Go live: live keys, one real order of each option (card entry: Codex or Grokbot), cancel and refund them, then switch the sales page buttons to the new page.
5. Update the receipt, mark this handoff executed in `Handoffs/README.md`.

## Limits

No ads turned on. No marketing email. Do not change the other five products. No card number, key or token in the repo (it is public). Live charges only in step 4.

## Done looks like

A buyer completes either option on one page on a phone, Shopify shows the paid order, Supliful receives it, the monthly charge is exactly $67, the reminder and cancel paths work, and the old two-step flow is still available as a fallback.
