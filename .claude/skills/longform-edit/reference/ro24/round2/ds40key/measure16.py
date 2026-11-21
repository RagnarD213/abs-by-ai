"""R2 measurement harness: the R1 reviewer's own formulas (audit3/scripts pass2.py, outline.py, seethru4.py,
islands.py), merged into one decode pass and pointed at any candidate pair.

    python3 measure16.py PALE.mp4 NAVY.mp4 OUT.json F0 NFRAMES

flicker  = pass2.py edge-band frame-to-frame alpha change, output vs source (plus the same restricted to the hair box)
rim      = outline.py dark-rim fraction on skin edges (pale)
seethru  = seethru4.py blue-cast pixels inside Dan at the wrist (navy + pale)
islands  = islands.py floating specks (pale)
"""
import numpy as np, subprocess, json, sys
from scipy import ndimage as ndi
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1726.MP4"
FPS = 30000 / 1001
W, H = 1920, 1080; OY = 0
VF = "scale=in_color_matrix=bt709:in_range=tv"
HAIR = (slice(40, 240), slice(780, 1220))   # output y, x: the hair above the glasses

def reader(args):
    p = subprocess.Popen([FF, "-v", "error"] + args + ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)

def main(pale, navy, out, f0, nf):
    global F0, NF; F0, NF = int(f0), int(nf)
    po = reader(["-i", pale, "-vf", VF]); pn = reader(["-i", navy, "-vf", VF])
    ps = reader(["-ss", f"{(F0 - 0.3) / FPS:.5f}", "-i", SRC, "-frames:v", str(NF), "-vf", VF + ":w=1920:h=1080:flags=area"])
    BG = np.array([216, 225, 235], np.int16); BGf = BG.astype(np.float32)
    bgl = 0.2126 * 216 + 0.7152 * 225 + 0.0722 * 235
    st = np.ones((3, 3), bool)
    rows = []; prev = None
    hair_band = np.zeros((H, W), bool); hair_band[HAIR] = True
    for i, (o8, n8, s0) in enumerate(zip(po, pn, ps)):
        o = o8.astype(np.int16)
        s = np.zeros((H, W, 3), np.int16); s[..., 1] = 200; s[OY:] = s0[:H - OY]
        gs = s[..., 1] - np.maximum(s[..., 0], s[..., 2])
        d = np.abs(o - BG).max(-1)
        fgo = d > 40
        band = ndi.binary_dilation(fgo, st, iterations=3) & ~ndi.binary_erosion(fgo, st, iterations=3)
        ao = np.clip((d - 8) / 60.0, 0, 1); as_ = np.clip((45 - gs) / 45.0, 0, 1)
        rec = dict(i=i)
        if prev is not None:
            pb = prev[2] | band
            rec['flick_out'] = float(np.abs(ao - prev[0])[pb].mean()); rec['flick_src'] = float(np.abs(as_ - prev[1])[pb].mean())
            hb = pb & hair_band
            rec['hair_out'] = float(np.abs(ao - prev[0])[hb].mean()); rec['hair_src'] = float(np.abs(as_ - prev[1])[hb].mean())
        prev = (ao, as_, band)
        # rim (outline.py)
        of = o8.astype(np.float32); L = of @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        df = np.abs(of - BGf).max(-1)
        ms = ndi.gaussian_filter((df > 60).astype(np.float32), 2)
        gy, gx = np.gradient(ms)
        edge = (np.abs(ms - 0.5) < 0.08) & (np.hypot(gx, gy) > 0.05)
        ys, xs = np.nonzero(edge); ys = ys[::3]; xs = xs[::3]
        gn = np.hypot(gx[ys, xs], gy[ys, xs]); nx = gx[ys, xs] / gn; ny = gy[ys, xs] / gn
        ts = np.arange(-6, 7)
        px = np.clip((xs[:, None] + nx[:, None] * ts).round().astype(int), 0, W - 1)
        py = np.clip((ys[:, None] + ny[:, None] * ts).round().astype(int), 0, H - 1)
        prof = L[py, px]; inner = of[py[:, -1], px[:, -1]]
        skin = (inner[:, 0] > 110) & (inner[:, 0] > inner[:, 1] + 12) & (inner[:, 1] > inner[:, 2])
        sel = skin & (df[py[:, 0], px[:, 0]] < 15)
        if sel.any():
            dip = np.minimum(prof[sel][:, -1], bgl) - prof[sel].min(1)
            rec['rim_n'] = int(sel.sum()); rec['rim_dark'] = int((dip > 20).sum()); rec['rim_p95'] = float(np.percentile(dip, 95))
        else:
            rec['rim_n'] = 0; rec['rim_dark'] = 0; rec['rim_p95'] = 0.0
        # see-through at the wrist (seethru4.py)
        b = n8.astype(np.int16)
        body = d > 40
        lab, n = ndi.label(body); body = lab == (np.argmax(ndi.sum(body, lab, range(1, n + 1))) + 1)
        holes = ndi.binary_fill_holes(body) & ~body
        hl, hn = ndi.label(holes)
        if hn:
            hs = ndi.sum(holes, hl, range(1, hn + 1)); body = body | np.isin(hl, np.nonzero(hs < 600)[0] + 1)
        inner2 = ndi.binary_erosion(body, st, iterations=2)
        blue = (b[..., 2] - b[..., 0] > 25) & (b[..., 2] - b[..., 1] > 12)
        see = inner2 & blue & (o[..., 2] - o[..., 0] > 4) & (d >= 20); pass                       # RO-24: whole frame (head-region hits are the glasses arm, reported by box)
        see = ndi.binary_opening(see, np.ones((2, 2), bool))
        rec['see'] = int(see.sum())
        if see.any():
            yy, xx = np.nonzero(see); rec['see_box'] = [int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())]
        # floating specks (islands.py)
        fg = d > 15
        lab, n = ndi.label(fg, np.ones((3, 3)))
        sz = ndi.sum(fg, lab, range(1, n + 1)); main_ = np.argmax(sz) + 1
        bodyd = ndi.binary_dilation(lab == main_, st, iterations=3)
        k = 0; sp = []
        for j, sl in enumerate(ndi.find_objects(lab)):
            if j + 1 == main_: continue
            comp = lab[sl] == j + 1
            if (comp & bodyd[sl]).any(): continue
            k += 1; sp.append([int(sz[j]), sl[1].start, sl[0].start, int(d[sl][comp].max())])
        rec['specks'] = k
        if sp: rec['speck_list'] = sp
        rows.append(rec)
        if i % 60 == 0: print(i, {k_: rec[k_] for k_ in rec if k_ not in ('speck_list',)}, flush=True)
    fl = [r for r in rows if 'flick_out' in r]
    ratio = [r['flick_out'] / r['flick_src'] for r in fl]
    hratio = [r['hair_out'] / r['hair_src'] for r in fl if r['hair_src'] > 0]
    summ = dict(frames=len(rows),
                flicker_ratio_mean=round(float(np.mean(ratio)), 3), flicker_ratio_worst=round(float(np.max(ratio)), 3),
                flicker_ratio_worst_frame=int(fl[int(np.argmax(ratio))]['i']),
                hair_flicker_ratio_mean=round(float(np.mean(hratio)), 3), hair_flicker_ratio_worst=round(float(np.max(hratio)), 3),
                rim_fraction=round(float(np.mean([r['rim_dark'] / max(1, r['rim_n']) for r in rows])), 4),
                rim_p95_median=round(float(np.median([r['rim_p95'] for r in rows])), 1),
                seethru_frames=[r['i'] for r in rows if r['see'] > 0], seethru_px_total=int(sum(r['see'] for r in rows)),
                speck_frames=[r['i'] for r in rows if r['specks']], speck_total=int(sum(r['specks'] for r in rows)))
    json.dump(dict(summary=summ, frames=rows), open(out, "w"), indent=0)
    print(json.dumps(summ))

if __name__ == "__main__":
    main(*sys.argv[1:6])
