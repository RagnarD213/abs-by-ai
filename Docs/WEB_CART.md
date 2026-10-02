# Web cart v2 build plan (2026-10-02, in progress)

Spec: `Docs/cart-design-20261002/`. Handoff: `Handoffs/handoff-20261002-cart-build.md`. Dan's three decisions, all yes:
Lifetime replaces Annual on the web cart; after payment a buyer with no goal picture goes to the photo upload, then
the five questions; a failed Lifetime charge retries once a day for 3 days with an email each time, then access ends.

Verified against Stripe's docs and the live account on 2026-10-02 (API `2026-09-30.endive`, Stripe.js
`js.stripe.com/endive/stripe.js`; the installed `stripe` package is 14.25, so the new sessions pass `apiVersion` per call):

- **Fields on the page.** Checkout Sessions with `ui_mode: 'elements'` (the old name was `custom`). Client:
  `stripe.initCheckoutElementsSdk({ clientSecret })`, `createExpressCheckoutElement()` for Apple Pay and Link,
  `createPaymentElement()` for the card, `loadActions()` then `actions.confirm({ email, redirect: 'if_required' })`
  from our own green button. `allowed_payment_method_types: ['card', 'link']` keeps Klarna, Cash App and Amazon Pay
  off the cart (`payment_method_types` is rejected on this API version). `absbyai.com` must be a registered payment
  method domain or Apple Pay never shows.
- **Monthly.** `mode: 'subscription'`, 7-day trial, $19.99 a month. Fulfilment is unchanged
  (`checkout.session.completed` to `fulfillMembershipSession` to the claim).
- **Lifetime.** `mode: 'setup'` with `customer_creation: 'always'`: $0 today, the card is saved, nothing recurring
  exists at Stripe. Fulfilment writes a `lifetime_pending` row (user, customer, payment method, amount, `charge_at`
  = checkout + 7 days) and sets `trialing` / `lifetime`. `lifetimeChargeSweep` (hourly) claims a due row, then creates
  one off-session PaymentIntent with an idempotency key built from the row id and the attempt number. Paid:
  `active` / `lifetime` / period end NULL, and the paid conversion is stamped from that charge. Failed: decision 3.
  Cancel before day 7 (`POST /api/membership/cancel-lifetime`): the row is cancelled, nothing is ever billed.
- **Statement name.** Read from the Stripe account (`settings.payments.statement_descriptor`, today `ABS BY AI`),
  served on `/api/config`.
- **Stripe.js trap (measured 2026-10-02).** The versioned Stripe.js the elements SDK needs (`dahlia`, `endive`)
  REMOVED `initEmbeddedCheckout` (now `createEmbeddedCheckoutPage`), and the old `v3` script refuses the elements SDK.
  While the switch is off, the page loads `v3` exactly as before; `?cart=v2` loads `endive`. The overlay checkout
  goes through `stripeEmbeddedCheckout()`, which calls the old name first and the new one only when Stripe says it
  is gone. Embedded checkout renders blank on `http://localhost` in live mode under either script: test it on HTTPS.
- **Stripe account changes made 2026-10-02:** `absbyai.com` registered as a payment method domain
  (`pmd_1UMFHoAC3gM1rghlXXXgCQLg`, Apple Pay, Google Pay and Link active); `payment_intent.succeeded` and
  `payment_intent.payment_failed` added to the `absbyai.com/api/stripe/webhook` endpoint.
- **Dark launch.** Real payments on the new cart: `absbyai.com/?join=1&from=vsl&cart=v2` (remembered for the tab).
  Look only: `absbyai.com/?demo=checkout`. Lifetime charge now, for a test buyer:
  `scripts/cart/lifetime-charge-now.sh <email>`.

---

# Web cart — pay first, account after (shipped 2026-09-10)

The membership checkout on **absbyai.com** (web only). A visitor goes **analysis page → cart → pays → account**,
instead of the old **analysis page → create account → five questions → membership screen → card**. The iOS and
Android apps are untouched: `IS_NATIVE_APP` keeps the In-App Purchase screen and the account-first flow.

Research behind it: the private "Cart teardown" artifact (2026-09-10) — MadMuscles, V Shred, BetterMe, Noom,
Muscle Booster, Blinkist; ten patterns copied / adapted / refused. Spec: `Handoffs/handoff-20260910-web-pay-first-cart.md`.

## Review without paying

- `absbyai.com/?demo=checkout` — the cart on the public sample pair. Add `&locked=1` (out-of-credits copy + lock),
  `&sex=female`. Same rules as `?demo=analysis`: no credits, no localStorage writes, no funnel events, and the pay
  button reads "Demo — checkout disabled" (a Stripe session is never created).
- `?vp=1` on any page shows the video placeholders (analysis page + cart) before the files exist.

## What is on the screen (`#cartSection` in `public/index.html`)

1. Headline tied to the result ("Your plan is ready." / locked: "Unlock your goal image — free for 7 days").
2. **Video slot** — `window.ABS_CART_VIDEO` in `public/site-video.js` (`youtubeId` or `mp4`). Empty = hidden for real
   visitors, placeholder on localhost / `?vp=1` / `?demo=checkout`. Events `cart_video_play`, `cart_video_progress`.
3. Recap: the goal image (blurred + lock when the result is locked) and one line of the analysis numbers.
4. Plans: **Monthly $19.99 — pre-selected** (`selectedPlan = 'monthly'`), Annual $69.99 with "SAVE 71%".
5. Trial timeline: today $0 → day 7 first charge, follows the plan. The day-5 reminder row and the 48-hour reminder
   email are OFF since 2026-09-30 (Dan); `TRIAL_REMINDER_ENABLED=true` on Railway turns `trialReminderSweep` back on.
6. Four benefit lines. No timers, no discount devices, no invented social proof (FTC v. MadMuscles' parent, June 2026).
7. Renewal disclosure in body-size type directly above the button, then **Start my free 7 days →**, then
   "Continue to my hub without a trial".

## How payment works

- Button → `POST /api/stripe/create-cart-checkout` (`optionalAuth`, rate-limited). Logged in: identical to
  `create-membership-checkout` (one trial per account, active-member rejection, credit coupon). Anonymous: **no
  `customer_email`** so Stripe's embedded form collects it; metadata `{kind:'membership', plan, anon:'1', deviceId,
  creditDiscountCents, adClickId, adClickType}`; 7-day trial always granted (the per-account check needs an account).
- `fulfillMembershipSession` (webhook `checkout.session.completed`, or the browser's claim / `session-status`
  fallback) for `anon` sessions: email from `customer_details.email` → `resolveCartAccount` (SELECT, then
  `INSERT … ON CONFLICT DO NOTHING RETURNING`, then re-select) → the same membership UPDATE → `recordAdClickId`
  (the gclid rode in the metadata, so the Google Ads offline feed still gets it) → a `checkout_claims` row
  (`created` true/false, 15-minute TTL) → email:
  - **new account**: `sendSetPasswordEmail` (a 7-day `password_reset_tokens` link, `/?reset=TOKEN&welcome=1`) +
    MailerLite push, log `CART_ACCOUNT_CREATED`;
  - **existing account**: `sendMembershipAttachedEmail` ("log in to continue", `/?login=1`), log
    `CART_MEMBERSHIP_ATTACHED`, plus `TRIAL_REUSE` when that account already had a subscription (allowed, logged).
  Concurrent callers for one session share one in-flight promise, so the webhook racing the browser yields one
  account, one fulfilment, one email.
- `POST /api/stripe/claim {session_id}` — the paying browser's login. Verifies the session is `complete` with Stripe,
  runs the idempotent fulfilment, then: `created` row → single-use, marks `used_at`, returns a real session token;
  pre-existing account → `{existingAccount:true, email}` and **never** logs the browser in.
- Client `handleCartComplete`: claim (retries "still activating" up to 6×) → `setLoggedIn` → **then** the
  conversions (`membership_subscribed`, Google Ads trial `AqLTCMnl4dkcEJvEqLNE` with the hashed email, TikTok
  `StartTrial`) → carry the funnel onto the account (transformation + analysis, slider height/weight) → unlock helpers
  → **"You're in"** screen (optional password → `POST /api/auth/set-password`) → the five questions as onboarding
  (`quizState.onboarding`, events `onboarding_quiz_*`) → the `returnTo` (pending feature / locked-image release / hub).
  Existing account → "log in to continue" with the email prefilled; the returnTo runs after login.
- Logged-in buyers keep the old post-payment routine (`handleMembershipComplete`).

## Analytics

New: `cart_viewed {from, locked, logged_in, plan}`, `cart_plan_selected`, `cart_checkout_opened`, `cart_skipped`,
`cart_checkout_completed {plan, anon, created}`, `account_claimed {created}`, `cart_password_set`,
`onboarding_quiz_started/completed/skipped`, `cart_video_play/progress`. Virtual pageview `/vp/cart`.
Kept: `trial_gate_shown`, `membership_subscribed`, both trial conversions, the paid conversion (`invoice.paid`).
**`account_signup` no longer sits between the trial button and payment for web buyers — rebuild PostHog funnels.**

## Dan's live card test (Claude cannot enter card numbers; there are no Stripe test keys)

1. Private window → absbyai.com → generate (or open `/?demo=analysis` to look, then use a real generation) →
   "Start your 7-day free trial" → the cart → Monthly → Start my free 7 days → Stripe form: email + card → pay ($0 today).
2. Expect: confetti, "You're in — logged in as …", the set-password email in the inbox, five questions, then the program.
3. Hub → Manage membership → cancel before day 7 → no charge. Then check Stripe (subscription trialing → canceled),
   Postgres (`users` row: status, plan, `ads_click_id`), PostHog (`cart_checkout_completed`, `account_claimed`).

## Tests

`node scripts/cart/cart-fulfillment.test.js` — pg-mem + stubbed Stripe/fetch: new email creates the account and
records the gclid and queues the set-password email; claim logs in once; existing email attaches with no claim;
webhook racing the claim → one account; logged-in sessions unchanged. 45 checks.

## Open defaults (Dan decides)

- Cart video hidden for real visitors until the file exists (default) vs a visible placeholder.
- Anonymous trial reuse: allowed and logged (default) vs blocked (blocking needs the email before the card).
- Email before checkout: no (Stripe collects it). Abandoned-checkout emails would need a field on the cart.
- **Google Pay**: off in the Stripe account; recommended on (Settings → Payment methods) — Dan's switch.
- No urgency or discount device shipped.
