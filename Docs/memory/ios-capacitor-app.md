---
name: ios-capacitor-app
description: "iOS app setup for Abs by AI — Capacitor 8 wrapper in ios-app/, status and remaining steps"
metadata: 
  node_type: memory
  type: project
  originSessionId: a5c9d91c-1ab0-42b5-a6c6-75777965b1b6
---

iOS app (started 2026-06-12): Capacitor 8 + SPM wrapper around https://absbyai.com in `ios-app/`,
app ID `com.absbyai.app` (matches Android TWA in [[android-twa-build-setup]]).

- Native integration script at the bottom of `index.html` (gated on `window.Capacitor`):
  safe areas, status bar, haptics, native share/save. Must be deployed to absbyai.com to take effect in the app.
- Plugins: App, Filesystem, Haptics, Keyboard, Share, SplashScreen, StatusBar. Icons/splash generated
  by `ios-app/scripts/gen-assets.swift` from `img/icon-512.png`.
- Goal: App Store publication. User chose: enroll in Apple Developer Program (Individual, $99/yr) — not yet done.
- Payments: only physical Printify goods sold → Stripe is App Store-compliant; paid digital goods would require IAP.
- Full phased plan (supersedes `HANDOFF_iOS_APP_STORE.md`) is in `HANDOFF_iOS_APP_PLAN.md`
  (created 2026-07-14). Decisions locked 2026-07-14: ship the existing wrapper (no native
  rebuild), Individual Apple Developer enrollment, digital purchases stay hidden in-app
  ([[native-app-iap-gating]]) — app sells only physical prints via Stripe.
- Blocker still true as of 2026-07-14: Mac on macOS 15.5, no Xcode (`xcode-select` points at
  CommandLineTools). App Store needs Xcode 26 → needs macOS 26 Tahoe. Dan to upgrade macOS +
  install Xcode from the Mac App Store (signed in as Daniel Rose), then Claude runs:
  `sudo xcode-select -s /Applications/Xcode.app`, accept license, `xcodebuild -downloadPlatform iOS`,
  then build/test:
  `cd ios-app && npx cap sync ios && xcodebuild -project ios/App/App.xcodeproj -scheme App -destination 'platform=iOS Simulator,name=iPhone 17' build`
- Simulator walkthrough must re-verify features shipped after June (Trainer, Nutritionist,
  Sleep Coach, Counsel, Progress Log, Coach Brief, Transformations) plus the purchase gating.

**2026-10-01, PROJECT FILE LOST:** iCloud's Documents sync made 672 duplicate `App N.xcodeproj` folders in
`ios-app/ios/App/` and the real `App.xcodeproj` lost `project.pbxproj`; `capacitor.config.json` is gone too (only numbered
copies). No Time Machine, no other copy found. The project must be regenerated outside iCloud-synced `~/Documents` before
any new App Store build (signing, IAP capability and plugin setup were in the lost file). Until then the smoke test falls
back to the last good simulator build (2026-07-29, `native-smoke-out/ios-dd/.../App.app`): fine for checking the live
website inside the shell, blind to native changes since July. `xcrun simctl io ... screenshot` cannot write into
`~/Documents` (capture to a temp file, copy in).

**2026-10-07, REBUILT:** The current iPhone source project is in the outside-iCloud worktree at
`/Users/danielrose/.codex/worktrees/ios-rebuild/Abs By AI/ios-app` and is tracked on GitHub `main`
from commit `8e5a9e3`. Capacitor 8 was regenerated with app ID `com.absbyai.app`, the September 20
compiled app's settings were restored, and RevenueCat Purchases was included from the last submitted
build notes. A Release simulator build and `scripts/native-smoke-test.sh ios` passed. The original
`ios-app/` folder in the iCloud-synced main checkout is still damaged and was not touched. The full
iCloud Data Recovery list was not searched because Chrome crashed after loading 7,168 entries.
