"""RO-03 edit sheet (schema abs-edit-sheet/1) for the RO-02 / RO-03 build family: several rolls, a crop MEASURED per shot
(frames.crop), one colour cube per exposure trim (frames.lut), PIL chips (gfx.title_chip, gfx.work_chip) beside the
HyperFrames lower thirds. The shared writer (_shared/edit-sheet/sheet_from_claude_build.py) reads a single-roll build or
RO-06's global-timeline build; this one reuses its measuring and validation code and copies every field from the build's
own files. Nothing is decided here.
usage: sheet.py MASTER.mp4 OUT.edit-sheet.json [--approved "Dan's words"]"""
import sys, os, json, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/edit-sheet"; sys.path.insert(0, SH)
import sheet_from_claude_build as SB, validate
import frames as F, edl as E, gfx as G
W = E.W; FPS = 30000/1001
ap = argparse.ArgumentParser(); ap.add_argument("master"); ap.add_argument("out"); ap.add_argument("--approved")
a = ap.parse_args(); master = os.path.abspath(a.master); od = os.path.dirname(master)
build = json.load(open(master + ".build.json")); segs = build["segments"]; S = {s["id"]: s for s in F.S}
plan = json.load(open(f"{W}/plan_resolved.json"))

rolls = {r: E.src(r) for r in sorted({S[s["shot"]]["roll"] for s in segs})}
V = SB.video_block(master, rolls); assert segs[-1]["o1"] == V["frames"], "build.json and the master disagree on length"
edl, crops, per_shot = [], [], {}
for i, s in enumerate(segs):
    sh = S[s["shot"]]; n = s["o1"] - s["o0"]; p = segs[i-1] if i else None
    join = "first" if not i else ("reframe" if S[p["shot"]]["roll"] == sh["roll"] and p["src0"] + (p["o1"] - p["o0"]) == s["src0"] else "cut")
    edl.append(dict(roll=sh["roll"], src_f0=s["src0"], src_in=round(s["src0"]/FPS, 5), src_out=round((s["src0"] + n)/FPS, 5),
                    out_f0=s["o0"], out_f1=s["o1"], out_in=round(s["o0"]/FPS, 5), out_out=round(s["o1"]/FPS, 5),
                    shot=s["shot"], audio="sync", join=join, covered=bool(s.get("covered")), side_card=s.get("card")))
    crops.append([int(v) for v in F.crop(sh, s["framing"], bool(s.get("card")))]); per_shot[s["shot"]] = dict(lut=F.lut(sh), pre_gamma=F.gamma(sh))
hc = json.load(open(f"{od}/logs/haircheck.json"))["rows"] if os.path.exists(f"{od}/logs/haircheck.json") else None
heads = SB.head_rows(edl, crops, rolls, f"{od}/_sheet_work", hc)
framing = [dict(name=s["framing"], crop=c, head=h, wall_stretch=False,
                measured="mediapipe face box + Apple Vision person mask on the raw roll (headmeasure.py)" + ("; hair top also from the dense haircheck.json on the master" if hc else ""))
           for s, c, h in zip(segs, crops, heads)]
grade = dict(filter="crop=<framing.crop>,scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,format=gbrpf32le,lut3d=file='<per_shot lut>':interp=tetrahedral",
             lut=None, per_shot=per_shot, look=F.LOOK, decode="bt709", order="after_scale_1080",
             note="recipe/frames.py vf(): crop, scale to 1920x1080 with a BT.709 decode, then that shot's cube (the approved poolside colour A after one exposure trim; the three sets share one trim)")

# words: the SRT's own list (srt_words.json applied), so the sheet and the captions agree
P = json.load(open(f"{od}/plan.json"))
words = dict(list=[dict(w=w["w"], t0=round(w["t"], 4), t1=round(w["e"], 4)) for w in P["words"]],
             timing="whisper medium.en on the assembled cut, carried through the shot map; srt_words.json rows applied",
             fixes=json.load(open(f"{od}/srt_words.json")) if os.path.exists(f"{od}/srt_words.json") else [])

man = {m["id"]: m for m in json.load(open(f"{W}/hf/manifest.json"))}; beats = {b["id"]: b for b in json.load(open(f"{W}/hf/beats.json"))}
graphics, pictures = [], []
for it in plan:
    k = it["kind"]
    if it["id"] in man:
        m = man[it["id"]]; cfg = json.load(open(f"{W}/hf/configs/{m['template']}/{it['id']}.json"))[0]
        graphics.append(dict(id=it["id"], template=m["template"], config=cfg, text=SB.texts_of(m["template"], cfg), t0=m["a"], t1=m["b"], layer="overlay",
                             driven_by=[dict(part=r["beat"], phrase=r["word"], t=r["t"]) for r in beats[it["id"]]["rows"] if r["word"]]))
    elif k == "wtitle":
        cfg = dict(fn="longform-edit/reference/ro03/gfx.py title_chip", xy=list(G.CHIP_XY), eyebrow=it["eyebrow"], headline=it["headline"], detail=it["detail"])
        graphics.append(dict(id=it["id"], template="softblue:title_chip", config=cfg, text=[it["eyebrow"], it["headline"], it["detail"]], t0=it["t0"], t1=it["t1"], layer="overlay", driven_by=[]))
    elif k == "work":
        lines = ["SET 1 OF 3: GET READY", "SET 1 OF 3: HOLD", "REST. SET 2 OF 3 IS NEXT", "SET 2 OF 3: HOLD", "REST. SET 3 OF 3 IS NEXT", "SET 3 OF 3: HOLD", "WORKOUT COMPLETE", "seconds", "sets done"]
        cfg = dict(fn="longform-edit/reference/ro03/gfx.py work_chip (states: work_state)", xy=list(G.CHIP_XY), holds=it["holds"], beeps=it["beeps"], secs=it["secs"], lines=lines)
        graphics.append(dict(id=it["id"], template="softblue:work_chip", config=cfg, text=lines, t0=it["t0"], t1=it["t1"], layer="overlay",
                             driven_by=[dict(part=f"hold {n+1}", phrase="phone timer start (marks.json)", t=h) for n, h in enumerate(it["holds"])] +
                                       [dict(part=f"beep {n+1}", phrase="phone timer beep, 3 kHz onset in the lav", t=b) for n, b in enumerate(it["beeps"])]))
    elif k == "clip":
        n = int(round(it["t1"]*FPS)) - int(round(it["t0"]*FPS)); sp = it["src"][0]
        pictures.append(dict(id=it["id"], t0=it["t0"], t1=it["t1"], kind="clip", sources=[dict(path=G.src_path(sp), src_in=G.src_start(sp), frames=n)],
                             label_kind="none", label=None, label_source="plan_resolved.json (no label: real moving footage of Dan, VIDEO-RULES 2026-09-16)",
                             people="dan", physique=False, people_source="the 16:9 session, after viewing the clip: this film's own live set (8/14 roll C1625)",
                             approved_crop=None, library_id=None, zoom=it.get("zoom", 1.0), note=it.get("note")))
    else: raise SystemExit(f"{it['id']}: kind {k} is not written by this sheet writer")
D = json.load(open(f"{W}/round2-plan/decisions.json"))
approvals = dict(status="approved" if a.approved else "pending", round=2, source=f"{W}/round2-plan/decisions.json", full_film=a.approved or None,
                 decisions=[dict(id=d["id"], verdict=d["verdict"], dan=d["dan_words"], **({"scope": d["scope"]} if d.get("scope") else {})) for d in D["items"]] +
                           [dict(id="answer: " + k, verdict="decided", dan=v) for k, v in D["answers"].items()] +
                           [dict(id="no other shoot", verdict="rule", dan=D["dan_reply_2"]["words"][1])])
inputs = {f: SB.sha(f"{W}/{f}") for f in ("edl.json", "shots.json", "plan_resolved.json", "words_out.json", "marks.json", "measure.json", "skin.json", "hf/manifest.json")}
inputs[os.path.basename(master) + ".build.json"] = SB.sha(master + ".build.json")
audio = dict(mix=master, untreated=f"{W}/film_untreated.wav", gate_stamp=master + ".audio_gate.json", chain=master + ".voice_chain.json",
             music=dict(bed=f"{W}/bed_full.wav", note="recipe/bed.py: the bed on the film timeline, a swell in each hold; levels locked in round 1"))
sheet = dict(schema=validate.SCHEMA, job="RO-03", title="The Vacuum: Workout Only", type="LFC", editor="claude", video=V, grade=grade, edl=edl, framing=framing,
             words=words, graphics=graphics, pictures=pictures, audio=audio, approvals=approvals,
             provenance=dict(written=time.strftime("%Y-%m-%dT%H:%M:%S"), by="longform-edit/reference/ro03/sheet.py (RO-02 / RO-03 family)", build_dir=W, inputs=inputs))
ERR = validate.check(sheet, do_hash=False)
if ERR:
    json.dump(sheet, open(a.out + ".INCOMPLETE.json", "w"), indent=1); print(f"EDIT SHEET INCOMPLETE ({len(ERR)})"); [print("  -", e) for e in ERR[:60]]; sys.exit(1)
json.dump(sheet, open(a.out, "w"), indent=1)
print(f"{a.out}: {len(edl)} segments, {len(words['list'])} words, {len(graphics)} graphics, {len(pictures)} pictures, approvals {approvals['status']}")
