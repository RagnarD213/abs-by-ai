# Abs by AI — Apple In-App Purchase subscription plan

Execution reference for `Handoffs/handoff-20260807-ios-iap-and-resubmission.md`.
Everything here must exist before the app can be resubmitted.

---

## Phase 0 — Dan's hands (blocks everything)

These four cannot be done by Claude: they need Dan's Apple ID password, his personal
tax/banking details, and a new account signup.

### 0.1 Paid Applications agreement — REQUIRED, blocks product creation

1. Go to **appstoreconnect.apple.com** → **Business** (top nav; older UI calls it
   "Agreements, Tax, and Banking").
2. Under **Agreements**, find **Paid Applications**. Status will say
   *"Request"* or *"Action needed"*.
3. Click **Request** / **Set Up**, read, tick the box, **Agree**.
4. Status changes to **Pending User Info**. Three sub-tasks appear:
   - **Contact info** — add yourself for all four roles (Financial, Technical,
     Legal, Senior Management). Same person is fine for a solo developer.
   - **Bank account** — add the account Apple should pay into. Needs routing +
     account number and the bank's name/address.
   - **Tax forms** — for a US individual/LLC this is the **U.S. Tax Form (W-9)**.
     Complete it. Non-US tax forms are only needed if selling outside the US —
     we are US-only, so skip those if offered.
5. When all three are green the agreement flips to **Active**. That can take a
   few minutes; occasionally a few hours for the bank details.

**Nothing in Phase 1 works until this reads Active.** In-app purchase products
cannot be created, and a submitted binary containing IAP will be rejected.

### 0.2 Small Business Program — 15% instead of 30% commission

Non-blocking, do it in parallel. **developer.apple.com/app-store/small-business-program/**
→ Enroll. Requires under $1M proceeds in the prior calendar year, which we
comfortably are. Takes ~2 minutes and cuts Apple's cut in half.

### 0.3 RevenueCat account — free

1. **app.revenuecat.com** → Sign up (free tier covers us to ~$2.5k/mo tracked revenue).
2. Create a project named **Abs by AI**.
3. Add an **App Store** app: bundle id `com.absbyai.app`.
4. Leave the rest — Claude configures products, entitlements and the webhook once
   the App Store Connect products exist.

### 0.4 App Store Connect API key for RevenueCat — needed for server notifications

RevenueCat needs an **In-App Purchase key** to validate and to receive Apple's
server notifications:

1. App Store Connect → **Users and Access** → **Integrations** → **In-App Purchase**.
2. **Generate In-App Purchase Key**, name it `RevenueCat`, download the `.p8`.
   **The download is one-time.** Save it somewhere safe.
3. Hand the `.p8` + its Key ID to the RevenueCat app settings (Claude can do this
   step once Dan is signed in, or Dan can upload it directly).

---

## Phase 1 — App Store Connect products — ✅ BUILT 2026-08-07

Everything below is created and saved. Apple IDs and the group id, recorded so
they never have to be looked up again:

| Object | Identifier |
|---|---|
| Subscription group | **22294450** — "Abs by AI Membership" |
| Annual | Apple ID **6799227966** — `com.absbyai.app.membership.annual`, 1 year, $19.99→**$69.99** US, free first week, level 1 |
| Monthly | Apple ID **6799231479** — `com.absbyai.app.membership.monthly`, 1 month, **$19.99** US, free first week, level 2 |

**Three things that differed from this plan and are worth knowing:**

1. **Subscription descriptions are capped at 55 characters** (display names at 35).
   Both products use `Unlimited AI transformations, training & nutrition.` (51).
   The longer marketing descriptions originally drafted here do not fit.
2. **Apple has no "7 days" free-trial option** — the durations are 3 days, 1 week,
   2 weeks, 1 month, … We used **1 Week**, which is exactly 7 days and matches the
   web copy ("7 days free").
3. **Annual is level 1, Monthly level 2**, deliberately. Level order defines
   upgrade vs downgrade, so monthly→annual is an upgrade (immediate, prorated) and
   annual→monthly is a downgrade (applies at renewal).

**Still outstanding on these products:** each needs a **review screenshot of the
in-app purchase screen**, which cannot be captured until the Phase 2 UI exists.
Also note Apple's banner: *"Your first subscription group must be submitted with
a new app version"* — confirming build 1.0 (2) is required, as planned.

**App Store Connect UI trap, cost several minutes:** the `Subscription Duration`
and `Localization` dropdowns are real `<select>` elements, but clicking them or
driving them with synthetic keystrokes does **not** register — the value stays
"Choose" and the Create button stays disabled. The fix is to set the value through
the native `HTMLSelectElement.prototype.value` setter and then dispatch bubbling
`input` + `change` events. The price and country pickers are *custom* components
with no `<select>` at all, and those must be clicked normally (type into the
search box, click the result).

### Original spec (kept for reference)

App Store Connect → **Abs by AI** → **Monetization** → **Subscriptions**.

### Subscription group

**Reference name:** `Abs by AI Membership`
**Group display name (user-visible, on the Apple receipt):** `Abs by AI Membership`

Both products live in this one group, so a member can upgrade/downgrade between
monthly and annual and Apple prorates it. Two separate groups would let someone
buy both at once — do not do that.

### Product 1 — Monthly

| Field | Value |
|---|---|
| Reference name | `Abs by AI Monthly` |
| Product ID | `com.absbyai.app.membership.monthly` |
| Duration | 1 Month |
| Price | **$19.99** USD (US only) |
| Display name | `Monthly Membership` |
| Description | `Unlimited AI transformations, your full AI training program, AI Nutritionist meal plans, unlimited macro tracking, Sleep Coach and Supplement Audits.` |
| Introductory offer | **Free — 7 days**, new subscribers, US storefront |

### Product 2 — Annual

| Field | Value |
|---|---|
| Reference name | `Abs by AI Annual` |
| Product ID | `com.absbyai.app.membership.annual` |
| Duration | 1 Year |
| Price | **$69.99** USD (US only) |
| Display name | `Annual Membership` |
| Description | `Everything in the monthly membership at $5.83/month — unlimited AI transformations, your full AI training program, AI Nutritionist meal plans, macro tracking, Sleep Coach and Supplement Audits.` |
| Introductory offer | **Free — 7 days**, new subscribers, US storefront |

> **Product IDs are permanent.** They cannot be renamed or reused after creation.
> Note the deviation from the handoff, which wrote `.yearly`: `.annual` is used so
> the id matches our own `MEMBERSHIP_PLANS.annual` key in `server.js` exactly.
> Apple is indifferent; this only affects our own mapping code.

> **Both plans get the 7-day free trial**, matching what the web checkout offers
> today (`public/index.html`: "7 days free, then $19.99/mo or $69.99/yr").
> Apple grants an introductory offer only once per subscription *group*, so a user
> who trials monthly and later switches to annual will not get a second free week —
> same as Stripe, where the trial is once per user.

### Required per-product assets

Each subscription needs, before it can be submitted:
- **Localization** (display name + description above) for English (U.S.).
- **Review screenshot** — a screenshot of the in-app purchase screen. Capture from
  the iOS simulator once Phase 2 UI is built. One image, any size, must show the
  plan cards and prices.
- **Review notes** — reuse: *"Sign in or create a free account, then open Member
  Hub → Membership. The purchase screen shows both plans."*

### Required app-level links (Apple rejects auto-renewables without these)

- App Store Connect → App Information → **EULA**: leave as Apple's standard EULA,
  and put `https://absbyai.com/terms` in the **License Agreement URL** field if
  offered; the Privacy Policy URL is already `https://absbyai.com/privacy`.
- **In the app itself**, the purchase screen must display, adjacent to the buy
  button: title, length, price of the subscription, plus tappable **Terms of Use**
  and **Privacy Policy** links, and the auto-renewal disclosure. Phase 2 builds this.

---

## Phase 2 — RevenueCat configuration (Claude, after 0.3/0.4 and Phase 1)

### RevenueCat dashboard

| Object | Identifier | Contents |
|---|---|---|
| Entitlement | `membership` | both products attached |
| Offering | `default` (make it Current) | 2 packages |
| Package — monthly | `$rc_monthly` | `com.absbyai.app.membership.monthly` |
| Package — annual | `$rc_annual` | `com.absbyai.app.membership.annual` |

Using RevenueCat's standard package identifiers (`$rc_monthly` / `$rc_annual`)
means the client can read the offering generically and never hardcodes a price.

### Keys to collect

| Key | Where it goes | Notes |
|---|---|---|
| **Public SDK key** (`appl_…`) | `public/index.html` constant | Safe to ship in client code — it is a publishable key |
| **Secret API key** (`sk_…`) | Railway env `REVENUECAT_SECRET_KEY` | Server-side REST lookups only. Never in the client |
| **Webhook auth header** (any random string we choose) | Railway env `REVENUECAT_WEBHOOK_SECRET` + RevenueCat webhook config | Verifies inbound webhooks are really from RevenueCat |

### Webhook

RevenueCat → Integrations → Webhooks:
- URL: `https://absbyai.com/api/revenuecat/webhook`
- Authorization header: the shared secret above
- Events: all (we act on `INITIAL_PURCHASE`, `RENEWAL`, `CANCELLATION`,
  `EXPIRATION`, `PRODUCT_CHANGE`, `BILLING_ISSUE`)

### App user identity — the load-bearing bit

The RevenueCat `app_user_id` **must be our own `users.id`**, set via `logIn` right
after the user authenticates in the web page. That is the key the webhook uses to
find the account to unlock. If it is left anonymous, a purchase cannot be attached
to an account and the member gets nothing.

---

## Phase 3 — Server (Claude)

- New column `membership_source TEXT` on `users` (`'stripe'` | `'apple'` | null).
- `POST /api/revenuecat/webhook` — constant-time compare on the auth header, map
  events onto `membership_status` / `membership_period_end` / `membership_plan`,
  keyed on `app_user_id`.
- `POST /api/apple/sync` — authenticated; the server calls RevenueCat's REST API
  with the **secret** key to read the caller's own entitlements and grants from
  that. Covers webhook latency so the buyer is unlocked instantly. The client's
  word is never trusted.
- Stripe safety: the delete-account cancel gate and any cancel/manage path must
  skip Apple-billed members (`membership_source = 'apple'`, no
  `stripe_subscription_id`). Apple members manage at
  `https://apps.apple.com/account/subscriptions`.

---

## Phase 4 — Sandbox testing

Sandbox tester: App Store Connect → **Users and Access** → **Sandbox** → **Test
Accounts** → add one with a fresh email (a `+sandbox` Gmail alias works).
Sign in on the device at **Settings → App Store → Sandbox Account** — *not* the
main Apple ID. Sandbox subscriptions renew on an accelerated clock (1 month = 5
minutes), so the whole trial → renew → expire loop is testable in under an hour.

---

## Cost math, for the record

| | Web (Stripe) | iOS (Apple, Small Business Program) |
|---|---|---|
| $19.99/mo | ~$18.72 net (2.9% + 30¢) | **$16.99 net** (15%) |
| $69.99/yr | ~$67.66 net | **$59.49 net** |

Apple costs roughly $1.73/month more per member than Stripe. That is the price of
being in the App Store; the web checkout stays the cheaper path and is unchanged
for web visitors.
