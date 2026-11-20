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

## Status 2026-11-19, 12:50 PM Central (Claude, from the records)

Steps 1 to 3 are done: free month is Shopify order #1030 ($9.99, monthly plan $67 every 30 days, first charge December 18) and one bottle is #1031 ($97.00). Both are paid, real, "In progress", statement text SIXPACKABS.COM, order emails sent.

**Step 6 (the undo) is NOT done.** Neither charge is refunded, the monthly plan is still active in trial, and both Shopify orders are still open with no shipment recorded yet. No declined-card attempt shows in Stripe either (step 4).

### Undo-only prompt (Grokbot, self-contained, fire now)

> Undo two real test orders for Dan Rose on his own shop (SixPackAbs.com). Dan authorizes every step, including refunds and cancellations; do not stop to ask him. The orders were placed on November 18, 2026 through his one-page order form: Shopify order #1030 (free month, $9.99 charged, with a monthly plan of $67 every 30 days whose first charge is December 18) and Shopify order #1031 (one bottle, $97.00). (1) In the Stripe dashboard (the account shown as "Abs By AI", live mode) find the two payments with statement text SIXPACKABS.COM from November 18, $9.99 and $97.00, and refund each in full. (2) In Stripe, cancel the subscription that belongs to the $9.99 customer immediately (Great Again T, $67 every 30 days, in trial). Or open the account page link in the free-month order email and press Cancel My Monthly Delivery. (3) In Shopify admin (store 1yar3v-ie) cancel orders #1030 and #1031 without issuing a second refund there (the money goes back through Stripe). (4) In Supliful's dashboard cancel or stop both orders so nothing ships; if one has already shipped, say so. (5) Report what you did for each order and anything that could not be undone. Do not change prices, settings, page copy or any other order.

### Same undo, Codex (GPT-6.2 Sol, high)

> Read `Handoffs/handoff-20261118-gat-real-test-orders-grokbot.md` in the Abs By AI project and do only the undo described under "Status 2026-11-19": in the Stripe dashboard refund the two November 18 payments with statement text SIXPACKABS.COM ($9.99 and $97.00) in full and cancel the $67 Great Again T subscription; in Shopify admin (store 1yar3v-ie) cancel orders #1030 and #1031 without a second refund; in Supliful stop both orders so nothing ships. Dan authorizes every step, including the refunds and cancellations. Do not use the Stripe API for the refunds, do not change prices, settings or page copy, and keep secrets out of repo files. Report what was done for each order.

Claude can also do this undo itself in the dashboards once Dan says yes to the two refund amounts in Claude's go-live task.

## Status 2026-11-20, 8:52 AM Central (Claude, from the records): the undo is half done

This replaces the 2026-11-19 status above. The two prompts above are out of date: use the ones below.

- **Done:** the $67 monthly plan was cancelled on 2026-11-19 at 1:29 PM Central (cancel email sent). No December charge will happen.
- **Done, but only on paper:** on 2026-11-19 at 5:03 PM Central a refund was recorded on each Shopify order ($9.99 on #1030, $97.00 on #1031). These orders were paid in Stripe, outside Shopify, so a Shopify refund moves no money. **In Stripe both charges still read succeeded, refunded $0.00.**
- **Tried and refused:** at 5:02 PM Central Shopify asked Supliful to cancel both orders and Supliful declined both. Both orders still read "In progress" with no shipment recorded, so two bottles will ship to Dan unless Supliful support stops them.
- Not done: no declined-card attempt shows in Stripe (step 4). The Shopify orders are not cancelled (they cannot be while Supliful holds them).

### What is left, Grokbot (self-contained, fire now)

> Finish undoing two real test orders for Dan Rose on his own shop (SixPackAbs.com). Dan authorizes every step, including the refunds; do not stop to ask him. The orders were placed on November 18, 2026: Shopify #1030 ($9.99) and Shopify #1031 ($97.00). The monthly plan is already cancelled and Shopify already shows both orders as refunded, but that Shopify refund moved no money, because the orders were paid in Stripe. (1) In the Stripe dashboard (the account shown as "Abs By AI", live mode) find the two payments from November 18 with statement text SIXPACKABS.COM, $9.99 and $97.00, and refund each in full. Do NOT refund anything again in Shopify. (2) In Supliful's dashboard find the two orders (Shopify #1030 and #1031). Shopify's cancel request was declined. If Supliful still lets you cancel them, cancel both; if not, message Supliful support from Dan's account and ask them to stop both orders before they ship. If they have shipped, say so. (3) Report what you did for each order and anything that could not be undone. Do not change prices, settings, page copy or any other order.

### What is left, Codex (GPT-6.2 Sol, high)

> Read `Handoffs/handoff-20261118-gat-real-test-orders-grokbot.md` in the Abs By AI project and do only what the section "Status 2026-11-20" says is left: in the Stripe dashboard (not the API) refund in full the two November 18 payments with statement text SIXPACKABS.COM, $9.99 and $97.00; do not refund again in Shopify (it already shows both as refunded, on paper only); in Supliful try to cancel the two orders for Shopify #1030 and #1031, and if the dashboard will not, ask Supliful support from Dan's account to stop them before they ship. Dan authorizes every step, including the refunds. Do not change prices, settings or page copy, and keep secrets out of repo files. Report what was done for each order.

Claude can also do the two Stripe refunds itself in the dashboard once Dan says yes to the two amounts in Claude's go-live task.
