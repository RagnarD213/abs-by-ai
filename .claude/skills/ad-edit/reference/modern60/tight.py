#!/usr/bin/env python3
"""Modern-edit 60s sample — Step 1: airtight pause removal + brighter grade.

Cuts every silence run >= MINSIL out of the sample span, leaving a small breath, so
the delivery matches the reference edit's density. NO speed-up: every kept word plays
at 1.0x with its original word-level timing.

Silence is measured from a 5 ms RMS envelope of the real audio, never from Whisper's
word end times (those run early on decays and late on soft onsets).

Outputs tight60.mp4 (+ tight_cuts.json for QC and for the graphics layout to map time).
"""
import json, subprocess, math

FF   = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
BASE = "CUT_v2_graded.mp4"
FPS  = 30000 / 1001
FD   = 1001 / 30000                    # frame duration
SPAN_LAST_WORD = 212                   # "...stare at it every day."
TAILPAD  = 0.42                        # let the last word ring out
SIL_DB   = -40.0                       # below this = room tone (floor is ~-50)
MINSIL   = 0.22                        # only compress silences at least this long
KEEP_TAIL = 0.055                      # room tone kept after the outgoing word
KEEP_HEAD = 0.100                      # kept before the incoming word (protects soft onsets)
MIN_REMOVE = 0.060                     # don't bother with cuts smaller than this
HOOK_SAFE  = 2.00                      # no splice at all inside the opening line
# talking-head lift: shadows/mids up ~20% to match the reference's brightness
GRADE = ("curves=all='0/0.015 0.20/0.262 0.40/0.472 0.70/0.762 1/1',"
         "eq=saturation=1.05:contrast=1.02")

def frames(t):  return round(t / FD)
def snapf(t):   return round(frames(t) * FD, 6)

edl = json.load(open("edl.json"))["ranges"]
wh  = json.load(open("C1591.whisper.json"))
ws  = [w for s in wh["segments"] for w in s.get("words", [])]
rw, off = [], 0.0
for rg in edl:
    for w in ws:
        if rg["start"] - 0.05 <= w["start"] <= rg["end"]:
            rw.append({"t": round(off + w["start"] - rg["start"], 3),
                       "e": round(off + w["end"] - rg["start"], 3),
                       "w": w["word"]})
    off += rg["end"] - rg["start"]
SPAN_END = round(rw[SPAN_LAST_WORD]["e"] + TAILPAD, 3)

env = json.load(open("env.json")); HOP = env["hop"]; DB = env["db"]
runs, cur = [], None
for i in range(int(SPAN_END / HOP)):
    if DB[i] < SIL_DB: cur = (cur[0], i) if cur else (i, i)
    else:
        if cur: runs.append(cur); cur = None
if cur: runs.append(cur)
sil = [(a * HOP, (b + 1) * HOP) for a, b in runs if (b - a + 1) * HOP >= MINSIL]

cuts = []
for s0, s1 in sil:
    # Placement comes from the ENVELOPE only. Whisper's word starts are unreliable in
    # exactly these spots -- it timestamps "I" 0.4s before any audio exists, and starts
    # "Fitness" before its /f/ -- so clamping to them either eats onsets or blocks the cut.
    # KEEP_HEAD carries the safety margin; the re-transcription QC is the real check.
    prev_w = max((w for w in rw if w["e"] <= s0 + 0.12), key=lambda w: w["e"], default=None)
    next_w = min((w for w in rw if w["t"] >= s1 - 0.02), key=lambda w: w["t"], default=None)
    ci, co = snapf(s0 + KEEP_TAIL), snapf(s1 - KEEP_HEAD)
    if co - ci < MIN_REMOVE: continue
    # The hook is the money zone and it carries a static callout graphic; a micro-jump
    # under a fixed overlay reads as a glitch rather than as an edit.
    if ci <= HOOK_SAFE: continue
    cuts.append({"in": ci, "out": co, "rm": round(co - ci, 3),
                 "a": prev_w["w"].strip() if prev_w else "?",
                 "b": next_w["w"].strip() if next_w else "?"})

keeps, prev = [], 0.0
for c in cuts:
    keeps.append([round(prev, 6), c["in"]]); prev = c["out"]
keeps.append([round(prev, 6), snapf(SPAN_END)])
keeps = [k for k in keeps if k[1] - k[0] > 0.05]
dur = sum(b - a for a, b in keeps)
words_in_span = SPAN_LAST_WORD + 1

print(f"span {SPAN_END:.2f}s -> tight {dur:.2f}s   {len(cuts)} cuts, {sum(c['rm'] for c in cuts):.2f}s removed")
print(f"density {words_in_span / dur * 60:.0f} wpm (reference edit: 206 wpm)")
for c in cuts:
    print(f"   {c['in']:6.2f} -> {c['out']:6.2f}  -{c['rm']:.2f}s   '{c['a']}' | '{c['b']}'")

# render-time map: source(cut) seconds -> tight seconds
def to_tight(t):
    acc = 0.0
    for a, b in keeps:
        if t < a:  return round(acc, 3)
        if t <= b: return round(acc + t - a, 3)
        acc += b - a
    return round(acc, 3)

json.dump({"keeps": keeps, "cuts": cuts, "dur": round(dur, 3), "span_end": SPAN_END,
           "words": [{"t": to_tight(w["t"]), "e": to_tight(w["e"]), "w": w["w"]}
                     for w in rw[:words_in_span]]},
          open("tight_cuts.json", "w"), indent=1)

parts, cat = [], ""
for i, (a, b) in enumerate(keeps):
    parts.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,setsar=1[v{i}]")
    parts.append(f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}]")
    cat += f"[v{i}][a{i}]"
fc = ";".join(parts) + f";{cat}concat=n={len(keeps)}:v=1:a=1[vc][ac];[vc]{GRADE}[vout]"
subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", BASE, "-filter_complex", fc,
                "-map", "[vout]", "-map", "[ac]", "-c:v", "libx264", "-preset", "slow",
                "-crf", "16", "-pix_fmt", "yuv420p", "-r", "30000/1001",
                "-c:a", "pcm_s16le", "tight60.mov"], check=True)
print("tight60.mov written")
