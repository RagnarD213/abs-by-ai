#!/bin/zsh
# Run before any batch. Proves the module still measures what it claims:
#   1 the gate reads ZERO error on the reference against itself (metric identity)
#   2 the gate PASSES the Ad 1 vertical (Dan-approved audio, 2026-09-02) and the approved website video rev 2
#     (EDT 75 ms -- the approved side of the room boundary), and FAILS the REJECTED rev 1 on floor + tone
#   3 the gate FAILS a synthetic both-mics-summed render of the same cut (far mic 7.5 ms late,
#     polarity-inverted, with a room tail) -- on the comb and floor rows (its decay reads 56 ms: a synthetic
#     tail is not a real room; the real rejected room measured 85)
#   4 pick_lav picks a:1 on an 8/28 four-track roll, c1 on an 8/3 roll and on the 8/14 ad roll
#     (polarity inverted), and the single live channel on an 8/14 ab-wheel roll (dead left input)
#   5 voice_chain REFUSES a stacked `pan` pull (ffmpeg renders it as silence, not an error)
#   6 voice_chain end-to-end on an 8/28 excerpt (4 tracks, wet room) -> the gate PASSES the output,
#     the untreated baseline is written, and the do_no_harm row actually runs
#   7 the do-no-harm row REFUSES the dereverb Dan rejected on 2026-09-09 and accepts the one he
#     approved, from the same source through the same chain; a MISSING baseline FAILS the file
#     (2026-09-09: it used to pass as "not measured"), and --untreated can restore it
#   8 a --synthetic stamp does NOT satisfy a caller that needs the full camera gate (require_stamp
#     is strict by default since 2026-09-09; --allow-synthetic is the explicit, visible opt-in)
# Steps 4 and 6 need the Seagate mounted; they are skipped (loudly) if it is not.
set -u
# ⚠ ZSH ONLY, AND IT MUST SAY SO. Run under bash, `${0:A:h}` below expands to nothing and the script
# dies with "A: unbound variable" -- which is indistinguishable from a real bug, and is how this
# selftest spent 2026-09-09 documented as BROKEN in README.md while passing 16/16 under zsh.
if [ -z "${ZSH_VERSION:-}" ]; then
  echo "selftest.sh is a zsh script (it uses \${0:A:h}). Run:  zsh $0" >&2; exit 2
fi
HERE="${0:A:h}"; cd "$HERE"
S="${SELFTEST_DIR:-/tmp/audio_selftest}"; mkdir -p "$S"
REPO="$HERE/../../../.."
# ⚠ PATHS MOVED 2026-09-08 by the editor-deliveries rename ("<title> - ad N/", filenames gain
# "| ad N"). Steps 1 and 2 broke outright; 3 and 5 then failed as CASCADES (an unreadable AD1V
# gave step 3 an empty wav -> "duration N/A", and step 5 an empty pull -> the wrong refusal),
# which is why the run looked like four independent faults. Fixed 2026-09-09.
P="$REPO/Muhammad Ad Videos/this picture got me abs - ad 1"
REF="$P/this picture got me abs | muhammad | 16x9 | ad 1.mp4"
# the Ad 1 VERTICAL (this used to be called AD2, which it never was): normal-mode PASS fixture,
# audio rebuilt 2026-09-02. Ad 2's vertical carries Muhammad's own mix and gates in
# --reference-mix mode, so it is not the right fixture for the full row set.
AD1V="$P/this picture got me abs | claude | 9x16 | ad 1.mp4"
R828="/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera"
R803="/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera"
R814="/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose"
FF="$REPO/Media/video_edit/bin/ffmpeg"
fail=0
ok()   { echo "  ✓ $1"; }
bad()  { echo "  ✗ $1"; fail=$((fail+1)); }
expect_lav() {  # file ss t expected_map expected_filter [expected_polarity]
  local extra=(); [[ -n "$2" ]] && extra+=(--ss "$2"); [[ -n "$3" ]] && extra+=(--t "$3")   # zsh does not word-split ${2:+--ss $2}
  local out; out=$(python3 pick_lav.py "$1" "${extra[@]}" --out "$S/$(basename "$1").audio_source.json" 2>&1); local rc=$?
  if [[ $rc -ne 0 ]]; then bad "pick_lav $(basename "$1") exited $rc"; echo "$out" | tail -3; return; fi
  local m; m=$(python3 -c "import json,sys;d=json.load(open(sys.argv[1]));print(d['map'],d['filter'],d.get('polarity'),d['verdict'])" "$S/$(basename "$1").audio_source.json")
  if [[ "$m" == "$4 $5 $6"* ]]; then ok "pick_lav $(basename "$1"): $m"; else bad "pick_lav $(basename "$1"): got '$m', expected '$4 $5 $6'"; fi
}
echo "== 1 reference identity"
python3 audio_gate.py "$REF" --reference-rows-only --no-stamp >"$S/1.log" 2>&1 && grep -q "mean |err| 0.00 dB" "$S/1.log" && ok "zero tone error, all reference rows pass" || { bad "reference identity"; tail -5 "$S/1.log"; }
echo "== 2 the Ad 1 vertical (approved audio) must PASS every measurable row"
# ⚠ LEGACY BASELINE GAP (2026-09-09). This file was rendered and approved before voice_chain started
# stashing the untreated signal, so `do_no_harm` reads NOT MEASURED -- which is now a FAIL, correctly:
# nobody looked. That is a fact about the file's history, not a fault in its audio, so the fixture
# asserts "no OTHER row fails". ⚠ Do NOT relax this into "do_no_harm may fail" for files we render
# from here on: those carry a baseline, and a missing one means the chain was bypassed.
_only_dnh() {   # log -> 0 if the only failing row is an unmeasured do_no_harm
  local other; other=$(grep "^  FAIL" "$1" | grep -v "do no harm: NOT MEASURED" | wc -l | tr -d ' ')
  [[ "$other" == "0" ]] && grep -q "FAIL  do no harm: NOT MEASURED" "$1"
}
if python3 audio_gate.py "$AD1V" --no-stamp >"$S/2.log" 2>&1; then ok "Ad 1 vertical PASS"
elif _only_dnh "$S/2.log"; then ok "Ad 1 vertical passes every measurable row (do_no_harm unmeasured: pre-09-09 render)"
else bad "Ad 1 vertical failed a real row"; grep FAIL "$S/2.log"; fi
echo "== 2b the website video: rev 2 (APPROVED, 8/28 room at 75 ms) must PASS; rev 1 (REJECTED on floor) must FAIL"
WV="$REPO/claude edited long form content/06 - Website Conversion Video (post-generation)"
# ⚠ NAME THE REVISION, NOT THE POINTER. This used to gate "website_video_16x9.mp4" and call it
# rev 2; that filename is now rev 5 (rev 2 was superseded on picture, not audio), so the test was
# silently checking a different file than its label claimed. Fixed 2026-09-09.
if [[ -f "$WV/website_video_16x9_REV2_REJECTED.mp4" ]]; then
  if python3 audio_gate.py "$WV/website_video_16x9_REV2_REJECTED.mp4" --no-stamp >"$S/2b.log" 2>&1; then
    ok "website rev 2 (audio approved: \"you got it nailed\") PASS"
  elif _only_dnh "$S/2b.log"; then
    ok "website rev 2 (approved) passes every measurable row (do_no_harm unmeasured: pre-09-09 render)"
  else bad "website rev 2 (approved) failed a real row"; grep FAIL "$S/2b.log"; fi
  if python3 audio_gate.py "$WV/website_video_16x9_REV1_REJECTED.mp4" --no-stamp >"$S/2c.log" 2>&1; then bad "website rev 1 (REJECTED) passed"; else
    grep -q "FAIL  clean between words" "$S/2c.log" && grep -q "FAIL  tone" "$S/2c.log" && ok "website rev 1 (rejected) FAILS on floor + tone ($(grep -c FAIL "$S/2c.log") rows)" || { bad "rev 1 failed, but not on floor/tone"; grep FAIL "$S/2c.log"; }; fi
else echo "  ⚠ SKIPPED: website video not in the project folder"; fi
echo "== 3 summed-both-mics render must FAIL"
python3 - "$AD1V" "$S/ad1v_summed_mics.wav" <<'EOF'
import sys, wave; sys.path.insert(0,'.')
import numpy as np, common as C
src,out=sys.argv[1],sys.argv[2]; sr=C.SR
m=C.pcm(src,ac=1); rng=np.random.default_rng(1)
tail=rng.standard_normal(int(0.35*sr))*np.exp(-np.arange(int(0.35*sr))/(0.08*sr)); tail/=np.sqrt((tail**2).sum())*3
N=1<<int(np.ceil(np.log2(len(m)+len(tail)))); far=np.fft.irfft(np.fft.rfft(m,N)*np.fft.rfft(tail,N),N)[:len(m)]
d=int(0.0075*sr); far=np.roll(far+m,d); far[:d]=0
comb=m-0.5*far; comb*=(np.sqrt((m**2).mean())/np.sqrt((comb**2).mean()))
w=wave.open(out,'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((np.clip(np.stack([comb,comb],1),-1,1)*32767).astype(np.int16).tobytes()); w.close()
EOF
if python3 audio_gate.py "$S/ad1v_summed_mics.wav" --video "$AD1V" --no-stamp >"$S/3.log" 2>&1; then bad "summed-mics render PASSED the gate"; else
  grep -q "FAIL  no comb" "$S/3.log" && grep -q "FAIL  clean between words" "$S/3.log" && ok "summed-mics render FAILS on comb + floor ($(grep -c FAIL "$S/3.log") rows)" || { bad "summed-mics failed, but not on the comb/floor rows"; grep FAIL "$S/3.log"; }; fi
echo "== 4 pick_lav on every roll type"
if [[ -d "$R828" ]]; then
  expect_lav "$R828/C1650.MP4" "" "" "0:a:1" "pan=mono|c0=c0" "inverted"
  expect_lav "$R803/C1514.MP4" 1492 40 "0:a:0" "pan=mono|c0=c1" "normal"
  expect_lav "$R814/C1591.MP4" "" "" "0:a:0" "pan=mono|c0=c1" "inverted"
  expect_lav "$R814/C1630.MP4" "" "" "0:a:0" "pan=mono|c0=c1" "None single-live"
else echo "  ⚠ SKIPPED: Seagate not mounted"; fi
echo "== 5 stacked pan refused"
if python3 voice_chain.py --in "$AD1V" --out "$S/doublepan.wav" --pull "pan=mono|c0=c1,pan=mono|c0=c1" --work "$S/_dp" >"$S/5.log" 2>&1; then bad "double pan was NOT refused"; else grep -q "SILENT" "$S/5.log" && ok "stacked pan refused as silence" || { bad "refused for another reason"; tail -2 "$S/5.log"; }; fi
echo "== 6 chain end-to-end on an 8/28 excerpt"
if [[ -d "$R828" ]]; then
  "$FF" -nostdin -y -v error -ss 40 -t 90 -i "$R828/C1650.MP4" -vn -map 0:a -c:a copy "$S/c1650_ex.mov" \
  && python3 pick_lav.py "$S/c1650_ex.mov" >"$S/6a.log" 2>&1 \
  && python3 voice_chain.py --in "$S/c1650_ex.mov" --out "$S/c1650_chain.mp4" --work "$S/_vc" >"$S/6b.log" 2>&1 \
  && python3 audio_gate.py "$S/c1650_chain.mp4" >"$S/6c.log" 2>&1 \
  && python3 require_stamp.py "$S/c1650_chain.mp4" >/dev/null 2>&1 \
  && grep -q "PASS  no worse than untreated" "$S/6c.log" \
  && [[ -f "$S/c1650_chain.mp4.audio_untreated.json" ]] \
  && ok "excerpt: $(grep -o 'EDT [0-9]* ms > 55 -> dereverb -> [0-9]* ms' "$S/6b.log"); gate PASS incl. do_no_harm; stamp verified" \
  || { bad "chain/gate on the excerpt"; tail -3 "$S/6b.log" "$S/6c.log"; }
  # and the stamp must fail once the file changes
  cp "$S/c1650_chain.mp4" "$S/c1650_chain_copy.mp4"; python3 require_stamp.py "$S/c1650_chain_copy.mp4" >/dev/null 2>&1 && bad "an unstamped copy passed require_stamp" || ok "unstamped copy refused"
else echo "  ⚠ SKIPPED: Seagate not mounted"; fi
echo "== 7 do-no-harm: the SETTING DAN REJECTED must FAIL, the one he APPROVED must PASS"
# ⚠ THE POINT OF THIS STEP. On 2026-09-02 the gate PASSED the build Dan later called "underwater",
# because edt / dryness / floor all reward MORE suppression - the gate measured the thing being
# fixed and not the harm being done. Both builds below come from the SAME source through the SAME
# chain; only the dereverb params differ. The rejected one still wins every suppression row
# (EDT ~37 ms against his 40, floor +33 dB) and must be refused anyway.
if [[ -f "$S/c1650_ex.mov" ]]; then
  python3 voice_chain.py --in "$S/c1650_ex.mov" --out "$S/harm_rejected.mp4" --work "$S/_harm" \
      --dereverb "alpha=0.62,d1_ms=20,d2_ms=150,floor_db=-24,smooth=0.30" >"$S/7a.log" 2>&1
  if python3 audio_gate.py "$S/harm_rejected.mp4" --no-stamp >"$S/7b.log" 2>&1; then
    bad "the dereverb Dan rejected PASSED the gate"; else
    grep -q "FAIL  no worse than untreated" "$S/7b.log" \
      && grep -q "PASS  dry room" "$S/7b.log" \
      && ok "rejected dereverb FAILS do_no_harm ($(grep -o 'swirl [0-9.]* vs untreated [0-9.]* (x[0-9.]*)' "$S/7b.log" | head -1)) while still PASSING the dry-room row" \
      || { bad "rejected dereverb failed, but not on do_no_harm"; grep -E "FAIL" "$S/7b.log"; }; fi
  # and a file with no baseline must FAIL, not pass. ⚠ Until 2026-09-09 this row appended
  # ok=True/not_measured=True: recorded, but PASSING -- so "nobody looked" read as "it is fine" to
  # every downstream caller, which is the exact shape of the defect the row exists to stop.
  cp "$S/harm_rejected.mp4" "$S/nobaseline.mp4"; rm -f "$S/nobaseline.mp4.audio_untreated.json"
  if python3 audio_gate.py "$S/nobaseline.mp4" --no-stamp >"$S/7c.log" 2>&1; then
    bad "a file with NO do-no-harm baseline PASSED the gate"
  else
    grep -q "FAIL  do no harm: NOT MEASURED" "$S/7c.log" && ok "a missing baseline FAILS the file, and says why" \
      || { bad "the file failed, but not on an unmeasured do_no_harm"; grep FAIL "$S/7c.log"; }
  fi
  # the row must be gradable against an explicitly supplied baseline too
  python3 audio_gate.py "$S/nobaseline.mp4" --untreated "$S/harm_rejected.mp4.audio_untreated.json" --no-stamp >"$S/7d.log" 2>&1
  grep -q "FAIL  no worse than untreated" "$S/7d.log" && ok "--untreated supplies the baseline for a file that lost its sidecar" \
    || bad "--untreated did not restore the do_no_harm row"
else echo "  ⚠ SKIPPED: step 6 did not produce an excerpt (Seagate not mounted)"; fi
echo "== 8 a --synthetic stamp must not satisfy a camera-audio caller"
# ⚠ require_stamp defaulted to synthetic_ok=True and required an opt-IN --strict that NO SKILL.md
# ever passed, so a weakened 4-row stamp silently satisfied every full-gate caller. Strict is the
# default now; --allow-synthetic is the explicit opt-in for the three AI-voice skills.
if [[ -f "$S/c1650_chain.mp4" ]]; then
  cp "$S/c1650_chain.mp4" "$S/synth.mp4"
  python3 audio_gate.py "$S/synth.mp4" --synthetic >"$S/8a.log" 2>&1
  if python3 require_stamp.py "$S/synth.mp4" >"$S/8b.log" 2>&1; then
    bad "a --synthetic stamp satisfied the default (camera-audio) require_stamp"
  else
    grep -q "synthetic" "$S/8b.log" && ok "a --synthetic stamp is refused by default, naming the reason" \
      || { bad "refused, but not because it is synthetic"; tail -2 "$S/8b.log"; }
  fi
  python3 require_stamp.py "$S/synth.mp4" --allow-synthetic >/dev/null 2>&1 \
    && ok "--allow-synthetic accepts it explicitly (make-ad / exercisegeneration / findassets)" \
    || bad "--allow-synthetic did not accept a valid synthetic stamp"
else echo "  ⚠ SKIPPED: step 6 did not produce a chained file (Seagate not mounted)"; fi
echo; if [[ $fail -eq 0 ]]; then echo "SELFTEST PASS"; else echo "SELFTEST: $fail FAILURE(S)"; exit 1; fi
