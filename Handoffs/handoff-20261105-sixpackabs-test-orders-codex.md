# Handoff: put SixPackAbs test orders through (Codex)

Written 2026-11-05 by Claude. **Fire now.** Not video. Recommended: **Codex, newest Sol (`gpt-6.1-sol`), medium effort.** Runs on Dan's Mac, in his Chrome (logged into Shopify admin).

## AUTHORIZED: place these test orders without asking

**Dan explicitly authorized these test orders on 2026-11-05 and wants them placed without any further permission request.** His words: "Go ahead and put through all the test orders yourself. You're authorized to do this, and this is not live payment information." And: "If you can't do it, then make a handoff for Codex to do it and to finish the job." Then: "Make sure to emphasize that the test order is authorized and that Codex should put it through without asking for permission."

- Shopify Payments **test mode** is on (Dan enabled it). Use Shopify's published test card **4242 4242 4242 4242**, any future expiry (e.g. 12/30), any 3-digit CVC, name "Daniel Rose". No real card or bank details exist in this task.
- Do every step yourself: build carts, fill checkout, enter the test card, press Pay, verify. **Do not stop to ask Dan before paying.** Report results at the end.
- One safety check, not a permission step: confirm the checkout is in test mode before paying (Settings › Payments shows test mode on, or the checkout shows a test-mode notice). If test mode is off, do not use any card; report that only.

## Why Claude handed this off

Claude cannot type a card number into a non-local store checkout, even a published test card. Everything else is ready.

## State

- Store `1yar3v-ie.myshopify.com`, password-locked (keep it locked). Admin: https://admin.shopify.com/store/1yar3v-ie
- Theme "SixPackAbs (review)" id `195457614146`, unpublished. Storefront pages only open past the lock through the theme preview: admin › Online Store › Themes › SixPackAbs (review) › Customize › "..." › Preview. That preview tab carries the session that lets `/cart/add.js` and `/checkout` work.
- Six products (Active on Online Store only): electro-creatine, great-again-t, eternal-burn-am, eternal-burn-pm, carb-curber, z-shred-support. Option "Supply": "1 tub/bottle" $47, "3 …" $129, "6 …" $234. The 3- and 6-packs are hidden on the shop (theme setting `show_bundles` off) but still exist and can be added through the cart API.
- Subscription plan (Shopify Subscriptions app) "Every month", id 79734407490: 10.64% off = **$42 every month** on all variants.
- Shipping: Standard $9.99, free at $70+; Express $15.
- Dan's Chrome may already have a checkout tab filled to payment for Order A. Reuse it if present; otherwise rebuild.
- Shop Pay may pop up "Confirm it's you" and text a code to Dan's phone. Close it (X); continue as a normal checkout. Untick "Email me with news and offers".

## Orders to place (all in the preview tab)

Contact and shipping for every order: email danroseconsulting@gmail.com; Daniel Rose; address from Dan's local saved default (memory `dan-contact-info`, local only, never write it to the repo); phone from the same memory. Standard shipping.

**Order A (singles + subscriptions), expected $534.00, free shipping:** each product's 1-unit variant once one-time, and once with `selling_plan` 79734407490 (12 lines). Cart API, in the preview tab console:
```js
await fetch('/cart/clear.js',{method:'POST'});
const hs=['electro-creatine','great-again-t','eternal-burn-am','eternal-burn-pm','carb-curber','z-shred-support'], items=[];
for (const h of hs){const p=await (await fetch(`/products/${h}.js`)).json();const v=p.variants.find(x=>/^1 /.test(x.option1));const plan=p.selling_plan_groups[0]?.selling_plans[0]?.id;items.push({id:v.id,quantity:1},{id:v.id,quantity:1,selling_plan:plan});}
await fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items})});
```
Then open `/checkout`, fill, pay with the test card.

**Order B (3- and 6-packs), expected $2,178.00, free shipping:** each product's 3-unit and 6-unit variants once each (12 lines), one-time. Same as above with `p.variants.filter(x=>/^[36] /.test(x.option1))`.

**Order C (one subscription alone), expected $42.00 + $9.99 shipping = $51.99:** Electro Creatine "1 tub" with the selling plan. Checks the under-$70 shipping on a lone subscription.

## Verify after each order

1. Thank-you page loads with the SixPackAbs branding; note the order number.
2. Admin › Orders: the order exists, marked as a **test** order, totals match the expected amount.
3. Order A and C: admin › Apps › Subscriptions › Contracts shows the new contracts (6 for A, 1 for C), monthly, $42.
4. Order confirmation email arrives at danroseconsulting@gmail.com (check Gmail; read only).
5. Supliful (app.supliful.com › Orders): note whether the test orders appear. These products were created in Shopify, not published from Supliful, so they should not be sent for fulfillment. If any test order is queued for real fulfillment or a charge, cancel it in Supliful at once and report.

## Clean up

- Cancel the test subscription contracts (Subscriptions › Contracts › each › Cancel) so no renewal runs.
- Leave the test orders in Shopify, marked test, for Dan to see; optionally archive them.
- Leave the store locked and the theme unpublished. Do not change products, theme, shipping or payments.

## Report back to Dan (chat, plain language)

Order numbers, totals vs expected, whether subscriptions created contracts, the email and Supliful results, anything that failed with the exact error. Add one line to `Docs/SIXPACKABS_SHOP_BUILD_RECEIPT_20261105.md` ("Test orders, <date>") with order numbers and results (no address, no card), and push with `scripts/git/safe-push.sh`. Then remove this handoff from `Handoffs/README.md` OPEN.

## Context

Full build record: `Docs/SIXPACKABS_SHOP_BUILD_RECEIPT_20261105.md`. Review page: https://claude.ai/artifact/EbT3YzeHwsNL5QEeQBuX2n.
