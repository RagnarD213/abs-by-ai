# Great Again T funnel: the two real test orders

Written 2026-11-17 by Claude (Fable 5.2). Website and shop work, no edit slot. For **Codex (newest Sol, high) and Grokbot**: it includes a real card payment, which Claude cannot type.

**Fire now.** Dan authorizes whoever runs this to do every step, including the card payment for the two test orders, signing in, and cancelling them afterwards. Do not stop to ask him. Secrets stay out of repo files.

Read first: `Docs/GAT_SALES_PAGE_BUILD_RECEIPT_20261117.md` (what is live, how it is built and deployed).

## Already done by Claude (2026-11-17), do not redo

- Refill shipping fixed (fix A): the plan is $57.01 and Shopify repeats the $9.99 shipping, so refills are $67.00 in total. The free-month button is open.
- Purchase pixel "Great Again T purchase" is saved and connected in Settings > Customer events.
- Checkout verified up to the payment step: bottle FREE with code `FREEMONTH`, Standard shipping $9.99, total $9.99, recurring $57.01 + $9.99 a month.

## The two real test orders

1. Free month: quiz > sales page (`?offer=1`) > order page > tick the box > checkout. Before paying confirm: today $9.99, recurring $57.01 plus $9.99 shipping a month. Pay with Dan's card. Confirm: order in Shopify, subscription contract at $67 a month in total, order email, Supliful received it, PostHog event `gat_purchase`.
2. One bottle, one time: expect $97.00, free shipping, no subscription.
3. Cancel the test subscription contract. Cancel or refund the two orders in Shopify and stop them in Supliful if Dan does not want the bottles (default: cancel both).
4. Add the results to `Docs/GAT_SALES_PAGE_BUILD_RECEIPT_20261117.md`, mark this handoff executed in `Handoffs/README.md`.

## Limits

No ads turned on. No emails to customers or the list. Do not change the other five products or any page copy.

## Done looks like

Both test orders are recorded in the receipt with their totals, the test subscription is cancelled, the orders are cancelled and refunded, and the Google Ads conversion and PostHog `gat_purchase` event are confirmed or reported missing.
