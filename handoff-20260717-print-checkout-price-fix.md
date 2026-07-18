# Handoff: Fix N1 — print checkout trusts the client's price ($0.50 buys an $87 canvas)

**Date:** 2026-07-17
**Project:** Abs By AI
**Business goal this serves:** Profitability (closes the only direct cash-loss hole found in the July 17 audit)

## Objective

Make the server the only authority on printed-product prices. Today `/api/stripe/create-checkout` charges whatever `priceInCents` the browser sends, and `fulfillProductOrder` submits the real Printify order without ever checking the amount paid. An attacker can pay Stripe's minimum ($0.50) for a framed 16×20 canvas and the system ships it — a ~$54 Printify cost to the business per hit, repeatable without limit, and the request shape is visible in the page source. After this fix, the price comes from the server's own catalog, a too-low payment can never reach Printify, and the printed artwork can only be an image that was actually uploaded through our Printify account.

**Source finding:** N1 in `AUDIT_money_security_20260717.md` (project root). Read that entry first — it has the full reasoning. This handoff is the build order.

## Current State

- Stripe is LIVE and charging on absbyai.com (Railway auto-deploys from `main`).
- `server.js:6741` — `PRODUCT_CONFIG` already holds the true retail price per variant (`price`, in cents) plus Printify costs. It is currently used only to build the Printify order, never to price the Stripe session.
- `server.js:6824-6870` — `/api/stripe/create-checkout` builds the Stripe line item from `req.body.priceInCents` (client-controlled). Unauthenticated by design (print buyers may have no account).
- `server.js:6876-6955` — `fulfillProductOrder` (called by the webhook at `server.js:19` and the `session-status` fallback at `server.js:6684`) checks only `payment_status === 'paid'`, derives the variant, and submits to Printify. No amount check. It also builds the artwork source as `imagePreviewUrl || images-api.printify.com/<imageId>` — and `imagePreviewUrl` is client-controlled metadata, so any internet image can be printed.
- Client call site: `index.html:3409-3424` (`handleCheckout`) sends `productType`, `size`, `framed`, `priceInCents`, `imageId`, `imagePreviewUrl`, `imgWidth/Height`, `productLabel`, `returnUrl`. The client price table (`UPSELL_PRICES`, `index.html:2688`) matches `PRODUCT_CONFIG` exactly (e.g. 16×20 framed = 5400 + 3300 = 8700), so switching to server-side pricing changes nothing visible.
- The audit doc, this handoff, and `AI_COORDINATION.md` are committed on `main` (audit commit `86c73ee`).

## Key Decisions Already Made

- **Server-side price lookup, not client-price validation.** Ignore `priceInCents` entirely rather than 400-ing on mismatch — the deployed iOS/Android wrappers also send it, and ignoring keeps them working even if their baked-in table ever goes stale.
- **Defense in depth: also gate fulfillment.** Even with correct session creation, add the amount check in `fulfillProductOrder` — it's the last line before money is spent with Printify, and it also protects against any future session-creation regression.
- **Keep the endpoint unauthenticated.** Print buyers don't need accounts; the fix is price integrity, not auth.
- **Do not refactor the checkout flow** (embedded checkout, webhook + session-status double path, `fulfilled` idempotency map all stay exactly as they are — the July audits verified them clean).

## Detailed Plan

1. **Share the variant-lookup logic.** Extract the key derivation already used in `fulfillProductOrder` (`server.js:6900`) into a small helper near `PRODUCT_CONFIG`:
   ```js
   function productVariant(productType, size, framed) {
     const key = productType === 'canvas' ? `${size}_${framed ? 'framed' : 'unframed'}` : size;
     return PRODUCT_CONFIG[productType]?.variants[key] || null;
   }
   ```
   Have `fulfillProductOrder` use it too (behavior-identical there).

2. **`/api/stripe/create-checkout` (`server.js:6824`):**
   - Look up `const variant = productVariant(productType, size, !!framed);` → `return res.status(400).json({ error: 'Unknown product or size' })` when null. (This also correctly rejects the nonexistent 8×10 framed combo.)
   - Use `unit_amount: variant.price` in the line item. Remove `priceInCents` from the destructure or leave it unread — either way it must not influence the charge.
   - Require `imageId` (400 if missing) and **drop `imagePreviewUrl` from the session metadata** so fulfillment can't be steered to an arbitrary URL.

3. **`fulfillProductOrder` (`server.js:6876`):**
   - After deriving `variant`, add the belt-and-braces gate **before** the Printify call:
     ```js
     if ((full.currency && full.currency !== 'usd') || (full.amount_total ?? 0) < variant.price) {
       console.error(`Print order ${sid} paid ${full.amount_total} ${full.currency} < required ${variant.price} — NOT submitted to Printify`);
       return false;
     }
     ```
     (`>=` not `===` so a future promo/discount raise doesn't need touching; there are no discounts on this path today.)
   - Build the artwork source from the id only: `const imageSrc = imageId ? `https://images-api.printify.com/${imageId}` : ''`. Sessions created before this deploy still carry `imagePreviewUrl` in metadata — it's fine to keep reading it as a *fallback* for ~24h-old sessions if you want zero disruption, but new sessions won't have it. Simplest safe order: `imageId`-URL first, metadata preview URL second. **OPEN:** before relying solely on the `images-api.printify.com/<id>` form, confirm with one real end-to-end order that Printify accepts it (the live path so far has used `preview_url` first; the id-URL was only ever the fallback). If it fails, instead keep `preview_url` but take it server-side — have `create-checkout` call nothing new: `/api/printify/upload-image` already returns it, so store upload results server-side keyed by `imageId`, or validate the submitted URL's host is exactly `images-api.printify.com`.

4. **Client (`index.html:3409`):** no functional change required (server ignores what it sends). Optional tidy-up: stop sending `priceInCents`/`imagePreviewUrl`. Leave `productLabel` — it's display-only.

5. **Verify locally** (`npm test` exists; server also runs standalone with test env):
   - `create-checkout` with `priceInCents: 50` for `canvas/16x20/framed:true` → session line item is **8700**, not 50 (retrieve the session with a Stripe test key, or stub `stripe.checkout.sessions.create` and assert the payload).
   - `create-checkout` with an unknown size or `canvas/8x10/framed:true` → 400.
   - `fulfillProductOrder` with a session whose `amount_total` is 50 → returns false, nothing sent to Printify, loud log line.
   - Normal-price session → submits exactly as before (compare the Printify payload).

6. **Deploy + live verification** (required by project delivery rules): commit, push to `main`, confirm Railway deploy, then on absbyai.com run the real print flow up to the mounted embedded checkout and confirm the displayed total is the catalog price ($34/$42/$54/$75/$87 canvas, $18/$27 poster). Then replay the attack with curl against production (`priceInCents: 50`) and confirm the returned session prices at the real amount — do **not** complete any live payment. Update `AI_COORDINATION.md` and mark N1 fixed in a short note referencing the audit doc.

## Things to Avoid / Lessons Learned

- **Don't move the `fulfilled[order_...]` flag or restructure idempotency** — the webhook + session-status double path is intentional and verified (see F6 in `AUDIT_membership.md` for why "fixing" fulfillment ordering can create a paid-but-unfulfilled state).
- **Don't reject old in-flight sessions.** A session created minutes before the deploy carries the old metadata shape (has `imagePreviewUrl`, was priced by the old code at the correct catalog price). The fulfillment amount-check must compare against the variant price, which old legitimate sessions satisfy — they'll pass. Only attacker-priced sessions fail.
- **Don't trust any other metadata for money decisions.** Metadata is fine for *what* to print (size/type were always attacker-visible but harmless once price is server-set); it is never fine for *how much was owed*.
- The webhook currently returns 200 even when fulfillment throws (audit finding N3, separate fix) — so during testing, a failed Printify submit will NOT be retried by Stripe. Check the Railway logs after any live order.

## Relevant Files & Locations

- `server.js:6741` `PRODUCT_CONFIG` · `server.js:6824` `/api/stripe/create-checkout` · `server.js:6876` `fulfillProductOrder` · `server.js:19` webhook · `server.js:6684` `session-status`
- `index.html:2688` `UPSELL_PRICES` · `index.html:3373` `handleCheckout`
- `AUDIT_money_security_20260717.md` — finding N1 (and N3 context)
- Env (Railway, names only): `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `PRINTIFY_API_KEY`, `PRINTIFY_SHOP_ID`
- Live site: https://absbyai.com · Deploys: Railway auto-deploy from GitHub `main` (`RagnarD213/abs-by-ai`)

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking — the spec above is exact (files, lines, code); the only judgment call is the flagged OPEN item on the Printify image URL. |
| **If Claude usage is high / approaching a limit** | Codex flagship model, **medium** effort — don't drop to a mini-tier model: this touches live money paths where a wrong comparison direction (`<` vs `>`) silently reopens the hole. |

No always-Claude override applies (no brand copy, no Anthropic-API code). If the implementer hits the OPEN Printify-URL question and it turns gnarly, escalate effort there only, not for the whole task.

## Starter Prompt for the Next Task

> Fix the critical print-checkout pricing hole in Abs By AI (repo root: the `Abs By AI` project folder, deployed to absbyai.com via Railway from `main`). Read `handoff-20260717-print-checkout-price-fix.md` and follow its Detailed Plan exactly: make `/api/stripe/create-checkout` (server.js:6824) price the Stripe session from `PRODUCT_CONFIG` server-side (ignore the client's `priceInCents`), add an amount_total ≥ variant.price guard in `fulfillProductOrder` (server.js:6876) before anything is sent to Printify, and stop trusting the client-supplied `imagePreviewUrl` for the printed artwork. Note the OPEN item about verifying the `images-api.printify.com/<imageId>` URL form before relying on it. Start with step 1 (extract the shared `productVariant` helper), verify per step 5, then commit, push, confirm the Railway deploy, and live-verify on absbyai.com per step 6 — including replaying the $0.50 attack with curl to prove it now prices at the real amount. Do not complete any live payment. When done, update `AI_COORDINATION.md` and mark N1 fixed.
