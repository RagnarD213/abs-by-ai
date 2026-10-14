#!/usr/bin/env python3
"""Rubber Band time-stretch (pitch and formants kept), offline, R3 'finer' engine.  Run with ~/.cache/absbyai/rbvenv/bin/python.
  rb_stretch.py IN.wav OUT.wav SPEED [smooth]
RA-05 round 2: ffmpeg atempo at 1.06x was heard as smeared consonants in two blind listens (scored 4 against 9)."""
import sys, wave, numpy as np, pylibrb as R
src, dst, sp = sys.argv[1], sys.argv[2], float(sys.argv[3])
w = wave.open(src); sr = w.getframerate(); ch = w.getnchannels()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, ch).T / 32768.0
O = R.Option
opts = O.PROCESS_OFFLINE | O.ENGINE_FINER | O.FORMANT_PRESERVED | O.CHANNELS_TOGETHER | O.PitchHighQuality
if len(sys.argv) > 4 and sys.argv[4] == "smooth": opts |= O.TRANSIENTS_SMOOTH | O.WINDOW_LONG
st = R.RubberBandStretcher(sample_rate=sr, channels=ch, options=opts, initial_time_ratio=1.0/sp)
st.set_expected_input_duration(x.shape[1])
BL = 4096; n = x.shape[1]
for i in range(0, n, BL):                      # offline: study the whole input first, in blocks
    st.study(x[:, i:i+BL], final=(i + BL >= n))
outs = []
for i in range(0, n, BL):
    st.process(x[:, i:i+BL], final=(i + BL >= n))
    outs.append(st.retrieve_available())
while not st.is_done():
    outs.append(st.retrieve_available())
outs.append(st.retrieve_available())
y = np.concatenate([o for o in outs if o.shape[1]], axis=1)
y = np.clip(y, -1, 1)
wo = wave.open(dst, "w"); wo.setnchannels(ch); wo.setsampwidth(2); wo.setframerate(sr)
wo.writeframes((y.T * 32767).astype(np.int16).tobytes()); wo.close()
print(f"rubberband {sp}x: {x.shape[1]/sr:.3f}s -> {y.shape[1]/sr:.3f}s (expected {x.shape[1]/sr/sp:.3f})")
