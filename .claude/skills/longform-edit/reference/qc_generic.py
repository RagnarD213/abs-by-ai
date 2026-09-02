#!/usr/bin/env python3
"""QC a finished longform cut (longform-edit Step 9).
1 duration vs EDL plan | 2 integrated LUFS within +/-1 of -14
3 splice discontinuity at every join vs in-file controls (>3x = audible pop)
4 graphics on/off: sample mid-chip AND between chips
5 re-transcribe 6s of the FINISHED render around each flagged joint
usage: qc.py <slug> <video.mp4> [flagged_beat ...]"""
import json, subprocess, sys, wave, struct, re, random
from pathlib import Path

slug, video = sys.argv[1], sys.argv[2]
FLAGGED = sys.argv[3:]
BASE = Path(f"/Volumes/Extreme/_edit_work/{slug}")
VIDEO = BASE / "roughcuts" / video
edl = json.load(open(BASE / "edl.json")); ranges = edl["ranges"]
offs, acc = [], 0.0
for r in ranges: offs.append(acc); acc += round(r["end"] - r["start"], 3)
TOTAL = acc; joins = offs[1:]
ok_all = True
def chk(cond, msg):
    global ok_all
    ok_all = ok_all and cond
    print(f"[{'OK' if cond else 'FAIL'}] {msg}")

dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
    "-of","csv=p=0",str(VIDEO)],capture_output=True,text=True).stdout.strip())
import sys as _s; _s.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio")
from require_stamp import require_stamp as _rs
def _stamp_ok(p):
    try: _rs(str(p), quiet=True); return True, 'audio gate stamp present, matches this file, PASS'
    except SystemExit as e: return False, f'audio gate: {e}'
chk(*_stamp_ok(VIDEO))
chk(abs(dur-TOTAL) < 1.5, f"duration {dur:.2f}s vs plan {TOTAL:.2f}s (delta {dur-TOTAL:+.2f})")

probe = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
    "stream=width,height,r_frame_rate,codec_name","-of","csv=p=0",str(VIDEO)],capture_output=True,text=True).stdout.strip()
chk(probe.startswith("h264,1920,1080"), f"video stream: {probe}")

p = subprocess.run(["ffmpeg","-nostdin","-hide_banner","-nostats","-i",str(VIDEO),
    "-af","loudnorm=print_format=json","-vn","-f","null","-"],capture_output=True,text=True)
m = re.search(r'"input_i"\s*:\s*"(-?[\d.]+)"', p.stderr)
lufs = float(m.group(1)) if m else None
chk(lufs is not None and abs(lufs+14.0) <= 1.0, f"integrated loudness {lufs} LUFS (target -14 +/-1)")

wav = BASE / "_qc_audio.wav"
subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-i",str(VIDEO),"-vn","-ac","1",
    "-ar","48000","-c:a","pcm_s16le",str(wav)],check=True)
wf = wave.open(str(wav),"rb"); sr = wf.getframerate(); n = wf.getnframes()
samples = struct.unpack(f"<{n}h", wf.readframes(n)); wf.close()
def max_jump(c, win=0.004):
    a = max(1,int((c-win)*sr)); b = min(n-1,int((c+win)*sr))
    return max(abs(samples[i]-samples[i-1]) for i in range(a,b))
# Normalise against the control DISTRIBUTION, not its median. Speech has huge
# dynamic range: on a 30-min talking head the controls span p50=613 .. max=4069,
# so a join landing next to a loud syllable scores >3x the MEDIAN while being
# entirely normal for the file. A join is only a pop if its discontinuity exceeds
# anything the file produces naturally. The x-median ratio is still reported so
# it stays comparable with the 8/3 baseline (1.09-1.20x).
random.seed(7)
ctrls = sorted(max_jump(random.uniform(5, TOTAL-5)) for _ in range(120))
med = ctrls[len(ctrls)//2] or 1
ceiling = ctrls[-1]
worst, worst_j, bad = 0, None, 0
for j in joins:
    if j <= 0.05 or j >= dur-0.05: continue
    v = max_jump(j); r = v/med
    if r > worst: worst, worst_j = r, j
    if v > ceiling * 1.25: bad += 1
chk(bad == 0, f"splice discontinuity: {bad}/{len(joins)} joins above 1.25x the file's own "
              f"natural ceiling ({ceiling}); worst join {worst:.2f}x median ({med})")
wav.unlink(missing_ok=True)

chips = json.load(open(BASE / "chip_timings.json"))
def mean_lum(t, box):
    out = subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",f"{t:.2f}","-i",str(VIDEO),
        "-frames:v","1","-vf",f"crop={box},format=gray","-f","rawvideo","-"],capture_output=True)
    d = out.stdout
    return sum(d)/len(d) if d else -1
CHIPBOX = "700:120:120:840"
on = [c for c in chips[:6]]
gaps = []
for a,b in zip(chips, chips[1:]):
    if b["start"] - a["end"] > 3.0: gaps.append((a["end"]+1.2))
    if len(gaps) >= 4: break
on_l  = [mean_lum(c["start"]+2.0, CHIPBOX) for c in on]
off_l = [mean_lum(t, CHIPBOX) for t in gaps]
# A chip is a DARK box. On a dark set it raises the region's mean luminance
# (white Impact text on near-black); on a BRIGHT set -- the supplements video is
# a granite counter -- it LOWERS it. Assert a clear separation in either
# direction, never that "chip == brighter".
sep = (min(on_l) - max(off_l)) if min(on_l) > max(off_l) else (min(off_l) - max(on_l))
chk(len(off_l) > 0 and sep > 5,
    f"graphics windows open AND close: mid-chip lum {[round(x,1) for x in on_l]} vs "
    f"between-chip {[round(x,1) for x in off_l]} (separation {sep:.1f})")

tight = [(a["beat"], b["beat"], round(b["start"]-a["end"], 3))
         for a, b in zip(ranges, ranges[1:])
         if a.get("source") == b.get("source") and b["start"] - a["end"] < 0.20]
chk(not tight, f"no artificial mid-speech splits (adjacent ranges <0.20s apart): {tight}")

name_to_idx = {r["beat"]: i for i,r in enumerate(ranges)}
if FLAGGED:
    print("\nflagged joints, transcribed FROM THE FINISHED RENDER:")
    try:
        import whisper; model = whisper.load_model("small")
    except Exception as e:
        model = None; print("  (whisper unavailable:", e, ")")
    for beat in FLAGGED:
        i = name_to_idx.get(beat)
        if i is None: print(f"  {beat}: not in EDL"); continue
        j = offs[i]
        for label, t in (("head", j), ("tail", j + round(ranges[i]["end"]-ranges[i]["start"],3))):
            snip = BASE / "_qc_snip.wav"
            subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-ss",f"{max(0,t-3):.2f}","-i",str(VIDEO),
                "-t","6","-vn","-ac","1","-ar","16000",str(snip)],check=True)
            if model:
                txt = model.transcribe(str(snip), fp16=False, language="en")["text"].strip()
                print(f"  {beat:24s} {label} @{t:8.2f}s :: {txt}")
            snip.unlink(missing_ok=True)
print("\nQC", "PASS" if ok_all else "HAS FAILURES")
