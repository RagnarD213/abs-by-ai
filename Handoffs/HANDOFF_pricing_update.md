# HANDOFF: Membership repricing + 7-day free trial

**Recommended implementer:** Claude Opus 4.8, high reasoning effort.
**Scope:** server.js + index.html only. No schema migrations beyond one column. No users are live yet, so no grandfathering or migration of existing subscribers is needed.

## Decision summary (already made — do not re-litigate)

Approved by Dan on July 11, 2026 after market research:

| Item | Old | New |
|---|---|---|
| Monthly plan | $9.99/mo | **$19.99/mo** |
| Annual plan | $59.99/yr | **$69.99/yr** ($5.83/mo equivalent, ~71% off monthly) |
| Free trial | none | **7 days, on BOTH plans, card required up front** |
| Trial reminder | n/a | **"Your trial ends in 2 days" email** via Resend |
| Credit paywall copy | packs only | add **"or go unlimited for $5.83/mo"** upsell line |
| Credit packs | Starter 5/$4.99, Power 20/$14.99 | unchanged |

## Current architecture (verified July 11, 2026)

- `MEMBERSHIP_PLANS` at server.js:101 — `monthly: 999`, `annual: 5999` (cents). Prices are inline `price_data` at checkout time, NOT Stripe dashboard Price objects, so repricing is purely a code change.
- Checkout: `POST /api/stripe/create-membership-checkout` (server.js ~2437) — embedded Stripe Checkout, `mode:'subscription'`, `redirect_on_completion:'never'`. Applies a one-time credit-conversion coupon (`creditDiscountCents`, capped at plan price minus $1).
- Fulfillment: `fulfillMembershipSession()` (server.js ~2519) — accepts `payment_status` of `'paid'` OR `'no_payment_required'` (the latter is what trial checkouts report, so this already works), then hard-codes `membership_status = 'active'` in the UPDATE around server.js:2539.
- Webhook (server.js ~48) already handles `customer.subscription.updated` / `.deleted` and syncs `membership_status` + `membership_period_end` (~server.js:2559).
- `isActiveMembership()` (server.js:2393) **already treats `'trialing'` as active** — no gating changes needed.
- Transactional email: Resend helper exists (server.js ~2080, `RESEND_API_KEY`; used for password reset). Key is not yet set in Railway — the email code must no-op gracefully when unset, same as the reset email does.
- All price strings in the UI live in **index.html only** (verified by repo-wide grep): plan cards ~2035–2045, and four `guarantee-note` lines at 4936, 5657, 6216, 6520 reading "$9.99/mo or $59.99/yr · 7-day money-back guarantee".

## Implementation steps

### 1. Reprice
- server.js:102–103 → `monthly: 1999`, `annual: 6999`.
- index.html plan cards: monthly `$19.99`, annual `$69.99`, "Billed $69.99/year". Annual badge currently says "BEST VALUE — $5/mo" → change to "BEST VALUE — $5.83/mo".
- The four guarantee-note lines → "$19.99/mo or $69.99/yr · 7-day free trial". (Keep the 7-day money-back guarantee mentions elsewhere if any exist standalone, but on these price lines the trial is now the lead message.)
- Sweep index.html for any other "$9.99"/"$59.99" strings (FAQ/membership copy) and update to match. Check hub.html FAQ copy too even though grep found no price strings there.

### 2. Add the 7-day trial to checkout
In `create-membership-checkout`, add to `stripe.checkout.sessions.create({...})`:

```js
subscription_data: { trial_period_days: 7 },
payment_method_collection: 'always',
```

Both plans get the trial. Card is required (`'always'` is Stripe's default for this shape, but set it explicitly so a future change can't silently make it optional).

**One-trial-per-user guard:** only include `trial_period_days` when the user has never had a subscription — condition on `row.stripe_subscription_id` being null/empty. A returning canceled member re-subscribing pays immediately; a brand-new member gets the trial.

**Fulfillment status fix:** `fulfillMembershipSession` sets `membership_status = 'active'` unconditionally. With a trial, the real subscription status is `trialing`. Retrieve the subscription (the function already fetches it for `periodEnd`) and write its actual `status` instead of the hard-coded `'active'`. During a trial, the subscription's `current_period_end`/`trial_end` is the trial end — that value lands in `membership_period_end`, which step 3 relies on.

**Coupon interaction:** the credit-conversion coupon is `duration:'once'` — with a trial it applies to the first real invoice after the trial, which is the intended behavior. No change needed; verify it in the test pass.

**Checkout UI copy:** Stripe's embedded checkout will show "7 days free, then $X". Update the `product_data.description` ("AI trainer, unlimited transformations & meal tracking. 7-day money-back guarantee.") → lead with "7-day free trial." Also update any front-end button/paywall copy near the plan picker to say "Start 7-day free trial".

### 3. Trial-ending email (2 days before)
Dan wants the reminder at exactly 2 days, so don't use Stripe's `customer.subscription.trial_will_end` event (it fires at 3 days). Instead:

- Add a nullable `trial_reminder_sent_at` timestamp column to `users` (follow the existing lightweight ALTER-if-missing pattern used for the `membership_*` columns).
- Daily sweep (a `setInterval` alongside the existing keep-warm/interval jobs in server.js, ~hourly is fine): select users where `membership_status = 'trialing'` AND `membership_period_end` is within the next 48 hours AND `trial_reminder_sent_at IS NULL` → send the email via the existing Resend helper → set `trial_reminder_sent_at`. Idempotent by construction; if `RESEND_API_KEY` is unset, log a warning and skip WITHOUT setting the flag (so it sends once the key exists).
- Email copy (plain, friendly, from the same sender identity as the password-reset email):
  - Subject: "Your Abs By AI free trial ends in 2 days"
  - Body: when the trial ends and what they'll be charged ($19.99/mo or $69.99/yr per their plan), one line on what they keep (AI trainer, nutritionist, sleep coach, unlimited transformations), and a clear "manage or cancel anytime" link to the billing portal / membership section of the hub. This email is a legal-goodwill requirement for negative-option billing — the cancel link must be prominent, not buried.

### 4. Credit paywall upsell line
On the credit-purchase paywall in index.html (the screen showing the Starter/Power packs when a non-member runs out of generations): under the packs, add a line like **"…or go unlimited for $5.83/mo — start your 7-day free trial"** linking/scrolling to the membership plan picker. $5.83 = $69.99/12; if only the monthly framing fits the layout, "$19.99/mo" is acceptable, but the $5.83 annual framing is preferred. Match the existing paywall styling.

## Verification (do before pushing, then again on prod)

1. Unit-level: `GET /api/membership` returns the new priceInCents for both plans.
2. Stripe test-mode end-to-end: subscribe as a fresh user → checkout shows "7 days free, then $19.99" → complete with test card → user row shows `membership_status = 'trialing'`, member gating unlocks (generate an image, analyze a 4th meal). Confirm a user WITH a prior `stripe_subscription_id` gets no trial.
3. Simulate the reminder: set a test user's `membership_period_end` to tomorrow, run the sweep function directly, confirm one email attempt and the flag is set; run again, confirm no second send.
4. Credit-conversion coupon: buy a credit pack on a device, then subscribe — confirm the coupon is attached and checkout still completes with the trial.
5. UI sweep: no remaining "$9.99"/"$59.99" strings anywhere in the repo (grep), paywall shows the go-unlimited line, plan cards show new prices/badge.

## Deploy notes

- Commit + push to main → Railway auto-deploys (per project workflow, no need to ask).
- **Dan actions after merge:** set `RESEND_API_KEY` in Railway (reminder emails silently skip until then — the code must tolerate this); optionally verify the Stripe webhook endpoint still has `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted` enabled (also required for the earlier membership work).
- Do NOT create Stripe dashboard Price/Product objects — pricing stays inline in code.
