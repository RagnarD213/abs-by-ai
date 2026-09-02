#!/usr/bin/env python3
"""Final delivery gate for a cut-down variant.

Replaces the two QC checks that proved to be wrong metrics, and upgrades the
clipped-word check from a noisy word-presence test to a measured one:

  * CLIPPED WORDS - for EVERY new joint, cross-correlate the render's energy
    envelope against the SOURCE (removing the render's accumulated frame-rounding
    drift, ~1 s by mid-file) and compare the last 150 ms. Score against joints
    INHERITED from the approved v3 edit in the SAME file, which carry the same
    encoder, loudnorm and 30 ms render.py fade. Fail only below the control floor.
    Word-presence alone is not evidence: Whisper re-spells the last word of a
    phrase whenever the phrase after it changed (proteins->protein).
  * CHIPS - difference of differences (chip box minus a chip-free control box in
    the same frame, chip-up frame vs chip-down frame). A raw luminance test is
    unusable here: a J2 chip RAISES luminance over the dark doorway and LOWERS it
    over a bright frame, and an olive-pixel test matches the olive door panel.
    Also writes an on/off strip for every chip, which is the real proof.
  * SRT - 48-character ceiling, now that the wrap is midpoint-balanced and the
    cue cap leaves headroom for the brand substitutions.

Usage: python3 final_gate.py cons|sub30
"""
import json, math, struct, subprocess, sys, wave, random
from pathlib import Path
import PIL.Image as I

HERE = Path(__file__).resolve().parent
SRCWAV = Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/"
              "Media/longform-raw/absbyai-0803-shoot/invest-health/C1511.wav")
V = sys.argv[1]
NAME = "INVEST_HEALTH_conservative" if V == "cons" else "INVEST_HEALTH_sub30"
D = HERE / V
VID = D / "out" / f"{NAME}.mp4"
SRT = D / "out" / f"{NAME}.srt"
edl = json.load(open(D / "edl.json"))["ranges"]
newj = json.load(open(D / "new_joints.json"))["joints"]
newset = {j["i"] for j in newj}
offs, acc = [], 0.0
for r in edl:
    offs.append(acc); acc += round(r["end"] - r["start"], 3)

fails = []
def check(ok, msg):
    print(f"[{'OK' if ok else 'FAIL'}] {msg}")
    if not ok: fails.append(msg)
import sys as _s; _s.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio")
from require_stamp import require_stamp as _rs
def _stamp_ok(p):
    try: _rs(str(p), quiet=True); return True, 'audio gate stamp present, matches this file, PASS'
    except SystemExit as e: return False, f'audio gate: {e}'
check(*_stamp_ok(VID))

def env(src, a, dur, step=0.010):
    p = Path(f"/tmp/_fg_{V}.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-i", str(src),
                    "-t", f"{dur:.3f}", "-vn", "-ac", "1", "-ar", "48000",
                    "-c:a", "pcm_s16le", str(p)], check=True)
    w = wave.open(str(p)); n = w.getnframes()
    sm = struct.unpack(f"<{n}h", w.readframes(n)); w.close()
    st = int(step * 48000)
    return [20*math.log10((sum(x*x for x in sm[i:i+st])/st)**0.5/32768 + 1e-9)
            for i in range(0, n - st, st)]
def demean(v):
    m = sum(v)/len(v); return [x-m for x in v]
def tail_dev(src_out, out_t):
    S = demean(env(SRCWAV, src_out - 1.60, 1.60))
    R = demean(env(VID, max(0.0, out_t - 4.2), 6.8))
    best, lag0 = None, 0
    for lag in range(0, len(R) - len(S)):
        c = sum(a*b for a, b in zip(S, R[lag:lag+len(S)]))
        if best is None or c > best: best, lag0 = c, lag
    return min(r - s for r, s in zip(R[lag0+len(S)-15:lag0+len(S)], S[-15:]))

print(f"=== FINAL GATE {V}: {NAME} ===")
# ---- control distribution from joints Dan already approved ----
inherited = [i for i in range(len(edl)-1) if (i+1) not in newset]
random.seed(5)
ctrl = sorted(tail_dev(edl[i]["end"], offs[i+1])
              for i in random.sample(inherited, min(20, len(inherited))))
floor = ctrl[0]
print(f"control: {len(ctrl)} inherited v3-approved joints, "
      f"{ctrl[0]:+.1f} .. {ctrl[-1]:+.1f} dB (median {ctrl[len(ctrl)//2]:+.1f})")

clipped = []
for j in newj:
    i = j["i"]
    d = tail_dev(edl[i-1]["end"], offs[i])
    if d < floor - 3:
        clipped.append((j["out_t"], j["beats"], round(d, 1)))
check(not clipped, f"clipped words: {len(clipped)} of {len(newj)} new joints below the "
                   f"control floor {floor:.1f} dB {clipped[:5]}")

# ---- chips ----
CHIP_BOX, CTRL_BOX = (120, 796, 620, 920), (1240, 796, 1740, 920)
def frame(t, out=None):
    p = Path(out or f"/tmp/_fg_{V}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(VID),
                    "-frames:v", "1", str(p)], check=True)
    return I.open(p).convert("L")
def contrast(t):
    im = frame(t); a = im.crop(CHIP_BOX); b = im.crop(CTRL_BOX)
    return sum(a.getdata())/(a.width*a.height) - sum(b.getdata())/(b.width*b.height)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", str(VID)], capture_output=True,
                           text=True).stdout.strip())
chips = json.load(open(D / "chip_timings.json"))
STRIP = D / "_qc_chips"; STRIP.mkdir(exist_ok=True)
deltas = []
for c in chips:
    on_t, off_t = c["start"] + 2.0, c["end"] + 1.5
    if on_t > dur - 1 or off_t > dur - 1: continue
    deltas.append((c["key"], round(contrast(on_t) - contrast(off_t), 1)))
    for tag, t in (("on", on_t), ("off", off_t)):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(VID),
                        "-frames:v", "1", "-vf", "crop=900:180:60:770,scale=600:-1",
                        str(STRIP / f"{c['key']}_{tag}.png")], check=True)
strong = [k for k, v in deltas if abs(v) > 8]
check(len(strong) >= 0.8 * len(deltas),
      f"chips: {len(strong)}/{len(deltas)} show a clear on/off change "
      f"(range {min(v for _k,v in deltas):+.0f}..{max(v for _k,v in deltas):+.0f}); "
      f"on/off strips in {STRIP.name}/ are the visual proof")

# ---- SRT ----
body = SRT.read_text()
cues = body.strip().split("\n\n")
lines = [l for c in cues for l in c.split("\n")[2:]]
check("GOP" not in body, f"SRT 'GOP' count {body.count('GOP')}")
for pat in ("Terzepetide", "Tersepityde", "reditrutide", "osepic", "Aura ring"):
    check(pat not in body, f"SRT unfixed spelling {pat!r}")
check(max(map(len, lines)) <= 48, f"SRT longest caption line {max(map(len, lines))} chars")
check(not [c for c in cues if len(c.split("\n")) > 4], "SRT has no 3-line cues")
print(f"    {len(cues)} cues, longest line {max(map(len, lines))} chars")

print("\n" + (f"FINAL GATE {V} PASSED" if not fails
              else f"FINAL GATE {V} FAILURES: " + "; ".join(fails)))
