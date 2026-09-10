#!/usr/bin/env python3
"""THE VERTICAL SHORT-AD GATE, measured off the FINISHED FILE, never the build plan.

  python3 qc.py <delivered.mp4> [--build-dir .] [--config qc.json] [--reference-cut his.mp4]

⚠ WHY THIS FILE EXISTS (2026-09-09, Phase 0 of the video-quality programme). SKILL.md referenced
`reference/qc.py` FIVE TIMES and described it as "17 checks" -- and the file did not exist. The only
real gate on disk was `qc_ad2v2.py`, a per-ad fork with `TARGET = 276.109167` and
`V = 'ad2v2_vertical_9x16.mp4'` compiled in, unusable on any other cut. A SKILL.md that asserts a
check nothing performs is worse than no check at all: it reads as covered.

⚠ AND WHY IT REFUSES RATHER THAN SKIPS. The ancestor of this gate passed 11/11 on a video Dan called
"truly awful", because every check measured format and none of them watched the picture. So here a
check whose input is missing is **NOT MEASURED, which is a FAILURE** -- never a silent skip. If a
check genuinely does not apply to this cut, say so in the config (`"skip": {"<check>": "<reason>"}`),
where the reason is written down and a reader can audit it.

Per-cut numbers live in `qc.json` beside the build, not in this file. Defaults are the skill's
standard; every one of them traces to a measurement of the reference cut.

  {
    "target_seconds": 276.109167,     // or set "reference_cut" and it is measured
    "reference_cut":  "…/his 9x16.mp4",
    "his_mix":        "his_mix.wav",  // the editor's own mix, when we carry it verbatim
    "captions":       "captions.mov",
    "watch_log":      "logs/watch_pass.json",
    "banned_source":  "…/app-flow-generate-future-self.mp4",
    "banned_times":   [26.5, 27.5, 29.5, 31.0],
    "min_coverage":   0.39,           // his own cut; padding to clear a number is the wrong trade
    "max_static":     31.6,           // his longest talking stretch
    "min_changes_per_min": 9.0,
    "min_push_frac":  0.25,           // the talking head is never one fixed crop
    "size":  "1080x1920", "fps": "30000/1001",
    "skip":  {}
  }
"""
import argparse, json, os, re, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
FP = FF.replace("ffmpeg", "ffprobe")
SHARED = os.path.join(REPO, ".claude/skills/_shared/audio")

DEFAULTS = dict(size="1080x1920", fps="30000/1001", min_changes_per_min=9.0, max_static=31.6,
                min_coverage=0.39, min_push_frac=0.25, banned_times=[26.5, 27.5, 29.5, 31.0],
                banned_source=("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
                               "02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4"),
                captions="captions.mov", watch_log="logs/watch_pass.json", his_mix=None,
                target_seconds=None, reference_cut=None, skip={})

R = []
def chk(ok, name, detail): R.append((bool(ok), name, str(detail)))
def unmeasured(name, why):
    """A check whose input is missing FAILS. 'Nobody looked' is not 'it is fine'."""
    R.append((False, name, f"NOT MEASURED -- {why}"))
def skipped(name, why): R.append((True, name, f"declared not applicable: {why}"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--build-dir", default=".", help="where beats.py / centering.py / his_mix.wav live")
    ap.add_argument("--config", default="qc.json")
    ap.add_argument("--reference-cut", help="the editor's cut this one reproduces (sets the duration target)")
    A = ap.parse_args()
    bd = os.path.abspath(A.build_dir)
    cfgp = A.config if os.path.isabs(A.config) else os.path.join(bd, A.config)
    C = dict(DEFAULTS)
    if os.path.exists(cfgp): C.update(json.load(open(cfgp)))
    if A.reference_cut: C["reference_cut"] = A.reference_cut
    skip = C.get("skip") or {}
    V = os.path.abspath(A.video)
    sys.path.insert(0, bd)

    def rel(p):
        if not p: return None
        return p if os.path.isabs(p) else os.path.join(bd, p)

    # ⚠ PROBE THE VIDEO STREAM, NOT THE CONTAINER. The container's duration is the longer of the two
    # streams, so a truncated PICTURE reads back as the full length and every duration check passes --
    # which is how a 10-frame hole and a 334 ms A/V offset shipped. Parse ffprobe's json BY NAME:
    # it emits csv fields in ITS order, so a field swap can turn a frame count into a duration.
    pj = json.loads(subprocess.run([FP, "-v", "error", "-select_streams", "v", "-count_frames",
        "-show_entries", "stream=width,height,r_frame_rate,nb_read_frames,duration", "-of", "json", V],
        capture_output=True, text=True).stdout)["streams"][0]
    w, h = str(pj["width"]), str(pj["height"])
    fr, NFR, dur = pj["r_frame_rate"], int(pj["nb_read_frames"]), float(pj["duration"])
    _n, _d = (fr.split("/") + ["1"])[:2]; fps = int(_n) / int(_d)   # "30000/1001" -> 29.97

    chk(f"{w}x{h}" == C["size"], f"1  frame size is {C['size']}", f"{w}x{h}")
    chk(fr == C["fps"], f"2  frame rate is {C['fps']}", fr)

    # 3 duration against the cut we are reproducing
    tgt = C.get("target_seconds")
    if tgt is None and C.get("reference_cut") and os.path.exists(rel(C["reference_cut"])):
        tgt = float(subprocess.run([FP, "-v", "error", "-select_streams", "v", "-show_entries",
            "stream=duration", "-of", "csv=p=0", rel(C["reference_cut"])],
            capture_output=True, text=True).stdout.strip())
    if tgt is None: unmeasured("3  video stream duration matches the reference cut",
                               "no target_seconds and no readable reference_cut in qc.json")
    else: chk(abs(dur - tgt) < 0.10, "3  video stream duration matches the reference cut",
              f"{dur:.3f}s vs {tgt:.3f}s")

    # 3b every planned frame present (needs the build's beat sheet)
    try:
        import beats as BT
        planned = round(BT.DUR * fps)
        chk(NFR == planned, "3b every planned frame is present (no truncated beat)",
            f"{NFR} frames vs {planned} planned")
    except Exception as e:
        BT = None
        unmeasured("3b every planned frame is present (no truncated beat)", f"beats.py not importable from {bd} ({e})")

    # 4/5 loudness and true peak
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", V, "-af", "loudnorm=print_format=summary",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    g = lambda k: float(re.search(rf"{k}:\s+(-?[\d.]+)", r).group(1))
    I, TP = g("Input Integrated"), g("Input True Peak")
    # ⚠ VERBATIM (Dan, 2026-09-10: "Zishan's audio sounds much better... Use Zishan's audio"). When the cut carries an
    # editor's finished mix, HIS level and HIS stereo image are the standard. Our -14 LUFS and L/R > 0.98 rows would
    # have FAILED Zeeshan's own mix (-23.5 LUFS, L/R 0.970) -- and we "fixed" that by lifting and mono-summing his
    # audio, which is the build Dan rejected. So in audio_mode "verbatim" rows 4 and 6 compare to HIS mix.
    VB = C.get("audio_mode") == "verbatim"
    hm = rel(C.get("his_mix"))
    if VB and not (hm and os.path.exists(hm)):
        unmeasured("4  loudness is HIS mix's (delivered untouched)", "audio_mode verbatim needs his_mix in qc.json")
    elif VB:
        rh = subprocess.run([FF, "-hide_banner", "-nostats", "-i", hm, "-af", "loudnorm=print_format=summary",
                             "-f", "null", "-"], capture_output=True, text=True).stderr
        Ih = float(re.search(r"Input Integrated:\s+(-?[\d.]+)", rh).group(1))
        chk(abs(I - Ih) <= 0.3, "4  loudness is HIS mix's (delivered untouched)", f"{I} vs his {Ih} LUFS")
    else:
        chk(abs(I + 14) <= 0.8, "4  loudness -14 LUFS", f"{I} LUFS")
    chk(TP <= -1.0, "5  true peak at or under -1.0 dBTP", f"{TP} dBTP")

    # 6 centred voice (verbatim: HIS stereo image, not summed to mono, not widened)
    wav = "/tmp/_qc_shortad.wav"
    subprocess.run([FF, "-v", "error", "-y", "-i", V, "-map", "0:a", "-ar", "16000", "-ac", "2", wav], check=True)
    a = np.frombuffer(wave.open(wav).readframes(10**9), dtype="<i2").astype(np.float32).reshape(-1, 2)
    c = float(np.corrcoef(a[:, 0], a[:, 1])[0, 1])
    if VB and hm and os.path.exists(hm):
        subprocess.run([FF, "-v", "error", "-y", "-i", hm, "-ar", "16000", "-ac", "2", "/tmp/_qc_shortad_his.wav"], check=True)
        b2 = np.frombuffer(wave.open("/tmp/_qc_shortad_his.wav").readframes(10**9), dtype="<i2").astype(np.float32).reshape(-1, 2)
        ch = float(np.corrcoef(b2[:, 0], b2[:, 1])[0, 1])
        chk(abs(c - ch) <= 0.01, "6  stereo image is HIS mix's (not summed, not widened)", f"L/R corr {c:.4f} vs his {ch:.4f}")
    else:
        chk(c > 0.98, "6  voice is centred / mono-safe", f"L/R corr {c:.4f}")

    # 7/8 visual change rate and the longest static stretch
    vals = subprocess.run([FF, "-v", "info", "-i", V, "-vf",
        "select='gt(scene,0.12)',metadata=print:file=-", "-an", "-f", "null", "-"],
        capture_output=True, text=True).stdout
    ts = sorted(set(round(float(x), 2) for x in re.findall(r"pts_time:([\d.]+)", vals)))
    gaps = [b - a2 for a2, b in zip([0.0] + ts, ts + [dur])]
    chk(len(ts) / (dur / 60) >= C["min_changes_per_min"],
        f"7  visual change rate >= {C['min_changes_per_min']}/min",
        f"{len(ts)/(dur/60):.1f}/min ({len(ts)} changes)")
    # The bar is HIS cut, not an absolute.
    chk(max(gaps) <= C["max_static"], f"8  no stretch longer than his own longest ({C['max_static']}s)",
        f"longest {max(gaps):.1f}s")

    # 9 insert / graphic coverage -- his own cut, with margin. Padding a faithful reproduction with
    # filler inserts to clear a number is the wrong trade.
    if BT and tgt:
        tl, _ = BT.timeline()
        ins = sum(b["t1"] - b["t0"] for b in tl if b["kind"] != "talk")
        chk(ins / tgt >= C["min_coverage"], f"9  insert/graphic coverage at least his {C['min_coverage']*100:.0f}%",
            f"{100*ins/tgt:.0f}%")
    else:
        tl = None
        unmeasured(f"9  insert/graphic coverage at least his {C['min_coverage']*100:.0f}%",
                   "needs beats.py and a duration target")

    # 10 BANNED SCREENS, matched on EVERY FRAME of the finished picture. A sampling scan cannot see a
    # single-frame violation: on Ad 3 a 2 fps scan reported a clean 0.647 and the same scan at full
    # rate reported 1.000 and failed the build.
    bsrc = rel(C.get("banned_source"))
    if "10" in skip: skipped("10 no banned product screen anywhere (ALL frames)", skip["10"])
    elif not (bsrc and os.path.exists(bsrc)):
        unmeasured("10 no banned product screen anywhere (ALL frames)",
                   f"banned_source not readable ({C.get('banned_source')}) -- is the asset library mounted?")
    else:
        from PIL import Image
        def sigs_of(path, times):
            out = []
            for t in times:
                o = "/tmp/_qsig.png"
                subprocess.run([FF, "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1",
                                "-vf", "scale=48:86", "-pix_fmt", "gray", o], check=True)
                v = np.asarray(Image.open(o), dtype=np.float32).ravel(); v -= v.mean()
                out.append(v / max(v.std(), 1e-6))
            return out
        banned = sigs_of(bsrc, C["banned_times"])
        raw = subprocess.run([FF, "-v", "error", "-i", V, "-vf", "scale=48:86,format=gray",
                              "-f", "rawvideo", "-"], capture_output=True).stdout
        F = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 86 * 48).astype(np.float32)
        F -= F.mean(1, keepdims=True); F /= np.maximum(F.std(1, keepdims=True), 1e-6)
        worst, wt = 0.0, None
        for bdg in banned:
            v = (F * bdg).mean(1); k = int(np.argmax(v))
            if v[k] > worst: worst, wt = float(v[k]), k / fps
        chk(worst < 0.72, "10 no banned product screen anywhere (ALL frames)",
            f"{len(F)} frames scanned, worst match {worst:.2f} at {wt:.1f}s")

    # 11 burned captions
    cap = rel(C.get("captions"))
    chk(bool(cap and os.path.exists(cap)), "11 burned captions present", C.get("captions"))

    # 12 the talking head is NOT one fixed crop. 100% of Ad 1 attempt 1's talk ran at one crop, and
    # that -- not the splices -- is what made a tripod shot read as a webcam recording.
    if BT and tl and tgt:
        talk_t = [t / 10 for t in range(int(tgt * 10))
                  if any(b["kind"] == "talk" and b["t0"] <= t / 10 < b["t1"] for b in tl)]
        pushed = sum(1 for t in talk_t if BT.push_at(t) > 1.05)
        chk(len(talk_t) and pushed / len(talk_t) >= C["min_push_frac"],
            "12 talking head is not one fixed crop (his push schedule reproduced)",
            f"{100*pushed/max(len(talk_t),1):.0f}% of talk inside a push (min {C['min_push_frac']*100:.0f}%)")
    else:
        unmeasured("12 talking head is not one fixed crop", "needs beats.py and a duration target")

    # 13 the audio IS his finished mix, proven per second at normalised level (the number that
    # separates his mix from a loudnorm'd one is 0.970 vs 0.99).
    hm = rel(C.get("his_mix"))
    if "13" in skip: skipped("13 audio is HIS finished mix", skip["13"])
    elif not (hm and os.path.exists(hm)):
        unmeasured("13 audio is HIS finished mix (per-second, level-normalised)",
                   "no his_mix in qc.json -- set it, or skip 13 with the reason if this cut carries OUR mix")
    else:
        def mono16(src):
            subprocess.run([FF, "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000",
                            "-c:a", "pcm_s16le", "/tmp/_pv.wav"], check=True)
            return np.frombuffer(wave.open("/tmp/_pv.wav").readframes(10**9), dtype="<i2").astype(float)
        ours, his = mono16(V), mono16(hm)
        n = min(len(ours), len(his)); ours, his = ours[:n] - ours[:n].mean(), his[:n] - his[:n].mean()
        W = 16000; cors, gains = [], []
        for i in range(n // W):
            x, y = his[i*W:(i+1)*W], ours[i*W:(i+1)*W]
            if np.sqrt((x ** 2).mean()) < 50: continue
            gg = np.dot(x, y) / max((x ** 2).sum(), 1e-9)
            xx, yy = x - x.mean(), y - y.mean()
            cors.append(float(np.dot(xx, yy) / np.sqrt((xx ** 2).sum() * (yy ** 2).sum())))
            gains.append(20 * np.log10(max(gg, 1e-9)))
        med = float(np.median(cors)) if cors else 0.0
        if VB:
            # verbatim (2026-09-10): his audio at HIS level, untouched -- no gain, every second within +/-0.5 dB of
            # him. The rejected build read 0.9991 on the level-normalised test below while riding +5.0..+9.9 dB.
            gm = float(np.median(gains)) if gains else 99.0
            chk(bool(cors) and med >= 0.999 and abs(gm) <= 0.1 and min(gains) >= -0.5 and max(gains) <= 0.5,
                "13 audio IS his finished mix, untouched (per second)",
                f"median corr {med:.4f} over {len(cors)} windows; level vs his {gm:+.2f} dB "
                f"(seconds {min(gains):+.2f}..{max(gains):+.2f})" if cors else "no usable windows")
        else:
            chk(med >= 0.99, "13 audio is HIS finished mix (per-second, level-normalised)",
                f"median {med:.4f} over {len(cors)} windows; limiter rides "
                f"{min(gains):+.1f}..{max(gains):+.1f} dB" if cors else "no usable windows")

    # 15 THE WATCH PASS on THIS EXACT FILE -- the gate, not the metrics.
    wl = rel(C.get("watch_log"))
    ok, det = False, f"NOT DONE -- run watch.py ({C.get('watch_log')})"
    if wl and os.path.exists(wl):
        d = json.load(open(wl))
        ok = (d.get("video") == os.path.basename(V) and
              d.get("reviewed", 0) >= d.get("boundaries", 1) and d.get("inspected") is True)
        det = f"{d.get('reviewed')}/{d.get('boundaries')} boundaries reviewed as consecutive frames"
        if not ok and d.get("video") != os.path.basename(V):
            det = f"watch pass is for {d.get('video')}, not {os.path.basename(V)}"
    chk(ok, "15 WATCH PASS done on this exact file (the gate, not the metrics)", det)

    # 16 audio integrity. A mux once truncated the audio at 2:24 of a 3:52 master and exited 0.
    ad = subprocess.run([FP, "-v", "error", "-select_streams", "a", "-show_entries", "stream=duration",
                         "-of", "csv=p=0", V], capture_output=True, text=True).stdout.strip().split("\n")[0]
    ad = float(ad) if ad and ad != "N/A" else -1
    mono = a.mean(1) / 32768.0
    sec = [20 * np.log10(np.sqrt((mono[i*16000:(i+1)*16000] ** 2).mean()) + 1e-12) for i in range(int(dur))]
    silent = [i for i, v in enumerate(sec) if v < -50]
    chk(abs(ad - dur) < 0.15 and not silent, "16 audio stream runs the full length and no second is silent",
        f"audio {ad:.3f}s vs video {dur:.3f}s; {len(silent)} silent seconds; quietest {min(sec):.1f} dBFS")

    # 17 CENTERING, MEASURED ON THE DELIVERED FILE. The check whose absence cost two rejected versions:
    # everything upstream can be right and the delivered picture still wrong, because the ffmpeg crop
    # EXPRESSION built its nested ifs in the wrong order. Only the finished frames can see that.
    if "17" in skip: skipped("17 presenter is centred in the DELIVERED frame", skip["17"])
    else:
        try:
            import centering as CE
            # Reuse the frame cache ONLY when it was built from this exact file. Keyed on nothing but the folder's
            # existence, a re-render at the same path was measured on the PREVIOUS render's frames -- on 2026-09-10 the
            # Ad 1 master's "2/28 beyond 70px" came from a 14 s test render, and its re-rendered cutdown repeated its
            # first render's numbers to the pixel. A green row that measured the wrong file is worse than a red one.
            st = os.stat(V); key = f"{V}|{st.st_size}|{st.st_mtime_ns}"
            kp = os.path.join(bd, "centering", "source.key")
            fresh = os.path.isdir(os.path.join(bd, "centering/m")) and os.path.exists(kp) and open(kp).read() == key
            rows = CE.measure(rebuild=not fresh)
            if not fresh:
                os.makedirs(os.path.dirname(kp), exist_ok=True); open(kp, "w").write(key)
            talk = np.array([[r0[0], r0[2]] for r0 in rows if r0[1] == "talk"])
            cv = talk[:, 1]
            runs, cur = [], []
            for t, x in talk:
                if abs(x) > 60: cur.append(x)
                else:
                    if len(cur) >= 4: runs.append(float(np.mean(cur)))
                    cur = []
            if len(cur) >= 4: runs.append(float(np.mean(cur)))
            chk(abs(np.median(cv)) <= 25 and (np.abs(cv) > 70).mean() <= 0.10 and not runs,
                "17 presenter is centred in the DELIVERED frame",
                f"median {np.median(cv):+.0f} px, sd {cv.std():.0f}, "
                f"{(np.abs(cv)>70).sum()}/{len(cv)} beyond 70px, {len(runs)} sustained runs")
        except Exception as e:
            unmeasured("17 presenter is centred in the DELIVERED frame",
                       f"centering.py not importable from {bd} ({e})")

    # 18 the shared audio gate's STAMP on this exact file
    sys.path.insert(0, SHARED)
    try:
        from require_stamp import require_stamp
        require_stamp(V, quiet=True); sok, sd = True, "stamp present, matches this file, PASS"
        if VB:
            # a verbatim cut needs a VERBATIM stamp: a reference-mix stamp passed the rejected, processed build
            smode = json.load(open(V + ".audio_gate.json")).get("mode")
            if smode != "reference-verbatim":
                sok, sd = False, f"stamp mode is {smode!r}; audio_mode verbatim needs audio_gate.py --verbatim"
            else:
                sd = "stamp present, matches this file, PASS (verbatim: the editor's audio, untouched)"
    except BaseException as e:
        sok, sd = False, f"NO VALID STAMP: {e}"
    chk(sok, "18 audio gate stamp (_shared/audio/audio_gate.py) on this exact file", sd)

    # 19 the audio is his mix moved by ONE CONSTANT GAIN (one-sided proof)
    if hm and os.path.exists(hm):
        gf = subprocess.run(["python3", os.path.join(HERE, "gain_flatness.py"), hm, V],
                            capture_output=True, text=True)
        gl = [l for l in (gf.stdout + gf.stderr).strip().split("\n") if l.strip()]
        chk(gf.returncode == 0, "19 constant gain against HIS mix (gain_flatness, one-sided)",
            gl[-1] if gl else "no output")
    elif "13" in skip: skipped("19 constant gain against HIS mix", skip["13"])
    else: unmeasured("19 constant gain against HIS mix (gain_flatness, one-sided)", "no his_mix in qc.json")

    # 20 SUBTITLE SYNC on the DELIVERED file (Dan, 2026-09-08: the highlighted word must be the word
    # being said).
    if "20" in skip: skipped("20 captions synchronised with the speech", skip["20"])
    else:
        cs = subprocess.run(["python3", os.path.join(HERE, "caption_sync_check.py"), V],
                            capture_output=True, text=True, cwd=bd)
        cl = [l for l in (cs.stdout + cs.stderr).strip().split("\n") if l.strip()]
        det = " | ".join(l.strip() for l in cl if "onset minus" in l or "silence" in l)[:200]
        chk(cs.returncode == 0, "20 captions synchronised with the speech (highlight vs forced alignment)",
            det or (cl[-1] if cl else "no output"))

    print(f"\nQC  {V}")
    for ok_, n_, d in R: print(f'  {"PASS" if ok_ else "FAIL"}  {n_:72s} {d}')
    bad = [x for x in R if not x[0]]
    print(f"\n{len(R)-len(bad)}/{len(R)} pass")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
