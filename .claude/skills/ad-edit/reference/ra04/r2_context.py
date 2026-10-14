#!/usr/bin/env python3
"""RA-04 round 2: tip 3 slot preview with the AI frames as labelled stills (motion pending), 0:35.5-0:45.5."""
import subprocess
from PIL import Image, ImageDraw, ImageFont
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
R = "/Volumes/Extreme/_edit_work/ra04/round2"
fr = lambda t: round(t * 30000 / 1001) * 1001 / 30000
SH = [("S1_a", "Shot 1 START", 39.139, 40.26), ("F2_a", "Shot 1 END = Shot 2 START", 40.26, 41.374),
      ("F3b_a", "Shot 2 END", 41.374, 42.509), ("F4b_a", "Shot 3 START", 42.509, 42.976), ("F5b_a", "Shot 3 END", 42.976, 43.4434)]
T0, T1 = 35.5, 45.5
f = ImageFont.truetype(FONT, 44)
for n, lab, a, b in SH:
    im = Image.open(f"{R}/frames/{n}.png").convert("RGB").resize((1080, 1920), Image.LANCZOS); d = ImageDraw.Draw(im)
    for i, t in enumerate(["AI FRAME, MOTION PENDING", lab]):
        w = d.textlength(t, font=f); y = 230 + i * 70
        d.rectangle([540 - w / 2 - 18, y - 8, 540 + w / 2 + 18, y + 56], fill=(10, 30, 60)); d.text((540 - w / 2, y), t, font=f, fill="white")
    im.save(f"{R}/context/{n}_label.png")
ins = ["-ss", f"{T0}", "-t", f"{T1 - T0}", "-i", f"{R}/draft_r2_9x16.mp4"]
fc, last = [], "0:v"
for i, (n, lab, a, b) in enumerate(SH):
    ins += ["-loop", "1", "-framerate", "30000/1001", "-t", f"{T1 - T0}", "-i", f"{R}/context/{n}_label.png"]
    fc.append(f"[{last}][{i + 1}:v]overlay=0:0:enable='between(t,{fr(a) - T0:.4f},{fr(b) - T0 - 0.001:.4f})'[v{i}]"); last = f"v{i}"
fc.append(f"[{last}]scale=540:960[out]")
subprocess.run([FF, "-nostdin", "-y", "-v", "error", *ins, "-filter_complex", ";".join(fc), "-map", "[out]", "-map", "0:a", "-t", f"{T1 - T0}",
                "-c:v", "libx264", "-crf", "22", "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
                f"{R}/context/AI1-tip3-context - REVIEW 540p.mp4"], check=True)
print("CONTEXT_DONE")
