#!/usr/bin/env python3
"""RA-07 round 3: smooth the music bed after the last word on the approved mix, and frame-lock it to the picture.
(RA-14 round 4 s91_tail.py, for this 16-bit mix.)

After "step." (ends 51.70 s) the mix is the bed alone under voice_chain.py's 2 s linear fade. Measured (50 ms, fade divided
out): the bed holds about -40 dBFS with one rest at 52.10-52.15 s (-53 to -56, about 14 dB down). The same inverse-envelope
gain as s91 is applied from TAIL_IN on; every sample before TAIL_IN is the approved mix_bass.wav sample (null-tested).
Frame-lock: mix_bass.wav is 46 samples (0.96 ms) shorter than the 1579-frame picture; zeros are appended to exactly
1579 * 1001/30000 s. (voice_chain.py --frame-lock would re-run the whole chain and move every voice sample.)

  python3 round3/s91_tail07.py    -> round3/mix_bass_r3.wav + round3/tail_fix.json
"""
import json, wave
import numpy as np

SRC, OUT, REP = "mix_bass.wav", "round3/mix_bass_r3.wav", "round3/tail_fix.json"
SR = 48000; FRAMES = 1579
NEED = round(FRAMES * 1001 / 30000 * SR)
LAST_WORD_END, TAIL_IN, RAMP, WIN, GAIN_SMOOTH = 51.70, 51.76, 0.20, 0.010, 3
GAIN_MAX_DB, GAIN_MIN_DB, FADE_S = 14.0, -10.0, 2.0

w = wave.open(SRC); assert w.getsampwidth() == 2 and w.getnchannels() == 2 and w.getframerate() == SR
xi = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).copy(); w.close()
n0 = len(xi); T0 = n0 / SR
x = xi.astype(np.float64) / 32768; mono = x.mean(1)
fade = np.clip((T0 - np.arange(n0) / SR) / FADE_S, 1e-4, 1.0)
h = int(WIN * SR); nb = n0 // h
env = np.sqrt(np.array([np.mean(mono[i*h:(i+1)*h]**2) for i in range(nb)]) + 1e-15)
fb = np.array([fade[min(n0-1, i*h + h//2)] for i in range(nb)])
env_c = env / fb
b0, b1 = int(TAIL_IN / WIN), int((T0 - 0.30) / WIN)
target = float(np.median(env_c[b0:b1]))
g = np.clip(target / np.maximum(env_c, 1e-12), 10**(GAIN_MIN_DB/20), 10**(GAIN_MAX_DB/20))
g = np.convolve(g, np.ones(GAIN_SMOOTH) / GAIN_SMOOTH, mode="same")
tb = (np.arange(nb) + 0.5) * WIN
wt = np.clip((tb - TAIL_IN) / RAMP, 0, 1); wt = 0.5 - 0.5*np.cos(np.pi*wt)
late = tb > (T0 - 0.30); wt[late] = np.clip(1 - (tb[late] - (T0 - 0.30)) / 0.15, 0, 1)
gs = np.interp(np.arange(n0), tb * SR, 1.0 + (g - 1.0) * wt); s0 = int(TAIL_IN * SR); gs[:s0] = 1.0
y = np.clip(np.round(x * gs[:, None] * 32768), -32768, 32767).astype(np.int16)
y[:s0] = xi[:s0]
y = np.vstack([y, np.zeros((NEED - n0, 2), np.int16)])
wv = wave.open(OUT, "w"); wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes(y.tobytes()); wv.close()

chk = np.frombuffer(wave.open(OUT).readframes(NEED), np.int16).reshape(-1, 2)
diff = np.nonzero(np.any(chk[:n0] != xi, axis=1))[0]
first = float(diff[0] / SR) if len(diff) else None
def span(sig, a, b, T, step=0.05):
    v = []
    for t in np.arange(a, b, step):
        s = sig[int(t*SR):int((t+step)*SR)]; f = max(1e-4, min(1.0, (T - t - step/2) / FADE_S))
        v.append(20*np.log10(np.sqrt(np.mean(s**2)) + 1e-15) - 20*np.log10(f))
    return round(max(v) - min(v), 1), [round(z, 1) for z in v]
bef, eb = span(mono, TAIL_IN, T0 - 0.30, T0); aft, ea = span(chk[:n0].astype(float).mean(1) / 32768, TAIL_IN, T0 - 0.30, T0)
rep = dict(src=SRC, out=OUT, samples=NEED, padded=NEED - n0, last_word_end=LAST_WORD_END, tail_in=TAIL_IN, first_diff_s=first,
           target_dbfs=round(20*np.log10(target), 1), span_before_db=bef, span_after_db=aft, env_before=eb, env_after=ea,
           gain_db=[round(float(20*np.log10(gs[s0:].min())), 1), round(float(20*np.log10(gs[s0:].max())), 1)])
json.dump(rep, open(REP, "w"), indent=1)
print(f"first differing sample {first} s (>= {TAIL_IN}); padded {NEED - n0}; tail span {bef} -> {aft} dB; gain {rep['gain_db']}")
assert first is None or first >= TAIL_IN
