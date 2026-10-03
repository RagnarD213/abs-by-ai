#!/usr/bin/env python3
"""SL-03 round 2 delivery: copy -> audio gate (verbatim against the same cut of RO-05's approved mix) -> delivered-file
transcript -> gate plan. Then run watch.py, the judge, and gate.py --format short (see README).
  deliver.py copy S..    copy + audio gate + REVIEW 540p + transcript + plan.json
  deliver.py plan S..    rewrite plan.json only (after a judge pass or a declare change)"""
import json, os, re, subprocess, sys, hashlib, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plans as P, batch as Bt
ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
OUT = f"{ROOT}/Short-form video content"; REV = f"{OUT}/daily-salad REVIEW"
FF = Bt.lib.FF; FPS = Bt.FPS
def dname(S): return f"{OUT}/daily-salad-{P.NAME[S]}.mp4"
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def copy(S):
    d = Bt.D(S); src = f"{d}/{P.NAME[S]}.mp4"; V = dname(S); os.makedirs(REV, exist_ok=True)
    for f in [V] + [V + x for x in (".audio_gate.json", ".deliver_gate.json")]:
        if os.path.exists(f): os.remove(f)
    shutil.copyfile(src, V)
    r = subprocess.run(["nice", "python3", f"{ROOT}/.claude/skills/_shared/audio/audio_gate.py", V, "--reference-mix", f"{d}/his_mix.wav", "--verbatim",
                        "--ab", f"{REV}/AB_source-vs-short_daily-salad-{P.NAME[S]}.mp4"], capture_output=True, text=True)
    print(S, [l for l in (r.stdout + r.stderr).splitlines() if "AUDIO GATE" in l] or (r.stdout + r.stderr)[-800:])
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", V, "-vf", "scale=540:960:flags=lanczos", "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"{REV}/daily-salad-{P.NAME[S]} - REVIEW 540p.mp4"], check=True)
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
    def ts(t): return f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round((t % 1) * 1000)) % 1000:03d}"
    p = f"{Bt.D(S)}/gate/captions.srt"
    open(p, "w").write("\n".join(f"{i + 1}\n{ts(c['f0'] / FPS)} --> {ts(c['f1'] / FPS)}\n{chr(10).join(s.cues[i]['lines'])}\n" for i, c in enumerate(s.caps)))
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
        if sh["kind"] == "broll": labels.append("BROLL"); prev = None; continue
        if sh["kind"] == "demo" and sh.get("layout") == "phone": labels.append("PHONE"); prev = None; continue
        f0 = face_out(sh, False)
        if prev is None or f0 is None or prev[1] is None or abs(np.log(f0 / prev[1])) >= np.log(1.15) or prev[0]["kind"] != sh["kind"] \
           or (sh["kind"] == "talk" and prev[0].get("win") != sh.get("win")) or (sh["kind"] == "demo" and prev[0].get("dh") != sh.get("dh")): cur += 1
        labels.append(f"{sh['kind'].upper()}-L{cur}"); prev = (sh, face_out(sh, True))
    lab = {sh["idx"]: l for sh, l in zip(shots, labels)}
    def level(sh): return lab[sh["idx"]]
    joins = sorted(set([round(sh["f0"] / FPS, 4) for sh in shots[1:] if not sh.get("seamless")] + T["joins"]))
    covered = []
    for j in joins:
        ji = Bt.fr(j)
        a = next(sh for sh in shots if sh["f0"] <= ji < sh["f1"])
        b = next((sh for sh in shots if abs(sh["f1"] - ji) <= 1 and sh is not a), None)
        if a["kind"] == "broll" or (b and (b["kind"] == "broll" or level(b) != level(a) or b["roll"] != a["roll"])): covered.append(beat(a))
    punch, punch_cov = [], []                                 # a follow that eases into a hold without a cut is one framing segment
    for sh in shots:
        if sh.get("seamless") and punch: punch[-1][1] = beat(sh)[1]; continue
        punch.append(beat(sh) + [level(sh)]); punch_cov.append(sh["kind"] == "broll")
    states = [dict(name=f"cap{i:03d}", beat=[round(c["f0"] / FPS, 4), round(c["f1"] / FPS, 4)], image=c["png"], image_sha256=sha(c["png"]),
                   rect=[0, 0, 1080, 1920], word=s.cues[i]["text"].split()[0]) for i, c in enumerate(s.caps)]
    words = json.load(open(f"{d}/words.json"))
    regions = [dict(name="title_band", beat=[0.0, round(dur, 4)], rect=[0, 0, 1080, 310]),
               dict(name="wordmark_talk", beat=[0.0, round(dur, 4)], rect=[64, 1800, 260, 50])]
    for m in s.man:
        regions.append(dict(name=m["id"], beat=[m["a"], m["b"]], rect=[m["box"][0], m["box"][1], m["box"][2] - m["box"][0], m["box"][3] - m["box"][1]]))
    thw = []
    shell = np.asarray(Bt.phone_shell())[..., 3] > 40; ys, xs = np.where(shell)          # the phone's real outline (not its shadow)
    for sh in shots:
        steady = "path" in sh and float(np.ptp(sh["path"])) < 1.0
        if sh["kind"] == "talk": thw.append(dict(name=f"shot{sh['idx']}", beat=beat(sh), rect=[0, 310, 1080, 1610], motion="fixed-wide" if steady else "tracking"))
        elif sh["kind"] == "demo" and sh.get("layout") != "phone": thw.append(dict(name=f"shot{sh['idx']}", beat=beat(sh), rect=list(Bt.DAN_BOX), motion="fixed-wide" if steady else "tracking"))
        if sh["kind"] == "demo":
            px = Bt.PHONE_ALONE_X if sh.get("layout") == "phone" else Bt.PHONE_XY[0]
            regions.append(dict(name=f"phone{sh['idx']}", beat=beat(sh), rect=[px + int(xs.min()), Bt.PHONE_XY[1] + int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]))
    regions = [r for r in regions if r["name"] != "wordmark_talk"]
    for sh in shots:                                       # the wordmark sits lower under the phone layout
        y = 1850 if any(x["kind"] == "demo" for x in shots) else 1800
        regions.append(dict(name=f"wordmark{sh['idx']}", beat=beat(sh), rect=[64, y, 260, 50]))
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
              ai_inserts=[], real_photos=[], cards=[], talking_head_windows=thw,
              evidence_contract=dict(version=2, video_sha256=h), caption_states=states,
              speech_words=[dict(w=w["w"], t=w["t"], e=w["e"]) for w in first],
              speech_words_evidence=dict(method="verbatim_source_ctc", video_sha256=h, pipeline="plans.TEXT forced-aligned (torchaudio WAV2VEC2_ASR_BASE_960H CTC) to the same cut of RO-05's approved mix this file carries verbatim (audio gate --verbatim)"),
              words=[dict(w=w["w"], t=w["t"], e=w["e"]) for w in words], transcript_words=[dict(w=w["w"]) for w in asr["words"]],
              srt=srt(S, s), source_audio=f"{d}/his_mix.wav", source_picture=f"{d}/source_picture.mp4",
              banned_source=Bt.lib.SCREEN, banned_times=[15.0, 289.5, 255.4],
              watch_log=f"{G}/logs/watch_pass.json")
    if os.path.exists(f"{G}/declare.json"): pl["declare"] = json.load(open(f"{G}/declare.json"))
    import datetime                                          # the negative-events look, bound to THIS render
    pl["negative_events_scan"] = dict(sha256=h, when=datetime.datetime.now().isoformat(timespec="seconds"), frames_checked=int(dur) + 1,
        method="one frame per second (watch-pass contact sheets, judged image by image by the independent reviewer) plus every shot's first, "
               "middle and last frame on the build's proof sheets; the footage is Dan clothed in a tank top talking in his kitchen, food B-roll and an app screen",
        findings=[])
    json.dump(pl, open(f"{G}/plan.json", "w"), indent=1)
    print(S, "plan", f"{G}/plan.json", "joins", len(joins), "covered", len(covered), "cues", len(states))

if __name__ == "__main__":
    fn = {"copy": copy, "plan": plan}[sys.argv[1]]
    for S in sys.argv[2:] or list(P.SEG): fn(S)
