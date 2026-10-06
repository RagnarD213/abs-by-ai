---
name: cross-platform-retest-rule
description: "Web deploys hit iOS/Android automatically, but some changes need native retesting — and Dan requires an explicit reminder or he assumes none is needed."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 894b25b0-4b6c-42ad-a79e-7668c9e048ba
  modified: 2026-07-27T22:04:41.667Z
---

Abs By AI's iOS (Capacitor, `server.url = https://absbyai.com`) and Android (TWA) apps are thin shells around the live website, so a push to `main` + Railway deploy updates all three platforms at once — no App Store/Play resubmission for web or server changes.

**Dan's instruction (2026-07-27):** when a change could break inside the native apps even though it works on the web, **tell him explicitly in the response** — name the platform and what to check. **If he doesn't hear the reminder, he assumes no native retest is needed.** Silence is read as "web-only verification is enough."

**Why:** he is non-technical and doesn't track which change types are native-risky; the burden of noticing is on the assistant, not on him.

**Preferred discharge:** don't hand Dan a to-do — run `scripts/native-smoke-test.sh` (added + baselined 2026-07-27) and show him the result. It boots an iPhone simulator + Pixel emulator against production, screenshots both, and asserts purchase gating on Android over the Chrome DevTools protocol. Makes zero AI calls on purpose (the apps hit prod; generations cost real money). Build iOS **Release** — Xcode 26 Debug builds won't launch from `simctl`.

**How to apply:** verify absbyai.com at 375×812 + desktop on every change. Then flag a native retest whenever the change touches: form inputs (`time`/`date`/`number`/file pickers — the iOS WebKit overflow bug, commit `d76c590`); photo upload/camera; share or save-to-Photos; **any price, buy button, credit pack, plan card, or "Manage membership" (mandatory, both stores — see [[native-app-iap-gating]])**; layout at screen top/bottom (safe areas); login/session/account deletion; navigation or back-button behaviour (Android especially). Native-only assets (icon, splash, permission strings, bundle id) never update from a web deploy and need a rebuild — see [[ios-capacitor-app]] and [[android-twa-build-setup]]. Stale WebView cache is the usual cause of "old behaviour" on the phone right after a deploy, not a bad deploy — see [[railway-deploy-workflow]]. Full table lives in the "Standing rule — cross-platform testing" section of `AI_COORDINATION.md`.
