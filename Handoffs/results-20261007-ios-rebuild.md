# iPhone project rebuild results, 2026-10-07

## Result

A new Capacitor 8 iPhone project for `com.absbyai.app` is buildable outside iCloud at `/Users/danielrose/.codex/worktrees/ios-rebuild/Abs By AI/ios-app`. It is tracked on GitHub `main` in commit `8e5a9e3`. No Apple upload, submission, TestFlight action, or reply was made. The damaged `ios-app/` folder in the iCloud-synced main checkout was not moved, deleted, or quarantined.

## Recovery attempt

- Signed-in iCloud Drive, Recently Deleted contained one unrelated folder and no iPhone project files.
- iCloud Data Recovery, Restore Files loaded more than 7,168 deleted entries. No `project.pbxproj`, `AppDelegate.swift`, `Info.plist`, `Package.swift`, `capacitor.config.json`, or `gen-assets.swift` appeared in the loaded entries. Chrome crashed before the full list finished. There is no search box in that recovery view, so absence from the entire list is not confirmed.
- The Mac Trash and local iCloud Trash contained none of those filenames. No file was recovered.
- iCloud Drive's search offered to enable search through the trusted Mac mini. That account setting was left unchanged. The local source inventory already showed the target files missing.
- The estimated iCloud recovery cutoff is October 17, 2026. If the original files are essential, the remaining uninspected Data Recovery entries need another method or Apple Support before then.

## Rebuild

- Copied the surviving `package.json` and lockfile, ran `npm ci`, created a minimal `www/index.html`, then ran `npx cap add ios` and `npx cap sync ios`.
- Restored `capacitor.config.json` from the September 20 compiled app, excluding the generated plugin list. All seven surviving numbered config copies matched it.
- Restored display name, minimum iOS 15, iPhone portrait and all iPad orientations, camera and photo descriptions, and the encryption declaration. Set version 1.0, build 4, based on the last documented App Store build 1.0 (3).
- Included the RevenueCat Purchases plugin. The August submitted build and successful sandbox purchase used it. The September 20 debug build's plugin list omitted it, so that debug build was not a reliable record of the last submission.
- Restored signing team `8C7HC8F4DR`, Release manual signing with the `AbsByAI App Store` profile, and the In-App Purchase capability from the archived build notes. Device and archive signing were not tested in this rebuild.
- The surviving asset catalog had no image files. Recreated the app icon and splash assets from `public/img/icon-512.png`. The exact former splash layout could not be confirmed.
- The generated native app contains no app-level privacy manifest, matching the old simulator builds.

## Verification

- Xcode 26.6 Release simulator build: `BUILD SUCCEEDED`.
- `scripts/native-smoke-test.sh ios`: `iOS Release build succeeded`, app installed, app launched, screenshot captured, 4 checks passed and 0 failed. Screenshot: `native-smoke-out/ios-01-launch.png` in the outside-iCloud worktree. It shows the live home screen and clear top safe area.
- Compared every compiled `Info.plist` key against the September 20 debug app. Only `CFBundleVersion` changed from 1 to 4 and `CAPACITOR_DEBUG` changed from `true` to blank because this is a Release build. Every other key matched.
- The new compiled plugin list has the old seven plugins plus `PurchasesPlugin`, for the reason above.
- The membership screen was not visually checked in the simulator because it requires signing into an app account. The smoke test does not run payments.
- No secrets were found in the iPhone source files selected for git. The tracked set excludes `node_modules/`, generated web copies, build output, and Xcode user data.

## Current limits

The iCloud-synced main checkout still has the damaged original folder. Use the outside-iCloud worktree for iPhone builds until the separate project-move handoff finishes. Recovery did not find the original project, and the full Data Recovery list remains uninspected. The RevenueCat purchase flow, device signing, and App Store archive still need testing before any future submission.
