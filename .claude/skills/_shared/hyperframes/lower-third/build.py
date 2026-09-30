"""Soft Blue Light MOTIVATION LOWER THIRD (HyperFrames), with an optional counter bar on the right of the strip.

Usage:
    python3 build.py config.json OUT_DIR [--render]

Each scene renders TWO overlays: OUT_DIR/<id>.mov (the strip's tint, border, accent, text and bar) and
OUT_DIR/<id>_mask.mov (the strip's shape only, white at 92 %, same motion). The glass blurs the footage under it,
which a transparent overlay cannot do, so the composite blurs the base itself inside the mask (README, "Composite").

config.json is a list of scenes; every time is the WORD's start in the finished film:

  {"id": "g04", "a": 56.24, "b": 67.8349, "topic": "THE MATH",
   "parts": [["1 lb A Week =", 56.40], ["7 MONTHS.", 57.86], ["All In =", 65.24], ["90 DAYS.", 66.12]],
   "bar": {"grow": 57.86, "grow_value": 7, "grow_unit": "MONTHS",
           "shrink": 65.24, "land": 66.42, "from_value": 210, "value": 90, "unit": "DAYS", "ratio": 0.4286},
   "drift": -4}

parts: the point copy split where Dan says each piece; joined with single spaces it must equal the approved point.
Each part rises in on its word (no typing). bar (optional): a track that fills to full while a counter counts
0 -> grow_value (the long way), then on "shrink" a cyan bar retracts to `ratio` of the track while its counter
counts from_value -> value, landing on "land"; the long bar stays behind as a dim ghost with its label, so both
numbers stay on screen. The strip leaves with a 0.33 s fade and 10 px drop that ends exactly on b.
Geometry is softblue.lower_third's: x 86..1828, bottom 64 px from the frame edge, 176 px tall for one line.
"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import hfbuild as H
B = H.B
W, Hh = 1920, 1080
U = 2.0


def layout(topic, parts, bar):
    x0, _, x1, _ = B.lower_third_default_box(W, Hh)
    point = " ".join(p for p, _ in parts)
    tx = x0 + 31 * U
    full_w = H.text_w(point, 28 * U)
    bar_zone = 420 if bar else 0
    wrap_w = x1 - x0 - 31 * U - 24 * U - (bar_zone + 64 if bar else 0)
    assert full_w <= wrap_w, f"point is {full_w:.0f} px; {wrap_w:.0f} px fit beside the bar (shorten it or drop the bar)"
    _, ytop, _, bh = B.lower_third_default_box(W, Hh, 1)
    xs, acc = [], ""
    for p, _ in parts:
        xs.append(round(tx + (H.text_w(acc + " ", 28 * U) if acc else 0), 1))
        acc = (acc + " " + p).strip()
    L = dict(strip=[x0, ytop, x1 - x0 + 1, bh + 1], radius=18 * U, accent=[x0 + U, ytop + 3 * U, 8 * U, bh - 6 * U],
             topic=dict(x=tx, y=ytop + 13 * U, s=topic.upper()), point_y=ytop + 38 * U,
             parts=[dict(s=p, x=x) for (p, _), x in zip(parts, xs)])
    if bar:
        bx1 = x1 - 22 * U; bx0 = bx1 - bar_zone
        L["bar"] = dict(x0=bx0, x1=bx1, y=ytop + 53 * U, h=7 * U, label_top=ytop + 23 * U, label_bottom=ytop + 62 * U,
                        label_px=15 * U)
    return L


def scene_cfg(s, mode):
    a = s["a"]
    assert all(p.strip() == p and p for p, _ in s["parts"]), "parts must be trimmed and non-empty"
    c = dict(id=s["id"] + ("_mask" if mode == "mask" else ""), mode=mode, dur=round(s["b"] - a, 3),
             drift=s.get("drift", -4), times=[H.rel(t, a) for _, t in s["parts"]], **layout(s["topic"], s["parts"], s.get("bar")))
    if s.get("bar"):
        b = dict(s["bar"])
        for k in ("grow", "shrink", "land"): b[k] = H.rel(b[k], a)
        c["bar"].update(b)
    return c


def main():
    cfg_path, out = sys.argv[1], pathlib.Path(sys.argv[2])
    tpl = HERE / "lower-third.template.htm"
    scenes = []
    for s in json.load(open(cfg_path)):
        scenes += [(tpl, scene_cfg(s, "content"), ()), (tpl, scene_cfg(s, "mask"), ())]
    H.run_all(scenes, out, "--render" in sys.argv)


if __name__ == "__main__":
    main()
