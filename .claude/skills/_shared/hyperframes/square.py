"""THE 1:1 LAYOUTS OF THE SOFT BLUE LIGHT TEMPLATES (2026-10-02). The same template files and the same configs that
draw a graphic at 16:9 (and at 9:16 through vertical.py) draw it at 1080x1080 here. Nothing is retyped: this module
loads a second copy of vertical.py with the square canvas and replaces only the layouts whose 9:16 numbers do not
hold in a square. softblue.py already carries the 1:1 geometry for the lower third and the 3A card.

  python3 square.py --sheet SHEET.json --out OUT_DIR [--only G01,G02] [--render] [--snap] [--range A B]

  template              1:1 layout (the standard it follows)
  lower-third           strip x 68..1012 at the BOTTOM (bottom edge 64 px from the frame edge); captions lift above it
                        (SOFTBLUE.md: "16:9 and 1:1 at the bottom"); a long point wraps and the strip grows upward
  side-list             the 3A card full width, 36 px margins, at the bottom, type 1.0x (locked by Dan 2026-09-28)
  cycle                 the 740 x 488 card scaled to the full width, at the bottom
  before-card           photo on top, glass fact card beneath (the stacked layout, shorter photo)
  title-card            eyebrow + headline lines (+ recap rows) on the field
  media-card            the field with a hole for the clip, photo or phone; a card under running captions ends above
                        the square caption line (y 848, the approved Ad 1 square's rule); the chip 68 px under the hole
  cta                   a glass button at the bottom (captions pause under it)
  tally                 the top-left chip (under the top 48 px)

NOT approved by Dan until he passes a square graphic-lock page (VIDEO-RULES 2026-10-01: the first square gets a full
pre-approval round).
"""
import importlib.util, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

_spec = importlib.util.spec_from_file_location("vertical_sq", HERE / "vertical.py")
SQ = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SQ)
H, B = SQ.H, SQ.B

W = Hh = 1080
CAP_LINE = 880                                       # the approved squares' caption line (a11_sq_ad1: CAP_Y 880)
CARD_END = 848                                       # a card under running captions ends here (same source)
SQ.W, SQ.Hh, SQ.CANVAS = W, Hh, [W, Hh]
SQ.U = B.unit(W, Hh)                                 # 2.0
SQ.CAP_TOP = CAP_LINE
SQ.CARD_BOTTOM = Hh - SQ.SIDE                        # the 3A card's 1:1 bottom (softblue._lt_geom)
SQ.CAPTION_BAND = (CAP_LINE - 20, CAP_LINE + 100)
U, SIDE = SQ.U, SQ.SIDE


def media_card_scene(gid, dur, media_ar, label=None, kicker=None, spans=None, max_w=None, max_h=None, caps=False):
    """The square plate for one card: (scene tuple, hole [x0, y0, x1, y1]). The hole keeps the media's own shape
    (a horizontal clip is never cropped shorter). Under running captions the card and its chip end above y 848;
    a card whose captions are off (a phone) may use the frame down to y 1040."""
    extra = (68 + 80 if label else 0)
    top, bottom = 64, (CARD_END if caps else Hh - 40)
    max_w = max_w or (W - 2 * SIDE)
    max_h = min(max_h or 10 ** 6, bottom - top - extra)
    hw = max_w; hh = hw / media_ar
    if hh > max_h: hh = max_h; hw = hh * media_ar
    hw, hh = int(hw) // 2 * 2, int(hh) // 2 * 2
    hx = (W - hw) // 2
    hy = int(top + (bottom - top - hh - extra) / 2)
    c = dict(id=gid, dur=round(dur, 3), canvas=[W, Hh], hole=[hx, hy, hw, hh], radius=26 if media_ar > 0.7 else 44)
    if label:
        cw_ = round(H.text_w(label, 23 * U, False) + 40 * U)
        c["chip"] = dict(x=round(W / 2 - cw_ / 2), y=hy + hh + 68, s=label, w=cw_)
        if spans: c["chip"]["spans"] = spans
    if kicker:
        c["kicker"] = dict(x=hx + 4, y=max(8, hy - 84), px=40, s=kicker)
    return (HERE / "media-card" / "media-card.template.htm", c, ()), [hx, hy, hx + hw, hy + hh]


def cta_scenes(gid, dur, top, big, hold_out=False, full=False):
    x0, _, x1, _ = B.lower_third_default_box(W, Hh)
    bw, bh = x1 - x0, 110 * U
    by = (Hh - 32 * U - bh) if not full else (Hh - bh) / 2
    big_px = 64
    while big_px > 44 and H.text_w(big, big_px) > bw - 200: big_px -= 2
    top_px = 30
    while top_px > 22 and H.text_w(top, top_px) > bw - 80: top_px -= 1
    bx_ = x0 + (bw - H.text_w(big, big_px) - 56) / 2
    L = dict(btn=[x0, by, bw, bh], radius=22 * U, top=dict(x=round(x0 + (bw - H.text_w(top, top_px)) / 2), y=round(by + 24 * U), px=top_px, s=top),
             big=dict(x=round(bx_), y=round(by + 24 * U + top_px * 1.4 + 6), px=big_px, s=big),
             arrow=dict(x=round(bx_ + H.text_w(big, big_px) + 22), y=round(by + 24 * U + top_px * 1.4 + 6), px=big_px))
    out = [(HERE / "cta" / "cta.template.htm", dict(id=gid + ("_mask" if m == "mask" else ""), mode=m, dur=round(dur, 3), canvas=[W, Hh],
                                                    hold_out=hold_out, full=full, **L), ()) for m in (("content",) if full else ("content", "mask"))]
    return out, dict(kind="opaque" if full else "glass", band=[int(by - 12), int(min(Hh, by + bh + 60))], box=[round(x0), round(by), round(x1), round(by + bh)])


def tally_scenes(gid, dur, label, value, frm=0, prefix="$", unit="/ month", at=0.45, count=0.6, y=60):
    return _tally(gid, dur, label, value, frm, prefix, unit, at, count, y)


def fact_scenes(c):
    """The 1:1 before / fact card: a square has the width for the 16:9 split, so the whole photo stands on the LEFT
    at full height and the glass fact card sits to its RIGHT, its lines stacked (never a cover crop of the photo)."""
    from PIL import Image, ImageOps
    a = c["a"]
    label = c.get("label"); detail = c.get("detail")
    iw, ih = ImageOps.exif_transpose(Image.open(c["photo"])).size
    top, bot = 70, Hh - 70 - (68 + 80 if label else 0)
    ph = bot - top; pw = round(ph * iw / ih)
    if pw > 500: pw = 500; ph = round(pw * ih / iw)
    px, py = 60, top + (bot - top - ph) // 2
    kx = px + pw + 44; kw = W - 50 - kx
    head = c["headline"]
    inner = kw - 27 * U - 16 * U
    hp = 42 * U                                       # the template's own headline size
    assert max(H.text_w(p, hp) for p, _ in head) <= inner, f"{c['id']}: headline too wide for the 1:1 card"
    assert H.text_w(c["eyebrow"][0], 32 * U) <= inner, f"{c['id']}: eyebrow too wide for the 1:1 card"
    lh = 60 * U
    kh = (83 + 0) * U + len(head) * lh + (56 * U if detail else 0) + 20 * U
    ky = py + (ph - kh) / 2
    cx = kx + 27 * U
    ext = pathlib.Path(c["photo"]).suffix.lower()
    chip = None
    if label:
        cw_ = round(H.text_w(label, 23 * U, False) + 40 * U)
        chip = dict(x=round(max(20, min(W - 20 - cw_, px + pw / 2 - cw_ / 2))), y=py + ph + 20 * U, s=label, w=cw_)
    s = dict(id=c["id"], dur=round(c["b"] - a, 3), push=c.get("push", 1.05), drift=c.get("drift", -8), canvas=[W, Hh],
             photo=dict(x=px, y=py, w=pw, h=ph, src="assets/photo" + ext), chip=chip,
             card=[kx, ky, kw, kh],
             eyebrow=dict(x=cx, y=ky + 22 * U, s=c["eyebrow"][0], t=H.rel(c["eyebrow"][1], a)),
             head=[dict(x=cx, y=ky + 83 * U + i * lh, s=p, t=H.rel(t, a)) for i, (p, t) in enumerate(head)],
             detail=None, sweep=H.rel(c["sweep"], a) if c.get("sweep") else None)
    if detail:
        lines = B.wrap(detail[0], B.font(23 * U, False), inner)
        assert len(lines) == 1, f"{c['id']}: detail {detail[0]!r} needs one line in the 1:1 card"
        s["detail"] = dict(x=cx + U, y=ky + 83 * U + len(head) * lh + 6 * U, s=detail[0], t=H.rel(detail[1], a))
    return [(HERE / "before-card" / "before-card.template.htm", s, [(c["photo"], "photo" + ext)])], dict(kind="opaque")


_tally = SQ.tally_scenes
SQ.fact_scenes = fact_scenes
SQ.media_card_scene = media_card_scene
SQ.cta_scenes = cta_scenes
SQ.tally_scenes = tally_scenes

# the names a caller uses, the same as vertical.py's
lt_scenes, list_scenes, cycle_scenes, title_scenes = SQ.lt_scenes, SQ.list_scenes, SQ.cycle_scenes, SQ.title_scenes
scenes_for, build, tsha = SQ.scenes_for, SQ.build, SQ.tsha

if __name__ == "__main__":
    SQ.main()
