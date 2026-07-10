# HANDOFF — iOS App Store membership strategy (decision memo + plan)

**Status: PLAN ONLY. Do not implement.** Implementation is a separate task once Dan
picks a path and Xcode 26 is installed. This memo answers "how do we sell the $9.99/mo
and $59.99/yr membership inside the iOS app without an App Store rejection, while keeping
Stripe as the single source of truth."

Grounding facts from the current code:
- Prices: `MEMBERSHIP_PLANS` in `server.js:102` — monthly `999`¢, annual `5999`¢.
- Checkout uses inline `price_data` (server.js:2468), **not** stored Stripe price IDs.
- Entitlement lives entirely on the user row: `membership_status`, `membership_plan`,
  `membership_period_end`, `stripe_customer_id`, `stripe_subscription_id`
  (`db.js:147`). `isActiveMembership()` (server.js:2393) is the single gate every
  feature checks. There is **no `membership_source` column yet** — added in this plan.
- Webhook keeps the row in sync: `fulfillMembershipSession` + `syncSubscriptionState`
  (server.js:2496, 2534).

---

## 1. Recommendation

**Ship the iOS app US-first with an External Purchase Link to the existing web Stripe
checkout, plus in-app login so web members use the app immediately. Keep StoreKit 2 IAP
as a documented, ready-to-build fallback — do not build it now.**

Why, in one line: the April 2025 *Epic v. Apple* contempt ruling lets US apps link to
outside payment **commission-free**, so the cheapest path is also now an Apple-permitted
one — and it reuses the Stripe stack that already exists and is the source of truth.

### The three options, with Dan's actual numbers

Net revenue **per subscriber per year**, at Dan's price points. Stripe fee = 2.9% + $0.30
per charge. Apple = 15% (Small Business Program — Dan is well under the $1M/yr threshold,
so 15% applies from day one, not the standard 30%-year-one rate).

| Path | Monthly plan ($119.88/yr gross) | Annual plan ($59.99/yr gross) |
|---|---|---|
| **Web Stripe** (external link or web) | 12×$0.59 fees → **net ≈ $112.82** | $2.04 fee → **net ≈ $57.95** |
| **Apple IAP** (15% SBP) | 15% = $17.98 → **net ≈ $101.90** | 15% = $9.00 → **net ≈ $50.99** |
| **Difference Apple takes** | **≈ $10.92/yr** (~9.7%) | **≈ $6.96/yr** (~11.6%) |

Blended sanity check at 100 members (70 monthly / 30 annual):
- Web/external-link: **≈ $9,636/yr net**
- All-IAP: **≈ $8,663/yr net** → Apple tax ≈ **$973/yr (~10%)**.

At Dan's current scale (near-zero members) the *dollar* gap is small, so the decision is
driven by **build cost and App Review risk, not margin.** That's what tips it to the
external link: zero StoreKit code, zero receipt-validation surface, reuse of a Stripe
pipeline that already works and is already the source of truth.

### Option A — External Purchase Link (RECOMMENDED, US-first)
- **What it is:** a button in the app that opens the web checkout (`absbyai.com`) in the
  system browser. Purchase happens on the web via the existing Stripe flow; the app never
  processes payment.
- **Commission:** In the US, **0%** as of the April 30 2025 contempt ruling in *Epic v.
  Apple*, which bars Apple from charging commission on external-link purchases and from
  restricting link placement/wording. The Ninth Circuit declined to stay the injunction,
  so it is in force in the US **pending Apple's appeal** (see risk note §4).
- **Pros:** no StoreKit build, no receipt validation, no App-Store-Server-Notifications
  listener, Stripe stays the sole source of truth, best margin, fastest to ship.
- **Cons:** legally contingent on a ruling under appeal; **US-only** — this does not
  license the same button in most other App Store storefronts (see §4). Slightly worse
  in-app conversion than a one-tap native sheet.

### Option B — StoreKit 2 In-App Purchase
- **What it is:** native Apple subscription products ($9.99/mo, $59.99/yr) purchased with
  a one-tap Apple sheet; Apple bills the user; we validate the receipt server-side and
  mirror the entitlement onto `users.membership_*`.
- **Commission:** 15% (SBP). Best in-app conversion; the only path Apple unconditionally
  blesses worldwide.
- **Pros:** universally compliant, highest conversion, works in every storefront.
- **Cons:** real engineering — StoreKit plugin, receipt-validation endpoint, ASSN v2
  listener, and a **dual source of truth** problem (Apple *and* Stripe can both own a
  subscription — see §3 collision handling). Ongoing 15% tax.

### Option C — "Reader-style" login-only (no purchase, no link)
- **What it is:** the app sells nothing and doesn't even link out. Users must already
  know to subscribe on the web; the app just logs them in.
- **Commission:** none.
- **Pros:** lowest possible App Review risk; zero payment code.
- **Cons:** worst conversion — a new iOS user who wants to subscribe hits a dead end.
  Only defensible as a stopgap. **Not recommended** except as an immediate day-one
  submission while Option A/B is finished.

**Recommendation restated:** launch on **A (external link, US)**. If/when Dan wants
non-US storefronts or the appeal reverses the US ruling, fall back to **B (IAP)** using
the plan in §2. Option C is the safe fallback if a reviewer rejects the external link
before the appeal settles — flip a server flag to hide the link and the app degrades to
login-only without a resubmission-blocking change.

---

## 2. If IAP (Option B) — implementation design

Written so this can be built directly later. Nothing here should be built now.

### 2a. Plugin choice — StoreKit 2 wrapper
- **`@capacitor-community/in-app-purchases`** (or the maintained StoreKit 2 community
  plugin): thin StoreKit 2 binding, no per-transaction fee, but **we** write the
  receipt-validation and entitlement-sync logic.
- **RevenueCat** (`@revenuecat/purchases-capacitor`): hosted entitlement layer, handles
  receipt validation, ASSN, restore, upgrade/downgrade, and cross-platform mapping for
  us. **Pricing: free under $2,500/mo tracked revenue, then 1% of tracked revenue.** At
  Dan's scale it is effectively free.
- **Call:** **Start with RevenueCat.** The 1% (which is $0 until Dan clears $2.5k/mo)
  buys away the two riskiest pieces of a from-scratch build — Apple receipt validation
  and App Store Server Notifications plumbing — and gives restore/upgrade for free. Once
  volume makes the 1% material, the community plugin + our own validation is a
  known-scoped migration. Do not hand-roll StoreKit receipt validation for launch.
  Whichever is used, **Apple must never become the source of truth** — it feeds
  `users.membership_*`, same as Stripe does today.

### 2b. Server-side receipt validation endpoint
New endpoint, e.g. `POST /api/iap/apple/verify`:
1. Auth via the existing `requireAuth` (server.js) so we know which `users.id` to credit.
2. Body: the StoreKit 2 signed transaction (JWS) or, with RevenueCat, the RC customer-info
   / webhook payload.
3. Verify the JWS signature against Apple's root certs (or trust RevenueCat's verified
   webhook, HMAC-checked). **Never trust a client-reported "I'm subscribed" boolean.**
4. On a valid active transaction, write the entitlement (see §2c) and return the same
   shape `/api/membership` returns today so the SPA needs no new client logic.

### 2c. Mapping an Apple subscription onto `users.membership_*`
- **Add one column** to the `db.js:147` migration loop:
  `'membership_source TEXT'` (values: `'stripe'` | `'apple'`; default/null = `'stripe'`
  for every existing row). This is the only schema change required.
- On a validated Apple transaction, set:
  `membership_status='active'`, `membership_plan` = `'monthly'`|`'annual'` (map from the
  Apple product id, e.g. `com.absbyai.app.membership.monthly`), `membership_period_end`
  = Apple's `expiresDate`, `membership_source='apple'`, and store the Apple
  `originalTransactionId` in a new `apple_original_txn_id TEXT` column (the stable key
  ASSN events arrive on — the Apple analogue of `stripe_subscription_id`).
- **`isActiveMembership()` needs no change** — it already keys off `membership_status`
  and `membership_period_end`, which are source-agnostic. That's the payoff of the
  existing design: gates don't care who billed the user.

### 2d. App Store Server Notifications v2 (the webhook-equivalent)
- Apple's ASSN v2 is the analogue of the Stripe webhook. Register an endpoint
  `POST /api/iap/apple/notifications`; Apple POSTs signed events (`DID_RENEW`,
  `DID_CHANGE_RENEWAL_STATUS`, `EXPIRED`, `REFUND`, `GRACE_PERIOD_EXPIRED`, …).
- Verify the JWS, look up the user by `apple_original_txn_id`, then call the Apple
  equivalent of `syncSubscriptionState()` (server.js:2534): update `membership_status`
  and `membership_period_end`. `REFUND`/`EXPIRED` → close the gate exactly like a Stripe
  `customer.subscription.deleted`.
- With RevenueCat, subscribe to RC webhooks instead — same handler shape, RC has already
  validated with Apple.

---

## 3. Restore, family sharing, upgrade/downgrade, and the collision case

- **Restore purchases** (Apple requires a visible "Restore Purchases" control on any
  screen that sells IAP): call StoreKit `Transaction.currentEntitlements` (or
  RevenueCat `restorePurchases()`), re-verify server-side, re-attach the entitlement to
  the logged-in `users.id`. Because entitlement is keyed to our account, restore after a
  reinstall or on a new device Just Works once the user logs in.
- **Family Sharing:** Apple auto-renewable subs *can* be family-shared if enabled in App
  Store Connect. **Recommend leaving it OFF** for launch — a shared sub would grant our
  per-account AI features (Trainer/Nutritionist/Counsel are personalized and metered per
  user, e.g. `COUNSEL_MONTHLY_CAP`) to family members who don't have their own account
  row, which breaks per-user metering. Revisit only with a deliberate design.
- **Upgrade/downgrade monthly↔annual:** within IAP, put both products in the **same
  StoreKit subscription group** so Apple handles proration/crossgrade natively (immediate
  upgrade, deferred downgrade). ASSN `DID_CHANGE_RENEWAL_PREF` then updates
  `membership_plan`/`membership_period_end`. Across ecosystems (Apple↔Stripe) there is no
  automatic migration — treat that as a cancel-here/subscribe-there, guarded by §3's
  collision rule.
- **"Already a web member" collision (the important one):** a user with an active Stripe
  membership must **not** be able to also buy the Apple IAP (or vice versa) — that's
  double billing.
  - Before showing the IAP paywall, call `/api/membership`; if `isActiveMembership()` is
    true and `membership_source='stripe'`, **hide IAP** and show "You're already a member
    (billed on the web). Manage it at absbyai.com." — mirror of the existing guard at
    server.js:2446 that already 400s a duplicate web subscribe.
  - The verify endpoint (§2b) must also **reject** an Apple purchase for a user who is
    already active via Stripe (refund the Apple txn / never activate) — belt and
    suspenders in case the client races the check.
  - Only one `membership_source` may be active at a time; switching ecosystems requires
    cancelling the first. Document this as an invariant.

---

## 4. App Review risk notes

- **Which path is safe to *say* what:**
  - **Option A (external link), US:** post-ruling, Apple may not reject solely for the
    presence of an external purchase link or dictate its wording in the US. Still, keep
    review notes factual: "Digital membership is purchased on our website; the app links
    out to it." Do not editorialize about Apple's fees in the UI.
  - **Non-US storefronts:** the US injunction does **not** globally license the external
    link. In other regions the app must either use IAP, use Apple's separate (and
    commissioned) External Purchase Link Entitlement where offered, or **not sell/link at
    all**. Simplest launch: **restrict availability to the US App Store**, or
    geo-gate the link server-side (a `showExternalPurchaseLink` flag off outside the US),
    degrading to Option C elsewhere.
- **The physical-goods carve-out is unaffected:** Stripe checkout for printed
  posters/canvas stays compliant under guideline 3.1.3(e) (physical goods) — already
  noted in `HANDOFF_iOS_APP_STORE.md` §6. Keep that Review-Notes language; it's about the
  print store, not the membership.
- **Kill-switch for a surprise rejection:** gate the in-app purchase/link behind a
  server flag (reuse the pattern of `getStripe()` returning 503 when unconfigured). If a
  reviewer rejects the external link before the appeal settles, flip the flag → the app
  becomes Option C (login-only) with no code change or blocking resubmission, and web
  signups continue.
- **Don't ship a paywall the reviewer can't complete:** whichever path, make sure a
  reviewer can reach a working purchase or a clear "buy on web" path — a dead-end paywall
  triggers guideline 3.1.1 / 2.1 rejections.
- **Legal-flux caveat (write this down):** Option A's 0% commission rests on an
  injunction Apple is appealing. If the Ninth Circuit reverses, US external links revert
  to Apple's commissioned External Purchase Link Entitlement (historically 27%/12%) — at
  which point the math flips toward IAP and Dan should execute the §2 plan. Re-check this
  status before submission, not from this memo's date.

---

## Bottom line for Dan
1. Ship iOS **US-first with the external web-checkout link** + login. No StoreKit code.
   Best margin, least build, currently Apple-permitted in the US.
2. Keep this doc's **§2 IAP plan on the shelf** (RevenueCat first) for when you go global
   or if Apple's appeal reverses the US rule.
3. The **only schema change** either path ever needs is one `membership_source` column in
   `db.js` — `isActiveMembership()` and every feature gate already work source-agnostically.
4. Put the in-app purchase link behind a **server flag** so a rejection is a config flip,
   not a resubmission.
