#!/usr/bin/env python3
"""WHICH TAKE is his audio on, per picture segment. The instrument that settles a conform argument.

The picture matcher (pic.json) cannot separate two takes of the same words where Dan barely moves and is small
under a graphic: through the 36-43 s window three instruments disagreed by up to 20 frames, and the EDL sat on a
take whose words matched but whose pictures were somebody else's moment. His AUDIO settles it, because a take is
a different performance even when the words and pace are identical.

⚠ Two traps, both paid for here:
  * the raw roll carries TWO MICS 7.88 ms apart and POLARITY INVERTED (pair corr -0.80, raw.audio_source.json).
    "-ac 1" downmixes them and cancels the voice: every segment then scores ~0.0-0.16 and reads as a wrong take,
    including ones that are certainly right. Use the LAV CHANNEL alone.
  * WAVEFORM correlation does not survive his mix (EQ, compression, limiter) -- it stays at noise even on the lav.
    Correlate the AMPLITUDE ENVELOPE (300-3400 Hz, rectified, 20 ms smoothing, decimated to ~200 Hz) instead.
Validated on a segment known right from the picture (3966-4285, off 2486, pic r 0.97 over 303 samples): the
envelope finds 2485, one frame away, at corr 0.880.

    python3 ztake.py [n_from n_to]
"""
import json, subprocess, sys
import numpy as np

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001
SR = 16000
DEC = 80                      # envelope sample rate = SR/DEC = 200 Hz
SEARCH = 45.0                 # seconds either side of our offset


def pcm(path, t0, dur, lav=False):
    cmd = [FF, "-v", "error", "-ss", f"{max(0.0, t0):.4f}", "-i", path, "-t", f"{dur:.4f}", "-vn"]
    cmd += ["-af", "pan=mono|c0=c0"] if lav else ["-ac", "1"]
    cmd += ["-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, dtype=np.float32).copy()


def env(x):
    if len(x) < 512: return np.zeros(0, np.float32)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1/SR)
    X[(f < 300) | (f > 3400)] = 0
    y = np.abs(np.fft.irfft(X, n=len(x)))
    w = int(SR*0.02)
    return np.convolve(y, np.ones(w)/w, mode='same')[::DEC]


def z(a):
    a = a - a.mean(); s = float(np.sqrt((a*a).sum())); return a/max(s, 1e-9)


def main():
    E = json.load(open('edl_picture.json'))
    a_n, b_n = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, 10**9)
    print(f"{'segment':>13} {'dur':>5} {'ours':>7} {'corr':>6}   {'his audio':>9} {'corr':>6}  {'delta':>7}  verdict")
    bad = []
    for s in E:
        if s['n1'] <= a_n or s['n0'] >= b_n: continue
        dur = (s['n1'] - s['n0'])/FPS
        if dur < 1.0: continue
        t0 = s['n0']/FPS; off = s['off']
        h = z(env(pcm('ref/ad3_v6hd.mp4', t0, dur)))
        if len(h) < 24: continue
        lo, hi = off - SEARCH, off + SEARCH
        pad = 0.5
        r = env(pcm('raw.mp4', t0 + lo - pad, dur + (hi - lo) + 2*pad, lav=True))
        n = len(h)
        if len(r) < n + 4: continue
        best = (-2.0, 0.0)
        for k in range(0, len(r) - n, 2):
            c = float(np.dot(h, z(r[k:k+n])))
            if c > best[0]: best = (c, (lo - pad) + k*DEC/SR)
        o = z(env(pcm('raw.mp4', t0 + off, dur, lav=True))[:n])
        c_ours = float(np.dot(h, o)) if len(o) == n else float('nan')
        d = (best[1] - off)*FPS
        verdict = 'ok' if abs(d) <= 4 else ('WRONG TAKE' if best[0] - c_ours > 0.12 else 'check')
        if verdict == 'WRONG TAKE': bad.append((s['n0'], s['n1'], off*FPS, best[1]*FPS))
        print(f"{s['n0']:5d}-{s['n1']:<7d}{dur:5.2f} {off*FPS:7.1f} {c_ours:6.3f}   {best[1]*FPS:9.1f} {best[0]:6.3f}  {d:+7.1f}  {verdict}")
    print(f"\nwrong-take segments: {len(bad)}")
    for n0, n1, o, nb in bad: print(f"   {n0}-{n1}: {o:.0f} -> {nb:.0f} fr")


if __name__ == '__main__':
    main()
