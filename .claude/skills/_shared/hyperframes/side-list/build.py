"""Soft Blue Light 3A SIDE LIST (HyperFrames): the locked 3A left-third card, with motion. Dan sits right of it.

Usage:
    python3 build.py config.json OUT_DIR [--render]

config.json is a list of scenes; every time is the WORD's start in the finished film (words_out.json /
mapped-words.json). build.py converts to scene-relative seconds and computes the card geometry with
softblue.left_third_box / _lt_text, so card, heading, divider, numbers and body sit on the locked 3A pixels.

  {"id": "g20", "a": 622.188, "b": 631.4637, "heading": "Your Weekly Check",
   "items": ["Down 2+ lb: change NOTHING", "Stalled a week: CUT 200 cal"],
   "reveal": [623.74, 627.14],     # each item lands on the word that starts it (Dan's speech, not a fixed stagger)
   "drift": -6}                    # px the card rises (-) or sinks (+) across the scene

a / b: the card's in and out; put them on shot boundaries so the reframe (README) hides in a cut. The card leaves
with a 0.33 s fade that ends exactly on b. heading may be a list of line strings. Up to 4 items.
"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import hfbuild as H
B = H.B
W, Hh = 1920, 1080


def layout(heading, items):
    g = B._lt_geom(W, Hh)
    x0, y0, x1, y1 = (round(v) for v in B.left_third_box(W, Hh, heading, items))
    k = g["k"]; fh, fb = B.font(60 * k), B.font(38 * k)
    hl = []
    for part in (heading if isinstance(heading, (list, tuple)) else [heading]):
        hl += B.wrap(part, fh, g["head_w"])
    div = round((22 + 75 * len(hl) + 14) * k)
    y = div + 32 * k; its = []
    for i, s in enumerate(items):
        lines = B.wrap(s, fb, g["body_w"])
        its.append(dict(n=f"{i + 1}.", y=round(y0 + y), lines=lines))
        y += (len(lines) * 49 + 30) * k
    return dict(card=[x0, y0, x1 - x0 + 1, y1 - y0 + 1], head=[dict(x=64, y=y0 + (22 + i * 75), s=ln) for i, ln in enumerate(hl)],
                divider=[x0 + 29, y0 + div, (x1 - 30) - (x0 + 29), 3], items=its, num_x=68, body_x=113, lh=49)


def scene_cfg(s):
    a = s["a"]
    assert len(s["reveal"]) == len(s["items"]), "one reveal word per item"
    return dict(id=s["id"], dur=round(s["b"] - a, 3), drift=s.get("drift", -6),
                reveal=[H.rel(t, a) for t in s["reveal"]], **layout(s["heading"], s["items"]))


def main():
    cfg_path, out = sys.argv[1], pathlib.Path(sys.argv[2])
    tpl = HERE / "side-list.template.htm"
    H.run_all([(tpl, scene_cfg(s), ()) for s in json.load(open(cfg_path))], out, "--render" in sys.argv)


if __name__ == "__main__":
    main()
