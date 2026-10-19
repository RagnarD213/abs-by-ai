#!/usr/bin/env python3
"""SL-06 R3 stage 1: context previews of the six AI flex intros as STILLS (no motion yet). The START frame for the first
half of the opening line, the END frame for the second half, the AI-GENERATED chip, then the round-2 short continues
(title band back on its first film frame). Audio is the round-2 short's own. Pages refuse pairs that fail require_pass.
  python3 preview_intros.py [S..]"""
import json, os, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/sl06"); sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck")
import batch as Bt
from gate import require_pass
from PIL import Image
R = "/Volumes/Extreme/_edit_work/sl06/round3"; AI = R + "/aiframes"; OUT = R + "/preview"; FF = Bt.lib.FF
HEAD = {"A": 4.14, "B": 4.61, "C": 2.84, "D": 3.28, "E": 3.15, "F": 2.50}
CHIP = {"A": (1046, 200, "rt", 2), "B": (1046, 200, "rt", 2), "C": (1046, 200, "rt", 2), "D": (540, 96, "mt", 1.75), "E": (1046, 190, "rt", 2), "F": (1046, 215, "rt", 2)}   # clear wall, off face, body and poster (checked on the frame)
TAIL = 4.0
def still(S, k):
    im = Image.open(f"{AI}/{S}_{k}.jpg").convert("RGB")
    x, y, an, u = CHIP[S]; Bt.B.disclosure(im, "AI-GENERATED", (x, y), u, anchor=an)
    p = f"{OUT}/{S}_{k}_chip.png"; im.save(p); return p
for S in (sys.argv[1:] or list(HEAD)):
    require_pass(f"{AI}/{S}_start.jpg", f"{AI}/{S}_end.jpg")
    st, en = still(S, "start"), still(S, "end"); h = HEAD[S]; m = round(h / 2, 3)
    src = f"{R}/../round2/media/{S} - 1080x1920.mp4"
    subprocess.run([FF, "-v", "error", "-y", "-i", src, "-loop", "1", "-i", st, "-loop", "1", "-i", en, "-t", f"{h + TAIL:.3f}",
                    "-filter_complex", f"[0:v][1:v]overlay=0:0:enable='lt(t,{m})'[a];[a][2:v]overlay=0:0:enable='between(t,{m},{h})'[v]",
                    "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    f"{OUT}/{S}_intro_context.mp4"], check=True)
    print(S, "ok", h)
