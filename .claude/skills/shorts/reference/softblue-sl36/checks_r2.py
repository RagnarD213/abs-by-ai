#!/usr/bin/env python3
"""SL-36 R2 exact-file checks on each draft (first vertical review): sha, ffprobe, audio gate --verbatim against the same cut of the
approved film mix, seamscan on every audio join, delivered-file transcript vs the burned captions, talking-picture frame continuity
(source frame index steps by exactly 1 inside every talking shot), and the vertical hair check (run separately: haircheck_v.py S).
Measurements only: none of this is a listening pass. Writes build/S/checks_r2.json."""
import json, os, subprocess, sys, hashlib, numpy as np
sys.path.insert(0, "recipe")
import plans as P, batch as Bt
import importlib.util as _iu
_sp = _iu.spec_from_file_location('sl36_deliver', 'recipe/deliver.py'); Dl = _iu.module_from_spec(_sp); _sp.loader.exec_module(Dl)
ROOT = "/Users/danrrose/Projects/Claude/Projects/Abs By AI"; FP = ROOT + "/Media/video_edit/bin/ffprobe"
for S in sys.argv[1:]:
    d = Bt.D(S); V = f"{d}/{P.NAME[S]}.mp4"; T = json.load(open(f"{d}/timeline.json")); out = dict(file=V, sha256=Dl.sha(V))
    pr = json.loads(subprocess.run([FP, "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate,nb_frames,sample_rate,channels:format=duration", "-of", "json", V], capture_output=True, text=True).stdout)
    out["probe"] = pr
    r = subprocess.run(["nice", "python3", f"{ROOT}/.claude/skills/_shared/audio/audio_gate.py", V, "--reference-mix", f"{d}/his_mix.wav", "--verbatim", "--ab", f"{d}/AB_film-vs-draft.mp4"], capture_output=True, text=True)
    out["audio_gate"] = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()][-25:]
    subprocess.run([Bt.lib.FF, "-v", "error", "-y", "-i", V, "-vn", "-c:a", "pcm_s16le", f"{d}/draft_audio.wav"], check=True)
    json.dump(T["joins"], open(f"{d}/joins.json", "w"))
    r = subprocess.run(["python3", f"{ROOT}/.claude/skills/_shared/audio/seamscan.py", f"{d}/draft_audio.wav", "--joins", f"{d}/joins.json", "--out", f"{d}/seamscan.json"], capture_output=True, text=True)
    out["seamscan"] = (r.stdout + r.stderr).strip().splitlines()[-20:]
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): Dl.transcript(S, V)
    out["transcript_vs_captions"] = buf.getvalue().strip()
    shots = json.load(open(f"{d}/shots.json")); s = Bt.Short(S); steps = []
    for sh in shots:
        if sh["kind"] != "talk": continue
        idx = [s.fidx(sh, x) for x in sh["raw"]]; dif = np.diff(idx)
        steps.append(dict(shot=sh["idx"], frames=len(idx), bad=[int(i) for i in np.where(dif != 1)[0]]))
    s.close(); out["talk_frame_steps"] = steps
    json.dump(out, open(f"{d}/checks_r2.json", "w"), indent=1)
    print(S, out["sha256"][:12], "| audio:", [l for l in out["audio_gate"] if "AUDIO GATE" in l], "| steps bad:", sum(len(x["bad"]) for x in steps), "|", out["transcript_vs_captions"][:300])
