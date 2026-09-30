"""Verify HyperFrames graphics on a rendered composite: clearance, face, card fill. Run on the film render (or a
review section of it), never on the overlays alone.

    python3 checks.py manifest.json --film film.mp4 --film-t0 <film s of frame 0> --out CHECK_DIR [--min-clear 60]

Every 10th frame while a graphic is up:
  * side cards (3A side list, cycle): the Vision person mask (shorts/reference/recentre/personmask) must stay right of
    the card's right edge; the closest person pixel minus the edge is the clearance (round 2 minimum: 78 px).
  * lower thirds: the Vision face box (facebox.swift) must end above the strip top (y 840) with a margin.
  * card fill (side list, cycle): the median of a text-free patch just inside the card's bottom edge must read
    (10, 38, 72) +/- 2 once the card has settled (0.6 s after its in, 0.5 s before its out).
Writes CHECK_DIR/checks.json and one contact sheet per graphic (<id>_every10th.jpg, red line = card edge / strip top).
Exit code 1 if any check fails.
"""
import argparse, json, os, pathlib, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import composite as C                                     # noqa: E402
PERSONMASK = HERE.parent.parent / "shorts/reference/recentre/personmask"
FACEBOX = pathlib.Path.home() / ".cache/absbyai/facebox"
FILL = (10, 38, 72); STRIP_TOP = 840


def facebox_bin():
    if not FACEBOX.exists():
        FACEBOX.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["swiftc", "-O", str(HERE / "facebox.swift"), "-o", str(FACEBOX)], check=True)
    return str(FACEBOX)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest"); ap.add_argument("--film", required=True); ap.add_argument("--film-t0", type=float, default=0.0)
    ap.add_argument("--out", required=True); ap.add_argument("--min-clear", type=int, default=60); ap.add_argument("--every", type=int, default=10)
    A = ap.parse_args()
    out = pathlib.Path(A.out); (out / "frames").mkdir(parents=True, exist_ok=True)
    man = json.load(open(A.manifest)); g_film = C.fr(A.film_t0)
    want = {}                                              # film frame -> [item ids]
    for m in man:
        g0, g1 = C.fr(m["a"]), C.fr(m["b"])
        for g in range(g0, g1, A.every): want.setdefault(g, []).append(m["id"])
        if m.get("card"):                                   # the settled frames for the fill patch
            for g in (g0 + 18, (g0 + g1) // 2, g1 - 15): want.setdefault(g, []).append(m["id"] + "#fill")
    saved = {}
    for i, f in enumerate(C.reader(A.film)):
        g = g_film + i
        if g in want:
            p = out / "frames" / f"{g}.png"; Image.fromarray(np.ascontiguousarray(f)).save(p); saved[g] = p
    byid = {m["id"]: m for m in man}; res = {m["id"]: dict(id=m["id"], template=m["template"], frames=0) for m in man if C.fr(m["a"]) >= g_film}
    # person masks for side cards, face boxes for lower thirds, in batches
    card_frames = sorted({g for g, ids in want.items() if g in saved and any(byid[x.split('#')[0]].get("card_right") and '#' not in x for x in ids)})
    lt_frames = sorted({g for g, ids in want.items() if g in saved and any(byid[x.split('#')[0]]["template"] == "lower-third" for x in ids)})
    if card_frames:
        subprocess.run([str(PERSONMASK), str(out / "masks")] + [str(saved[g]) for g in card_frames], check=True, capture_output=True)
    faces = {}
    if lt_frames:
        r = subprocess.run([facebox_bin()] + [str(saved[g]) for g in lt_frames], capture_output=True, text=True, check=True).stdout
        for line in r.strip().splitlines():
            path, box = line.split("\t"); g = int(pathlib.Path(path).stem)
            faces[g] = None if box in ("none", "error") else [int(v) for v in box.split()]
    thumbs = {}
    for g in sorted(want):
        if g not in saved: continue
        im = Image.open(saved[g]).convert("RGB"); arr = np.asarray(im)
        for key in want[g]:
            iid = key.split("#")[0]; m = byid[iid]; r = res.get(iid)
            if r is None: continue
            t = g / C.FPS
            if key.endswith("#fill"):
                # the card's own fill as the compositor decodes it (BT.601 rule) must be the spec; on the composite
                # the 91 % card lets 9 % of the footage through, so that reading is reported, bounded at +/- 8
                x0, y0, x1, y1 = m["card"]; sl = (slice(y1 - 26, y1 - 14), slice(x0 + 40, x1 - 40))
                ov = next(C.reader(m["mov"], g - C.fr(m["a"]), 1, rgba=True))
                own = [int(v) for v in np.median(ov[sl][..., :3].reshape(-1, 3), axis=0)]; al = int(np.median(ov[sl][..., 3]))
                comp = [int(v) for v in np.median(arr[sl].reshape(-1, 3), axis=0)]
                ok = all(abs(a - b) <= 2 for a, b in zip(own, FILL)) and abs(al - 232) <= 3 and all(abs(a - b) <= 8 for a, b in zip(comp, FILL))
                r.setdefault("fill", []).append(dict(t=round(t, 2), rgb=own, alpha=al, composite=comp, ok=ok))
                continue
            r["frames"] += 1; lab = f"{t:.2f}s"
            if m.get("card_right"):
                mk = np.asarray(Image.open(out / "masks" / f"{g}.mask.png").convert("L")) > 127
                cols = np.nonzero(mk.sum(axis=0) > 6)[0]
                xmin = int(cols.min()) if len(cols) else None
                clear = None if xmin is None else xmin - m["card_right"]
                if clear is not None and (r.get("min_clear") is None or clear < r["min_clear"]): r["min_clear"], r["min_clear_t"] = clear, round(t, 2)
                lab += f"  person from x {xmin} ({clear} px clear)"
                line = ("v", m["card_right"])
            elif m["template"] == "lower-third":
                fb = faces.get(g)
                gap = None if fb is None else STRIP_TOP - fb[3]
                if gap is not None and (r.get("min_face_gap") is None or gap < r["min_face_gap"]): r["min_face_gap"], r["min_face_gap_t"] = gap, round(t, 2)
                if fb is None: r["no_face"] = r.get("no_face", 0) + 1
                lab += f"  face bottom {None if fb is None else fb[3]} (strip {STRIP_TOP})"
                line = ("h", STRIP_TOP)
            else:
                line = None
            th = im.resize((480, 270)); d = ImageDraw.Draw(th)
            if line and line[0] == "v": d.line((line[1] / 4, 0, line[1] / 4, 270), fill=(255, 60, 60))
            if line and line[0] == "h": d.line((0, line[1] / 4, 480, line[1] / 4), fill=(255, 60, 60))
            d.rectangle((0, 0, 480, 16), fill=(0, 0, 0)); d.text((4, 2), lab, fill=(255, 255, 255))
            thumbs.setdefault(iid, []).append(th)
    for iid, ths in thumbs.items():
        cols = 4; rows = (len(ths) + cols - 1) // cols; sh = Image.new("RGB", (480 * cols, 270 * rows))
        for k, th in enumerate(ths): sh.paste(th, ((k % cols) * 480, (k // cols) * 270))
        sh.save(out / f"{iid}_every10th.jpg", quality=82)
    fail = []
    for r in res.values():
        if r.get("min_clear") is not None and r["min_clear"] < A.min_clear: fail.append(f"{r['id']}: person {r['min_clear']} px from the card at {r['min_clear_t']} s")
        if r.get("min_face_gap") is not None and r["min_face_gap"] < 40: fail.append(f"{r['id']}: face ends {r['min_face_gap']} px above the strip at {r['min_face_gap_t']} s")
        for f in r.get("fill", []):
            if not f["ok"]: fail.append(f"{r['id']}: card fill {f['rgb']} at {f['t']} s (want {list(FILL)} +/- 2)")
    json.dump(dict(film=A.film, items=list(res.values()), failures=fail), open(out / "checks.json", "w"), indent=1)
    for r in res.values(): print({k: v for k, v in r.items() if k != "fill"}, [f["rgb"] for f in r.get("fill", [])])
    print("FAIL" if fail else "PASS", *fail, sep="\n  ")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
