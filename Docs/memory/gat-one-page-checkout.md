---
name: gat-one-page-checkout
description: "11-19 Great Again T one-page order form is LIVE for everyone (Stripe live mode, ?classic=1 = old flow); traps: shop auto-sends paid orders to Supliful, statement text needs invoices, Stripe receipts say Abs By AI, Codex will not create keys without Dan"
metadata:
  node_type: memory
  type: project
  originSessionId: fcfbbe60-5bab-4705-830d-fcc38373fc8a
  modified: 2026-11-18T23:23:16.606Z
---

Built 2026-11-18 for Dan ("pay all on one page... eliminate the two-step checkout"). **Live since 2026-11-19:** Stripe live mode, `CFG['onePage'] = 'on'`, every visitor gets the form, `?classic=1` is the two-step fallback; the funnel itself is still not launched (noindex, no ads). Receipt with every ID and the go-live record: `Docs/GAT_ONE_PAGE_CHECKOUT_RECEIPT_20261118.md`.

- Server: `gat-checkout.js` in the Abs By AI app (Railway), settings `GAT_*`, routes `/api/gat/*`. Pages: `refine/onepage.py` + `refine/live/gat-pay.js`, switched by `CFG['onePage']` in `build_live.py` (`preview` = only at `?onepage=1`, `on` = everyone, `?classic=1` = old two-step flow).
- **The SixPackAbs shop sends every paid order to Supliful within seconds** (auto fulfilment). Never create a paid Shopify order with a real product variant as a test, even flagged test. Test mode uses a custom line "TEST ORDER, do not ship".
- **Card statement text on the shared Stripe account:** a plain charge reads `ABS BY AI* SIXPACKABS.`. Charging through Stripe invoices whose product has `statement_descriptor` gives exactly `SIXPACKABS.COM`. Keep every GAT charge on invoices.
- Stripe webhook events arrive in the account's default API shape, not the app's pinned one: read ids from the event and fetch the object again.
- Shopify Admin API access is the Dev Dashboard app `gat-order-sync` (client credentials, 24-hour tokens; legacy custom apps no longer exist). Created from the M2 with `shopify app init --organization-id 245324494`.
- The order page takes REAL cards now: never type a test card on the live shop. Proofs with typing run only against the local proof server; `GAT_PROOF=look` only looks.
- Order emails: the Railway `RESEND_API_KEY` is locked to absbyai.com. Great Again T uses `GAT_RESEND_API_KEY` (send-only, sixpackabs.com, Resend domain verified 2026-11-19) and `GAT_FROM` set to the "orders" address at sixpackabs.com.
- First real orders (2026-11-18): #1030 ($9.99, $67 every 30 days) and #1031 ($97). Shopify's timeline showed "Supliful accepted the request" within two seconds, so orders made by the API do reach Supliful.
- Open as of 2026-11-19: Stripe's "Successful payments" receipt is on for the shared account (Abs By AI members rely on it), so buyers also get "Your receipt from Abs By AI". Fix before launch needs Dan's yes: keep the buyer email off the Stripe customer, or a separate Stripe account.
- Codex's computer use can click in Dan's signed-in Chrome on the M6, but it stops for a person's confirmation before creating any API key and refuses Full access keys. Plan: Codex fills the form, Dan presses the last button.
- The Claude Chrome extension may be attached to a different Chrome than the one on Dan's screen. Before asking him to sign in "on the tab", open a marked address and look for it in his Chrome with `osascript` (target the non-headless Chrome by process id; many headless proof Chromes run on the M6).
- A local privacy guard blocks any shell command naming a file I edited that holds Dan's personal email. `server.js` had it as a web push fallback; replaced with `dan@absbyai.com`.

**Why:** the next session touching this checkout, or testing any SixPackAbs order flow, needs these traps before it spends money or ships a test bottle.

**How to apply:** any work on the Great Again T order page, its payments, upsells on the saved card, or Shopify order tests. Related: [[gat-live-funnel-build]], [[supliful-shopify-linking]], [[repo-is-public]].
