#!/usr/bin/env python3
"""rev5 Step 1 -- airtight pause removal + the new grade, across the WHOLE ad.

Same mechanism as the 60 s sample's tight.py (which this supersedes for the full build):
silence measured from a 5 ms RMS envelope of the real audio, never from Whisper's word
times. Differences:

  * no SPAN cap -- the sample stopped at word 212, this runs to the end of the EDL;
  * env_full.json (265 s) instead of env.json (76 s);
  * the grade is refitted to Muhammad's 2.5-min cut on SKIN pixels (grade25.txt);
  * audio stays the RIGHT channel only -- the roll carries two different microphones.

Target density is his measured 203 wpm (ours ungated is 175 wpm).

Outputs rev5/tight_full.mov + rev5/tight_cuts_full.json (the source->tight time map that
every later graphics/caption pass uses).
"""
import json, subprocess, os

FF   = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
BASE = f"{WORK}/CUT_v2_graded.mp4"
FD   = 1001 / 30000
TAILPAD    = 0.42
SIL_DB     = -40.0
MINSIL     = 0.22
KEEP_TAIL  = 0.055
KEEP_HEAD  = 0.100
MIN_REMOVE = 0.060
HOOK_SAFE  = 2.00
GRADE = open(f"{WORK}/grade25.txt").read().strip()

def frames(t): return round(t / FD)
def snapf(t):  return round(frames(t) * FD, 6)

edl = json.load(open(f"{WORK}/edl.json"))["ranges"]
wh  = json.load(open(f"{WORK}/C1591.whisper.json"))
ws  = [w for s in wh["segments"] for w in s.get("words", [])]
rw, off = [], 0.0
for rg in edl:
    for w in ws:
        if rg["start"] - 0.05 <= w["start"] <= rg["end"]:
            rw.append({"t": round(off + w["start"] - rg["start"], 3),
                       "e": round(off + w["end"] - rg["start"], 3),
                       "w": w["word"]})
    off += rg["end"] - rg["start"]
SPAN_END = round(min(rw[-1]["e"] + TAILPAD, off), 3)

env = json.load(open(f"{WORK}/env_full.json")); HOP = env["hop"]; DB = env["db"]
runs, cur = [], None
for i in range(min(int(SPAN_END / HOP), len(DB))):
    if DB[i] < SIL_DB: cur = (cur[0], i) if cur else (i, i)
    else:
        if cur: runs.append(cur); cur = None
if cur: runs.append(cur)
sil = [(a * HOP, (b + 1) * HOP) for a, b in runs if (b - a + 1) * HOP >= MINSIL]

cuts = []
for s0, s1 in sil:
    prev_w = max((w for w in rw if w["e"] <= s0 + 0.12), key=lambda w: w["e"], default=None)
    next_w = min((w for w in rw if w["t"] >= s1 - 0.02), key=lambda w: w["t"], default=None)
    ci, co = snapf(s0 + KEEP_TAIL), snapf(s1 - KEEP_HEAD)
    if co - ci < MIN_REMOVE: continue
    if ci <= HOOK_SAFE: continue          # never splice inside the opening line
    cuts.append({"in": ci, "out": co, "rm": round(co - ci, 3),
                 "a": prev_w["w"].strip() if prev_w else "?",
                 "b": next_w["w"].strip() if next_w else "?"})

keeps, prev = [], 0.0
for c in cuts:
    keeps.append([round(prev, 6), c["in"]]); prev = c["out"]
keeps.append([round(prev, 6), snapf(SPAN_END)])
keeps = [k for k in keeps if k[1] - k[0] > 0.05]
dur = sum(b - a for a, b in keeps)

print(f"span {SPAN_END:.2f}s -> tight {dur:.2f}s  ({int(dur//60)}:{dur%60:04.1f})")
print(f"{len(cuts)} cuts, {sum(c['rm'] for c in cuts):.1f}s removed")
print(f"density {len(rw)/dur*60:.0f} wpm   (his cut: 203 wpm)")

def to_tight(t):
    acc = 0.0
    for a, b in keeps:
        if t < a:  return round(acc, 3)
        if t <= b: return round(acc + t - a, 3)
        acc += b - a
    return round(acc, 3)

json.dump({"keeps": keeps, "cuts": cuts, "dur": round(dur, 3), "span_end": SPAN_END,
           "grade": GRADE,
           "words": [{"t": to_tight(w["t"]), "e": to_tight(w["e"]), "w": w["w"]} for w in rw]},
          open(f"{HERE}/tight_cuts_full.json", "w"), indent=1)
print("tight_cuts_full.json written")

if os.environ.get("RENDER", "1") == "1":
    parts = [f"[0:a]pan=mono|c0=c1,asplit={len(keeps)}" + "".join(f"[m{i}]" for i in range(len(keeps)))]
    cat = ""
    for i, (a, b) in enumerate(keeps):
        parts.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,setsar=1[v{i}]")
        parts.append(f"[m{i}]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}]")
        cat += f"[v{i}][a{i}]"
    fc = ";".join(parts) + f";{cat}concat=n={len(keeps)}:v=1:a=1[vc][ac];[vc]{GRADE}[vout]"
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", BASE, "-filter_complex", fc,
                    "-map", "[vout]", "-map", "[ac]", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "16", "-pix_fmt", "yuv420p", "-r", "30000/1001",
                    "-c:a", "pcm_s16le", f"{HERE}/tight_full.mov"], check=True)
    print("tight_full.mov written")
