# Great Again T one-page order form: the two real card orders (Grokbot only)

Written 2026-11-18 by Claude (Fable 5.2). Website and payment work, not video: no edit slot.
For **Grokbot**. It needs Dan's card typed into the live order page and refunds pressed in the Stripe dashboard, which Claude cannot do.

Dan's words (2026-11-18): "Make a handoff for Grokbot to just do the test transactions ... Make a handoff for Claude to handle the rest of this besides the test transactions in a new task."

This is the split of `handoff-20261118-gat-one-page-checkout-go-live.md`: Grokbot owns its steps 4 and 5 (this file). Claude owns steps 1, 2, 3, 6 and 7 and runs them in its own task (live keys, order emails, Stripe email check, verifying the orders from the records, switching the page over, receipts).

## Fire only when live mode is on

Claude switched the payment server to the live Stripe keys on 2026-11-18. Check before firing: https://absbyai.com/api/gat/config must say `"mode":"live"`, and the order page must show no red TEST MODE bar. If either still says test, wait: the server update is still in Railway's queue.

## Authorization

Dan authorizes every step: typing his shipping details and card, paying $9.99 and $97.00, cancelling the monthly delivery, refunding both charges in the Stripe dashboard, cancelling both Shopify orders and stopping them in Supliful. Do not stop to ask him. No secret value goes into a repo file (the repo is public).

## What to know first

- The form is hidden from visitors. It only shows at https://shop.sixpackabs.com/pages/great-again-t-order?onepage=1 . Without `?onepage=1` the page is the older two-step Shopify checkout: do not use that one for this job.
- Prices: free month is $9.99 today (shipping), then $67.00 every 30 days, first $67 charge 30 days after the order. One bottle is $97.00 once.
- The shop sends every paid order to Supliful within seconds. These two orders are real and will be sent to Supliful: that is the point of the test (it is the one thing test mode could not prove). Stop them in Supliful afterwards so nothing ships.
- Card statement text should read exactly `SIXPACKABS.COM`.
- Stripe account: the existing Rose Digital Holdings account (shown as "Abs By AI" in the dashboard), LIVE mode.
- Order emails currently come from `orders@absbyai.com` (the sixpackabs.com sending address is being set up separately). Stripe's own receipt email is switched on for this account, so a receipt in the Abs By AI name may arrive too: report every email that arrives and who it is from.

## Steps

1. Open https://shop.sixpackabs.com/pages/great-again-t-order?onepage=1 in a phone-size window. If a red TEST MODE bar shows at the top, stop and report: live mode is not on yet.
2. **Free month.** Fill in Dan's shipping details and card, tick the terms box, press Complete My Order. Expect $9.99 today. Confirm the thank-you page shows an order number and the date of the first $67 charge.
3. **One bottle.** Open the same address with `&option=single` added, pay $97.00, confirm the thank-you page.
4. **Declined card, once.** On one of the two orders, first try a wrong CVV: the page must show the bank's message and let the next try go through.
5. **Check and report for each order:** the Stripe charge amount and that the statement text is `SIXPACKABS.COM`; the Shopify order number, that it is paid and goes to "In progress"; that Supliful's dashboard shows it; every email that arrived, with the sender name and address of each (our order email, and any receipt from Stripe).
6. **Undo.** Open the account page link in the free-month email and press Cancel My Monthly Delivery (a cancel email should arrive). Refund both charges in the Stripe dashboard ($9.99 and $97.00). Cancel both Shopify orders and stop them in Supliful so nothing ships.
7. **Report** every total, order number and anything that failed. Dan pastes the report into Claude's go-live task, which then checks the records and switches the page over.

## Limits

Do not turn on ads, send marketing email, or change prices, settings or page copy. Two charges only ($9.99 and $97.00), both refunded in step 6.

## Done looks like

Two real orders placed through the one-page form, each with a Shopify order number, seen in Supliful, then the monthly delivery cancelled, both charges refunded, both Shopify orders cancelled and stopped in Supliful, and a report with every total and order number.

## Starter prompt (Grokbot, self-contained)

> Place two real test orders for Dan Rose on his own shop (SixPackAbs.com) and then undo them. Dan authorizes every step, including paying with his card, refunding and cancelling; do not stop to ask him. Use a phone-size window. (1) Open https://shop.sixpackabs.com/pages/great-again-t-order?onepage=1 . If a red TEST MODE bar shows at the top, stop and report: live mode is not on yet. (2) Free month: fill in Dan's shipping details and card, tick the terms box, press Complete My Order. Expect $9.99 today. Confirm the thank-you page shows an order number and the date of the first $67 charge. (3) One bottle: open the same address with &option=single added, pay $97.00, confirm the thank-you page. (4) Also try one wrong CVV once: the page must show the bank's message and let the next try go through. (5) Check and report for each order: the Stripe charge amount and that the statement text is SIXPACKABS.COM; the Shopify order number, that it is paid and goes to In progress; that Supliful's dashboard shows it; that the confirmation email arrived and which address it came from, plus any other email that arrived for the order (for example a receipt from Stripe) and who it is from. (6) Undo: open the account page link in the free-month email and press Cancel My Monthly Delivery; refund both charges in the Stripe dashboard ($9.99 and $97.00); cancel both Shopify orders and stop them in Supliful so nothing ships. (7) Report every total, order number and anything that failed. Do not turn on ads, send marketing email, or change prices, settings or page copy.
