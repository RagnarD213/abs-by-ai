#!/usr/bin/env python3
"""Spectral dereverberation (moved unchanged from shorts/reference/spray-tan/dereverb.py, 2026-09-02;
that file is now a shim). Originally for the 8/3 shoot's kitchen-doorway rolls.

⚠ WHY THIS EXISTS. Dan rejected the spray-tan shorts' audio on 2026-09-02 and attributed it to
the two-mic fault. It was NOT that - measured, the delivered file correlates +0.9912 with the
source's RIGHT channel through the same EQ (left 0.60, sum 0.69), so the single-mic fix was
applied correctly. The real, measurable gap against his reference ad is ROOM:

    early decay time (ms to fall 20 dB after a speech offset)
      Muhammad's ad   40 ms   (37 ms high-passed at 250 Hz, so it is a genuinely dry voice,
                               not a floor filled by a music bed - that was tested and ruled out)
      our short       85 ms   (87 ms high-passed)

Neither EQ nor a noise gate can fix that: the reverb is inside the words, not between them, and
a broadband expander only reached 63 ms and started pumping at 0.6 dB.

METHOD - spectral subtraction of the LATE field, the standard approach. In each frequency bin the
late reverberation at time t is modelled as a scaled copy of the same bin a little earlier:

    Rev[k,t] = alpha * max( |X[k, t-d1 .. t-d2]| )

and a Wiener-style gain removes it with a floor so the result cannot go negative or turn into
musical noise:

    G[k,t] = max( floor, 1 - Rev[k,t] / (|X[k,t]| + eps) )

`d1` is the start of the late field (direct sound and early reflections are KEPT - they are what
makes a voice sound close), `alpha` is how much of the tail to remove, `floor` bounds the damage.
"""
import sys
import numpy as np

def dereverb(x, sr=48000, n_fft=1024, hop=192, alpha=0.62, d1_ms=22, d2_ms=70,
             floor_db=-14.0, smooth=0.35):
    w = np.hanning(n_fft).astype(np.float64)
    pad = n_fft
    xp = np.concatenate([np.zeros(pad), x.astype(np.float64), np.zeros(pad + n_fft)])
    n = 1 + (len(xp) - n_fft) // hop
    idx = np.arange(n_fft)[None, :] + (np.arange(n) * hop)[:, None]
    X = np.fft.rfft(xp[idx] * w, axis=1)
    M = np.abs(X)
    d1 = max(1, int(d1_ms / 1000 * sr / hop))
    d2 = max(d1 + 1, int(d2_ms / 1000 * sr / hop))
    # running max of |X| over the lag window [t-d2, t-d1]
    Rev = np.zeros_like(M)
    for lag in range(d1, d2 + 1):
        sh = np.empty_like(M); sh[:lag] = 0.0; sh[lag:] = M[:-lag]
        np.maximum(Rev, sh, out=Rev)
    Rev *= alpha
    fl = 10 ** (floor_db / 20)
    G = np.maximum(fl, 1.0 - Rev / (M + 1e-12))
    # smooth the gain across time so it cannot chatter (musical noise)
    if smooth > 0:
        for t in range(1, len(G)):
            G[t] = smooth * G[t - 1] + (1 - smooth) * G[t]
    Y = X * G
    y = np.zeros(len(xp)); wsum = np.zeros(len(xp))
    frames = np.fft.irfft(Y, axis=1) * w
    for t in range(n):
        s = t * hop
        y[s:s + n_fft] += frames[t]
        wsum[s:s + n_fft] += w ** 2
    y = y[pad:pad + len(x)] / np.maximum(1e-9, wsum[pad:pad + len(x)])
    return y.astype(np.float32)

if __name__ == '__main__':
    import wave
    src, dst = sys.argv[1], sys.argv[2]
    kw = {k: float(v) for k, v in (a.split('=') for a in sys.argv[3:])}
    w = wave.open(src)
    sr, nch, sw, nfr = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
    # ⚠ THE WAV IS STEREO (dual-mono) AND MUST BE DE-INTERLEAVED FIRST. Reading it as one
    # stream treats L,R,L,R as consecutive samples - a zero-order hold that acts as a brutal
    # lowpass. It cost a whole render: the finished shorts came back 11-16 dB down above
    # 450 Hz, and the byte-size check could not see it because a mono file with twice the
    # frames is exactly the same size. Frame COUNT and CHANNEL COUNT are what to assert.
    if sw != 2:
        raise SystemExit(f'{src}: expected 16-bit PCM, got {sw*8}-bit')
    raw = np.frombuffer(w.readframes(nfr), np.int16).astype(np.float64) / 32768.
    w.close()
    ch = raw.reshape(-1, nch)
    out = np.stack([dereverb(ch[:, c], sr=sr, **kw) for c in range(nch)], axis=1)
    assert out.shape == ch.shape, f'dereverb changed shape {ch.shape} -> {out.shape}'
    o = wave.open(dst, 'w'); o.setnchannels(nch); o.setsampwidth(2); o.setframerate(sr)
    o.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).ravel().tobytes()); o.close()
    print(f"{src} -> {dst}  {nfr/sr:.2f}s  {nch}ch (preserved)")
