"""THE 9:16 LAYOUTS OF THE SOFT BLUE LIGHT TEMPLATES. The same template files and the same configs that drew a graphic
at 16:9 draw it at 1080x1920 here: only the layout (where things sit, how lines wrap) is computed for the tall frame,
from softblue.py's own 9:16 geometry. Text and timing are never retyped.

  python3 vertical.py --sheet SHEET.json --out OUT_DIR [--only G01,G02] [--render] [--snap] [--range A B]

reads the edit sheet's `graphics` (_shared/edit-sheet/README.md) and writes OUT/configs/<id>.json (the scene config),
OUT/proj/<id>/ (the HyperFrames project), OUT/renders/<id>.mov (+ <id>_mask.mov for glass over footage) and
OUT/manifest.json (what the vertical's renderer needs). --snap also writes OUT/stills/<id>.png (the settled graphic).

  sheet template        9:16 layout (the standard it follows)
  lower-third           strip x 68..1012, bottom at 68 % of the height, above the caption band (SOFTBLUE.md); a long
                        point WRAPS and the strip grows upward; each part still rises on the word Dan says it
  before-card           photo on top, glass fact card beneath (softblue.scene_fact's stacked layout), chip under the photo
  side-list             the 3A card full width, 36 px margins, bottom at 87 % of the height, type 1.25x (locked 2026-09-28)
  cycle                 the same 740 x 488 card scaled to the full width, bottom at 87 %
  softblue:title_card   title-card/ (new): eyebrow + headline lines on the field
  softblue:recap        title-card/ with glass rows, one column
  (kit) card / phone    media-card/ (new): the field with a hole for the clip, chip under it      media_card_scene()
  (kit) cta             cta/ (new): a glass button over footage                                    cta_scenes()

Anything else in the sheet (softblue:study, :chart, :portraits, adkit:*, codex:*) has no 9:16 template yet and STOPS
the run with its id: a graphic is never dropped or redrawn by hand.
"""
import argparse, hashlib, importlib.util, json, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hfbuild as H                                  # noqa: E402
B = H.B
W, Hh = 1080, 1920
CAP_TOP = 1400                                       # the kit's caption line (vlib.CAP_Y) at 1080x1920
U = B.unit(W, Hh)                                    # 2.0
CANVAS = [W, Hh]
FPS = 30000 / 1001
SIDE, CARD_BOTTOM = 36, round(Hh * 0.87)             # the 3A card's 9:16 placement (GRAPHICS-STANDARDS.md)
CAPTION_BAND = (round(Hh * 0.70), round(Hh * 0.84))


def _mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


# ------------------------------------------------------------------ lower third
def lt_scenes(c):
    assert not c.get("bar"), f"{c['id']}: the counter bar has no 9:16 layout yet"
    a = c["a"]
    x0, _, x1, _ = B.lower_third_default_box(W, Hh)
    tx = x0 + 31 * U
    wrap_w = x1 - x0 - 31 * U - 24 * U
    toks = [(w, k) for k, (p, _) in enumerate(c["parts"]) for w in p.split()]
    fits = lambda words, lim: H.text_w(" ".join(words), 28 * U) <= lim

    def wrap(lim):
        lines, cur = [], []
        for w, k in toks:
            # a part that fits a line of its own never starts in the middle of the previous part's line
            # (L01 read "...Nutritionist Saved $1,000 A" as one run-on line, Ad 13 round 1)
            whole = [x for x, kk in toks if kk == k]
            newpart = bool(cur) and cur[-1][1] != k
            if cur and (not fits([x for x, _ in cur] + [w], lim)
                        or (newpart and fits(whole, wrap_w) and not fits([x for x, _ in cur] + whole, lim))):
                lines.append(cur); cur = [(w, k)]
            else:
                cur.append((w, k))
        lines.append(cur)
        return lines
    lines = wrap(wrap_w)
    # balanced lines: the narrowest wrap that keeps the same number of lines (no one-word last line: "...Over 20 / YEARS")
    lim = wrap_w
    while lim > wrap_w * 0.45:
        lim -= 16
        cand = wrap(lim)
        if len(cand) != len(lines) or not all(fits([x for x, _ in ln], wrap_w) for ln in cand):
            break
        lines = cand
    assert all(H.text_w(" ".join(x for x, _ in ln), 28 * U) <= wrap_w for ln in lines), f"{c['id']}: one word is wider than the strip"
    _, ytop, _, bh = B.lower_third_default_box(W, Hh, len(lines))
    parts, times = [], []
    for li, ln in enumerate(lines):
        j = 0
        while j < len(ln):
            k = ln[j][1]; e = j
            while e < len(ln) and ln[e][1] == k: e += 1
            pre = " ".join(x for x, _ in ln[:j])
            parts.append(dict(s=" ".join(x for x, _ in ln[j:e]), x=round(tx + (H.text_w(pre + " ", 28 * U) if pre else 0), 1),
                              y=ytop + (38 + 36 * li) * U))
            times.append(H.rel(c["parts"][k][1], a))
            j = e
    L = dict(strip=[x0, ytop, x1 - x0 + 1, bh + 1], radius=18 * U, accent=[x0 + U, ytop + 3 * U, 8 * U, bh - 6 * U],
             topic=dict(x=tx, y=ytop + 13 * U, s=c["topic"].upper()), point_y=ytop + 38 * U, parts=parts)
    assert H.text_w(c["topic"].upper(), 14 * U) <= wrap_w, f"{c['id']}: topic too wide for 9:16"
    out = []
    for mode in ("content", "mask"):
        out.append((HERE / "lower-third" / "lower-third.template.htm",
                    dict(id=c["id"] + ("_mask" if mode == "mask" else ""), mode=mode, dur=round(c["b"] - a, 3), drift=c.get("drift", -4),
                         times=times, canvas=CANVAS, **L), ()))
    meta = dict(kind="glass", band=[int(ytop - 12), int(min(Hh, ytop + bh + 60))], box=[round(x0), round(ytop), round(x1), round(ytop + bh)],
                lines=len(lines))
    return out, meta


# ------------------------------------------------------------------ before / fact card
def fact_scenes(c):
    a = c["a"]
    label = c.get("label"); detail = c.get("detail")
    gap = (70 if label else 30) * U
    ch = (215 if detail else 150) * U
    pw, ph = W - 80 * U, round(Hh * .46)
    if c.get("whole"):
        # the whole photo, never a cover crop: a before picture keeps its head AND its stomach (Ad 6, 2026-10-02)
        from PIL import Image, ImageOps
        iw, ih = ImageOps.exif_transpose(Image.open(c["photo"])).size
        ph = round(Hh * .50)
        pw = min(pw, round(ph * iw / ih)); ph = round(pw * ih / iw)
    px, py = (W - pw) / 2, (Hh - (ph + gap + ch)) / 2 + 12 * U
    cy = py + ph + gap
    card = (40 * U, cy, W - 40 * U, cy + ch)
    cx = card[0] + 27 * U
    inner = card[2] - card[0] - 27 * U - 20 * U
    head = c["headline"]
    assert H.text_w(c["eyebrow"][0], 32 * U) <= inner, f"{c['id']}: eyebrow too wide for 9:16"
    assert H.text_w(" ".join(p for p, _ in head), 42 * U) <= inner, f"{c['id']}: headline too wide for 9:16"
    xs, acc = [], ""
    for p, _ in head:
        xs.append(round(cx + (H.text_w(acc + " ", 42 * U) if acc else 0), 1)); acc = (acc + " " + p).strip()
    ext = pathlib.Path(c["photo"]).suffix.lower()
    chip = None
    if label:
        cw_ = round(H.text_w(label, 23 * U, False) + 40 * U)
        chip = dict(x=round(px + pw / 2 - cw_ / 2), y=py + ph + 20 * U, s=label, w=cw_)
    s = dict(id=c["id"], dur=round(c["b"] - a, 3), push=c.get("push", 1.07), drift=c.get("drift", -8), canvas=CANVAS,
             photo=dict(x=px, y=py, w=pw, h=ph, src="assets/photo" + ext), chip=chip,
             card=[card[0], card[1], card[2] - card[0] + 1, card[3] - card[1] + 1],
             eyebrow=dict(x=cx, y=card[1] + 22 * U, s=c["eyebrow"][0], t=H.rel(c["eyebrow"][1], a)),
             head=[dict(x=x_, y=card[1] + 83 * U, s=p, t=H.rel(t, a)) for (p, t), x_ in zip(head, xs)],
             detail=dict(x=cx + U, y=card[1] + 164 * U, s=detail[0], t=H.rel(detail[1], a)) if detail else None,
             sweep=H.rel(c["sweep"], a) if c.get("sweep") else None)
    if detail:
        assert H.text_w(detail[0], 23 * U, False) <= inner, f"{c['id']}: detail too wide for 9:16"
    if c.get("count"):
        k = c["count"]; p0 = head[0][0]
        s["count"] = dict(value=int(k["value"]), frm=k.get("from", 0), dur=k.get("dur", 0.55), w=H.text_w(k["value"], 42 * U), rest=p0[len(k["value"]):])
    return [(HERE / "before-card" / "before-card.template.htm", s, [(c["photo"], "photo" + ext)])], dict(kind="opaque")


# ------------------------------------------------------------------ 3A side list (full width, bottom)
def list_scenes(c):
    a = c["a"]
    g = B._lt_geom(W, Hh)
    x0, y0, x1, y1 = (round(v) for v in B.left_third_box(W, Hh, c["heading"], c["items"]))
    k = g["k"]; fh, fb = B.font(60 * k), B.font(38 * k); ox = g["x0"] - 36 * k
    hl = []
    for part in (c["heading"] if isinstance(c["heading"], (list, tuple)) else [c["heading"]]):
        hl += B.wrap(part, fh, g["head_w"])
    div = round((22 + 75 * len(hl) + 14) * k)
    y = div + 32 * k; its = []
    for i, s in enumerate(c["items"]):
        lines = B.wrap(s, fb, g["body_w"])
        its.append(dict(n=f"{i + 1}.", y=round(y0 + y), lines=lines))
        y += (len(lines) * 49 + 30) * k
    s = dict(id=c["id"], dur=round(c["b"] - a, 3), drift=c.get("drift", -6), canvas=CANVAS,
             reveal=[H.rel(t, a) for t in c["reveal"]], card=[x0, y0, x1 - x0 + 1, y1 - y0 + 1],
             head=[dict(x=round(ox + 64 * k), y=round(y0 + (22 + i * 75) * k), s=ln) for i, ln in enumerate(hl)],
             divider=[round(x0 + 29 * k), y0 + div, round((x1 - 30 * k) - (x0 + 29 * k)), round(3 * k)], items=its,
             num_x=round(ox + 68 * k), body_x=round(ox + 113 * k), lh=round(49 * k, 2),
             type=dict(head=round(60 * k, 2), body=round(38 * k, 2), radius=round(32 * k)))
    return [(HERE / "side-list" / "side-list.template.htm", s, ())], dict(kind="overlay", box=[x0, y0, x1, y1])


# ------------------------------------------------------------------ cycle
def cycle_scenes(c):
    cb = _mod(HERE / "cycle" / "build.py", "cycle_build")
    s = cb.scene_cfg(c)
    k = (W - 2 * SIDE) / 740
    y = CARD_BOTTOM - 488 * k
    s.update(canvas=CANVAS, place=dict(x=SIDE, y=round(y, 1), scale=round(k, 4)))
    return [(HERE / "cycle" / "cycle.template.htm", s, ())], dict(kind="overlay", box=[SIDE, round(y), W - SIDE, CARD_BOTTOM])


# ------------------------------------------------------------------ title / statement / recap
def title_scenes(gid, t0, t1, eyebrow, headline, items=None):
    x, maxw = 40 * U, W - 80 * U
    lines = headline.split("\n")
    size = 96 if not items else 72
    while size > 60 and max(H.text_w(l, size) for l in lines) > maxw: size -= 2
    if max(H.text_w(l, size) for l in lines) > maxw:
        lines = B.wrap(headline.replace("\n", " "), B.font(size), maxw)
    lh = size * 1.22
    rows, rh, rg = [], 116, 18
    blockh = (64 + 34 if eyebrow else 0) + len(lines) * lh + ((40 + len(items) * (rh + rg)) if items else 0)
    y = (Hh - blockh) / 2 - (60 if not items else 0)
    c = dict(id=gid, dur=round(t1 - t0, 3), drift=-10, canvas=CANVAS, line_px=size)
    ly = y
    if eyebrow:
        assert H.text_w(eyebrow, 34) <= maxw
        c["accent"] = [x, round(y + 8), 78]
        c["eyebrow"] = dict(x=x, y=round(y + 30), px=34, s=eyebrow)
        ly = y + 98
    c["lines"] = [dict(x=x - 4, y=round(ly + i * lh), s=ln) for i, ln in enumerate(lines)]
    if items:
        ry = ly + len(lines) * lh + 40
        for i, s in enumerate(items):
            assert H.text_w(s, 46) <= maxw - 100 - 34, f"{gid}: recap row {s!r} too wide for 9:16"
            rows.append(dict(x=x, y=round(ry + i * (rh + rg)), w=maxw, h=rh, s=s, t=round(0.35 + i * 0.16, 3)))
        c.update(rows=rows, row_px=46, row_ty=round((rh - 46 * 1.4) / 2))
    return [(HERE / "title-card" / "title-card.template.htm", c, ())], dict(kind="opaque")


# ------------------------------------------------------------------ media card (the kit's clip / photo / phone cards)
def media_card_scene(gid, dur, media_ar, label=None, kicker=None, spans=None, max_w=None, max_h=1240, caps=False):
    """The plate for one card: returns (scene tuple, hole [x0, y0, x1, y1]). The hole keeps the media's own shape
    (a horizontal clip is never cropped shorter: VIDEO-RULES 2026-10-01), as large as the frame allows.
    caps: captions run under this card, so a tall picture ends above the caption line (y 1370) instead of sitting
    under the words (the before photo's stomach was captioned over, Ad 13 round 1)."""
    max_w = max_w or (W - 2 * SIDE)
    if caps and not label:
        max_h = min(max_h, 1370 - 190)
    hw = max_w; hh = hw / media_ar
    if hh > max_h: hh = max_h; hw = hh * media_ar
    hw, hh = int(hw) // 2 * 2, int(hh) // 2 * 2
    extra = (68 + 80 if label else 0)
    hx, hy = (W - hw) // 2, int((Hh - hh - extra) / 2 - 40 * (media_ar > 1))
    # a tall card (a centre square, 2026-10-01) must end above the caption line: centred, its chip sat under the
    # captions and a chip-less square's bottom edge sat behind them (RO-10 O1 and C02). It moves up until the card and
    # its chip clear the line by 24 px; a card too tall to do that (a phone, whose captions are off) stays centred.
    top = CAP_TOP - 24 - (hh + extra)
    if hy > top >= 150:
        hy = int(top)
    c = dict(id=gid, dur=round(dur, 3), canvas=CANVAS, hole=[hx, hy, hw, hh], radius=26 if media_ar > 0.7 else 44)
    if label:
        cw_ = round(H.text_w(label, 23 * U, False) + 40 * U)
        c["chip"] = dict(x=round(W / 2 - cw_ / 2), y=hy + hh + 68, s=label, w=cw_)      # 68 px under the hole (kit9x16 README, measured trap)
        if spans: c["chip"]["spans"] = spans
    if kicker:
        c["kicker"] = dict(x=hx + 4, y=hy - 84, px=40, s=kicker)
    return (HERE / "media-card" / "media-card.template.htm", c, ()), [hx, hy, hx + hw, hy + hh]


# ------------------------------------------------------------------ CTA button over footage
def cta_scenes(gid, dur, top, big, hold_out=False, full=False):
    x0, _, x1, _ = B.lower_third_default_box(W, Hh)
    bw, bh = x1 - x0, 110 * U
    by = Hh * .68 - bh if not full else (Hh - bh) / 2
    big_px = 64
    while big_px > 44 and H.text_w(big, big_px) > bw - 200: big_px -= 2
    top_px = 30
    while top_px > 22 and H.text_w(top, top_px) > bw - 80: top_px -= 1
    bx_ = x0 + (bw - H.text_w(big, big_px) - 56) / 2
    L = dict(btn=[x0, by, bw, bh], radius=22 * U, top=dict(x=round(x0 + (bw - H.text_w(top, top_px)) / 2), y=round(by + 24 * U), px=top_px, s=top),
             big=dict(x=round(bx_), y=round(by + 24 * U + top_px * 1.4 + 6), px=big_px, s=big),
             arrow=dict(x=round(bx_ + H.text_w(big, big_px) + 22), y=round(by + 24 * U + top_px * 1.4 + 6), px=big_px))
    out = [(HERE / "cta" / "cta.template.htm", dict(id=gid + ("_mask" if m == "mask" else ""), mode=m, dur=round(dur, 3), canvas=CANVAS,
                                                    hold_out=hold_out, full=full, **L), ()) for m in (("content",) if full else ("content", "mask"))]
    return out, dict(kind="opaque" if full else "glass", band=[int(by - 12), int(by + bh + 60)], box=[round(x0), round(by), round(x1), round(by + bh)])


# ------------------------------------------------------------------ running total chip (top left, over footage)
def tally_scenes(gid, dur, label, value, frm=0, prefix="$", unit="/ month", at=0.45, count=0.6, y=170):
    """A small glass chip in the top-left safe area: `label` (cyan caps) over `prefix + value` with `unit` beside it.
    The number counts up from `frm` (the last total) `at` seconds in. y 170: under the platform's top 150 px."""
    x0 = 34 * U
    lpx, apx, upx = 26, 60, 30
    full = prefix + f"{int(value):,}"
    aw = max(H.text_w(full, apx), H.text_w(prefix + f"{int(frm):,}", apx))
    bw = round(34 + max(H.text_w(label.upper(), lpx) * 1.08, aw + 14 + H.text_w(unit, upx, False)) + 34)
    bh = 150
    L = dict(chip=[x0, y, bw, bh], radius=14 * U, accent=[x0 + 12, y + 20, 8, bh - 40],
             label=dict(x=x0 + 36, y=y + 16, px=lpx, s=label.upper()),
             amount=dict(x=x0 + 36, y=y + 50, px=apx), unit=dict(x=round(x0 + 36 + aw + 14), y=y + 50 + round((apx - upx) * 1.05), px=upx, s=unit),
             value=int(value), frm=int(frm), prefix=prefix, at=at, count=count)
    out = [(HERE / "tally" / "tally.template.htm", dict(id=gid + ("_mask" if m == "mask" else ""), mode=m, dur=round(dur, 3), canvas=CANVAS, **L), ())
           for m in ("content", "mask")]
    return out, dict(kind="glass", band=[int(y - 40), int(y + bh + 40)], box=[round(x0), y, round(x0 + bw), y + bh])


# ------------------------------------------------------------------ the sheet's graphics
def scenes_for(g):
    t, c = g["template"], g["config"]
    if t == "lower-third": return lt_scenes(c)
    if t == "before-card": return fact_scenes(c)
    if t == "side-list": return list_scenes(c)
    if t == "cycle": return cycle_scenes(c)
    if t == "softblue:title_card": return title_scenes(g["id"], g["t0"], g["t1"], c.get("eyebrow"), c["headline"])
    if t == "softblue:recap": return title_scenes(g["id"], g["t0"], g["t1"], c.get("eyebrow"), c.get("headline") or "", c["items"])
    if t == "tally": return tally_scenes(g["id"], g["t1"] - g["t0"], c["label"], c["value"], c.get("frm", 0), c.get("prefix", "$"), c.get("unit", "/ month"))
    if t == "cta": return cta_scenes(g["id"], g["t1"] - g["t0"], c["top"], c["big"], hold_out=c.get("hold_out", False))
    raise SystemExit(f"{g['id']}: template {t!r} has no 9:16 layout (vertical.py). Add one; a graphic is never dropped.")


def tsha(scenes):
    h = hashlib.sha256()
    for tpl, cfg, assets in scenes:
        h.update(pathlib.Path(tpl).read_bytes()); h.update(json.dumps(cfg, sort_keys=True).encode())
        for src, _ in assets: h.update(pathlib.Path(src).read_bytes())
    h.update((HERE / "vertical.py").read_bytes())
    return h.hexdigest()[:16]


def build(scenes, out, render=True, snap=None, force=False, check=True):
    """Build (and render) one graphic's scenes into OUT. Returns {scene id: mov path}. Cached on template + config."""
    out = pathlib.Path(out); (out / "renders").mkdir(parents=True, exist_ok=True); (out / "configs").mkdir(exist_ok=True)
    proj = out / "proj"
    gid = scenes[0][1]["id"]
    sha = tsha(scenes); stamp = out / "renders" / f"{gid}.sha"
    movs = {cfg["id"]: out / "renders" / f"{cfg['id']}.mov" for _, cfg, _ in scenes}
    (out / "configs" / f"{gid}.json").write_text(json.dumps([cfg for _, cfg, _ in scenes], indent=1))
    fresh = (not force) and stamp.exists() and stamp.read_text() == sha
    if fresh and (not render or all(m.exists() for m in movs.values())) and (snap is None or (out / "stills" / f"{gid}.png").exists()):
        return movs
    built = [H.make_scene(t, c, proj, a) for t, c, a in scenes]
    if check:
        for d in built: H.lint_check(d)
    if snap is not None:
        (out / "stills").mkdir(exist_ok=True)
        d = built[0]
        for old in (d / "snapshots").glob("*.png"):
            try: old.unlink()                              # exFAT leaves ._ AppleDouble twins that vanish with their file
            except FileNotFoundError: pass
        shots = [x for x in H.snapshot(d, [snap]) if not x.name.startswith("._")]
        if shots: (out / "stills" / f"{gid}.png").write_bytes(shots[-1].read_bytes())
    if render:
        for d in built:
            m = out / "renders" / f"{d.name}.mov"
            if m.exists(): m.unlink()
            H.render(d, m)
        stamp.write_text(sha)
    elif snap is not None and not stamp.exists():
        pass
    return movs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheet", required=True); ap.add_argument("--out", required=True); ap.add_argument("--only")
    ap.add_argument("--render", action="store_true"); ap.add_argument("--snap", action="store_true"); ap.add_argument("--force", action="store_true")
    ap.add_argument("--range", nargs=2, type=float, help="only graphics that overlap these film seconds")
    A = ap.parse_args()
    S = json.load(open(A.sheet)); out = pathlib.Path(A.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    only = set(A.only.split(",")) if A.only else None
    man = []
    for g in S["graphics"]:
        scenes, meta = scenes_for(g)
        dur = scenes[0][1]["dur"]
        m = dict(id=g["id"], template=g["template"], a=g["t0"], b=g["t1"], canvas=CANVAS, mov=str(out / "renders" / f"{g['id']}.mov"), **meta)
        if meta["kind"] == "glass": m["mask"] = str(out / "renders" / f"{g['id']}_mask.mov")
        man.append(m)
        if (only and g["id"] not in only) or (A.range and not (g["t0"] < A.range[1] and g["t1"] > A.range[0])):
            continue
        build(scenes, out, render=A.render, snap=(max(0.5, dur - 0.6) if A.snap else None), force=A.force)
        print(f"{g['id']:5s} {g['template']:22s} {g['t0']:8.2f} - {g['t1']:8.2f}  {meta['kind']}", flush=True)
    json.dump(man, open(out / "manifest.json", "w"), indent=1)
    print(len(man), "graphics in", out / "manifest.json")


if __name__ == "__main__":
    main()
