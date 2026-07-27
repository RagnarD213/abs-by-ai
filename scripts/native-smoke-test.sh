#!/usr/bin/env bash
# Abs By AI — native smoke test
#
# WHY THIS EXISTS
# iOS (Capacitor) and Android (TWA) both load the live https://absbyai.com.
# A Railway deploy therefore updates all three platforms at once, but some
# changes can pass on the web and still break inside the app shells.
# This script boots both simulated phones against PRODUCTION and captures
# proof, so Dan does not have to pick up a physical phone.
#
# WHAT IT DOES NOT DO
#  - It does not touch real hardware, real payments, or the app stores.
#  - It deliberately makes NO AI calls (no generations / macro / trainer runs),
#    because the apps hit production and every call is real money.
#
# USAGE
#   scripts/native-smoke-test.sh            # both platforms
#   scripts/native-smoke-test.sh ios        # iOS only
#   scripts/native-smoke-test.sh android    # Android only
#
# Screenshots + a summary land in ./native-smoke-out/ (git-ignored).

set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${REPO}/native-smoke-out"
ADB="${HOME}/Library/Android/sdk/platform-tools/adb"
EMULATOR="${HOME}/Library/Android/sdk/emulator/emulator"
AVD="${AVD_NAME:-Pixel_8}"
IOS_SIM="${IOS_SIM_UDID:-A43844F9-3EA4-4EB3-B21D-9F8945317C94}"   # iPhone 17 Pro
BUNDLE_ID="com.absbyai.app"
TARGET="${1:-both}"

mkdir -p "$OUT"
PASS=0; FAIL=0
ok()   { echo "  PASS  $*"; PASS=$((PASS+1)); }
bad()  { echo "  FAIL  $*"; FAIL=$((FAIL+1)); }
step() { echo ""; echo "== $* =="; }

# ---------------------------------------------------------------- iOS --------
run_ios() {
  step "iOS — iPhone simulator"

  xcrun simctl boot "$IOS_SIM" >/dev/null 2>&1
  xcrun simctl bootstatus "$IOS_SIM" -b >/dev/null 2>&1

  # IMPORTANT: build Release, not Debug. Xcode 26 Debug builds use a separate
  # App.debug.dylib and refuse to launch from simctl (SBMainWorkspace denies
  # the request). Release launches cleanly. Discovered 2026-07-27.
  step "iOS — building Release simulator app"
  local dd="${OUT}/ios-dd"
  ( cd "${REPO}/ios-app/ios/App" && xcodebuild \
      -project App.xcodeproj -scheme App -configuration Release \
      -sdk iphonesimulator -derivedDataPath "$dd" \
      -destination "platform=iOS Simulator,id=${IOS_SIM}" \
      CODE_SIGNING_ALLOWED=NO build ) >"${OUT}/ios-build.log" 2>&1

  local app="${dd}/Build/Products/Release-iphonesimulator/App.app"
  if [ ! -d "$app" ]; then
    bad "iOS build produced no App.app (see ${OUT}/ios-build.log)"; return
  fi
  ok "iOS Release build succeeded"

  xcrun simctl install "$IOS_SIM" "$app" >/dev/null 2>&1 \
    && ok "iOS app installed" || bad "iOS install failed"
  xcrun simctl launch "$IOS_SIM" "$BUNDLE_ID" >/dev/null 2>&1 \
    && ok "iOS app launched" || bad "iOS launch failed"

  sleep 12
  xcrun simctl io "$IOS_SIM" screenshot "${OUT}/ios-01-launch.png" >/dev/null 2>&1 \
    && ok "iOS screenshot captured -> native-smoke-out/ios-01-launch.png" \
    || bad "iOS screenshot failed"

  echo "  NOTE  iOS purchase-gating is a visual check — open the screenshot and"
  echo "        confirm no credit packs / plan cards / 'Manage membership' button,"
  echo "        and that 'Delete my account' is still present in the hub."
}

# ------------------------------------------------------------ Android --------
run_android() {
  step "Android — Pixel emulator"

  if ! "$ADB" devices | grep -q "emulator.*device"; then
    echo "  booting $AVD ..."
    "$EMULATOR" -avd "$AVD" -no-snapshot-load -no-boot-anim \
      >"${OUT}/emulator.log" 2>&1 &
    "$ADB" wait-for-device
    for _ in $(seq 1 60); do
      [ "$("$ADB" shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')" = "1" ] && break
      sleep 3
    done
  fi
  ok "emulator ready"

  local apk="${REPO}/android/app/build/outputs/apk/release/app-release.apk"
  [ -f "$apk" ] || { bad "no APK at $apk"; return; }
  "$ADB" install -r "$apk" 2>&1 | grep -q Success \
    && ok "APK installed" || bad "APK install failed"

  # Force-stop first so we always start from a fresh page load — a resumed task
  # would keep whatever DOM state a previous run left behind.
  "$ADB" shell am force-stop "$BUNDLE_ID" >/dev/null 2>&1
  "$ADB" shell monkey -p "$BUNDLE_ID" -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
  sleep 14

  # Chrome's first-run screen can sit in front of the TWA on a fresh emulator.
  # "Use without an account" is near the bottom; tapping it is harmless if absent.
  "$ADB" shell input tap 540 2087 >/dev/null 2>&1
  sleep 6
  "$ADB" exec-out screencap -p > "${OUT}/android-01-launch.png" 2>/dev/null \
    && ok "Android screenshot captured -> native-smoke-out/android-01-launch.png"

  # Programmatic gating assertions over the Chrome DevTools protocol.
  step "Android — purchase-gating assertions"
  "$ADB" forward tcp:9222 localabstract:chrome_devtools_remote >/dev/null 2>&1
  python3 - "$OUT" <<'PY'
import json, sys, urllib.request
try:
    from websocket import create_connection
except ImportError:
    print("  SKIP  pip3 install websocket-client to enable Android assertions"); sys.exit(0)

def ev(expr):
    tabs = json.load(urllib.request.urlopen("http://localhost:9222/json"))
    tab = next(t for t in tabs if t["type"] == "page" and "absbyai.com" in t.get("url", ""))
    ws = create_connection(tab["webSocketDebuggerUrl"], suppress_origin=True)
    ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
                        "params": {"expression": expr, "returnByValue": True}}))
    while True:
        m = json.loads(ws.recv())
        if m.get("id") == 1:
            ws.close()
            return json.loads(m["result"]["result"]["value"])

state = ev("""JSON.stringify({
  twaFlag: sessionStorage.getItem('absbyai_twa'),
  nativeClass: document.documentElement.classList.contains('native-app'),
  gatedTotal: document.querySelectorAll('.app-hide-purchase').length,
  gatedVisible: [...document.querySelectorAll('.app-hide-purchase')].filter(e=>e.offsetParent!==null).length,
  noteRuleActive: [...document.querySelectorAll('.app-only-note')]
    .every(e => getComputedStyle(e).display !== 'none' || e.style.display === 'none')
})""")

checks = [
    ("TWA detected (absbyai_twa flag set)",      state["twaFlag"] == "1"),
    ("native-app class applied to <html>",       state["nativeClass"] is True),
    ("purchase elements exist in the page",      state["gatedTotal"] > 0),
    ("ZERO purchase controls visible",           state["gatedVisible"] == 0),
    ("app-only explanatory notes enabled",       state["noteRuleActive"] is True),
]
for label, good in checks:
    print(("  PASS  " if good else "  FAIL  ") + label)
print("  DATA  " + json.dumps(state))

# Force the membership + paywall screens open and re-check. These are the two
# screens Apple/Google actually look at, and they are otherwise unreachable
# without spending money on a real generation.
for sid in ("membershipSection", "paywallSection"):
    r = ev("""(()=>{const s=document.getElementById('%s');if(!s)return JSON.stringify({missing:true});
      document.querySelectorAll('section').forEach(x=>x.style.display='none');s.style.display='block';
      return JSON.stringify({visible:[...s.querySelectorAll('.app-hide-purchase')].filter(e=>e.offsetParent!==null).length,
      total:s.querySelectorAll('.app-hide-purchase').length})})()""" % sid)
    if r.get("missing"):
        print(f"  WARN  {sid} not found")
    else:
        good = r["visible"] == 0
        print(("  PASS  " if good else "  FAIL  ") +
              f"{sid}: {r['visible']} of {r['total']} purchase controls visible")
PY
}

case "$TARGET" in
  ios)     run_ios ;;
  android) run_android ;;
  *)       run_ios; run_android ;;
esac

step "Summary"
echo "  script-level checks: ${PASS} passed, ${FAIL} failed"
echo "  screenshots: ${OUT}"
echo ""
echo "  Reminder: this runs against PRODUCTION absbyai.com and makes no AI calls."
echo "  Simulators prove rendering, layout and gating. They do NOT prove real"
echo "  camera behaviour, real payments, or your specific physical handset."
[ "$FAIL" -eq 0 ]
