#!/usr/bin/env python3
"""prep_clips.py: copy every cutaway source into clips/ (never read another session's folder at render time).
25 fps stock is conformed FRAME FOR FRAME to 29.97 (each source frame shown once, 1.2x speed; never the fps filter, which repeats every
fifth frame: DS-49 lesson), starting at the film's own in-point, so plans.COVERS t is on the conformed file (t=0 is the film's in-point).
29.97 / 59.94 sources are copied whole (the batch's fps filter maps them exactly); plans t is then the source time."""
import os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import lib
ST = "/Volumes/Expansion/_edit_work/ro20/stock/"; LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/"
CL = "/Users/danielrose/Projects/_edit_work/SL-21/clips/"
# id: (source, film in-point s, conform 25->29.97?, source seconds to keep)
C = {
 "Cd08": (ST + "pexels-6953392-people-eating-together.mp4", 2.0, True, 12),
 "Cd09": (ST + "pexels-6631688-a-person-paying-bill-with-a-card.mp4", 5.0, True, 8),
 "Cd10": (ST + "pexels-3768985-slow-motion-footage-of-men-working-in-the-kitchen.mp4", 1.0, True, 9.4),
 "Cd11a": (ST + "pexels-8626681-a-smoky-hot-pan.mp4", 0.5, True, 7),
 "Cd11b": (ST + "pexels-14584573-cooking-pasta-and-putting-on-plate.mp4", 4.0, True, 7),
 "Cd13": (LIB + "dan-filmed/B0528_vinegar-measured-into-tablespoon-over-salad_16x9_4s.mp4", 0.0, False, 0),
 "Cd18": (ST + "pexels-17696508-toma-aerea-de-drone-en-la-playa.mp4", 0.0, False, 0),
 "Cd19a": (ST + "pexels-30403007-buffet-breakfast-at-luxurious-beach-resort.mp4", 1.0, False, 0),
 "Cd19b": (ST + "pexels-28099100-a-person-holding-a-plate-of-food-in-front-of-a-buffet.mp4", 0.0, True, 7),
 "Cd20": (LIB + "dan-filmed/B0461_dan-push-ups-black-mat-poolside-45_16x9_9s.mp4", 0.5, False, 0),
 "Cd21": (ST + "pexels-7015435-person-pouring-chocolate-syrup-to-pancakes-with-strawberries-and-blueberries.mp4", 2.0, "dedup", 9),      # R1b (reviewer D): the file says 29.97 fps but every sixth frame is a repeat (25 fps footage): the repeats come out, then it conforms like the other 25 fps stock
 "Cd23": (LIB + "stock/food-nutrition/B0045_man-drinking-fresh-coconut-water_16x9_16s.mp4", 8.0, True, 8),
 "Cd24": (ST + "pexels-7199187-man-on-a-counseling-session-with-psychiatrist.mp4", 2.0, True, 9.4),
 "Cd25": (ST + "pexels-4367640-a-man-walking-inside-the-gym.mp4", 1.0, False, 0),
 "Cd26": (ST + "pexels-7033769-prescription-pills-and-tablets.mp4", 1.0, True, 8),
 "B0642": (LIB + "dan-filmed/B0642_pull-ups-full-body-o23-c1829-01-t01_16x9_17s.mp4", 0.0, False, 0),
}
def dedup_select(src, t, keep):
    """R1c (reviewer D): mpdecimate left one repeat in. Measure every frame of the window (192x108 gray) and drop each frame whose
    difference from the frame before is under 30 % of the smaller of its two neighbours' differences (a repeat inside moving footage)."""
    import numpy as np
    raw = subprocess.run([lib.FF, "-v", "error", "-ss", f"{t:.3f}", "-t", f"{keep:.3f}", "-i", src, "-vf", "scale=192:108,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 108, 192).astype(np.float32); d = np.abs(fr[1:] - fr[:-1]).mean((1, 2))
    drop = [i + 1 for i in range(len(d)) if d[i] < 0.3 * min(d[i - 1] if i else 9e9, d[i + 1] if i + 1 < len(d) else 9e9)]
    print("   repeats dropped:", len(drop), "of", len(fr), drop[:40])
    return ("select='" + "*".join(f"not(eq(n\\,{i}))" for i in drop) + "'," if drop else "")
for k, (src, t, conform, keep) in C.items():
    out = CL + k + ".mp4"
    if os.path.exists(out): continue
    assert os.path.exists(src), src
    if not conform: shutil.copyfile(src, out); print(k, "copied"); continue
    subprocess.run([lib.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{t:.3f}", "-t", f"{keep:.3f}", "-i", src, "-an",
                    "-vf", (dedup_select(src, t, keep) if conform == "dedup" else "") + "scale=-2:'min(ih,1620)':flags=lanczos:in_color_matrix=bt709:out_color_matrix=bt709,setpts=N/(30000/1001)/TB", "-r", "30000/1001",
                    "-c:v", "libx264", "-crf", "10", "-preset", "medium", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], check=True)
    print(k, "conformed 25 -> 29.97 from source", t)
