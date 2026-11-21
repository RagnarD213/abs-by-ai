"""Soft Blue Light TOP STRIP kit for an editor (Muhammad shorts, 2026-10-01).
The approved Motivation lower third (same template, same type, same motion), placed ABOVE Dan's head for a short,
on a denser tint because an editor's overlay cannot blur the footage under it.
  python3 kit.py <NAME> [--render] [--only g01,g02]
reads out/<NAME>.graphics.json, writes kit/<NAME>/{proj,mov,png}."""
import json, pathlib, subprocess, sys
SH = pathlib.Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
sys.path.insert(0, str(SH / "hyperframes"))
import hfbuild as H
B = H.B
from PIL import Image
M = pathlib.Path(__file__).resolve().parent.parent
TPL = M / "kit/tpl/strip.template.htm"
W, Hh = 1080, 1920
U = 1.75                      # 0.875 of the 9:16 lower third (point 49 px, eyebrow 24.5 px): two lines fit above his hair
X0, X1 = 60, 1020
TOP_MIN, TOP_DEFAULT = 64, 96
FF = str(H.BIN / "ffmpeg")

def layout(g):
    tx = X0 + 31 * U
    wrap_w = X1 - X0 - 31 * U - 24 * U
    words = g["text"].split()
    lines, cur = [], []
    for w in words:
        if cur and H.text_w(" ".join(cur + [w]), 28 * U) > wrap_w:
            lines.append(cur); cur = [w]
        else: cur.append(w)
    lines.append(cur)
    assert len(lines) <= 3, (g["id"], "too long", g["text"])
    if len(lines) == 2 and len(lines[1]) == 1 and len(lines[0]) > 2:      # no orphan word
        lines[1].insert(0, lines[0].pop())
    bh = (88 + 36 * (len(lines) - 1)) * U
    ytop = TOP_DEFAULT
    if g.get("under") == "camera" and g.get("hair_top_px"):
        ytop = max(TOP_MIN, min(TOP_DEFAULT, g["hair_top_px"] - 28 - bh))
    if g.get('under') == 'camera' and g.get('hair_top_px'): assert ytop + bh <= g['hair_top_px'] - 18, (g['id'], 'hits hair', ytop + bh, g['hair_top_px'])
    parts = [dict(s=" ".join(ln), x=round(tx, 1), y=ytop + (38 + 36 * i) * U) for i, ln in enumerate(lines)]
    L = dict(strip=[X0, ytop, X1 - X0 + 1, bh + 1], radius=18 * U, accent=[X0 + U, ytop + 3 * U, 8 * U, bh - 6 * U],
             topic=dict(x=tx, y=ytop + 13 * U, s=g["eyebrow"].upper()), point_y=ytop + 38 * U, parts=parts)
    return L, [0.45 + 0.18 * i for i in range(len(lines))], (ytop, ytop + bh)

def css_scale(html):
    return html.replace("#topic { font-size: 28px;", f"#topic {{ font-size: {14*U}px;").replace(".part { font-size: 56px;", f".part {{ font-size: {28*U}px;")

def main():
    name = sys.argv[1]; render = "--render" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    gs = json.load(open(M / f"out/{name}.graphics.json"))
    out = M / "kit" / name; (out / "mov").mkdir(parents=True, exist_ok=True); (out / "png").mkdir(exist_ok=True)
    tpl = out / "strip.tpl.htm"; tpl.write_text(css_scale(TPL.read_text()))
    rep = []
    for g in gs:
        if g["kind"] in ("label_ai", "label_real"): continue
        if only and g["id"] not in only: continue
        dur = round(max(1.6, g["t1"] - g["t0"]), 3)
        L, times, band = layout(g)
        cfg = dict(id=f"{name}_{g['id']}", mode="content", dur=dur, drift=-3, times=times, canvas=[W, Hh], **L)
        d = H.make_scene(tpl, cfg, out / "proj")
        rep.append(dict(id=g["id"], band=band, dur=dur))
        if render:
            raw = out / "proj" / f"{cfg['id']}.mov"
            if not raw.exists():
                H.lint_check(d); H.render(d, raw)
            tag = f"{int(g['t0']//60)}m{g['t0']%60:04.1f}s".replace(".", "_")
            base = f"{g['id']}_{tag}_{g['kind']}"
            vf = "scale=in_color_matrix=bt601:in_range=tv:out_range=pc,format=argb"
            subprocess.run([FF, "-v", "error", "-y", "-i", str(raw), "-vf", vf, "-c:v", "qtrle", str(out / "mov" / f"{base}.mov")], check=True)
            subprocess.run([FF, "-v", "error", "-y", "-ss", str(min(dur - 0.5, 1.4)), "-i", str(raw), "-vf", vf.replace("argb", "rgba"), "-frames:v", "1", str(out / "png" / f"{base}.png")], check=True)
            print("done", base, flush=True)
    json.dump(rep, open(out / "report.json", "w"), indent=1)
main()
