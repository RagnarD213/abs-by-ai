"""Soft Blue Light LINE GRAPH (HyperFrames): a line that climbs and falls over a dashed baseline, each segment drawing on the
words that describe it (rising cyan, falling red), a glowing head that keeps breathing, on the moving field. Opaque scene.
Built 2026-10-20 for SL-18 short 1 (RO-25's approved G02 "My Mentor's Productivity Sketch", re-laid for a 9:16 short's
1080 x 1610 picture area); NOT yet approved by Dan as a template (shown on the SL-18 round-1 page).

Usage:
    python3 build.py config.json OUT_DIR [--render]

  {"id": "B_graph", "a": 67.60, "b": 102.70, "canvas": [1080, 1610],
   "eyebrow": "Regret 1: ADHD Medication", "title": "My Mentor's Productivity Sketch",
   "foot": "Illustrative Personal Experience, Not Measured Study Data",
   "src_box": [85, 120, 910, 476], "src_base": 265,            # the points' own frame (here: the film's 960x540 graph)
   "pts": [[85, 265], [205, 146], ...],                         # n points
   "segments": [[67.94, 71.04], [71.40, 77.78], ...]}           # n - 1 (start, end) times, same clock as a / b

The plot fills the picture area under the header and stays above canvas y 1080, so captions (1102 px into the picture area)
never cross the line. Axis labels: Productivity (top of the y axis), Baseline, Time.
"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import hfbuild as H


def scene_cfg(s, x0=96, x1=1000, ytop=330, yaxis=1040):
    a, b = s["a"], s["b"]; W, Hh = s.get("canvas", [1080, 1610])
    sx0, sy0, sx1, sy1 = s["src_box"]
    kx = (x1 - x0) / (sx1 - sx0); ky = (yaxis - ytop) / (sy1 - sy0)
    m = lambda p: [round(x0 + (p[0] - sx0) * kx, 1), round(ytop + (p[1] - sy0) * ky, 1)]
    pts = [m(p) for p in s["pts"]]
    assert len(s["segments"]) == len(pts) - 1, "one (start, end) per segment"
    segs = [dict(a=H.rel(t0, a), b=H.rel(t1, a)) for t0, t1 in s["segments"]]
    for k in range(1, len(segs)): assert segs[k]["a"] >= segs[k - 1]["b"] - 1e-6, f"segment {k} starts before {k - 1} ends"
    assert segs[-1]["b"] <= b - a, "the line must finish on screen"
    ybase = round(ytop + (s["src_base"] - sy0) * ky, 1)
    tpx, epx = s.get("title_px", 54), 32
    assert H.text_w(s["title"], tpx) <= W - 2 * 64, f"title too wide: {s['title']!r}"
    labels = [dict(s="Productivity", x=x0 - 6, y=ytop - 52, px=30, c="white", bold=True),
              dict(s="Baseline", x=x0 + 14, y=ybase + 10, px=26, c="cyan", bold=False),
              dict(s="Time", x=x1 - H.text_w("Time", 30) - 4, y=yaxis + 12, px=30, c="white", bold=True)]
    return dict(id=s["id"], dur=round(b - a, 3), drift=s.get("drift", -10), canvas=[W, Hh], accent=[64, 46, 78],
                eyebrow=dict(x=64, y=64, px=epx, s=s.get("eyebrow", "")), title=dict(x=64, y=112, px=tpx, s=s["title"]),
                foot=dict(x=64, y=196, px=24, s=s.get("foot", "")),
                plot=dict(x0=x0, x1=x1, ytop=ytop, yaxis=yaxis, ybase=ybase, axis_w=4, base_w=3, line_w=9, dot_r=11),
                labels=labels, points=pts, segments=segs)


if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2])
    for s in (cfg if isinstance(cfg, list) else [cfg]):
        H.run_all([(HERE / "line-graph.template.htm", scene_cfg(s), ())], out, "--render" in sys.argv)
