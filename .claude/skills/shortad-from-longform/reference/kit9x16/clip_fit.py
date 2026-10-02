#!/usr/bin/env python3
"""A HORIZONTAL CLIP IN A VERTICAL: fill the frame, else the centre square, else the whole clip (Dan, 2026-10-01,
VIDEO-RULES "A horizontal clip in a vertical").

  "I want to make it full screen, if that makes sense. If that cuts off too much, make it a center square. If the
   center square cuts off too much, show the whole clip. I want it to depend on whether there's something in the
   sides that's critical."      His worked examples: the AI man on the scale fills; the overhead salad is a square.

For one clip this builds the three candidate crops at three moments of the span that is used, shows them to a small
vision model (one ledgered call through ai_calls.py, a fraction of a cent) and asks, for the fill and for the square,
what is lost at the sides and whether it is critical. The verdict is the TIGHTEST crop that loses nothing critical.
Real-or-AI labels are never asked here: they stay facts from the sheet.

Why a model and not the person mask: the mask's extent read the salad table as 90 % wide and the man on the scale as
35 % (round 1), which says nothing about whether the sides matter, and on a hands-only clip its centre is the arm, not
the bowl. So two small calls per clip: WHERE is what must stay visible (the windows are centred on it), then the judged
crops.

  import clip_fit
  v = clip_fit.decide(path, src_in, dur, work_dir, ai, people="other", key="C02")
  -> dict(verdict="fill"|"square"|"whole", cx=0..1, fill=dict(ok, lost), square=dict(ok, lost), why, sheet=<jpg>, by)

  python3 clip_fit.py --build B --sheet SHEET.json          # every clip of a sheet: verdicts + the proof sheets
"""
import hashlib
import json
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
FF = os.path.join(MAIN, "Media/video_edit/bin/ffmpeg")
MODEL = "gemini-3.8-flash"
VERSION = "clip-fit-5"
TIMES = (0.12, 0.5, 0.88)
FW, FH = 640, 360                       # the working frame (16:9 sources are scaled to this height)

PROMPT = """You are helping re-frame a HORIZONTAL video clip for a VERTICAL phone video (9:16).
You get three images of the same clip at three moments (early, middle, late):
  IMAGE "whole":  the whole horizontal frame, the three moments stacked TOP TO BOTTOM. A yellow box marks what the FILL crop
                  keeps; a cyan box marks what the SQUARE crop keeps.
  IMAGE "fill":   the clip cropped to a full phone frame (9:16), the three moments left to right. The sides are cut off.
  IMAGE "square": the clip cropped to a square, the three moments left to right. Less of the sides is cut off.

The editor's rule, in his words: "I want to make it full screen, if that makes sense. If that cuts off too much, make it a
center square. If the center square cuts off too much, show the whole clip. I want it to depend on whether there's something
in the sides that's critical... unless there's something critical in the sides where the clip wouldn't make sense, where
there are body parts cut off."

His two worked examples:
  - A man standing on a bathroom scale, one centred person, nothing that matters at the sides: FILL is fine.
  - An overhead shot of a table of salad bowls and food that spreads across the frame: FILL does not make sense
    (it shows a sliver of the table), the SQUARE is fine.

FILL IS THE DEFAULT. He wants the clip full screen unless there is a STRONG reason not to. Judge each crop BY ITSELF, the
way a phone viewer who never saw the whole frame would see it: does the crop still show the main subject whole, and is it
still clear what is happening?

A crop is OK (the normal case) when what it removes is only: background, walls, furniture, empty table; OTHER items around
the subject (side dishes, extra food, props, a jar, a pitcher); a person who is not the subject; the rest of an arm, a
forearm, a shoulder or an elbow, as long as the hand doing the action and the thing it acts on are still in the crop; a
tighter framing of a person whose face and torso are still there. Losing context is fine. Being tighter is fine.

A crop is NOT OK only for a strong reason:
  - the ONE main object the clip is about (the bowl, the plate, the phone, the mug, the scale and what is on it) is wider
    than the crop, so the crop edge slices through it on a side and the viewer sees a piece of it instead of the object;
  - a face is cut by the crop edge;
  - the hand or the tool doing the action is outside the crop, or leaves it, at any of the three moments;
  - the scene is ABOUT several things or people spread across the frame (a table of dishes, a group at a meal, a pattern)
    and the crop shows a sliver that no longer reads as that scene.
Judge all three moments: the crop must work for the whole clip, not just one frame. Decide the SQUARE the same way.

Answer with JSON only:
{"subject": "what the clip shows, a few words",
 "fill": {"ok": true|false, "lost": "what the fill crop removes, a few words", "critical": "why that is or is not critical"},
 "square": {"ok": true|false, "lost": "...", "critical": "..."},
 "confidence": 0.0-1.0}"""


LOCATE = """Three moments (early, middle, late) of one horizontal video clip, stacked top to bottom.
Find the part of the frame that MUST stay visible for the clip to make sense: the main subject together with its action
(a person's face and torso; the hand or tool doing the action and the thing it acts on; the one object the clip is about).
Leave out background, empty table, other items around the subject, and the rest of an arm.
Give its left and right edges as fractions of the frame width, from 0 (left edge) to 1 (right edge), wide enough to hold it
at ALL three moments.
Answer with JSON only: {"subject": "a few words", "x0": 0.0-1.0, "x1": 0.0-1.0}"""


def locate(ai, whole_path, key):
    """(x0, x1) of what must stay visible, as fractions of the width; None with no usable answer."""
    for _ in range(3):
        a = ai._call(MODEL, [_img(whole_path), {"text": LOCATE}], purpose="clip_fit:" + key, max_tokens=2048, think=512)
        try:
            x0, x1 = float(a["x0"]), float(a["x1"])
            if 0 <= x0 < x1 <= 1:
                return x0, x1, a.get("subject")
        except (TypeError, KeyError, ValueError):
            pass
    return None


def probe(path):
    o = subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0:s=x", path], capture_output=True, text=True).stdout.strip().split("\n")[0]
    w, h = (int(x) for x in o.split("x")[:2])
    return w, h


def frames(path, src_in, dur, work, key):
    os.makedirs(work, exist_ok=True)
    out = []
    isimg = path.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    for k, f in enumerate(TIMES[:1] if isimg else TIMES):
        p = os.path.join(work, f"{key}_f{k}.jpg")
        if not os.path.exists(p):
            cmd = [FF, "-v", "error", "-y"] + ([] if isimg else ["-ss", f"{src_in + dur * f:.3f}"]) + \
                  ["-i", path, "-frames:v", "1", "-vf", f"scale=-2:{FH}", "-q:v", "2", p]
            subprocess.run(cmd)
        if os.path.exists(p):
            out.append(p)
    return out


def windows(w, h, cx):
    """(x0, x1) of the fill (9:16) and square windows in a w x h frame, centred on cx and kept inside the frame."""
    out = {}
    for name, ar in (("fill", 9 / 16), ("square", 1.0)):
        ww = min(w, h * ar)
        x0 = min(max(0.0, cx * w - ww / 2), w - ww)
        out[name] = (x0, x0 + ww)
    return out


def ox_of(w, h, cx, ar):
    """render.cover_chain's `ox` (0 = left, 1 = right) for a window of aspect `ar` centred on cx."""
    ww = min(w, h * ar)
    return 0.5 if w - ww < 1 else round(float(min(1.0, max(0.0, (cx * w - ww / 2) / (w - ww)))), 3)


def sheets(files, cx, work, key):
    """The three images the model sees, and one combined proof sheet for the review page."""
    ims = [Image.open(f).convert("RGB") for f in files]
    w, h = ims[0].size
    W = windows(w, h, cx)
    def row(fn, stack=False):
        tiles = [fn(im) for im in ims]
        if stack:                                              # top to bottom: an x fraction read off it is the frame's own
            out = Image.new("RGB", (tiles[0].size[0], sum(t.size[1] for t in tiles) + 8 * (len(tiles) - 1)), (20, 20, 20))
            y = 0
            for t in tiles:
                out.paste(t, (0, y)); y += t.size[1] + 8
            return out
        out = Image.new("RGB", (sum(t.size[0] for t in tiles) + 8 * (len(tiles) - 1), tiles[0].size[1]), (20, 20, 20))
        x = 0
        for t in tiles:
            out.paste(t, (x, 0)); x += t.size[0] + 8
        return out
    def whole(im):
        im = im.copy(); d = ImageDraw.Draw(im)
        d.rectangle([W["square"][0], 1, W["square"][1] - 1, h - 2], outline=(0, 220, 255), width=3)
        d.rectangle([W["fill"][0], 1, W["fill"][1] - 1, h - 2], outline=(255, 220, 0), width=3)
        return im
    paths = {}
    for name, fn in (("whole", whole), ("fill", lambda im: im.crop((round(W["fill"][0]), 0, round(W["fill"][1]), h))),
                     ("square", lambda im: im.crop((round(W["square"][0]), 0, round(W["square"][1]), h)))):
        p = os.path.join(work, f"{key}_{name}.jpg")
        row(fn, stack=(name == "whole")).save(p, quality=88)
        paths[name] = p
    # the proof sheet for the review page: the middle moment as WHOLE (with the two boxes) | SQUARE | FILL, one row
    mid = ims[len(ims) // 2]
    parts = [whole(mid), mid.crop((round(W["square"][0]), 0, round(W["square"][1]), h)), mid.crop((round(W["fill"][0]), 0, round(W["fill"][1]), h))]
    gap = 14
    proof = Image.new("RGB", (sum(p.size[0] for p in parts) + gap * 2, h), (12, 22, 36))
    x = 0
    for p in parts:
        proof.paste(p, (x, 0)); x += p.size[0] + gap
    pp = os.path.join(work, f"{key}_proof.jpg")
    proof.save(pp, quality=88)
    return paths, pp


def ask(ai, paths, key):
    parts = []
    for name in ("whole", "fill", "square"):
        parts += [{"text": f'IMAGE "{name}":'}, _img(paths[name])]
    parts.append({"text": PROMPT})
    return ai._call(MODEL, parts, purpose="clip_fit:" + key, max_tokens=4096, think=1024)


def _img(path):
    import ai_calls
    return ai_calls._img_part(path)


def decide(path, src_in, dur, work, ai, people="other", key=None, override=None):
    """One clip's verdict. Cached on the source, the span and this file's version."""
    key = key or re.sub(r"[^A-Za-z0-9]", "_", os.path.basename(path))[-40:]
    w, h = probe(path)
    sig = hashlib.sha1(json.dumps([path, round(src_in, 3), round(dur, 3), VERSION, MODEL, PROMPT]).encode()).hexdigest()[:16]
    cp = os.path.join(work, f"{key}.verdict.json")
    if os.path.exists(cp):
        c = json.load(open(cp))
        if c.get("sig") == sig and os.path.exists(c.get("sheet", "")):
            return c
    files = frames(path, src_in, dur, work, key)
    if not files:
        raise SystemExit(f"{key}: no frame could be read from {path}")
    cx, by, need, ans, tries = 0.5, "frame centre", None, None, []
    have_ai = getattr(ai, "name", "none") != "none"
    paths, proof = sheets(files, cx, work, key)
    if have_ai:
        # 1. where is what must stay visible (the person mask cannot say: on a hands-only clip it centres on the arm)
        loc = locate(ai, paths["whole"], key)
        if loc:
            need = [round(loc[0], 3), round(loc[1], 3)]
            cx, by = (loc[0] + loc[1]) / 2, "the centre of what must stay visible"
            paths, proof = sheets(files, cx, work, key)
        # 2. the three crops on that centre, judged
        for _ in range(3):
            ans = ask(ai, paths, key)
            if isinstance(ans, dict) and isinstance(ans.get("fill"), dict) and isinstance(ans.get("square"), dict):
                break
            ans = None
        if ans is not None:
            tries.append(dict(cx=round(cx, 3), need=need, answer=ans))
    if ans is None:
        v = dict(verdict="whole", why="no vision verdict (no provider, or no usable answer): the whole clip, the crop that cannot lose anything",
                 fill=None, square=None, subject=None, confidence=None)
    else:
        verdict = "fill" if ans["fill"].get("ok") else "square" if ans["square"].get("ok") else "whole"
        lost = ans[verdict]["lost"] if verdict != "whole" else None
        why = {"fill": f"fills the frame: it only loses {lost}",
               "square": f"centre square: filling the frame would lose {ans['fill'].get('lost')} ({ans['fill'].get('critical')}); the square only loses {lost}",
               "whole": f"whole clip: the square would still lose {ans['square'].get('lost')} ({ans['square'].get('critical')})"}[verdict]
        v = dict(verdict=verdict, why=why, fill=ans["fill"], square=ans["square"], subject=ans.get("subject"), confidence=ans.get("confidence"))
    v.update(sig=sig, key=key, size=[w, h], cx=round(cx, 3), centred_by=by, must_stay=need, sheet=proof, model=MODEL if ans else None, tries=tries,
             ox=dict(fill=ox_of(w, h, cx, 9 / 16), square=ox_of(w, h, cx, 1.0)))
    if override:
        v.update(model_verdict=v["verdict"], verdict=override["verdict"], why=override["why"], overridden_by=override.get("by", "the editor"))
    json.dump(v, open(cp, "w"), indent=1)
    return v


def main():
    import argparse
    import ai_calls
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True); ap.add_argument("--sheet", required=True); ap.add_argument("--ai", default="gemini")
    a = ap.parse_args()
    B = os.path.abspath(a.build)
    ai = ai_calls.provider(a.ai, os.path.join(B, "ai_ledger.jsonl"))
    S = json.load(open(a.sheet))
    FPS = 30000 / 1001
    for p in S["pictures"]:
        if p.get("in_graphic") or p["kind"] == "phone":
            continue
        f0, f1 = round(p["t0"] * FPS), round(p["t1"] * FPS)
        for k, src in enumerate(p["sources"]):
            key = p["id"] if len(p["sources"]) == 1 else f"{p['id']}_{k + 1}"
            n = src.get("frames") or (f1 - f0)
            v = decide(src["path"], float(src.get("src_in", 0.0)), n / FPS, os.path.join(B, "_clipfit"), ai, people=p["people"], key=key)
            print(f"{key:7s} {v['verdict']:6s} cx {v['cx']:.2f} ({v['centred_by']})  {v['why']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    sys.exit(main())
