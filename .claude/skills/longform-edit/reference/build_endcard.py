#!/usr/bin/env python3
"""The end card: a real app screen, not a text box.

The delivered cut ended on a static text box. The reference edit ends on the product,
and so does every ad we ship. This puts the actual absbyai.com generation flow in a
phone-shaped window on the brand field, with the URL beside it.

The app recording is used from 3.0 s only. From 25.25 s it reaches the "Meet the new
you" BEFORE/AFTER screen and then an email-capture screen: Dan's standing rule is no
side-by-side before/after on screen in ANY video, and email capture is never shown.
"""
import os, subprocess, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
os.environ["MOTIONLIB_FFMPEG"] = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
from PIL import Image, ImageDraw
import motionlib as M
import spec

FF = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
P  = M.MIL
G  = [g for g in spec.G if g[2] == "endcard"][0]
START, DUR, _, KEY, PL = G
APP, APP_SS = spec.OWN["app_flow"]
PHONE = [1216, 118, 1616, 962]        # 400 x 844, an iPhone aspect
IDX = [i for i, ins in enumerate(spec.INSERTS)][-1] + 1

def overlay():
    """Alpha layer: brand field with a phone-shaped hole, plus the CTA type."""
    fH = M.font(112, "ExtraBold"); fS = M.font(44, "Bold"); fT = M.font(30, "ExtraBold")
    base = Image.new("RGBA", (M.W, M.H), P.field + (255,))
    M.bracket_frame(base, P)
    d = ImageDraw.Draw(base)
    x = 140
    d.text((x, 372), "ABSBYAI", font=fH, fill=(255, 255, 255), anchor="lt")
    w0 = M.text_size("ABSBYAI", fH)[0]
    d.text((x + w0, 372), ".COM", font=fH, fill=P.accent, anchor="lt")
    d.rectangle([x, 372 + M.ink_bottom("ABSBYAI", fH) + 26, x + w0 + 120,
                 372 + M.ink_bottom("ABSBYAI", fH) + 36], fill=P.mid)
    d.text((x, 372 + M.ink_bottom("ABSBYAI", fH) + 74), PL["sub"].upper(), font=fS,
           fill=P.ink_soft, anchor="lt")
    M.chip(base, (x, 300), "FREE AI PREVIEW", fT, P.mid + (255,), (255, 255, 255, 255), radius=6)
    hole = Image.new("L", (M.W, M.H), 255)
    ImageDraw.Draw(hole).rounded_rectangle(PHONE, radius=42, fill=0)
    base.putalpha(Image.composite(base.getchannel("A"), Image.new("L", (M.W, M.H), 0), hole))
    ImageDraw.Draw(base).rounded_rectangle(PHONE, radius=42, outline=P.accent + (255,), width=4)
    p = "gfx/_end_overlay.png"; base.save(p); return p

if __name__ == "__main__":
    ov = overlay()
    ph_w, ph_h = PHONE[2] - PHONE[0], PHONE[3] - PHONE[1]
    # the recording is 1320x2868 (0.4603) and the phone window is 0.4739 -- scaling to
    # the window HEIGHT leaves it 12 px too narrow, so cover-scale and crop the excess
    # height instead, which loses a sliver of status bar rather than the UI's edges
    fc = (f"[1:v]scale={ph_w}:{ph_h}:force_original_aspect_ratio=increase:flags=lanczos,"
          f"crop={ph_w}:{ph_h}[s];"
          f"color=c=0x0d0e0b:s=1920x1080:r=30000/1001[bg];"
          f"[bg][s]overlay={PHONE[0]}:{PHONE[1]}:shortest=1[b];"
          f"[b][0:v]overlay=0:0:shortest=1,format=yuv420p[v]")
    dst = f"inserts/ins_{IDX:02d}_endcard.mp4"
    r = subprocess.run([FF, "-nostdin", "-v", "error", "-y",
        "-loop", "1", "-framerate", "30000/1001", "-t", f"{DUR:.3f}", "-i", ov,
        "-ss", f"{APP_SS}", "-i", APP, "-t", f"{DUR:.3f}",
        "-filter_complex", fc, "-map", "[v]", "-an",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-r", "30000/1001", dst], capture_output=True, text=True)
    print("rc", r.returncode, r.stderr[-400:] if r.returncode else dst)
