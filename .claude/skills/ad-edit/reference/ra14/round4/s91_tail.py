#!/usr/bin/env python3
"""RA-14 round 4: smooth the two rests in the music bed after the last word, on the approved mix itself.

WHY ON THE MIX AND NOT THE BED (s42_bed.py's route). mix_bass_r3.wav was loudness-normalised over the whole file by
voice_chain.py (gain 9.8 dB). Re-running the chain with a corrected bed would move that gain by a hundredth of a dB and
change every sample of the approved voice. After the last word ("started.", ends 48.365 s) the mix is the bed alone,
ducking released, under the chain's linear 2 s fade, with the limiter idle (bed near -38 dBFS). So the same
inverse-envelope gain s42_bed.py applies to the bed can be applied to the mix from TAIL_IN on, and every sample before
TAIL_IN stays the approved one, bit for bit (checked below: integer null test).

MEASURED (50 ms windows, the chain's fade divided out, 48.45-50.00 s): span 15.7 dB, the two rests at 49.25 s and
49.65 s. RA-01's tail measured 15 dB the same way before its bed fix and 4.5 dB after (approved).

  python3 round4/s91_tail.py   (run from /Volumes/Extreme/_edit_work/ra14)  -> round4/mix_bass_r4.wav + round4/tail_fix.json
"""
import json, subprocess, sys, wave
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import ra01lib as L

SRC, OUT, REP = "mix_bass_r3.wav", "round4/mix_bass_r4.wav", "round4/tail_fix.json"
SR = 48000
LAST_WORD_END = 48.365
TAIL_IN = 48.42          # first sample that may change: after the word's decay
RAMP = 0.20              # raised-cosine blend 1.0 -> full correction over TAIL_IN .. TAIL_IN+RAMP
WIN = 0.010              # s42_bed.py's envelope window
GAIN_SMOOTH = 3          # blocks -> 30 ms, as s42_bed.py
GAIN_MAX_DB, GAIN_MIN_DB = 14.0, -10.0
FADE_S = 2.0             # voice_chain.py's linear fade-out to the last sample

raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", SRC, "-f", "s32le", "-acodec", "pcm_s32le", "-"],
                     capture_output=True, check=True).stdout
xi = np.frombuffer(raw, np.int32).reshape(-1, 2).copy()
assert not np.any(xi & 0xFF), "source is not 24-bit in 32-bit words"
x = xi.astype(np.float64) / 2**31
n = len(x); T = n / SR
mono = x.mean(1)
fade = np.clip((T - (np.arange(n) / SR)) / FADE_S, 1e-4, 1.0)      # the chain's fade, as an amplitude curve

h = int(WIN * SR); nb = n // h
env = np.sqrt(np.array([np.mean(mono[i*h:(i+1)*h]**2) for i in range(nb)]) + 1e-15)
fb = np.array([fade[min(n-1, i*h + h//2)] for i in range(nb)])
env_c = env / fb                                                       # fade divided out: the bed's own level
b0, b1 = int(TAIL_IN / WIN), int((T - 0.30) / WIN)                     # the last 0.3 s is below -55 dBFS: leave the fade
target = float(np.median(env_c[b0:b1]))
g = np.clip(target / np.maximum(env_c, 1e-12), 10**(GAIN_MIN_DB/20), 10**(GAIN_MAX_DB/20))
g = np.convolve(g, np.ones(GAIN_SMOOTH) / GAIN_SMOOTH, mode="same")
tb = (np.arange(nb) + 0.5) * WIN
w = np.clip((tb - TAIL_IN) / RAMP, 0.0, 1.0); w = 0.5 - 0.5*np.cos(np.pi*w)
w[tb > (T - 0.30)] = np.clip(1 - (tb[tb > (T - 0.30)] - (T - 0.30)) / 0.15, 0, 1)   # hand back to the plain fade
gb = 1.0 + (g - 1.0) * w
gs = np.interp(np.arange(n), tb * SR, gb)
gs[: int(TAIL_IN * SR)] = 1.0

y = x * gs[:, None]
yi = np.clip(np.round(y * 2**23), -2**23, 2**23 - 1).astype(np.int64) << 8
s0 = int(TAIL_IN * SR)
yi[:s0] = xi[:s0]                                                      # untouched: the approved samples themselves
yi = yi.astype(np.int32)

wv = wave.open(OUT, "w"); wv.setnchannels(2); wv.setsampwidth(3); wv.setframerate(SR)
b = yi.astype("<i4").view(np.uint8).reshape(-1, 4)[:, 1:].tobytes()    # top three bytes, little endian
wv.writeframes(b); wv.close()

# null test: decode the written file and compare with the approved mix
chk = np.frombuffer(subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", OUT, "-f", "s32le", "-acodec", "pcm_s32le", "-"],
                                   capture_output=True, check=True).stdout, np.int32).reshape(-1, 2)
assert len(chk) == n, (len(chk), n)
diff = np.nonzero(np.any(chk != xi, axis=1))[0]
first_diff = float(diff[0] / SR) if len(diff) else None

def span(sig, a, bb, step=0.05):
    v = []
    for t in np.arange(a, bb, step):
        s = sig[int(t*SR):int((t+step)*SR)]
        f = max(1e-4, 1 - max(0.0, (t + step/2 - (T - FADE_S))) / FADE_S)
        v.append(20*np.log10(np.sqrt(np.mean(s**2)) + 1e-15) - 20*np.log10(f))
    return round(max(v) - min(v), 1), [round(z, 1) for z in v]
before, env_b = span(mono, 48.45, 50.0)
after, env_a = span((chk.astype(np.float64) / 2**31).mean(1), 48.45, 50.0)
rep = dict(src=SRC, out=OUT, last_word_end=LAST_WORD_END, tail_in=TAIL_IN, ramp=RAMP, target_dbfs=round(20*np.log10(target), 1),
           gain_db=dict(min=round(float(20*np.log10(gs[s0:].min())), 1), max=round(float(20*np.log10(gs[s0:].max())), 1)),
           identical_before_s=first_diff, samples=n,
           span_fade_corrected_50ms=dict(before=before, after=after, window=[48.45, 50.0]), env_before=env_b, env_after=env_a)
json.dump(rep, open(REP, "w"), indent=1)
print(f"first differing sample at {first_diff} s (must be >= 47.0)")
print(f"tail span 48.45-50.00 s, fade divided out: BEFORE {before} dB  AFTER {after} dB  (RA-01: 15 -> 4.5)")
print(f"gain applied {rep['gain_db']}")
assert first_diff is None or first_diff >= 47.0
