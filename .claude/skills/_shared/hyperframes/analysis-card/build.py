"""Soft Blue Light ANALYSIS CARD (HyperFrames): THE standard "AI reads your picture" card for every video (Dan, 2026-10-14:
"Redo the analysis card in our graphics in soft blue light with our hyperframes. Make that standardized with the rest of
our videos."). It replaces the J2 card of `_shared/adkit/analysis_card.py` for every new film; that one stays only for
re-exports of films already approved with it (RA-01).

What it shows, unchanged from the RA-01 card Dan asked to reuse: the subject's picture with a scan line sweeping it once,
three label + bar rows (BODY FAT / FAT TO LOSE / MUSCLE TO GAIN) and the plan band (YOUR WORKOUT PLAN). An opaque scene on
the moving Soft Blue field: it cuts in and out on hard cuts (nothing fades in), the picture pushes in slowly and the card
drifts, so it never stops moving.

Rules it enforces (the RA-01 rules, do not route around them):
  * NO PRINTED NUMBERS. Rows are labels and bars; a digit in a label or the band stops the build.
  * One label chip: "AI-GENERATED" for an AI picture, "Real picture of me. Not AI-generated." for a real one, none only
    for a picture with no physique in it. It sits on the field UNDER the picture, so it can never touch his face or abs.
  * Same person as the video's before/after. The subject is the video's own person.
  * Every row lands on the word that starts its clause (`reveal`, film seconds); the band after the last row with at
    least 0.5 s to the out. Minimum length 3.5 s.

Config (one scene; film seconds, as from_plan.py resolves them):
  {"id": "A1", "a": 22.42, "b": 26.59, "photo": "/abs/path/goal.png", "label": "AI-GENERATED",
   "rows": ["BODY FAT", "FAT TO LOSE", "MUSCLE TO GAIN"],        # optional (these are the default)
   "levels": [0.58, 0.42, 0.66],                                  # optional: how full each bar ends (0.15..0.85)
   "reveal": [24.06, 24.66, 25.40],                               # one per row
   "band": ["YOUR WORKOUT PLAN", 25.82],
   "scan": [22.52, 23.70],                                        # optional: default a+0.1 .. min(a+1.4, first reveal-0.1)
   "push": 1.05, "drift": -6}

Layouts (one function, every aspect: `layout(s, canvas, bottom)`):
  16:9  picture left (cover crop, top anchored, aspect 0.86), chip under it, glass card right with the rows inline
  9:16  picture on top, chip under it, glass card full width beneath, ending `bottom` (24 px above the caption line)
  1:1   picture left, chip under it, glass card right with each label above its bar, ending above the caption line

    python3 build.py config.json OUT_DIR [--render]          # 16:9; vertical.py / square.py draw the other two
"""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import hfbuild as H

ROWS = ["BODY FAT", "FAT TO LOSE", "MUSCLE TO GAIN"]
LEVELS = [0.58, 0.42, 0.66]
BAND = "YOUR WORKOUT PLAN"
TPL = HERE / "analysis-card.template.htm"


def _check(s):
    rows = s.get("rows") or ROWS; band = (s.get("band") or [BAND, None])[0]
    for t in rows + [band, s.get("label") or ""]:
        if re.search(r"\d", t):
            raise SystemExit(f"{s['id']}: '{t}' prints a number. The analysis card shows labels and bars only.")
    rv = s["reveal"]
    assert len(rv) == len(rows), f"{s['id']}: one reveal per row"
    assert s["b"] - s["a"] >= 3.5, f"{s['id']}: under 3.5 s the rows cannot build"
    assert rv == sorted(rv) and rv[0] >= s["a"], f"{s['id']}: reveals {rv} out of order or before the in"
    bt = s["band"][1]
    assert rv[-1] + 0.3 <= bt <= s["b"] - 0.5, f"{s['id']}: band at {bt} must follow the last row and leave 0.5 s to the out {s['b']}"
    lv = s.get("levels") or LEVELS
    assert all(0.15 <= v <= 0.85 for v in lv) and len(lv) == len(rows), f"{s['id']}: levels 0.15..0.85, one per row"
    return rows, lv


def layout(s, canvas=(1920, 1080), bottom=None):
    """The scene config for one aspect. `bottom`: the lowest y the card may reach (above the caption line)."""
    W, Hc = canvas
    rows, lv = _check(s)
    a = s["a"]; rel = lambda t: H.rel(t, a)
    label = s.get("label")
    band_s = s["band"][0]
    sc = s.get("scan") or [a + 0.1, min(a + 1.4, s["reveal"][0] - 0.1)]
    ext = pathlib.Path(s["photo"]).suffix.lower()
    if W > Hc:                                                     # ---- 16:9
        bottom = bottom or Hc - 60
        lpx, rh, bpx, bh, chpx, chh = 40, 96, 46, 100, 40, 72
        px_, py_, ph = 134, 76, min(810, bottom - 76 - 40 - chh)
        pw = round(ph * 0.86)
        kx = px_ + pw + 110; kw = W - 120 - kx
        inline = True
    elif W == Hc:                                                  # ---- 1:1
        bottom = bottom or Hc - 40
        lpx, rh, bpx, bh, chpx, chh = 30, 92, 32, 76, 28, 54
        px_, py_ = 48, 64
        ph = bottom - py_ - 22 - chh
        pw = min(480, round(ph * 0.73)); ph = min(ph, round(pw / 0.73))
        kx = px_ + pw + 40; kw = W - 40 - kx
        inline = False
    else:                                                          # ---- 9:16
        bottom = bottom or round(Hc * 0.72)
        lpx, rh, bpx, bh, chpx, chh = 34, 76, 40, 84, 34, 64
        kx, kw = 36, W - 72
        inline = True
    pad = 28
    kh = pad + len(rows) * rh + 12 + bh + pad
    if W < Hc:                                                     # 9:16 stacks: card at the bottom, chip, picture above
        ky = bottom - kh
        chy = ky - 26 - chh
        py_ = 160; ph = chy - 26 - py_
        pw = min(W - 2 * 96, round(ph * 0.86))
        px_ = (W - pw) // 2
    else:
        ky = py_ + (ph - kh) / 2
        chy = py_ + ph + 22
    assert ph >= 360, f"{s['id']}: the picture would be {ph} px tall; give the card more room"
    labw = max(H.text_w(r, lpx) for r in rows)
    if inline:
        bx = kx + pad + labw + 30; bw = kx + kw - pad - bx
        assert bw >= 180, f"{s['id']}: bars {bw} px wide; labels too long for this card"
    else:
        assert labw <= kw - 2 * pad, f"{s['id']}: a label is too wide for the 1:1 card"
    out_rows = []
    for i, (r, t) in enumerate(zip(rows, s["reveal"])):
        y = ky + pad + i * rh
        if inline:
            lab_y = y + (rh - 12 - lpx * 1.4) / 2; bar_h = 26; bar_y = y + (rh - 12 - bar_h) / 2
            out_rows.append(dict(s=r, px=lpx, lx=kx + pad, ly=round(lab_y), bx=round(bx), by=round(bar_y), bw=round(bw), bh=bar_h, v=lv[i], t=rel(t)))
        else:
            bar_h = 22
            out_rows.append(dict(s=r, px=lpx, lx=kx + pad, ly=round(y), bx=kx + pad, by=round(y + lpx * 1.4 + 6), bw=kw - 2 * pad, bh=bar_h, v=lv[i], t=rel(t)))
    by_ = ky + pad + len(rows) * rh + 12
    bpx_ = bpx
    while H.text_w(band_s, bpx_) > kw - 2 * pad - 40 and bpx_ > 22: bpx_ -= 1
    band = dict(x=kx + pad, y=round(by_), w=kw - 2 * pad, h=bh, s=band_s, px=bpx_, t=rel(s["band"][1]),
                tx=round((kw - 2 * pad - H.text_w(band_s, bpx_)) / 2), ty=round((bh - bpx_ * 1.4) / 2))
    chip = None
    if label:
        cw_ = round(H.text_w(label, chpx, False) + 48)
        chip = dict(x=round(max(20, min(W - 20 - cw_, px_ + pw / 2 - cw_ / 2))), y=round(chy), w=cw_, h=chh, s=label,
                    px=chpx, pad=24, ty=round((chh - chpx * 1.4) / 2))
    cfg = dict(id=s["id"], dur=round(s["b"] - a, 3), canvas=[W, Hc], push=s.get("push", 1.05), drift=s.get("drift", -6),
               photo=dict(x=px_, y=py_, w=pw, h=ph, src="assets/photo" + ext), chip=chip,
               card=[kx, round(ky), kw, kh], rows=out_rows, band=band, scan=[rel(sc[0]), rel(sc[1])])
    box = dict(photo=[px_, py_, px_ + pw, py_ + ph], chip=[chip["x"], chip["y"], chip["x"] + chip["w"], chip["y"] + chh] if chip else None,
               card=[kx, round(ky), kx + kw, round(ky + kh)])
    return cfg, [(s["photo"], "photo" + ext)], box


def scene_cfg(s):
    cfg, assets, _ = layout(s, (1920, 1080))
    return cfg, assets


def main():
    cfg_path, out = sys.argv[1], pathlib.Path(sys.argv[2])
    H.run_all([(TPL, *scene_cfg(s)) for s in json.load(open(cfg_path))], out, "--render" in sys.argv)


if __name__ == "__main__":
    main()
