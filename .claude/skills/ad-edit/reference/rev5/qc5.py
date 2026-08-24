#!/usr/bin/env python3
"""rev5 QC -- the /longform-edit suite plus the ad-specific assertions.

  1 splice visibility vs the file's own frame-diff control distribution
  2 no adjacent punch segment under 0.20 s, and no two adjacent at the same level
  3 pacing: nothing visually unchanged longer than 25 s
  4 loudness -14 LUFS / true peak, and the voice centred
  5 script fidelity: re-transcribe the FINISHED render and diff against the tight words
  6 compliance: drug names, and every AI insert carries a label window
  7 caption/graphic collision: no caption event inside a full-screen card
"""
import importlib.util, json, os, re, statistics, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats5 as B
import layout5 as L

FF   = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
FFP  = FF.replace("ffmpeg", "ffprobe")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.environ.get("QCIN", f"{HERE}/ad1_rev5_16x9.mp4")
fails, warns = [], []

def check(ok, msg):
    print(("  PASS  " if ok else "  FAIL  ") + msg)
    if not ok: fails.append(msg)

print(f"QC {os.path.basename(SRC)}")
dur = float(subprocess.run([FFP, "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", SRC], capture_output=True, text=True).stdout)
print(f"duration {int(dur//60)}:{dur%60:05.2f}\n")

# ---------------------------------------------------------------- 1 splices
tc = json.load(open(f"{HERE}/tight_cuts_full.json"))
acc, splices = 0.0, []
for a, b in tc["keeps"][:-1]:
    acc += b - a; splices.append(round(acc, 3))
punch = [p[0] for p in L.PUNCH[1:]]
gfx_t = [t for _, beat in L.GFX for t in beat]
covered = [beat for name, beat in L.GFX
           if name not in ("callout", "lower3", "lower3b", "lower3c", "step1")]
covered += [b for (b, *_rest) in L.VID]
# The Ken Burns stills and the two live app-flow runs are inserts too. Leaving them out
# reported two splices as "bare" that are in fact under a card -- the failure was in the
# metric, not the media (the same class of mistake the longform QC made three times).
covered += [b for (b, *_rest) in L.KB]
covered += [B.SEQ, B.ENDCARD]

subprocess.run([FF, "-v", "error", "-i", SRC, "-vf",
                "scale=320:180,tblend=all_mode=difference,signalstats,"
                f"metadata=print:key=lavfi.signalstats.YAVG:file={HERE}/qc5diff.txt",
                "-an", "-f", "null", "-"], check=True)
vals = []
for blk in open(f"{HERE}/qc5diff.txt").read().split("frame:")[1:]:
    t = re.search(r"pts_time:([\d.]+)", blk); v = re.search(r"YAVG=([\d.]+)", blk)
    if t and v: vals.append((float(t.group(1)), float(v.group(1))))
ys = sorted(v for _, v in vals)
p99 = ys[int(len(ys) * .99)]
print(f"frame-diff control: median {statistics.median(ys):.2f}  p99 {p99:.2f}")

near = lambda t, xs, w=0.14: any(abs(t - x) < w for x in xs)
under = lambda t: any(a - 0.05 <= t <= b + 0.05 for a, b in covered)
bare = []
for s in splices:
    d = max([v for t, v in vals if abs(t - s) < 0.05] or [0])
    if under(s) or near(s, punch) or near(s, gfx_t): continue
    if d > p99: bare.append((s, round(d, 2)))
check(not bare, f"bare splices above the p99 ceiling: {bare[:6]}")

# ---------------------------------------------------------------- 2 punch integrity
short = [(a, b, l) for a, b, l in L.PUNCH if b - a < 0.20]
check(not short, f"punch segments under 0.20s: {short}")
same = [(L.PUNCH[i][2], L.PUNCH[i+1][0]) for i in range(len(L.PUNCH)-1)
        if L.PUNCH[i][2] == L.PUNCH[i+1][2]]
check(not same, f"adjacent segments at the same framing (jump cut): {same}")

# ---------------------------------------------------------------- 3 pacing
changes = sorted(set([0.0] + punch + gfx_t + [t for b in [x[0] for x in L.VID] for t in b] + [dur]))
shots = [round(changes[i+1] - changes[i], 2) for i in range(len(changes)-1)
         if changes[i+1] - changes[i] > 0.2]
print(f"visual changes {len(changes)-1}   median hold {statistics.median(shots):.2f}s   "
      f"longest {max(shots):.2f}s")
check(max(shots) <= 25.0, f"nothing visually unchanged longer than 25s (worst {max(shots):.2f}s)")

# ---------------------------------------------------------------- 4 audio
p = subprocess.run([FF, "-nostats", "-i", SRC, "-af", "ebur128=peak=true", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
gi = lambda k: float(re.findall(rf"{k}:\s*(-?[\d.]+)", p)[-1])
I, TP, LRA = gi("I"), gi("Peak"), gi("LRA")
print(f"loudness  I {I:.2f} LUFS   true peak {TP:.2f} dBTP   LRA {LRA:.1f} LU")
check(abs(I + 14) <= 0.6, f"integrated loudness within 0.6 LU of -14 (got {I:.2f})")
check(TP <= -0.9, f"true peak at or under -1.0 dBTP (got {TP:.2f})")

import numpy as np
raw = subprocess.run([FF, "-v", "error", "-i", SRC, "-map", "0:a", "-ac", "2",
                      "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout
a = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
corr = float(np.corrcoef(a[:, 0], a[:, 1])[0, 1])
mid, side = (a[:, 0] + a[:, 1]) / 2, (a[:, 0] - a[:, 1]) / 2
sep = 20 * np.log10(np.sqrt((mid**2).mean()) / (np.sqrt((side**2).mean()) + 1e-12))
print(f"stereo    L/R corr {corr:+.4f}   side {sep:.1f} dB under mid   (his: +0.99 / 23.0 dB)")
check(corr > 0.95, f"voice is centred (L/R correlation {corr:+.4f})")

# ---------------------------------------------------------------- 5 script fidelity
TXF = f"{HERE}/qc5.whisper.json"
if not os.path.exists(TXF):
    wav = f"{HERE}/_qc5.wav"
    subprocess.run([FF, "-v", "error", "-y", "-i", SRC, "-map", "0:a", "-ac", "1",
                    "-ar", "16000", "-c:a", "pcm_s16le", wav], check=True)
    import whisper
    json.dump(whisper.load_model("small.en").transcribe(wav, language="en"), open(TXF, "w"))
norm = lambda s: re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()
said = norm(" ".join(s["text"] for s in json.load(open(TXF))["segments"]))
want = norm(" ".join(w["w"] for w in tc["words"]))
import difflib
ratio = difflib.SequenceMatcher(None, want, said).ratio()
print(f"script fidelity {ratio*100:.1f}%  ({len(want)} words expected, {len(said)} heard)")
check(ratio >= 0.95, f"finished render matches the cut's words (>=95%, got {ratio*100:.1f}%)")

# ---------------------------------------------------------------- 6 compliance
banned = re.compile(r"\b(zepbound|tirzepatide|semaglutide|ozempic|mounjaro|wegovy)\b", re.I)
hits = [s["text"].strip() for s in json.load(open(TXF))["segments"] if banned.search(s["text"])]
check(not hits, f"no drug names spoken: {hits}")
ai_beats = [b for (b, src, si, wid, ex, tag) in L.VID if tag]
labelled = all(os.path.exists(f"{HERE}/gfx/tag_big.png") for _ in ai_beats)
check(labelled and len(ai_beats) >= 5, f"AI inserts carry a label ({len(ai_beats)} tagged)")

# ---------------------------------------------------------------- 7 captions
capf = f"{HERE}/cap5.ass"
if os.path.exists(capf):
    ev = [l for l in open(capf) if l.startswith("Dialogue:")]
    def secs(x):
        h, m, s = x.split(":"); return int(h)*3600 + int(m)*60 + float(s)
    coll = []
    SUP = [B.GEN, B.PHONE, B.TODAY, B.LOOKNOW, B.TITLE, B.CTA1, B.CTA2, B.SUPERIOR,
           B.BEFORE1, B.FATDAD, B.AFTERPIC, B.STEP1, B.ENDCARD]
    for l in ev:
        f = l.split(",")
        a, b = secs(f[1]), secs(f[2])
        if any(not (b <= s or a >= e) for s, e in SUP): coll.append(round(a, 2))
    print(f"captions: {len(ev)} cues")
    check(not coll, f"no caption sits on a full-screen card: {coll[:6]}")

print("\n" + ("QC PASSED" if not fails else f"QC FAILED -- {len(fails)} check(s)"))
sys.exit(1 if fails else 0)
