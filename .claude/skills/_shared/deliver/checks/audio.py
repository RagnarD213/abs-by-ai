#!/usr/bin/env python3
"""Audio rows.

⚠ THIS MODULE DOES NOT GRADE AUDIO. `_shared/audio/audio_gate.py` is the one audio gate and it
already owns loudness, true peak, the stereo image, the room, artifacts, do-no-harm and the
verbatim rows. Re-implementing any of that here would create fork number eighteen. What lives here
is the two things the audio gate cannot see, because they are about the audio's relationship to the
PICTURE and to the CONTAINER rather than to the sound:

    audio:stamp              the audio gate ran, on THIS file, in the right mode, and passed
    audio:stream_integrity   the audio runs the full length of the picture and no second is silent
    audio:lipsync            the finished audio is not late against the audio the picture was cut to
"""
import json
import math
import os
import subprocess
import sys

import numpy as np

from .. import common as C
from ..common import Row, unmeasured

SHARED_AUDIO = os.path.join(C.REPO, ".claude/skills/_shared/audio")


def stamp(key, pr, cfg, plan, video):
    """audio:stamp -- the shared audio gate's verdict on this exact file.

    A delivered file with no stamp has had its audio checked by nobody. A stamp whose sha256 does
    not match is a stamp for a different render. And a VERBATIM cut needs a VERBATIM stamp: a plain
    reference-mix stamp passed the processed Zeeshan build Dan rejected on 2026-09-10.
    """
    sys.path.insert(0, SHARED_AUDIO)
    try:
        from require_stamp import require_stamp
    except Exception as e:                                   # noqa: BLE001
        return unmeasured(key, f"_shared/audio/require_stamp.py not importable ({e})")
    try:
        require_stamp(video, quiet=True)
    except BaseException as e:                               # noqa: BLE001
        return Row(key, False, f"no valid audio-gate stamp: {e}")
    want_mode = cfg.get("mode")
    if want_mode:
        try:
            got = json.load(open(video + ".audio_gate.json")).get("mode")
        except Exception as e:                               # noqa: BLE001
            return unmeasured(key, f"stamp file unreadable ({e})")
        if got != want_mode:
            return Row(key, False,
                       f"stamp mode is {got!r}; this format requires {want_mode!r} "
                       f"(run audio_gate.py with the matching flag)")
        return Row(key, True, f"stamp present, matches this file, PASS (mode {got})",
                   dict(mode=got))
    return Row(key, True, "stamp present, matches this file, PASS")


def stream_integrity(key, pr, cfg, plan, video):
    """audio:stream_integrity -- the audio runs the whole picture and no second of it is silent.

    A mux once truncated the audio at 2:24 of a 3:52 master and exited 0.
    """
    if not pr["has_audio"]:
        return Row(key, False, "there is no audio stream in this file")
    vdur, adur = pr["vdur"], pr["adur"]
    if adur is None:
        return unmeasured(key, "the audio stream reports no duration")
    a = C.pcm(video, ac=1, sr=16000)
    n = int(min(vdur, adur))
    sec = [20 * math.log10(math.sqrt(float((a[i * 16000:(i + 1) * 16000] ** 2).mean()) + 1e-24) + 1e-12)
           for i in range(max(n, 1))]
    floor = cfg.get("silent_second_dbfs", -50.0)
    lead = cfg.get("allow_silent_lead_s", 0)
    tail = cfg.get("allow_silent_tail_s", 0)
    silent = [i for i, v in enumerate(sec) if v < floor and lead <= i < n - tail]
    tol = cfg["length_tolerance_s"]
    # ⚠ ASYMMETRIC BY CONFIG, never by widening. `exercise-demo` legitimately runs picture past
    # audio (the narration ends, the rep keeps looping) and declares `max_audio_short_s` measured
    # off the files Dan approved. Every other format leaves it unset and gets the symmetric bound.
    short_ok = cfg.get("max_audio_short_s", tol)
    gap = vdur - adur                                        # positive = the picture outruns audio
    length_ok = (-tol <= gap <= short_ok)
    ok = length_ok and not silent
    return Row(key, ok,
               f"audio {adur:.3f}s vs picture {vdur:.3f}s (gap {gap:+.3f}s; allowed "
               f"{-tol:+.2f}..{short_ok:+.2f}s); "
               f"{len(silent)} silent second(s){' at ' + str(silent[:8]) if silent else ''}; "
               f"quietest {min(sec) if sec else float('nan'):.1f} dBFS",
               dict(adur=round(adur, 3), vdur=round(vdur, 3), gap=round(gap, 3),
                    silent=silent[:40]))


def lipsync(key, pr, cfg, plan, video):
    """audio:lipsync -- the finished audio is aligned with the audio the picture was cut against.

    ⚠ THE DEFECT THIS EXISTS FOR, measured on V4 2026-08-28 (longform-edit/SKILL.md):
    `alimiter=…:attack=5` shifts the whole programme by EXACTLY 219 samples = 4.966 ms at 44.1 kHz,
    correlation 1.0000 against a gain-only render at three checkpoints. Our standing loudness finish
    uses alimiter, so every master finished that way has been ~5 ms late against its own picture.
    Inaudible on a talking head, free to fix, and it corrupts any lip-sync measurement made against
    the source. The fix is `atrim=start_sample=219,asetpts=N/SR/TB,apad` with `-t <duration>`.

    ⚠ AND THE AUDIO GATE CANNOT SEE IT. `audio_gate.py` checks audio LENGTH (+/-0.10 s); a 5 ms
    shift keeps the length. Nothing in this repo has ever measured ALIGNMENT. This row is why the
    plan carries `source_audio`: the mix the picture was cut to, before the loudness finish.
    """
    src = plan.get("source_audio")
    if not src:
        return unmeasured(key, "the plan gives no `source_audio` -- the mix the picture was cut "
                               "against, before the loudness finish. Without it nothing can tell a "
                               "5 ms limiter delay from a correct render")
    if not os.path.exists(src):
        return unmeasured(key, f"`source_audio` is not on disk: {src}")
    sr = 48000
    a = C.pcm(video, ac=1, sr=sr)
    b = C.pcm(src, ac=1, sr=sr)
    n = min(len(a), len(b))
    if n < sr * 5:
        return unmeasured(key, "less than 5 s of comparable audio")
    checkpoints = cfg.get("checkpoints", 5)
    win = int(sr * 4.0)
    max_lag = int(sr * 0.050)
    lags = []
    for k in range(checkpoints):
        i = int((k + 0.5) / checkpoints * (n - win))
        x = a[i:i + win] - a[i:i + win].mean()
        y = b[i:i + win] - b[i:i + win].mean()
        if float(np.sqrt((y ** 2).mean())) < 1e-4:
            continue                                        # silence: nothing to align
        nfft = 1 << int(math.ceil(math.log2(win * 2)))
        cc = np.fft.irfft(np.fft.rfft(x, nfft) * np.conj(np.fft.rfft(y, nfft)), nfft)
        cc = np.concatenate([cc[-max_lag:], cc[:max_lag + 1]])
        lag = int(np.argmax(cc)) - max_lag
        lags.append(lag / sr * 1000.0)
    if not lags:
        return unmeasured(key, "every checkpoint landed in silence")
    worst = max(lags, key=abs)
    tol = cfg["tolerance_ms"]
    return Row(key, abs(worst) <= tol,
               f"finished audio vs source at {len(lags)} checkpoints: "
               f"{', '.join(f'{v:+.3f}' for v in lags)} ms (worst {worst:+.3f}, max {tol} ms)",
               dict(lags_ms=[round(v, 4) for v in lags], worst_ms=round(worst, 4), tol=tol))


def click_at_joins(key, pr, cfg, plan, video):
    """audio:click_at_joins -- a join landing mid-waveform, against the file's OWN natural ceiling.

    The control distribution is 150 random points in this same file, so a busy mix and a dry room
    are each graded against themselves rather than against a constant somebody picked once.
    """
    joins = plan.get("joins")
    if not joins:
        return unmeasured(key, "the plan declares no `joins`; declare them, or declare this row "
                               "not applicable (a single continuous take has none)")
    sr = 48000
    a = C.pcm(video, ac=1, sr=sr)

    def jump(t, win=0.004):
        i0, i1 = max(1, int((t - win) * sr)), min(len(a) - 1, int((t + win) * sr))
        return float(np.abs(np.diff(a[i0:i1])).max()) if i1 > i0 + 1 else 0.0

    rng = np.random.default_rng(7)
    ctrl = sorted(jump(float(x)) for x in rng.uniform(5, max(6, len(a) / sr - 5), 150))
    ceiling = ctrl[-1]
    mult = cfg.get("ceiling_mult", 1.25)
    bad = [(round(t, 2), round(jump(t) / max(ceiling, 1e-9), 2)) for t in joins
           if jump(t) > ceiling * mult]
    return Row(key, not bad,
               f"{len(bad)}/{len(joins)} joins above {mult}x the file's own natural ceiling "
               f"({ceiling:.4f}): {bad[:6]}",
               dict(bad=bad[:30], ceiling=round(ceiling, 5), joins=len(joins)))
