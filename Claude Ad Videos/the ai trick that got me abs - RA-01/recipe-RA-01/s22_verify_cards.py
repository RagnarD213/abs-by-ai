#!/usr/bin/env python3
"""Every card clip must be exactly the frame count the timeline gives it, and decodable."""
import json, subprocess, sys
B = json.load(open("beats.json"))
FP = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffprobe"
bad = 0
for key in ("9x16", "16x9"):
    for c in B["cards"]:
        p = f"cards_{key}/{c['name']}.mp4"
        r = subprocess.run([FP, "-v", "error", "-count_frames", "-select_streams", "v",
                            "-show_entries", "stream=nb_read_frames,width,height", "-of", "csv=p=0", p],
                           capture_output=True, text=True)
        want_w, want_h = (1080, 1920) if key == "9x16" else (1920, 1080)
        try:
            w, h, n = r.stdout.strip().split(",")
            ok = int(n) == c["frames"] and int(w) == want_w and int(h) == want_h
        except Exception:
            ok, n, w, h = False, "?", "?", "?"
        if not ok:
            bad += 1
            print(f"  BAD {key} {c['name']}: {w}x{h} {n} frames, want {want_w}x{want_h} {c['frames']}")
print("all card clips correct" if not bad else f"{bad} bad card clip(s)")
sys.exit(1 if bad else 0)
