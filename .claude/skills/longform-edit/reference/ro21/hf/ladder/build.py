"""RO-21 BODY FAT LADDER (Soft Blue Light HyperFrames, opaque): optional title, a row of N portrait pictures that rise in on
their words with a % label under each, one AI-GENERATED chip for the row, an optional highlight that moves tile to tile
(dimming the rest), and an optional glass band whose line swaps on words. New 2026-10-28 for RO-21, NOT yet approved by Dan.

Config:
  {"id": "G01", "dur": 4.6, "title": ["What Every Body Fat %", "Looks Like On Me"] | null,
   "tiles": [{"media": "L35.png", "pct": "35%", "at": 0.10, "pos": "50% 20%"}, ...],
   "highlight": [{"tile": 0, "at": 1.2}, ...] (optional),
   "band": {"lines": [{"s": "Start Zepbound, 5-minute morning workout, fast until 2 PM", "lead": "35%", "at": 1.2}, ...]} (optional),
   "tile_h": 470 (optional)}
Usage: python3 build.py CONFIG.json OUT_DIR [--render] [--snap 1.0,2.5]
"""
import json, sys, pathlib
HF = pathlib.Path("/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
sys.path.insert(0, str(HF)); import hfbuild as H
HERE = pathlib.Path(__file__).resolve().parent
W, HH, M, GAP, RADIUS = 1920, 1080, 70, 22, 22
CHIP_PX, CHIP_H = 28, 50


def scene_cfg(cfg):
    n = len(cfg["tiles"]); title = cfg.get("title"); band = cfg.get("band")
    tw = min(420, (W - 2 * M - (n - 1) * GAP) // n)
    th = cfg.get("tile_h") or min(int(tw * 2.25), 480 if band else 620)
    top = 250 if title else 120
    if not title and not band: top = (HH - th - 90) // 2
    if not title and band: top = (HH - (th + 14 + int((54 if tw < 260 else 72) * 1.2) + 26 + 110)) // 2
    x0 = (W - (n * tw + (n - 1) * GAP)) // 2
    pctpx = 54 if tw < 260 else 72
    tiles, assets = [], []
    for i, t in enumerate(cfg["tiles"]):
        nm = f"t{i}{pathlib.Path(t['media']).suffix}"; assets.append((t["media"], nm))
        tiles.append(dict(box=[x0 + i * (tw + GAP), top, tw, th], at=t["at"], media=f"assets/{nm}", pos=t.get("pos", "50% 20%"),
                          pct=t["pct"], pctpx=pctpx))
    out = dict(id=cfg["id"], dur=cfg["dur"], tiles=tiles, radius=RADIUS, highlight=cfg.get("highlight") or [])
    if title:
        l1, l2 = (title + [None])[:2]
        out["title"] = dict(l1=dict(s=l1, px=72, x=round((W - H.text_w(l1, 72)) / 2), y=40, at=0.05),
                            l2=dict(s=l2, px=50, x=round((W - H.text_w(l2, 50)) / 2), y=134, at=0.25) if l2 else None,
                            accent=dict(x=(W - 240) // 2, y=214 if l2 else 140, w=240, at=0.45))
        assert H.text_w(l1, 72) < W - 120 and (not l2 or H.text_w(l2, 50) < W - 120), title
    cw = round(H.text_w("AI-GENERATED", CHIP_PX, False)) + 36
    out["chip"] = dict(s="AI-GENERATED", px=CHIP_PX, x=x0 + n * tw + (n - 1) * GAP - cw, y=top - CHIP_H - 14, w=cw, h=CHIP_H, tx=18, ty=4)
    if cfg.get("chip") is False: out.pop("chip")
    if band:
        by = top + th + 14 + int(pctpx * 1.2) + 26; bh = 110; bw = W - 2 * M
        lines = []
        for L in band["lines"]:
            px = L.get("px", 44)
            wd = H.text_w((L.get("lead", "") + "  " if L.get("lead") else "") + L["s"], px)
            assert wd + 70 <= bw, ("band line too wide", L["s"], wd)
            lines.append(dict(s=L["s"], lead=L.get("lead"), at=L["at"], px=px, x=round((bw - wd) / 2), y=round((bh - px * 1.4) / 2)))
        out["band"] = dict(x=M, y=by, w=bw, h=bh, lines=lines)
        assert by + bh <= HH - 30, ("band off canvas", by + bh)
    return out, assets


def main():
    cfg = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2])
    sc, assets = scene_cfg(cfg)
    d = H.make_scene(HERE / "ladder.template.htm", sc, out, assets)
    H.lint_check(d)
    if "--snap" in sys.argv:
        ts = [float(v) for v in sys.argv[sys.argv.index("--snap") + 1].split(",")]
        for p in H.snapshot(d, ts): print("snapshot", p)
    if "--render" in sys.argv: H.render(d, out / f"{d.name}.mov")


if __name__ == "__main__":
    main()
