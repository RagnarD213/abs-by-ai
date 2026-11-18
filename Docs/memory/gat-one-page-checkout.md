---
name: gat-one-page-checkout
description: "11-18 Great Again T one-page order form: Stripe on our page, Shopify orders by API; test-mode traps (shop auto-sends paid orders to Supliful, statement text needs invoices)"
metadata:
  node_type: memory
  type: project
  originSessionId: fcfbbe60-5bab-4705-830d-fcc38373fc8a
  modified: 2026-11-18T23:23:16.606Z
---

Built 2026-11-18 for Dan ("pay all on one page... eliminate the two-step checkout"). Receipt with every ID: `Docs/GAT_ONE_PAGE_CHECKOUT_RECEIPT_20261118.md`. Go-live steps: `Handoffs/handoff-20261118-gat-one-page-checkout-go-live.md`.

- Server: `gat-checkout.js` in the Abs By AI app (Railway), settings `GAT_*`, routes `/api/gat/*`. Pages: `refine/onepage.py` + `refine/live/gat-pay.js`, switched by `CFG['onePage']` in `build_live.py` (`preview` = only at `?onepage=1`, `on` = everyone, `?classic=1` = old two-step flow).
- **The SixPackAbs shop sends every paid order to Supliful within seconds** (auto fulfilment). Never create a paid Shopify order with a real product variant as a test, even flagged test. Test mode uses a custom line "TEST ORDER, do not ship".
- **Card statement text on the shared Stripe account:** a plain charge reads `ABS BY AI* SIXPACKABS.`. Charging through Stripe invoices whose product has `statement_descriptor` gives exactly `SIXPACKABS.COM`. Keep every GAT charge on invoices.
- Stripe webhook events arrive in the account's default API shape, not the app's pinned one: read ids from the event and fetch the object again.
- Shopify Admin API access is the Dev Dashboard app `gat-order-sync` (client credentials, 24-hour tokens; legacy custom apps no longer exist). Created from the M2 with `shopify app init --organization-id 245324494`.
- The Railway `RESEND_API_KEY` can only send from absbyai.com; sixpackabs.com needs its own Resend domain and key (sign-in needed).
- A local privacy guard blocks any shell command naming a file I edited that holds Dan's personal email. `server.js` had it as a web push fallback; replaced with `dan@absbyai.com`.

**Why:** the next session touching this checkout, or testing any SixPackAbs order flow, needs these traps before it spends money or ships a test bottle.

**How to apply:** any work on the Great Again T order page, its payments, upsells on the saved card, or Shopify order tests. Related: [[gat-live-funnel-build]], [[supliful-shopify-linking]], [[repo-is-public]].
