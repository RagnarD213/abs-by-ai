"""RO-19 headroom proof: the camera framed Dan's hair on the top row of the picture for the whole roll (no room to crop higher).
This adds N rows ABOVE the camera frame: the wall, trim and door frame are continued straight up from the frame's own top rows
(they are vertical), the wall behind his hair is filled from the wall either side of it, and where his hair is cut by the top
edge a rounded cap is drawn from his own hair pixels (dome depth from the width of hair on the top row). The picture moves down
N rows (N rows of his torso leave the bottom). Then the normal grade and the normal two sizes.
usage: headroom.py <shot id> <framing W|T> <out.mp4> [seconds]   -> before | after side by side, graded, 1920x540"""
import sys, json, subprocess, numpy as np
from PIL import Image, ImageFilter
W = "/Volumes/Extreme/_edit_work/ro19"; FPS = 30000/1001; N = 56; R = 170.0
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
S = {s["id"]: s for s in json.load(open(f"{W}/shots.json"))}; SF = json.load(open(f"{W}/shot_framing.json"))
ROLLS = json.load(open(f"{W}/rolls.json")); GR = json.load(open(f"{W}/grades.json")); LOOK = open(f"{W}/look_option.txt").read().strip()
LUM = np.array([0.2126, 0.7152, 0.0722], np.float32)
def hair_span(fr, cx):
    """columns of the top rows covered by his hair: darker than the wall, nearest the head centre"""
    x0, x1 = max(0, int(cx-330)), min(1920, int(cx+330)); y = fr[0:4, x0:x1].mean(0) @ LUM
    wall = np.percentile(y, 80); dark = y < 0.55*wall; best = None; i = 0
    while i < len(dark):
        if dark[i]:
            j = i; gap = 0
            while j+1 < len(dark) and (dark[j+1] or gap < 8):
                gap = 0 if dark[j+1] else gap+1; j += 1
            while not dark[j]: j -= 1
            if best is None or abs((i+j)/2+x0-cx) < abs((best[0]+best[1])/2-cx): best = (i+x0, j+x0)
            i = j+1
        else: i += 1
    return best if best and best[1]-best[0] >= 14 else None
def extend(fr, span):
    """fr: 1080x1920x3 float (source colours). Returns the frame with N new rows on top and its last N rows dropped."""
    top = fr[0:2].mean(0); E = np.repeat(top[None], N, 0).copy()
    if span:
        a, b = span; a2, b2 = max(0, a-10), min(1919, b+10)
        L = fr[0:4, max(0, a2-24):max(1, a2-4)].reshape(-1, 3).mean(0); Rr = fr[0:4, min(1918, b2+4):min(1919, b2+24)].reshape(-1, 3).mean(0)
        t = np.linspace(0, 1, b2-a2+1, dtype=np.float32)[:, None]; E[:, a2:b2+1] = (L*(1-t) + Rr*t)[None]
        w = b-a; d = int(min(N-8, max(3, w*w/(8*R))))
        cap = np.zeros((N, 1920), np.float32); mid = (a+b)/2
        for r in range(1, d+1):                                   # r rows above the old top edge
            h = d-r; half = np.sqrt(max(0.0, 2*R*h - h*h)) if h > 0 else 0.0
            if half > 0: cap[N-r, int(max(0, mid-half)):int(min(1919, mid+half))+1] = 1
        cap = np.asarray(Image.fromarray((cap*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6)), np.float32)/255
        row = fr[0:3].mean(0).copy(); seg = row[a:b+1]; k = 21; pad = np.pad(seg, ((k//2, k//2), (0, 0)), mode="edge")
        sm = np.stack([np.convolve(pad[:, c], np.ones(k, np.float32)/k, mode="valid") for c in range(3)], 1)   # no streaks: his hair colour, smoothed along the row
        row[a:b+1] = 0.35*seg + 0.65*sm
        row[:a] = row[a]; row[b+1:] = row[b]                     # the dome is wider than the cut: keep hair colour to its edges
        hair = np.repeat(row[None], N, 0)*0.95                   # carried up
        E = E*(1-cap[..., None]) + hair*cap[..., None]
    E += np.random.default_rng(7).normal(0, 1.1, E.shape).astype(np.float32)      # a little grain so the strip is not flat
    return np.concatenate([np.clip(E, 0, 255), fr[:1080-N]], 0)
def run(shot, framing, out, secs):
    s = S[shot]; roll = s["roll"]; lf = s["src_f0"]-ROLLS[roll]["f0"]; n = min(int(secs*FPS), s["src_f1"]-s["src_f0"]); cx = SF[shot]["cx"]
    cw, ch, x0, y0 = (1920, 1080, 0, 0) if framing == "W" else SF[shot]["T"]
    dec = subprocess.Popen([FF, "-v", "error", "-ss", f"{lf/FPS:.4f}", "-i", ROLLS[roll]["path"], "-frames:v", str(n),
                            "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    vf = (f"split[a][b];[a]crop=1920:1080:0:0,crop={cw}:{ch}:{x0}:{y0},scale=960:540:flags=lanczos,format=gbrp16le,{GR[roll][LOOK]},format=rgb24[l];"
          f"[b]crop=1920:1080:0:1080,crop={cw}:{ch}:{x0}:0,scale=960:540:flags=lanczos,format=gbrp16le,{GR[roll][LOOK]},format=rgb24[r];[l][r]hstack")
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x2160", "-framerate", "30000/1001", "-i", "-",
                            "-filter_complex", vf, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    hist = []
    for k in range(n):
        buf = dec.stdout.read(1920*1080*3)
        if len(buf) < 1920*1080*3: break
        fr = np.frombuffer(buf, np.uint8).reshape(1080, 1920, 3).astype(np.float32)
        sp = hair_span(fr, cx); hist.append(sp); last = [h for h in hist[-5:] if h]
        if last: sp = (int(np.median([h[0] for h in last])), int(np.median([h[1] for h in last])))
        ext = extend(fr, sp)
        enc.stdin.write(np.concatenate([fr, ext], 0).astype(np.uint8).tobytes())     # top: the camera frame; bottom: with headroom
    enc.stdin.close(); enc.wait(); dec.wait()
    ws = [h[1]-h[0] for h in hist if h]
    print(shot, framing, n, "frames; hair on the top row in", len(ws), "of", len(hist), "frames; width median", int(np.median(ws)) if ws else 0, "max", max(ws) if ws else 0, flush=True)
if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 6.0)
