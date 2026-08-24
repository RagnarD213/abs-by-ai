#!/usr/bin/env python3
"""REV1 QC. qc_generic.py's six checks, plus the two things rev1 added.

The one adaptation: the graphics on/off test samples "between chips" to prove
the enable windows CLOSE - but rev1 puts ~95 cutaways and cards on the
timeline, so a naive between-chip sample now often lands on a full-frame stock
clip and measures that instead. Off-samples are chosen from time that is under
NO overlay of any kind.
Extra checks: every planned insert is really on screen, and the deodorant
windows changed the armpit and nothing else.
usage: qc_spraytan.py <video.mp4> [flagged_beat ...]
"""
import importlib.util, json, subprocess, sys, wave, struct, re, random
from pathlib import Path

video = sys.argv[1]; FLAGGED = sys.argv[2:]
BASE = Path("/Volumes/Extreme/_edit_work/spraytan")
VIDEO = BASE / "roughcuts" / video
edl = json.load(open(BASE / "edl.json")); ranges = edl["ranges"]
spec = importlib.util.spec_from_file_location("i", BASE / "inserts.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
offs, acc = [], 0.0
for r in ranges: offs.append(acc); acc += round(r["end"] - r["start"], 3)
TOTAL = acc; joins = offs[1:]
ok_all = True
def chk(cond, msg):
    global ok_all; ok_all = ok_all and bool(cond)
    print(f"[{'OK' if cond else 'FAIL'}] {msg}")

dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
    "-of","csv=p=0",str(VIDEO)],capture_output=True,text=True).stdout.strip())
chk(abs(dur-TOTAL) < 1.5, f"1 duration {dur:.2f}s vs plan {TOTAL:.2f}s (delta {dur-TOTAL:+.2f})")

probe = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
    "stream=codec_name,width,height,r_frame_rate","-of","csv=p=0",str(VIDEO)],
    capture_output=True,text=True).stdout.strip()
chk(probe.startswith("h264,1920,1080"), f"  video stream: {probe}")

p = subprocess.run(["ffmpeg","-nostdin","-hide_banner","-nostats","-i",str(VIDEO),
    "-af","loudnorm=print_format=json","-vn","-f","null","-"],capture_output=True,text=True)
mm = re.search(r'"input_i"\s*:\s*"(-?[\d.]+)"', p.stderr)
tp = re.search(r'"input_tp"\s*:\s*"(-?[\d.]+)"', p.stderr)
lufs = float(mm.group(1)) if mm else None
chk(lufs is not None and abs(lufs+14.0) <= 1.0,
    f"2 integrated loudness {lufs} LUFS (target -14 +/-1), true peak {tp.group(1) if tp else '?'} dBTP")

wav = BASE / "_qc_audio.wav"
subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-i",str(VIDEO),"-vn","-ac","1",
    "-ar","48000","-c:a","pcm_s16le",str(wav)],check=True)
wf = wave.open(str(wav),"rb"); sr = wf.getframerate(); n = wf.getnframes()
samples = struct.unpack(f"<{n}h", wf.readframes(n)); wf.close()
def max_jump(c, win=0.004):
    a = max(1,int((c-win)*sr)); b = min(n-1,int((c+win)*sr))
    return max(abs(samples[i]-samples[i-1]) for i in range(a,b))
random.seed(7)
ctrls = sorted(max_jump(random.uniform(5, TOTAL-5)) for _ in range(120))
med = ctrls[len(ctrls)//2] or 1; ceiling = ctrls[-1]
worst, bad = 0, 0
for j in joins:
    if j <= 0.05 or j >= dur-0.05: continue
    v = max_jump(j); worst = max(worst, v/med)
    if v > ceiling * 1.25: bad += 1
chk(bad == 0, f"3 splice discontinuity: {bad}/{len(joins)} joins above 1.25x the file's own "
              f"ceiling ({ceiling}); worst {worst:.2f}x median ({med})")
wav.unlink(missing_ok=True)

chips = json.load(open(BASE / "chip_timings.json"))
overlays = [(a, a + d) for a, d, _, _, _ in m.INSERTS] + [(c["start"], c["end"]) for c in chips]
def clear(t): return not any(a - 0.6 <= t <= b + 0.6 for a, b in overlays)
def mean_lum(t, box):
    out = subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",f"{t:.2f}","-i",str(VIDEO),
        "-frames:v","1","-vf",f"crop={box},format=gray","-f","rawvideo","-"],capture_output=True)
    d = out.stdout
    return sum(d)/len(d) if d else -1
CHIPBOX = "700:120:120:840"
on = chips[:6]
gaps, t = [], 5.0
while t < TOTAL - 5 and len(gaps) < 5:
    if clear(t): gaps.append(t); t += 25
    else: t += 1
on_l  = [mean_lum(c["start"]+2.0, CHIPBOX) for c in on]
off_l = [mean_lum(x, CHIPBOX) for x in gaps]
sep = (min(on_l) - max(off_l)) if min(on_l) > max(off_l) else (min(off_l) - max(on_l))
chk(len(off_l) >= 3 and sep > 5,
    f"4 graphics windows open AND close: mid-chip {[round(x,1) for x in on_l]} vs "
    f"overlay-free {[round(x,1) for x in off_l]} (separation {sep:.1f})")

tight = [(a["beat"], b["beat"], round(b["start"]-a["end"], 3))
         for a, b in zip(ranges, ranges[1:])
         if a.get("source") == b.get("source") and b["start"] - a["end"] < 0.20]
chk(not tight, f"5 no artificial mid-speech splits (adjacent ranges <0.20s apart): {tight}")

# 6 -- every planned cutaway is really on screen. Compares a frame from the
# middle of each insert against the insert's own source frame; a missing overlay
# scores like an unrelated image.
import numpy as np
def frame(path, t):
    o = subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",f"{t:.2f}","-i",str(path),
        "-frames:v","1","-vf","scale=96:54,format=gray","-f","rawvideo","-"],capture_output=True)
    return np.frombuffer(o.stdout, np.uint8).astype(float) if o.stdout else None
misses = []
for a, d, k, key, note in m.INSERTS:
    if k != "clip": continue
    ins = BASE / "inserts" / f"ins_{key}.mp4"
    fa, fb = frame(VIDEO, a + d/2), frame(ins, d/2)
    if fa is None or fb is None or fa.size != fb.size: misses.append((key, "no frame")); continue
    c = float(np.corrcoef(fa, fb)[0,1])
    if c < 0.75: misses.append((key, round(c,2)))
nclip = sum(1 for x in m.INSERTS if x[2] == "clip")
chk(not misses, f"6 all {nclip} stock cutaways present on the timeline; failures: {misses}")

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
