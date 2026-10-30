"""RO-37 round 2 lower thirds: round 1's approved copy, parts and word times unchanged, re-laid out for the cut-out Dan
(Dan's rule for this round: lower thirds sit beside or below him, never across his face or abs). Under a lower third Dan
stands right (W), so the strip ends left of his body: its right edge is measured from the mattes (the leftmost edge of his
silhouette in the strip's rows over the whole lower third, minus 28 px), and a point too long for one line wraps onto a
second line at a part boundary. Same Soft Blue Light HyperFrames template (shared lower-third/build.py, imported, not
changed); this file only computes the layout it is given.
  python3 lt2.py [--render] [--only G02,G03]   -> round2/hf/lt/<id>.mov + _mask.mov, round2/hf/lt/layout.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2
import numpy as np, cv2
HFD = f"{r2.P}/.claude/skills/_shared/hyperframes"
sys.path.insert(0, HFD)
import hfbuild as H                                   # noqa: E402
import importlib.util                                 # the shared lower-third builder ('build' is round 1's module name here)
_spec = importlib.util.spec_from_file_location("lt_build", f"{HFD}/lower-third/build.py"); LT = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(LT)
OUT = f"{r2.W2}/hf/lt"; U = LT.U; PAD_R = 48 + 16


def silhouette_left(shots, plan, y0, y1):
    """Left edge (screen x) of Dan's TORSO in rows y0..y1 over these shots (every 3rd frame): per row the solid run of his
    silhouette that contains his body centre (a hand held out to the side is a separate run and does not count), the
    frame's value is its leftmost row; the 10th percentile over frames (a hand in front of his waist for a moment may
    sit under the strip's end; his face and abs never do). The 5th-percentile full silhouette edge is kept for the record."""
    tor, full = [], []
    for s in shots:
        place, framing = r2.placement(s, r2.seg_type(plan, s))
        if place == "closeup": continue
        k0 = r2.src_index(s["src0"]); n = s["out_f1"] - s["out_f0"]
        top, cx = r2.shot_geo(s)
        k, ox, oy = r2.affine(place, framing, top, cx)
        sx = k * r2.SW / r2.MW; cc = int((cx * k + ox - ox) / sx)        # body centre column in matte pixels
        for j in list(range(0, n, 3)) + [n - 1]:
            p = r2.mpath(s["roll"], k0 + j)
            if not os.path.exists(p): continue
            a = cv2.imread(p, cv2.IMREAD_GRAYSCALE) > 128
            ra, rb = int(max(0, (y0 - oy) / sx)), int(min(r2.MH, (y1 - oy) / sx))
            if rb <= ra: continue
            lefts = []
            for row in a[ra:rb:4]:
                if not row[cc]: continue
                z = np.where(~row[:cc])[0]; lefts.append((z[-1] + 1) if len(z) else 0)
            if lefts: tor.append(min(lefts) * sx + ox)
            cols = np.where(a[ra:rb].any(0))[0]
            if len(cols): full.append(cols[0] * sx + ox)
    if not tor: return None, None
    return float(np.percentile(tor, 10)), float(np.percentile(full, 5)) if full else None


def layout(topic, parts, strip_right, topic_case="preserve"):
    """The shared layout with the strip ending at strip_right; a point wider than the strip wraps at a part boundary
    onto a second line (the template sets parts with their own y, as on 9:16)."""
    x0, _, _, _ = LT.B.lower_third_default_box(LT.W, LT.Hh)
    tx = x0 + 31 * U; px = 28 * U
    point = " ".join(p for p, _ in parts); wrap_w = strip_right - x0 - 31 * U - 24 * U
    lines = [[p for p, _ in parts]]
    if H.text_w(point, px) > wrap_w:
        best = None
        for i in range(1, len(parts)):
            a, b = " ".join(p for p, _ in parts[:i]), " ".join(p for p, _ in parts[i:])
            w = max(H.text_w(a, px), H.text_w(b, px))
            if best is None or w < best[0]: best = (w, i)
        assert best and best[0] <= wrap_w, f"{point!r} does not fit in two lines of {wrap_w:.0f} px"
        lines = [[p for p, _ in parts[:best[1]]], [p for p, _ in parts[best[1]:]]]
    nl = len(lines)
    _, ytop, _, bh = LT.B.lower_third_default_box(LT.W, LT.Hh, nl)
    text_w = max(H.text_w(" ".join(l), px) for l in lines)
    x1 = min(strip_right, round(tx + text_w + PAD_R))      # the strip hugs its text: as far from Dan as it can be
    L = dict(strip=[x0, ytop, x1 - x0 + 1, bh + 1], radius=18 * U, accent=[x0 + U, ytop + 3 * U, 8 * U, bh - 6 * U],
             topic=dict(x=tx, y=ytop + 13 * U, s=topic if topic_case == "preserve" else topic.upper()), point_y=ytop + 38 * U, parts=[])
    for n, l in enumerate(lines):
        acc = ""
        for p in l:
            L["parts"].append(dict(s=p, x=round(tx + (H.text_w(acc + " ", px) if acc else 0), 1), y=ytop + 38 * U + n * 36 * U))
            acc = (acc + " " + p).strip()
    return L, nl, x1


def main():
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
    plan = json.load(open(f"{r2.W2}/bg_plan.json"))["segments"]; shots = r2.final_shots(plan)
    cfgs = {}
    for f in sorted(os.listdir(f"{r2.R1}/hf/configs/lower-third")):
        if f.endswith(".json") and not f.startswith("._"):
            for c in json.load(open(f"{r2.R1}/hf/configs/lower-third/{f}")): cfgs[c["id"]] = c
    lay_path = f"{OUT}/layout.json"; lay = json.load(open(lay_path)) if os.path.exists(lay_path) else {}
    scenes = []
    for gid, c in sorted(cfgs.items()):
        if only and gid not in only: continue
        under = [s for s in shots if s["lt"] == gid]
        _, ytop2, _, _ = LT.B.lower_third_default_box(LT.W, LT.Hh, 2)
        left, hands = silhouette_left(under, plan, ytop2, 1016)
        assert left is not None, f"{gid}: no mattes under it yet"
        sr = int(min(1828, left - 28))
        L, nl, x1 = layout(c["topic"], c["parts"], sr, c.get("topic_case", "preserve"))
        lay[gid] = dict(torso_left=round(left), hands_left=round(hands) if hands else None, strip_right=x1, lines=nl, band=[int(L["strip"][1]) - 8, 1080])
        print(f"{gid}: torso edge {left:.0f} (hands reach {hands or 0:.0f}), strip ends {x1}, {nl} line(s): {' / '.join(p['s'] for p in L['parts'])}", flush=True)
        for mode in ("content", "mask"):
            cfg = dict(id=gid + ("_mask" if mode == "mask" else ""), mode=mode, dur=round(c["b"] - c["a"], 3), drift=c.get("drift", -4),
                       times=[H.rel(t, c["a"]) for _, t in c["parts"]], **L)
            scenes.append((LT.HERE / "lower-third.template.htm", cfg, ()))
    json.dump(lay, open(lay_path, "w"), indent=1)
    H.run_all(scenes, OUT, "--render" in sys.argv)
    # the round 2 manifest: round 1's items with every lower third replaced by its round 2 render
    man = json.load(open(f"{r2.R1}/hf/manifest.json"))
    for m in man:
        if m["template"] == "lower-third" and m["id"] in lay and os.path.exists(f"{OUT}/{m['id']}.mov"):
            m.update(mov=f"{OUT}/{m['id']}.mov", mask=f"{OUT}/{m['id']}_mask.mov", band=lay[m["id"]]["band"], r2=True)
    json.dump(man, open(f"{r2.W2}/hf/manifest2.json", "w"), indent=1)


if __name__ == "__main__":
    main()
