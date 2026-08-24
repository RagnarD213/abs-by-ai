#!/usr/bin/env python3
"""THE STYLE GATE — the checks that used to exist only as prose in SKILL.md.

WHY THIS FILE EXISTS. The ab-wheel video passed 6/6 of the old QC and was still rejected:
"substantially better than what we made -- it looks better, it sounds better, and the
graphics are better." Seven of the nine techniques the outside editor used were ALREADY
in this repo. They were skipped because the skill's quality bar was prose and its quality
gate was code, and under time pressure a session ships what the gate checks. So every
style rule now fails the build.

EVERYTHING HERE IS MEASURED OFF THE FINISHED FILE, not off the build plan. A plan can
claim thirty cutaways; only the file proves it. The one exception is the splice check,
which needs to know where the joins are.

usage: qc_style.py <video.mp4> [--plan plan.json] [--srt captions.srt] [--talking-head]
"""
import argparse, json, math, re, subprocess, sys, wave
import numpy as np

FF  = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
FFP = FF.replace("ffmpeg", "ffprobe")

# ---- the gate values. Each one traces to a measurement of the reference cut or to a
# rule Dan wrote down; none of them is a taste call.
MIN_SCENES_PER_MIN = 4.0     # reference cut: 54 cuts / 6:58 = 7.7/min. Ours was 0.1.
MAX_STATIC_RUN     = 30.0    # Dan's own written rule, 2026-08-21 (spray-tan rev 1)
MIN_COVERAGE       = 0.40    # reference cut ~90%; spray tan shipped 51%; ab wheel 21%
MIN_WPM            = 170.0   # reference cut 189 wpm over its whole runtime
MAX_DEAD_AIR       = 0.25    # reference cut 23%; ours was 38%
MIN_CHANNEL_SNR    = 10.0    # a dead input measures 0.6-1.4 dB
MIN_LR_CORR        = 0.90    # dead channel: -0.005. two-mic comb: +0.07. good: +0.999
BED_FLOOR_DB       = -52.0   # a ducked bed holds the 2nd-percentile frame above this
MAX_TRUE_PEAK      = -0.5

FAILS, OKS = [], []
def chk(cond, msg, fix=""):
    (OKS if cond else FAILS).append(msg if cond else f"{msg}\n        -> FIX: {fix}")
    print(f"[{'OK  ' if cond else 'FAIL'}] {msg}")
    if not cond and fix: print(f"        -> FIX: {fix}")
    return cond

def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()

def pcm(path, af=None, ac=1, sr=48000):
    cmd = [FF, "-v", "error", "-i", path]
    if af: cmd += ["-af", af]
    cmd += ["-ac", str(ac), "-ar", str(sr), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    return a.reshape(-1, ac) if ac > 1 else a

# ---------------------------------------------------------------- checks
def check_streams(v):
    p = sh([FFP, "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=codec_name,width,height", "-of", "csv=p=0", v])
    chk(p.startswith("h264,1920,1080"), f"video stream: {p}",
        "render at 1920x1080 h264 (Step 7)")
    return float(sh([FFP, "-v", "error", "-show_entries", "format=duration",
                     "-of", "csv=p=0", v]))

def check_loudness(v):
    p = subprocess.run([FF, "-nostdin", "-hide_banner", "-nostats", "-i", v,
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-vn", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    m = json.loads(p[p.rindex("{"):p.rindex("}") + 1])
    i, tp = float(m["input_i"]), float(m["input_tp"])
    chk(abs(i + 14.0) <= 1.0, f"integrated loudness {i} LUFS (target -14 +/-1)",
        "re-run the corrective measured loudnorm (Step 7.6)")
    chk(tp <= MAX_TRUE_PEAK, f"true peak {tp} dBTP (must be <= {MAX_TRUE_PEAK})",
        "the two-pass measured loudnorm caps this; do NOT reach for alimiter, it costs "
        "a dB of loudness per dB of peak (Step 7.6)")

def check_channels(v):
    """Catches BOTH shoot audio defects this project has hit: a dead input (ab wheel,
    8/14 -- left channel SNR 0.6-1.4 dB) and two hard-panned microphones (8/3 -- the
    same voice 7.5 ms apart, zero-lag correlation +0.07). Both shipped. Both are
    inaudible on a QC that only measures LUFS."""
    a = pcm(v, ac=2)
    L, R = a[:, 0], a[:, 1]
    x, y = L - L.mean(), R - R.mean()
    corr = float((x * y).sum() / max(math.sqrt((x * x).sum() * (y * y).sum()), 1e-12))
    snrs = []
    for sig, name in ((L, "L"), (R, "R")):
        N = 1024
        fr = sig[:len(sig)//N*N].reshape(-1, N)
        rms = np.sqrt((fr ** 2).mean(1) + 1e-15)
        sp, nz = rms > np.percentile(rms, 70), rms < np.percentile(rms, 5)
        snrs.append(20 * math.log10(rms[sp].mean() / max(rms[nz].mean(), 1e-9)))
    chk(min(snrs) >= MIN_CHANNEL_SNR,
        f"channel SNR L {snrs[0]:.1f} dB / R {snrs[1]:.1f} dB (min {MIN_CHANNEL_SNR})",
        "one input is dead or unused. Run reference/chan_analyse.py on the roll, then "
        "rebuild from the good channel only with build_audio_singlemic.py (Step 5.6)")
    chk(corr >= MIN_LR_CORR,
        f"L/R correlation {corr:+.4f} (min {MIN_LR_CORR:+.2f})",
        "the voice is not centred: either two mics are hard-panned or one channel is "
        "dead. Fold the good mic to BOTH channels with pan=stereo|c0=c0|c1=c0 (Step 5.6)")
    return a

def check_bed(a):
    """A music bed is the difference between 'a talking head' and 'a video'. Its
    signature is that the programme floor never falls to room tone."""
    mid = a.mean(1)
    n = 4800
    fr = mid[:len(mid)//n*n].reshape(-1, n)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-12)
    p2 = float(np.percentile(db, 2))
    chk(p2 >= BED_FLOOR_DB,
        f"music bed: 2nd-percentile frame level {p2:.1f} dBFS (a ducked bed holds this "
        f"above {BED_FLOOR_DB})",
        "no bed detected. Pick one by measurement with reference/pick_bed.py (Pixabay "
        "Content Licence: commercial, no attribution) and duck it under the voice (Step 7)")

def scene_times(v, dur, fps=6):
    """Visual-change events, measured directly rather than with ffmpeg's `scene` filter.

    `select='gt(scene,0.25)'` only sees HARD cuts. It scored this rebuild at 44 changes
    and reported a 44.9 s static stretch through a passage that actually carries seven
    full-frame cutaways -- because each one dissolved over 0.14 s and a dissolve spreads
    the change across four frames, none of which trips the threshold. A gate that can be
    satisfied by a cut but not by a dissolve is measuring the encoder, not the edit.

    Instead: sample the picture, take the frame-to-frame difference, and call anything
    above the file's own robust noise level a change event, merging events inside 0.4 s
    so one dissolve counts once.
    """
    raw = subprocess.run([FF, "-v", "error", "-i", v, "-vf",
        f"fps={fps},scale=64:36,format=gray", "-f", "rawvideo", "-"],
        capture_output=True).stdout
    F = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 36 * 64).astype(np.float32)
    d = np.abs(np.diff(F, axis=0)).mean(1)
    med = float(np.median(d))
    mad = float(np.median(np.abs(d - med))) or 0.5
    thr = max(med + 6.0 * mad, 3.0)
    idx = [i for i in range(len(d)) if d[i] > thr]
    ts, last = [], -9.0
    for i in idx:
        t = (i + 1) / fps
        if t - last >= 0.4: ts.append(round(t, 2)); last = t
        else: last = t
    return ts

def check_cutting(v, dur):
    ts = scene_times(v, dur)
    per_min = len(ts) / (dur / 60)
    chk(per_min >= MIN_SCENES_PER_MIN,
        f"visual cuts: {len(ts)} in {dur/60:.1f} min = {per_min:.1f}/min "
        f"(min {MIN_SCENES_PER_MIN}/min; the reference cut runs 7.7/min)",
        "the shot never changes. Add punch-in reframes at joins and mid-take, and cut "
        "away to B-roll (Steps 5.4 and 5.5)")
    edges = [0.0] + ts + [dur]
    runs = [(edges[i], edges[i+1] - edges[i]) for i in range(len(edges) - 1)]
    worst_t, worst = max(runs, key=lambda r: r[1])
    chk(worst <= MAX_STATIC_RUN,
        f"longest stretch with no visual change {worst:.1f}s at "
        f"{int(worst_t//60)}:{worst_t%60:04.1f} (Dan's rule: {MAX_STATIC_RUN}s max)",
        "break it with a cutaway, a reframe or a graphic (Step 5.5)")
    return ts

def coverage_of(v):
    """Fraction of the runtime that is NOT the main talking-head scene.

    First attempt compared each frame to the per-pixel MEDIAN frame and called anything
    far from it "covered". That scored this rebuild at 100%, which is nonsense: once
    every shot is a punch-in, no frame matches the plate any more, and the metric stopped
    measuring cutaways and started measuring reframes.

    A punch-in keeps the SCENE -- same sky, same pool, same patio -- so what separates a
    cutaway from a reframe is the PALETTE, not the pixels. Compare coarse RGB histograms
    against the programme's median histogram: a gym, a dark product shot and a brand-field
    card are all far away in that space; a tighter crop of the same patio is not.
    """
    raw = subprocess.run([FF, "-v", "error", "-i", v, "-vf",
        "fps=2,scale=48:27", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True).stdout
    F = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 27 * 48, 3)
    q = (F >> 6).astype(np.int32)                       # 4 levels per channel
    idx = q[:, :, 0] * 16 + q[:, :, 1] * 4 + q[:, :, 2]
    H = np.zeros((len(F), 64), np.float32)
    for i in range(len(F)):
        H[i] = np.bincount(idx[i], minlength=64)
    H /= H.sum(1, keepdims=True)
    ref = np.median(H, axis=0)
    d = np.abs(H - ref).sum(1) / 2.0                    # 0 = identical, 1 = disjoint
    # Threshold calibrated on three cuts of the SAME footage:
    #     the outside editor's 6:58 cut   64.6%   (the standard to hit)
    #     this rebuild                    58.2%
    #     the 8/20 cut Dan rejected        8.7%
    # 0.12 is the value that separates them; tightening it to 0.34 collapsed all three
    # toward each other and scored the rejected cut and the good one within 12 points.
    return float((d > 0.12).mean()), d

def check_coverage(v, dur, plan):
    cov, _ = coverage_of(v)
    chk(cov >= MIN_COVERAGE,
        f"cutaway/graphic coverage {cov*100:.0f}% of runtime (min {MIN_COVERAGE*100:.0f}%; "
        f"the reference cut measures 65%)",
        "too much of this is the one camera shot. Plan cutaways against the transcript "
        "with reference/plan_map.py and build them (Step 5.5)")
    return cov

def check_pace(v, srt, dur):
    words = None
    if srt:
        txt = open(srt).read()
        words = len(re.findall(r"\b[\w']+\b",
                    re.sub(r"^\d+$|^[\d:,]+ --> [\d:,]+$", "", txt, flags=re.M)))
    if words is None:
        chk(False, "pace: no transcript supplied", "pass --srt so wpm can be measured")
        return
    wpm = words / (dur / 60)
    chk(wpm >= MIN_WPM,
        f"pace {wpm:.0f} wpm over {dur/60:.1f} min (min {MIN_WPM}; reference cut 189)",
        "remove dead air. Measure silence from a 5 ms RMS envelope of the real audio, "
        "never from Whisper's word times, and guard every cut so it lands BETWEEN two "
        "spoken words (Step 3)")

def check_dead_air(a, dur):
    mid = a.mean(1)
    n = 2400                                  # 50 ms
    fr = mid[:len(mid)//n*n].reshape(-1, n)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-12)
    thr = np.percentile(db, 50) - 14
    quiet, runs, cur = db < thr, [], 0
    for q in quiet:
        if q: cur += 1
        elif cur: runs.append(cur * 0.05); cur = 0
    if cur: runs.append(cur * 0.05)
    dead = sum(r for r in runs if r >= 0.25)
    frac = dead / dur
    chk(frac <= MAX_DEAD_AIR,
        f"dead air {dead:.0f}s = {frac*100:.0f}% of runtime (max {MAX_DEAD_AIR*100:.0f}%)",
        "tighten the pauses, and check whether a silent demo section is carrying it "
        "(Step 3)")

def check_captions(v, dur, talking_head):
    """Burned captions leave a signature: a band of near-white pixels with dark outline
    in the lower third, present on most frames of a talking-head video."""
    if not talking_head:
        print("[SKIP] captions: not flagged as talking-head content"); return
    hits, n = 0, 0
    for t in np.linspace(dur * 0.05, dur * 0.95, 36):
        raw = subprocess.run([FF, "-v", "error", "-ss", f"{t:.2f}", "-i", v, "-frames:v", "1",
            "-vf", "crop=1320:110:300:930,format=gray", "-f", "rawvideo", "-"],
            capture_output=True).stdout
        if not raw: continue
        b = np.frombuffer(raw, dtype=np.uint8)
        n += 1
        white = (b > 225).mean(); dark = (b < 40).mean()
        if 0.004 < white < 0.20 and dark > 0.01: hits += 1
    frac = hits / max(n, 1)
    chk(frac >= 0.45,
        f"burned captions present on {frac*100:.0f}% of sampled frames (min 45%)",
        "burn word-timed captions from the FINAL audio; ship the .srt too (Step 8)")

def check_splices(v, plan):
    if not plan: print("[SKIP] splice discontinuity: no --plan given"); return
    P = json.load(open(plan))
    keeps = P["keeps"]; joins, acc = [], 0.0
    for a, b in keeps[:-1]:
        acc += b - a; joins.append(round(acc, 3))
    a = pcm(v, ac=1)
    sr = 48000
    def jump(c, win=0.004):
        i0, i1 = max(1, int((c - win) * sr)), min(len(a) - 1, int((c + win) * sr))
        return float(np.abs(np.diff(a[i0:i1])).max()) if i1 > i0 + 1 else 0.0
    rng = np.random.default_rng(7)
    ctrls = sorted(jump(float(x)) for x in rng.uniform(5, max(6, len(a)/sr - 5), 150))
    ceiling = ctrls[-1]; med = ctrls[len(ctrls)//2] or 1e-9
    bad = sum(1 for j in joins if jump(j) > ceiling * 1.25)
    worst = max((jump(j) / med) for j in joins) if joins else 0
    chk(bad == 0, f"splice discontinuity: {bad}/{len(joins)} joins above 1.25x the file's "
                  f"own natural ceiling; worst join {worst:.2f}x median",
        "a join is landing mid-waveform. Snap it into measured silence (Step 3)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--plan"); ap.add_argument("--srt")
    ap.add_argument("--talking-head", action="store_true")
    A = ap.parse_args()
    dur = check_streams(A.video)
    print(f"       duration {dur:.2f}s ({int(dur//60)}:{dur%60:05.2f})")
    check_loudness(A.video)
    a = check_channels(A.video)
    check_bed(a)
    check_dead_air(a, dur)
    check_cutting(A.video, dur)
    check_coverage(A.video, dur, A.plan)
    check_pace(A.video, A.srt, dur)
    check_captions(A.video, dur, A.talking_head)
    check_splices(A.video, A.plan)
    print(f"\n{len(OKS)} passed, {len(FAILS)} failed")
    print("STYLE GATE", "PASS" if not FAILS else "FAIL")
    sys.exit(1 if FAILS else 0)
