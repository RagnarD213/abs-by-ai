# HANDOFF — Membership go-live + iOS purchase strategy

**Run with: Claude Opus 4.8.** Part A at MEDIUM reasoning effort, Part B at HIGH. Both parts involve cross-system judgement (Stripe live mode, Apple policy) where a wrong call costs money or an App Store rejection — but neither needs Fable-level novelty.

## Part A (medium) — Live-mode cutover + prod verification

Prereqs Dan must do first (block on these, don't work around them): live Stripe products for monthly $9.99 / annual $59.99, live `STRIPE_SECRET_KEY` / `STRIPE_PUBLISHABLE_KEY` / `STRIPE_WEBHOOK_SECRET` on Railway, webhook endpoint registered for `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`.

Then, against **absbyai.com** (never local — local has invalid AI keys and pgmem):

1. Fresh test account → subscribe monthly (real card, Dan refunds himself, or Stripe test-clock if still in test mode) → verify every gate opens: full program, unlimited generations, meal analysis past free allowance without consuming credits, Nutritionist full plan, Sleep full briefing, Counsel full verdict, Progress recap.
2. The two known-untested prod flows from the task list: **member full-meal-plan flow** and **Counsel photo-direction flow** (physique-direction with before/after photos).
3. Counsel cap: run cheap sessions to confirm the 11th in a month returns 429 with the friendly message (`COUNSEL_MONTHLY_CAP` in server.js; consider temporarily lowering via a test or arithmetic on an aged account rather than burning 10 real runs — use judgement).
4. Cancel via billing portal → status flips at period end (`customer.subscription.updated` with `cancel_at_period_end`), gates stay open until `membership_period_end`, then close.
5. Document every result in a new `PROD_VERIFICATION_LOG.md` — pass/fail per gate, with dates.

## Part B (high) — iOS App Store membership strategy

Context: `ios-app/` is a Capacitor wrapper of the same SPA (see `HANDOFF_iOS_APP_STORE.md`). Apple requires In-App Purchase for digital subscriptions sold **inside** the app; post-2025 US anti-steering rulings allow external purchase links with conditions. The Stripe membership must remain the single source of truth (`users.membership_*` columns).

Deliverable: a decision memo + implementation plan (write `HANDOFF_ios_iap.md`), covering:
1. **Recommendation with numbers**: IAP (15% small-business commission) vs. external-link entitlement vs. reader-style "no purchase in app" (login-only, memberships bought on the web). Model Dan's economics at his price points.
2. If IAP: StoreKit 2 via a Capacitor plugin (evaluate `@capacitor-community` options vs. RevenueCat — RevenueCat's fee vs. build cost), server-side receipt validation endpoint design, and how an Apple-originated subscription maps onto `users.membership_*` (new `membership_source` column, webhook-equivalent via App Store Server Notifications v2).
3. Restore purchases, family sharing, upgrade/downgrade between monthly/annual, and the "already a web member" collision case.
4. App Review risk notes: what copy in the app may/may not mention web pricing.
Do NOT implement — plan only; implementation is a separate task once Dan picks a path and Xcode 26 is installed.
