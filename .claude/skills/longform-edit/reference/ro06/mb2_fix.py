"""Round 6 (Dan, 9:24: "crop a little wider and higher so that my hair, when I raise my arms a few seconds after that, doesn't go out of frame").
Shots mb2.0r0 and mb2.0r1, roll C1574. Facts: once the operator has tilted down (about 174 source px over the first 7 s of the take) the camera's top
row sits ON his hair: the crown is cut by up to about 7 source px, and there is no recorded picture above it. Before the tilt the camera recorded the
trees, sky and pavilion roof above his head. So:
  1. a still PLATE of that upper background from the take's own first 1.3 s (camera 170 px higher), registered to the settled camera, sits above the
     camera frame: a taller canvas;
  2. while the camera is still coming down, the real picture above his head is used as shot (stab offsets from round 5), the plate only above it;
  3. the few rows of hair crown the camera cut are put back from his own hair in an earlier frame of the same take (camera 10 px higher), matched on
     the width of hair at the frame edge, so only as many rows as were cut come back;
  4. one fixed crop for both shots: 1600x900 (1.2x, was 1.3x and then the full frame), top 52 px above the camera's top row.
render(sg) -> cached graded 1920x1080 segment for build.render_seg.  usage: mb2_fix.py stills | proof"""
import sys, os, json, subprocess, hashlib, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, cv2
from PIL import Image
import frames as F
W = "/Volumes/Extreme/_edit_work/ro06"; D = f"{W}/round6/mb2"; FPS = 30000/1001; FF = F.FF
ROLL = "C1574"; G0 = F.ROLLS[ROLL]["f0"]; PATH = F.ROLLS[ROLL]["path"]
CROP = (1600, 900, 154, -52); UP = 96                    # canvas rows above the camera's top row
R0 = (30106 - G0, 30330 - G0)                            # mb2.0r0 in roll frames (76..300): stabilised in round 5
STAB = json.load(open(f"{W}/round5/stab.json"))["mb2.0r0"]
REF_F = 190                                              # the crown donor frame: camera 10 px above settled, his whole hair in frame, same stance
def off(lf):                                             # where the background sits against the settled camera, per roll frame
    if R0[0] <= lf < R0[1]: return STAB[lf - R0[0]]
    assert lf >= R0[1], lf; return [0.0, 0.0]
def decode(f0, n):
    ts = f0/FPS; ss = max(0, ts - 1)
    p = subprocess.Popen([FF, "-v", "error", "-ss", f"{ss:.4f}", "-i", PATH, "-ss", f"{max(0, ts-ss-0.4/FPS):.4f}", "-frames:v", str(n), "-pix_fmt", "yuv444p", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    for _ in range(n):
        b = p.stdout.read(1920*1080*3); assert len(b) == 1920*1080*3
        yield np.frombuffer(b, np.uint8).reshape(3, 1080, 1920)
    p.stdout.close(); p.wait()
def mask(lf):                                            # Apple Vision person mask made for every frame of the take (960x540)
    return np.asarray(Image.open(f"{D}/m/f_{lf+1:05d}.mask.png").convert("L").resize((960, 540)), np.uint8) > 127
def plate():
    """Rows -UP..0 of the settled camera, from frames 0..39 (camera 170 to 174 px higher, he has not moved): median of the frames after each is
    registered to the settled background by phase correlation on the shared band, his own column left out."""
    p = f"{D}/plate.npy"
    if os.path.exists(p): return np.load(p)
    settled = np.median(np.stack([f for f in decode(380, 24)]).astype(np.float32), 0)                 # [3, 1080, 1920]
    moff = np.load(f"{D}/off.npy"); acc = []
    for i, f in enumerate(decode(0, 40)):
        if i % 3: continue
        dx, dy = moff[i]; f = f.astype(np.float32)
        M = np.float32([[1, 0, -dx], [0, 1, UP - dy]])                                                 # frame -> canvas (canvas row UP = settled row 0)
        c = np.stack([cv2.warpAffine(f[k], M, (1920, UP + 240), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE) for k in range(3)])
        a = c[0, UP:UP + 200].copy(); b = settled[0, :200].copy(); a[:, 700:1250] = 0; b[:, 700:1250] = 0  # refine on the overlap, background only
        (sx, sy), _ = cv2.phaseCorrelate(a, b)
        M2 = np.float32([[1, 0, sx], [0, 1, sy]]); c = np.stack([cv2.warpAffine(c[k], M2, (1920, UP + 240), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE) for k in range(3)])
        acc.append(c); print("plate frame", i, "refine", round(sx, 2), round(sy, 2), flush=True)
    pl = np.median(np.stack(acc), 0)
    g = [float(np.median(settled[k, 4:120, np.r_[100:650, 1300:1850]]) - np.median(pl[k, UP + 4:UP + 120, np.r_[100:650, 1300:1850]])) for k in range(3)]
    print("plate level against the settled frames (Y, U, V):", [round(x, 2) for x in g]); pl[0] += g[0]
    np.save(p, pl.astype(np.float32)); return pl
def hair_span(m):
    """Hair touching the camera's top row: (x0, x1) in source px of the widest run in mask row 1 near his head, else None."""
    xs = np.where(m[1, 400:560])[0]
    if not len(xs): return None
    runs = np.split(xs, np.where(np.diff(xs) > 3)[0] + 1); r = max(runs, key=len)
    return (int(r[0] + 400)*2, int(r[-1] + 400)*2 + 2) if len(r) >= 6 else None
_REF = None
def crown():
    """The donor crown: frame REF_F's hair top rows (YUV), its soft mask, and width / centre of the hair per row below the crown."""
    global _REF
    if _REF is None:
        f = next(decode(REF_F, 1)).astype(np.float32); m = mask(REF_F); ys = np.where(m[:, 400:560].sum(1) >= 2)[0]; top = int(ys[0])*2
        mm = cv2.GaussianBlur(cv2.resize(m.astype(np.float32), (1920, 1080), interpolation=cv2.INTER_LINEAR), (0, 0), 1.2)
        prof = []
        for d in range(0, 30):
            xs = np.where(mm[top + d, 800:1120] > 0.5)[0]; prof.append((len(xs), 800 + (xs[0] + xs[-1])/2 if len(xs) else None))
        _REF = (f, mm, top, prof)
    return _REF
def canvas(f, lf, spans):
    """One source frame on the taller canvas (float YUV, [3, 1080+UP, 1920]) at the settled camera position."""
    pl = plate(); dx, dy = off(lf); f = f.astype(np.float32)
    M = np.float32([[1, 0, -dx], [0, 1, UP - dy]]); H = 1080 + UP
    c = np.stack([cv2.warpAffine(f[k], M, (1920, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE) for k in range(3)])
    edge = UP - dy                                                    # canvas row of the camera's top row in this frame
    yy = np.arange(H, dtype=np.float32)[:, None]
    a = np.clip((yy - edge)/6.0, 0, 1)[:UP + 240]                     # 0 = plate, 1 = the frame; a 6 row ramp just inside the frame's top edge
    c[:, :UP + 240] = pl*(1 - a) + c[:, :UP + 240]*a
    sp = spans.get(lf)
    if sp and dy < 12:                                                # the camera's top row is on his hair: put back the rows it cut
        rf, rm, top, prof = crown(); w0 = sp[1] - sp[0]; c0 = (sp[0] + sp[1])/2 - dx
        d0 = next((d for d, (w, _) in enumerate(prof) if w >= w0), None)
        if d0 and d0 <= 16:
            d0 = d0 + 1; cx = prof[d0][1]; sh = int(round(c0 - cx)); e = int(round(edge)); x0, x1 = 760, 1160
            src = rf[:, top - 3:top + d0, x0:x1]; al = rm[top - 3:top + d0, x0:x1].copy()
            al *= np.clip((np.arange(d0 + 3, dtype=np.float32)[:, None] + 0.5)/2.0, 0, 1)             # soft top
            ys = slice(e - d0 - 3 + 1, e + 1); xs = slice(x0 + sh, x1 + sh)
            c[:, ys, xs] = c[:, ys, xs]*(1 - al) + src*al
    return c
def spans_for(a, b):
    """Smoothed hair spans (median of 5 frames) so the restored rows do not flicker."""
    raw = {lf: hair_span(mask(lf)) for lf in range(max(0, a - 2), b + 2) if os.path.exists(f"{D}/m/f_{lf+1:05d}.mask.png")}
    out = {}
    for lf in range(a, b):
        v = [raw[k] for k in range(lf - 2, lf + 3) if raw.get(k)]
        if raw.get(lf) and len(v) >= 3: out[lf] = (int(np.median([x[0] for x in v])), int(np.median([x[1] for x in v])))
    return out
def crop_frame(c):
    cw, ch, cx, cy = CROP; return np.clip(c[:, UP + cy:UP + cy + ch, cx:cx + cw] + 0.5, 0, 255).astype(np.uint8)
def render(sg, sharpen=None):
    lf = sg["src0"] - G0; n = sg["o1"] - sg["o0"]; cw, ch = CROP[:2]
    vf = F.vf(ROLL, (cw, ch, 0, 0)).replace("format=rgb24", "format=yuv420p").replace(f"crop={cw}:{ch}:0:0,", "")
    if sharpen: vf = vf.replace(",format=yuv420p", f",{sharpen},format=yuv420p")
    key = hashlib.sha1(json.dumps([lf, n, vf, CROP, UP, REF_F, "v3-plateonly"]).encode()).hexdigest()[:12]; out = f"{W}/cache/seg_mb2fix_{sg['src0']}_{key}.mp4"
    if os.path.exists(out): return out
    sp = {}                                               # round 6: the crown donor (step 3) is OFF. Seen side by side, the plate alone is cleaner and leaves his picture untouched; the camera cut at most about 7 px of crown
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv444p", "-s", f"{cw}x{ch}", "-framerate", "30000/1001", "-color_range", "tv", "-colorspace", "bt709", "-i", "-",
                            "-vf", vf, "-an", "-c:v", "libx264", "-crf", "12", "-preset", "veryfast", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    for i, f in enumerate(decode(lf, n)): enc.stdin.write(crop_frame(canvas(f, lf + i, sp)).tobytes())
    enc.stdin.close(); enc.wait(); os.rename(out + ".tmp.mp4", out); return out
if __name__ == "__main__":
    os.makedirs(f"{D}/stills", exist_ok=True)
    for lf in [int(a) for a in sys.argv[2:]] or [80, 131, 160, 200, 230, 257, 272, 284, 300, 311, 335, 346]:
        f = next(decode(lf, 1)); sp = spans_for(lf, lf + 1); c = canvas(f, lf, sp)
        for tag, cc in (("fix", c), ("plateonly", canvas(f, lf, {}))):
            y = crop_frame(cc); bgr = cv2.cvtColor(np.transpose(y, (1, 2, 0)), cv2.COLOR_YUV2BGR)   # rough preview only (the build grades it)
            cv2.imwrite(f"{D}/stills/{tag}_{lf:04d}.jpg", cv2.resize(bgr, (1920, 1080), interpolation=cv2.INTER_LANCZOS4), [cv2.IMWRITE_JPEG_QUALITY, 92])
        print(lf, "span", sp.get(lf), "off", off(lf))
