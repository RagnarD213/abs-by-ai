---
name: android-twa-build-setup
description: Where the Android signing keystore and build toolchain live for the Abs by AI TWA app (none of it is in git)
metadata: 
  node_type: memory
  type: project
  originSessionId: 7aeb94f8-e6fd-47c2-b9d7-c4e342d4cc5e
---

The Abs by AI Android app (created 2026-06-10) is a Trusted Web Activity in `android/` (package `com.absbyai.app`) that wraps https://absbyai.com. Build-critical pieces that are gitignored or outside the repo:

- **Signing keystore**: `android/keystore/absbyai-release.keystore`, alias `absbyai`, password in `android/keystore.properties`. Losing these means losing the ability to update the app — user was told to back them up.
- **Cert SHA-256** (also in `.well-known/assetlinks.json`): `2D:99:A8:35:0B:C6:EE:3F:19:BA:95:FF:2A:22:7D:9B:8A:5A:A7:B1:CD:8E:F5:BF:8F:00:7A:76:1F:A6:75:E9`
- **Toolchain**: JDK 17 at `~/Library/Java/jdk-17.0.19+10/Contents/Home`, Android SDK at `~/Library/Android/sdk` (build-tools 35.0.0, platform android-35), Gradle dist at `~/Library/Android/dist/gradle-8.9` (project wrapper uses 8.11.1).
- **Build**: `cd android && JAVA_HOME=~/Library/Java/jdk-17.0.19+10/Contents/Home ./gradlew assembleRelease bundleRelease`
- Pin `androidbrowserhelper` at 2.5.0 — 2.6.2 drags in `androidx.browser:1.9.0-alpha04` which demands compileSdk 36.
- If user enrolls in Play App Signing, Google's signing cert SHA-256 (from Play Console) must be *added* to `.well-known/assetlinks.json` alongside the local one.

**Why:** none of this is recoverable from the repo; the keystore password and toolchain paths exist only on this machine.
**How to apply:** reuse these paths for rebuilds/version bumps (bump `versionCode` in `android/app/build.gradle`).
