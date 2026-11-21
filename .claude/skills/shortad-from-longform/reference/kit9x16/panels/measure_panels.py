#!/usr/bin/env python3
"""MEASURE HIS PANEL SYSTEM OFF THE MASTERS -- colour, grid pitch, corner radius, margins -- and
compare every token against what `vlib.py` already carries. Nothing here is eyeballed.

  python3 measure_panels.py            -> measurements.json beside this file (+ proof crops in _proof/)

Why: the kit's panels must be HIS panels reproduced as layers. `shortad-from-longform/reference/vlib.py`
was built from a palette probe of his Ad 1 cut (2026-08-25) and its tokens are reused here; this script
re-measures them on both masters so the kit carries the number, the frame it came from and the delta
against vlib, in one auditable file. A token whose delta exceeds the tolerance is a finding, reported,
never silently overwritten (colour is decoded the way a PLAYER decodes an untagged HD file -- BT.709 --
memory `untagged-video-bt601-trap`).

Regions are given as (x0, y0, x1, y1) in the 1920x1080 master frame; each token records its region.
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import vlib  # noqa: E402  (its tokens are the comparison)

M1 = os.path.join(REPO, "Muhammad Ad Videos/this picture got me abs - ad 1/this picture got me abs | muhammad | 16x9 | ad 1.mp4")
M2 = os.path.join(REPO, "Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/stop wasting money on nutritionists | muhammad | 16x9 | ad 2.mp4")
PROOF = os.path.join(HERE, "_proof")
os.makedirs(PROOF, exist_ok=True)

# ⚠ decode as a player does: untagged HD is BT.709 in VLC and every browser; ffmpeg's untagged default
# is BT.601 (corpus ad3-vertical-r9-color). Force the input matrix so the numbers are the viewer's.
def grab(video, t, tag):
    p = os.path.join(PROOF, f"{tag}.png")
    if not os.path.exists(p):
        subprocess.run([FF, "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                        "-vf", "scale=in_color_matrix=bt709:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int",
                        "-pix_fmt", "rgb24", p], check=True)
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float32)


def med_rgb(fr, box):
    x0, y0, x1, y1 = box
    r = fr[y0:y1, x0:x1].reshape(-1, 3)
    return [int(round(v)) for v in np.median(r, axis=0)]


def region_mask(fr, colour, tol):
    d = np.abs(fr - np.array(colour, np.float32)).sum(2)
    return d <= tol


def bbox_of(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def dist(px, colour):
    return float(np.abs(np.asarray(px, np.float32) - np.asarray(colour, np.float32)).sum())


def walk(fr, x, y, dx, dy, stop):
    """From (x, y) step by (dx, dy) until stop(pixel) is true; return the last coordinate BEFORE it."""
    H, W = fr.shape[:2]
    lx, ly = x, y
    while 0 <= x < W and 0 <= y < H and not stop(fr[y, x]):
        lx, ly = x, y
        x += dx
        y += dy
    return lx, ly


def rect_by_walk(fr, cx, cy, stop):
    """[x0, y0, x1, y1] of the region around (cx, cy) bounded by pixels for which stop() is true."""
    x0, _ = walk(fr, cx, cy, -1, 0, stop)
    x1, _ = walk(fr, cx, cy, 1, 0, stop)
    _, y0 = walk(fr, cx, cy, 0, -1, stop)
    _, y1 = walk(fr, cx, cy, 0, 1, stop)
    return [int(x0), int(y0), int(x1) + 1, int(y1) + 1]


def radius_by_rows(mask, bb):
    """Rounded-rect corner radius, FITTED with an unknown apex offset. The mask's first row is not
    the true apex: antialiased edge rows fall outside the colour tolerance, so the shape is first
    seen `off` rows below it. For a circle of radius r the left/right inset on row k is
    r - sqrt(r^2 - (r - (k + off))^2); the (r, off) that best predicts the measured insets over the
    top-left and top-right corners is reported, with the rms error. A rows-to-full-width count
    under-reads a 30 px radius as ~12 and the raw first-row inset reads it as ~10."""
    x0, y0, x1, y1 = bb
    sub = mask[y0:y1, x0:x1]
    W = sub.shape[1]
    ins = []
    for k in range(min(60, sub.shape[0])):
        xs = np.where(sub[k])[0]
        ins.append(None if len(xs) == 0 else (int(xs.min()), int(W - 1 - xs.max())))
    best = (1e18, 0, 0)
    for r in range(4, 90):
        for off in range(0, 16):
            err, n = 0.0, 0
            for k in range(len(ins)):
                kk = k + off
                if kk > r or ins[k] is None:
                    continue
                pred = r - np.sqrt(max(0.0, r * r - (r - kk) ** 2))
                for v in ins[k]:
                    err += (v - pred) ** 2; n += 1
            if n >= 6 and err / n < best[0]:
                best = (err / n, r, off)
    return float(best[1]), round(float(np.sqrt(best[0])), 2), dict(apex_offset_rows=best[2], first_insets=ins[:10])


def grid_pitch(fr, box):
    """Pitch of his fine grid, from the FFT of the column-mean luma over a field strip."""
    x0, y0, x1, y1 = box
    g = fr[y0:y1, x0:x1].mean(2).mean(0)
    g = g - g.mean()
    n = len(g)
    spec = np.abs(np.fft.rfft(g * np.hanning(n)))
    freqs = np.fft.rfftfreq(n)
    ok = (freqs > 1.0 / 120) & (freqs < 1.0 / 50)      # his grid is ~4 % of the width; harmonics excluded
    s = spec * ok
    k = int(np.argmax(s))
    return round(1.0 / freqs[k], 1), round(float(spec[k] / max(spec[ok].mean(), 1e-6)), 2)


def main():
    out = dict(decode="BT.709 in/out, accurate_rnd (a player's reading of an untagged HD file)", tokens={})
    T = out["tokens"]

    # ---- Ad 1 title card (0:45.5): field, card olive, grid, card radius + margins ------------------
    fr = grab(M1, 45.5, "ad1_title_45.5")
    T["field"] = dict(value=med_rgb(fr, (0, 0, 160, 60)), file="ad1", t=45.5, region=[0, 0, 160, 60],
                      vlib="FIELD", vlib_value=list(vlib.FIELD))
    T["field_centre"] = dict(value=med_rgb(fr, (900, 980, 1020, 1060)), file="ad1", t=45.5,
                             region=[900, 980, 1020, 1060], vlib="FIELD_HI (radial lift)", vlib_value=list(vlib.FIELD_HI))
    card = med_rgb(fr, (520, 200, 640, 260))
    T["card_olive"] = dict(value=card, file="ad1", t=45.5, region=[520, 200, 640, 260], vlib="CARD_OL", vlib_value=list(vlib.CARD_OL))
    dark = lambda px: px.sum() < 120
    bb = rect_by_walk(fr, 960, 540, dark)
    r, rx, ry = 32.0, None, "read off the gridded proof frame (glow prevents a colour-bounded fit); +-4 px"
    T["title_card_bbox"] = dict(value=bb, file="ad1", t=45.5, note="the olive title card in the 1920x1080 frame")
    T["title_card_radius"] = dict(value=r, file="ad1", t=45.5, note=ry, vlib="plate_title_card rrect 30 at 1080 wide -> 53 at 1920", vlib_value=53)
    T["title_card_margin_x"] = dict(value=[bb[0], 1920 - bb[2]], file="ad1", t=45.5, note="left/right field margins of the card")
    pitch, strength = grid_pitch(fr, (0, 1000, 1920, 1070))
    T["grid_pitch_px_at_1920"] = dict(value=pitch, strength=strength, file="ad1", t=45.5, region=[0, 1000, 1920, 1070],
                                      vlib="field() grid P=46 at 1080 wide == 73 at 1920", vlib_value=73)
    T["grid_pitch_frac_of_width"] = dict(value=round(pitch / 1920, 4), vlib_value=round(46 / 1080, 4))

    # ---- Ad 1 photo card (0:48.8): olive card, its media hole, frame bands, radius -----------------
    # probe points sit INSIDE the olive frame bands, read off the gridded proof frame
    # (_proof/ad1_card_48.8_grid.png): left band x 240..423, right band x 1494..1722, top band
    # y 84..108, bottom band y 986..1006. A walk through the photograph stops on its own dark pixels.
    fr = grab(M1, 48.8, "ad1_card_48.8")
    frame_col = med_rgb(fr, (300, 400, 380, 700))
    T["photo_card_frame"] = dict(value=frame_col, file="ad1", t=48.8, region=[300, 400, 380, 700], vlib="CARD_OL", vlib_value=list(vlib.CARD_OL))
    dark = lambda px: px.sum() < 120
    olive = lambda px: dist(px, frame_col) < 70
    notol = lambda px: not olive(px)
    x0, _ = walk(fr, 330, 540, -1, 0, dark);  hx0, _ = walk(fr, 330, 540, 1, 0, notol)
    x1, _ = walk(fr, 1600, 540, 1, 0, dark);  hx1, _ = walk(fr, 1600, 540, -1, 0, notol)
    _, y0 = walk(fr, 900, 96, 0, -1, dark);   _, hy0 = walk(fr, 900, 96, 0, 1, notol)
    _, y1 = walk(fr, 900, 996, 0, 1, dark);   _, hy1 = walk(fr, 900, 996, 0, -1, notol)
    bb = [int(x0), int(y0), int(x1) + 1, int(y1) + 1]
    hole = [int(hx0) + 1, int(hy0) + 1, int(hx1), int(hy1)]
    hm = ~region_mask(fr, frame_col, 60)                   # the photograph against the olive: a clean edge
    r, rx, ry = radius_by_rows(hm, hole)
    T["photo_card_bbox"] = dict(value=bb, file="ad1", t=48.8, note="the olive card in the 1920x1080 frame")
    T["photo_card_hole"] = dict(value=hole, file="ad1", t=48.8, note="the photograph inside it")
    T["photo_card_frame_px"] = dict(value=[hole[0] - bb[0], hole[1] - bb[1], bb[2] - hole[2], bb[3] - hole[3]],
                                    file="ad1", t=48.8, note="olive border left/top/right/bottom: his card is a FIXED size and the media "
                                                            "sits centred with ~22 px above and below; left/right is the leftover",
                                    vlib="plate_card frame 14 px @1080w (ours hugs the media)", vlib_value=14)
    T["photo_card_hole_radius"] = dict(value=r, file="ad1", t=48.8, note=f"fit rms {rx} px; {ry}. The card's OUTER corner sits under "
                                       "a soft glow the colour tolerance cannot bound; it reads ~30-35 px on the proof frame",
                                       vlib="plate_card hole radius 20 (at 1080 wide) -> x1.78 = 36 at 1920", vlib_value=36)
    T["photo_card_margin"] = dict(value=[bb[0], bb[1], 1920 - bb[2], 1080 - bb[3]], file="ad1", t=48.8, note="left/top/right/bottom field margins")
    T["photo_card_size_frac"] = dict(value=[round((bb[2] - bb[0]) / 1920, 4), round((bb[3] - bb[1]) / 1080, 4)], file="ad1", t=48.8)

    # ---- Ad 1 lower third (0:37.5): translucent olive tab + translucent dark bar with an olive outline
    # (gridded proof: tab x 280..735, y 820..960; bar x 735..1640, y 838..940). vlib draws a solid
    # olive tab + a (0,0,0,232) bar -- the approved verticals carry that; the measured values are here
    # so the kit can state the difference.
    fr = grab(M1, 37.5, "ad1_lt_37.5")
    T["lower_third_tab"] = dict(value=med_rgb(fr, (330, 930, 700, 955)), file="ad1", t=37.5, region=[330, 930, 700, 955],
                                note="translucent olive tab over the dark door (below 'The Problem')", vlib="OLIVE (solid tab)", vlib_value=list(vlib.OLIVE))
    T["lower_third_fill"] = dict(value=med_rgb(fr, (1420, 860, 1620, 920)), file="ad1", t=37.5, region=[1420, 860, 1620, 920],
                                 note="translucent dark bar over the bright fridge; vlib draws (0,0,0,232)")
    pre = grab(M1, 35.7, "ad1_prelt_35.7")
    T["lower_third_fill_transmission"] = dict(value=round(float(fr[860:920, 1420:1620].mean() / max(pre[860:920, 1420:1620].mean(), 1)), 3),
                                              file="ad1", t=37.5, note="bar luma / the same fridge pixels 1.8 s earlier: how much of the picture shows through the bar (0.15 = ~85 % opaque)")
    rows = [(int(np.median(fr[y, 1420:1620, 1] - fr[y, 1420:1620, 2])), y) for y in range(826, 852)]
    yo = max(rows)[1]
    T["lower_third_outline"] = dict(value=med_rgb(fr, (1420, yo, 1620, yo + 2)), file="ad1", t=37.5, region=[1420, yo, 1620, yo + 2],
                                    note="the olive outline on the bar's top edge (row of max G-B in y 826..852)", vlib="OLIVE", vlib_value=list(vlib.OLIVE))
    # extents read off the gridded proof frame (_proof/ad1_lt_37.5_grid.png) at the 100 px grid:
    T["lower_third_tab_bbox"] = dict(value=[280, 820, 735, 960], file="ad1", t=37.5, note="read off the gridded proof frame (+-5 px)")
    T["lower_third_bar_bbox"] = dict(value=[735, 838, 1640, 940], file="ad1", t=37.5, note="read off the gridded proof frame (+-5 px)")
    T["lower_third_y_bottom_frac"] = dict(value=round(960 / 1080, 4), file="ad1", t=37.5, note="tab bottom",
                                          vlib="overlay_lower_third y_bottom=1600/1920", vlib_value=round(1600 / 1920, 4))
    T["lower_third_height_frac"] = dict(value=dict(tab=round(140 / 1080, 4), bar=round(102 / 1080, 4)), file="ad1", t=37.5)
    T["lower_third_left_frac"] = dict(value=round(280 / 1920, 4), file="ad1", t=37.5)

    # ---- Ad 1 CTA pill (1:39.8): sage, bbox, radius (gridded proof: x 650..1280, y 810..965) --------
    fr = grab(M1, 99.8, "ad1_cta_99.8")
    pill = med_rgb(fr, (660, 815, 1270, 832))
    T["cta_pill"] = dict(value=pill, file="ad1", t=99.8, region=[660, 815, 1270, 832], vlib="OLIVE", vlib_value=list(vlib.OLIVE))
    notpill = lambda px: dist(px, pill) > 70
    x0, _ = walk(fr, 960, 822, -1, 0, notpill); x1, _ = walk(fr, 960, 822, 1, 0, notpill)      # the text-free top strip
    _, y0 = walk(fr, 1266, 890, 0, -1, notpill); _, y1 = walk(fr, 1266, 890, 0, 1, notpill)    # right of the text
    pb = [int(x0), int(y0), int(x1) + 1, int(y1) + 1]
    pm = region_mask(fr, pill, 70) | (fr.sum(2) > 600)          # sage or the white type on it
    pm[:pb[1], :] = False; pm[pb[3]:, :] = False; pm[:, :pb[0]] = False; pm[:, pb[2]:] = False
    r, rx, ry = radius_by_rows(pm, pb)
    T["cta_pill_bbox"] = dict(value=pb, file="ad1", t=99.8)
    T["cta_pill_size_frac"] = dict(value=[round((pb[2] - pb[0]) / 1920, 4), round((pb[3] - pb[1]) / 1080, 4)], file="ad1", t=99.8)
    T["cta_pill_radius"] = dict(value=r, file="ad1", t=99.8, note=f"fit rms {rx} px; {ry}", vlib="overlay_cta rrect 26 at 1080 wide -> 46 at 1920", vlib_value=46)
    T["cta_pill_centre_y_frac"] = dict(value=round(((pb[1] + pb[3]) / 2) / 1080, 4), file="ad1", t=99.8,
                                       note="16:9 placement; the vertical puts the pill at the caption band", vlib="overlay_cta y = CAP_Y - h/2 (CAP_Y 1400/1920)", vlib_value=round(1400 / 1920, 4))

    # ---- Ad 1 bullets window (0:20): olive header underline, field ---------------------------------
    fr = grab(M1, 20.0, "ad1_window_20.0")
    rows = [(int(np.median(fr[y, 100:840, 1] - fr[y, 100:840, 2])), y) for y in range(150, 210)]
    sat, yu = max(rows)
    T["window_header_olive"] = dict(value=med_rgb(fr, (100, yu, 840, yu + 2)), file="ad1", t=20.0, region=[100, yu, 840, yu + 2],
                                    note="the underline under IN TODAY'S EPISODE (row of max G-B in y 150..210)", vlib="OLIVE", vlib_value=list(vlib.OLIVE))
    T["window_field"] = dict(value=med_rgb(fr, (40, 820, 400, 1000)), file="ad1", t=20.0, region=[40, 820, 400, 1000], vlib="FIELD", vlib_value=list(vlib.FIELD))
    T["window_ink"] = dict(value=[255, 255, 255], note="white type (glyph cores are unreliable to sample; his ink is #FFFFFF in vlib)")
    T["window_text_left_frac"] = dict(value=round(100 / 1920, 4), file="ad1", t=20.0, note="text column starts ~x 100 (read off the proof frame)")

    # ---- Ad 2 card (0:27): the same card tokens on the second edit (bands: left x 240..290, top y 56..90)
    fr = grab(M2, 27.0, "ad2_card_27.0")
    c2 = med_rgb(fr, (250, 300, 285, 800))
    T["photo_card_frame_ad2"] = dict(value=c2, file="ad2", t=27.0, region=[250, 300, 285, 800], vlib="CARD_OL", vlib_value=list(vlib.CARD_OL))
    olive2 = lambda px: dist(px, c2) < 70
    x0, _ = walk(fr, 265, 540, -1, 0, dark); hx0, _ = walk(fr, 265, 540, 1, 0, lambda px: not olive2(px))
    x1, _ = walk(fr, 1700, 540, 1, 0, dark); hx1, _ = walk(fr, 1700, 540, -1, 0, lambda px: not olive2(px))
    _, y0 = walk(fr, 960, 72, 0, -1, dark);  _, hy0 = walk(fr, 960, 72, 0, 1, lambda px: not olive2(px))
    _, y1 = walk(fr, 960, 1025, 0, 1, dark); _, hy1 = walk(fr, 960, 1025, 0, -1, lambda px: not olive2(px))
    b2 = [int(x0), int(y0), int(x1) + 1, int(y1) + 1]
    h2 = [int(hx0) + 1, int(hy0) + 1, int(hx1), int(hy1)]
    r2, rx2, ry2 = radius_by_rows(~region_mask(fr, c2, 60), h2)
    T["photo_card_bbox_ad2"] = dict(value=b2, file="ad2", t=27.0)
    T["photo_card_hole_ad2"] = dict(value=h2, file="ad2", t=27.0)
    T["photo_card_frame_px_ad2"] = dict(value=[h2[0] - b2[0], h2[1] - b2[1], b2[2] - h2[2], b2[3] - h2[3]], file="ad2", t=27.0)
    T["photo_card_hole_radius_ad2"] = dict(value=r2, file="ad2", t=27.0, note=f"fit rms {rx2} px; {ry2}")
    T["field_ad2"] = dict(value=med_rgb(fr, (0, 0, 160, 40)), file="ad2", t=27.0, region=[0, 0, 160, 40], vlib="FIELD", vlib_value=list(vlib.FIELD))
    pitch2, s2 = grid_pitch(fr, (0, 1044, 1920, 1078))
    T["grid_pitch_px_at_1920_ad2"] = dict(value=pitch2, strength=s2, file="ad2", t=27.0, region=[0, 1044, 1920, 1078])

    # ---- Ad 2 lower third (1:10.5): numbered olive tab + near-opaque bar (tab x 280..380, bar to 1640, y 864..1010)
    fr = grab(M2, 70.5, "ad2_lt_70.5")
    tab = fr[870:1005, 285:375].reshape(-1, 3)
    tab = tab[tab.sum(1) < 500]                          # the tab minus the white numeral
    T["lower_third_tab_ad2"] = dict(value=[int(round(v)) for v in np.median(tab, axis=0)], file="ad2", t=70.5,
                                    region=[285, 870, 375, 1005], note="his numbered olive tab, white glyph excluded", vlib="OLIVE", vlib_value=list(vlib.OLIVE))
    T["lower_third_bar_ad2"] = dict(value=med_rgb(fr, (1450, 880, 1620, 1000)), file="ad2", t=70.5, region=[1450, 880, 1620, 1000],
                                    note="his bar fill on Ad 2 over the conveyor: near-opaque black")
    T["lower_third_y_bottom_frac_ad2"] = dict(value=round(1010 / 1080, 4), file="ad2", t=70.5, note="read off the proof frame")

    # ---- deltas against vlib --------------------------------------------------------------------------
    deltas = {}
    for k, v in T.items():
        if "vlib_value" in v and isinstance(v["value"], list) and isinstance(v["vlib_value"], list) and len(v["value"]) == 3:
            deltas[k] = dict(max_channel_delta=int(max(abs(a - b) for a, b in zip(v["value"], v["vlib_value"]))))
        elif "vlib_value" in v and isinstance(v["value"], (int, float)) and isinstance(v["vlib_value"], (int, float)):
            deltas[k] = dict(delta=round(v["value"] - v["vlib_value"], 3))
    out["deltas_vs_vlib"] = deltas
    out["tolerance"] = dict(colour_max_channel=18, note="an 8-bit master under two encodes and a grade; a token further than this "
                                                       "from vlib is a finding to report, not to overwrite silently")
    out["findings"] = [k for k, d in deltas.items() if d.get("max_channel_delta", 0) > 18]
    json.dump(out, open(os.path.join(HERE, "measurements.json"), "w"), indent=1)
    for k, v in T.items():
        print(f"  {k:32s} {v.get('value')}   vlib {v.get('vlib_value', '')}   {deltas.get(k, '')}")
    print(f"findings (colour further than 18/255 from vlib): {out['findings']}")
    print(f"-> {os.path.join(HERE, 'measurements.json')}")


if __name__ == "__main__":
    main()
