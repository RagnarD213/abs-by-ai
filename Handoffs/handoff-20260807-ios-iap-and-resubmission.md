# Handoff: iOS In-App Purchase subscription + full resubmission after second Apple rejection

**Date:** 2026-08-07
**Project:** Abs By AI
**Business goal this serves:** Profitability + app adoption — the iOS app cannot launch (or monetize) until Apple approves it, and Apple has now demanded IAP in writing.

## Objective

Get the iOS app approved. That means: (1) build the Abs by AI membership as an Apple **auto-renewable In-App Purchase subscription** in the iOS app, wired to real membership provisioning on our server; (2) complete the already-drafted App Review reply for the privacy issues; (3) run the pre-resubmission verification checklist; (4) resubmit a new binary. The privacy fixes for the other two rejection issues are ALREADY SHIPPED AND LIVE — do not redo them.

## Current State

Apple rejected `1.0 (1)` a second time on **2026-08-07** (submission `c4dc7f48-72d6-4ecd-b809-65be264fce85`, reviewed on iPad Air 11-inch M3) under three guidelines:

1. **5.1.1(i)/5.1.2(i)** (data sent to third-party AI without in-app disclosure/consent) — **FIXED, SHIPPED, LIVE-VERIFIED** (commit `f07b2f5`). A one-time consent modal (`#aiConsentOverlay` / `ensureAiConsent()` in `public/index.html`) now names exactly what data goes to which AI provider and blocks all seven AI entry points until the user agrees (photo pick, trainer, nutritionist, macro analyze, sleep check-in, supplement label scan, audit start). Persistent disclosure line under the Generate button. Consent stored in localStorage + cookie (`absbyai_ai_consent`), PostHog events `ai_consent_granted`/`ai_consent_declined`.
2. **2.1 face data questions** — **ANSWERED**. `public/privacy.html` now has a dedicated quotable "Face data" section + "Fitness details you enter" section (live at absbyai.com/privacy, dated Aug 7 2026). The six answers Apple demands are drafted verbatim in `app-store-assets/APP_REVIEW_REPLY_20260807.md`.
3. **3.1.1 payments** — **NOT FIXED; this handoff's main job.** Apple rejected the external-purchase-link approach: *"Once the user's free trial has expired, the subscription is not available for purchase using In-App Purchase."* Dan has decided (2026-08-07): **build the IAP subscription.**

The web product is one page (`public/index.html`) served by `server.js` on Railway; the iOS app (`ios-app/`, Capacitor) is a thin wrapper with `server.url = https://absbyai.com` — the Capacitor JS bridge IS injected into the remotely loaded site, so `window.Capacitor` is available to the live page inside the app. Purchase UI inside the apps is currently hidden via `.app-hide-purchase` with external link-outs (`openExternalPurchase`, added for rejection 1). Web membership: Stripe, $19.99/mo or $69.99/yr, 7-day free trial, `MEMBERSHIP_PLANS` in `server.js`, status on the `users` table (`membership_status`).

## Key Decisions Already Made

- **Build IAP** (Dan, 2026-08-07) — hiding purchase UI failed rejection 1; US external link-out failed rejection 2; Apple demanded IAP twice in writing. Do not relitigate.
- **Keep the web Stripe path byte-untouched** — web visitors keep the existing checkout. IAP is additive, native-only.
- **Keep the external link-out alongside IAP** (allowed on the US storefront) unless it complicates the build — IAP availability is what Apple demands, not link removal.
- **Same prices as web**: $19.99/mo, $69.99/yr, 7-day free trial as an introductory offer. Parity not required by Apple but keeps messaging honest.
- **US-only availability stays** (set 2026-08-05).
- The two shipped privacy fixes and the reply draft are settled — don't rewrite them, just paste and reference.

## Detailed Plan

### Phase 0 — Dan's personal prerequisites (~20 min, blocks everything)
1. App Store Connect → Business (Agreements) → sign the **Paid Applications agreement** and complete **banking + tax** forms. IAP products cannot be created until this is Active.
2. Enroll in the **App Store Small Business Program** (developer.apple.com → membership) to get 15% instead of 30% commission. Parallel, non-blocking.

### Phase 1 — App Store Connect products
3. Create a subscription group (e.g. "Abs by AI Membership") with two auto-renewable subscriptions:
   - `com.absbyai.app.membership.monthly` — $19.99/mo, **7-day free introductory offer**
   - `com.absbyai.app.membership.yearly` — $69.99/yr
   Each needs a display name, description, and a **review screenshot** (capture the in-app purchase screen once built; a simulator screenshot is fine).
4. Auto-renewable subs REQUIRE functional **Terms of Use (EULA)** and **Privacy Policy** links in the app AND in the App Store metadata. Put `https://absbyai.com/terms` in the EULA/Terms field of the listing and confirm both links render on the in-app purchase screen.

### Phase 2 — Native purchase plumbing (recommended: RevenueCat)
5. **OPEN (implementer's call): RevenueCat vs. raw StoreKit 2 plugin.** Recommendation: **RevenueCat Capacitor SDK** (`@revenuecat/purchases-capacitor`) — free below ~$2.5k/mo tracked revenue, handles receipt validation, entitlements, restore, sandbox weirdness, and gives server webhooks, cutting days of custom StoreKit + App Store Server API work. If choosing raw StoreKit instead, budget for App Store Server Notifications V2 handling and JWS verification on our server.
6. Add the SDK to `ios-app/`, configure with the RevenueCat public API key, and set `appUserID` to our account's user id/email **after login** (the site knows auth state; call the plugin from the page via `window.Capacitor.Plugins.Purchases`). Rebuild the wrapper.
7. In `public/index.html`, on the membership screen inside the native app (`.native-app`), replace the hidden-Stripe/link-out treatment with real IAP UI: plan cards (monthly w/ "7-day free trial" + yearly), a **Restore Purchases** button (Apple requires it), and Terms/Privacy links. Purchase via the plugin; on success, sync to server then `refreshMembership()`. Guard everything so the web experience is unchanged (`window.Capacitor?.isNativePlatform?.()`).

### Phase 3 — Server-side provisioning (`server.js`)
8. New endpoint(s) to grant/revoke membership from Apple purchases:
   - RevenueCat route: `POST /api/revenuecat/webhook` (verify the webhook auth header) mapping `INITIAL_PURCHASE`/`RENEWAL`/`CANCELLATION`/`EXPIRATION` events → `users.membership_status`, keyed by `app_user_id`.
   - Plus a client-driven `POST /api/apple/sync` fallback that trusts only a server-side RevenueCat REST lookup (never the client's word) — covers webhook latency so the user is unlocked immediately after buying.
9. Membership from Apple must coexist with Stripe: add a `membership_source` (or reuse existing plan/status fields) so Stripe cancel logic never touches Apple subs and account deletion doesn't call Stripe for an Apple-billed member. Check `isActiveMembership()` and the delete-account Stripe-cancel gate.
10. "Manage membership" for Apple-billed members must point to Apple's subscription management (`https://apps.apple.com/account/subscriptions`), not the Stripe portal.

### Phase 4 — Verify (sandbox)
11. Sandbox tester account in ASC → run the full loop on the iOS simulator/TestFlight: buy monthly with trial → server grants membership → features unlock → Restore Purchases works → cancellation in sandbox eventually expires the membership. Verify the web Stripe flow is untouched and Android still shows its current treatment.
12. **Native retest of the consent modal** (flagged 2026-08-07, standing rule): confirm `#aiConsentOverlay` renders correctly inside the iOS app (safe areas, buttons reachable) on first photo pick.

### Phase 5 — New binary + resubmission
13. Bump the build (`1.0 (2)`), archive **Release** (never Debug — known simulator/launch trap), upload, attach to the submission.
14. Finish `app-store-assets/APP_REVIEW_REPLY_20260807.md`: fill the 3.1.1 paragraph with option (a) ("membership is now available as an auto-renewable In-App Purchase subscription in build 1.0 (2)…"), then paste the whole reply into "Reply to App Review" and mirror the face-data answers into App Review Information notes.
15. Update the review notes' demo-account caveat: the comp demo account never shows purchase UI — tell the reviewer a fresh free account (or signed-out use) shows the IAP flow after the free generations run out, and after account creation.
16. Resubmit. Record everything in `AI_COORDINATION.md` and check off the dashboard Key task (`money::Execute handoff: iOS IAP subscription + resubmission` — added 2026-08-07 per Rule 8).

## Things to Avoid / Lessons Learned

- **Do NOT resubmit before IAP is in the build.** Two rejections have proven both non-IAP approaches dead: hiding purchase UI (rejection 1) and US link-out without IAP (rejection 2).
- **Debug builds won't launch on new simulators** (Xcode 26 `App.debug.dylib` / SBMainWorkspace refusal) — always archive/install Release.
- The consent modal gate in `handlePhoto` must stay **before** `finalizePhoto` — `finalizePhoto` fires `/api/check-photo`, which sends the photo to Anthropic at photo-pick time.
- The comp/demo account (`danroseconsulting+applereview@gmail.com`) hides all purchase UI — reviewers must use a fresh account to see IAP; say so in the notes.
- `welcome_images` stores email-capture users' before/after pairs — the privacy policy now discloses this; don't "simplify" that disclosure away.
- Never key server-side grants on client-supplied identifiers alone (same class as the F1/unlock-token lessons) — verify purchases server-side via webhook or REST lookup.
- Web deploys update the app instantly, but **this task needs a native rebuild** — the IAP plugin is binary-side.

## Relevant Files & Locations

- `public/index.html` — membership screen, `.app-hide-purchase` gating, `openExternalPurchase`, consent modal, `refreshMembership()`
- `server.js` — `MEMBERSHIP_PLANS`, `isActiveMembership()` (~4286), Stripe webhook, delete-account Stripe cancel gate
- `ios-app/` — Capacitor wrapper (`capacitor.config.json` has `server.url`)
- `app-store-assets/APP_REVIEW_REPLY_20260807.md` — drafted reply (3.1.1 paragraph pending)
- `AI_COORDINATION.md` — "iOS SECOND rejection (2026-08-07)" entry has the full rejection text summary
- App Store Connect app id `6794097836`, submission `c4dc7f48-72d6-4ecd-b809-65be264fce85`
- absbyai.com/privacy — live face-data + AI sections

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Opus, extended thinking** — payment provisioning + native/StoreKit + server auth interplay is exactly the "expensive to unwind if wrong" class |
| **If Claude usage is high / approaching a limit** | Still Claude (Opus if possible, Sonnet 5 with careful review otherwise) for Phases 3–4 (server payment logic); Codex flagship high-effort is acceptable for the mechanical native-plugin wiring in Phase 2 |

Dan has already asked for **Opus** to run this handoff. Payment-granting code should not go to a low-effort model regardless of usage.

## Starter Prompt for the Next Task

> Read `Handoffs/handoff-20260807-ios-iap-and-resubmission.md` and `AI_COORDINATION.md` (the "iOS SECOND rejection (2026-08-07)" entry) in the Abs By AI project. Apple rejected the iOS app a second time; the two privacy issues are already fixed and live — your job is Phase 0–5 of the handoff: build the membership as an Apple auto-renewable In-App Purchase subscription (RevenueCat Capacitor SDK recommended), wire server-side provisioning, verify in sandbox, produce build 1.0 (2), finish the drafted App Review reply's 3.1.1 paragraph, and resubmit. Start by walking Dan through Phase 0 (Paid Applications agreement + banking/tax in App Store Connect — his hands, ~20 min), and while waiting, create the subscription products plan and scaffold the RevenueCat integration.
