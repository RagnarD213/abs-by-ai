# Great Again T: live shop matched to the sales letter offer (2026-11-17, Claude)

Dan approved in chat: "Yes, change it" to "Change the live shop to match your script ($97 bottle, $67 refill, new guarantee)". Store `1yar3v-ie.myshopify.com` (shop.sixpackabs.com). No active subscription contracts existed (only Dan's two canceled tests), so no customer's plan changed.

## What changed

| Area | Before | After |
|---|---|---|
| Great Again T, one bottle (product 15503050178882) | $47 | **$97** |
| Monthly plan for Great Again T | shared plan 79734407490, 10.64% off ($42) | new plan "Every month", fixed price **$67** (selling plan 693056045378); Great Again T removed from the shared plan. The other five products keep $42 |
| Standard shipping (General profile 139968282946, Domestic) | $9.99, free from $70 | $9.99, **free from $67** (so the $67 plan ships free). Express $15 unchanged |
| Refund policy | any reason, 365 days from the order, no questions asked | **unopened bottles or tubs, within 365 days of receiving them**; applies to orders placed on or after 2026-11-17, earlier orders keep the old terms |
| Shipping policy | free on orders of $70 or more | free on orders of $67 or more |
| Cancellation policy | "plus shipping"; 365-day guarantee | shipping stated ($9.99, free from $67); guarantee "on unopened bottles and tubs" |
| Theme (live theme 195457614146, commit f0cd97a in `sixpackabs-shop-theme`) | guarantee card, founder line and help FAQ said any reason; "plus shipping" on every row; cart note hard-coded "$42 plus shipping" | six files: `snippets/guarantee.liquid`, `sections/home-founder.liquid`, `snippets/page-help.liquid`, `snippets/cart-body.liquid`, `sections/main-product.liquid`, `snippets/offer-row.liquid`. Rows of $67 or more say "free shipping"; subscription terms use the plan's own price |

The guarantee is one store-wide policy, so the unopened-bottle wording now applies to all six products, not only Great Again T.

## Verified live

- Product page: 1 bottle $97 free shipping; monthly $67 free shipping; terms line "$67 with free shipping today, then every month until you cancel".
- Throwaway cart with the $67 plan: Standard shipping $0.00, Express $15.00.
- Home, help page, the three policy pages, collection, cart, contact, search and two other product pages return 200 with the new wording; Electro Creatine still shows $47 and $42 plus shipping.

## Not done (not in the approval)

- The free first bottle (first payment 100% off, $9.99 shipping) and the 7-day reminder email before the first $67 charge: part of the funnel checkout build. Today the $67 plan charges $67 on the first order.
- 3 and 6 bottle packs stay $129 and $234 (the page now shows "Save $162" and "Save $348" against the $97 bottle).
- Supliful's own retail price field for the product still says $47 (it is not shown to customers).
- `sections/main-collection.liquid` still says "plus shipping" and "$42 every month" in its bundles line.

## How to undo

Product price back to $47; add Great Again T back to plan 79734407490 and delete the $67 plan; Standard free-shipping minimum back to $70; restore the three policy texts from this table; `git revert f0cd97a` in the theme repo and push the six files (`shopify theme push --only ... --allow-live`, run from the M2, where the Shopify CLI is signed in; the M6 CLI is signed out).
