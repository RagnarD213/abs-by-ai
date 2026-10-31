"""RO-37 round 2 picture for a film range: Dan cut out of the upright pool footage (colour F, BiRefNet matte with the
3-frame median, the approved test's soft drop shadow, a 22 px feather where the upright frame's own edge is on screen),
placed per shot (r2.placement) on the locked green-screen background template (gsbg, bg_plan.json), his gym clips full
screen where round 1 put them (round 1's tune and labels), the pool close-up at r2.CLOSEUPS, then every graphic
(HyperFrames compositor, round 2 lower thirds). Hair is measured on every rendered cut-out frame (VIDEO-RULES 2026-10-20).

  assemble.py OUT.mp4 --t0 0 --t1 61.0944          (video only; mux.sh adds the voice)
  assemble.py STILL.jpg --frame 1234                (one frame, for stills)
Writes OUT.mp4.build.json: every run (film frames, kind, shot, placement, background, rect) and the hair rows."""
import argparse, json, os, subprocess, sys, time
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2
sys.path.insert(0, f"{r2.P}/.claude/skills/_shared/greenscreen-bg"); import gsbg as G           # noqa: E402
sys.path.insert(0, f"{r2.P}/.claude/skills/_shared/hyperframes"); import composite as HC        # noqa: E402
FPS = r2.FPS; OW, OH = 1920, 1080; FEATHER = 22
TO_RGB = "scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24"
CLIPMAP = {"list": "plain"}


def writer(path):
    return subprocess.Popen([r2.FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", "30000/1001", "-i", "-",
                             "-an", "-vf", "scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p", "-c:v", "libx264",
                             "-crf", "14", "-preset", "medium", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                             "-movflags", "+faststart", path], stdin=subprocess.PIPE)


class Raw:
    """Sequential rgb24 frames of an ffmpeg decode."""
    def __init__(self, args, w, h):
        self.w, self.h = w, h
        self.p = subprocess.Popen([r2.FF, "-nostdin", "-v", "error"] + args + ["-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    def read(self):
        raw = self.p.stdout.read(self.w * self.h * 3); assert len(raw) == self.w * self.h * 3, "decode ended early"
        return np.frombuffer(raw, np.uint8).reshape(self.h, self.w, 3)
    def close(self):
        self.p.stdout.close(); self.p.wait()


def clip_reader(it, q0, n):
    """round 1's full-screen gym clip (render_clip), as frames from film frame q0. Round 3's AI inserts are finished files."""
    if it["kind"] == "ai3":
        return Raw(["-ss", f"{(q0 - r2.fr(it['t0'])) / FPS:.6f}", "-i", it["file"], "-frames:v", str(n), "-fps_mode", "passthrough", "-vf", TO_RGB], OW, OH), None
    cid, s0 = it["src"].split("@")[0], float(it["src"].split("@")[1])
    g = json.load(open(f"{r2.R1}/broll/grade.json")).get(f"{cid}@{s0}", {})
    import broll_tune as BT
    path = g.get("path") or BT.path(cid); vf = g.get("vf", "")
    dur = float(subprocess.check_output([r2.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]))
    s0 = max(0.0, min(s0, dur - (it["t1"] - it["t0"]) - 0.05))     # a take shorter than its slot from round 1's in point starts earlier (never a held frame)
    ts = s0 + (q0 - r2.fr(it["t0"])) / FPS
    rd = Raw(["-ss", f"{ts:.4f}", "-i", path, "-frames:v", str(n), "-fps_mode", "passthrough", "-vf", f"{r2.F.DEC},{vf + ',' if vf else ''}scale=1920:1080:flags=lanczos,{TO_RGB}"], OW, OH)
    chip = None
    if it.get("chip"):
        c = cv2.imread(f"{r2.R1}/broll/chip_{it['id']}.png", cv2.IMREAD_UNCHANGED)
        chip = (c[..., 2::-1].astype(np.float32), c[..., 3:4].astype(np.float32) / 255)
    return rd, chip


from gapfix import gapmask, skinfill, softmotion


class Presenter:
    """One run of a cut-out shot: graded source frames scaled to the placement, the matte (3-frame median) scaled with it."""
    def __init__(self, s, q0, n, place, framing):
        self.s = s; top, cx = r2.shot_geo(s)
        self.k, self.ox, self.oy = r2.affine(place, framing, top, cx)
        self.ox += r2.DX.get(s["id"].split("~")[0], 0) if place == "right" else 0
        self.w, self.h = int(round(r2.SW * self.k / 2)) * 2, int(round(r2.SH * self.k / 2)) * 2
        self.kk = r2.src_index(s["src0"]) + (q0 - s["out_f0"])
        self.lo, self.hi = r2.src_index(s["src0"]), r2.src_index(s["src0"]) + (s["out_f1"] - s["out_f0"]) - 1
        self.rd = Raw(["-ss", f"{(self.kk - 0.5) / FPS:.6f}", "-i", r2.F.ROLLS[s["roll"]], "-frames:v", str(n + 1), "-fps_mode", "passthrough", "-vf",
                       f"{r2.F.DEC},{r2.F.GRADES[os.environ.get('RO37_GRADE', 'F')][1]},scale={self.w}:{self.h}:flags=lanczos:in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24"],
                      self.w, self.h)
        x, y = int(round(self.ox)), int(round(self.oy)); self.x, self.y = x, y
        r = np.ones((self.h, self.w), np.float32)
        if x > 0: r[:, :FEATHER] *= np.linspace(0, 1, FEATHER, dtype=np.float32)[None]
        if x + self.w < OW: r[:, -FEATHER:] *= np.linspace(1, 0, FEATHER, dtype=np.float32)[None]
        if y > 0: r[:FEATHER] *= np.linspace(0, 1, FEATHER, dtype=np.float32)[:, None]
        self.ramp = r; self.i = 0; self.prev = None; self.nxt = None
        self.rect = (x, y, self.w, self.h)

    def read(self):
        rgb = self.nxt if self.nxt is not None else self.rd.read(); k = self.kk + self.i; self.i += 1
        try: self.nxt = self.rd.read()
        except AssertionError: self.nxt = None
        nx = self.nxt if self.nxt is not None else rgb
        f = rgb.astype(np.float32); mot = np.abs(f - nx).max(2)
        if self.prev is not None: mot = np.maximum(mot, np.abs(f - self.prev).max(2))
        self.prev = f
        a = r2.alpha(self.s["roll"], k, self.lo, self.hi)
        a = cv2.resize(a, (self.w, self.h), interpolation=cv2.INTER_LINEAR)
        a = main_body(a)
        a = skinfill(rgb, a, mot)
        a = a * (1 - gapmask(rgb, a))
        a = softmotion(a, mot)
        rgb = decontaminate(rgb, a)
        return rgb, a * self.ramp, k

    def close(self): self.rd.close()


def main_body(a):
    """No floating specks: only the connected shape of him survives (a hand or a strand always joins him at some alpha)."""
    n, lab, st, _ = cv2.connectedComponentsWithStats((a > 0.04).astype(np.uint8), connectivity=8)
    if n <= 2: return a
    keep = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    return a * (lab == keep)


def decontaminate(rgb, a):
    """Round 3: a pixel on his edge is part hedge or bright wall, which printed as a pale line around him. The solved foreground
    colour (pymatting's estimate_foreground_ml) replaces the picture only in the edge band; the inside of him stays untouched."""
    from pymatting import estimate_foreground_ml
    Fg = estimate_foreground_ml(rgb.astype(np.float64) / 255, a.astype(np.float64), n_small_iterations=8, n_big_iterations=2)
    solid = cv2.erode((a > 0.98).astype(np.uint8), np.ones((5, 5), np.uint8)).astype(np.float32)
    w = 1 - cv2.GaussianBlur(solid, (0, 0), 1.5)
    out = rgb.astype(np.float32) * (1 - w[..., None]) + np.clip(Fg, 0, 1).astype(np.float32) * 255 * w[..., None]
    return out.astype(np.uint8)


def despill(rgb, a, y_limit):
    """The pool hedge behind him is green and shows through the soft hair edge: inside an 8 px band along the edge of
    his silhouette, above y_limit (hair, face, shoulders; never his green shorts), green is held to the larger of red and
    blue (the standard green despill), faded in by how close the pixel is to the edge."""
    hard = (a > 0.5).astype(np.uint8)
    inner = cv2.erode(hard, np.ones((17, 17), np.uint8))
    band = cv2.GaussianBlur((hard - inner).astype(np.float32), (0, 0), 3) * 1.6
    band[y_limit:] = 0
    if not band.any(): return rgb
    f = rgb.astype(np.float32); g = np.minimum(f[..., 1], np.maximum(f[..., 0], f[..., 2]))
    w = np.clip(band, 0, 1); f[..., 1] = f[..., 1] * (1 - w) + g * w
    return f.astype(np.uint8)


def compose(bg, rgb, a, rect):
    """The approved test's composite: a soft dark drop shadow (blur 18, offset 10/14, 55 %), then Dan over it."""
    x, y, w, h = rect
    X0, Y0, X1, Y1 = max(0, x), max(0, y), min(OW, x + w), min(OH, y + h)
    A = a[Y0 - y:Y1 - y, X0 - x:X1 - x]; Fg = rgb[Y0 - y:Y1 - y, X0 - x:X1 - x].astype(np.float32) * (1 / 255)
    sh = np.zeros((OH, OW), np.float32); sh[Y0:Y1, X0:X1] = A
    sh = cv2.GaussianBlur(sh, (0, 0), 18)
    M = np.float32([[1, 0, 10], [0, 1, 14]]); sh = cv2.warpAffine(sh, M, (OW, OH)) * 0.55
    dark = np.array([2, 8, 18], np.float32) / 255
    out = bg * (1 - sh[..., None]) + dark * sh[..., None]
    reg = out[Y0:Y1, X0:X1]
    out[Y0:Y1, X0:X1] = Fg * A[..., None] + reg * (1 - A[..., None])
    return out


def camera(place, framing, s):
    """camera-locked types (soft, the list's field): a tight cut zooms the background with him (gsbg.camera's idea)."""
    if framing == "W": return (1.0, 0.0, 0.0)
    top, cx = r2.shot_geo(s)
    kw, oxw, oyw = r2.affine(place, "W", top, cx); k, ox, oy = r2.affine(place, framing, top, cx)
    sc = k / kw; return (sc, ox - oxw * sc, oy - oyw * sc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--t0", type=float); ap.add_argument("--t1", type=float); ap.add_argument("--frame", type=int)
    ap.add_argument("--plan", default=f"{r2.W2}/bg_plan.json"); ap.add_argument("--manifest", default=f"{r2.W2}/hf/manifest2.json")
    ap.add_argument("--no-graphics", action="store_true")
    A = ap.parse_args()
    plan = json.load(open(A.plan))["segments"]; shots = r2.final_shots(plan)
    segf = [dict(g, f0=r2.fr(g["t0"]), f1=r2.fr(g["t1"])) for g in plan]
    C = None if A.no_graphics else HC.Compositor(json.load(open(A.manifest)))
    ctx = G.Context(r2.W2)
    g0, g1 = (A.frame, A.frame + 1) if A.frame is not None else (r2.fr(A.t0), min(r2.END_F, r2.fr(A.t1)))
    still = A.frame is not None
    wr = None if still else writer(A.out)
    def seg_of(q): return next((g for g in segf if g["f0"] <= q < g["f1"]), None)
    def shot_of(q): return next(s for s in shots if s["out_f0"] <= q < s["out_f1"])
    def clip_of(q): return next((r for r in r2.CLIPS if r2.fr(r["t0"]) <= q < r2.fr(r["t1"])), None)
    runs, hair, bgs = [], [], {}; t_start = time.time(); q = g0
    while q < g1:
        c = clip_of(q); s = shot_of(q); g = None if c else seg_of(q)
        e = q + 1
        while e < g1 and clip_of(e) is c and (c or (shot_of(e) is s and seg_of(e) is g)): e += 1
        n = e - q
        if c:
            rd, chip = clip_reader(c, q, n)
            for j in range(n):
                f = rd.read().astype(np.float32)
                if chip is not None:
                    hh, ww = chip[0].shape[:2]; reg = f[952:952 + hh, 64:64 + ww]
                    f[952:952 + hh, 64:64 + ww] = chip[0] * chip[1] + reg * (1 - chip[1])
                o8 = np.clip(f + .5, 0, 255).astype(np.uint8)
                if not A.no_graphics: o8 = C.apply(o8, q + j)
                out_frame(wr, o8, A.out, still)
            rd.close(); runs.append(dict(f0=q, f1=e, kind="clip", item=c["id"])); q = e; continue
        typ = g["type"] if g else "soft"
        place, framing = r2.placement(s, typ)
        if g and q / FPS < g.get("dan_corner_until", 0): place, framing = "corner", "T" if framing == "T" else "W"
        if place == "closeup":
            y = r2.F.t_y(s["roll"], s["src0"], s["src1"]); kk = r2.src_index(s["src0"]) + (q - s["out_f0"])
            rd = Raw(["-ss", f"{(kk - 0.5) / FPS:.6f}", "-i", r2.F.ROLLS[s["roll"]], "-frames:v", str(n), "-fps_mode", "passthrough", "-vf",
                      f"{r2.F.DEC},crop={r2.F.TW}:{r2.F.TH}:0:{y},scale=1920:1080:flags=lanczos,{r2.F.GRADES[os.environ.get('RO37_GRADE', 'F')][1]},{TO_RGB}"], OW, OH)
            for j in range(n):
                o8 = rd.read().copy()
                if not A.no_graphics: o8 = C.apply(o8, q + j)
                out_frame(wr, o8, A.out, still)
            rd.close(); runs.append(dict(f0=q, f1=e, kind="closeup", shot=s["id"], crop_y=y)); q = e; continue
        assert g is not None, f"film frame {q}: Dan on screen but no background segment"
        bg = bgs.get(g["id"])
        if bg is None:
            for kx in list(bgs): bgs.pop(kx).close()
            seg = dict(g, type=CLIPMAP.get(g["type"], g["type"]), frames=g["f1"] - g["f0"], t_field=round(g["t0"], 3))
            bg = bgs[g["id"]] = G.make_background(seg, ctx); bg._next = g["f0"]
        cam = camera(place, framing, s) if typ in ("soft", "list") else (1.0, 0.0, 0.0)
        pr = Presenter(s, q, n, place, framing)
        for j in range(n):
            qq = q + j
            while bg._next < qq: bg.frame(bg._next - g["f0"], cam); bg._next += 1
            img = bg.frame(qq - g["f0"], cam).copy(); bg._next = qq + 1
            top_bg = img[:420].copy()
            rgb, a, k = pr.read()
            img = compose(img, rgb, a, pr.rect)
            dd = (np.abs(img[:420] - top_bg).max(-1) > 14 / 255).sum(1) >= 3
            hair.append((qq, int(np.argmax(dd)) if dd.any() else None, framing, place, s["id"]))
            o8 = (np.clip(img, 0, 1) * 255 + .5).astype(np.uint8)
            if not A.no_graphics: o8 = C.apply(o8, qq)
            out_frame(wr, o8, A.out, still)
        pr.close()
        runs.append(dict(f0=q, f1=e, kind="presenter", shot=s["id"], roll=s["roll"], src_k0=pr.kk, framing=framing, placement=place,
                         bg=g["id"], bg_type=typ, rect=list(pr.rect), k=pr.k))
        q = e
        if not still: print(f"  {q - g0}/{g1 - g0} frames, {(q - g0) / (time.time() - t_start):.2f} fps", flush=True)
    for b in bgs.values(): b.close()
    if wr: wr.stdin.close(); assert wr.wait() == 0
    json.dump(dict(g0=g0, g1=g1, runs=runs, hair=hair, plan=A.plan, manifest=A.manifest), open(A.out + ".build.json", "w"), indent=1)
    print("ASSEMBLE DONE", A.out, g1 - g0, "frames", f"{(g1 - g0) / max(1e-6, time.time() - t_start):.2f} fps", flush=True)


def out_frame(wr, o8, path, still):
    if still: cv2.imwrite(path, np.ascontiguousarray(o8[:, :, ::-1]), [cv2.IMWRITE_JPEG_QUALITY, 93])
    else: wr.stdin.write(np.ascontiguousarray(o8).tobytes())


if __name__ == "__main__":
    main()
