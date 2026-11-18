# Great Again T funnel: finish it (refill shipping fix, purchase pixel, test order)

Written 2026-11-17 by Claude (Fable 5.2). Website and shop work, no edit slot. For **Codex (newest Sol, high) and Grokbot**: it includes a real card payment, which Claude cannot type.

**Fire after Dan picks fix A or B below.** Dan authorizes whoever runs this to do every step, including the card payment for the two test orders, signing in, and changing the shop settings named here. Do not stop to ask him. Secrets stay out of repo files.

Read first: `Docs/GAT_SALES_PAGE_BUILD_RECEIPT_20261117.md` (what is live, how it is built and deployed).

## Where it stands

All twelve pages are live on shop.sixpackabs.com (store `1yar3v-ie.myshopify.com`, live theme 195457614146), hidden from search, no ads. Order page: https://shop.sixpackabs.com/pages/great-again-t-order?preview=1 . The free-month button is closed to the public (`trialOpen: False` in `build_live.py`) and works only with `?preview=1`.

Verified up to the payment step: bottle FREE with code `FREEMONTH`, Standard shipping $9.99, total $9.99. **Wrong:** Shopify shows "Recurring shipments: Standard · $9.99 every month", so each refill would be $67 + $9.99 = $76.99. The pages promise $67 a month with shipping included.

## Step 1. Apply Dan's fix

**Fix A (Claude's recommendation): plan $57.01 + $9.99 shipping = $67.**
1. Shopify admin > Apps > Subscriptions > plan "Every month" on Great Again T (selling plan 693056045378): fixed price $67 to **$57.01**.
2. In `Media/research/gat-sales-page-contest-20261117/refine/build_live.py`: `CFG['trialPlanPrice']` 6700 to 5701; in `order_body()` change "billed $67 plus tax per bottle, with free shipping" to "billed $67 plus tax per bottle, shipping included". Leave every "$67" on the pages as it is.
3. Check the regular product page reads sensibly ($57.01 plus $9.99 shipping every month); the theme prints the plan's own price.

**Fix B: Great Again T ships free, first $9.99 is a cart line.**
1. New product "Shipping and handling (first bottle)", $9.99, not a physical product, hidden from the shop's grid and search.
2. New shipping profile for Great Again T only: Standard free, Express $15.
3. In `refine/live/gat.js`, add that product's variant to the cart with the free-month option; in `order_body()` nothing changes.

Either way: set `'trialOpen': True`, run `python3 build_live.py` (must print PASS), then `./deploy_live.sh` from the M6 (it pushes through the M2). Open the order page, go to checkout with a real address and confirm **today $9.99, recurring $67.00 a month in total** before paying.

## Step 2. Install the purchase pixel

Shopify admin > Settings > Customer events > Add custom pixel, name "Great Again T purchase". Paste `refine/live/shopify-pixel.js` exactly. Permission: Marketing and Analytics. Save, then Connect.

## Step 3. Two real test orders

1. Free month: quiz > sales page (`?offer=1`) > order page > tick the box > checkout. Pay with Dan's card. Expect $9.99. Confirm: order in Shopify, subscription contract at $67 a month total, order email, Supliful received it, PostHog event `gat_purchase`.
2. One bottle, one time: expect $97.00, free shipping, no subscription.
3. Cancel the test subscription contract. Cancel or refund the two orders in Shopify and stop them in Supliful if Dan does not want the bottles (default: cancel both).
4. Add the results to `Docs/GAT_SALES_PAGE_BUILD_RECEIPT_20261117.md`, mark this handoff executed in `Handoffs/README.md`.

## Limits

No ads turned on. No emails to customers or the list. Do not change the other five products. Do not rewrite page copy beyond the one sentence in fix A.

## Done looks like

Refills are $67 in total at checkout, the free-month button is open, the pixel is connected, both test orders are recorded and cleaned up, the receipt says so.
