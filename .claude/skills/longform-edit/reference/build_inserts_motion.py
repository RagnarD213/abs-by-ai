#!/usr/bin/env python3
"""Pre-render every cutaway to an exact-duration 1920x1080 29.97 MP4.

Pre-rendering matters: the composite pass opens one decoder per insert, and a 3-second
file costs almost nothing to hold open while a 30-second 4K source would.

Two forms:
  full  -- the stock fills the frame, cover-scaled and centre-cropped
  inset -- the stock sits inside a rounded window on the bracketed military-green field,
           which is the reference edit's signature presentation for B-roll

A light unifying S-curve is applied to all stock so it does not sit brighter or flatter
than the graded camera footage; it is deliberately much gentler than the C163x grade.
Vertical sources (the app screen recording) are never centre-cropped -- they are fitted
whole inside the window, because cropping a phone screen to 16:9 loses the UI.
"""
import os, subprocess, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
os.environ["MOTIONLIB_FFMPEG"] = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
import motionlib as M
import spec
from concurrent.futures import ThreadPoolExecutor

FF   = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
FFP  = FF.replace("ffmpeg", "ffprobe")
OUT  = "inserts"; os.makedirs(OUT, exist_ok=True)
TMP  = "inserts/_frames"; os.makedirs(TMP, exist_ok=True)
FPS  = "30000/1001"
TONE = "curves=all='0/0 0.06/0.028 0.5/0.512 0.94/0.952 1/1'"
WX0, WY0, WX1, WY1 = spec.WINDOW
WW, WH = WX1 - WX0, WY1 - WY0

def src_for(key):
    if key in spec.OWN: return spec.OWN[key]
    stem, ss = spec.STOCK[key]
    return (f"stock/raw/{stem}.mp4", ss)

def probe(p):
    o = subprocess.run([FFP, "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()
    w, h = o.split(",")[:2]; return int(w), int(h)

def build(job):
    i, (start, dur, kind, key, note) = job
    dst = f"{OUT}/ins_{i:02d}_{key}.mp4"
    if os.path.exists(dst) and os.path.getsize(dst) > 5000: return f"{dst} [cached]"
    src, ss = src_for(key)
    w, h = probe(src)
    if kind == "full":
        vf = (f"scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,"
              f"crop=1920:1080,{TONE},format=yuv420p")
        cmd = [FF, "-nostdin", "-v", "error", "-y", "-ss", f"{ss:.2f}", "-i", src,
               "-t", f"{dur:.3f}", "-vf", vf]
    else:
        box = spec.WINDOW_FOR.get(key, spec.WINDOW)
        bx0, by0 = box[0], box[1]
        bw, bh = box[2] - box[0], box[3] - box[1]
        frame = f"{TMP}/frame_{i:02d}.mov"
        M.inset_frame(frame, dur, box, pal=M.MIL, radius=42 if bh > bw else 26)
        fit = (f"scale={bw}:{bh}:force_original_aspect_ratio=increase:flags=lanczos,"
               f"crop={bw}:{bh}")
        vf = (f"[1:v]{fit},{TONE}[s];"
              f"color=c=0x0d0e0b:s=1920x1080:r={FPS}[bg];"
              f"[bg][s]overlay={bx0}:{by0}:shortest=1[b];"
              f"[b][0:v]overlay=0:0:shortest=1,format=yuv420p[v]")
        cmd = [FF, "-nostdin", "-v", "error", "-y", "-i", frame,
               "-ss", f"{ss:.2f}", "-i", src, "-t", f"{dur:.3f}",
               "-filter_complex", vf, "-map", "[v]"]
    cmd += ["-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
            "-pix_fmt", "yuv420p", "-r", FPS, "-movflags", "+faststart", dst]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: return f"FAIL {key}: {r.stderr[-300:]}"
    return dst

if __name__ == "__main__":
    jobs = list(enumerate(spec.INSERTS))
    with ThreadPoolExecutor(max_workers=5) as ex:
        for r in ex.map(build, jobs): print(" ", r)
    bad = []
    for i, (start, dur, kind, key, note) in jobs:
        p = f"{OUT}/ins_{i:02d}_{key}.mp4"
        if not os.path.exists(p): bad.append((key, "absent")); continue
        d = float(subprocess.run([FFP, "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip())
        if abs(d - dur) > 0.10: bad.append((key, f"{d:.3f} vs planned {dur:.3f}"))
    print("duration check:", bad or f"all {len(jobs)} inserts within 0.10s of plan")
