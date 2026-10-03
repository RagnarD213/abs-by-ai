#!/usr/bin/env python3
"""plan.json FOR THE SQUARE'S DELIVERY GATE (--format ad1x1), derived from the locked vertical's own plan and the square
build's records (sq_render.py), never typed by hand. The square shares the vertical's timeline, cuts, pushes, words and
audio stream (md5-asserted at mux), so those carry over; what is re-derived is everything with a position:

  label_tracks / real_photos / ai_inserts   our chips on the square: a fill's measured chip (sq_fit.json), a card's
                                            chip under its hole (cropped from the delivered frame, the plate draws it)
  caption_states                            the vertical's states at the square position each frame was drawn at
                                            (Q/cap_drawn.json); a state the square did not draw is not declared, and
                                            its span is declared muted (a card) instead
  graphic_regions / talking_head_windows    the vertical's spans on the 1080x1080 frame
  speech_words evidence                     the vertical's delivered-ASR words: the square's audio IS that stream

  python3 sq_plan.py --build B --out Q --video "Q/<name>.mp4"
"""
import argparse, copy, datetime, hashlib, json, math, os, subprocess, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
FPS = 30000 / 1001
S = 1080


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()


def amd5(p):
    return subprocess.run([FF, "-v", "error", "-i", p, "-map", "0:a", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True).stdout.strip()


def frame(video, n):
    o = subprocess.run([FF, "-v", "error", "-i", video, "-vf", f"select=eq(n\\,{n}),scale=in_color_matrix=bt709:in_range=tv,format=rgb24",
                        "-frames:v", "1", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(o, np.uint8).reshape(S, S, 3)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--build", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--video", required=True); ap.add_argument("--vertical", required=True)
    ap.add_argument("--cut", action="store_true", help="the <=0:59 square: --vertical is the vertical CUTDOWN, its plan B/cut_audit/plan.json")
    a = ap.parse_args()
    B, Q, V = os.path.abspath(a.build), os.path.abspath(a.out), os.path.abspath(a.video)
    if a.cut:
        return cut_plan(a, B, Q, V)
    VP = json.load(open(os.path.join(B, "plan.json")))
    fit = json.load(open(os.path.join(Q, "sq_fit.json")))
    plates = json.load(open(os.path.join(Q, "plates.json")))
    drawn = json.load(open(os.path.join(Q, "cap_drawn.json")))
    assert amd5(V) == amd5(a.vertical), "the square's audio is not the vertical's stream: its words cannot be carried over"
    assert VP["speech_words_evidence"].get("video_sha256") == sha(a.vertical), "the vertical's plan is not bound to the vertical given"
    P = copy.deepcopy(VP)
    os.makedirs(os.path.join(Q, "plan_assets"), exist_ok=True)
    q2 = lambda t: round(t, 3)

    # ---- labels: one track per labelled picture, at its square position
    real, ai, tracks, chips, pos = [], [], [], {}, {}
    for i, c in sorted(fit.items(), key=lambda kv: kv[1]["t0"]):
        kind = {"Real picture of me - not AI-generated": "real", "AI-GENERATED": "ai"}.get(c.get("label"))
        name = c["media"]; beat = [q2(c["t0"]), q2(c["t1"])]
        if c.get("his_chip") or (c["fit"] == "fill" and kind is None and "ai" in str(c.get("label_kind", ""))):
            pass
        item = dict(name=name, beat=beat)
        if kind and c["fit"] == "fill" and c.get("chip_png"):
            im = Image.open(c["chip_png"]).convert("RGBA"); bb = im.getchannel("A").getbbox()
            p_ = os.path.join(Q, "plan_assets", f"chip_{kind}_{i}_{name}.png"); im.crop(bb).save(p_)
            item.update(chip=p_, pos=[bb[0], bb[1]])
        elif kind and c["fit"] == "card":
            ch = plates[i]["chip"]
            g = int(round((c["t0"] + c["t1"]) / 2 * FPS))
            fr_ = frame(V, g)
            p_ = os.path.join(Q, "plan_assets", f"chip_{kind}_{i}_{name}_card.png")
            Image.fromarray(fr_[ch["y"]:ch["y"] + 80, ch["x"]:ch["x"] + ch["w"]]).convert("RGBA").save(p_)
            item.update(chip=p_, pos=[ch["x"], ch["y"]])
        if kind == "real": real.append(item)
        elif kind == "ai" or c.get("his_chip"): ai.append(item)
        if item.get("chip") and kind not in chips:
            chips[kind], pos[kind] = item["chip"], item["pos"]
    for kind, items in (("ai", ai), ("real", real)):
        other = "real" if kind == "ai" else "ai"
        for j, it in enumerate(items):
            if not it.get("chip"): continue
            w = chips.get(other)
            tracks.append(dict(name=f"{kind}-{j}-{it['name']}", kind=kind, beat=it["beat"], image=it["chip"], image_sha256=sha(it["chip"]),
                               wrong_image=w, wrong_image_sha256=sha(w) if w else None, pos=it["pos"], search_px=2, visibility="full"))
    P.update(real_photos=real, ai_inserts=ai, label_chips=chips, label_pos=pos, label_tracks=tracks)

    # ---- captions: the vertical's states where (and as) the square drew them
    at = {g: (yy, r0, x0, x1, h) for g, yy, r0, x0, x1, h in drawn}
    states, muted = [], []
    for st in VP["caption_states"]:
        g0 = int(round(st["beat"][0] * FPS)); g1 = int(round(st["beat"][1] * FPS))   # beats are frame times (k / FPS, 4 decimals)
        runs, cur = [], None
        for g in range(g0, g1):
            k = at.get(g)
            key = k[0] if k else None
            if cur and cur[2] == key and cur[1] == g: cur[1] = g + 1
            else:
                if cur: runs.append(cur)
                cur = [g, g + 1, key]
        if cur: runs.append(cur)
        src = Image.open(st["image"]).convert("RGBA")
        for r0, r1, yy in runs:
            if yy is None:
                muted.append([r0 / FPS, r1 / FPS]); continue
            _, top, _, _, h = at[r0]
            band = src.crop((0, top, S, top + h))
            bb = band.getchannel("A").getbbox()
            if not bb: continue
            p_ = os.path.join(Q, "plan_assets", f"cap_{st['name']}_{r0}.png"); band.crop(bb).save(p_)
            states.append(dict(st, name=f"{st['name']}@{r0}", beat=[round(r0 / FPS, 4), round(r1 / FPS, 4)], image=p_,
                               pos=[bb[0], yy + bb[1]], scale=1.0, image_sha256=sha(p_)))
    P["caption_states"] = states
    # spans the square keeps captions off that the vertical had on (a lift above a tall side card has no room) are muted spans
    merged = []
    for x, y in sorted(muted):
        if merged and x - merged[-1][1] < 1.5 / FPS: merged[-1][1] = max(merged[-1][1], y)
        else: merged.append([x, y])
    P["cards"] = sorted(VP["cards"] + [[round(x, 3), round(y, 3)] for x, y in merged])
    P["square_caption_muted"] = [[round(x, 3), round(y, 3)] for x, y in merged]

    # ---- regions and windows on the square frame
    P["graphic_regions"] = [dict(r, rect=[0, 0, S, S]) for r in VP["graphic_regions"] if "rect" in r] + \
        [dict(name=f"sqmuted@{x:.3f}", beat=[math.ceil(x * FPS - 1e-6) / FPS, (math.floor(y * FPS + 1e-6) + 1) / FPS], rect=[0, 0, S, S]) for x, y in merged]
    P["talking_head_windows"] = [dict(w, rect=[0, 0, S, S]) for w in VP["talking_head_windows"] if w["motion"] == "tracking"]
    P["graphics"] = []
    P["watch_log"] = os.path.join(Q, "logs", "watch_pass.json")
    for k in ("negative_events_scan", "declare"):
        P.pop(k, None)
    old = os.path.join(Q, "plan.json")
    if os.path.exists(old):
        o = json.load(open(old))
        if o.get("negative_events_scan", {}).get("sha256") == sha(V): P["negative_events_scan"] = o["negative_events_scan"]
    vs = sha(V)
    P["speech_words_evidence"] = dict(VP["speech_words_evidence"], video_sha256=vs,
                                      carried_from=dict(vertical_sha256=VP["speech_words_evidence"]["video_sha256"], audio_stream_md5=amd5(V)))
    P["evidence_contract"] = dict(version=2, video_sha256=vs, generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    json.dump(P, open(os.path.join(Q, "plan.json"), "w"), indent=1)
    print(f"square plan.json: {len(tracks)} label tracks, {len(states)} caption states ({len(VP['caption_states'])} in the vertical), "
          f"{len(merged)} spans the square mutes, {len(P['talking_head_windows'])} windows")


def caption_states(VP, drawn, outdir, S_=S):
    """The vertical's caption states where (and as) the square drew them; returns (states, muted spans)."""
    at = {g: (yy, r0, x0, x1, h) for g, yy, r0, x0, x1, h in drawn}
    states, muted = [], []
    for st in VP["caption_states"]:
        g0 = int(round(st["beat"][0] * FPS)); g1 = int(round(st["beat"][1] * FPS))
        runs, cur = [], None
        for g in range(g0, g1):
            k = at.get(g); key = k[0] if k else None
            if cur and cur[2] == key and cur[1] == g: cur[1] = g + 1
            else:
                if cur: runs.append(cur)
                cur = [g, g + 1, key]
        if cur: runs.append(cur)
        src = Image.open(st["image"]).convert("RGBA")
        for r0, r1, yy in runs:
            if yy is None:
                muted.append([r0 / FPS, r1 / FPS]); continue
            _, top, _, _, h = at[r0]
            band = src.crop((0, top, S_, top + h)); bb = band.getchannel("A").getbbox()
            if not bb: continue
            p_ = os.path.join(outdir, f"cap_{st['name']}_{r0}.png"); band.crop(bb).save(p_)
            states.append(dict(st, name=f"{st['name']}@{r0}", beat=[round(r0 / FPS, 4), round(r1 / FPS, 4)], image=p_,
                               pos=[bb[0], yy + bb[1]], scale=1.0, image_sha256=sha(p_)))
    merged = []
    for x, y in sorted(muted):
        if merged and x - merged[-1][1] < 1.5 / FPS: merged[-1][1] = max(merged[-1][1], y)
        else: merged.append([x, y])
    return states, merged


def cut_plan(a, B, Q, V):
    """The square cutdown: the vertical cutdown's plan (same frames, same audio stream, same caption track), with the
    square full plan's labels mapped through the cut ranges and the caption states at the square's drawn positions."""
    VP = json.load(open(os.path.join(B, "cut_audit", "plan.json")))
    SP = json.load(open(os.path.join(Q, "plan.json")))
    ranges = json.load(open(os.path.join(B, "cut_plan.json")))["ranges"]
    assert amd5(V) == amd5(a.vertical), "the square cutdown's audio is not the vertical cutdown's stream"
    assert VP["evidence_contract"]["video_sha256"] == sha(a.vertical), "the vertical cutdown's plan is not bound to the file given"
    out = os.path.join(Q, "cut_audit"); os.makedirs(os.path.join(out, "plan_assets"), exist_ok=True); os.makedirs(os.path.join(out, "logs"), exist_ok=True)

    def spans(beat):
        a0, a1 = float(beat[0]), float(beat[1]); res = []
        for r in ranges:
            lo, hi = max(a0, r["src0"]), min(a1, r["src1"])
            if hi - lo >= 0.5 / FPS:
                res.append([round(r["dst0"] + lo - r["src0"], 6), round(r["dst0"] + hi - r["src0"], 6)])
        return res
    mapit = lambda items: [dict(it, beat=sp) for it in items or [] for sp in spans(it["beat"])]
    P = copy.deepcopy(VP)
    P.update(real_photos=mapit(SP.get("real_photos")), ai_inserts=mapit(SP.get("ai_inserts")),
             label_tracks=[dict(t, name=f"{t['name']}@{i}") for i, t in enumerate(mapit(SP.get("label_tracks")))],
             label_chips=SP.get("label_chips", {}), label_pos=SP.get("label_pos", {}))
    states, merged = caption_states(VP, json.load(open(os.path.join(Q, "cap_drawn_cut.json"))), os.path.join(out, "plan_assets"))
    P["caption_states"] = states
    P["cards"] = sorted(VP["cards"] + [[round(x, 3), round(y, 3)] for x, y in merged])
    P["graphic_regions"] = [dict(r, rect=[0, 0, S, S]) for r in VP["graphic_regions"] if "rect" in r] + \
        [dict(name=f"sqmuted@{x:.3f}", beat=[math.ceil(x * FPS - 1e-6) / FPS, (math.floor(y * FPS + 1e-6) + 1) / FPS], rect=[0, 0, S, S]) for x, y in merged]
    P["talking_head_windows"] = [dict(w, rect=[0, 0, S, S]) for w in VP.get("talking_head_windows", []) if w.get("motion") == "tracking"]
    P["graphics"] = []
    P["watch_log"] = os.path.join(out, "logs", "watch_pass.json")
    P.pop("negative_events_scan", None)
    old = os.path.join(out, "plan.json")
    if os.path.exists(old):
        o = json.load(open(old))
        if o.get("negative_events_scan", {}).get("sha256") == sha(V): P["negative_events_scan"] = o["negative_events_scan"]
    P["evidence_contract"] = dict(version=2, video_sha256=sha(V), generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    json.dump(P, open(old, "w"), indent=1)
    print(f"square cutdown plan.json: {len(P['label_tracks'])} label tracks, {len(states)} caption states ({len(VP['caption_states'])} in the "
          f"vertical cutdown), {len(merged)} spans the square mutes")


if __name__ == "__main__":
    main()
