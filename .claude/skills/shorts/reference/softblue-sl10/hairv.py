#!/usr/bin/env python3
"""SL-10 hair clearance on the EXACT delivered short (VIDEO-RULES 2026-10-20, head and hair clearance).
Every 0.25 s of presenter picture plus the first and last native frame of every talking shot: the delivered 1080x1920 frame,
the Vision person mask (largest component, a row counts when >= 12 px of it are person), his head columns (mask at the top
120 rows of the person), and the TOP of the person inside the picture area (canvas y 310 down). Clearance = person top - 310.
Calibrated on this set: the studio backdrop is a mottled dark green-grey, the mask separates his dark hair from it (checked on
the native-scale proof sheet hair_proof_<S>.jpg, the tightest samples, which the executor LOOKS at).
FAIL: any valid sample under 20 px, or any talking sample where no person is found (an unresolved sample is not a pass).
EVERY FRAME edge test, independent of the mask's top: in his head columns (from the nearest mask sample), the share of
hair-dark pixels (luma < DARK, set from this backdrop: its own share is printed as the calibration) in the picture's top 6 rows
(canvas y 310-316) must stay under 0.20 on every talking frame. Hair touching the edge reads 0.5+.
  python3 hairv.py S VIDEO"""
import json, os, subprocess, sys, glob, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import batch as Bt
PM = Bt.PM; FF = Bt.lib.FF; FPS = Bt.FPS; DROP = 310; MIN = 20; DARK = 32; EDGE_MAX = 0.20
SP = os.environ.get("HAIRV_TMP", "/private/tmp/claude-501/sl10_hairv")
def main(S, V):
    shots = json.load(open(f"{Bt.D(S)}/shots.json"))
    DANCLIPS = set()      # SL-10: no B-roll of Dan in these four Shorts
    talk = [sh for sh in shots if sh["kind"] == "talk" or (sh["kind"] == "clip" and sh.get("cover", {}).get("id") in DANCLIPS)]
    want = set()
    for sh in talk:
        want |= set(range(sh["f0"], sh["f1"], 8)); want |= {sh["f0"], sh["f1"] - 1}
    want = sorted(want); td = f"{SP}/{S}"; os.makedirs(td + "/m", exist_ok=True)
    for f in glob.glob(td + "/*.png") + glob.glob(td + "/m/*"): os.remove(f)
    sel = "+".join(f"eq(n\\,{i})" for i in want)
    subprocess.run([FF, "-nostdin", "-v", "error", "-i", V, "-vf", f"select='{sel}',scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-vsync", "0", f"{td}/f_%05d.png"], check=True)
    fs = sorted(glob.glob(td + "/f_*.png")); assert len(fs) == len(want), (len(fs), len(want))
    subprocess.run([PM, td + "/m"] + fs, check=True, capture_output=True)
    rows = []
    for i, f in zip(want, fs):
        m = np.array(Image.open(f"{td}/m/{os.path.basename(f)[:-4]}.mask.png")) > 127
        m[:DROP] = False; m[1412:] = False                       # the picture area above the caption band
        lab, n = ndimage.label(m)
        if not n: rows.append(dict(f=i, t=round(i / FPS, 3), top=None)); continue
        b = lab == (int(np.argmax(ndimage.sum(m, lab, range(1, n + 1)))) + 1)
        rr = np.where(b.sum(1) >= 12)[0]
        rows.append(dict(f=i, t=round(i / FPS, 3), top=int(rr[0]) - DROP if len(rr) else None, png=f))
    bad = [r for r in rows if r["top"] is None or r["top"] < MIN]
    valid = [r for r in rows if r["top"] is not None]
    tight = sorted(valid, key=lambda r: r["top"])[:6]
    tiles = []
    for r in tight:
        im = Image.open(r["png"]).crop((240, DROP - 40, 840, DROP + 260)); d = ImageDraw.Draw(im)
        d.line((0, 40, 600, 40), fill=(255, 0, 0)); d.line((0, 40 + r["top"], 600, 40 + r["top"]), fill=(0, 255, 0))
        d.text((6, 4), f"{S} {r['t']:.2f}s clearance {r['top']} px", fill=(255, 255, 0)); tiles.append(im)
    if tiles:
        sh_ = Image.new("RGB", (600 * 3, 300 * ((len(tiles) + 2) // 3)))
        for k, im in enumerate(tiles): sh_.paste(im, ((k % 3) * 600, (k // 3) * 300))
        sh_.save(f"{Bt.D(S)}/gate/hair_proof_{S}.jpg", quality=90)
    # every frame: top 6 picture rows in the head columns
    heads = {}
    for r in rows:
        if r["top"] is None: continue
        m = np.array(Image.open(f"{td}/m/{os.path.basename(r['png'])[:-4]}.mask.png")) > 127
        band = m[DROP + r["top"]:DROP + r["top"] + 90]; cols = np.where(band.any(0))[0]
        if len(cols): heads[r["f"]] = (int(cols[0]), int(cols[-1]) + 1)
    hk = sorted(heads); talkf = [i for sh in talk if sh["kind"] == "talk" for i in range(sh["f0"], sh["f1"])]      # edge test calibrated on the studio backdrop only (dark trees read as hair outdoors)
    p = subprocess.Popen([FF, "-v", "error", "-i", V, "-vf", f"crop=1080:6:0:{DROP},format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    edge, bgd, n = [], [], 0; ts = set(talkf)
    while True:
        b = p.stdout.read(1080 * 6)
        if len(b) < 1080 * 6: break
        if n in ts and hk:
            g = np.frombuffer(b, np.uint8).reshape(6, 1080); k = min(hk, key=lambda x: abs(x - n)); c0, c1 = heads[k]
            edge.append((n, float((g[:, c0:c1] < DARK).mean()))); out_ = np.r_[0:max(0, c0 - 40), min(1080, c1 + 40):1080]
            if len(out_): bgd.append(float((g[:, out_] < DARK).mean()))
        n += 1
    p.wait()
    ebad = [(round(i / FPS, 3), round(v, 2)) for i, v in edge if v > EDGE_MAX]
    if ebad: bad = bad + [dict(t=t, top="edge %.2f" % v) for t, v in ebad]
    res_edge = dict(frames=len(edge), max_share=round(max(v for _, v in edge), 3) if edge else None, backdrop_share_median=round(float(np.median(bgd)), 3) if bgd else None, fails=ebad[:20])
    res = dict(edge_every_frame=res_edge, video=V, samples=len(rows), checked_frames=sum(sh["f1"] - sh["f0"] for sh in talk), min_px=min(r["top"] for r in valid) if valid else None,
               median_px=float(np.median([r["top"] for r in valid])) if valid else None, fails=[dict(t=r["t"], top=r["top"]) for r in bad],
               tightest=[dict(t=r["t"], top=r["top"]) for r in tight], verdict="PASS" if not bad else "FAIL")
    json.dump(res, open(f"{Bt.D(S)}/gate/hair_clearance.json", "w"), indent=1)
    print(S, "edge every frame:", res_edge)
    print(S, res["verdict"], "samples", res["samples"], "min", res["min_px"], "median", res["median_px"], "fails", res["fails"][:6])
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
