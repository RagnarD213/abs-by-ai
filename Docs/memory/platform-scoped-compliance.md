---
name: platform-scoped-compliance
description: "App Store/Play compliance changes default to that platform ONLY — never all three — and going cross-platform needs Dan's OK first"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7443cbb4-cf21-4500-9c33-ea67cb690ff6
  modified: 2026-08-07T23:37:19.335Z
---

Any change made to satisfy an Apple App Store or Google Play requirement is scoped to **that platform only, by default**. Gate it on `IS_NATIVE_APP` (or an iOS/Android-specific check) so the web is untouched. Before applying a compliance change to every platform, **ask Dan first** — do not decide it yourself.

**Why:** all three platforms load the same live absbyai.com (`server.url` in the Capacitor config, and the Android TWA wraps the same URL), so "ship it once" silently pushes an app-store-mandated screen onto the web too. On 2026-08-07 that put an Apple-required AI-consent modal in front of every first-time web visitor — a blocking gate on the acquisition funnel that was never discussed. Dan found it live and objected. Compliance surface is not the same as product surface: Apple's rule is about Apple's app, and the web funnel pays a real conversion cost for obeying it.

**How to apply:** when writing the change, ask "does the web need this, or only the store build?" Default to the store build. Say explicitly in the response which platforms the change is visible on — Dan's standing assumption is that silence means it went everywhere. If the web genuinely should carry it too (a legal requirement rather than a store policy, say), state the reasoning and get his answer before shipping. Keep a lighter web-appropriate equivalent where one makes sense — the consent modal's fix kept a one-line disclosure under the Generate button plus the privacy policy on web, while the full modal stayed native-only.

Related: [[cross-platform-retest-rule]] — the mirror-image obligation, that a web deploy silently changes both native apps and must be flagged for retest. [[ios-appstore-prep]], [[native-app-iap-gating]].
