#!/usr/bin/env python3
"""plan.json FOR THE DELIVERY GATE, read out of the kit build's own files (never typed by hand):
beats.json (the kit's sheet), edl_picture.json (the picture cuts), piccuts.json (which were moved /
covered), the compositor's cap/manifest.json (caption states), gfx/*.mov (graphic regions) and
gfx/p*.mov.json (window holes), the chips the compositor drew, words_ctc.json, his_mix.wav.
Evidence contract v2, bound to the delivered file's sha256.

  python3 kit_plan.py --build DIR --video master.mp4 [--transcribe] [--reference-cut his.mp4]
                      [--banned-source REC --banned-times 26.4 27.5 ...]
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.abspath(os.path.join(HERE, ".."))
FPS = 30000 / 1001


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True)
    ap.add_argument("--video", required=True)
    ap.add_argument("--transcribe", action="store_true")
    ap.add_argument("--reference-cut")
    ap.add_argument("--banned-source")
    ap.add_argument("--banned-times", nargs="*", type=float)
    ap.add_argument("--source-audio", default="his_mix.wav")
    a = ap.parse_args()
    os.chdir(a.build)
    sys.path.insert(0, os.getcwd())
    import beats as B                                         # the kit's shim, reading beats.json
    import captions as CP
    VID = a.video
    if not os.path.exists(VID):
        raise SystemExit(f"delivered file not on disk: {VID}")
    tl, ov = B.timeline()
    P = json.load(open("edl_picture.json"))
    NTOT = P[-1]["n1"]
    pc = json.load(open("piccuts.json")) if os.path.exists("piccuts.json") else []

    # joins: every PICTURE cut on the delivered timeline (the pose-matched frames, not the audio splices)
    joins = sorted({round(s["n0"] / FPS, 3) for s in P[1:]})
    covered = [[round(b["t0"], 3), round(b["t1"], 3)] for b in tl if b["kind"] != "talk"]
    muted = set(B.NO_CAPS_KINDS)
    cards = [[round(b["t0"], 3), round(b["t1"], 3)] for b in tl + ov
             if b["kind"] in muted or b["kind"] in ("lt", "cta") or b.get("caps") is False]
    # a splice the rule covered with a push: its push window is a declared beat (the push IS the cover)
    for r in pc:
        if r.get("cover") == "push":
            pass                                              # the push schedule below already declares it

    # punch: NEAR inside a push, FAR outside (plan_sq.py: ramp frames belong to the segment they head into)
    lev, prev, a0 = [], None, 0.0
    for k in range(NTOT):
        t = k / FPS
        L = "NEAR" if B.push_at(t) > 1.0 + (B.PUSH_Z - 1.0) * 0.5 else "FAR"
        if L != prev:
            if prev is not None:
                lev.append([round(a0, 3), round(t, 3), prev])
            prev, a0 = L, t
    lev.append([round(a0, 3), round(NTOT / FPS, 3), prev])
    kind_at = {}
    for b in tl:
        for k in range(int(round(b["t0"] * FPS)), min(NTOT, int(round(b["t1"] * FPS)))):
            kind_at[k] = b["kind"]
    punch, punch_covered = [], []
    for x, y, L in lev:
        punch.append([x, y, L])
        k0 = int(round(x * FPS))
        punch_covered.append(kind_at.get(k0 - 1, "talk") != "talk" or kind_at.get(k0, "talk") != "talk")

    # the chips the compositor drew (full-bleed: render.chip PNGs; cards: plate_card's own chip)
    from PIL import Image
    os.makedirs("plan_assets", exist_ok=True)

    def _name(b):
        return os.path.basename(str(b.get("media") or b.get("kind")))

    def insert_list(kind):
        out = []
        for b in tl:
            if b.get("label_kind") != kind:
                continue
            item = dict(name=_name(b), beat=[round(b["t0"], 3), round(b["t1"], 3)])
            if b["kind"] == "bleed" and b.get("chip_png") and os.path.exists(b["chip_png"]):
                im = Image.open(b["chip_png"]).convert("RGBA")
                bb = im.getchannel("A").getbbox()
                q = f"plan_assets/chip_{kind}_{_name(b)}.png"
                im.crop(bb).save(q)
                item.update(chip=os.path.abspath(q), pos=[bb[0], bb[1]])
            elif b["kind"] == "card":
                # plate_card hangs the chip off the hole: rebuild the same layer the plate drew
                import vlib
                metas = sorted(glob.glob(f"gfx/p{tl.index(b):03d}_*.mov.json"), key=os.path.getmtime)   # the plate THIS render used
                if metas:
                    holes = json.load(open(metas[-1]))
                    hole = holes.get("media")
                    if hole:
                        fl = vlib.font(30, "SemiBold")
                        from PIL import ImageDraw
                        from motionlib import text_size
                        txt = b.get("label") or ("AI-GENERATED" if kind == "ai" else "Real picture of me - not AI-generated")
                        lw, lh_ = text_size(txt, fl)
                        lay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
                        bx = (1080 - (lw + 34)) // 2
                        by = int(hole[3]) + 14 + 54                # vlib.plate_card: 54 px below the card frame, never over the picture
                        ImageDraw.Draw(lay).rounded_rectangle([bx, by, bx + lw + 34, by + lh_ + 22], radius=9, fill=(0, 0, 0, 215))
                        ImageDraw.Draw(lay).text((bx + 17, by + 11), txt, font=fl, fill=(255, 255, 255, 255), anchor="lt")
                        bb = lay.getchannel("A").getbbox()
                        q = f"plan_assets/chip_{kind}_{_name(b)}_card.png"
                        lay.crop(bb).save(q)
                        item.update(chip=os.path.abspath(q), pos=[bb[0], bb[1]])
            out.append(item)
        return out
    real_photos = insert_list("real")
    ai_inserts = insert_list("ai")
    chips, pos = {}, {}
    for kind, lst in (("real", real_photos), ("ai", ai_inserts)):
        for it in lst:
            if it.get("chip"):
                chips[kind], pos[kind] = it["chip"], it["pos"]
                break

    graphics = []
    for i, o in enumerate(ov):
        for f in sorted(glob.glob(f"gfx/ov_{o['kind']}_*.mov")):
            if os.path.exists(f + ".beat") and open(f + ".beat").read().strip() == f"{o['t0']:.4f}":
                graphics.append(dict(name=f"{o['kind']}@{o['t0']:.2f}", beat=[round(o["t0"], 3), round(o["t1"], 3)], mov=os.path.abspath(f)))
                break

    # captions as SRT from the SAME groups the compositor burned, with the rendered cue end (plan_build.py)
    words = CP.load_words()
    gs = CP.groups(words, CP.suppressed())
    _STOPS = sorted(set([x for x, _ in CP.suppressed()] + list(getattr(B, "SEAMS", []))))

    def ts(t):
        h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
        return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")

    def cue_end(g, nxt):
        ws, we = g[-1][1], g[-1][2]
        hold = max(we, ws + 0.12)
        end = min(nxt, max(hold, min(nxt, we + 0.8))) if nxt is not None else we + 0.3
        end = max(end, ws + 1.0 / 29.97)
        stop = next((s_ for s_ in _STOPS if s_ > ws + 1e-3), None)
        if stop is not None:
            end = max(min(end, stop), ws + 1.0 / 29.97)
        return end
    srt = []
    for i, g in enumerate(gs, 1):
        nxt = gs[i][0][1] if i < len(gs) else None
        srt.append(f"{i}\n{ts(g[0][1])} --> {ts(cue_end(g, nxt))}\n{' '.join(x[0] for x in g)}\n")
    open("plan_assets/captions.srt", "w").write("\n".join(srt))

    plan = dict(
        target_seconds=round(NTOT / FPS, 6), target_frames=NTOT,
        joins=joins, covered=covered, cards=cards, punch=punch, punch_covered=punch_covered,
        real_photos=real_photos, ai_inserts=ai_inserts, graphics=graphics,
        label_chips=chips, label_pos=pos,
        srt=os.path.abspath("plan_assets/captions.srt"),
        words=[dict(w=w["word"], t=round(float(w["start"]), 3), e=round(float(w["end"]), 3)) for w in json.load(open("words_ctc.json"))],
        source_audio=os.path.abspath(a.source_audio),
        watch_log=os.path.abspath("logs/watch_pass.json"),
        kit=dict(piccuts=os.path.abspath("piccuts.json"), report=os.path.abspath("kit_report.json"),
                 moved_cuts=sum(1 for r in pc if r.get("k")), covered_cuts=sum(1 for r in pc if r.get("cover"))),
    )
    if a.reference_cut:
        plan["reference_cut"] = os.path.abspath(a.reference_cut)
    if a.banned_source:
        plan["banned_source"] = os.path.abspath(a.banned_source)
        plan["banned_times"] = a.banned_times or []
    old = json.load(open("plan.json")) if os.path.exists("plan.json") else {}
    for k in ("transcript_words", "negative_events_scan", "declare"):
        if k in old:
            plan[k] = old[k]
    delivered_speech = None
    speech_timing = None
    if a.transcribe:
        import shutil
        import subprocess
        import whisper
        r = whisper.load_model("small").transcribe(VID, word_timestamps=True, language="en")
        plan["transcript_words"] = [dict(w=w) for seg in r["segments"] for w in seg["text"].split()]
        delivered_speech = [dict(w=w["word"].strip(), t=round(float(w["start"]), 3), e=round(float(w["end"]), 3))
                            for seg in r["segments"] for w in seg.get("words", []) if w["word"].strip()]
        speech_timing = "whisper word timestamps"
        # Whisper's own word starts run ~130 ms EARLY (captions.py: measured against a CTC forced alignment, the
        # reason the captions moved to CTC timing after Dan's 2026-09-08 rejection). Measured against them, a
        # CTC-exact caption track reads +109 ms late with 191 misses (kit9x16 from-raw pass 8). So the delivered
        # ASR's WORDS keep their provenance and their TIMING comes from the same forced aligner run on the
        # DELIVERED audio -- still evidence from the delivered file, just the accurate instrument.
        d = os.path.abspath("_asr_ctc")
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        try:
            json.dump(r, open(os.path.join(d, "ref.whisper.json"), "w"))
            env = dict(os.environ, PYTHONPATH=os.getcwd() + os.pathsep + os.environ.get("PYTHONPATH", ""))   # the build's captions/beats/assets
            ff = os.path.join(REF, "..", "..", "..", "..", "Media", "video_edit", "bin", "ffmpeg")
            ff = ff if os.path.exists(ff) else "ffmpeg"
            subprocess.run([ff, "-v", "error", "-y", "-i", os.path.abspath(VID), "-vn", "-ac", "2", "-ar", "48000",
                            "-c:a", "pcm_s16le", os.path.join(d, "his_mix.wav")], check=True)
            subprocess.run([sys.executable, os.path.join(REF, "a2", "align_ctc.py")], cwd=d, check=True,
                           capture_output=True, text=True, env=env)
            ctc = json.load(open(os.path.join(d, "words_ctc.json")))
            delivered_speech = [dict(w=w["word"].strip(), t=round(float(w["start"]), 3), e=round(float(w["end"]), 3))
                                for w in ctc if w["word"].strip()]
            speech_timing = "wav2vec2 CTC forced alignment of the delivered ASR words to the delivered audio"
        except Exception as e:                                    # the words stand; only the timing falls back
            tail = (getattr(e, "stderr", "") or "")[-400:]
            print(f"delivered-ASR CTC timing unavailable ({e}) {tail}; whisper word timestamps used", flush=True)

    # ---- evidence contract v2
    manifest = "cap/manifest.json"
    if not os.path.exists(manifest):
        raise SystemExit("cap/manifest.json is missing; run captions.py (the compositor manifest) before the plan")
    plan["caption_states"] = json.load(open(manifest))["caption_states"]
    plan["speech_words"] = delivered_speech or list(plan["words"])
    plan["speech_words_evidence"] = (dict(method="delivered_asr", video_sha256=sha(VID), timing=speech_timing) if delivered_speech
                                     else dict(method="verbatim_source_ctc"))
    # region beats on the FRAME grid: a graphic enabled at t0 first draws on the first frame at or after t0, and
    # the compositor's caption states are frame-exact, so a state that ends on that frame (exclusive) does not
    # share a frame with it. Declared at the unquantised t0 the gate read a 0.9 ms "overlap" as a collision
    # (round 5: 'improves.' ending 111.0109 vs card@111.000). The end rounds UP to the next frame: stricter.
    import math
    qa = lambda t: math.ceil(t * FPS - 1e-6) / FPS
    qb = lambda t: (math.floor(t * FPS + 1e-6) + 1) / FPS
    regions = [dict(name=f"card@{x:.3f}", beat=[qa(x), qb(y)], rect=[0, 0, 1080, 1920]) for x, y in cards]
    for g in graphics:
        regions.append(dict(name=g["name"], beat=[qa(g["beat"][0]), qb(g["beat"][1])], mov=g["mov"], mov_sha256=sha(g["mov"])))
    plan["graphic_regions"] = regions
    windows = []
    for i, b in enumerate(tl):
        beat = [round(b["t0"], 3), round(b["t1"], 3)]
        if b["kind"] == "talk":
            windows.append(dict(name=f"talk-{i}", beat=beat, rect=[0, 0, 1080, 1920], motion="tracking"))
            continue
        metas = sorted(glob.glob(f"gfx/p{i:03d}_*.mov.json"), key=os.path.getmtime)
        if metas:
            holes = json.load(open(metas[-1]))
            if "dan" in holes:
                x0, y0, x1, y1 = holes["dan"]
                windows.append(dict(name=f"{b['kind']}-{i}", beat=beat, rect=[round(x0), round(y0), round(x1 - x0), round(y1 - y0)], motion="fixed-wide"))
    plan["talking_head_windows"] = windows
    tracks = []
    for kind, items in (("ai", ai_inserts), ("real", real_photos)):
        other = "real" if kind == "ai" else "ai"
        for i, item in enumerate(items):
            image = item.get("chip")
            if not image:
                continue
            wrong = chips.get(other)
            tracks.append(dict(name=f"{kind}-{i}-{item.get('name', 'insert')}", kind=kind, beat=item["beat"], image=image,
                               image_sha256=sha(image), wrong_image=wrong, wrong_image_sha256=sha(wrong) if wrong else None,
                               pos=item.get("pos"), search_px=2, visibility="full"))
    plan["label_tracks"] = tracks
    plan["evidence_contract"] = dict(version=2, video_sha256=sha(VID),
                                     generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    json.dump(plan, open("plan.json", "w"), indent=1)
    print(f"plan.json: {len(joins)} joins, {len(punch)} framing segments, {len(real_photos)} real photos, {len(ai_inserts)} AI inserts, "
          f"{len(graphics)} graphics, {len(gs)} caption cues, {len(plan['words'])} words, {len(windows)} windows, {len(tracks)} label tracks, "
          f"transcript {len(plan.get('transcript_words') or [])}")


if __name__ == "__main__":
    sys.exit(main())
