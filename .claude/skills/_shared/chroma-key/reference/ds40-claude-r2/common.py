"""DS-40 green screen keyer: shared decode helpers."""
import subprocess, numpy as np, os
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4"
W, H = 2160, 3840
DEC = "scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb48le"

def frames(t0, dur=None, nframes=None, scale=None, src=SRC, fps=None):
    """Yield float32 RGB 0..1 frames (H,W,3), BT.709 decode, autorotated portrait."""
    vf = DEC if scale is None else f"scale={scale[0]}:{scale[1]}:in_color_matrix=bt709:in_range=tv:out_range=pc:flags=area,format=rgb48le"
    if fps: vf = f"fps={fps}," + vf
    cmd = [FF, "-v", "error", "-ss", f"{t0:.3f}", "-i", src]
    if dur: cmd += ["-t", f"{dur:.3f}"]
    if nframes: cmd += ["-frames:v", str(nframes)]
    cmd += ["-vf", vf, "-f", "rawvideo", "-"]
    w, h = (W, H) if scale is None else scale
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=w*h*6)
    n = w*h*3*2
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint16).reshape(h, w, 3).astype(np.float32) / 65535.0
    p.wait()
