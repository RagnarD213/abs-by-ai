# Handoff: rebuild the lost iPhone app project

Written 2026-10-01 by Claude (Opus 5.5). Not executed. Recommended: **Codex GPT-6 Sol, high effort** (ops work, mostly
command line; routing memory `model-routing-plan`).

## Goal

A complete, buildable iPhone project for `com.absbyai.app` again, stored where iCloud cannot touch it and protected by
git, that produces a Release simulator build and passes `scripts/native-smoke-test.sh ios` with a real build.

**This is a rebuild only. Do not upload, submit or reply to Apple.** The iOS app was rejected on 2026-09-17 (4.3(b) and
1.1) and the board says no resubmit until Dan rules.

## What happened

The project folder sits inside iCloud's Documents sync. Between about 2026-09-17 and 2026-09-25 iCloud made 672 numbered
copies of the Xcode project folder and the real one lost its contents. Nothing is in Time Machine (none is set up), in
git (`ios-app/` was never tracked) or in Spotlight.

## Inventory, measured 2026-10-01

**Lost** (not on disk under any name):
- `ios-app/ios/App/App.xcodeproj/project.pbxproj` (all 673 `App*.xcodeproj` folders hold only `project.xcworkspace` and `xcuserdata`)
- `ios-app/ios/App/App/AppDelegate.swift`, `Info.plist`, the entitlements file, `Base.lproj` storyboards
- `ios-app/ios/App/CapApp-SPM/Package.swift`
- `ios-app/capacitor.config.json` (only numbered copies `capacitor.config 2.json` to `8.json` remain)
- `ios-app/scripts/gen-assets.swift` (the icon and splash generator)

**Survives:**
- `ios-app/package.json`: Capacitor 8.4 (`@capacitor/core`, `cli`, `ios`), plugins `app`, `filesystem`, `haptics`,
  `keyboard`, `share`, `splash-screen`, `status-bar`, and `@revenuecat/purchases-capacitor` ^13.4.0. `node_modules/` is present.
- `ios-app/ios/App/App/Assets.xcassets`, `capacitor.config.json`, `config.xml` (1,151 copies), `public/`
- Two compiled simulator builds, the best record of the real settings:
  - `ios-app/build/Build/Products/Debug-iphonesimulator/App.app` (2026-09-20): version 1.0, build 1, bundle id
    `com.absbyai.app`, with `Info.plist`, `Base.lproj`, `Assets.car` and the synced `capacitor.config.json`
  - `native-smoke-out/ios-dd/Build/Products/Release-iphonesimulator/App.app` (2026-07-29): what the smoke test uses today
- `~/Library/Developer/Xcode/DerivedData/App-cyylhssfkrhqrgcrfiidyrsjxgpl` (build records, no sources)
- The written record: memory `ios-capacitor-app`, `ios-appstore-prep`, `native-app-iap-gating`; `Handoffs/HANDOFF_ios_iap.md`,
  `handoff-20260807-ios-iap-build-and-resubmit.md`, `handoff-20260812-ios-iap-purchase-audit.md`,
  `handoff-20260812-ios-second-rejection-resolution.md`. Session logs that touched the lost files: 3 under
  `~/.codex/sessions` and 11 under `~/.claude/projects/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/` mention
  `project.pbxproj` (`grep -l`); they may hold the exact edits to replay.

**Good news:** there is no custom native code. The config's plugin list is `AppPlugin` (Capacitor's own App plugin),
`FilesystemPlugin`, `HapticsPlugin`, `KeyboardPlugin`, `SharePlugin`, `SplashScreenPlugin`, `StatusBarPlugin`. The app is
a standard Capacitor shell around `https://absbyai.com`, so it can be regenerated, not rewritten.

**One thing to resolve:** `package.json` lists RevenueCat, but the 2026-09-20 build's plugin list has no purchases
plugin. Work out from the IAP handoffs and the App Store build history (1.0 (3) was reviewed on 2026-08-26) whether the
submitted builds had it, and make the rebuilt project match what was last submitted.

## Steps

### 0. Try to get the originals back first (time limit: about 2026-10-17)

iCloud keeps deleted files for 30 days. Dan signs in at iCloud.com (an agent cannot type his password), then:
iCloud Drive, **Recently Deleted**; and the account menu, **Data Recovery**, **Restore Files**. Look for
`project.pbxproj`, `AppDelegate.swift`, `Info.plist`, `Package.swift`, `capacitor.config.json` and `gen-assets.swift`
from `Documents/Claude/Projects/Abs By AI/ios-app`. Also Finder, iCloud Drive, Recently Deleted on the Mac (on
2026-10-01 the local `~/Library/Mobile Documents/.Trash` held nothing relevant). If they come back, restore them into a
copy of the folder, skip to step 3, and note which files were recovered.

### 1. Work outside iCloud

Best: run `handoff-20261001-move-project-out-of-icloud.md` first, then work in `ios-app/` in place. If Dan wants the
iPhone project sooner, build in `~/abs-native/ios-app` and replace `ios-app` in the project with a symlink to it.
Rename the damaged folder to `ios-app-damaged-20261001` first; delete nothing in this handoff.

### 2. Regenerate

1. New folder with `package.json` and `package-lock.json` from the old one. `npm ci`.
2. `capacitor.config.json`: take it from the 2026-09-20 build (the last config that was actually synced), minus the
   generated `packageClassList`. Diff it against the newest numbered copy and keep any newer intentional setting. It must
   contain `appId com.absbyai.app`, `appName "Abs by AI"`, `webDir www`, `server.url https://absbyai.com` with
   `allowNavigation` for `absbyai.com` and `www.absbyai.com`, the `ios` block (`contentInset never`, `backgroundColor
   #f6f5f2`, `preferredContentMode mobile`), `SplashScreen` (1200 ms, auto hide, same colour, no spinner) and
   `Keyboard.resize native`.
3. A minimal `www/index.html`, then `npx cap add ios` and `npx cap sync ios`.

### 3. Put the settings back

Compare the new build's `Info.plist` with the 2026-09-20 build's, key by key (`plutil -convert json -o - Info.plist`),
and restore every difference that is not generated. The values read from that build on 2026-10-01, in case the build
folder is gone by the time this runs:

| key | value |
|---|---|
| `CFBundleDisplayName` | `Abs by AI` |
| version / build | 1.0 / 1 in this Debug build; use the next build number after the highest in App Store Connect |
| `MinimumOSVersion` | 15.0 |
| `UIDeviceFamily` | 1 and 2 (iPhone and iPad) |
| `UISupportedInterfaceOrientations` | Portrait only on iPhone; all four on iPad |
| `ITSAppUsesNonExemptEncryption` | false |
| `NSCameraUsageDescription` | Abs by AI uses the camera so you can take a photo for your fitness transformation. |
| `NSPhotoLibraryUsageDescription` | Abs by AI lets you choose a photo from your library for your fitness transformation. |
| `NSPhotoLibraryAddUsageDescription` | Abs by AI saves your finished transformation image to your photo library. |
| storyboards | `Main`, `LaunchScreen` |

Then:

- Copy the surviving `Assets.xcassets` in (app icon, splash). If it is incomplete, regenerate from
  `public/img/icon-512.png`; the old generator script is lost.
- Capabilities and entitlements: read them off the old builds (`codesign -d --entitlements :- <App.app>`) and the IAP
  handoffs. In-App Purchase if RevenueCat was in the submitted build.
- Signing team: needed only for a device or App Store build. Record it in the project if Xcode is signed in; a simulator
  build needs none.
- Privacy manifest: neither old build contains an app-level `PrivacyInfo.xcprivacy`, so there is none to restore.
- The 2026-09-20 build's `Frameworks/` holds only `Capacitor.framework` and `Cordova.framework`, which supports the
  RevenueCat question above: confirm before adding the purchases plugin back.

### 4. Verify

- `xcodebuild -project App.xcodeproj -scheme App -configuration Release -sdk iphonesimulator ... build` succeeds.
- `scripts/native-smoke-test.sh ios` prints "iOS Release build succeeded" (not the WARN fallback line) and the screenshot
  shows the app's home screen with the live site.
- The new build's plugin list and `Info.plist` match the old build, with every remaining difference listed and explained.
- In the simulator: the app loads, safe areas look right at the top and bottom, the membership screen shows no web
  purchase buttons (memory `native-app-iap-gating`).

### 5. Make sure it can never be lost again

Put the iPhone project under git: track `ios-app/` except `node_modules/`, `build/`, DerivedData and `ios/App/App/public/`
(add them to `.gitignore`). The Android project is already tracked the same way. The repo is public (memory
`repo-is-public`): check the files for anything secret before the first commit and tell Dan in one line what is going in.
Commit from a fresh worktree off `origin/main` if the main checkout still cannot push.

### 6. Close out

- Update memory `ios-capacitor-app` (project restored, where it lives, tracked in git) and the smoke-test note in
  `android-device-testing`.
- Leave `ios-app-damaged-20261001` and its 24,841 duplicates for the duplicate cleanup in the iCloud handoff (one batch
  approval there), or ask Dan once here if that handoff has already run.
- Delete this handoff's lines from `AI_COORDINATION.md` and `Handoffs/README.md`. Report in chat: what was recovered,
  what was regenerated, and the list of settings that could not be confirmed against the old build.

## Out of scope

Any upload to App Store Connect, any reply to Apple, TestFlight, changes to the website or the Android app, switching
iCloud settings.

## What Dan has to do

Sign in at iCloud.com for step 0 (about ten minutes, before 2026-10-17). Sign in to Xcode only if a signed build is wanted.

## Starter prompt

> Read `Handoffs/handoff-20261001-rebuild-ios-project.md` in full, then rebuild the lost iPhone app project for
> com.absbyai.app as written: try the iCloud recovery with me first, work outside iCloud, regenerate the Capacitor
> project, restore the settings by comparing against the 2026-09-20 build, verify with a Release simulator build and
> `scripts/native-smoke-test.sh ios`, and put `ios-app/` under git. Rebuild only: no upload, submission or reply to Apple.

Recommended model: **Codex GPT-6 Sol, high effort.**
