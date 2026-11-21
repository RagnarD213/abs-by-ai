#!/usr/bin/env python3
"""SL-06 R7: context previews of the five no-face AI intro STILLS (no motion yet). The still, with the AI-GENERATED chip and
the slow push-in the edit will add, plays over the short's real opening line, then the approved round-2 short continues.
Audio is the round-2 short's own. Refuses a still without gate + reviewer PASS.
  python3 preview_r7.py [S..]"""
import os, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/sl06"); sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck")
import batch as Bt
from gate import require_pass
from PIL import Image
R = "/Volumes/Extreme/_edit_work/sl06/round7"; FR = R + "/frames"; OUT = R + "/preview"; FF = Bt.lib.FF
HEAD = {"A": 4.14, "B": 4.61, "C": 2.84, "E": 3.15, "F": 1.94}
CHIP = {"A": (1046, 200, "rt", 2), "B": (1046, 200, "rt", 2), "C": (1046, 200, "rt", 2), "E": (1046, 190, "rt", 2), "F": (1046, 215, "rt", 2)}
PUSH = 0.07                      # 1.00 -> 1.07 over the intro: the camera move the edit will add (Veo itself stays locked)
TAIL = 4.0
os.makedirs(OUT, exist_ok=True)
for S in (sys.argv[1:] or list(HEAD)):
    st = f"{FR}/{S}_r7.jpg"; require_pass(st, st); K = S[0]            # "E2" = a second option for short E
    h = HEAD[K]; n = int(round(h * 30))
    src = f"{R}/../round2/media/{K} - 1080x1920.mp4"
    chip = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); x, y, an, u = CHIP[K]; Bt.B.disclosure(chip, "AI-GENERATED", (x, y), u, anchor=an)
    cp = f"{OUT}/{S}_chip.png"; chip.save(cp)
    fc = (f"[1:v]scale=2160:3840,zoompan=z='1+{PUSH}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps=30,"
          f"setpts=PTS-STARTPTS[z];[z][2:v]overlay=0:0[zc];[0:v][zc]overlay=0:0:enable='lt(t,{h})'[v]")
    subprocess.run([FF, "-v", "error", "-y", "-i", src, "-loop", "1", "-t", f"{h:.3f}", "-i", st, "-loop", "1", "-i", cp,
                    "-t", f"{h + TAIL:.3f}", "-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "20",
                    "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-frames:v", str(int((h + TAIL) * 30)),
                    f"{OUT}/{S}_preview.mp4"], check=True)
    print("preview", S, f"{OUT}/{S}_preview.mp4")
