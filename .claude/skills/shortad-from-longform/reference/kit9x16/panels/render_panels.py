#!/usr/bin/env python3
"""RENDER HIS PANEL SYSTEM AS LAYERS at 1080x1920 -- the kit's visual asset set, produced by the SAME
vlib calls the renderer makes, so a layer here is what a build will composite.

  python3 render_panels.py        -> panels/layers/*.png + panels/layers/index.json

Layers: the field (dark + radial lift + grid), a photo card frame at the card hole for a 4:5 and a
16:9 media, the window plate (Dan above / bullets below) at its settled frame, the statement window,
the title card, the lower third (settled frame), the CTA pill (settled frame). Every layer names the
vlib function and the arguments it was rendered with, and `measurements.json` beside it holds his
numbers for the same elements, so the pairing is auditable. Nothing in Media/.
"""
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))       # shortad-from-longform/reference (vlib, motionlib via vlib)
import vlib  # noqa: E402

OUT = os.path.join(HERE, "layers")
os.makedirs(OUT, exist_ok=True)


def save(name, im, meta):
    p = os.path.join(OUT, name + ".png")
    im.save(p)
    meta["file"] = os.path.basename(p)
    return meta


def main():
    idx = {}
    idx["field"] = save("field", vlib.field(), dict(fn="vlib.field()", tokens=dict(FIELD=vlib.FIELD, FIELD_HI=vlib.FIELD_HI, grid_px=46)))
    # photo card frames: settled frame (t = 1 s) of plate_card for two media aspects
    for tag, ar in (("card_4x5", 0.80), ("card_16x9", 16 / 9)):
        fr, hole = vlib.plate_card(1.2, media_ar=ar)
        idx[tag] = save(tag, fr[-1], dict(fn=f"vlib.plate_card(dur, media_ar={ar:.3f})", hole=list(hole),
                                          tokens=dict(CARD_OL=vlib.CARD_OL, frame_px=14, radius=30, hole_radius=20, glow=26)))
    fr, hole = vlib.plate_card(1.2, media_ar=0.80, label="AI-GENERATED")
    idx["card_4x5_ai_chip"] = save("card_4x5_ai_chip", fr[-1], dict(fn="vlib.plate_card(dur, media_ar=0.80, label='AI-GENERATED')", hole=list(hole),
                                                                   note="the card's own chip hangs off the hole bottom (plate_card): not on Dan's body"))
    fr, rect = vlib.plate_window("In today's episode",
                                 ["How I got limitless motivation to work out, to eat healthy.",
                                  "What I needed to do to lose my belly fat and get six-pack abs."], 3.0)
    idx["window_bullets"] = save("window_bullets", fr[-1], dict(fn="vlib.plate_window(header, bullets, dur)", dan_window=list(rect),
                                                              tokens=dict(header_px=46, bullet_px=50, margin=vlib.MARGIN, clamp=[820, 1220])))
    fr, rect = vlib.plate_stmt_window([("Its far superior at making these images than", "ink"), ("Chat GPT", "olive"),
                                       ("Or any general purpose AI", "big")], 3.0)
    idx["window_statement"] = save("window_statement", fr[-1], dict(fn="vlib.plate_stmt_window(parts, dur)", dan_window=list(rect)))
    fr, rect, mh = vlib.plate_window_media(3.0, 9 / 16)
    idx["window_media"] = save("window_media", fr[-1], dict(fn="vlib.plate_window_media(dur, media_ar=0.5625)", dan_window=list(rect), media_hole=list(mh)))
    fr, _ = vlib.plate_title_card("Visualizing your goal", "One of the most powerful ways to motivate yourself", 3.0)
    idx["title_card"] = save("title_card", fr[-1], dict(fn="vlib.plate_title_card(headline, sub, dur)", tokens=dict(radius=30, glow=26, headline_px=96)))
    fr, _ = vlib.overlay_lower_third(["The Problem", "No time, no motivation"], 3.0)
    idx["lower_third"] = save("lower_third", fr[len(fr) // 2], dict(fn="vlib.overlay_lower_third(lines, dur, y_bottom=1600)",
                                                                   tokens=dict(tab=vlib.OLIVE, bar_alpha=232, y_bottom=1600, line1_px=52, line2_px=40),
                                                                   his=dict(tab="translucent olive", bar="translucent black ~85 % opaque with an olive outline",
                                                                            note="see measurements.json lower_third_*; the approved verticals carry vlib's solid tab")))
    fr, _ = vlib.overlay_cta("Get A FREE AI Image Of Yourself", "With Abs", 3.0)
    idx["cta_pill"] = save("cta_pill", fr[len(fr) // 2], dict(fn="vlib.overlay_cta(top, big, dur)", tokens=dict(fill=vlib.OLIVE, radius=26, glow=16, y="CAP_Y - h/2")))
    fr, _ = vlib.overlay_flash(0.44)
    idx["flash_peak"] = save("flash_peak", fr[len(fr) // 3], dict(fn="vlib.overlay_flash(dur)", note="the synthesised light leak; the attempt-3 Ad 1 build used his extracted template instead (_flash/final)"))
    m = (vlib.vignette_mask() * 255).clip(0, 255).astype("uint8") if os.path.exists(os.path.join(HERE, "..", "..", "grade.py")) else None
    if m is not None:
        idx["vignette"] = save("vignette", Image.fromarray(m), dict(fn="vlib.vignette_mask()", note="his radial falloff remapped into 9:16 (grade.VIGNETTE)"))
    idx["_meta"] = dict(frame=[vlib.VW, vlib.VH], cap_y=vlib.CAP_Y, safe=dict(top=vlib.TOP_SAFE, bottom=vlib.BOT_SAFE),
                        palette=dict(FIELD=vlib.FIELD, FIELD_HI=vlib.FIELD_HI, OLIVE=vlib.OLIVE, CARD_OL=vlib.CARD_OL, INK=vlib.INK, INK_SOFT=vlib.INK_SOFT))
    json.dump(idx, open(os.path.join(OUT, "index.json"), "w"), indent=1)
    print(f"{len(idx) - 1} layers -> {OUT}")


if __name__ == "__main__":
    main()
