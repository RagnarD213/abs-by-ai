"""Soft Blue Light COMPARE CARD (HyperFrames): two stacked glass panels, option A and option B, each a header and rows that
land on the words that name them, on the moving field. Opaque scene. Built 2026-10-18 for SL-09 short 5 ("Oura Ring Or WHOOP?"),
at the 1080 x 1610 picture area under a short's title band; NOT yet approved by Dan (shown on the SL-09 round-1 page).

Usage:
    python3 build.py config.json OUT_DIR [--render]

  {"id": "J_compare", "a": 20.70, "b": 43.15, "canvas": [1080, 1610], "eyebrow": "Advantages",
   "panels": [{"head": "Oura Ring", "t": 20.70, "rows": [["More Accurate", 23.45], ["Better App", 28.45]]},
              {"head": "WHOOP", "t": 33.01, "rows": [["Better For Workout Tracking", 34.49]]}]}

Times are in the same clock as a / b (the words' starts). A panel rises in on its header's word; its rows slide in on theirs; while
it is the newest panel a light travels its top edge and its border breathes, and the whole card drifts, so it moves for its whole
time on screen (VIDEO-RULES 2026-10-17). Every row is one line: build() refuses a row wider than the panel. Keep the content above
canvas y 1066 when captions run under it (a short's captions start 1102 px into the picture area).
"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import hfbuild as H


def scene_cfg(s, x=48, wd=984, pad=44, head_px=54, row_px=42, ck=48, rh=78, top=150, gap=26):
    a, b = s["a"], s["b"]; W, Hh = s.get("canvas", [1080, 1610])
    panels, y = [], top
    for k, p in enumerate(s["panels"]):
        until = s["panels"][k + 1]["t"] if k + 1 < len(s["panels"]) else b
        rows, ry = [], 128
        for txt, t in p["rows"]:
            assert H.text_w(txt, row_px) <= wd - 2 * pad - ck - 36, f"{s['id']}: row {txt!r} too wide"
            rows.append(dict(s=txt, y=ry, h=rh, ty=round((rh - row_px * 1.4) / 2, 1), t=H.rel(t, a))); ry += rh + 6
        panels.append(dict(head=p["head"], head_px=head_px, pad=pad, head_y=22, div_y=104, x=x, y=y, w=wd, h=ry + 10, ck=ck,
                           row_px=row_px, rows=rows, t=H.rel(p["t"], a), until=H.rel(until, a)))
        y += ry + 10 + gap
    return dict(id=s["id"], dur=round(b - a, 3), drift=s.get("drift", -10), canvas=[W, Hh], accent=[64, 40, 78],
                eyebrow=dict(x=64, y=62, px=34, s=s.get("eyebrow", "")), panels=panels)


if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2])
    for s in (cfg if isinstance(cfg, list) else [cfg]):
        H.run_all([(HERE / "compare-card.template.htm", scene_cfg(s), ())], out, "--render" in sys.argv)
