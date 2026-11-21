# Handoff: Web pay-first checkout — a research-led cart that comes BEFORE the account

**Date:** 2026-09-10
**Project:** Abs By AI — absbyai.com, **web only** (the iOS and Android apps are out of scope)
**Business goal this serves:** Profitability. The steps between "saw my analysis" and "card entered" are where the funnel dies.
**Status:** spec'd, NOT executed. No dashboard row (Dan's 2026-09-08 rule: only when he asks).

## Objective

Rebuild the membership checkout ("the cart") so a web visitor goes **analysis page → cart → pays → gets an account**,
instead of today's **analysis page → create account → five questions → membership screen → card**. The cart is designed
from a short teardown of high-converting direct-response fitness carts, carries a short-video slot (placeholder for now),
and offers Monthly and Annual with **Monthly pre-selected**. The questions move to after payment, as onboarding.

## Dan's asks (the acceptance list — 2026-09-10)

1. **Research** high-converting carts and find a few examples, "like the Mad Muscles cart and the V Shred cart."
2. **Show Dan** a few carts that work well for direct-response competitors, **then build** the new cart based on them.
3. **A short video in the cart.** He does not have the video yet, so it is a **placeholder** for now.
4. **Annual or Monthly** at checkout, with **Monthly as the default**.

## Why — the evidence (measured 2026-09-09, production only)

PostHog ordered funnel, last 60 days, 1-day window, `$current_url` contains absbyai.com:

| Step | People |
|---|---|
| `trial_gate_shown` (tapped a trial button) | 16 |
| `account_signup` | 6 |
| `quiz_completed` | 3 |
| `membership_screen_viewed` | 3 |
| `membership_subscribed` | 0 |

Stripe, `mode=subscription` checkout sessions, last 60 days: **11 opened, 1 completed** (the trial whose card was
declined at trial end on 2026-09-01), 9 expired, 1 open. A session is only created when someone taps Start trial on the
membership screen (`handleMembershipSubscribe` → `create-membership-checkout` → `initEmbeddedCheckout`), so each one is a
person who reached the card form. Postgres: 11 real accounts in 60 days with test emails excluded — 7 `none`, 3 `comp`,
1 `active`.

**Read this carefully:** that is far too little traffic to prove anything, and the early-August Stripe sessions look like
testing around the iOS resubmission. The direction is clear (the account wall is the biggest drop, the questions cost
half of what is left, and the card page itself converts badly), and the category pattern agrees (MadMuscles takes the card
before the email). Decide on direction + pattern + reversibility. **Do not set up an A/B test at this volume.**

## Current State (read before touching anything — line numbers drift, grep the function names)

### The web flow today (`public/index.html`)

- **Analysis page** `#analysisSection`: the top CTA `#anTopCta` and bottom `#anTrialBtn` both call `primaryCta()` →
  member: `openTrainer()`; locked result: `startTrialAndUnlock()`; otherwise `showTrialGate(null)`.
- **`showTrialGate(feature)`** (~6459): fires `trial_gate_shown`; logged in → `showMembershipScreen(openPendingTrialFeature,
  {trialGate:true})`; logged out → `showAuthScreen('signup', {trialGate:true})`.
- **After signup:** `continueTrialAfterAccountCreation()` (~6227) → `seedProfileFromFunnel()` + `startQuiz()` →
  `finishQuiz()` (~6426) → `proceedToTrialGate(planReady)` (~6454) → `showMembershipScreen(…, {trialGate:true, planReady})`.
- **Membership screen** `#membershipSection` (~2796): "Everything, unlocked", a 7-bullet benefit list, plan cards
  (`#planAnnual` listed FIRST with "BEST VALUE — $5.83/mo", then `#planMonthly`), the renewal disclosure
  (`.guarantee-note`), `#membershipSubscribeBtn`. **Today's default plan is ANNUAL:** `let selectedPlan = 'annual';`
  (~7835); the plan-card click handler is ~9036.
- **`handleMembershipSubscribe()`** (~8015): `if (IS_NATIVE_APP) return;` then **`if (!isLoggedIn())` → signup** (a second
  account-first gate). Then `POST /api/stripe/create-membership-checkout` with `{plan, deviceId, adClickId, adClickType}`
  → `Stripe(...).initEmbeddedCheckout({clientSecret, onComplete})` mounted in `#checkoutOverlay` / `#checkout`.
- **`handleMembershipComplete(sessionId)`** (~8050): `GET /api/stripe/session-status` (fallback fulfillment) → PostHog
  `membership_subscribed {plan}` → **`fireAdConversion('AqLTCMnl4dkcEJvEqLNE', {value:20})`** (the trial-start conversion)
  → **`fireTikTokEvent('StartTrial')`** → `refreshMembership()` → confetti/toast.
- **`fireAdConversion`** (~3535) attaches the enhanced-conversions email **only when `isLoggedIn()`** (`auth.email`). An
  account-less buyer would send the trial conversion with no hashed email unless the order of operations changes.
- **Paid (post-trial) conversion:** `reportPaidMembershipConversion` (~7880) fires `AD_SUBSCRIBE_LABEL` when the server
  flags it, keyed on the account (`paid_conversion_fired_at`), stamped from Stripe `invoice.paid` (memory
  `stripe-trial-end-active-before-charge`). Unchanged by this work, but it needs the account to exist.
- **Every other entry point into `showMembershipScreen`** must reach the new cart for a non-member on the web: hub "Become a
  member" (~7299), hub preview join (~5831), hub tiles in preview mode (~7312 → `showTrialGate(feature)`), the 402
  handlers in trainer / program / nutrition / counsel / sleep / macro / progress (~7793, 8714, 8800, 8813, 9007, 9594,
  9623, 9659, 10250, 10289, 10315, 10604, 11432), transformations (~6921), and the locked-result path
  `startTrialAndUnlock()` (~3817), whose callback releases the held sharp image once the user is a member.

### Server (`server.js`)

- **`POST /api/stripe/create-membership-checkout`** (~6321): `requireAuth`; `recordAdClickId(req.user.id, adClickId,
  adClickType)` (feeds the Google Ads offline-conversion CSV at `/api/ads/offline-conversions.csv`); rejects existing
  active members; a credit-conversion coupon keyed on `deviceId` (`creditDiscountCents`); `isFirstSubscription =
  !row.stripe_subscription_id` so the 7-day trial is **one per account**. Session: `ui_mode:'embedded'`,
  `mode:'subscription'`, `redirect_on_completion:'never'`, `customer_email: req.user.email`,
  `payment_method_collection:'always'`, `price_data` from `MEMBERSHIP_PLANS` (monthly 1999/month, annual 6999/year),
  `metadata {kind:'membership', plan, userId, deviceId, creditDiscountCents}`.
- **Webhook** `checkout.session.completed` (~43) → `meta.kind === 'membership'` → **`fulfillMembershipSession(session)`**
  (~6524): **returns false without `meta.userId`**; idempotent via `creditsStore.fulfilled['member_' + sid]`; `UPDATE users
  SET stripe_customer_id, stripe_subscription_id, status, plan, period_end WHERE id = userId`.
- **`GET /api/stripe/session-status`** (~10116): unauthenticated, keyed by `session_id`; runs the same idempotent
  fulfillment when the session is complete (the webhook may land after the browser's `onComplete`).
- **Password reset — reuse it for "set your password":** `sendResetEmail(email, token)` (~4693),
  `POST /api/auth/request-reset` (~5023, `password_reset_tokens`, 60-minute expiry), `POST /api/auth/reset-password` (~5043).
- **The trial-ending reminder EXISTS:** `trialReminderSweep` emails 2 days before the trial ends (~4712, ~6956;
  `users.trial_reminder_sent_at`). The cart may truthfully say "we'll email you 2 days before your trial ends."
- **Stripe account:** live keys only (`sk_live` / `pk_live`; no test keys in `~/.absbyai-secrets.env`). Payment-method
  configuration "Default": card on, **Apple Pay on, Google Pay OFF**, Link on.

### Related, out of scope

- **iOS In-App Purchase pay-first** is its own doc: `Handoffs/handoff-20260812-purchase-before-account.md`, gated on Apple
  approval and the RevenueCat audit. **Do not touch** `#iapSection`, `handleIapSubscribe`, `parseAppUserId` or any IAP code.
- **Native apps** (`IS_NATIVE_APP` — the iOS wrapper and the Android TWA) keep today's account-first behavior exactly.

## Key Decisions Already Made (do not reopen)

- **Web only.** Native keeps IAP and account-first until the iOS handoff runs (memories `platform-scoped-compliance`,
  `native-app-iap-gating`).
- **Card before account.** Stripe collects the email with the card; the account is created from that email after payment.
- **An account is still required afterwards** — memberships, programs, meal plans and the gallery all key off `users`.
  This is "purchase before account", not "purchase instead of account".
- **The questions move to after payment**, as onboarding. The earlier "quiz stays before the paywall" rule (in the iOS
  handoff) predates the analysis page, which now does the personalization job; the funnel lost half its people at the
  quiz. The quiz still runs, right after the account is claimed, and still skips the height/weight step when the
  analysis-page sliders were set.
- **Monthly is the default plan**; Annual stays as an option with its savings shown (Dan, 2026-09-10).
- **The cart has a video slot**, placeholder only until the video exists (Dan).
- **Research first, show Dan, then build** (Dan).
- **Compliance is the moat.** MadMuscles' parent, Genesis Tech, was halted by a federal court on the FTC's motion on
  2026-06-17 for hidden auto-renew terms, unauthorized and double charges, and obstructed cancellation (memory
  `madmuscles-deep-dive`). Copy their structure; never copy their tricks.
- **One-tap wallets matter on phones.** Apple Pay is on; turning **Google Pay** on is a Stripe account-settings change —
  **ask Dan in chat before flipping it.**

## Detailed Plan

### Phase 0 — orient (~15 min)

1. Read this doc, `AI_COORDINATION.md`, and the memories `madmuscles-deep-dive`, `youtube-ad-competitor-research`,
   `ad-suspension-prevention`, `native-app-iap-gating`, `platform-scoped-compliance`, `stripe-trial-end-active-before-charge`,
   `deploy-drops-locked-holds`, `local-funnel-test-recipe`, `github-push-false-failure`.
2. Add a one-line ACTIVE TASK entry to `AI_COORDINATION.md`.

### Phase 1 — research: high-converting direct-response carts

1. **Targets:** MadMuscles and V Shred (Dan named both), plus two to four of BetterMe, Muscle Booster, Noom, Fitme,
   Unimeal, Freeletics — prefer the biggest spenders (`youtube-ad-competitor-research`: V Shred ~$20M/yr, Fitme ~$48M/yr,
   Muscle Booster ~$35M/yr).
2. **How to look:**
   - Walk the live funnels in the **in-app Browser pane**, not Dan's Chrome. Clicking generic quiz answers is fine.
   - **Stop at any email, phone, name or payment field.** Never enter real or invented personal data; never submit a payment.
   - If a cart sits behind an email gate, use public sources instead: the brand's own order/landing pages, funnel teardown
     write-ups, YouTube funnel walkthroughs, the Meta and Google ad libraries (for landing URLs), archive.org snapshots.
   - Screenshot every cart at **390 px wide** — the traffic is mostly phones.
3. **For each cart capture:** headline and subhead; what is above the fold; the plan layout and which plan is pre-selected;
   price framing (per day/week, strike-through, savings %); trial wording; where the renewal disclosure sits and how legible
   it is; guarantee; social proof (counts, testimonials, ratings); video (placement, length, autoplay, captions); urgency
   devices; the payment UI (wallets first? embedded or redirect?); what happens after payment (account, upsells).
4. **Classify each device COPY / ADAPT / AVOID.** AVOID includes everything the FTC named: buried or hidden renewal terms,
   pre-selected add-ons, fake or resetting countdown timers, confirmshaming, obstructed cancellation. V Shred's order bumps
   and upsell chains: note them, don't build them (we sell one subscription).
5. **Deliverable:** a private Artifact titled "Cart teardown" — one card per competitor (screenshot + the capture above), a
   comparison table, and the 6–10 patterns we will use with a one-line reason each. Load `/artifact-design` first. Send Dan
   the link with a five-line summary.
6. **Do not wait for his reply to start Phase 2** — build from the strongest patterns and adjust if he redirects. Exception:
   any urgency or discount device waits for his explicit OK.

### Phase 2 — the new cart (`public/index.html`)

1. **New screen `cart`** (`#cartSection`), added to the `renderScreen()` array so the `/vp/cart` virtual pageview fires for
   Google Ads audiences. Back button → wherever the visitor came from.
2. **Baseline layout** (the research refines it):
   - A headline tied to their result ("Your plan is ready") with their goal image thumbnail (`LAST_AFTER_KEY` /
     `state.lastAfterDataUrl`; a locked result shows the blurred teaser with the lock chip, as the analysis page does).
   - **The video slot** directly under the headline (step 4).
   - **Plan picker: Monthly $19.99/mo — PRE-SELECTED — and Annual $69.99/yr** ("$5.83/mo · save 71%"). Change
     `let selectedPlan = 'annual'` to `'monthly'`; Monthly first in the markup and selected on load.
   - **A trial timeline** that follows the selected plan: "Today: $0 · 2 days before it ends: we email you · Day 7: $19.99
     (or $69.99) · cancel anytime before."
   - A short benefit list (three or four lines). Social proof only if it is real — no invented testimonials, no fake counts.
   - **The renewal disclosure directly above the pay button** — keep the substance of `.guarantee-note`: price, trial length,
     automatic renewal, how to cancel, the Terms link.
   - The pay button → Stripe embedded checkout (wallets render at the top automatically when enabled).
   - A secondary "Continue to my hub" link — no dead ends, same rule as today's paywall.
3. **Make it THE checkout for non-members on the web.** `showTrialGate()` for a logged-out visitor goes straight to the cart
   (no signup). Remove `handleMembershipSubscribe()`'s `!isLoggedIn()` early return on the web. On the web,
   `showMembershipScreen()` for a non-member renders the cart; keep the member / manage / beta states and the entire
   native/IAP path exactly as they are. Keep every `returnTo` callback working after payment (`openPendingTrialFeature`,
   the locked-image release in `startTrialAndUnlock`, the 402 feature returns).
4. **Video slot.** Extend `public/site-video.js` (already the single place for site videos, loaded by `index.html` and
   `/start`): `window.ABS_CART_VIDEO = { youtubeId: '', mp4: '', poster: '' };`. Render it with the same pattern as the
   analysis page's `renderAnalysisVideo()`: YouTube → `youtube-nocookie.com` iframe; mp4 → `<video playsinline controls
   preload="metadata">`; empty → **hidden for real users**, a labelled placeholder ("CART VIDEO — coming") on localhost,
   `?vp=1` and `?demo=checkout`. Events `cart_video_play` / `cart_video_progress` (the mp4 path, like the analysis page).
   - When the video exists: a YouTube embed carries a "Watch on YouTube" button — an exit on the page where exits cost the
     most. A self-hosted mp4 on a CDN is better there (the repo bans committed video — see `.gitignore`).
5. **Review link: `/?demo=checkout`** (plus `&locked=1`, `&sex=female`). Mirror the `/?demo=analysis` design in
   `index.html` (`DEMO` const, `anCapture()`): no funnel analytics, no ad pageview, never writes localStorage, and **never
   creates a Stripe session** — the pay button shows a "Demo — checkout disabled" state. Dan must be able to see the cart
   without paying.
6. **Copy** in Dan's voice: second person, direct. Follow `ad-suspension-prevention` — never promise a physical result; the
   goal image is labelled an AI visualization; no before/after framed as real. Every body-fat number keeps the "visual
   estimate … sources" line.

### Phase 3 — pay first on the server (`server.js`)

1. **Anonymous checkout.** A branch of `create-membership-checkout` (or a sibling endpoint) that works without auth
   (`optionalAuth` plus a rate limit):
   - **Logged in** → today's behavior, unchanged.
   - **Anonymous** → no `customer_email`, so Stripe's form collects it. If the visitor gave an email on the analysis page
     (`localStorage.absbyai_email`) you MAY prefill it — first check whether Stripe then renders it read-only, and decide.
   - `metadata`: `kind:'membership'`, `plan`, `anon:'1'`, `deviceId`, `creditDiscountCents`, and **`adClickId` +
     `adClickType`** — `recordAdClickId` needs a user id that does not exist yet, so the gclid has to ride along to the
     webhook or the Google Ads offline feed loses the sale.
   - Grant the 7-day trial (the per-account first-subscription check cannot run without an account). In the webhook, if the
     email matches an account that already had a subscription, log it (`trial_reuse`) rather than block, and flag it to Dan.
   - Credit-conversion coupon: unchanged (keyed on `deviceId`).
2. **`fulfillMembershipSession` for `meta.anon === '1'`:**
   - Email = `session.customer_details.email`, normalised.
   - **No account with that email** → create one (an unusable random password hash, `device_id` from metadata), apply the
     membership fields exactly as today, `recordAdClickId(newId, …)`, and send a **"set your password"** email — a variant of
     `sendResetEmail` with purchase copy ("Your trial is active — set a password to secure your account").
   - **Account already exists** → attach the membership (same UPDATE), `recordAdClickId`, and send a "log in to finish"
     email. **Never log that browser in automatically** — otherwise anyone could pay with someone else's email and walk into
     their account.
   - Keep the existing idempotency, and make create-or-find safe when the webhook and `session-status` race (rely on the
     unique email constraint: insert-or-nothing, then re-select).
3. **Claim — logging in the browser that just paid.** `session-status` (or a new `POST /api/stripe/claim`) returns, only for
   a session whose fulfillment **created** the account, a one-time claim that logs the browser in: single use, ~15-minute
   TTL, bound to that session id, stored hashed, never logged. For a pre-existing account it returns `{existingAccount:true}`
   and nothing that grants access.

### Phase 4 — after payment (client)

1. **`handleMembershipComplete`** for anonymous buyers: claim → `setLoggedIn(data)` → **then** fire the conversions, so
   `fireAdConversion` carries the hashed email: `membership_subscribed`, `fireAdConversion('AqLTCMnl4dkcEJvEqLNE',
   {value:20})`, `fireTikTokEvent('StartTrial')` — exactly once each — then `refreshMembership()`.
2. **Post-payment screen:** "You're in — your 7-day trial is active" + one optional "Create a password" field (the emailed
   link is the backup) → carry the funnel into the account (`saveTransformationIfLoggedIn` for the before/after and the
   analysis; `seedProfileFromFunnel` including the slider height/weight) → **`startQuiz()` as onboarding** ("A few questions
   to build your program") → the `returnTo` callback (`openPendingTrialFeature`, the locked-image release, or the hub).
3. **Existing-account buyers:** "Your membership is active on you@… — log in to continue" → the auth screen with the email
   prefilled.
4. **Locked results:** after the claim the user is a member → `releaseLockedImage()` (the member path skips the device check)
   → `unlockResult()`. A deploy wipes held images (`deploy-drops-locked-holds`), so keep today's "generate it again" fallback.

### Phase 5 — analytics

New events: `cart_viewed {from, locked}`, `cart_plan_selected {plan}`, `cart_checkout_opened {plan}`,
`cart_checkout_completed {plan, anon}`, `account_claimed {created|existing}`, `onboarding_quiz_started` / `_completed`.
Keep `trial_gate_shown`, `membership_subscribed`, the Google Ads + TikTok trial conversions and the paid conversion. Say in
the commit message that `account_signup` no longer sits between the trial button and payment for web buyers, so PostHog
funnels must be rebuilt.

### Phase 6 — verify, deploy, close

1. **Local** (memory `local-funnel-test-recipe`): the cart at 390 px; Monthly selected on load; both plans; locked,
   unlocked and female variants; `/?demo=checkout`; the video placeholder; every entry point landing on the cart for a
   logged-out web visitor; and with `IS_NATIVE_APP` forced, the IAP screen and account-first flow unchanged.
2. **Server logic without a card** — fixture tests of `fulfillMembershipSession` against pg-mem: (a) a new email creates the
   account, applies the membership, queues the set-password email and records the gclid; (b) an existing email attaches the
   membership and issues no claim; (c) a duplicate webhook racing `session-status` yields one account and one fulfillment.
3. **The live card test is Dan's step.** Claude never enters card numbers (test or real), and there are no test keys. Give
   him a short script: a private window on absbyai.com → generate or use the analysis page → cart → Monthly → pay ($0 today)
   → confirm he is logged in and the set-password email arrived → Manage membership → cancel before day 7 (no charge). Then
   check Stripe, Postgres and PostHog yourself.
4. Commit and push (verify it landed with `git fetch && git branch -r --contains <sha>` — memory `github-push-false-failure`),
   confirm Railway `SUCCESS`, live-verify on absbyai.com.
5. **Native retest trigger — say it explicitly:** the native apps load the same page; Dan confirms they still show the IAP
   screen and the account-first flow.
6. Remove this doc from the HANDOFFS list in `AI_COORDINATION.md` and from `Handoffs/README.md`; record the OPEN decisions.

## OPEN — ship the default, ask Dan in the delivery message

- **Cart video before the file exists:** hidden for real users (default) or a visible placeholder.
- **Anonymous trial reuse:** allowed and logged (default) or blocked (blocking needs the email before checkout).
- **Email before checkout:** default no — Stripe collects it. If the research shows the top carts all ask for email first
  and Dan wants abandoned-checkout emails, a single email field can go on the cart, but it re-introduces a step.
- **Google Pay:** recommend on; needs Dan's go-ahead (a Stripe account setting).
- **Urgency or discount devices** found in the research: only with Dan's explicit OK.

## Things to Avoid / Lessons Learned

- **Never break the tracking the ads are judged on:** the trial-start conversion (`AqLTCMnl4dkcEJvEqLNE` + TikTok
  `StartTrial`), the enhanced-conversion email, the gclid on the account (offline feed), and the paid conversion.
- **Never auto-login an email that already has an account.**
- **Never leave a paying buyer without a way in** — the set-password email and "forgot password" must both work for created
  accounts.
- **Don't touch IAP or native code**, and don't apply web purchase changes to the apps (the Apple 3.1.1 history).
- **Don't copy MadMuscles' dark patterns.** The renewal disclosure stays above the button.
- **Don't promise what the system doesn't do.** The 2-days-before reminder is real; "cancel with two taps" must stay true
  (Manage membership → the Stripe portal).
- **Live Stripe only** — the card step is Dan's.
- **Every push redeploys and wipes held locked images and the analysis cache** — batch doc edits into code commits and
  deploy in a quiet minute.
- **`git push` can print "fatal error in commit_refs" while succeeding** — verify before retrying.
- **The repo is public** — competitor screenshots and personal images never go in git; the teardown lives in an Artifact.
- The Browser pane's `window.fetch` override does not intercept the app's own calls; test failure paths with the
  dummy-key server.

## Relevant Files & Locations

- `public/index.html` — `#analysisSection`, `primaryCta`, `showTrialGate` (~6459), `continueTrialAfterAccountCreation`
  (~6227), `startQuiz` / `finishQuiz` (~6426), `proceedToTrialGate` (~6454), `#membershipSection` (~2796),
  `selectedPlan` (~7835), `handleMembershipSubscribe` (~8015), `handleMembershipComplete` (~8050), `fireAdConversion`
  (~3535), `reportPaidMembershipConversion` (~7880), `startTrialAndUnlock` (~3817), `renderAnalysisVideo` (~5030),
  the `DEMO` const / `anCapture()` / `startAnalysisDemo()` (the pattern for `/?demo=checkout`), `IS_NATIVE_APP`.
- `public/site-video.js` — the single place for site video config (add `ABS_CART_VIDEO`).
- `server.js` — `create-membership-checkout` (~6321), the webhook (~43), `fulfillMembershipSession` (~6524),
  `session-status` (~10116), `MEMBERSHIP_PLANS`, `recordAdClickId`, `sendResetEmail` (~4693), `request-reset` (~5023),
  `reset-password` (~5043), `trialReminderSweep` (~6956).
- `Handoffs/handoff-20260812-purchase-before-account.md` — the separate iOS version (do not execute here).
- Env var names (values in `~/.absbyai-secrets.env`, never in git): `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`,
  `STRIPE_WEBHOOK_SECRET`, `POSTHOG_PERSONAL_KEY`, `POSTHOG_PROJECT_ID`, `DATABASE_PUBLIC_URL`, `RESEND_API_KEY`.
- Stripe dashboard → Settings → Payment methods (Google Pay toggle).
- Review links today: `absbyai.com/?demo=analysis` (+ `&locked=1`, `&sex=female`).

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Fable 5.1, high effort** — Dan's standing choice for Abs By AI (memory `astra-vs-fable-verdict`), included in Max. |
| **If Claude usage is high / approaching a limit** | **Claude Sonnet 5, high effort** for the research and the cart UI; keep Phase 3 (account creation, the claim login, the webhook) on **Fable 5.1 or Claude Opus 5**. |

Always-Claude override: this is the money path, account security and brand copy — not a Codex task at any usage level.

## Starter Prompt for the Next Task

> Execute `Handoffs/handoff-20260910-web-pay-first-cart.md` in the Abs By AI repo. On the WEB only (the native apps stay
> exactly as they are), rebuild the membership checkout into a research-led cart that comes right after the analysis page
> and BEFORE any account. (1) Research high-converting direct-response fitness carts — MadMuscles and V Shred plus a few
> others — walking funnels in the Browser pane but stopping at any email or payment field. (2) Publish a private "Cart
> teardown" artifact that shows Dan the best carts and the patterns you will copy, adapt or avoid, send it to him, then
> build without waiting. (3) Put a short-video slot in the cart as a placeholder (`window.ABS_CART_VIDEO` in
> `public/site-video.js`; hidden for real users until a file exists, visible on `?vp=1` and `?demo=checkout`). (4) Offer
> Monthly $19.99, pre-selected as the default, and Annual $69.99. Stripe collects the email with the card; the account is
> created from it after payment, with a one-time claim login and a set-password email; an email that already has an
> account gets the membership attached but is never logged in automatically; the five questions move to after payment as
> onboarding. Keep every conversion firing (trial-start Google Ads + TikTok with the hashed email, the gclid on the
> account). Start with the doc's Current State and Key Decisions. Verify locally with fixture tests; the live card test is
> Dan's step. Commit, push, confirm the Railway deploy, live-verify, flag the native retest, and close the coordination
> entry.

**Recommended:** Fable 5.1, high effort. **Budget:** ~$0 in AI generation (the research is browsing; no image or video
generation needed).
