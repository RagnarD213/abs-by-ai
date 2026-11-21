#!/usr/bin/env python3
"""SL-06 round 2 review clips: for each pickup short, the opening through 3 s past the pickup join (from the delivered
1080x1920 file, scaled to 540p), and short D's opening with the two pickup treatments (A: the fitted EQ that is built,
B: the film's own voice chain EQ + bass), same picture, same level.
  make_joins.py      -> round2/joins/<S>_join.mp4, round2/joins/D_voiceA.mp4, D_voiceB.mp4"""
import os, subprocess, sys, wave, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plans as P, batch as Bt
import importlib.util as _iu
_sp = _iu.spec_from_file_location("sl06_deliver", os.path.join(HERE, "deliver.py")); Dl = _iu.module_from_spec(_sp); _sp.loader.exec_module(Dl)
FF = Bt.lib.FF; J = Bt.WORK + "/round2/joins"; os.makedirs(J, exist_ok=True)
def clip(src, t1, out, audio=None):
    cmd = [FF, "-nostdin", "-v", "error", "-y", "-i", src] + (["-i", audio] if audio else []) + ["-t", f"{t1:.3f}", "-vf", "scale=540:960:flags=lanczos",
           "-map", "0:v", "-map", "1:a" if audio else "0:a", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
for S in P.PICKUP:
    h = Bt.head(S); clip(Dl.dname(S), h + 3.0, f"{J}/{S}_join.mp4"); print(S, "join clip to", round(h + 3, 2))
# D: the same opening with the alternative pickup treatment laid over the built audio's pickup span
def rd(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1, w.getnchannels()); return x, w.getframerate()
a, sr = rd(f"{Bt.D('D')}/audio.wav"); alt, _ = rd(f"{Bt.WORK}/pickups/alt_filmeq/D.wav"); cur, _ = rd(f"{Bt.WORK}/pickups/D.wav")
assert len(alt) == len(cur), (len(alt), len(cur))
b = a.copy(); n = len(alt)
assert np.abs(a[:n].astype(int) - cur.astype(int)).max() <= 2, "the built audio does not start with pickups/D.wav"
b[:n] = alt
w = wave.open(f"{J}/D_audioB.wav", "w"); w.setnchannels(b.shape[1]); w.setsampwidth(2); w.setframerate(sr); w.writeframes(b.tobytes()); w.close()
clip(Dl.dname("D"), Bt.head("D") + 4.0, f"{J}/D_voiceA.mp4")
clip(Dl.dname("D"), Bt.head("D") + 4.0, f"{J}/D_voiceB.mp4", audio=f"{J}/D_audioB.wav")
print("D voice A/B done")
