#!/usr/bin/env python3
"""ROUND 3, plan section 13: the music bed's own 15 dB step at ~56.06 s.

DIAGNOSIS (measured, not assumed). The step is not a join and not the aloop seam -- `Realizer.mp3`
is 310 s long and the bed starts at t=0, so bed time == mix time. The track's own rhythm leaves a
~0.10 s gap between phrases roughly once a second: 55.00, 55.95, 56.95 s read -26 .. -28 dBFS
against a -13 dBFS median. Under speech those gaps are masked and ducked; after the last word
(55.2 s) the bed is the only thing left, so the gap at 55.94-56.06 and the note onset that follows
it read as a dropout and a ~15 dB step. Every other offset in the track has the same pattern (a
250 s sweep: the smoothest 3.7 s window anywhere still dips 13.1 dB), so re-picking the bed's start
does not fix it, and the chain's linear 2 s fade-out does not either -- a fade scales the gap, it
does not remove it.

THE FIX IS IN THE BED ASSET, NOT IN THE CHAIN. `voice_chain.py` stays exactly as it is (it is the
one shared chain; nothing here processes the voice, the loudness or the L/R image). This writes a
bed FILE whose level is held constant across the exposed tail: the track's own short-term envelope
is measured and the inverse gain applied from TAIL_IN onward, ramped in over RAMP seconds so the
correction itself has no step. The chain then does what it always does -- loop, -32 dB, 1.5 s fade
in, 2 s fade out, sidechain duck -- and the bed holds level and then fades smoothly to the last
frame.
"""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L

SRC = os.environ.get("BED_SRC", "music/Realizer.mp3")
OUT = os.environ.get("BED_OUT", "music/Realizer_r3bed.wav")
SR = 48000
KEEP = 62.0          # seconds written (the cut is 57.19 s; the chain atrims what it needs)
TAIL_IN = 53.20      # full correction from here -- under speech, 2.0 s before the last word
RAMP = 1.20          # gain ramps 1.0 -> full correction over TAIL_IN-RAMP .. TAIL_IN
# ⚠ THE WINDOW AND THE SMOOTHING ARE THE WHOLE FIX. The rests are ~0.10 s long, so a 50 ms envelope
# smoothed over 250 ms (the first attempt) spreads the correction across five times the hole and
# recovers almost nothing: tail span 17.6 -> 16.8 dB. A 10 ms envelope with the GAIN smoothed over
# 30 ms fills the hole and still moves gently: 17.6 -> 4.5 dB. Measured, not guessed.
WIN = 0.010          # envelope window
GAIN_SMOOTH = 3      # blocks -> 30 ms on the gain curve
GAIN_MAX_DB = 14.0
GAIN_MIN_DB = -10.0

raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", SRC, "-ac", "2", "-ar", str(SR),
                      "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
x = x[:int(KEEP*SR)]
n = len(x)
mono = x.mean(1)

# short-term RMS envelope on a WIN grid, then smoothed so the gain curve is itself gentle
h = int(WIN*SR)
nb = n//h
env_s = np.sqrt(np.array([np.mean(mono[i*h:(i+1)*h]**2) for i in range(nb)]) + 1e-12)

b0 = int(TAIL_IN/WIN)
target = float(np.median(env_s[b0:min(nb, int(58.0/WIN))]))   # the level the tail should hold
g = np.clip(target/np.maximum(env_s, 1e-9),
            10**(GAIN_MIN_DB/20), 10**(GAIN_MAX_DB/20))
k = GAIN_SMOOTH
g = np.convolve(g, np.ones(k)/k, mode="same")           # no step in the correction itself

# blend: 1.0 before TAIL_IN-RAMP, g from TAIL_IN on, raised-cosine in between
t_b = (np.arange(nb)+0.5)*WIN
w = np.clip((t_b - (TAIL_IN-RAMP))/RAMP, 0.0, 1.0)
w = 0.5 - 0.5*np.cos(np.pi*w)
gb = 1.0 + (g - 1.0)*w

# per-sample gain by linear interpolation of the block curve
gs = np.interp(np.arange(n), (np.arange(nb)+0.5)*h, gb).astype(np.float32)
y = np.clip(x * gs[:, None], -1.0, 1.0)

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
import wave
wv = wave.open(OUT, "w"); wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR)
wv.writeframes((y*32767).astype(np.int16).tobytes()); wv.close()

def env_db(sig, t0, t1, step=0.05):
    out = []
    for t in np.arange(t0, t1, step):
        s = int(t*SR); seg = sig[s:s+int(step*SR)]
        out.append((round(float(t), 3), round(float(20*np.log10(np.sqrt(np.mean(seg**2))+1e-12)), 1)))
    return out
before = env_db(mono, 53.0, 58.0)
after = env_db(y.mean(1), 53.0, 58.0)
def stats(e, a, b):
    v = [d for t, d in e if a <= t < b]
    return dict(min=min(v), max=max(v), span=round(max(v)-min(v), 1))
rep = dict(src=SRC, out=OUT, target_rms_dbfs=round(20*np.log10(target+1e-12), 2),
           tail_in=TAIL_IN, ramp=RAMP, gain_db_range=[GAIN_MIN_DB, GAIN_MAX_DB],
           gain_applied_db=dict(min=round(float(20*np.log10(gb[b0:min(nb,int(57.3/WIN))].min())),2), max=round(float(20*np.log10(gb[b0:min(nb,int(57.3/WIN))].max())),2)),
           before=stats(before, 53.5, 57.3), after=stats(after, 53.5, 57.3),
           before_env=before, after_env=after)
json.dump(rep, open("r3/bed_fix.json", "w"), indent=1)
print(f"bed -> {OUT}  ({len(y)/SR:.1f}s)")
print(f"tail 53.5-57.3 s envelope span: BEFORE {rep['before']['span']} dB  AFTER {rep['after']['span']} dB")
print(f"  before min {rep['before']['min']} max {rep['before']['max']} | "
      f"after min {rep['after']['min']} max {rep['after']['max']}")
