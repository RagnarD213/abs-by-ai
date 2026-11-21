"""Soft Blue Light BEFORE / FACT CARD (HyperFrames): full-screen scene, real photo left, glass fact card right,
on the moving Soft Blue field (drawn live, same formula as softblue.field). An opaque scene, not an overlay: the
photo is the content, so the render replaces the frames between a and b.

Usage:
    python3 build.py config.json OUT_DIR [--render]

  {"id": "g02", "a": 19.12, "b": 24.36, "photo": "/abs/path/dan_before_200lb.jpg",
   "label": "Real picture of me. Not AI-generated.",
   "eyebrow": ["TWO YEARS AGO", 19.30],
   "headline": [["200 lb", 20.44], ["at 5'7\"", 21.50]],
   "count": {"value": "200", "from": 0, "dur": 0.55},      # optional: the number in headline part 0 counts up on its word
   "detail": ["No abs.", 22.80],
   "sweep": 21.05,                                           # optional: one light sweep across the card's glass
   "push": 1.07, "drift": -8}                                # photo push-in (end scale) and card drift (px)

The disclosure chip arrives with the photo on its first visible frame (VIDEO-RULES). Geometry is
softblue.scene_fact's 16:9 layout with fit=True (photo fills its frame, top-anchored crop).
"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import hfbuild as H
B = H.B
U = 2.0


def scene_cfg(s):
    a = s["a"]
    x, y, w, h = 67 * U, 38 * U, 362 * U, 405 * U
    card = (476 * U, 126 * U, 906 * U, 359 * U)
    cx = card[0] + 27 * U
    head = s["headline"]
    xs, acc = [], ""
    for p, _ in head:
        xs.append(round(cx + (H.text_w(acc + " ", 42 * U) if acc else 0), 1)); acc = (acc + " " + p).strip()
    c = dict(id=s["id"], dur=round(s["b"] - a, 3), push=s.get("push", 1.07), drift=s.get("drift", -8),
             photo=dict(x=x, y=y, w=w, h=h, src="assets/photo" + pathlib.Path(s["photo"]).suffix.lower()),
             chip=dict(x=162 * U, y=484 * U, s=s["label"], w=round(H.text_w(s["label"], 23 * U, False) + 40 * U)) if s.get("label") else None,
             card=[card[0], card[1], card[2] - card[0] + 1, card[3] - card[1] + 1],
             eyebrow=dict(x=cx, y=card[1] + 22 * U, s=s["eyebrow"][0], t=H.rel(s["eyebrow"][1], a)),
             head=[dict(x=x_, y=card[1] + 83 * U, s=p, t=H.rel(t, a)) for (p, t), x_ in zip(head, xs)],
             detail=dict(x=cx + U, y=card[1] + 164 * U, s=s["detail"][0], t=H.rel(s["detail"][1], a)) if s.get("detail") else None,
             sweep=H.rel(s["sweep"], a) if s.get("sweep") else None)
    if s.get("count"):
        k = s["count"]; p0 = head[0][0]
        assert p0.startswith(k["value"]), "the counted number must start headline part 0"
        c["count"] = dict(value=int(k["value"]), frm=k.get("from", 0), dur=k.get("dur", 0.55),
                          w=H.text_w(k["value"], 42 * U), rest=p0[len(k["value"]):])
    return c, [(s["photo"], "photo" + pathlib.Path(s["photo"]).suffix.lower())]


def main():
    cfg_path, out = sys.argv[1], pathlib.Path(sys.argv[2])
    tpl = HERE / "before-card.template.htm"
    H.run_all([(tpl, *scene_cfg(s)) for s in json.load(open(cfg_path))], out, "--render" in sys.argv)


if __name__ == "__main__":
    main()
