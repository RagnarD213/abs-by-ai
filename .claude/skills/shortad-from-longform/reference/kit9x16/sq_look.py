#!/usr/bin/env python3
"""THE SQUARE LOOK PAGE'S MEDIA (the first 1:1 in Soft Blue Light gets a pre-approval round: VIDEO-RULES 2026-10-01).
From a vertical Soft Blue Light build that has reached `captions`, draw every graphic of the film at 1080x1080 with the
SAME configs (hyperframes/square.py), and cut one moving sample. Nothing here is a finished square film.

  python3 sq_look.py --build B --out B/review/square [--sample 0 35] [--no-sample]

  OUT/hf/                  the square HyperFrames projects, stills and (inside the sample's range) renders
  OUT/stills/<id>.jpg      each graphic, settled, on its real frame (the talking head is the conform at 1.00x)
  OUT/stills/P_<key>.jpg   each picture kind once: a portrait photo, a square clip, a whole clip, a phone
  OUT/sample.mp4 (+ 540p)  the sample span moving, with the editor's audio and the captions at the square line
  OUT/items.json           what the page lists

Square geometry (square.py): lower third and 3A card at the bottom, captions at y 880, lifted above a side card,
paused under a lower third; a card under running captions ends above y 848.
"""
import argparse, json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, ".claude/skills/_shared/hyperframes"))
import square as SQM  # noqa: E402
import composite as CP  # noqa: E402
SQ = SQM.SQ
FF = CP.FF; FPS = CP.FPS
S = 1080
CAP_Y, LIFT_GAP, LIFT_MIN = 880, 150, 560
REAL = "Real picture of me - not AI-generated"; AI = "AI-GENERATED"


def run(c): subprocess.run(c, check=True)


def frame_at(path, n, wh):
    for f in CP.reader(path, start=n, n=1, wh=wh):
        return f
    raise SystemExit(f"no frame {n} in {path}")


def media_frame(spec, t, B):
    p = spec[1] if os.path.isabs(spec[1]) else os.path.join(B, spec[1])
    if spec[0] == "img":
        from PIL import ImageOps
        return ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    o = subprocess.run([FF, "-v", "error", "-ss", f"{spec[2] + t:.3f}", "-i", p, "-frames:v", "1", "-vf", "scale=in_color_matrix=bt709,format=rgb24",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    import io
    return Image.open(io.BytesIO(o)).convert("RGB")


def cover(im, w, h, ox=0.5, oy=0.5):
    k = max(w / im.width, h / im.height)
    r = im.resize((max(w, round(im.width * k)), max(h, round(im.height * k))), Image.LANCZOS)
    x = round((r.width - w) * ox); y = round((r.height - h) * oy)
    return r.crop((x, y, x + w, y + h))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--sample", nargs=2, type=float, default=[0.0, 35.0]); ap.add_argument("--no-sample", action="store_true")
    a = ap.parse_args()
    B = os.path.abspath(a.build); out = os.path.abspath(a.out)
    os.makedirs(os.path.join(out, "stills"), exist_ok=True)
    hf = os.path.join(out, "hf")
    sheet = json.load(open(os.path.join(B, "sbl_sheet.json")))
    J = json.load(open(os.path.join(B, "beats.json")))
    ft = json.load(open(os.path.join(B, "facetrack.json")))
    sys.path.insert(0, B)
    from assets import MEDIA
    base = os.path.join(B, "base.mp4")
    t0s, t1s = a.sample
    sqx = lambda g: int(min(1920 - S, max(0, np.interp(g, ft["n"], ft["x"]) + ft["crop_w"] / 2 - S / 2)))
    talk = lambda g: np.ascontiguousarray(frame_at(base, g, (1920, 1080))[:, sqx(g):sqx(g) + S])

    # the kit's own times for each graphic (a beat can move a few frames onto a cut)
    kt = {m["id"]: (m["a"], m["b"]) for m in json.load(open(os.path.join(B, "hf", "manifest.json")))}
    for b in J["beats"]:
        if b.get("kind") == "hf":
            kt[b["gid"]] = (b["t0"], b["t1"])
    man, items = [], []
    for g in sheet["graphics"]:
        ta, tb = kt.get(g["id"], (g["t0"], g["t1"]))
        g = dict(g, t0=ta, t1=tb, config=dict(g["config"], a=ta, b=tb))
        if g["template"] == "before-card" or g["template"].startswith("softblue:"):
            g["config"]["a"], g["config"]["b"] = CP.fr(ta) / FPS, CP.fr(tb) / FPS
        scenes, meta = SQ.scenes_for(g)
        dur = scenes[0][1]["dur"]
        ins = (not a.no_sample) and ta < t1s and tb > t0s
        SQ.build(scenes, hf, render=ins, snap=max(0.5, dur - 1.0))
        m = dict(id=g["id"], template=g["template"], a=ta, b=tb, mov=os.path.join(hf, "renders", g["id"] + ".mov"), **meta)
        if meta["kind"] == "glass": m["mask"] = os.path.join(hf, "renders", g["id"] + "_mask.mov")
        if ins: man.append(m)
        # the still: the settled graphic on its real frame
        st = Image.open(os.path.join(hf, "stills", g["id"] + ".png")).convert("RGBA")
        if meta["kind"] == "opaque":
            fr_ = st.convert("RGB")
        else:
            fr_ = Image.fromarray(talk(CP.fr(max(ta + 0.5, tb - 1.0))))
            if meta["kind"] == "glass":
                x0, y0, x1, y1 = meta["box"]
                reg = fr_.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(14))
                msk = Image.new("L", reg.size, 0)
                from PIL import ImageDraw
                ImageDraw.Draw(msk).rounded_rectangle([0, 0, reg.width - 1, reg.height - 1], 36, fill=255)
                fr_.paste(reg, (x0, y0), msk)
            fr_ = Image.alpha_composite(fr_.convert("RGBA"), st).convert("RGB")
        fr_.save(os.path.join(out, "stills", g["id"] + ".jpg"), quality=92)
        items.append(dict(id=g["id"], kind=g["template"], t0=ta, t1=tb, copy=g["text"], box=meta.get("box")))
        print(g["id"], g["template"], meta["kind"], flush=True)

    # one of each picture kind: portrait photo (real label), a square clip (AI label), a whole clip, a phone
    def card(key, label, caps, phone=False, gid=None, dur=3.0, render=False):
        spec = MEDIA[key]; o = spec[4] if len(spec) > 4 and isinstance(spec[4], dict) else {}
        im = media_frame(spec, 0.6, B)
        ar = o.get("ar") or im.width / im.height
        pid = gid or f"sqcard_{key}"
        scene, hole = SQM.media_card_scene(pid, dur, ar, label=label, kicker="AbsByAI.com" if phone else None, caps=caps)
        SQ.build([scene], hf, render=render, snap=1.0)
        return scene, hole, o

    def bleed_still(key, label):
        """A clip that fills the phone frame fills the square too (a 1:1 window of a 16:9 clip is a modest crop)."""
        from PIL import ImageDraw
        o = MEDIA[key][4] if len(MEDIA[key]) > 4 and isinstance(MEDIA[key][4], dict) else {}
        im = cover(media_frame(MEDIA[key], 0.6, B), S, S, o.get("ox", 0.5), o.get("oy", 0.5)).convert("RGBA")
        if label:
            f = SQM.B.font(46, False); w_ = round(f.getlength(label)) + 80
            ch = Image.new("RGBA", im.size); d = ImageDraw.Draw(ch)
            d.rounded_rectangle([40, 60, 40 + w_, 140], 24, fill=(4, 12, 26, 224)); d.text((80, 72), label, font=f, fill=(255, 255, 255, 255))
            im = Image.alpha_composite(im, ch)
        im.convert("RGB").save(os.path.join(out, "stills", f"P_{key}.jpg"), quality=92)
        return [0, 0, S, S]

    def card_still(key, label, caps, phone=False):
        scene, hole, o = card(key, label, caps, phone)
        plate = Image.open(os.path.join(hf, "stills", scene[1]["id"] + ".png")).convert("RGBA")
        bg = Image.new("RGB", (S, S)); x0, y0, x1, y1 = hole
        bg.paste(cover(media_frame(MEDIA[key], 2.0 if phone else 0.6, B), x1 - x0, y1 - y0, o.get("ox", 0.5), o.get("oy", 0.5)), (x0, y0))
        Image.alpha_composite(bg.convert("RGBA"), plate).convert("RGB").save(os.path.join(out, "stills", f"P_{key}.jpg"), quality=92)
        return hole

    seen = set()
    for b in sorted(J["beats"], key=lambda b: b["t0"]):
        if b.get("kind") not in ("card", "bleed") or b["media"] in seen:
            continue
        spec = MEDIA[b["media"]]; o = spec[4] if len(spec) > 4 and isinstance(spec[4], dict) else {}
        kind = "phone" if b.get("phone") else ("photo" if spec[0] == "img" else ("square clip" if o.get("ar") == 1.0 else ("full clip" if b["kind"] == "bleed" else "whole clip")))
        if kind in {i.get("pkind") for i in items}:
            continue
        seen.add(b["media"])
        lab = {"real": REAL, "ai": AI}.get(b.get("label_kind"))
        hole = bleed_still(b["media"], lab) if kind == "full clip" else card_still(b["media"], lab, b.get("caps") is not False, phone=bool(b.get("phone")))
        items.append(dict(id="P_" + b["media"], kind="picture", pkind=kind, t0=b["t0"], t1=b["t1"], copy=[x for x in [lab] if x], hole=hole))
        print("picture", kind, b["media"], hole, flush=True)

    json.dump(items, open(os.path.join(out, "items.json"), "w"), indent=1)
    if a.no_sample:
        return
    # ---- the moving sample
    g0, g1 = CP.fr(t0s), CP.fr(t1s)
    C = CP.Compositor(man, wh=(S, S))
    pics = []                                       # picture beats inside the sample: a card plate each
    for b in J["beats"]:
        if b.get("kind") in ("card", "bleed") and b["t0"] < t1s and b["t1"] > t0s:
            f0, f1 = CP.fr(b["t0"]), CP.fr(b["t1"])
            lab = {"real": REAL, "ai": AI}.get(b.get("label_kind"))
            scene, hole, o = card(b["media"], lab, b.get("caps") is not False, bool(b.get("phone")), gid=f"sqs_{b['media']}_{f0}",
                                  dur=(f1 - f0) / FPS, render=True)
            pics.append(dict(f0=f0, f1=f1, key=b["media"], hole=hole, o=o, mov=os.path.join(hf, "renders", scene[1]["id"] + ".mov")))
    cards = [(m["a"], m["b"], m["box"][1]) for m in man if m["kind"] == "overlay"]
    lts = [(m["a"], m["b"]) for m in man if m["kind"] == "glass"]
    caps = CP.reader(os.path.join(B, "captions.mov"), start=g0, n=g1 - g0, rgba=True, wh=(1080, 1920))
    basef = CP.reader(base, start=g0, n=g1 - g0, wh=(1920, 1080))
    raw = os.path.join(out, "_sample_pic.mp4")
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{S}x{S}", "-r", CP.FPSS, "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "17", "-preset", "medium",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", raw], stdin=subprocess.PIPE)
    readers = {}
    for g in range(g0, g1):
        t = g / FPS
        bf = next(basef); cf = next(caps)
        x = sqx(g)
        fr_ = np.ascontiguousarray(bf[:, x:x + S])
        pb = next((p for p in pics if p["f0"] <= g < p["f1"]), None)
        if pb:
            if pb["key"] not in readers or readers[pb["key"]][0] != pb["f0"]:
                readers[pb["key"]] = (pb["f0"], CP.reader(pb["mov"], start=g - pb["f0"], rgba=True, wh=(S, S)))
            plate = next(readers[pb["key"]][1])
            x0, y0, x1, y1 = pb["hole"]
            spec = MEDIA[pb["key"]]
            im = media_frame(spec, (g - pb["f0"]) / FPS if spec[0] == "vid" else 0, B)
            z = 1.0 + 0.05 * (g - pb["f0"]) / max(1, pb["f1"] - pb["f0"]) if spec[0] == "img" else 1.0     # a still never sits frozen
            w_, h_ = x1 - x0, y1 - y0
            c = cover(im, round(w_ * z), round(h_ * z), pb["o"].get("ox", 0.5), pb["o"].get("oy", 0.5))
            dx, dy = (c.width - w_) // 2, 0                                                               # the push holds the top (his hair)
            bg = np.zeros((S, S, 3), np.uint8); bg[y0:y1, x0:x1] = np.asarray(c.crop((dx, dy, dx + w_, dy + h_)))
            fr_ = CP.over(bg, plate)
        fr_ = C.apply(fr_, g)
        # captions: the vertical's own caption states, moved to the square line (lifted above a side card, off under a lower third)
        al = cf[..., 3]
        if al.max() > 8 and not any(a_ <= t < b_ for a_, b_ in lts) and not C.opaque(g) and not (pb and "sqs_" in pb["mov"] and False):
            rows = np.where(al.max(axis=1) > 8)[0]
            y0c, y1c = rows[0], rows[-1] + 1
            cy = next((top - LIFT_GAP for a_, b_, top in cards if a_ <= t < b_), CAP_Y)
            if cy >= LIFT_MIN:
                band = cf[y0c:y1c]
                yy = int(cy)
                if yy + band.shape[0] <= S:
                    reg = fr_[yy:yy + band.shape[0]].astype(np.float32); al_ = band[..., 3:4].astype(np.float32) / 255
                    fr_[yy:yy + band.shape[0]] = (reg * (1 - al_) + band[..., :3].astype(np.float32) * al_).astype(np.uint8)
        enc.stdin.write(fr_.tobytes())
    enc.stdin.close(); enc.wait()
    sm = os.path.join(out, "sample.mp4")
    run([FF, "-v", "error", "-y", "-i", raw, "-ss", f"{g0 / FPS:.5f}", "-t", f"{(g1 - g0) / FPS:.5f}", "-i", os.path.join(B, "his_mix.wav"),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", sm])
    run([FF, "-v", "error", "-y", "-i", sm, "-vf", "scale=540:-2", "-c:v", "libx264", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "copy",
         "-movflags", "+faststart", sm.replace(".mp4", " - REVIEW 540p.mp4")])
    run([FF, "-v", "error", "-y", "-ss", "5", "-i", sm, "-frames:v", "1", "-vf", "scale=540:-2", sm.replace(".mp4", ".jpg")])
    os.remove(raw)
    print("sample ok", sm)


if __name__ == "__main__":
    main()
