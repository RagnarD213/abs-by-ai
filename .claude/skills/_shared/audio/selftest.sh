#!/bin/zsh
# Run before any batch. Proves the module still measures what it claims:
#   1 the gate reads ZERO error on the reference against itself (metric identity)
#   2 the gate PASSES Ad 2 rev 2 (Dan-approved audio, 2026-09-02) and the approved website video rev 2
#     (EDT 75 ms -- the approved side of the room boundary), and FAILS the REJECTED rev 1 on floor + tone
#   3 the gate FAILS a synthetic both-mics-summed render of the same cut (far mic 7.5 ms late,
#     polarity-inverted, with a room tail) -- on the comb and floor rows (its decay reads 56 ms: a synthetic
#     tail is not a real room; the real rejected room measured 85)
#   4 pick_lav picks a:1 on an 8/28 four-track roll, c1 on an 8/3 roll and on the 8/14 ad roll
#     (polarity inverted), and the single live channel on an 8/14 ab-wheel roll (dead left input)
#   5 voice_chain REFUSES a stacked `pan` pull (ffmpeg renders it as silence, not an error)
#   6 voice_chain end-to-end on an 8/28 excerpt (4 tracks, wet room) -> the gate PASSES the output
# Steps 4 and 6 need the Seagate mounted; they are skipped (loudly) if it is not.
set -u
HERE="${0:A:h}"; cd "$HERE"
S="${SELFTEST_DIR:-/tmp/audio_selftest}"; mkdir -p "$S"
REPO="$HERE/../../../.."
P="$REPO/Muhammad Ad Videos/this picture got me abs"
REF="$P/this picture got me abs | muhammad | 16x9.mp4"
AD2="$P/this picture got me abs | claude | 9x16.mp4"
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
echo "== 2 Ad 2 rev 2 must PASS"
python3 audio_gate.py "$AD2" --no-stamp >"$S/2.log" 2>&1 && ok "Ad 2 rev 2 PASS" || { bad "Ad 2 rev 2 did not pass"; grep FAIL "$S/2.log"; }
echo "== 2b the website video: rev 2 (APPROVED, 8/28 room at 75 ms) must PASS; rev 1 (REJECTED on floor) must FAIL"
WV="$REPO/claude edited long form content/06 - Website Conversion Video (post-generation)"
if [[ -f "$WV/website_video_16x9.mp4" ]]; then
  python3 audio_gate.py "$WV/website_video_16x9.mp4" --no-stamp >"$S/2b.log" 2>&1 && ok "website rev 2 (approved) PASS" || { bad "website rev 2 (approved) did not pass"; grep FAIL "$S/2b.log"; }
  if python3 audio_gate.py "$WV/website_video_16x9_REV1_REJECTED.mp4" --no-stamp >"$S/2c.log" 2>&1; then bad "website rev 1 (REJECTED) passed"; else
    grep -q "FAIL  clean between words" "$S/2c.log" && grep -q "FAIL  tone" "$S/2c.log" && ok "website rev 1 (rejected) FAILS on floor + tone ($(grep -c FAIL "$S/2c.log") rows)" || { bad "rev 1 failed, but not on floor/tone"; grep FAIL "$S/2c.log"; }; fi
else echo "  ⚠ SKIPPED: website video not in the project folder"; fi
echo "== 3 summed-both-mics render must FAIL"
python3 - "$AD2" "$S/ad2_summed_mics.wav" <<'EOF'
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
if python3 audio_gate.py "$S/ad2_summed_mics.wav" --video "$AD2" --no-stamp >"$S/3.log" 2>&1; then bad "summed-mics render PASSED the gate"; else
  grep -q "FAIL  no comb" "$S/3.log" && grep -q "FAIL  clean between words" "$S/3.log" && ok "summed-mics render FAILS on comb + floor ($(grep -c FAIL "$S/3.log") rows)" || { bad "summed-mics failed, but not on the comb/floor rows"; grep FAIL "$S/3.log"; }; fi
echo "== 4 pick_lav on every roll type"
if [[ -d "$R828" ]]; then
  expect_lav "$R828/C1650.MP4" "" "" "0:a:1" "pan=mono|c0=c0" "inverted"
  expect_lav "$R803/C1514.MP4" 1492 40 "0:a:0" "pan=mono|c0=c1" "normal"
  expect_lav "$R814/C1591.MP4" "" "" "0:a:0" "pan=mono|c0=c1" "inverted"
  expect_lav "$R814/C1630.MP4" "" "" "0:a:0" "pan=mono|c0=c1" "None single-live"
else echo "  ⚠ SKIPPED: Seagate not mounted"; fi
echo "== 5 stacked pan refused"
if python3 voice_chain.py --in "$AD2" --out "$S/doublepan.wav" --pull "pan=mono|c0=c1,pan=mono|c0=c1" --work "$S/_dp" >"$S/5.log" 2>&1; then bad "double pan was NOT refused"; else grep -q "SILENT" "$S/5.log" && ok "stacked pan refused as silence" || { bad "refused for another reason"; tail -2 "$S/5.log"; }; fi
echo "== 6 chain end-to-end on an 8/28 excerpt"
if [[ -d "$R828" ]]; then
  "$FF" -nostdin -y -v error -ss 40 -t 90 -i "$R828/C1650.MP4" -vn -map 0:a -c:a copy "$S/c1650_ex.mov" \
  && python3 pick_lav.py "$S/c1650_ex.mov" >"$S/6a.log" 2>&1 \
  && python3 voice_chain.py --in "$S/c1650_ex.mov" --out "$S/c1650_chain.mp4" --work "$S/_vc" >"$S/6b.log" 2>&1 \
  && python3 audio_gate.py "$S/c1650_chain.mp4" >"$S/6c.log" 2>&1 \
  && python3 require_stamp.py "$S/c1650_chain.mp4" >/dev/null 2>&1 \
  && ok "excerpt: $(grep -o 'EDT [0-9]* ms > 55 -> dereverb -> [0-9]* ms' "$S/6b.log"); gate PASS; stamp verified" \
  || { bad "chain/gate on the excerpt"; tail -3 "$S/6b.log" "$S/6c.log"; }
  # and the stamp must fail once the file changes
  cp "$S/c1650_chain.mp4" "$S/c1650_chain_copy.mp4"; python3 require_stamp.py "$S/c1650_chain_copy.mp4" >/dev/null 2>&1 && bad "an unstamped copy passed require_stamp" || ok "unstamped copy refused"
else echo "  ⚠ SKIPPED: Seagate not mounted"; fi
echo; if [[ $fail -eq 0 ]]; then echo "SELFTEST PASS"; else echo "SELFTEST: $fail FAILURE(S)"; exit 1; fi
