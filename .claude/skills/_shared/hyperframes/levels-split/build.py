"""Soft Blue Light LEVELS SPLIT: a big two-line title over three clip tiles that open on their words (RO-20C round 5).

New 2026-10-20, NOT yet approved by Dan. Replaces RO-20's static `cards20.levels_card` for video 3's intro: Dan asked for
"a top title graphic ... larger" over "a three-way AI-generated clip split screen" (dead broke / middle class / over
$10,000 a month). The plate is the moving field with three transparent rounded holes; the video build lays the three
clips under it. Each hole opens on its word with a frame, a travelling specular line, a glass label under it and an
AI-GENERATED chip inside it. With `--mockup` the template draws stills (START then END frame) in the holes itself, for
the review page.

Config (JSON):
  {"id": "LS-ro20c", "dur": 6.87,
   "title": ["What To Buy For Your Health", "At Every Income Level"],
   "tiles": [{"at": 2.99, "a": "Dead Broke", "b": "A Home Setup Under $100",
              "media": ["I1-start.png", "I1-end.png"], "pos": "50% 50%", "chip": "tl"}, ...]}
  "at" is the scene time the tile opens (its tier word). "chip" is the corner for the AI chip: tl, tr, bl, br, or null.
  Optional "crop": [x, y, w, h], the square window of the source the tile shows (else the centre, cover-fit).

Usage: python3 build.py CONFIG.json OUT_DIR [--mockup] [--render] [--snap 6.5,...]
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import hfbuild as H  # noqa: E402

W, HH = 1920, 1080
TILE, GAP, X0, TY, RADIUS = 560, 40, 80, 272, 28
L1PX, L2PX = 84, 54
LAB_Y, LAB_H, APX, BPX = TY + TILE + 20, 150, 44, 30
CHIP_PX, CHIP_H = 30, 52


def scene_cfg(cfg, mockup=False):
    l1, l2 = cfg["title"]
    t = dict(l1=dict(s=l1, px=L1PX, x=round((W - H.text_w(l1, L1PX)) / 2), y=36, at=0.08),
             l2=dict(s=l2, px=L2PX, x=round((W - H.text_w(l2, L2PX)) / 2), y=148, at=0.32),
             accent=dict(x=(W - 240) // 2, y=240, w=240, at=0.55))
    tiles, assets = [], []
    for i, tl in enumerate(cfg["tiles"]):
        x = X0 + i * (TILE + GAP)
        aw = H.text_w(tl["a"], APX)
        lab = dict(a=tl["a"], apx=APX, ax=26, ay=14, y=LAB_Y, h=LAB_H if tl.get("b") else 96)
        if tl.get("b"): lab.update(b=tl["b"], bpx=BPX, bx=26, by=82)
        assert aw + 52 <= TILE and (not tl.get("b") or H.text_w(tl["b"], BPX, False) + 52 <= TILE), tl
        out = dict(box=[x, TY, TILE, TILE], at=tl["at"], label=lab, pos=tl.get("pos", "50% 50%"), swap=tl.get("swap", 1.2))
        if tl.get("crop"):                    # [x, y, w, h] window of the source (w == h for the square tile)
            from PIL import Image
            assert abs(tl["crop"][2] - tl["crop"][3]) <= 2, tl["crop"]
            out.update(crop=tl["crop"], src=list(Image.open(tl["media"][0]).size))
        if tl.get("chip"):
            cw = round(H.text_w("AI-GENERATED", CHIP_PX, False)) + 36
            cx = x + 18 if tl["chip"][1] == "l" else x + TILE - 18 - cw
            cy = TY + 18 if tl["chip"][0] == "t" else TY + TILE - 18 - CHIP_H
            out["chip"] = dict(s="AI-GENERATED", px=CHIP_PX, x=cx, y=cy, w=cw, h=CHIP_H, tx=18, ty=4)
        if mockup and tl.get("media"):
            names = []
            for k, src in enumerate(tl["media"]):
                nm = f"t{i}_{k}{pathlib.Path(src).suffix}"; assets.append((src, nm)); names.append(f"assets/{nm}")
            out["media"] = names
        tiles.append(out)
    return dict(id=cfg["id"], dur=cfg["dur"], title=t, tiles=tiles, radius=RADIUS, mockup=mockup), assets


def main():
    cfg = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2]); mock = "--mockup" in sys.argv
    sc, assets = scene_cfg(cfg, mock)
    d = H.make_scene(HERE / "levels-split.template.htm", sc, out, assets)
    H.lint_check(d)
    if "--snap" in sys.argv:
        ts = [float(v) for v in sys.argv[sys.argv.index("--snap") + 1].split(",")]
        for p in H.snapshot(d, ts): print("snapshot", p)
    if "--render" in sys.argv: H.render(d, out / f"{d.name}.mov")


if __name__ == "__main__":
    main()
