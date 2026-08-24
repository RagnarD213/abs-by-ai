#!/usr/bin/env python3
"""Pre-render every stock cutaway to an exact-duration 1920x1080 29.97 MP4.

Pre-rendering matters: the composite pass opens one decoder per insert, and a
4-second file costs almost nothing to hold open while a 30-second 4K source
would. Vertical sources get a blurred-fill background rather than a hard
centre-crop - a 9:16 clip cropped to 16:9 loses the subject's head.
No audio: the programme audio is Dan's, continuous, underneath every cutaway.
usage: build_inserts.py [--force]
"""
import importlib.util, subprocess, sys, os
from pathlib import Path

B = Path("/Volumes/Extreme/_edit_work/spraytan")
RAW = B / "stock" / "raw"; OUT = B / "inserts"; OUT.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location("i", B / "inserts.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
FORCE = "--force" in sys.argv
FPS = "30000/1001"
# a light unifying S-curve so stock does not sit brighter/flatter than the
# graded camera footage; deliberately much gentler than the C1512 grade.
TONE = "curves=all='0/0 0.06/0.025 0.5/0.515 0.94/0.955 1/1'"

def probe(p):
    o = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
        "stream=width,height","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip()
    w,h = o.split(",")[:2]; return int(w), int(h)

built, missing = 0, []
for start, dur, kind, key, note in m.INSERTS:
    if kind != "clip": continue
    src_key, ss = (m.ALIASES.get(key) or (key, None))
    stem, default_ss = m.STOCK[src_key]
    ss = default_ss if ss is None else ss
    src = RAW / f"{stem}.mp4"
    if not src.exists(): missing.append(stem); continue
    dst = OUT / f"ins_{key}.mp4"
    if dst.exists() and not FORCE and dst.stat().st_size > 0: continue
    w, h = probe(src)
    if h > w:   # vertical: blurred 16:9 fill + sharp centred original
        vf = (f"[0:v]split=2[bg][fg];"
              f"[bg]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
              f"gblur=sigma=30,eq=brightness=-0.10:saturation=0.85[b];"
              f"[fg]scale=-2:1080[f];[b][f]overlay=(W-w)/2:0,{TONE},format=yuv420p[v]")
        cmd = ["ffmpeg","-nostdin","-v","error","-y","-ss",f"{ss:.2f}","-i",str(src),
               "-t",f"{dur:.3f}","-filter_complex",vf,"-map","[v]"]
    else:       # landscape: cover-scale then centre-crop to 16:9
        vf = (f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
              f"{TONE},format=yuv420p")
        cmd = ["ffmpeg","-nostdin","-v","error","-y","-ss",f"{ss:.2f}","-i",str(src),
               "-t",f"{dur:.3f}","-vf",vf]
    cmd += ["-an","-c:v","libx264","-preset","fast","-crf","16","-pix_fmt","yuv420p",
            "-r",FPS,"-movflags","+faststart",str(dst)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print("FAIL", key, r.stderr[-300:]); continue
    built += 1
print(f"built {built} inserts -> {OUT}")
if missing: print("MISSING SOURCES:", set(missing))
# every clip insert must now exist and be within 1 frame of its planned duration
bad = []
for start, dur, kind, key, note in m.INSERTS:
    if kind != "clip": continue
    p = OUT / f"ins_{key}.mp4"
    if not p.exists(): bad.append((key,"absent")); continue
    d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip())
    if abs(d - dur) > 0.10: bad.append((key, f"{d:.3f} vs {dur:.3f}"))
print("duration check:", bad or "all inserts within 0.10s of plan")
