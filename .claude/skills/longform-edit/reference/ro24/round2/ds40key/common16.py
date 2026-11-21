"""RO-24 port of the approved DS-40 Claude R2 key (house standard, 2026-10-21) to C1726, 16:9 landscape 3840x2160.
Decode: BT.709 limited -> full, accurate rounding + full chroma interpolation (chroma-key README). Frame-exact: frame f
has pts f*1001/30000; seek to (f - 0.3)/FPS."""
import subprocess, numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1726.MP4"
W, H = 3840, 2160
OW, OH = 2880, 1620            # output scale 0.75: Dan's head here is ~0.75x DS-40's, so features land ~1.1x DS-40 output px
FPS = 30000 / 1001
WORK = "/Volumes/Expansion/_edit_work/RO-24/round2/key"
DEC = "scale=in_color_matrix=bt709:in_range=tv:out_range=pc:flags=accurate_rnd+full_chroma_int"

def frames(f0, n, scale=None, fps=None, ff=FF):
    """Yield float32 RGB 0..1 frames from source frame f0 (n frames, or a duration in fps mode)."""
    vf = DEC + ("" if scale is None else f",scale={scale[0]}:{scale[1]}:flags=area") + ",format=rgb48le"
    if fps: vf = f"fps={fps}," + vf
    cmd = [ff, "-v", "error", "-ss", f"{(f0 - 0.3) / FPS:.5f}", "-i", SRC]
    cmd += (["-t", f"{n / FPS:.3f}"] if fps else ["-frames:v", str(n)])
    cmd += ["-an", "-vf", vf, "-f", "rawvideo", "-"]
    w, h = (W, H) if scale is None else scale
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=w * h * 6)
    nb = w * h * 6
    while True:
        b = p.stdout.read(nb)
        if len(b) < nb: break
        yield np.frombuffer(b, np.uint16).reshape(h, w, 3).astype(np.float32) / 65535.0
    p.wait()
