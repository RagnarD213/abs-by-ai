---
name: gat-live-funnel-build
description: "11-17 Great Again T funnel is live (not launched) on shop.sixpackabs.com; built only from the generator, deployed through the M2; Shopify repeats first-order shipping on subscription refills"
metadata:
  type: project
---

The Great Again T quiz, sales page, order page and nine compliance pages went live on shop.sixpackabs.com on 2026-11-17, unlaunched (noindex, no ads, placeholder video). Receipt with every address, ID and the undo steps: `Docs/GAT_SALES_PAGE_BUILD_RECEIPT_20261117.md`.

- The pages are generated: `refine/gen.py` (mockups, copy checks) then `refine/build_live.py` (theme files) then `refine/deploy_live.sh`. Never hand-edit the theme's `gat*` files. Copy comes only from Dan's two Google Docs.
- The Shopify CLI is signed in on the M2, not the M6: deploys rsync to the M2 and push from there, only the gat files (`--only`, `--nodelete`).
- Shopify fact worth remembering: on a subscription, checkout copies the FIRST shipment's shipping rate onto every refill. A free first bottle (subtotal $0) gets the $9.99 rate, so a $67 refill becomes $76.99 even though $67 normally ships free. Check "Recurring shipments" at checkout before trusting any trial offer.
- Shopify admin pages can be driven in Dan's Chrome, but another extension sometimes blocks clicks ("chrome-extension:// URL of different extension"): reload or reopen the tab group and retry. Native selects sit in shadow DOM.

**Why:** the next session that touches this funnel needs to know it is generated, where it deploys from, and why the free-month button is closed.

**How to apply:** any change to the Great Again T pages, checkout, tracking or launch. Related: [[gat-sales-page-direction]], [[gat-page-google-ads-words]], [[supliful-shopify-linking]], [[two-mac-edit-routing]].
