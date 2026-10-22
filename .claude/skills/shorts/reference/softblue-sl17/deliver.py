#!/usr/bin/env python3
"""SL-17 delivery (from SL-15) (from softblue-sl07 deliver.py): copy -> audio gate (verbatim against the same cut of RO-26's approved mix (plus, in short A, the raw meal-prep line through the film's fixed voice chain)) -> delivered-file
transcript -> gate plan. Then run watch.py, the judge, and gate.py --format short (see README).
  deliver.py copy S..    copy + audio gate + REVIEW 540p + transcript + plan.json
  deliver.py plan S..    rewrite plan.json only (after a judge pass or a declare change)"""
import json, os, re, subprocess, sys, hashlib, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plans as P, batch as Bt
ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
OUT = f"{ROOT}/Short-form video content"; REV = f"{OUT}/top1 REVIEW"; PRE = "top1-"
FF = Bt.lib.FF; FPS = Bt.FPS
def dname(S):
    """a short whose opening line is still the desk-mic recording is NOT a delivery: its name says so (VIDEO-RULES 2026-10-13)"""
    return f"{OUT}/{PRE}{P.NAME[S]}" + (" PLACEHOLDER PICKUP" if P.PICKUP.get(S, {}).get("placeholder") else "") + ".mp4"
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def copy(S):
    d = Bt.D(S); src = f"{d}/{P.NAME[S]}.mp4"; V = dname(S); os.makedirs(REV, exist_ok=True)
    for f in [V] + [V + x for x in (".audio_gate.json", ".deliver_gate.json")]:
        if os.path.exists(f): os.remove(f)
    shutil.copyfile(src, V)
    r = subprocess.run(["nice", "python3", f"{ROOT}/.claude/skills/_shared/audio/audio_gate.py", V, "--reference-mix", f"{d}/his_mix.wav", "--verbatim",
                        "--ab", f"{REV}/AB_film-vs-short_{os.path.basename(V)[:-4]}.mp4"], capture_output=True, text=True)
    print(S, [l for l in (r.stdout + r.stderr).splitlines() if "AUDIO GATE" in l] or (r.stdout + r.stderr)[-800:])
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", V, "-vf", "scale=540:960:flags=lanczos", "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"{REV}/{os.path.basename(V)[:-4]} - REVIEW 540p.mp4"], check=True)
    transcript(S, V); plan(S)

def transcript(S, V):
    """what the finished file says: local Whisper (small.en) on the delivered audio."""
    import whisper, numpy as np
    d = Bt.D(S); a = subprocess.run([FF, "-v", "error", "-i", V, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(a, "<i2").astype(np.float32) / 32768
    r = whisper.load_model("small.en").transcribe(x, fp16=False, condition_on_previous_text=False, word_timestamps=True)
    ws = [dict(w=w["word"].strip(), t=round(w["start"], 3), e=round(w["end"], 3)) for s in r["segments"] for w in s["words"]]
    json.dump(dict(sha256=sha(V), words=ws, text=r["text"]), open(f"{d}/delivered_asr.json", "w"))
    import difflib
    nz = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    cap = [nz(w["w"]) for w in json.load(open(f"{d}/words.json"))]; got = [nz(w["w"]) for w in ws]
    sm = difflib.SequenceMatcher(None, cap, got, autojunk=False)
    diffs = [(op, " ".join(cap[a0:a1]), " ".join(got[b0:b1])) for op, a0, a1, b0, b1 in sm.get_opcodes() if op != "equal"]
    print(S, "caption text vs delivered transcript:", f"{sm.ratio():.3f}", diffs)

def srt(S, s):
    """the burned captions as an .srt (same cues, same times) for the gate's caption rows."""
    def ts(t): m = int(round(t * 1000)); return f"{m // 3600000:02d}:{m % 3600000 // 60000:02d}:{m % 60000 // 1000:02d},{m % 1000:03d}"      # round the whole time: 32.9997 s is 33,000, not 32,000
    p = f"{Bt.D(S)}/gate/captions.srt"
    open(p, "w").write("\n".join(f"{i + 1}\n{ts(c['f0'] / FPS)} --> {ts(max(c['f1'], c['f0'] + 2) / FPS)}\n{chr(10).join(s.cues[i]['lines'])}\n" for i, c in enumerate(s.caps)))
    return p

def plan(S):
    d = Bt.D(S); V = dname(S); h = sha(V); T = json.load(open(f"{d}/timeline.json")); s = Bt.Short(S); G = f"{d}/gate"; os.makedirs(G, exist_ok=True)
    dur = T["frames"] / FPS
    beat = lambda sh: [round(sh["f0"] / FPS, 4), round(sh["f1"] / FPS, 4)]
    import numpy as np
    shots = s.shots
    def face_out(sh, at_end):
        """Dan's face width on the delivered frame at the shot's first or last 0.3 s (track.json, measured)."""
        trk = [r for r in s.track.get(s.key(sh), []) if "fw" in r]
        if not trk: return None
        t = sh["raw1"] if at_end else sh["raw0"]; near = [r["fw"] for r in trk if abs(r["t"] - t) <= 0.35] or [min(trk, key=lambda r: abs(r["t"] - t))["fw"]]
        scale = (1080 / sh["cw"]) if sh["kind"] == "talk" else (Bt.DAN_BOX[2] / sh["cw"])
        return float(np.median(near)) * scale
    labels, prev, cur = [], None, 0
    for sh in shots:          # a new framing label only where the face really changes size (>= 1.15x) or the picture changes kind
        if sh["kind"] in ("clip", "scene"): labels.append("BROLL"); prev = None; continue        # a clip or a rebuilt film graphic: no presenter framing
        if sh["kind"] == "phone": labels.append("PHONE"); prev = None; continue                     # the phone beside Dan: its own composition
        f0 = face_out(sh, False)
        if prev is None or f0 is None or prev[1] is None or abs(np.log(f0 / prev[1])) >= np.log(1.15) or prev[0]["kind"] != sh["kind"] \
           or (sh["kind"] == "talk" and prev[0].get("win") != sh.get("win")): cur += 1
        labels.append(f"{sh['kind'].upper()}-L{cur}"); prev = (sh, face_out(sh, True))
    lab = {sh["idx"]: l for sh, l in zip(shots, labels)}
    def level(sh): return lab[sh["idx"]]
    joins = sorted(set([round(sh["f0"] / FPS, 4) for sh in shots[1:] if not sh.get("seamless")] + T["joins"]))
    covered = []
    for j in joins:
        ji = Bt.fr(j)
        a = next(sh for sh in shots if sh["f0"] <= ji < sh["f1"])
        b = next((sh for sh in shots if abs(sh["f1"] - ji) <= 1 and sh is not a), None)
        if a["kind"] != "talk" or (b and (b["kind"] != "talk" or level(b) != level(a) or b["roll"] != a["roll"])): covered.append(beat(a))
    punch, punch_cov = [], []                                 # a follow that eases into a hold without a cut is one framing segment
    for sh in shots:
        if sh.get("seamless") and punch: punch[-1][1] = beat(sh)[1]; continue
        punch.append(beat(sh) + [level(sh)]); punch_cov.append(sh["kind"] != "talk")
    states = [dict(name=f"cap{i:03d}", beat=[round(c["f0"] / FPS, 4), round(c["f1"] / FPS, 4)], image=c["png"], image_sha256=sha(c["png"]),
                   rect=[0, 0, 1080, 1920], word=s.cues[i]["text"].split()[0]) for i, c in enumerate(s.caps)]
    words = json.load(open(f"{d}/words.json"))
    regions = [dict(name="title_band", beat=[0.0, round(dur, 4)], rect=[0, 0, 1080, 310]),
               dict(name="wordmark_talk", beat=[0.0, round(dur, 4)], rect=[64, 1800, 260, 50])]
    for m in s.man:
        regions.append(dict(name=m["id"], beat=[m["a"], m["b"]], rect=[m["box"][0], m["box"][1], m["box"][2] - m["box"][0], m["box"][3] - m["box"][1]]))
    # the rebuilt film graphics (scenes.py) are drawn above canvas y 1380 and leave the caption band (from 1412) clear, so captions run
    # over them as RA-14 approved: they are graphic regions (the gate measures caption clearance), not full-screen cards
    # the real-photo displays (scenes.py) are pictures, like B-roll: captions run over the photo's lower edge; their chip and tabs are regions (below)
    thw = []
    shell = np.asarray(Bt.phone_shell())[..., 3] > 40; ys, xs = np.where(shell)          # the phone's real outline (not its shadow)
    for sh in shots:
        steady = "path" in sh and float(np.ptp(sh["path"])) < 1.0
        if sh["kind"] == "talk": thw.append(dict(name=f"shot{sh['idx']}", beat=beat(sh), rect=[0, 310, 1080, 1610], motion="fixed-wide" if steady else "tracking"))
        elif sh["kind"] == "phone":
            thw.append(dict(name=f"shot{sh['idx']}", beat=beat(sh), rect=list(Bt.DAN_BOX), motion="fixed-wide" if steady else "tracking"))
            regions.append(dict(name=f"phone{sh['idx']}", beat=beat(sh), rect=[Bt.PHONE_XY[0] + int(xs.min()), Bt.PHONE_XY[1] + int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]))
    ai = []                                                 # AI clips (not of Dan): the AI-GENERATED chip is drawn on the frame at cover['ai']
    for sh in shots:
        if sh["kind"] == "clip" and sh["cover"].get("ai"):
            x0, y0 = sh["cover"]["ai"][:2]; cb = Bt.chip_png("AI-GENERATED", (x0, y0), u=sh["cover"]["ai"][2] if len(sh["cover"]["ai"]) > 2 else 2)[1]      # the chip's REAL box (it was declared 280 x 60 and drawn 505 x 80)
            ai.append(dict(name=sh["cover"]["id"], beat=beat(sh), pos=[x0, y0]))
            regions.append(dict(name=f"chip{sh['idx']}", beat=beat(sh), rect=[cb[0], cb[1], cb[2] - cb[0], cb[3] - cb[1]]))
    # captions:sync gets ONE delivered word per caption chunk, its first word (DS-17 method): matching chunk-first words
    # alone against every spoken word lands on the wrong repeat
    first, k = [], 0
    nz = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
    for c in s.cues:
        toks = [nz(t) for t in c["text"].split() if nz(t)]
        while k < len(words) and nz(words[k]["w"]) != toks[0]: k += 1
        assert k < len(words), (S, c["text"])
        first.append(words[k]); k += len(toks)
    asr = json.load(open(f"{d}/delivered_asr.json")); assert asr["sha256"] == h, "transcript is of another render"
    pl = dict(target_seconds=round(dur, 6), target_frames=T["frames"], joins=joins, covered=covered,
              punch=punch, punch_covered=punch_cov,
              graphics=[dict(name=m["id"], beat=[m["a"], m["b"]], mov=m["mov"]) for m in s.man], graphic_regions=regions,
              ai_inserts=ai, real_photos=[], cards=[], talking_head_windows=thw,
              evidence_contract=dict(version=2, video_sha256=h), caption_states=states,
              speech_words=[dict(w=w["w"], t=w["t"], e=w["e"]) for w in first],
              speech_words_evidence=dict(method="verbatim_source_ctc", video_sha256=h, pipeline="plans.TEXT forced-aligned (torchaudio WAV2VEC2_ASR_BASE_960H CTC) to the same cut of RO-26's approved mix (plus, in short A, the raw meal-prep line through the film's fixed voice chain) this file carries verbatim (audio gate --verbatim)"),
              words=[dict(w=w["w"], t=w["t"], e=w["e"]) for w in words], transcript_words=[dict(w=w["w"]) for w in asr["words"]],
              srt=srt(S, s), source_audio=f"{d}/his_mix.wav", source_picture=f"{d}/source_picture.mp4",
              banned_source=f"{ROOT}/Media/longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4", banned_times=[15.0, 289.5, 255.4],      # the recording that holds the banned app screens (softblue-sl03 lib.SCREEN)
              watch_log=f"{G}/logs/watch_pass.json")
    import scenes as Sc                                     # the real-photo displays (scenes.py): the chip is drawn above the card, centred at y 322
    from PIL import Image
    real = []
    for sh in shots:
        if sh["kind"] == "scene" and sh["cover"]["scene"] in ("photo1", "pair"):      # SL-17's group photo carries no chip (the film showed it without one: not a physique picture)
            txt = Sc.REAL1 if sh["cover"]["scene"] == "photo1" else Sc.REAL2
            rg, cb = Bt.chip_png(txt, (0, 0), u=Sc.CHIP_U); cw_ = cb[2] - cb[0]; p_ = f"{G}/real_chip_{sh['cover']['id']}.png"
            Image.fromarray(rg[cb[1]:cb[3], cb[0]:cb[2]]).save(p_); x_ = int(round(Bt.W / 2 - cw_ / 2)); y_ = Bt.DROP + 12
            real.append(dict(name=sh["cover"]["id"], beat=[round(sh["f0"] / Bt.FPS + 0.3, 4), round(sh["f1"] / Bt.FPS, 4)], chip=p_, pos=[x_, y_]))      # the chip appears 0.25 s into the scene
            regions.append(dict(name=f"chip_{sh['cover']['id']}", beat=beat(sh), rect=[x_, y_, cw_, cb[3] - cb[1]]))
            if sh["cover"]["scene"] == "pair": regions.append(dict(name="pair_tabs", beat=beat(sh), rect=[27, Sc.PAIR_Y + Sc.PAIR_H - 92, 1026, 62]))
    pl["real_photos"] = real
    rgba, cb = Bt.chip_png("AI-GENERATED", (0, 0), u=1.6); Image.fromarray(rgba[cb[1]:cb[3], cb[0]:cb[2]]).save(f"{G}/ai_chip.png")
    rg2, c2 = Bt.chip_png(Sc.REAL1, (0, 0), u=Sc.CHIP_U); Image.fromarray(rg2[c2[1]:c2[3], c2[0]:c2[2]]).save(f"{G}/real_chip.png")
    pl["label_chips"] = dict(ai=f"{G}/ai_chip.png", real=f"{G}/real_chip.png")
    if os.path.exists(f"{G}/declare.json"): pl["declare"] = json.load(open(f"{G}/declare.json"))
    import datetime                                          # the negative-events look, bound to THIS render
    pl["negative_events_scan"] = dict(sha256=h, when=datetime.datetime.now().isoformat(timespec="seconds"), frames_checked=int(dur) + 1,
        method="one frame per second (watch-pass contact sheets; " + (lambda w: f"judged image by image by {w['judged_by']}, {w.get('open_defects')} open defect(s)" if w.get("judged_by") and w.get("sha256") == h else "scanned by the builder only, the independent judge has not run on this file yet")(json.load(open(f"{G}/logs/watch_pass.json")) if os.path.exists(f"{G}/logs/watch_pass.json") else {}) + ") plus every shot's first, "
               "middle and last frame on the build's proof sheets; the footage is Dan in a black tank top talking in his studio, his own kitchen and pool "
               "B-roll, the film's approved food and AI clips (AI clip with the AI-GENERATED chip), his real black-belt promotion and group photo, "
               "and two Pexels martial-arts clips (Muay Thai bag work, a judo throw)",
        findings=[])
    json.dump(pl, open(f"{G}/plan.json", "w"), indent=1)
    print(S, "plan", f"{G}/plan.json", "joins", len(joins), "covered", len(covered), "cues", len(states))

if __name__ == "__main__":
    sys.path.insert(0, ROOT + "/.claude/skills/_shared"); import buildcap; buildcap.wait("SL-17 deliver " + " ".join(sys.argv[1:]))
    fn = {"copy": copy, "plan": plan}[sys.argv[1]]
    for S in sys.argv[2:] or list(P.SEG): fn(S)
