#!/usr/bin/env python3
"""THE VERTICAL'S GRAPHICS PASS (sheet builds): every graphic drawn fresh at 9:16 in Soft Blue Light with HyperFrames,
from the 16:9's own configs in the edit sheet. Runs AFTER build_kit.py, so each graphic is rendered for the beat times
the kit settled on (a few frames can move when a beat snaps to a cut).

  python3 sbl_graphics.py --build B --sheet SHEET.json [--range A B] [--no-render]

  full-screen graphics (`hf` beats)   -> one opaque render per beat, exactly the beat's frames
  lower thirds / CTAs                 -> a content render + a mask render (the glass blurs the footage under it)
  side cards (3A list, cycle)         -> one transparent overlay at the bottom; captions lift above it (cap_lifts)
  cards (clips, photos, phones)       -> one media-card plate per beat: the moving field with a hole for the picture,
                                         the chip under it. A horizontal clip keeps its full height.

Writes B/hf/ (configs, projects, renders), B/hf/manifest.json (overlays, for the compositor), B/hf/plates.json (hf and
card beats, for render_sbl.py), and `cap_lifts` into beats.json. Cached per graphic on its template + config.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, ".claude/skills/_shared/hyperframes"))
import vertical as VT  # noqa: E402

FPS = 30000 / 1001
FF = VT.B.FF
CAP_LIFT_GAP = 150            # px from the card's top edge up to the caption line's top (a 64 px line + its shadow)


def media_ar(spec):
    o_ = spec[4] if len(spec) > 4 and isinstance(spec[4], dict) else {}
    if o_.get("ar"):
        return float(o_["ar"])                                # the card shows this shape of the picture (render.media_ar's rule)
    o = subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0:s=x", spec[1]], capture_output=True, text=True).stdout.strip().split("\n")[0]
    w, h = (int(x) for x in o.split("x")[:2])
    return w / h


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True); ap.add_argument("--sheet", required=True)
    ap.add_argument("--range", nargs=2, type=float); ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--snap", action="store_true", help="also write hf/stills/<id>.png (the settled graphic)")
    a = ap.parse_args()
    B = os.path.abspath(a.build)
    os.chdir(B); sys.path.insert(0, B)
    S = json.load(open(a.sheet))
    G = {g["id"]: g for g in S["graphics"]}
    J = json.load(open("beats.json"))
    import beats as BT
    from assets import MEDIA
    tl, ov = BT.timeline()
    out = os.path.join(B, "hf")
    inr = lambda t0, t1: (not a.range) or (t0 < a.range[1] and t1 > a.range[0])
    render = not a.no_render
    plates, manifest, lifts = {}, [], []
    prev = 0
    for i, b in enumerate(tl):
        cum = round(b["t1"] * FPS); n = cum - prev; f0 = prev; prev = cum
        if b["kind"] == "hf":
            g = dict(G[b["gid"]]); c = dict(g["config"])
            a_, b_ = f0 / FPS, cum / FPS                       # the beat's exact frames
            c.update(a=a_, b=b_); g.update(config=c, t0=a_, t1=b_)
            scenes, meta = VT.scenes_for(g)
            plates[str(i)] = dict(kind="hf", gid=b["gid"], frames=n, mov=os.path.join(out, "renders", scenes[0][1]["id"] + ".mov"))
            if inr(b["t0"], b["t1"]):
                VT.build(scenes, out, render=render, snap=(max(0.5, n / FPS - 0.6) if a.snap else None))
                print(f"{b['gid']:6s} full-screen {g['template']:22s} {a_:8.2f} {n:5d} f", flush=True)
        elif b["kind"] == "card":
            key = b["media"]; pid = f"card_{key}_{f0}"
            label = b.get("label")
            spans = [[round(x - b["t0"], 3), round(y - b["t0"], 3)] for x, y in b.get("label_spans", [])] or None
            scene, hole = VT.media_card_scene(pid, n / FPS, media_ar(MEDIA[key]), label=label, spans=spans,
                                              kicker="AbsByAI.com" if b.get("phone") else None)
            plates[str(i)] = dict(kind="card", media=key, frames=n, hole=hole, mov=os.path.join(out, "renders", pid + ".mov"),
                                  chip=scene[1].get("chip"))
            if inr(b["t0"], b["t1"]):
                VT.build([scene], out, render=render, snap=(1.0 if a.snap else None))
                print(f"{key:6s} card        hole {hole} {n:5d} f", flush=True)
    for o in ov:
        gid = o.get("gid")
        if o["kind"] == "cta" and not gid:
            gid = f"cta_{round(o['t0'] * 100)}"
            scenes, meta = VT.cta_scenes(gid, o["t1"] - o["t0"], o["top"], o["big"], hold_out=abs(o["t1"] - BT.DUR) < 0.05)
        elif gid in G:
            g = dict(G[gid]); c = dict(g["config"]); c.update(a=o["t0"], b=o["t1"]); g.update(config=c, t0=o["t0"], t1=o["t1"])
            scenes, meta = VT.scenes_for(g)
        else:
            raise SystemExit(f"overlay {o} names no sheet graphic")
        m = dict(id=gid, template=G[gid]["template"] if gid in G else "cta", a=o["t0"], b=o["t1"], mov=os.path.join(out, "renders", gid + ".mov"), **meta)
        if meta["kind"] == "glass":
            m["mask"] = os.path.join(out, "renders", gid + "_mask.mov")
        manifest.append(m)
        if o["kind"] == "hfov":
            lifts.append([o["t0"], o["t1"], int(meta["box"][1] - CAP_LIFT_GAP)])
        if inr(o["t0"], o["t1"]):
            VT.build(scenes, out, render=render, snap=(max(0.5, o["t1"] - o["t0"] - 0.6) if a.snap else None))
            print(f"{gid:6s} overlay     {m['template']:22s} {o['t0']:8.2f} - {o['t1']:8.2f} {meta['kind']}", flush=True)
    json.dump(sorted(manifest, key=lambda m: m["a"]), open(os.path.join(out, "manifest.json"), "w"), indent=1)
    json.dump(plates, open(os.path.join(out, "plates.json"), "w"), indent=1)
    J["cap_lifts"] = lifts
    json.dump(J, open("beats.json", "w"), indent=1)
    print(f"{len(plates)} plates, {len(manifest)} overlays, {len(lifts)} caption lifts -> {out}")


if __name__ == "__main__":
    main()
