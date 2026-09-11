#!/usr/bin/env python3
"""sets_level.py — how loud the effort sounds in a workout's live sets are, measured against the talking.

    python3 sets_level.py CUT.mp4 --whisper CUT.json [--sets 0:02-1:01,1:17-2:03] [--min-gap 8]

Talking = the Whisper speech segments (3+ words; one- and two-word segments such as "Oh" / "Ah" are
Whisper hallucinations on music and are ignored). Sets = stretches with no speech longer than
--min-gap seconds, or the ranges given with --sets.

Reports the talking level (median momentary loudness inside speech) and, for each set, the effort
peaks (95th percentile and max of the 400 ms momentary loudness) and the floor (10th percentile)
relative to it.

Measured in the 250-4000 Hz band by default (--band full for full-band). Grunting and breathing live
where the voice does; a bass-heavy music bed does not. On the approved explainer, set 2 read as loud as
the talking full-band, and 80% of that window's energy was under 150 Hz: the bed swelling while he was
silent, not grunting (his talking is 75% in 400-3000 Hz, and that window only 7%).

Dan's target (2026-09-11): during a set the grunting, breathing and the equipment are audible but
clearly under the voice, never annoying or overwhelming. His instruction on Zeeshan's ab wheel cut was
"reduce volume of my mic by 80% while I am actively doing sets" (about -14 dB). Verdicts:
  LOUD   effort p95 is less than --loud-db under the talking level (default 5 dB)
  BURIED effort max is more than --buried-db under the talking level (default 20 dB): the camera
         sound is effectively gone, the explainer round-3 failure ("a workout with no sound")
  OK     in between (target: effort peaks 5-14 dB under the talking)
Calibrated 2026-09-11 on one rejected and one approved file, the corpus rule (fail the rejected, pass the approved):
Zeeshan's ab wheel follow-along, rejected by Dan: p95 +2.2 / +3.7 / +5.4 dB against the talking, all three sets LOUD. His
ab wheel explainer, approved 2026-09-09: -9.6 / -6.9 / -9.9 dB, all three OK (full-band, its set 2 false-alarmed at
+0.1 dB on the music's bass). Dan's "80%" (-14 dB) applied to the rejected file lands at about -9 to -12 dB.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
FF = ROOT / "Media/video_edit/bin/ffmpeg"
FF = str(FF) if FF.exists() else "ffmpeg"


def tc(s):
    p = [float(x) for x in s.split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0]


def fmt(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def momentary(path, band=None):
    """(times, LUFS) of ffmpeg's ebur128 momentary loudness, one value per 100 ms, optionally band-limited."""
    pre = f"highpass=f={band[0]},lowpass=f={band[1]}," if band else ""
    out = subprocess.run([FF, "-v", "error", "-i", path, "-vn", "-af",
                          pre + "ebur128=metadata=1,ametadata=print:key=lavfi.r128.M:file=-",
                          "-f", "null", "-"], capture_output=True, text=True).stdout
    T, V, t = [], [], None
    for line in out.splitlines():
        m = re.search(r"pts_time:([0-9.]+)", line)
        if m:
            t = float(m.group(1))
            continue
        m = re.search(r"lavfi\.r128\.M=(\S+)", line)
        if m and t is not None:
            try:
                v = float(m.group(1))
            except ValueError:
                v = -120.0
            T.append(t)
            V.append(v if np.isfinite(v) else -120.0)
    return np.array(T), np.array(V)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cut")
    ap.add_argument("--whisper", required=True, help="Whisper JSON for the cut (segments with start/end/text)")
    ap.add_argument("--sets", help="comma-separated m:ss-m:ss ranges; default: auto from the speech gaps")
    ap.add_argument("--min-gap", type=float, default=8.0)
    ap.add_argument("--loud-db", type=float, default=5.0)
    ap.add_argument("--buried-db", type=float, default=20.0)
    ap.add_argument("--band", default="250-4000", help="Hz band to measure in, or 'full'")
    a = ap.parse_args()

    segs = json.load(open(a.whisper))["segments"]
    # Word timings when the JSON has them (whisper --word_timestamps True): segment starts snap to Whisper's
    # 30 s windows after music, which marks the end of a set as "speech". Merge words closer than 0.6 s.
    spans = []
    for s in segs:
        if len(s["text"].split()) < 3:
            continue
        ws = s.get("words") or []
        spans += [(w["start"], w["end"]) for w in ws] if ws else [(s["start"], s["end"])]
    speech = []
    for st, en in sorted(spans):
        if speech and st - speech[-1][1] < 0.6:
            speech[-1] = (speech[-1][0], max(en, speech[-1][1]))
        else:
            speech.append((st, en))
    band = None if a.band == "full" else tuple(float(x) for x in a.band.split("-"))
    T, V = momentary(a.cut, band)
    if not len(T):
        sys.exit("no loudness data — is this a media file with audio?")
    dur = T[-1]

    in_speech = np.zeros(len(T), bool)
    for s, e in speech:
        in_speech |= (T >= s + 0.2) & (T <= e - 0.2)
    talk = V[in_speech & (V > -40)]
    if len(talk) < 20:
        sys.exit("FAIL: fewer than 2 s of speech found — cannot measure the talking level (pass a better --whisper)")
    talk_lvl = float(np.median(talk))

    if a.sets:
        sets = [tuple(tc(x) for x in r.split("-")) for r in a.sets.split(",")]
    else:
        edges = [0.0] + [x for se in speech for x in se] + [dur]
        sets = [(edges[i], edges[i + 1]) for i in range(0, len(edges) - 1, 2)
                if edges[i + 1] - edges[i] >= a.min_gap]
    if not sets:
        sys.exit("FAIL: no set found (no speech gap >= --min-gap and no --sets given)")

    print(f"band {a.band} Hz; talking: median momentary {talk_lvl:.1f} LUFS over {in_speech.sum() / 10:.0f} s of speech")
    worst = "OK"
    for i, (s, e) in enumerate(sets, 1):
        w = (T >= s + 0.5) & (T <= e - 0.5)
        v = V[w]
        if not len(v):
            continue
        p95, mx, p10 = np.percentile(v, 95), v.max(), np.percentile(v, 10)
        verdict = ("LOUD" if p95 > talk_lvl - a.loud_db else
                   "BURIED" if mx < talk_lvl - a.buried_db else "OK")
        if verdict == "LOUD" or (verdict == "BURIED" and worst == "OK"):
            worst = verdict
        print(f"set {i}  {fmt(s)}-{fmt(e)} ({e - s:.0f} s): effort p95 {p95:.1f} ({p95 - talk_lvl:+.1f} vs talk)"
              f"  max {mx:.1f} ({mx - talk_lvl:+.1f})  floor p10 {p10:.1f} ({p10 - talk_lvl:+.1f})  -> {verdict}")
    advice = {
        "LOUD": "the effort sounds are as loud as the talking — bring the mic down during the sets (about 80%, "
                "-14 dB) so the peaks land 5-14 dB under the voice, still audible",
        "BURIED": "the camera sound is effectively gone during the sets — bring it back so the breathing and the "
                  "equipment are audible, 5-14 dB under the voice",
        "OK": "effort sounds sit under the voice and stay audible",
    }
    print(f"verdict: {worst} — {advice[worst]}")


if __name__ == "__main__":
    main()
