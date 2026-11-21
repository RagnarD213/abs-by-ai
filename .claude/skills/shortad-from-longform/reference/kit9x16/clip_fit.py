#!/usr/bin/env python3
"""A HORIZONTAL CLIP IN A VERTICAL OR A SQUARE: the NARROWEST side crop that keeps what the clip is about (Dan,
2026-10-02, VIDEO-RULES "Verticals and squares: fill as much of the screen as the clip allows").

  "unless we have to preserve the content on the left and right sides and we can't crop, we want to fill as much of
   the screen area as possible and avoid having a lot of blank space."   "crop out the space on the left and a little
   bit on the right"; "nearly vertical"; "we need the stuff on the sides there" (the overhead salad table).

Full screen, a square and the whole clip are points on one line. For one clip, at three moments of the span used:
  1. LOCATE  a small vision call reads the left and right edges of what must stay visible, off the three frames
             stacked top to bottom under a ruler (no crop boxes drawn: round 2's boxes pulled 8 of 18 answers onto
             the square's own edges);
  2. the window is those edges plus a 2 % margin, never narrower than full screen (9:16); a window within 10 % of
     full screen IS full screen, one within 6 % of the whole clip is the whole clip; a span wider than a square is
     tried as the square on its centre first;
  3. JUDGE   a second call sees that crop and says whether it cuts something the clip needs, and on which side; a
             rejected crop widens 8 % on that side and is judged again (three tries, then the whole clip).
Height is never cropped. Real-or-AI is never asked here. Blank space carries its reason in sheet_report.json.

  import clip_fit
  v = clip_fit.decide(path, src_in, dur, work_dir, ai, key="C02", override=None)
  -> dict(verdict="fill"|"crop"|"whole", window=[x0, x1], ar, ox, pan=None|[x0, x1], why, sheet=<proof jpg>, ...)

override (Dan's own note on a clip, <build>/clip_overrides.json) wins over the model:
  {"x0": 0.33, "x1": 0.80, "dan": "<his words>"}              a window, as fractions of the width
  {"x0": .., "x1": .., "pan_to": [x0, x1], "dan": ..}         the window travels to pan_to over the clip (the subject moves)
  {"verdict": "fill"|"whole", "cx": 0.5, "dan": ..}           full screen centred on cx, or the whole clip

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
VERSION = "clip-fit-6"
TIMES = (0.12, 0.5, 0.88)
FW, FH = 640, 360                       # the working frame (16:9 sources are scaled to this height)
MARGIN = 0.02                           # air kept each side of what must stay, as a fraction of the width
FILL_SNAP = 1.10                        # a window within 10 % of full screen becomes full screen
WHOLE_SNAP = 0.94                       # a window this much of the clip's width is the whole clip
WIDEN = 0.08                            # one step wider on the side the judge says is cut

LOCATE = """Three moments (early, middle, late) of one horizontal video clip, stacked top to bottom. Above each one is a
ruler: 0.0 is the left edge of the frame, 1.0 the right edge, a tick every 0.1.

The clip will be cropped at the SIDES to fill a tall phone screen, so the editor wants the NARROWEST crop that still
shows what the clip is about. His words: "crop out the unnecessary space on the left and right", "fill as much of the
screen as possible", and blank space only when "we have to preserve the content on the left and right sides".

Find what MUST stay visible:
  - a person who is the subject: the face and the torso, plus the hand doing the action and the thing it acts on;
  - a hands-only or object clip: the ONE main object (the bowl, plate, mug, glass, phone, syringe) WHOLE, edge to edge,
    plus the hand or tool acting on it where they meet. The rest of the arm, the sleeve and the wrist are NOT needed;
  - a scene that is ABOUT many things spread across the frame (a laid table seen from above, a group at a meal, a
    scatter of sweets or pills): the spread itself is the subject, so give the full extent of it.
Leave out background, walls, empty table or counter, and other items standing around the subject.
The subject may MOVE between the three moments: give edges wide enough to hold it at ALL three.
Read the edges off the rulers. Be tight: do not add air.

Answer with JSON only: {"subject": "a few words", "x0": 0.0-1.0, "x1": 0.0-1.0, "spread": true|false}"""

JUDGE = """You are checking ONE side crop of a horizontal video clip that will play in a vertical phone video.
  IMAGE "whole": the whole frame at three moments (early, middle, late), stacked top to bottom; the yellow box is the crop.
  IMAGE "crop":  what the viewer will see, the same three moments left to right.

The editor wants the clip cropped as narrow as it will go ("fill as much of the screen as possible"), so a tight crop is
GOOD. Judge the crop by itself, the way a phone viewer who never saw the whole frame would see it.

The crop is OK when what it removes is only background, walls, empty table, other items around the subject, a person who
is not the subject, or the rest of an arm (as long as the hand doing the action and the thing it acts on are in the crop).
The crop is NOT OK only when, at ANY of the three moments:
  - the one main object the clip is about is sliced by a crop edge, so the viewer sees a piece of it;
  - a face is cut by a crop edge;
  - the hand or tool doing the action is outside the crop;
  - the scene is about things spread across the frame and the crop shows a sliver that no longer reads as that scene.

Answer with JSON only:
{"ok": true|false, "cut": "none"|"left"|"right"|"both", "lost": "what the crop removes, a few words",
 "critical": "why that is or is not critical", "confidence": 0.0-1.0}"""


def _json_call(ai, parts, key, max_tokens, think, good):
    for _ in range(3):
        a = ai._call(MODEL, parts, purpose="clip_fit:" + key, max_tokens=max_tokens, think=think)
        try:
            if good(a):
                return a
        except (TypeError, KeyError, ValueError):
            pass
    return None


def locate(ai, ruled_path, key):
    """dict(x0, x1, subject, spread) of what must stay visible, as fractions of the width; None with no usable answer."""
    def norm(a):
        # the model sometimes answers in percent (26, 59) or thousandths (290, 591) instead of 0..1 (RO-10 C14)
        x0, x1 = float(a["x0"]), float(a["x1"])
        k = 1 if x1 <= 1 else 100 if x1 <= 100 else 1000
        return x0 / k, x1 / k
    a = _json_call(ai, [_img(ruled_path), {"text": LOCATE}], key, 2048, 512, lambda a: 0 <= norm(a)[0] < norm(a)[1] <= 1)
    return a and dict(x0=norm(a)[0], x1=norm(a)[1], subject=a.get("subject"), spread=bool(a.get("spread")))


def judge(ai, whole_path, crop_path, key):
    parts = [{"text": 'IMAGE "whole":'}, _img(whole_path), {"text": 'IMAGE "crop":'}, _img(crop_path), {"text": JUDGE}]
    return _json_call(ai, parts, key, 4096, 1024, lambda a: isinstance(a["ok"], bool))


def fit_window(x0, x1, w, h, margin=MARGIN):
    """The crop for a must-stay span: (x0, x1, verdict). Never narrower than full screen (9:16), snapped to full screen
    within FILL_SNAP of it and to the whole clip above WHOLE_SNAP, centred on the span and kept inside the frame."""
    minw = min(1.0, (9 / 16) / (w / h))
    ww = max(minw, (x1 - x0) + 2 * margin)
    verdict = "crop"
    if ww <= minw * FILL_SNAP:
        ww, verdict = minw, "fill"
    if ww >= WHOLE_SNAP:
        return 0.0, 1.0, "whole"
    a = min(max(0.0, (x0 + x1) / 2 - ww / 2), 1.0 - ww)
    return round(a, 4), round(a + ww, 4), verdict


def shape(x0, x1, w, h):
    """(ar, ox) of a window: the card's shape and render.cover_chain's `ox` (0 = left, 1 = right)."""
    ww = x1 - x0
    return round(ww * w / h, 4), (0.5 if ww > 0.999 else round(float(min(1.0, max(0.0, x0 / (1 - ww)))), 3))


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


def _row(tiles, stack=False, gap=8):
    if stack:                                                  # top to bottom: an x read off it is the frame's own
        out = Image.new("RGB", (tiles[0].size[0], sum(t.size[1] for t in tiles) + gap * (len(tiles) - 1)), (20, 20, 20))
        y = 0
        for t in tiles:
            out.paste(t, (0, y)); y += t.size[1] + gap
        return out
    out = Image.new("RGB", (sum(t.size[0] for t in tiles) + gap * (len(tiles) - 1), tiles[0].size[1]), (20, 20, 20))
    x = 0
    for t in tiles:
        out.paste(t, (x, 0)); x += t.size[0] + gap
    return out


def ruled(files, work, key):
    """The three moments stacked, each under a 0..1 ruler, with NO crop drawn (the LOCATE image)."""
    tiles = []
    for f in files:
        im = Image.open(f).convert("RGB"); w, h = im.size
        t = Image.new("RGB", (w, h + 22), (0, 0, 0)); t.paste(im, (0, 22)); d = ImageDraw.Draw(t)
        for i in range(21):
            x = min(w - 1, round(i * w / 20))
            d.line([x, 12 if i % 2 else 4, x, 21], fill=(255, 255, 0), width=2 if i % 2 == 0 else 1)
            if i % 2 == 0:
                s = f"{i / 20:.1f}"
                d.text((min(w - 20, max(0, x + 3 if i < 20 else x - 20)), 0), s, fill=(255, 255, 255))
        tiles.append(t)
    p = os.path.join(work, f"{key}_ruled.jpg")
    _row(tiles, stack=True).save(p, quality=88)
    return p


def sheets(files, win, work, key, tag="", pan=None):
    """For a window (x0, x1 as fractions): the boxed whole frames (stacked), the crop at the three moments, and the
    one-row proof for the review page (whole with the box | the crop, middle moment). With a pan the window travels."""
    ims = [Image.open(f).convert("RGB") for f in files]
    w, h = ims[0].size
    def at(k):
        if not pan or len(ims) < 2:
            return win
        f = k / (len(ims) - 1)
        return [win[0] + (pan[0] - win[0]) * f, win[1] + (pan[1] - win[1]) * f]
    def boxed(im, k):
        im = im.copy(); a, b = at(k)
        ImageDraw.Draw(im).rectangle([round(a * w), 1, round(b * w) - 1, h - 2], outline=(255, 220, 0), width=3)
        return im
    crop = lambda im, k: im.crop((round(at(k)[0] * w), 0, round(at(k)[1] * w), h))
    whole_p, crop_p = os.path.join(work, f"{key}{tag}_whole.jpg"), os.path.join(work, f"{key}{tag}_crop.jpg")
    _row([boxed(im, k) for k, im in enumerate(ims)], stack=True).save(whole_p, quality=88)
    _row([crop(im, k) for k, im in enumerate(ims)]).save(crop_p, quality=88)
    m = len(ims) // 2
    parts = [boxed(ims[m], m), crop(ims[m], m)]
    proof = Image.new("RGB", (sum(p.size[0] for p in parts) + 14, h), (12, 22, 36))
    x = 0
    for p in parts:
        proof.paste(p, (x, 0)); x += p.size[0] + 14
    pp = os.path.join(work, f"{key}{tag}_proof.jpg")
    proof.save(pp, quality=88)
    return whole_p, crop_p, pp


def _img(path):
    import ai_calls
    return ai_calls._img_part(path)


def model_fit(path, src_in, dur, work, ai, key, w, h, files):
    """The model's own answer (cached on the source, the span, the prompts and this file's version)."""
    sig = hashlib.sha1(json.dumps([path, round(src_in, 3), round(dur, 3), VERSION, MODEL, LOCATE, JUDGE]).encode()).hexdigest()[:16]
    cp = os.path.join(work, f"{key}.fit6.json")
    if os.path.exists(cp):
        c = json.load(open(cp))
        if c.get("sig") == sig and os.path.exists(c.get("sheet", "")):
            return c
    v = dict(sig=sig, verdict="whole", window=[0.0, 1.0], must_stay=None, subject=None, spread=None, tries=[], model=None, confidence=None,
             why="no vision verdict (no provider, or no usable answer): the whole clip, the crop that cannot lose anything")
    if getattr(ai, "name", "none") != "none":
        loc = locate(ai, ruled(files, work, key), key)
        if loc:
            x0, x1, verdict = fit_window(loc["x0"], loc["x1"], w, h)
            if x1 - x0 > h / w:
                # wider than a square: the square on its centre is tried FIRST (bias toward tighter: on RO-10 the
                # located span alone left C04, C08, C13 and C15 wider than the crops Dan had already approved);
                # the judge widens it only if the square cuts something the clip needs
                c = (loc["x0"] + loc["x1"]) / 2
                x0 = round(min(max(0.0, c - h / w / 2), 1.0 - h / w), 4); x1, verdict = round(x0 + h / w, 4), "crop"
            v.update(must_stay=[round(loc["x0"], 3), round(loc["x1"], 3)], subject=loc["subject"], spread=loc["spread"], model=MODEL)
            for n in range(4):
                if verdict == "whole":
                    v.update(verdict="whole", window=[0.0, 1.0],
                             why="whole clip: " + (v["tries"][-1]["answer"].get("critical") if v["tries"] else "what must stay visible spans the frame"))
                    break
                wp, cp_, _ = sheets(files, [x0, x1], work, key, tag=f"_t{n}")
                ans = judge(ai, wp, cp_, key)
                if ans is None:
                    v.update(why="no usable judge answer: the whole clip"); break
                v["tries"].append(dict(window=[x0, x1], answer=ans))
                if ans["ok"]:
                    kept = f"keeps {loc['subject']}; only loses {ans.get('lost')}"
                    v.update(verdict=verdict, window=[x0, x1], confidence=ans.get("confidence"),
                             why=("fills the frame: " if verdict == "fill" else f"side crop {x0:.2f} to {x1:.2f} of the width: ") + kept)
                    break
                if n == 3:
                    v.update(why="whole clip: three wider crops were each rejected (" + str(ans.get("critical")) + ")"); break
                side = ans.get("cut") if ans.get("cut") in ("left", "right") else "both"
                a_ = x0 - (WIDEN if side in ("left", "both") else 0); b_ = x1 + (WIDEN if side in ("right", "both") else 0)
                x0, x1, verdict = fit_window(max(0.0, a_), min(1.0, b_), w, h, margin=0.0)
    _, _, v["sheet"] = sheets(files, v["window"], work, key)
    json.dump(v, open(cp, "w"), indent=1)
    return v


def decide(path, src_in, dur, work, ai, people="other", key=None, override=None):
    """One clip's crop. The model's answer is cached; an override (Dan's note) is applied on top and never cached."""
    key = key or re.sub(r"[^A-Za-z0-9]", "_", os.path.basename(path))[-40:]
    w, h = probe(path)
    files = frames(path, src_in, dur, work, key)
    if not files:
        raise SystemExit(f"{key}: no frame could be read from {path}")
    v = dict(model_fit(path, src_in, dur, work, ai, key, w, h, files))
    v.update(key=key, size=[w, h], pan=None)
    if override:
        minw = min(1.0, (9 / 16) / (w / h))
        v.update(model_verdict=v["verdict"], model_window=v["window"], model_why=v["why"], overridden_by=override.get("by", "the editor"),
                 why=override["why"])
        if "x0" in override:
            x0, x1 = float(override["x0"]), float(override["x1"])
            assert 0 <= x0 < x1 <= 1 and x1 - x0 >= minw - 0.005, f"{key}: an override window must lie in the frame and be no narrower than full screen ({minw:.3f})"
            v.update(verdict="fill" if x1 - x0 <= minw * 1.01 else "whole" if x1 - x0 > 0.999 else "crop", window=[x0, x1])
            if override.get("pan_to"):
                p0, p1 = (float(x) for x in override["pan_to"])
                assert abs((p1 - p0) - (x1 - x0)) < 0.005 and 0 <= p0 < p1 <= 1, f"{key}: pan_to must be the same width, inside the frame"
                assert v["verdict"] == "crop", f"{key}: a travelling window is a card (render_sbl.py); a full-screen fill does not pan"
                v["pan"] = [p0, p1]
        elif override["verdict"] == "fill":
            cx = float(override.get("cx", sum(v["must_stay"] or [0.0, 1.0]) / 2))
            a_ = min(max(0.0, cx - minw / 2), 1.0 - minw)
            v.update(verdict="fill", window=[round(a_, 4), round(a_ + minw, 4)])
        elif override["verdict"] == "whole":
            v.update(verdict="whole", window=[0.0, 1.0])
        else:
            raise SystemExit(f"{key}: override verdict {override['verdict']!r} (use fill, whole, or a window x0/x1)")
        _, _, v["sheet"] = sheets(files, v["window"], work, key, tag="_ov", pan=v["pan"])
    v["ar"], v["ox"] = shape(v["window"][0], v["window"][1], w, h)
    if v["pan"]:
        v["ox1"] = shape(v["pan"][0], v["pan"][1], w, h)[1]
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
            print(f"{key:7s} {v['verdict']:6s} {v['window'][0]:.2f}-{v['window'][1]:.2f} ar {v['ar']:.2f}  {v['why']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    sys.exit(main())
