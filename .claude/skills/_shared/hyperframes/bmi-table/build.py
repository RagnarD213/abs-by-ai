"""Soft Blue Light BMI TABLE (HyperFrames), full screen on the moving field. New 2026-10-22, approved by Dan 2026-10-23
(DS-40 R6, Bill Maher Fat 90-Year-Old).

    python3 build.py config.json OUT_DIR [--render] [--snap T]

Height down the side, weight across the top, every cell coloured by its BMI band (BMI = 703 x lb / in^2) with the value
printed in it; a legend under the table states the band boundaries (18.5, 25, 30). The table builds in a diagonal wave,
then each band lights up on the word that names it (the other cells dim) and breathes while it is lit. The field keeps
moving and a specular line keeps sweeping the glass panel for the whole time on screen.

config.json (one scene; times are seconds from the scene's start, i.e. the word's start in the film minus `a`):

  {"id": "bmi", "dur": 13.88, "canvas": [1080, 1920],
   "eyebrow": "BMI TABLE", "headline": "Where Do You Land?",
   "heights_in": [60, 62, 64, 66, 68, 70, 72, 74, 76], "weights_lb": [120, 140, 160, 180, 200, 220, 240, 260, 280],
   "beats": [["overweight", 3.28], ["normal", 8.23], ["obese", 9.63]],
   "bottom": 1380}

bottom: the lowest pixel the legend may reach (a 9:16 short keeps its captions running from y 1412 under it).
Bands: underweight < 18.5 (muted, not lit), normal 18.5 to 24.9, overweight 25 to 29.9, obese 30 and over.
"""
import json, math, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import hfbuild as H
TPL = HERE / "bmi-table.template.htm"


def band(b):          # the colour from the exact BMI; the printed value rounds half up (35.15 -> 35.2, R6 review)
    return "under" if b < 18.5 else "normal" if b < 25 else "over" if b < 30 else "obese"


def ft(i):
    return f"{i // 12}' {i % 12}\""


def layout(c):
    W, Hh = c.get("canvas", [1080, 1920])
    hs, ws = c["heights_in"], c["weights_lb"]
    m = 36                                            # side margin
    top = 182                                         # under the platform's top strip (150)
    eb_y, hl_y, hl_px = top, top + 46, 78
    panel_y = hl_y + round(hl_px * 1.4) + 30
    legend_h, gap = 150, 22
    panel_h = c.get("bottom", 1380) - legend_h - gap - panel_y
    hdr_w, hdr_h = 150, 96                            # row-header column, column-header row (unit label + numbers)
    pad = 18
    gw = W - 2 * m - 2 * pad - hdr_w
    gh = panel_h - 2 * pad - hdr_h
    cw, ch = gw / len(ws), gh / len(hs)
    gx, gy = m + pad + hdr_w, panel_y + pad + hdr_h
    cells = []
    for r, h in enumerate(hs):
        for k, w in enumerate(ws):
            b = 703.0 * w / (h * h)
            cells.append(dict(x=round(gx + k * cw + 3, 1), y=round(gy + r * ch + 3, 1), w=round(cw - 6, 1), h=round(ch - 6, 1),
                              v=f"{math.floor(b * 10 + 0.5 + 1e-9) / 10:.1f}", b=band(b), d=r + k))
    cols = [dict(x=round(gx + k * cw, 1), w=round(cw, 1), s=str(w)) for k, w in enumerate(ws)]
    rows = [dict(y=round(gy + r * ch, 1), h=round(ch, 1), s=ft(h)) for r, h in enumerate(hs)]
    ly = panel_y + panel_h + gap
    legend = [dict(b="normal", t="Normal", r="18.5 to 24.9"), dict(b="over", t="Overweight", r="25 to 29.9"),
              dict(b="obese", t="Obese", r="30 and over")]
    lw = (W - 2 * m - 2 * 16) / 3
    for i, L in enumerate(legend):
        L.update(x=round(m + i * (lw + 16), 1), y=ly, w=round(lw, 1), h=104)
    return dict(id=c["id"], dur=c["dur"], canvas=[W, Hh], drift=c.get("drift", -10),
                eyebrow=dict(x=m + 28, y=eb_y, px=34, s=c.get("eyebrow", "BMI TABLE")), accent=[m, eb_y + 14, 12, 34],
                headline=dict(x=m - 2, y=hl_y, px=hl_px, s=c["headline"]),
                panel=[m, panel_y, W - 2 * m, panel_h], units=dict(w="Weight (lb)", h="Height"),
                unit_y=panel_y + pad, num_y=panel_y + pad + 44, hdr_x=m + pad, hdr_w=hdr_w,
                cols=cols, rows=rows, cells=cells, legend=legend, under=dict(x=m + 4, y=ly + 112, s="Under 18.5 is underweight"),
                beats=c.get("beats", []), cell_px=c.get("cell_px", 28 if cw >= 90 else 24))


def scene(c):
    return (TPL, layout(c), ())


if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2])
    d = H.make_scene(TPL, layout(cfg), out / "proj")
    H.lint_check(d)
    if "--snap" in sys.argv:
        t = float(sys.argv[sys.argv.index("--snap") + 1]); print(H.snapshot(d, [t]))
    if "--render" in sys.argv:
        H.render(d, out / f"{cfg['id']}.mov")
