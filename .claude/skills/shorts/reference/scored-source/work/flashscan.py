#!/usr/bin/env python3
"""Muhammad's cut joins sections with a WHITE FLASH BLOOM. A short that starts or ends on
one opens/closes on a white frame, which reads as a rendering fault. Scan +-1.2s around
every piece boundary and report where the picture is more than 12 Y above its local base."""
import subprocess, sys, json, re
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "../mrepro/ref_hd.mp4"
def yavg(t0, dur):
    p = subprocess.run([FF, "-nostdin", "-v", "info", "-ss", str(t0), "-i", SRC, "-t", str(dur),
        "-vf", "scale=64:36,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-",
        "-f", "null", "-"], capture_output=True, text=True)
    out = []
    cur = None
    for line in p.stdout.splitlines():
        m = re.search(r"pts_time:([\d.]+)", line)
        if m: cur = float(m.group(1))
        m = re.search(r"YAVG=([\d.]+)", line)
        if m and cur is not None: out.append((round(t0 + cur, 3), float(m.group(1))))
    return out
for label, t in json.load(open(sys.argv[1])):
    s = yavg(max(0, t - 1.2), 2.4)
    if not s: print(label, t, "no frames"); continue
    base = sorted(v for _, v in s)[len(s) // 4]
    hot = [(tt, v) for tt, v in s if v > base + 12]
    at = min(s, key=lambda x: abs(x[0] - t))
    flag = "  <-- FLASH AT CUT" if at[1] > base + 12 else ""
    print(f"{label:14s} t={t:7.2f}  Y={at[1]:6.1f} base={base:6.1f}"
          f"  hot window {hot[0][0]:.2f}-{hot[-1][0]:.2f}" if hot else
          f"{label:14s} t={t:7.2f}  Y={at[1]:6.1f} base={base:6.1f}  clean", end="")
    print(flag)
