# Handoff: Swap Dan's phone from the internal-test build to the public Play build

**Date:** 2026-08-18
**Project:** Abs By AI (Android / Google Play)
**Business goal this serves:** App adoption — Dan needs to see and use exactly what a real
new user downloads. Right now he is running a tester build, so any judgement he forms about
the store experience is judging the wrong artifact.

## Objective

Dan's Galaxy A14 is still running the **internal-testing** build of `com.absbyai.app`. He has
already been opted out of the test track, but Google Play on the device has not propagated the
change yet — the store page still renders the app as **"Abs by AI (Internal Beta)"** with a
*"You're an internal tester"* warning. The job is to **poll the device's Play page until that
label disappears, then uninstall the test build and install the public production build**, and
verify the app still works afterwards. This is a waiting task with a short action at the end.

## Current State

- **The app IS published and live on Google Play** — approved 2026-08-18. Public link:
  `https://play.google.com/store/apps/details?id=com.absbyai.app`
- **The public listing was fully verified on 2026-08-18** (name "Abs by AI", Health & Fitness,
  Everyone, developer Rose Digital Holdings LLC, 6 screenshots at 1350x2400, feature graphic
  1024x500, icon 512x512). **Do not re-verify it — that work is done.**
- **Gating assertions already passed 9/9 on this exact phone** against production. **Do not
  re-run them as new work** — you only re-run them at the end as a post-reinstall regression check.
- **Dan HAS been opted out of the internal test track.** Confirmed by Google's own page:
  *"You have left the testing program for Abs by AI (com.absbyai.app)."* Done via
  `https://play.google.com/apps/internaltest/4700579003000125158` → **Leave test program**.
- **The device still shows the test build.** Checked four times over ~7 minutes after opt-out;
  the Play page still said "Internal Beta" every time. Google's guidance is that leaving a test
  track can take **minutes to several hours** to propagate.
- Installed package state on the phone: `versionName=1.0`, `versionCode=1`,
  `installerPackageName=com.android.vending`, installed 2026-07-25. It is **Play-signed**
  (Google's app-signing key), and it launches full-screen with no Chrome address bar.
- Device: **Samsung Galaxy A14 5G, `SM-A146U`, Android 15**, adb serial **`R92W60LKM2D`**,
  connected over USB with debugging authorised.

## Key Decisions Already Made

- **Do NOT uninstall before Play offers the public version.** This is the whole reason the task
  exists. If you uninstall while Dan's account still resolves to the test track, he is left with
  **no app at all** for an unknown window. Waiting is strictly better than stranding him.
- **Do NOT run `adb shell pm clear com.android.vending`** to force a cache refresh. It wipes Play
  Store app data and settings on Dan's personal phone for a change that resolves on its own.
- **The opt-out itself is finished.** Do not click "Leave test program" again or go near the
  Play Console tester list.
- **Dan explicitly asked for a lower-tier model on this task** — it is polling plus a handful of
  taps. Do not escalate unless something genuinely unexpected happens.
- **Uninstall + reinstall is expected to preserve his absbyai.com login**, because a TWA keeps
  site data in **Chrome's** storage for the origin rather than inside the wrapper app. This is
  expected behaviour, **not verified** — if he does get signed out, that is annoying but normal,
  not a defect.

## Detailed Plan

**Preconditions:** the phone must be plugged in with USB debugging on. Confirm first:

```bash
~/Library/Android/sdk/platform-tools/adb devices -l
```

You want a line containing `R92W60LKM2D ... device`. If the list is empty, **stop and tell Dan
to plug the phone in** — do not proceed. (Note: the device can take ~30s to enumerate after
plugging in; poll a few times before declaring it absent.)

### 1. Poll until the "Internal Beta" label is gone

Each check force-stops Play (so it re-fetches rather than showing a cached page), reopens the
listing, dumps the UI, and greps for the label:

```bash
A=~/Library/Android/sdk/platform-tools/adb
$A shell am force-stop com.android.vending
sleep 2
$A shell am start -a android.intent.action.VIEW -d "market://details?id=com.absbyai.app" com.android.vending
sleep 10
$A shell uiautomator dump /sdcard/u.xml >/dev/null 2>&1
$A shell cat /sdcard/u.xml | grep -o 'Internal Beta' | head -1
```

- **Output `Internal Beta`** → not ready. Wait and check again.
- **Empty output** → propagated. Screenshot to confirm the page now looks like the normal public
  listing (no orange "You're an internal tester" warning), then go to step 2.

**Cadence:** check roughly every **20–30 minutes**, not every minute. This is a server-side
propagation with an hours-long tail; rapid polling buys nothing. If it has not flipped after
about **6 hours**, stop polling and tell Dan — at that point it is worth him checking whether the
opt-out registered against the right Google account.

### 2. Uninstall the test build

Get the button's real coordinates from the UI dump rather than guessing from a screenshot:

```bash
$A shell uiautomator dump /sdcard/u.xml >/dev/null 2>&1
$A shell cat /sdcard/u.xml | tr '>' '\n' | grep -iE 'text="Uninstall"|text="Install"|text="Open"|text="Update"' \
  | sed 's/.*text="\([^"]*\)".*bounds="\([^"]*\)".*/\1 :: \2/'
```

Bounds come back as `[x1,y1][x2,y2]`; tap the centre with `$A shell input tap <x> <y>`.
A confirmation dialog will appear — dump the UI again and tap its **OK / Uninstall** button.
Confirm the package is gone:

```bash
$A shell pm list packages | grep absbyai   # expect NO output
```

### 3. Install the public build

On the same Play page (re-open it if needed), find and tap **Install**. Wait for the download —
poll every ~15s for up to ~3 minutes:

```bash
$A shell dumpsys package com.absbyai.app | grep -iE "versionName|versionCode=|installerPackageName"
```

Success looks like `installerPackageName=com.android.vending`.

**If Install fails or the page still offers only the test build**, the propagation was partial.
**Reinstall the test build (tap Install again / the app is still on his account) rather than
leaving him with nothing**, and report back.

### 4. Verify, then leave his phone in a clean state

```bash
$A shell monkey -p com.absbyai.app -c android.intent.category.LAUNCHER 1
sleep 15
$A exec-out screencap -p > /tmp/absbyai-after-reinstall.png
```

Check on the screenshot:
- App fills the screen with **no Chrome address bar** (this is the assetlinks check — the single
  most important thing to confirm after a reinstall).
- The hub renders (either the member hub if his login survived, or the logged-out home).

Then re-run the gating assertions as a regression check:

```bash
cd "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
./scripts/native-smoke-test.sh android
```

**Caveat:** that script targets the **emulator** (`Pixel_8`) and will install the local sideloaded
APK. **Do not point it at Dan's phone** — that would replace the freshly installed Play build with
a sideloaded one and undo the entire task. To assert against the phone, do it directly over CDP
instead:

```bash
$A forward tcp:9222 localabstract:chrome_devtools_remote
curl -s http://localhost:9222/json    # expect a page whose url is https://absbyai.com/
```

then evaluate, via `websocket-client` in Python (already installed), that
`document.querySelectorAll('.app-hide-purchase')` has **> 0 total and 0 visible**. The full
working script from the 2026-08-18 session is reproduced in `AI_COORDINATION.md` under the
Android verification entry.

### 5. Close out

- Report to Dan: the app is now the public build, whether his login survived, and the
  no-address-bar result.
- Update `AI_COORDINATION.md` — the existing entry says the phone is *pending* the swap; change it
  to record the outcome.
- **Check the dashboard task off** (`money::Execute handoff: Swap Dan's phone to the public Play build`)
  per Rule 9. Mechanism and the two traps are in `CLAUDE.md` — note the `business` list is displayed
  as **`money`**, so the id is `money::…`.

## Things to Avoid / Lessons Learned

- **A Samsung "Open with" chooser (Google Play Store vs Galaxy Store) can intercept a
  `market://` intent.** Passing `com.android.vending` as the explicit component on `am start`
  avoids it. If it appears anyway, tap "Google Play Store" then "Just once".
- **Do not trust coordinates read off a screenshot.** In the 2026-08-18 session a click by
  element `ref` silently did nothing on the Play web page and only a coordinate click worked; on
  the device, `uiautomator dump` bounds were reliable and eyeballed coordinates were not. Dump,
  parse, tap the centre.
- **A system dialog "Allow access to phone data?" may be on screen** from the USB connection. It
  is a device permission — leave it for Dan, do not tap Allow.
- **Do not make AI calls.** The app hits production absbyai.com and every generation is real
  money. Launching, screenshotting and reading the DOM are all free; do not upload a photo or
  press Generate.
- **Dan is signed in as a member/admin**, so the hub shows a visible **"Manage membership"**
  button (`hubMembershipManageAppBtn`). That is expected and was already cleared as
  subscription *management*, not a purchase. Its Stripe-portal twin `hubMembershipManageBtn`
  correctly carries `app-hide-purchase` and stays hidden. **Do not report this as a defect.**
- **The emulator cannot substitute for this task.** Its Play Store sits behind a Google sign-in
  gate (`UnauthenticatedMainActivity`) and cannot install from Play at all.

## Relevant Files & Locations

- Public store page: `https://play.google.com/store/apps/details?id=com.absbyai.app`
- Internal test page (already left — reference only):
  `https://play.google.com/apps/internaltest/4700579003000125158`
- adb: `~/Library/Android/sdk/platform-tools/adb` (not on the default PATH)
- Repo: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`
- Smoke test (emulator-targeted): `scripts/native-smoke-test.sh`
- Screenshots from the prior session: `native-smoke-out/phone-01-play-listing.png`,
  `native-smoke-out/phone-02-app-launch.png` (git-ignored)
- Asset links: `public/.well-known/assetlinks.json` (holds **both** the upload-key and Google
  app-signing-key fingerprints — this is why the Play-signed build opens without an address bar)
- Coordination record: `AI_COORDINATION.md`, the 2026-08-18 Android verification entry

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Sonnet 5, standard thinking.** The task is polling plus a handful of `uiautomator`-guided taps — well-specified, low ambiguity. |
| **If Claude usage is high / approaching a limit** | **Codex mini-tier model, low effort.** It runs locally with shell access, so `adb` works fine. |

**Dan explicitly asked for a lower-tier model here — honour that.** There is no brand-voice,
architecture, or Anthropic-API work in this task, so none of the always-Claude overrides apply.
The one thing worth escalating for is if the label never flips after ~6 hours, which becomes an
account-level question rather than an execution one.

**Worth considering:** this is a natural fit for `/loop` in dynamic mode — it self-paces the
wake-ups, so the model is not burning tokens sitting in a foreground wait. Suggest a ~20–30
minute cadence, matching the polling guidance above.

## Starter Prompt for the Next Task

> Read `Handoffs/handoff-20260818-android-public-build-swap.md` in the Abs By AI repo and execute it.
>
> Short version: Dan's Galaxy A14 (`adb` serial `R92W60LKM2D`) is still running the internal-testing
> build of `com.absbyai.app`. He has already been opted out of the test track, but Google Play on the
> device has not propagated it yet and the store page still says "Abs by AI (Internal Beta)". Poll
> that page roughly every 20–30 minutes until the "Internal Beta" label is gone, then uninstall the
> test build and install the public production build from Play, then verify the app still opens
> full-screen with no Chrome address bar and that zero purchase controls are visible.
>
> **Critical: do NOT uninstall before Play actually offers the public version — that would leave Dan
> with no app.** Do not run `pm clear com.android.vending`. Do not point `scripts/native-smoke-test.sh`
> at the phone (it installs a sideloaded APK and would undo the work). Make no AI calls.
>
> First action: run `~/Library/Android/sdk/platform-tools/adb devices -l` and confirm the phone is
> connected. If it is not, stop and ask Dan to plug it in.
