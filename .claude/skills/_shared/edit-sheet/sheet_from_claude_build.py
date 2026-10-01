#!/usr/bin/env python3
"""WRITE THE EDIT SHEET (README.md here) FROM A CLAUDE 16:9 BUILD. Nothing is re-decided: every field is copied from
the build's own files, or measured on the raw roll where the build never stored it (head position).

  python3 sheet_from_claude_build.py BUILD_DIR [--master FILE] [--out SHEET.json] [--facts FACTS.json]
                                     [--job RO-10] [--title "..."] [--type LFC|SFC|AD] [--approved "Dan's words"]

Two build families are read:
  round   /longform-edit and /ad-edit round-method builds (RO-10, RO-11, RO-13, RO-16): edl.json, shots.json,
          plan_resolved.json, words_out.json, hf/ (configs, manifest, beats), recipe/frames.py (roll, LUT, crops),
          <master>.build.json (the solved picture segments), round*-plan/decisions.json
  adkit   the RA-01 ad build: cut.json, beats.json, timeline_16x9.json, framing.json, grade.json, ra01lib.py,
          words_aligned.json. Its graphics are the older adkit set, recorded as `adkit:<kind>`.

--facts: {picture id: {people, physique}} for pictures whose plan item did not record who is in them. New plans
carry `people` and `physique` on every clip / photo item; a picture with neither, no --facts row and no clip-library
record is an ERROR here (never a guess). The sheet is validated before it is written.
"""
import argparse
import glob
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import headmeasure  # noqa: E402
import validate  # noqa: E402

REPO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
FF = f"{REPO}/Media/video_edit/bin/ffmpeg"
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
CATALOG = f"{REPO}/Media/clip-library/catalog.json"
FPS = 30000 / 1001
REAL_CHIP = "Real picture of me. Not AI-generated."


def sha(path, cap=None):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def load_py(path, name):
    cwd = os.getcwd()
    os.chdir(os.path.dirname(path))
    sys.path.insert(0, os.path.dirname(path))
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m
    finally:
        os.chdir(cwd)
        sys.path.pop(0)


def video_block(master, rolls):
    o = subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0", "-count_packets",
                        "-show_entries", "stream=width,height,nb_read_packets", "-of", "csv=p=0", master],
                       capture_output=True, text=True).stdout.strip().split(",")
    w, h, n = int(o[0]), int(o[1]), int(o[2])
    R = {}
    for name, p in rolls.items():
        rw, rh, rr = headmeasure.probe(p)
        R[name] = dict(path=p, width=rw, height=rh, fps=rr)
    return dict(master=master, sha256=sha(master), fps="30000/1001", frames=n, duration=round(n / FPS, 4), width=w, height=h, rolls=R)


def label_kind(label):
    if not label:
        return "none"
    return "ai" if "AI-GEN" in label.upper() else ("real" if "REAL" in label.upper() else "none")


_CAT = None
def catalog(cid):
    global _CAT
    if _CAT is None:
        _CAT = {c["id"]: c for c in json.load(open(CATALOG))["clips"]} if os.path.exists(CATALOG) else {}
    return _CAT.get(cid)


def who(pid, item, facts, lib_id=None):
    """(people, physique, source) from the plan item, the --facts file, or the clip library; never a guess."""
    if "people" in item and "physique" in item:
        return item["people"], bool(item["physique"]), "plan item"
    if pid in facts:
        return facts[pid]["people"], bool(facts[pid]["physique"]), "facts file (recorded by the 16:9 session after viewing the clip)"
    c = catalog(lib_id) if lib_id else None
    if c and c.get("people"):
        p = c["people"]
        people = "none" if p == "none" else ("dan" if p.startswith("dan") else "other")
        phys = any(t in (c.get("tags") or []) for t in ("shirtless", "physique", "abs"))
        return people, phys, f"clip library {lib_id}"
    raise SystemExit(f"picture {pid}: who is in it is not recorded (add people / physique to the plan item, or a --facts row)")


def head_rows(edl, crops, rolls, work, haircheck=None):
    """framing[].head per segment: min hair top, median centre and chin over samples of the segment, raw pixels."""
    import numpy as np
    by_roll = {}
    for i, s in enumerate(edl):
        n = s["out_f1"] - s["out_f0"]
        d = n / FPS
        ts = sorted({round(s["src_in"] + d * q, 3) for q in ((0.5,) if d < 1.2 else (0.12, 0.5, 0.88) if d < 8 else (0.08, 0.3, 0.5, 0.7, 0.92))})
        by_roll.setdefault(s["roll"], []).append((i, ts))
    out = [None] * len(edl)
    for roll, rows in by_roll.items():
        allt = sorted({t for _, ts in rows for t in ts})
        M = headmeasure.measure(rolls[roll], allt, os.path.join(work, f"heads_{roll}"))
        for i, ts in rows:
            ok = [M[t] for t in ts if M.get(t)]
            if not ok:
                continue
            out[i] = dict(hair_top=min(m["hair_top"] for m in ok), cx=float(np.median([m["cx"] for m in ok])),
                          chin=float(np.median([m["chin"] for m in ok])), face_w=float(np.median([m["face_w"] for m in ok])),
                          samples=len(ok))
    # a segment with no face found (covered by an insert, or too short) takes its neighbour on the same take
    for i in range(len(out)):
        if out[i] is None:
            near = sorted((j for j in range(len(out)) if out[j] is not None and edl[j]["roll"] == edl[i]["roll"]),
                          key=lambda j: abs(edl[j]["src_in"] - edl[i]["src_in"]))
            if not near:
                raise SystemExit(f"no head found anywhere on roll {edl[i]['roll']}")
            out[i] = dict(out[near[0]], samples=0, borrowed_from=near[0])
    # the build's own dense hair check on the delivered file (4 fps), mapped back through each segment's crop
    if haircheck:
        for i, s in enumerate(edl):
            cw, ch, cx, cy = crops[i]
            tops = [r["top"] for r in haircheck if r.get("top") is not None and s["out_in"] + 0.05 <= r["t"] < s["out_out"] - 0.05]
            if tops:
                out[i]["hair_top"] = round(min(out[i]["hair_top"], cy + min(tops) * ch / 1080.0), 1)
                out[i]["hair_dense_samples"] = len(tops)
    return out


# ------------------------------------------------------------------------------------------------ round family
def texts_of(template, c):
    if template == "lower-third":
        return [c["topic"]] + [p for p, _ in c["parts"]]
    if template == "before-card":
        return [c["eyebrow"][0]] + [p for p, _ in c["headline"]] + ([c["detail"][0]] if c.get("detail") else []) + ([c["label"]] if c.get("label") else [])
    if template == "side-list":
        return (c["heading"] if isinstance(c["heading"], list) else [c["heading"]]) + list(c["items"])
    if template == "cycle":
        return [c["title"]] + list(c["boxes"])
    return []


def from_round(B, a, facts):
    masters = [a.master] if a.master else sorted(glob.glob(os.path.join(B, "round*", "*MASTER*.mp4")) +
                                                 glob.glob(os.path.join(B, "round*", "*.mp4")), key=os.path.getmtime)
    masters = [m for m in masters if os.path.exists(m + ".build.json")]
    if not masters:
        raise SystemExit("no master with a .build.json beside it (pass --master)")
    master = os.path.abspath(masters[-1])
    build = json.load(open(master + ".build.json"))
    F = load_py(os.path.join(B, "recipe", "frames.py"), "frames_recipe")
    roll = os.path.splitext(os.path.basename(F.SRC))[0]
    rolls = {roll: F.SRC}
    V = video_block(master, rolls)
    segs = build["segments"]
    if segs[-1]["o1"] != V["frames"]:
        raise SystemExit(f"{master}.build.json ends on frame {segs[-1]['o1']}, the master has {V['frames']}")
    edl, fr_rows, crops = [], [], []
    for i, s in enumerate(segs):
        n = s["o1"] - s["o0"]
        p = segs[i - 1] if i else None
        join = "first" if not i else ("reframe" if p["src0"] + (p["o1"] - p["o0"]) == s["src0"] else "cut")
        edl.append(dict(roll=roll, src_f0=s["src0"], src_in=round(s["src0"] / FPS, 5), src_out=round((s["src0"] + n) / FPS, 5),
                        out_f0=s["o0"], out_f1=s["o1"], out_in=round(s["o0"] / FPS, 5), out_out=round(s["o1"] / FPS, 5),
                        shot=s["shot"], audio="sync", join=join, covered=bool(s.get("covered")), side_card=s.get("card")))
        crops.append(list(F.CROP[s["framing"]]))
    hc = None
    hp = os.path.join(os.path.dirname(master), "logs", "haircheck.json")
    if os.path.exists(hp):
        hc = json.load(open(hp))["rows"]
    heads = head_rows(edl, crops, rolls, a.work, hc)
    for s, c, h in zip(segs, crops, heads):
        fr_rows.append(dict(name=s["framing"], crop=c, head=h, wall_stretch=bool(s.get("shifted") and s["framing"] == "W2"),
                            measured="mediapipe face box + Apple Vision person mask on the raw roll (headmeasure.py)"
                                     + ("; hair top also from the build's dense haircheck.json on the master" if hc else "")))
    grade = dict(filter="scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,format=gbrpf32le,"
                        f"lut3d=file='{F.LUT}':interp=tetrahedral", lut=F.LUT, decode="bt709", order="after_scale_1080",
                 note="the build's recipe/frames.py vf(): crop, scale to 1920x1080 with a BT.709 decode, then the LUT in float RGB")
    # words
    W = [dict(w=w["w"], t0=round(w["t0"], 4), t1=round(w["t1"], 4)) for w in json.load(open(os.path.join(B, "words_out.json"))) if w.get("t0") is not None]
    fx = os.path.join(os.path.dirname(master), "srt_fixes.json")
    words = dict(list=W, timing="mapped-source (roll word timings carried through the shot map)", fixes=json.load(open(fx)) if os.path.exists(fx) else [])
    # graphics
    plan = json.load(open(os.path.join(B, "plan_resolved.json")))
    man = {m["id"]: m for m in json.load(open(os.path.join(B, "hf", "manifest.json")))} if os.path.exists(os.path.join(B, "hf", "manifest.json")) else {}
    beats = {b["id"]: b for b in json.load(open(os.path.join(B, "hf", "beats.json")))} if man else {}
    LAYER = {"lower-third": "overlay", "before-card": "full", "side-list": "side", "cycle": "side"}
    ntitles = sum(1 for it in plan if it["kind"] == "title")
    graphics, pictures = [], []
    for it in plan:
        k = it["kind"]
        if it["id"] in man:
            m = man[it["id"]]
            cfg = json.load(open(os.path.join(B, "hf", "configs", m["template"], it["id"] + ".json")))[0]
            graphics.append(dict(id=it["id"], template=m["template"], config=cfg, text=texts_of(m["template"], cfg),
                                 t0=m["a"], t1=m["b"], layer=LAYER[m["template"]],
                                 driven_by=[dict(part=r["beat"], phrase=r["word"], t=r["t"]) for r in beats[it["id"]]["rows"] if r["word"]]))
            if m["template"] == "before-card":
                people, phys, src = who(it["id"], it, facts)
                pictures.append(dict(id=it["id"] + "-photo", in_graphic=it["id"], t0=m["a"], t1=m["b"], kind="photo",
                                     sources=[dict(path=cfg["photo"], src_in=0.0)], label_kind=label_kind(cfg.get("label")),
                                     label=cfg.get("label"), label_source="plan_resolved.json label (the editor's record)",
                                     people=people, physique=phys, people_source=src, approved_crop=None))
        elif k == "title":
            cfg = dict(eyebrow=it.get("eyebrow") or f"WAY {it['step']} OF {ntitles}", headline=it["headline"], step=it["step"], start=it["start"])
            graphics.append(dict(id=it["id"], template="softblue:title_card", config=cfg, text=[cfg["eyebrow"]] + it["headline"].split("\n"),
                                 t0=it["t0"], t1=it["t1"], layer="full", driven_by=[dict(part="in", phrase=it["start"], t=it["t0"])]))
        elif k == "scene":
            cfg = {x: it[x] for x in it if x not in ("id", "kind", "t0", "t1", "end", "pad_to_next", "note")}
            txt = [s for key in ("eyebrow", "headline", "detail") for s in ([it[key]] if isinstance(it.get(key), str) else [])] + list(it.get("items") or [])
            txt = [s for t_ in txt for s in t_.split("\n")]
            graphics.append(dict(id=it["id"], template="softblue:" + it["scene"], config=cfg, text=txt, t0=it["t0"], t1=it["t1"],
                                 layer="full", driven_by=[dict(part="in", phrase=it["start"], t=it["t0"])]))
        elif k in ("clip", "phone", "ai"):
            n = int(round(it["t1"] * FPS)) - int(round(it["t0"] * FPS))
            per = n // len(it["src"])
            srcs, lib_id = [], None
            for j, sp in enumerate(it["src"]):
                if sp.startswith("/"):
                    path, st = sp.split("@")[0], float(sp.split("@")[1]) if "@" in sp else 0.0
                else:
                    lib_id = sp.split("@")[0]
                    hits = sorted(glob.glob(f"{LIB}/*/*/{lib_id}_*") + glob.glob(f"{LIB}/*/*/*/{lib_id}_*"))
                    if not hits:
                        raise SystemExit(f"{it['id']}: library clip {lib_id} not found under {LIB}")
                    path, st = hits[0], float(sp.split("@")[1]) if "@" in sp else 0.0
                srcs.append(dict(path=path, src_in=st, frames=per if j < len(it["src"]) - 1 else n - per * (len(it["src"]) - 1)))
            people, phys, src = who(it["id"], it, facts, lib_id)
            pictures.append(dict(id=it["id"], t0=it["t0"], t1=it["t1"], kind="phone" if k == "phone" else "clip", sources=srcs,
                                 label_kind=label_kind(it.get("label")), label=it.get("label"),
                                 label_source="plan_resolved.json label (the editor's record)", people=people, physique=phys,
                                 people_source=src, approved_crop=None, library_id=lib_id, zoom=it.get("zoom", 1.0),
                                 clean_until=it.get("max_len"), note=it.get("note")))
    audio = dict(mix=master, untreated=master + ".untreated.wav", gate_stamp=master + ".audio_gate.json",
                 chain=master + ".voice_chain.json", music=None)
    dec = sorted(glob.glob(os.path.join(B, "round*-plan", "decisions.json")))
    D = json.load(open(dec[-1])) if dec else {}
    approvals = dict(status="approved" if a.approved else "pending", round=D.get("round"), source=dec[-1] if dec else None,
                     full_film=a.approved or None,
                     decisions=[{k: d.get(k) for k in ("id", "verdict", "dan", "scope") if d.get(k) is not None} for d in D.get("decisions", [])])
    inputs = {f: sha(os.path.join(B, f)) for f in ("edl.json", "shots.json", "plan_resolved.json", "words_out.json", "hf/manifest.json")
              if os.path.exists(os.path.join(B, f))}
    inputs[os.path.basename(master) + ".build.json"] = sha(master + ".build.json")
    return dict(video=V, grade=grade, edl=edl, framing=fr_rows, words=words, graphics=graphics, pictures=pictures, audio=audio,
                approvals=approvals, inputs=inputs)


# ------------------------------------------------------------------------------------------------ adkit family (RA-01)
def from_adkit(B, a, facts):
    import numpy as np
    L = load_py(os.path.join(B, "ra01lib.py"), "ra01lib_recipe")
    master = os.path.abspath(a.master or os.path.join(B, "master_16x9.mp4"))
    roll = os.path.splitext(os.path.basename(L.ROLL))[0]
    V = video_block(master, {roll: L.ROLL})
    cut = json.load(open(os.path.join(B, "cut.json")))
    bt = json.load(open(os.path.join(B, "beats.json")))
    tl = json.load(open(os.path.join(B, "timeline_16x9.json")))["items"]
    fm = json.load(open(os.path.join(B, "framing.json")))
    gr = json.load(open(os.path.join(B, "grade.json")))
    # picture/audio segments: the cut's pieces on the frame grid; the last one runs to the end hold
    edl, prev = [], 0
    P = cut["pieces"]
    for i, p in enumerate(P):
        f1 = int(round(p["t_out"] * FPS)) if i < len(P) - 1 else V["frames"]
        n = f1 - prev
        edl.append(dict(roll=roll, src_f0=int(round(p["src_in"] * FPS)), src_in=p["src_in"], src_out=round(p["src_in"] + n / FPS, 5),
                        out_f0=prev, out_f1=f1, out_in=round(prev / FPS, 5), out_out=round(f1 / FPS, 5), shot=f"{p['range']}.{i}",
                        audio="sync", join="first" if not i else "cut"))
        prev = f1
    dan = [x for x in tl if x["kind"] == "dan"]
    fr_rows = []
    for s in edl:
        d = min(dan, key=lambda x: abs((x["a"] + x["b"]) / 2 - (s["out_in"] + s["out_out"]) / 2))
        sm = [x for x in fm["samples"] if s["src_in"] - 0.3 <= x["src"] <= s["src_out"] + 0.3] or \
            sorted(fm["samples"], key=lambda x: abs(x["src"] - s["src_in"]))[:3]
        lvl = next((p["level"] for p in bt["punch"] if p["beat"][0] <= d["a"] + 1e-3 < p["beat"][1]), "NEAR")
        fr_rows.append(dict(name=lvl, crop=list(d["crop"]),
                            head=dict(hair_top=min(x["hair"] for x in sm), cx=float(np.median([x["cx"] for x in sm])),
                                      chin=float(np.median([x["chin"] for x in sm])), samples=len(sm)),
                            measured="the build's framing.json (5 fps on the raw roll: hair, cx, chin)"))
    grade = dict(filter=gr["filter"], lut=gr.get("lut"), decode="bt709", order="at_source_size", note=gr.get("_rule", ""))
    wa = json.load(open(os.path.join(B, "words_aligned.json")))["words"]
    words = dict(list=[dict(w=w["w"], t0=w["t"], t1=w["e"]) for w in wa], timing="ctc", fixes=[])
    graphics, pictures = [], []
    chips = {"ai": getattr(L, "CHIP_AI", "AI-GENERATED"), "real": getattr(L, "CHIP_REAL", REAL_CHIP)}
    for c in bt["cards"]:
        t0, t1 = c["beat"]
        src = L.ASSETS[c["asset"]]
        isdan = c["asset"] != "macro"
        lk = c["chip"] or "none"
        if c["kind"] == "before":
            lk = "real"
        pictures.append(dict(id=c["name"], t0=t0, t1=t1, kind="clip" if src.lower().endswith(".mp4") else "photo",
                             sources=[dict(path=src, src_in=bt.get("macro_slice", {}).get("in", 0.0) if c["asset"] == "macro" else 0.0)],
                             label_kind=lk if isdan else "none", label=chips.get(lk) if isdan and lk != "none" else None,
                             label_source="beats.json cards[].chip + ra01lib.ASSETS (the editor's record)",
                             people="dan" if isdan else "none", physique=isdan, people_source="ra01lib.ASSETS", approved_crop=None,
                             card_kind=c["kind"]))
        graphics.append(dict(id="card-" + c["name"], template="adkit:" + c["kind"], config=dict(card=c, asset=src),
                             text=[], t0=t0, t1=t1, layer="full", driven_by=[]))
    for k, (t0, t1) in enumerate(bt.get("cta", [])):
        graphics.append(dict(id=f"cta{k + 1}", template="adkit:cta_pill", config=dict(beat=[t0, t1]), text=[], t0=t0, t1=t1,
                             layer="overlay", driven_by=[]))
    audio = dict(mix=master, untreated=os.path.join(B, "cut_audio.wav"), gate_stamp=master + ".audio_gate.json",
                 chain=os.path.join(B, "mix.wav.voice_chain.json"), music=(sorted(glob.glob(os.path.join(B, "music", "*"))) or [None])[0])
    approvals = dict(status="approved" if a.approved else "pending", round=3, source=os.path.join(B, "notes-RA-01.md"),
                     full_film=a.approved or None, decisions=[])
    inputs = {f: sha(os.path.join(B, f)) for f in ("cut.json", "beats.json", "timeline_16x9.json", "framing.json", "grade.json")}
    return dict(video=V, grade=grade, edl=edl, framing=fr_rows, words=words, graphics=graphics, pictures=pictures, audio=audio,
                approvals=approvals, inputs=inputs)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("build")
    ap.add_argument("--master"); ap.add_argument("--out"); ap.add_argument("--facts")
    ap.add_argument("--job"); ap.add_argument("--title"); ap.add_argument("--type", choices=["LFC", "SFC", "AD"])
    ap.add_argument("--approved", help="Dan's words approving the finished film (sets approvals.status approved)")
    ap.add_argument("--work", help="scratch dir for the head measurement frames (default: beside the sheet)")
    a = ap.parse_args()
    B = os.path.abspath(a.build)
    facts = json.load(open(a.facts)) if a.facts else {}
    fam = "round" if os.path.exists(os.path.join(B, "plan_resolved.json")) else ("adkit" if os.path.exists(os.path.join(B, "cut.json")) else None)
    if fam is None:
        raise SystemExit(f"{B}: neither a round-method build (plan_resolved.json) nor an adkit build (cut.json)")
    out_default = None
    a.work = a.work or os.path.join(os.path.dirname(os.path.abspath(a.out)) if a.out else B, "_sheet_work")
    body = (from_round if fam == "round" else from_adkit)(B, a, facts)
    job = a.job or os.path.basename(B).upper().replace("RO", "RO-").replace("RA", "RA-").replace("--", "-")
    title = a.title
    if not title:
        m = re.search(r'RO-?\d+[^"\n]*?"([^"]+)"', open(os.path.join(os.path.dirname(body["video"]["master"]), "ROUND-2-REVIEW.md")).read()) \
            if os.path.exists(os.path.join(os.path.dirname(body["video"]["master"]), "ROUND-2-REVIEW.md")) else None
        title = m.group(1) if m else job
    inputs = body.pop("inputs")
    S = dict(schema=validate.SCHEMA, job=job, title=title, type=a.type or ("AD" if fam == "adkit" or job.startswith("RA") else "LFC"),
             editor="claude", **body,
             provenance=dict(written=time.strftime("%Y-%m-%dT%H:%M:%S"), by="sheet_from_claude_build.py (" + fam + " family)",
                             build_dir=B, inputs=inputs))
    E = validate.check(S, do_hash=False)
    out = a.out or (body["video"]["master"][:-4] + ".edit-sheet.json")
    if E:
        json.dump(S, open(out + ".INCOMPLETE.json", "w"), indent=1)
        print(f"EDIT SHEET INCOMPLETE ({len(E)}), written for inspection to {out}.INCOMPLETE.json")
        for e in E[:60]:
            print("  -", e)
        return 1
    json.dump(S, open(out, "w"), indent=1)
    print(f"{out}: {len(S['edl'])} segments, {len(S['words']['list'])} words, {len(S['graphics'])} graphics, "
          f"{len(S['pictures'])} pictures, approvals {S['approvals']['status']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
