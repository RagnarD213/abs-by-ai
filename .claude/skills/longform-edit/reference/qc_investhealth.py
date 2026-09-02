#!/usr/bin/env python3
"""QC for the invest-health cut.
1. duration vs EDL plan
2. integrated loudness within +/-1 of -14 LUFS
3. splice discontinuity at every join vs in-file controls (>3x = audible pop)
4. transcribe audio around each FLAGGED tight joint and print the text so a
   clipped word / partial fragment is visible (metric: human-readable text)
"""
import json, subprocess, sys, wave, struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = Path(sys.argv[1])
edl = json.load(open(HERE / "edl.json"))
ranges = edl["ranges"]
offs = []; acc = 0.0
for r in ranges:
    offs.append(acc); acc += round(r["end"] - r["start"], 3)
TOTAL = acc
joins = offs[1:]  # output-time positions where two segments meet

import sys as _s; _s.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio")
from require_stamp import require_stamp as _rs
def _stamp_ok(p):
    try: _rs(str(p), quiet=True); return True, 'audio gate stamp present, matches this file, PASS'
    except SystemExit as e: return False, f'audio gate: {e}'
_ok,_m=_stamp_ok(VIDEO); print(f"[{'OK' if _ok else 'FAIL'}] {_m}")
# --- 1. duration
out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", str(VIDEO)], capture_output=True, text=True)
dur = float(out.stdout.strip())
ok = abs(dur - TOTAL) < 1.5
print(f"[{'OK' if ok else 'FAIL'}] duration {dur:.2f}s vs plan {TOTAL:.2f}s (delta {dur-TOTAL:+.2f})")

# --- 2. loudness
proc = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(VIDEO),
                       "-af", "loudnorm=print_format=json", "-vn", "-f", "null", "-"],
                      capture_output=True, text=True)
import re
m = re.search(r'"input_i"\s*:\s*"(-?[\d.]+)"', proc.stderr)
lufs = float(m.group(1)) if m else None
ok = lufs is not None and abs(lufs - (-14.0)) <= 1.0
print(f"[{'OK' if ok else 'FAIL'}] integrated loudness {lufs} LUFS (target -14 +/-1)")

# --- 3. splice discontinuity
wav = HERE / "_qc_audio.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VIDEO), "-vn", "-ac", "1",
                "-ar", "48000", "-c:a", "pcm_s16le", str(wav)], check=True)
wf = wave.open(str(wav), "rb")
sr = wf.getframerate(); n = wf.getnframes()
data = wf.readframes(n); wf.close()
samples = struct.unpack(f"<{n}h", data)

def max_jump(center_s, win=0.004):
    a = max(1, int((center_s - win) * sr)); b = min(n - 1, int((center_s + win) * sr))
    return max(abs(samples[i] - samples[i - 1]) for i in range(a, b))

import random
random.seed(7)
controls = [max_jump(random.uniform(5, TOTAL - 5)) for _ in range(60)]
controls.sort()
ctrl = controls[len(controls) // 2] or 1
worst = 0; worst_j = None; bad = 0
for j in joins:
    if j <= 0.05 or j >= dur - 0.05:
        continue
    r = max_jump(j) / ctrl
    if r > worst:
        worst, worst_j = r, j
    if r > 3.0:
        bad += 1
print(f"[{'OK' if bad == 0 else 'FAIL'}] splice discontinuity: {bad}/{len(joins)} joins >3x control "
      f"(worst {worst:.2f}x at t={worst_j:.1f}s, control median {ctrl})")

# --- 4. flagged-joint listen check: transcribe 6s around each tight joint
FLAGGED_BEATS = ["halo-science", "top10-a", "grind-retake", "longterm-b", "mattress-rent",
                 "recap-sacrifice", "equipment-list", "costco", "clean-eats", "summary-b"]
print("\nflagged joints — transcribed from the FINISHED video (read for clipped words):")
try:
    import whisper
    model = whisper.load_model("small")
except Exception as e:
    model = None
    print("  (whisper unavailable:", e, ")")
name_to_idx = {r["beat"]: i for i, r in enumerate(ranges)}
for beat in FLAGGED_BEATS:
    i = name_to_idx.get(beat)
    if i is None or i + 1 >= len(ranges):
        continue
    j = offs[i] + round(ranges[i]["end"] - ranges[i]["start"], 3)  # join after this beat
    snip = HERE / "_qc_snip.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, j-3):.2f}", "-i", str(VIDEO),
                    "-t", "6", "-vn", "-ac", "1", "-ar", "16000", str(snip)], check=True)
    if model:
        txt = model.transcribe(str(snip), fp16=False, language="en")["text"].strip()
        print(f"  {beat:18s} join@{j:8.2f}s :: {txt}")
print("\nQC done")
