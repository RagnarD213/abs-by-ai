---
name: app-store-policy-verify-first
description: "Before advising on Google Play / App Store account setup or publishing requirements, verify current platform policy via docs/browser first — don't answer from general knowledge"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 23964aac-ebc8-4ca5-bb8a-10ea9be6234d
  modified: 2026-07-21T20:40:47.056Z
---

Before giving guidance on Google Play Console or Apple App Store account setup, account types, category restrictions, or publishing requirements, actively look up the current official policy (support.google.com / developer.apple.com, via browser) BEFORE answering — don't rely on general/remembered knowledge, even when the answer seems obviously fine.

**Why:** During the Abs by AI Android launch (2026-07-21), advised Dan that a Personal Play Console account would be fine since the app doesn't sell anything through Play Billing. This was wrong — Google restricts Health & Fitness category apps to Organization accounts regardless of billing model, and Personal accounts also face a 12-tester/14-day closed-testing gate before public release that Organization accounts skip. The correct answer only surfaced when a doc lookup was actually run, and only because Dan asked a follow-up question — the mistake would have cost him a redone signup (website verification, D-U-N-S number, organization payments profile) if he'd already gone further down the Personal path. Dan explicitly said this wasn't a model-capability gap — no LLM reasons its way to a platform's current policy without checking it; it's a thoroughness gap in when the check happens.

**How to apply:** Any time app-store publishing, account types, category eligibility, review requirements, or distribution rules come up (Android or iOS), do the docs-check pass proactively, before the user starts clicking through signup flows — not reactively after something breaks or they ask a pointed follow-up. Applies to [[android-twa-build-setup]] and the iOS Capacitor app work alike.
