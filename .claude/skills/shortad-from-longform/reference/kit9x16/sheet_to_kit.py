#!/usr/bin/env python3
"""THE SECOND WAY IN: an edit sheet (a 16:9 Claude or Codex made, `_shared/edit-sheet/`) -> the kit's inputs.

  python3 sheet_to_kit.py --sheet SHEET.json --build B

Replaces `recover`, `measure` and `content` (which reverse-engineer an editor's master). Nothing here is measured from
the finished video and nothing is guessed: every value is copied from the sheet, and the one thing the sheet cannot
know (how does a horizontal clip sit in a phone frame) is decided per clip by Dan's three-step rule, fill the frame,
else the centre square, else the whole clip (`clip_fit.py`: the three crops are looked at, each verdict and its reason
is recorded in sheet_report.json, and `<build>/clip_overrides.json` {key: {"verdict", "dan"}} holds his own flips).
Writes into B:

  rolls.json          the raw rolls
  edl_final.json      the cut: one row per take change (same-take `reframe` joins are merged: no cut in the vertical)
  piccuts.json        every picture cut sits ON its audio cut (the sheet's exact frames; no pose search)
  grade.py            the sheet's grade on a HAIR-ANCHORED 16:9 window of the raw (framing standard, 2026-09-08): the
                      window's top is the lowest hair top of the film minus 4 % of its height, so the kit's full-height
                      608 px talk crop is the FAR level and its 1.2x punch is NEAR
  m.whisper.json / ref.whisper.json   the sheet's words (caption fixes applied) in the shape the kit reads
  content.json        beats: every picture as a `card` or a `bleed` (label_kind from the sheet, NEVER a library match
                      or a model), every full-screen graphic as an `hf` beat; lower thirds; side cards; CTAs
  assets.py           the media map
  sheet_report.json   what was decided here and why (fill / square / whole per clip, the base window, anything dropped: nothing)

Graphics are NOT drawn here: `sbl_graphics.py` renders them at 9:16 from the sheet's configs after `build_kit.py` has
fixed the beat times.
"""
import argparse
import json
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
MAIN = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
SHARED = os.path.join(REPO, ".claude/skills/_shared")
FF = os.path.join(MAIN, "Media/video_edit/bin/ffmpeg")
sys.path.insert(0, os.path.join(SHARED, "edit-sheet"))
sys.path.insert(0, HERE)
import validate  # noqa: E402
import ai_calls  # noqa: E402
import clip_fit  # noqa: E402

FPS = 30000 / 1001
OPAQUE = {"before-card", "softblue:title_card", "softblue:recap", "title-card"}
SIDE = {"side-list", "cycle"}


def probe(path):
    d = json.loads(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height,duration:format=duration", "-of", "json", path], capture_output=True, text=True).stdout)
    s = d["streams"][0]
    return int(s["width"]), int(s["height"]), float(s.get("duration") or d["format"].get("duration") or 0)


def apply_fixes(words, fixes):
    """The sheet's caption fixes are regexes on the running text (the 16:9's SRT pass). A fix whose replacement has
    the same number of words is applied to the timed words; any other is reported, never silently skipped."""
    skipped = []
    for pat, rep in fixes or []:
        if isinstance(pat, list):
            pat, rep = pat
        txt = " ".join(w["w"] for w in words)
        for m in list(re.finditer(pat, txt))[::-1]:
            i0 = len(txt[:m.start()].split())
            old = m.group(0).split(); new = m.expand(rep).split()
            if len(old) != len(new):
                skipped.append([pat, rep]); continue
            for k, s in enumerate(new):
                words[i0 + k]["w"] = s
    return skipped


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--build", required=True)
    ap.add_argument("--ai", default="gemini", help="the vision provider for the clip rule (clip_fit.py); 'none' = every clip whole")
    ap.add_argument("--ledger", help="AI ledger (default <build>/ai_ledger.jsonl)")
    ap.add_argument("--flash", action="store_true", help="carry Muhammad's white flash on card returns (default: hard cuts, like our 16:9s)")
    a = ap.parse_args()
    S = json.load(open(a.sheet))
    E = validate.check(S, do_hash=False)
    if E:
        raise SystemExit("the edit sheet is incomplete (fix the 16:9 side, never the sheet by hand):\n  - " + "\n  - ".join(E[:40]))
    B = os.path.abspath(a.build)
    os.makedirs(B, exist_ok=True)
    V = S["video"]
    report = dict(sheet=os.path.abspath(a.sheet), job=S["job"], decisions=[], pictures=[], stops=[])
    AI = ai_calls.provider(a.ai, a.ledger or os.path.join(B, "ai_ledger.jsonl"))
    op = os.path.join(B, "clip_overrides.json")
    OVER = json.load(open(op)) if os.path.exists(op) else {}
    if len(V["rolls"]) != 1:
        raise SystemExit(f"{len(V['rolls'])} rolls in the sheet: the kit's one-grade base handles a single roll today")
    roll, R = next(iter(V["rolls"].items()))
    json.dump({roll: R["path"]}, open(os.path.join(B, "rolls.json"), "w"), indent=1)

    # ---- the cut: merge same-take reframes; every picture cut ON its audio cut
    rows = []
    for s in S["edl"]:
        if rows and s["join"] == "reframe" and s["roll"] == rows[-1]["roll"]:
            rows[-1]["f1"] = s["out_f1"]
            continue
        rows.append(dict(roll=s["roll"], f0=s["out_f0"], f1=s["out_f1"], src_f0=s.get("src_f0", round(s["src_in"] * FPS))))
    edl = [dict(i=i, cut_in=round(r["f0"] / FPS, 6), cut_out=round(r["f1"] / FPS, 6), dur=round((r["f1"] - r["f0"]) / FPS, 6),
                src_in=round(r["src_f0"] / FPS, 6), src_out=round((r["src_f0"] + r["f1"] - r["f0"]) / FPS, 6), roll=None,
                from_sheet=True) for i, r in enumerate(rows)]
    json.dump(edl, open(os.path.join(B, "edl_final.json"), "w"), indent=1)
    pc = [dict(i=e["i"], cut=round(e["cut_in"], 3), n0=round(e["cut_in"] * FPS), k=0, pic_frame=round(e["cut_in"] * FPS), conf=1.0,
               method="sheet", cover=None, sim_at_k=1.0, sim_at_0=1.0) for e in edl[1:]]
    json.dump(pc, open(os.path.join(B, "piccuts.json"), "w"), indent=1)
    report["decisions"].append(f"{len(S['edl'])} sheet segments -> {len(edl)} takes ({len(S['edl']) - len(edl)} same-take reframes merged); "
                               f"{len(pc)} picture cuts, all on their audio cut")

    # ---- the hair-anchored base window and the grade
    hair = min(f["head"]["hair_top"] for f in S["framing"])
    cxm = float(np.median([f["head"]["cx"] for f in S["framing"]]))
    hc = min(R["height"], (R["height"] - hair) / 0.96)
    y0 = max(0.0, hair - 0.04 * hc)
    hc = R["height"] - y0
    wc = hc * 16 / 9
    if wc > R["width"]:
        wc = R["width"]; hc = wc * 9 / 16
    x0 = min(max(0.0, cxm - wc / 2), R["width"] - wc)
    cw, ch, cx, cy = (int(round(v / 2)) * 2 for v in (wc, hc, x0, y0))
    sub_cx = round((cxm - cx) / cw * 1920)
    grade = S["grade"]["filter"]
    if S["grade"]["order"] == "after_scale_1080":
        # the 16:9 graded the 1080p picture (crop, scale, then the LUT): the same order here, which is also 3.5x faster
        assert grade.startswith("scale="), "an after_scale_1080 grade starts with its decode scale"
        grade = "scale=1920:1080:" + grade[len("scale="):]
    open(os.path.join(B, "grade.py"), "w").write(
        f'"""The 16:9\'s own grade (edit sheet {S["job"]}), on a hair-anchored 16:9 window of the raw: {cw}x{ch} at {cx},{cy}.\n'
        f'Lowest hair top of the film {hair:.0f} px; the window\'s top is 4 % of its height above it (framing standard)."""\n\n'
        f"CURVES = (\n    {('crop=%d:%d:%d:%d,' % (cw, ch, cx, cy))!r}\n    {grade!r}\n"
        f"    ',scale=1920:1080:out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p'\n)\n\n"
        f"# no vignette: the look is the sheet's grade (the kit's vignette belongs to Muhammad's masters)\nVIGNETTE = [(0.0, 1.0), (2.0, 1.0)]\n\n"
        f"SUBJECT_CX = {sub_cx}\nBASE_WINDOW = {[cw, ch, cx, cy]!r}\n")
    report["base_window"] = dict(crop=[cw, ch, cx, cy], hair_top_min=hair, head_cx_median=cxm,
                                 far_crop_raw=[round(608 / 1920 * cw), ch], headroom_px_at_1080=round((hair - cy) / ch * 1080, 1))

    # ---- words
    words = []
    for w in S["words"]["list"]:
        # the roll transcript splits a hyphenated word ("low", "-carb"): one caption word, as it is written
        if words and w["w"].startswith("-") and len(w["w"]) > 1:
            words[-1]["w"] += w["w"]; words[-1]["t1"] = w["t1"]
        else:
            words.append(dict(w))
    skipped = apply_fixes(words, S["words"].get("fixes"))
    if skipped:
        report["stops"].append(dict(what="caption fixes that change the word count were not applied to the timed words", fixes=skipped))
    segs, cur = [], []
    for w in words:
        cur.append(dict(word=" " + w["w"], start=w["t0"], end=w["t1"], probability=1.0))
        if w["w"].rstrip().endswith((".", "?", "!")):
            segs.append(cur); cur = []
    if cur:
        segs.append(cur)
    wj = dict(text=" ".join(w["w"] for w in words), language="en",
              segments=[dict(id=i, start=s[0]["start"], end=s[-1]["end"], text="".join(x["word"] for x in s), words=s) for i, s in enumerate(segs)])
    for f in ("m.whisper.json", "ref.whisper.json"):
        json.dump(wj, open(os.path.join(B, f), "w"))

    # ---- pictures -> media map + beats
    media, beats = {}, []
    for p in S["pictures"]:
        if p.get("in_graphic"):
            continue                                              # the photo inside a fact card: the graphic carries it and its chip
        f0, f1 = round(p["t0"] * FPS), round(p["t1"] * FPS)
        at = f0
        for k, src in enumerate(p["sources"]):
            key = p["id"] if len(p["sources"]) == 1 else f"{p['id']}_{k + 1}"
            n = src.get("frames") or (f1 - f0)
            w, h, _ = probe(src["path"])
            ar = w / h
            isimg = src["path"].lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
            mode, why, opts, fit = "card", "", {}, None
            if p["kind"] == "phone":
                why = "a phone screen stays whole in a card"
            elif ar < 0.8:
                mode, why = "bleed", "a portrait source fills the frame"
            elif p.get("vertical", {}).get("mode") in ("bleed", "card"):
                mode, why = p["vertical"]["mode"], "the sheet says so"
                opts = {"ox": p["vertical"].get("ox", 0.5)} if mode == "bleed" else {}
            else:
                # THE THREE-STEP RULE (Dan, 2026-10-01): fill the frame; if that cuts something critical at the sides,
                # the centre square; if the square still does, the whole clip
                ov = OVER.get(key)
                fit = clip_fit.decide(src["path"], float(src.get("src_in", 0.0)), n / FPS, os.path.join(B, "_clipfit"), AI,
                                      people=p["people"], key=key,
                                      override=dict(verdict=ov["verdict"], why="Dan: " + ov["dan"], by="Dan") if ov else None)
                why = fit["why"]
                if fit["verdict"] == "fill":
                    mode, opts = "bleed", {"ox": fit["ox"]["fill"]}
                elif fit["verdict"] == "square":
                    opts = {"ar": 1.0, "ox": fit["ox"]["square"]}
            media[key] = ("img", src["path"], 0, 1.0, dict(opts, oy=0.0)) if isimg else \
                ("vid", src["path"], float(src.get("src_in", 0.0))) + ((1.0, opts) if opts else ())
            b = dict(t0=round(at / FPS, 4), t1=round((at + n) / FPS, 4), kind=mode, media=key, pid=p["id"],
                     label_kind=p["label_kind"] if p["label_kind"] != "none" else None, flash_after=False, his_flash=False)
            if p["label_kind"] != "none":
                b["sheet_label"] = p["label"]
            if p["kind"] == "phone":
                b.update(caps=False, phone=True)
            if p["people"] == "dan" and p["label_kind"] != "none":
                b["caps"] = False                                 # a labelled picture of Dan drops the captions (kit rule)
            beats.append({k_: v for k_, v in b.items() if v is not None})
            report["pictures"].append(dict(id=key, mode=mode, why=why, source=os.path.basename(src["path"]), size=[w, h],
                                           label=p.get("label"), people=p["people"],
                                           shape=("phone" if p["kind"] == "phone" else fit["verdict"] if fit else mode),
                                           fit=({k_: fit.get(k_) for k_ in ("verdict", "model_verdict", "overridden_by", "fill", "square", "subject",
                                                                            "must_stay", "cx", "centred_by", "sheet", "confidence", "model")} if fit else None)))
            at += n
    lts, insets, ctas = [], [], []
    for g in S["graphics"]:
        t = g["template"]
        if t in OPAQUE:
            beats.append(dict(t0=g["t0"], t1=g["t1"], kind="hf", gid=g["id"], caps=False, flash_after=False, his_flash=False))
        elif t == "lower-third":
            lts.append(dict(t0=g["t0"], t1=g["t1"], lines=[g["text"][0], " ".join(g["text"][1:])], gid=g["id"]))
        elif t in SIDE:
            insets.append(dict(kind="hfov", t0=g["t0"], t1=g["t1"], gid=g["id"]))
        elif t == "cta":
            ctas.append(dict(t0=g["t0"], t1=g["t1"], top=g["config"]["top"], big=g["config"]["big"], gid=g["id"]))
        else:
            raise SystemExit(f"graphic {g['id']}: template {t!r} has no 9:16 Soft Blue Light layout yet (hyperframes/vertical.py). "
                             f"A graphic is never dropped: add the layout, or re-author it in the 16:9.")
    beats.sort(key=lambda b: b["t0"])
    for x, y in zip(beats, beats[1:]):
        if y["t0"] < x["t1"] - 1.5 / FPS:
            raise SystemExit(f"two full-screen items overlap in the sheet: {x.get('media') or x.get('gid')} and {y.get('media') or y.get('gid')}")
    for x, y in zip(beats, beats[1:]):
        x["t1"] = min(x["t1"], y["t0"])                           # a frame of rounding between two back-to-back items
    C = dict(source=f"sheet_to_kit.py from the edit sheet of {S['job']} ({S['editor']}); no reverse-engineering",
             style="softblue", words="m.whisper.json", dur=V["duration"], beats=beats, lower_thirds=lts, insets=insets, ctas=ctas,
             auto_cta=False, flash=bool(a.flash), no_caps_kinds=["hf", "cta"],
             deviations=[["graphics", "Soft Blue Light, drawn at 9:16 with HyperFrames from the 16:9's own configs (Dan, 2026-10-01)."],
                         ["picture", "Recut from the raw roll on the sheet's exact frames; the 16:9's delivered mix is untouched."]])
    json.dump(C, open(os.path.join(B, "content.json"), "w"), indent=1)
    open(os.path.join(B, "assets.py"), "w").write(
        '#!/usr/bin/env python3\n"""Media map written by kit9x16/sheet_to_kit.py from the edit sheet (pictures[].sources)."""\n\n'
        f"MASTER = {V['master']!r}\n\nMEDIA = {{\n" + "".join(f"    {k!r}: {v!r},\n" for k, v in media.items()) + "}\n")
    json.dump(report, open(os.path.join(B, "sheet_report.json"), "w"), indent=1)
    nb = sum(1 for b in beats if b["kind"] == "bleed"); nc = sum(1 for b in beats if b["kind"] == "card")
    print(f"{S['job']}: {len(edl)} takes, {len(words)} words, {nc} cards + {nb} fills, {sum(1 for b in beats if b['kind'] == 'hf')} full-screen graphics, "
          f"{len(lts)} lower thirds, {len(insets)} side cards, {len(ctas)} CTAs; base window {cw}x{ch}@{cx},{cy}")
    for p in report["pictures"]:
        print(f"  {p['id']:8s} {p['shape']:6s} {p['why']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
