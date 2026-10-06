---
name: stripe-test-mode-cart-recipe
description: "How to run the web cart end to end with fake cards: Stripe TEST keys are in ~/.absbyai-secrets.env since 2026-10-03; local server recipe, Stripe iframe typing quirks, and the ad-tag guard that must run before every test purchase"
metadata:
  node_type: memory
  type: project
  originSessionId: 90e35380-378f-4e82-9fd9-25d52845088f
  modified: 2026-10-03T14:13:47.323Z
---

Since 2026-10-03 `~/.absbyai-secrets.env` holds `STRIPE_TEST_PUBLISHABLE_KEY` and `STRIPE_TEST_SECRET_KEY` (Dan added them; they are NOT on Railway). With them Claude can test payments itself, because Stripe's published test cards on localhost are allowed where Dan's real card never is. Claude cannot type a real card or trigger a live charge (its own limit, not Dan's rule): Dan runs `scripts/cart/lifetime-charge-now.sh` on live himself.

**Recipe (verified on the v2 cart, all cases passed):**
- Temporary `.claude/launch.json` config: a `sh -c` that exports `STRIPE_SECRET_KEY`/`STRIPE_PUBLISHABLE_KEY` from the two TEST lines, plus `DASH_SECRET=local-dash-test DATABASE_URL=pgmem://local PORT=3013`. Revert the file with `git checkout` after (it is tracked).
- Test mode had no billing portal config; one was created 2026-10-03 mirroring live (cancel at period end, card update, invoices). Manage membership works in test mode now.
- No webhook reaches localhost. Fulfilment still runs through the browser's claim / session-status fallback, and the Lifetime charge confirms in the same call, so nothing is missed.
- Cards: `4242…4242` ok; `4000 0000 0000 0341` saves fine and declines when charged later (Lifetime retries); `4000 0000 0000 0002` declined at checkout; `4000 0025 0000 3155` shows the bank verification pop-up (click COMPLETE).
- Lifetime charge now: `curl -X POST localhost:3013/api/admin/lifetime/charge-now -H 'X-Dash-Key: local-dash-test' -d '{"email":…}'`. Each call is one attempt, so four calls walk the whole retry ladder.

**Traps:**
- **Ad and analytics tags are live on localhost.** Before every test purchase, in the page: `posthog.opt_out_capturing()`, replace `window.gtag` with a recorder, and replace `window.fireTikTokEvent` (overriding `ttq.track` does NOT hold, TikTok's script swaps it back; one fake `StartTrial` reached TikTok on 2026-10-03 this way). The page reloads between buyers, so re-apply after each load.
- **A wallet payment reloads the page** (Stripe redirects to `/?cart_return=`), so in-page guards are gone when the conversions fire on return. To run that path locally, add `if (location.hostname === 'localhost') return false;` at the top of `fireAdConversion` and `fireTikTokEvent` in the working copy, and remove it before committing. PostHog's opt-out survives the reload.
- No Apple Pay in the Browser pane. Drive the wallet handlers with a fake event instead: patch `c2.actions.confirm` to call the real one with only `{ email }`, then call `c2ExpressClick({expressPaymentType:'apple_pay', resolve(){}, reject(){}})` and `c2ExpressConfirm({expressPaymentType:'apple_pay', paymentFailed(){}})` with a test card filled in.
- Log out between buyers with `handleLogout()`; removing the localStorage keys alone leaves the session logged in.
- Stripe's fields are a cross-origin iframe: fill them with `computer` click + type by coordinate. The FIRST click after a navigation only focuses the iframe and the typing is dropped: click, wait 1 s, click again, then type. A coordinate click needs a fresh screenshot after each navigation. Check `actions.getSession().canConfirm` before pressing pay.
- Scroll to the payment element only after it has mounted (`c2.actions` set), or the clicks land on the footer.
- While the Browser pane is hidden, Stripe's iframe can paint blank or at half width. `preview_start` again / `tabs_select`, then reload. It is a preview artefact, not a bug.
- Embedded (overlay) Checkout renders blank on `http://localhost` with LIVE keys under any Stripe.js; test that on HTTPS.

Related: [[web-cart-pay-first]], [[cart-follows-start-button]], [[local-funnel-test-recipe]], [[autonomy-credentials-framing]].
