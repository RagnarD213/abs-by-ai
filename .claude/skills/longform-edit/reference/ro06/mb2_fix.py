"""Round 6 (Dan, 9:24: "crop a little wider and higher so that my hair, when I raise my arms a few seconds after that, doesn't go out of frame").
Shots mb2.0r0 and mb2.0r1, roll C1574. Facts: once the operator has tilted down (about 174 source px over the first 7 s of the take) the camera's top
row sits ON his hair: the crown is cut by up to about 7 source px, and there is no recorded picture above it. Before the tilt the camera recorded the
trees, sky and pavilion roof above his head. So:
  1. a still PLATE of that upper background from the take's own first 1.3 s (camera 170 px higher), registered to the settled camera, sits above the
     camera frame: a taller canvas;
  2. while the camera is still coming down, the real picture above his head is used as shot (stab offsets from round 5), the plate only above it;
  3. the few rows of hair crown the camera cut are put back from his own hair in an earlier frame of the same take (camera 10 px higher), matched on
     the width of hair at the frame edge, so only as many rows as were cut come back;
  4. one fixed crop for the three shots of the take (the two before the toe-touch cutaway and, after the first review, the one after it):
     1600x900 (1.2x, was 1.3x and then the full frame), top 52 px above the camera's top row. Step 3 is switched off (CROWN): it left a ghost.
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
_LATE = None
def late_off():
    """After the stabilised shot the operator still lets the camera creep a pixel or two. Measured every 10 frames against the settled frames
    (phase correlation on the top band, his column left out), smoothed; cached in round6/mb2/late_off.json."""
    global _LATE
    if _LATE is None:
        p = f"{D}/late_off.json"
        if not os.path.exists(p):
            settled = np.median(np.stack([f[0] for f in decode(380, 24)]).astype(np.float32), 0)[:260]; settled[:, 700:1300] = 0
            ks = list(range(R0[1], 794, 10)) + [793]; v = {}
            for k in ks:
                a = next(decode(k, 1))[0].astype(np.float32)[:260].copy(); a[:, 700:1300] = 0
                (sx, sy), _ = cv2.phaseCorrelate(settled, a); v[k] = [round(float(sx), 2), round(float(sy), 2)]
            json.dump(v, open(p, "w"))
        v = {int(k): x for k, x in json.load(open(p)).items()}; ks = sorted(v)
        xs = np.interp(np.arange(R0[1], 794), ks, [v[k][0] for k in ks]); ys = np.interp(np.arange(R0[1], 794), ks, [v[k][1] for k in ks])
        k = np.ones(31)/31; xs = np.convolve(np.pad(xs, 15, mode="edge"), k, "valid"); ys = np.convolve(np.pad(ys, 15, mode="edge"), k, "valid")
        w = np.clip(np.arange(len(xs))/45.0, 0, 1)                                         # in step with the stabilised shot at the join (it ends on exactly 0)
        _LATE = np.stack([xs*w, ys*w], 1)
    return _LATE
def off(lf):                                             # where the background sits against the settled camera, per roll frame
    if R0[0] <= lf < R0[1]: return STAB[lf - R0[0]]
    assert lf >= R0[1], lf; return [float(x) for x in late_off()[lf - R0[1]]]
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
    p = f"{D}/plate_v2.npy"
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
    pl[0] = pl[0] + 0.45*(pl[0] - cv2.GaussianBlur(pl[0], (0, 0), 1.1))                    # a median of 14 moving-leaf frames is softer than one live frame (review: 17 to 20 %)
    np.save(p, pl.astype(np.float32)); return pl
def hair_span(m):
    """Hair touching the camera's top row: (x0, x1) in source px of the widest run in mask row 1 near his head, else None."""
    xs = np.where(m[1, 400:560])[0]
    if not len(xs): return None
    runs = np.split(xs, np.where(np.diff(xs) > 3)[0] + 1); r = max(runs, key=len)
    return (int(r[0] + 400)*2, int(r[-1] + 400)*2 + 2) if len(r) >= 6 else None
_REF = None
def crown():
    """The donor crown: frame REF_F's hair top rows (YUV) with a matte made of the person mask AND darkness (his hair reads under 60 in Y, the trees behind
    it 70 and up: the first attempt used the mask alone and carried a line of tree pixels with it), and the width / centre of that hair per row."""
    global _REF
    if _REF is None:
        f = next(decode(REF_F, 1)).astype(np.float32); m = mask(REF_F); ys = np.where(m[:, 400:560].sum(1) >= 2)[0]
        mm = cv2.GaussianBlur(cv2.resize(m.astype(np.float32), (1920, 1080), interpolation=cv2.INTER_LINEAR), (0, 0), 1.5)
        dark = np.clip((78.0 - cv2.GaussianBlur(f[0], (0, 0), 0.8))/22.0, 0, 1); al = np.minimum(mm*1.6, 1)*dark
        rows = np.where((al[:, 800:1120] > 0.5).sum(1) >= 6)[0]; top = int(rows[0]); prof = []
        for d in range(0, 34):
            xs = np.where(al[top + d, 800:1120] > 0.5)[0]; prof.append((int(xs[-1] - xs[0] + 1) if len(xs) else 0, 800 + (xs[0] + xs[-1])/2 if len(xs) else None))
        _REF = (f, al, top, prof)
    return _REF
def hair_run(y_row, m_row):
    """The run of hair on the camera's top row: dark pixels inside his mask's columns. (x0, x1) in source px, or None."""
    xs = np.where(m_row)[0]
    if not len(xs): return None
    lo, hi = max(0, int(xs[0])*2 - 12), min(1920, int(xs[-1])*2 + 14); dk = np.where(y_row[lo:hi] < 64)[0]
    if len(dk) < 10: return None
    runs = np.split(dk, np.where(np.diff(dk) > 4)[0] + 1); r = max(runs, key=len)
    return (lo + int(r[0]), lo + int(r[-1]) + 1) if len(r) >= 10 else None
def canvas(f, lf, spans):
    """One source frame on the taller canvas (float YUV, [3, 1080+UP, 1920]) at the settled camera position."""
    pl = plate(); dx, dy = off(lf); f = f.astype(np.float32)
    M = np.float32([[1, 0, -dx], [0, 1, UP - dy]]); H = 1080 + UP
    c = np.stack([cv2.warpAffine(f[k], M, (1920, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE) for k in range(3)])
    edge = UP - dy                                                    # canvas row of the camera's top row in this frame
    yy = np.arange(H, dtype=np.float32)[:, None]
    a = np.clip((yy - edge)/6.0, 0, 1)[:UP + 240]                     # 0 = plate, 1 = the frame; a 6 row ramp just inside the frame's top edge
    pn = pl.copy(); rng = np.random.default_rng(lf); pn[0] += rng.normal(0, GRAIN, pn[0].shape).astype(np.float32)   # the live picture has sensor grain; a still plate without it reads frozen
    c[:, :UP + 240] = pn*(1 - a) + c[:, :UP + 240]*a
    sp = spans.get(lf)
    if sp and dy < 12:                                                # the camera's top row is on his hair: put back the rows it cut, from his own hair
        rf, ral, top, prof = crown(); w0 = sp[1] - sp[0]; c0 = (sp[0] + sp[1])/2 - dx
        d0 = next((d for d, (w, _) in enumerate(prof) if w >= w0), None)
        if d0 is not None and 2 <= d0 <= 22:
            cx = prof[d0][1]; sh = int(round(c0 - cx)); e = int(round(edge)); x0, x1 = 760, 1160; ov = 5       # ov rows of overlap below the edge, faded, so no line shows at the join
            src = rf[:, top - 4:top + d0 + ov, x0:x1]; al = ral[top - 4:top + d0 + ov, x0:x1].copy()
            al[-ov:] *= np.linspace(1, 0, ov + 2, dtype=np.float32)[1:-1][:, None]
            ys = slice(e - d0 - 4, e + ov); xs = slice(x0 + sh, x1 + sh)
            c[:, ys, xs] = c[:, ys, xs]*(1 - al) + src*al
    return c
GRAIN = 1.6; CROWN = False   # the crown donor stays OFF: two attempts, both left a faint ghost above his hair in close-up (stills/crown3.jpg). The plate alone reads as natural hair
def spans_for(a, b):
    """Hair on the camera's top row per frame (median of 5 frames so the restored rows do not flicker). Only once the camera has come down onto it."""
    raw = {}
    lo = max(R0[0], a - 2); fr_ = decode(lo, b + 2 - lo)
    for lf in range(lo, b + 2):
        try: f = next(fr_)
        except (StopIteration, AssertionError): break
        if off(lf)[1] < 12 and os.path.exists(f"{D}/m/f_{lf+1:05d}.mask.png"): raw[lf] = hair_run(f[0][1].astype(np.float32), mask(lf)[1])
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
    key = hashlib.sha1(json.dumps([lf, n, vf, CROP, UP, REF_F, "v5", CROWN, GRAIN]).encode()).hexdigest()[:12]; out = f"{W}/cache/seg_mb2fix_{sg['src0']}_{key}.mp4"
    if os.path.exists(out): return out
    sp = spans_for(lf, lf + n) if CROWN else {}
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv444p", "-s", f"{cw}x{ch}", "-framerate", "30000/1001", "-color_range", "tv", "-colorspace", "bt709", "-i", "-",
                            "-vf", vf, "-an", "-c:v", "libx264", "-crf", "6", "-preset", "veryfast", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    for i, f in enumerate(decode(lf, n)): enc.stdin.write(crop_frame(canvas(f, lf + i, sp)).tobytes())
    enc.stdin.close(); enc.wait(); os.rename(out + ".tmp.mp4", out); return out
if __name__ == "__main__":
    os.makedirs(f"{D}/stills", exist_ok=True)
    for lf in [int(a) for a in sys.argv[2:]] or [80, 131, 160, 200, 230, 257, 272, 284, 300, 311, 335, 346]:
        f = next(decode(lf, 1)); sp = spans_for(lf - 2, lf + 3); c = canvas(f, lf, sp)
        for tag, cc in (("fix", c), ("plateonly", canvas(f, lf, {}))):
            y = crop_frame(cc); bgr = cv2.cvtColor(np.transpose(y, (1, 2, 0)), cv2.COLOR_YUV2BGR)   # rough preview only (the build grades it)
            cv2.imwrite(f"{D}/stills/{tag}_{lf:04d}.jpg", cv2.resize(bgr, (1920, 1080), interpolation=cv2.INTER_LANCZOS4), [cv2.IMWRITE_JPEG_QUALITY, 92])
        print(lf, "span", sp.get(lf), "off", off(lf))
