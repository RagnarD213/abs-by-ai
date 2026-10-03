# Web cart: pay first, account after

The membership checkout on **absbyai.com** (web only). Live since 2026-10-03 in the approved navy design
(`Docs/cart-design-20261002/`, the boards are the authority for look and copy). It replaced the 2026-09-10 cart
(overlay Stripe sheet, Monthly plus Annual). The iOS and Android apps never see it: `IS_NATIVE_APP` keeps the In-App
Purchase screen.

**Address: `absbyai.com/cart`** (2026-10-03). `/?join=1` opens the same page: it is what the `/start` buy buttons
(`/?join=1&from=vsl`) and the apps' external links use. Every web paywall (the analysis page, hub tiles, trial gates)
goes through `showCartScreen()` in `public/index.html`.

**It shows for everyone on the web, logged in or not** (Dan, 2026-10-03). `showMembershipScreen()` sends every web
visitor to the cart; the older "Everything, unlocked" screen with Monthly and Annual cards is native-only now.
- Logged out: the email typed in step 1 becomes the account.
- Logged in: the email is the account's and is locked; the membership attaches to that account (no claim) and the
  buyer gets the same "You're in" screen without the password box.
- Admin-allowlist and beta (comp) accounts have access with no membership of their own, so they can check out.
- An account that is already paying or in a trial (`hasOwnMembership` on the server, `ownMembership` on
  `/api/membership`) still sees the cart, but step 3 says there is nothing to pay and the button reads
  "Go To My Hub". The server refuses a second membership either way.

## What is on the page (`#cartV2`, outside `.app`, full width)

Top stripe, hero box with the app screenshot and the yellow "FREE 7 days" callout, new-members notice, then three
numbered steps on one page:

1. **Your Email.** Our own field. It becomes the login. A logged-in non-member sees their email filled in and locked.
2. **Order Summary.** Monthly (pre-selected) or Lifetime. The line item and the block above the button follow the plan.
3. **Payment Information.** Stripe draws the wallet buttons (Apple Pay, Link, Google Pay if switched on) and the card
   fields. Then, Monthly only, "How This Free Trial Offer Works" with a required tick box; Lifetime shows its one
   sentence instead. Our green **Start My Free Trial** button confirms.

Below: contact line, the statement name (read from Stripe, today `ABS BY AI`), the 365-day guarantee (gold seal, the
same one as `/start`, since 2026-10-03; SVG from `Build.seal()` in the design-sales-page generator), Dan's quote,
footer. Desktop (900 px and up) adds the right column with the bullet box. No back button, no skip link, no video.

Differences from the boards that Stripe controls: the card form's own labels and field order, Country and ZIP under
the name (kept on purpose, removing ZIP can raise declines), one line of Stripe authorization text, and wallet buttons
only on devices that have them (the "or pay by card" divider hides when there are none).

## Plans

| | Monthly | Lifetime |
|---|---|---|
| Promise | 7 days free, then $19.99 a month | 7 days free, then ONE charge of $69.99, lifetime access, no recurring billing |
| Stripe session | `mode: 'subscription'`, 7-day trial | `mode: 'setup'` (card saved, nothing due, no subscription exists) |
| Who charges | Stripe Billing | Our server, once, on day 7 (`lifetimeChargeSweep`) |
| Cancel | Manage membership opens Stripe's portal | Manage membership opens our sheet (Cancel, Use a different card) |

Annual stays in `MEMBERSHIP_PLANS` for existing annual subscribers and the apps. It is not sold on the web cart.

## How payment works

- **Stripe pieces.** Checkout Sessions with `ui_mode: 'elements'`, created with `apiVersion` `2026-09-30.endive`
  per call (the installed `stripe` package pins an older version). Page script: `js.stripe.com/endive/stripe.js`.
  Client: `stripe.initCheckoutElementsSdk({ clientSecret })`, `createExpressCheckoutElement()`,
  `createPaymentElement()`, `loadActions()`, then `actions.confirm({ email, redirect: 'if_required' })`.
  `allowed_payment_method_types: ['card', 'link']` keeps Klarna, Cash App and Amazon Pay off the cart.
- **One session per plan.** `POST /api/stripe/create-cart-checkout { plan, ui: 'elements' }` when the cart opens and
  again when the buyer switches plan (the two plans are different session modes, so Stripe's fields remount). Own rate
  limit (`cartLimiter`, 40 per 15 minutes).
- **Fulfilment** (`fulfillMembershipSession`, from the webhook `checkout.session.completed` or the browser's claim):
  the email finds or creates the account, the membership is applied, the ad click id is recorded, a `checkout_claims`
  row is written, and the buyer is emailed (new account: set-password link; existing account: "log in to continue").
  The webhook racing the browser yields one account.
- **Claim.** `POST /api/stripe/claim { session_id }` logs the paying browser in once, only for an account this
  checkout created. An email that already had an account is never logged in automatically.
- **A payment that had to leave the page** returns to `/?cart_return=<session id>` and finishes the same way
  (`applyCartReturn`).
- **Wallet buyers:** the wallet supplies the email, not step 1. The tick box rule is checked in the wallet button's
  `click` event before Stripe opens the sheet.

## Lifetime: the one charge (server.js, section LIFETIME PLAN)

- Fulfilment (`saveLifetimePending`) writes a `lifetime_pending` row (`db.js`): user, Stripe customer, payment
  method, amount (6999 less any credit balance), `charge_at` = checkout + 7 days. Membership: `trialing` /
  `lifetime`, period end = `charge_at`. A newer checkout cancels an older waiting row; a live subscription on the
  same account is cancelled at Stripe; a later subscription cancels the waiting Lifetime row.
- `lifetimeChargeSweep` (hourly, first pass 60 s after boot) calls `chargeLifetimeRow`: an UPDATE moves the row from
  `pending` to `charging` (one caller wins), any already-succeeded charge for the row is recorded instead of repeated,
  then one off-session PaymentIntent with idempotency key `lifetime-<row>-attempt-<n>`.
- **Paid:** row `paid`; membership `active` / `lifetime` / period end NULL (permanent, the shape of a comp account).
  The Google Ads paid conversion is stamped from this charge (`markPaidConversionPending`).
- **Declined** (Dan, 2026-10-02): first try plus one retry a day for 3 days, an email each time
  (`sendLifetimeChargeFailedEmail`), the buyer keeps access (`past_due` with a future period end), then the row is
  `failed`, the membership `expired`, access ends. A retry uses the newest card on the customer. A Stripe outage is
  not a strike: the row goes back to `pending` untouched.
- **Cancel before the charge:** `POST /api/membership/cancel-lifetime`. The row is `canceled`, nothing is ever
  billed, access runs to the end of the 7 days.
- Deleting the account removes its rows (FK cascade), so a deleted account is never charged.
- Refunds are by hand in Stripe and do not remove access: clear the row's membership by hand if needed.

## After payment

The navy "You're in" screen with an optional password. A new buyer with no goal picture goes to the photo upload
first; the analysis page's "Build my program" then starts the five questions and ends in the trainer
(`absbyai_cart_onboarding` in localStorage). A buyer who already has a goal picture goes straight to the five
questions. An existing account gets "Log in to continue".

## Analytics

`cart_viewed {from, locked, logged_in, plan}`, `cart_plan_selected {plan: monthly|lifetime}`, `cart_terms_checked`,
`cart_checkout_opened {plan, logged_in, method}`, `account_claimed {created}`, `membership_subscribed`,
`cart_checkout_completed {plan, anon, created}`, `cart_password_set`, `lifetime_trial_cancelled`,
`onboarding_quiz_*`. Virtual pageview `/vp/cart`. Google Ads trial conversion `AqLTCMnl4dkcEJvEqLNE` with the hashed
email, TikTok `StartTrial`, the ad click ids in the session metadata. Removed with the old cart: `cart_skipped`,
`cart_video_play`, `cart_video_progress`.

## Review and testing

- Look only: `absbyai.com/?demo=checkout` (no Stripe session, pay button disabled, no events).
- Unit tests: `node scripts/cart/cart-fulfillment.test.js` (105 checks, pg-mem and a stubbed Stripe).
- End to end with fake cards: Stripe TEST keys are in `~/.absbyai-secrets.env`; the recipe, the card numbers and
  the traps are in memory `stripe-test-mode-cart-recipe`. All cases passed on 2026-10-03 (Monthly, Monthly cancel,
  Lifetime, day-7 charge, double-charge guard, cancel, decline plus 3 retries, declined at checkout, bank
  verification, existing account, logged-in buyer, photo-first routing).
- A real card: only Dan. Claude cannot type one or trigger a live charge.
  `scripts/cart/lifetime-charge-now.sh <email>` runs one buyer's Lifetime charge now instead of on day 7 (it calls
  `POST /api/admin/lifetime/charge-now` with the dashboard key).

## Traps

- **Stripe.js versions.** The versioned script (`dahlia`, `endive`) REMOVED `initEmbeddedCheckout` (now
  `createEmbeddedCheckoutPage`); the old `v3` script refuses the elements SDK. The overlay checkout that print orders
  still use goes through `stripeEmbeddedCheckout()`, which tries the old name first.
- Embedded checkout renders blank on `http://localhost` with live keys under any script. Test it on HTTPS.
- `payment_method_types` is rejected on the `endive` API version; use `allowed_payment_method_types`.
- With Link left on inside the Payment Element, Stripe adds a "Bank" tab and a save-my-details box: the element is
  created with `wallets: { link: 'never' }`; Link lives in the wallet buttons.
- The page must show the session's own total (`session.total.total.amount`) or `confirm` throws: Order Total is
  bound to it (it reads $0.00 for both plans).
- Stripe account settings this depends on (set 2026-10-02): `absbyai.com` registered as a payment method domain
  (Apple Pay, Google Pay, Link active); `payment_intent.succeeded` and `payment_intent.payment_failed` on the
  `absbyai.com/api/stripe/webhook` endpoint. Google Pay is still switched off in Stripe (Dan's switch).
- Every web deploy reaches the iOS and Android wrappers: confirm they still show In-App Purchase and never this cart.
