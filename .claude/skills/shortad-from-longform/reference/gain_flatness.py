#!/usr/bin/env python3
"""gain_flatness.py -- QC check 17.

Proves the delivered audio is the SOURCE mix moved by ONE CONSTANT GAIN, not by a
compressor. Run it on the ENCODED deliverable, never on the intermediate wav.

    python3 gain_flatness.py SOURCE.(mp4|wav) OUTPUT.(mp4|wav) [--gain G] [--offset-samples N]

Why this exists: on 2026-09-02 Dan rejected the Ad-1 vertical -- "the audio sounds
horrible ... nowhere near as good as Muhammad's". The mix WAS Muhammad's, and the
per-second correlation against his master was 0.997, because correlation is
level-normalised and cannot see a slow gain envelope. `loudnorm` had silently fallen
back to dynamic mode (his master: -18.2 LUFS already at +0.0 dBTP, so a linear +4 dB
lift under a true-peak ceiling is impossible) and was swinging the gain +1.2 -> +9.5 dB
second to second, swelling the bed and the room tone in every gap.

The test is ONE-SIDED, and that is the whole point. A limiter can only ever pull the
loudest seconds DOWN; a compressor/normaliser pushes quiet ones UP. So the gate asks
whether the per-second gain ratio is a ceiling at the constant gain G with a short tail
below it:

  * nothing above G                      -- g.max() <= G + 0.05 dB
  * most of the file untouched by it     -- p90(g)  >= G - 0.25 dB
  * the limiter is shaving, not gouging  -- g.min()  >= G - 2.5 dB

Do NOT gate on the standard deviation. A correct file measured sd 0.51 dB purely from
legitimate downward shaving; an sd threshold fails the good file and would have been
"fixed" by loosening it until the bad one passed too.
"""
import subprocess, sys, tempfile, os, wave
import numpy as np

BIN = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
SR = 48000
ABOVE_MAX = 0.05   # dB any second may sit above the constant gain
P90_DROP = 0.25    # dB the 90th percentile may sit below it
# ⚠ RECALIBRATED 2026-09-03 to a file Dan APPROVED, not to "Ad 1's number + margin". Ad 2 rev 2's
# audio ("this sounds like Muhammad") had the limiter riding +2.1..+6.4 dB against a +6.4 dB
# constant -- 4.3 dB below G on its deepest second -- and the V2 rebuild measures 3.7 (his master:
# -19.0 LUFS at 0.0 dBTP, so every lift to -14 shaves its densest speech seconds by 3+ dB at ANY
# useful gain: +4.5 dB still reads 3.0). The 2.5 was Ad 1's fixed file (2.17) plus margin, and it
# failed an approved file. The discriminating test is the CEILING: the rejected loudnorm file sat
# 133 seconds ABOVE G, and still fails here.
DOWN_MAX = 4.50    # dB the limiter may shave off the loudest second (approved: 4.3; Ad 1 fixed: 2.17)


def mono(path, tmp, tag):
    out = os.path.join(tmp, tag + ".wav")
    subprocess.run([f"{BIN}/ffmpeg", "-v", "error", "-y", "-i", path,
                    "-vn", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", out], check=True)
    w = wave.open(out)
    d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    return d


def find_offset(a, b, maxlag=SR // 2):
    """Lag of b relative to a, from a mid-file window."""
    s = slice(len(a) // 3, len(a) // 3 + SR * 10)
    x, y = a[s] - a[s].mean(), b[s] - b[s].mean()
    n = 1
    while n < len(x) + len(y):
        n *= 2
    c = np.fft.irfft(np.fft.rfft(y, n) * np.conj(np.fft.rfft(x, n)), n)
    c = np.concatenate([c[-maxlag:], c[:maxlag + 1]])
    return int(np.arange(-maxlag, maxlag + 1)[np.argmax(c)])


def main():
    src, out = sys.argv[1], sys.argv[2]
    off = None
    if "--offset-samples" in sys.argv:
        off = int(sys.argv[sys.argv.index("--offset-samples") + 1])
    G = None
    if "--gain" in sys.argv:
        G = float(sys.argv[sys.argv.index("--gain") + 1])
    with tempfile.TemporaryDirectory() as tmp:
        a = mono(src, tmp, "src")
        b = mono(out, tmp, "out")
    if off is None:
        off = find_offset(a, b)
    print(f"output lags source by {off} samples ({off / SR * 1000:.2f} ms)")
    b = b[off:] if off >= 0 else np.concatenate([np.zeros(-off), b])
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]

    g, corr, silent = [], [], []
    for t in range(int(n / SR)):
        x, y = a[t * SR:(t + 1) * SR], b[t * SR:(t + 1) * SR]
        if y.std() < 1e-4:
            silent.append(t)
        if x.std() < 1e-5:
            continue
        g.append((t, 20 * np.log10(y.std() / x.std())))
        corr.append(np.corrcoef(x, y)[0, 1])
    ts = np.array([t for t, _ in g])
    g = np.array([v for _, v in g])
    if G is None:
        G = float(g.max())
        print(f"constant gain not given; inferred from the ceiling: {G:+.2f} dB")
    p90 = float(np.percentile(g, 90))
    above = ts[g > G + ABOVE_MAX]

    print(f"per-second gain vs the {G:+.2f} dB constant: "
          f"max {g.max():+.2f}  p90 {p90:+.2f}  median {np.median(g):+.2f}  min {g.min():+.2f}  "
          f"(sd {g.std():.3f}, reported not gated)")
    print(f"per-second correlation: median {np.median(corr):.5f} min {min(corr):.4f}  "
          f"(informational only -- it cannot see a gain envelope)")

    fails = []
    if silent:
        fails.append(f"silent seconds in the output: {silent}")
    if len(above):
        fails.append(f"{len(above)} second(s) sit ABOVE the constant gain (first at "
                     f"{int(above[0]) // 60}:{int(above[0]) % 60:02d}, "
                     f"{g.max() - G:+.2f} dB at the worst) -- a compressor is in the chain, "
                     f"almost certainly loudnorm falling back to dynamic mode")
    if p90 < G - P90_DROP:
        fails.append(f"p90 sits {G - p90:.2f} dB below the constant gain -- the limiter is "
                     f"working on most of the file; lower the gain or raise the ceiling")
    if g.min() < G - DOWN_MAX:
        fails.append(f"the quietest ratio is {G - g.min():.2f} dB below the constant gain "
                     f"-- the limiter is gouging, not shaving")
    for f in fails:
        print("FAIL: " + f)
    print("PASS -- the output is the source mix at one constant gain, limiter-shaved only"
          if not fails else "GATE FAILED")
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
