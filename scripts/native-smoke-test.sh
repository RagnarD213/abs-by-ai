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
#
# LOCAL PREREQUISITES (not in this repo)
#   - ios-app/  ... the Capacitor wrapper, untracked; iOS run needs it
#   - Xcode + an iPhone simulator; Android SDK + an AVD (default Pixel_8)
#   - pip3 install websocket-client   (enables the Android gating assertions)

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
PASS=0; FAIL=0; PHYSICAL=0
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
  local built=$?

  local app="${dd}/Build/Products/Release-iphonesimulator/App.app"
  if [ ! -d "$app" ]; then
    bad "iOS build produced no App.app (see ${OUT}/ios-build.log)"; return
  fi
  if [ "$built" -eq 0 ]; then
    ok "iOS Release build succeeded"
  else
    # The app only wraps the live site (server.url), so the last good build still tests
    # today's website. It does not test native code changed since that build.
    # 2026-09-30: iCloud had wiped ios-app/ios/App/App.xcodeproj/project.pbxproj.
    echo "  WARN  iOS build failed (see ${OUT}/ios-build.log); using the last good build from $(stat -f '%Sm' -t '%Y-%m-%d' "$app")"
  fi

  xcrun simctl install "$IOS_SIM" "$app" >/dev/null 2>&1 \
    && ok "iOS app installed" || bad "iOS install failed"
  xcrun simctl launch "$IOS_SIM" "$BUNDLE_ID" >/dev/null 2>&1 \
    && ok "iOS app launched" || bad "iOS launch failed"

  sleep 12
  # The simulator service may not write into ~/Documents ("Operation not permitted",
  # 2026-10-01), so capture to a temp file and copy it in.
  local shot; shot="$(mktemp -t ios-smoke).png"
  xcrun simctl io "$IOS_SIM" screenshot "$shot" >/dev/null 2>&1 && cp "$shot" "${OUT}/ios-01-launch.png" \
    && ok "iOS screenshot captured -> native-smoke-out/ios-01-launch.png" \
    || bad "iOS screenshot failed"
  rm -f "$shot"

  echo "  NOTE  iOS purchase-gating is a visual check — open the screenshot and"
  echo "        confirm no credit packs / plan cards / 'Manage membership' button,"
  echo "        and that 'Delete my account' is still present in the hub."
}

# ------------------------------------------------------------ Android --------
# Poll Chrome DevTools (forwarded to localhost:9222) until a page whose URL contains $1 exists
# and has finished loading. Taps past Chrome's first-run screen once if nothing shows up.
wait_for_page() {
  local want="$1" limit="${2:-120}" waited=0 tapped=0
  while [ "$waited" -lt "$limit" ]; do
    if python3 - "$want" <<'PY' 2>/dev/null; then return 0; fi
import json, sys, urllib.request
from websocket import create_connection
tabs = json.load(urllib.request.urlopen("http://localhost:9222/json", timeout=5))
tab = next(t for t in tabs if t["type"] == "page" and sys.argv[1] in t.get("url", ""))
ws = create_connection(tab["webSocketDebuggerUrl"], suppress_origin=True, timeout=10)
ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": "document.readyState", "returnByValue": True}}))
while True:
    m = json.loads(ws.recv())
    if m.get("id") == 1: break
sys.exit(0 if m["result"]["result"].get("value") == "complete" else 1)
PY
    if [ "$PHYSICAL" -eq 0 ] && [ "$tapped" -eq 0 ] && [ "$waited" -ge 30 ]; then
      # Chrome's first-run screen can sit in front of the TWA on a fresh emulator.
      # "Use without an account" is near the bottom; tapping it is harmless if absent.
      "$ADB" shell input tap 540 2087 >/dev/null 2>&1; tapped=1
    fi
    "$ADB" forward tcp:9222 localabstract:chrome_devtools_remote >/dev/null 2>&1
    sleep 5; waited=$((waited + 5))
  done
  return 1
}

run_android() {
  step "Android — Pixel emulator"

  # A plugged-in phone (USB debugging on) wins over the emulator: it is the real Play Store app
  # and does not depend on the Mac having spare CPU.
  local serial
  serial=$("$ADB" devices | awk 'NR>1 && $2=="device" && $1 !~ /^emulator-/ {print $1; exit}')
  if [ -n "$serial" ] && [ "${SMOKE_USE_EMULATOR:-0}" != "1" ]; then  # SMOKE_USE_EMULATOR=1 forces the emulator
    export ANDROID_SERIAL="$serial"; PHYSICAL=1
    ok "using the plugged-in Android phone ($serial)"
  else
    # The emulator's watchdog kills it when its virtual CPUs stall for 15 s. With video renders
    # running (load 300 to 650 on 10 cores, 2026-09-30) it crashed on every boot. Skip cleanly.
    local load cores
    load=$(sysctl -n vm.loadavg | awk '{print int($2)}'); cores=$(sysctl -n hw.ncpu)
    if [ "$load" -gt $((cores * 8)) ]; then
      bad "Mac too busy for the emulator (load ${load} on ${cores} cores). Rerun when the renders finish, or plug in the Android phone."
      return
    fi
    if ! "$ADB" devices | grep -q "emulator.*device"; then
      echo "  booting $AVD ..."
      "$EMULATOR" -avd "$AVD" -no-snapshot-load -no-boot-anim \
        >"${OUT}/emulator.log" 2>&1 &
      "$ADB" -e wait-for-device
      for _ in $(seq 1 60); do
        [ "$("$ADB" -e shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')" = "1" ] && break
        sleep 3
      done
    fi
    # Pin every later adb call to the emulator (a phone may be plugged in as well).
    export ANDROID_SERIAL="$("$ADB" devices | awk '$1 ~ /^emulator-/ && $2=="device" {print $1; exit}')"
    ok "emulator ready"

    local apk="${REPO}/android/app/build/outputs/apk/release/app-release.apk"
    [ -f "$apk" ] || { bad "no APK at $apk"; return; }
    "$ADB" install -r "$apk" 2>&1 | grep -q Success \
      && ok "APK installed" || bad "APK install failed"
  fi

  # Force-stop first so we always start from a fresh page load — a resumed task
  # would keep whatever DOM state a previous run left behind.
  "$ADB" shell am force-stop "$BUNDLE_ID" >/dev/null 2>&1
  # On the emulator, restart Chrome too: a Chrome left over from an earlier boot showed the app
  # as a blank page and never opened its DevTools socket (2026-10-01). Never on a real phone.
  [ "$PHYSICAL" -eq 0 ] && "$ADB" shell am force-stop com.android.chrome >/dev/null 2>&1
  "$ADB" shell monkey -p "$BUNDLE_ID" -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
  # Wait for the page itself, not a fixed time: on a loaded Mac (video builds running) the TWA
  # sat on its splash screen past the old 20 s sleep and every check after it failed (2026-09-30).
  "$ADB" forward tcp:9222 localabstract:chrome_devtools_remote >/dev/null 2>&1
  if wait_for_page "absbyai.com" 150; then ok "app page loaded"; else bad "app page never loaded (150 s)"; fi
  "$ADB" exec-out screencap -p > "${OUT}/android-01-launch.png" 2>/dev/null \
    && ok "Android screenshot captured -> native-smoke-out/android-01-launch.png"

  # Programmatic gating assertions over the Chrome DevTools protocol.
  step "Android — purchase-gating assertions"
  python3 - "$OUT" <<'PY'
import json, sys, time, urllib.request
try:
    from websocket import create_connection
except ImportError:
    print("  SKIP  pip3 install websocket-client to enable Android assertions"); sys.exit(0)

def ev(expr, want="absbyai.com"):
    for attempt in range(6):  # the DevTools socket drops connections while Chrome is busy
        try:
            return _ev(expr, want)
        except Exception:
            if attempt == 5: raise
            time.sleep(5)

def _ev(expr, want):
    tabs = json.load(urllib.request.urlopen("http://localhost:9222/json", timeout=10))
    tab = next(t for t in tabs if t["type"] == "page" and want in t.get("url", ""))
    ws = create_connection(tab["webSocketDebuggerUrl"], suppress_origin=True, timeout=20)
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
  # The /start sales page opened INSIDE the app (an ad click on a phone with the app installed
  # lands here, because the app claims every absbyai.com link): no buy buttons, no prices,
  # the "Open Abs By AI" button instead (2026-09-30).
  step "Android: /start sales page inside the app"
  "$ADB" shell am start -a android.intent.action.VIEW -d "https://absbyai.com/start" \
    -n "${BUNDLE_ID}/com.google.androidbrowserhelper.trusted.LauncherActivity" >/dev/null 2>&1
  if wait_for_page "absbyai.com/start" 120; then
    "$ADB" exec-out screencap -p > "${OUT}/android-02-start.png" 2>/dev/null \
      && ok "Android /start screenshot -> native-smoke-out/android-02-start.png"
    python3 - <<'PY'
import json, time, urllib.request
from websocket import create_connection
def ev(expr):
    for attempt in range(6):
        try:
            tabs = json.load(urllib.request.urlopen("http://localhost:9222/json", timeout=10))
            tab = next(t for t in tabs if t["type"] == "page" and "absbyai.com/start" in t.get("url", ""))
            ws = create_connection(tab["webSocketDebuggerUrl"], suppress_origin=True, timeout=20)
            ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True}}))
            while True:
                m = json.loads(ws.recv())
                if m.get("id") == 1:
                    ws.close(); return json.loads(m["result"]["result"]["value"])
        except Exception:
            if attempt == 5: raise
            time.sleep(5)
st = ev("""JSON.stringify({
  nativeClass: document.documentElement.classList.contains('native-app'),
  buttons: document.querySelectorAll('.js-cta').length,
  buttonsVisible: [...document.querySelectorAll('.js-cta')].filter(e => e.offsetParent !== null).length,
  pricesVisible: [...document.querySelectorAll('.app-hide-purchase')].filter(e => e.offsetParent !== null).length,
  openAppVisible: [...document.querySelectorAll('.app-only-note')].filter(e => e.offsetParent !== null).length,
  video: !!document.getElementById('vsl')
})""")
for label, good in [("sales page loaded in the app (video present)", st["video"]),
                    ("native-app class applied on /start",           st["nativeClass"]),
                    ("buy buttons exist in the page",                st["buttons"] > 0),
                    ("ZERO buy buttons or price lines visible",      st["buttonsVisible"] == 0 and st["pricesVisible"] == 0),
                    ("'Open Abs By AI' shown instead",               st["openAppVisible"] > 0)]:
    print(("  PASS  " if good else "  FAIL  ") + label)
print("  DATA  " + json.dumps(st))
PY
  else
    bad "/start never loaded inside the app (120 s)"
  fi
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
