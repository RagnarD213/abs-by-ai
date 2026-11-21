# Abs by AI iPhone app

This is the Capacitor 8 iOS shell for https://absbyai.com. It uses the bundle ID `com.absbyai.app` and Swift Package Manager. The website supplies the screens. The native project supplies the app icon, launch screen, camera and photo permissions, safe area handling, and plugins.

The native plugins are App, Filesystem, Haptics, Keyboard, Share, SplashScreen, StatusBar, and RevenueCat Purchases. The Purchases plugin is needed for the Apple subscription flow used in the last submitted build.

## Build for the simulator

From the repository root:

```bash
cd ios-app
npm ci
npx cap sync ios
xcodebuild -project ios/App/App.xcodeproj -scheme App -configuration Release -sdk iphonesimulator -destination 'platform=iOS Simulator,name=iPhone 17 Pro' CODE_SIGNING_ALLOWED=NO build
cd ..
scripts/native-smoke-test.sh ios
```

The smoke test must report `iOS Release build succeeded`. Its output and screenshot are in `native-smoke-out/`.

The source assets and Xcode project are tracked in git. Generated web copies, dependencies, and build output are excluded. The `www/index.html` file is a placeholder because the app loads the live site through `server.url` in `capacitor.config.json`.

Release signing records team `8C7HC8F4DR` and the `AbsByAI App Store` provisioning profile for a later device or archive build. The simulator build disables signing. Rebuilding this project does not upload or submit anything to Apple.
