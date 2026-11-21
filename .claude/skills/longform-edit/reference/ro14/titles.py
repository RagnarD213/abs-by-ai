"""RO-14 (from RO-17 / RO-11 round 3): the picture on the right of each of the seven section cards (Dan 2026-10-08: "Those look a little
empty... add an image to the right on each of those full-screen graphics").
TITLES holds, per card, the source, its licence, the label it needs and one crop per layout (fractions of the source:
left, top, right, bottom; the crop is then cut to the layout's exact aspect around its centre). prep() writes
assets/titles/<ID>_frame.jpg and <ID>_bleed.jpg, graded; gfx.title_card reads them.
usage: titles.py prep [IDS...] | titles.py stills <outdir> [IDS...]"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageOps, ImageEnhance
W = "/Volumes/Extreme/_edit_work/RO-14/round1"; OUT = f"{W}/assets/titles"; SRC = f"{OUT}/src"
ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
PHOTOS = f"{ROOT}/photos/finalized social media photos"
REAL = "Real picture of me. Not AI-generated."
AI = "AI-GENERATED"
PEX = "Pexels licence (free to use, no attribution needed)"
TITLES = {
 "T1": dict(src=f"{W}/assets/photos/px1309595.jpg", label=None, what="a plate of grilled chicken, carrots, broccoli and fries",
            licence=PEX, url="https://www.pexels.com/photo/1309595/", frame=(.25, 0, 1, 1), bleed=(.30, 0, 1, 1)),
 "T2": dict(src=f"{W}/assets/photos/px15572592.jpg", label=None, what="olive oil poured into a white bowl",
            licence=PEX, url="https://www.pexels.com/photo/15572592/", frame=(.2, 0, .85, 1), bleed=(.2, 0, .85, 1)),
 "T3": dict(src=f"{W}/assets/photos/px36729762.jpg", label=None, what="four friends sharing a pizza at a cafe table",
            licence=PEX, url="https://www.pexels.com/photo/36729762/", frame=(.3, 0, 1, 1), bleed=(.35, 0, 1, 1)),
 "G02": dict(src=f"{W}/assets/photos/px7991910.jpg", label=None, what="feet in grey socks on a bathroom scale (the 'In this video' card)",
            licence=PEX, url="https://www.pexels.com/photo/7991910/", frame=(.1, 0, .9, 1), bleed=(.12, 0, .88, 1)),
 "T4": dict(src=f"{W}/assets/photos/px6373219_app.jpg", label=None, what="a cup of black coffee beside a phone showing the app's photo-to-calories result (real B0035 frame put on the blank screen)",
            licence=PEX, url="https://www.pexels.com/photo/6373219/", frame=(.15, .05, .85, .95), bleed=(.15, .05, .85, .95)),
}
# gentle, per-picture: (brightness, contrast, saturation). Bright studio stills come down so they do not glare on the navy field.
GRADE = {"T2": (.96, 1.04, .98)}
SIZES = {"frame": lambda lab: (905, 820 if lab else 900), "bleed": lambda lab: (1120, 1080)}

def crop_to(im, box, aspect):
    """Largest window of the given aspect inside `box` (fractions), centred on the box."""
    iw, ih = im.size; l, t, r, b = box[0] * iw, box[1] * ih, box[2] * iw, box[3] * ih
    bw, bh = r - l, b - t
    if bw / bh > aspect: w, h = bh * aspect, bh
    else: w, h = bw, bw / aspect
    cx, cy = (l + r) / 2, (t + b) / 2
    return im.crop((round(cx - w / 2), round(cy - h / 2), round(cx + w / 2), round(cy + h / 2)))

def prep(only=()):
    os.makedirs(OUT, exist_ok=True); rec = {}
    for k, c in TITLES.items():
        if only and k not in only: continue
        src = ImageOps.exif_transpose(Image.open(c["src"])).convert("RGB")
        for lay in ("frame", "bleed"):
            w, h = SIZES[lay](c["label"])
            p = crop_to(src, c[lay], w / h)
            scale = (w * 1.06) / p.width                      # 6 % spare for the slow push
            p = p.resize((round(w * 1.06), round(h * 1.06)), Image.Resampling.LANCZOS)
            if k in GRADE:
                br, co, sa = GRADE[k]
                p = ImageEnhance.Color(ImageEnhance.Contrast(ImageEnhance.Brightness(p).enhance(br)).enhance(co)).enhance(sa)
            p.save(f"{OUT}/{k}_{lay}.jpg", quality=95, subsampling=0)
            rec[f"{k}_{lay}"] = dict(size=p.size, source_px=round(w * 1.06 / scale), scale=round(scale, 3))
        print(k, rec[f"{k}_frame"], rec[f"{k}_bleed"], flush=True)
    return rec

def item(k, layout="frame"):
    c = TITLES[k]
    return dict(photo=f"{OUT}/{k}", label=c["label"], layout=layout, chip=c.get("chip"))

if __name__ == "__main__":
    if sys.argv[1] == "prep":
        json.dump(prep(set(sys.argv[2:])), open(f"{OUT}/prep.json", "w"), indent=1)
    elif sys.argv[1] == "measure":
        # Label placement, measured on the rendered card (VIDEO-RULES: never over his face or abs). Vision person mask
        # + face box on the card WITHOUT the chip; the chip box must not touch the mask at all, with a margin.
        import gfx as G, numpy as np, subprocess, softblue as B
        PM = f"{ROOT}/.claude/skills/shorts/reference/recentre/personmask"
        out = sys.argv[2]; os.makedirs(out, exist_ok=True); res = {}
        R = {it["id"]: it for it in json.load(open(f"{W}/plan_resolved.json")) if it["kind"] == "title"}
        for k, c in TITLES.items():
            if not c["label"]: continue
            for lay in ("frame", "bleed"):
                x = item(k, lay); it = R[k]
                bare = G.title_card(2.0, it["step"], it["headline"], x["photo"], None, lay, None)
                if lay == "frame":      # the bare card draws the taller no-label frame; measure the labelled one
                    bare = B.field(2.0); F_ = G.TITLE_FRAME; fy = (1080 - F_["h_label"] - F_["gap"] - 80) / 2
                    B.photo_card(bare, f"{x['photo']}_frame.jpg", (F_["x"], fy, F_["w"], F_["h_label"]), 2.0, 0, fit=True, u=2.0)
                p = f"{out}/{k}_{lay}_bare.png"; bare.save(p)
                subprocess.run([PM, out, p], check=True, capture_output=True)
                mk = np.asarray(Image.open(f"{out}/{k}_{lay}_bare.mask.png").convert("L").resize((1920, 1080))) > 127
                full = G.title_card(2.0, it["step"], it["headline"], x["photo"], x["label"], lay, x["chip"])
                tmp = Image.new("RGB", (1920, 1080))
                if lay == "frame": box = B.disclosure(tmp, x["label"], (F_["x"] + F_["w"] / 2, fy + F_["h_label"] + F_["gap"]), 2.0, anchor="mt")
                else: box = B.disclosure(tmp, x["label"], tuple(x["chip"][0]), 2.0, anchor=x["chip"][1])
                x0, y0, x1, y1 = (int(round(v)) for v in box)
                ys, xs = np.nonzero(mk); m = 16
                over = int(mk[max(0, y0 - m):y1 + m, max(0, x0 - m):x1 + m].sum())
                # nearest mask pixel to the chip box
                dx = np.maximum(np.maximum(x0 - xs, xs - x1), 0); dy = np.maximum(np.maximum(y0 - ys, ys - y1), 0)
                res[f"{k}_{lay}"] = dict(chip=[x0, y0, x1, y1], person_bbox=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                                         mask_px_within_16=over, nearest_person_px=round(float(np.sqrt(dx * dx + dy * dy).min()), 1))
                print(k, lay, res[f"{k}_{lay}"], flush=True)
        json.dump(res, open(f"{out}/chips.json", "w"), indent=1)
    elif sys.argv[1] == "stills":
        import gfx as G
        out = sys.argv[2]; os.makedirs(out, exist_ok=True); only = set(sys.argv[3:])
        R = json.load(open(f"{W}/plan_resolved.json"))
        for it in R:
            if it["kind"] != "title" or (only and it["id"] not in only): continue
            for lay in ("frame", "bleed"):
                x = item(it["id"], lay)
                G.title_card(2.0, it["step"], it["headline"], x["photo"], x["label"], lay, x["chip"]).save(f"{out}/{it['id']}_{lay}.jpg", quality=90)
            print(it["id"], flush=True)
