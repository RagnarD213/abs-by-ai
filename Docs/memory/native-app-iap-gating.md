---
name: native-app-iap-gating
description: How digital purchases (credits + membership) are hidden inside the iOS/Android apps for App Store / Play compliance
metadata: 
  node_type: memory
  type: project
  originSessionId: d54ec65c-6b95-4405-b8e7-cdf1a4200824
---

Shipped 2026-07-14 (Phase 0 of the app-store push): inside the native apps we hide
all DIGITAL purchase UI, because Apple/Google require their own in-app billing for
digital goods. Physical print checkout (Printify, Stripe) is untouched and stays.

- Detection in `index.html`: `const IS_NATIVE_APP` = `window.Capacitor.isNativePlatform()`
  (iOS Capacitor) OR an `android-app://com.absbyai.app` referrer captured once in
  `sessionStorage['absbyai_twa']` (Android TWA — the referrer clears on later in-app
  navigations, so it's captured on launch). Sets `document.documentElement` class `native-app`.
- Hiding: CSS `.native-app .app-hide-purchase { display:none !important }` on the credit
  pack cards, the "go unlimited" line, membership plan-cards/subscribe btn/guarantee/
  credit-convert note, the credits-alt block, and the hub "Manage membership" button.
  Neutral `.app-only-note` elements ("not available for purchase in the app") show instead.
  `#membershipAppNote` is JS-toggled in `showMembershipScreen` for non-comp native users.
- Defense-in-depth: `handleCreditsCheckout`, `handleMembershipSubscribe`,
  `handleManageMembership` early-return when `IS_NATIVE_APP`.
- Web/PWA behavior is unchanged (IS_NATIVE_APP is false in a browser) — verified.
- **App Store review note:** this is what makes the Stripe/physical-goods claim in
  [[ios-capacitor-app]]'s `HANDOFF_iOS_APP_STORE.md` true again now that credits/membership
  ([[pay-for-generations]], [[ai-trainer-membership]]) sell digital goods on the web.
- The TWA loads the LIVE site, so gating reaches the apps on Railway deploy of index.html,
  NOT via a new AAB build. See [[android-twa-build-setup]] / [[railway-deploy-workflow]].
