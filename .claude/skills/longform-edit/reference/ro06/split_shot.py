"""Add a pure reframe cut inside one shot (nothing removed, the output timeline does not move): the shot is split at the
quietest 40 ms between two output times. usage: split_shot.py SHOT_ID T_LO T_HI   (idempotent: SHOT_ID+'b' is the second half)"""
import sys, json, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro06"; FPS = 30000/1001; SR = 48000
sid, lo, hi = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
S = json.load(open(f"{W}/shots.json"))
if any(s["id"] == sid + "b" for s in S): print("already split:", sid); sys.exit(0)
k = next(i for i, s in enumerate(S) if s["id"] == sid); s = S[k]
assert s["out_f0"]/FPS + 1.0 < lo < hi < s["out_f1"]/FPS - 1.0, "split must sit inside the shot"
wv = wave.open(f"{W}/lav.wav"); src = lambda t: s["src_f0"]/FPS + t - s["out_f0"]/FPS
wv.setpos(int(src(lo)*SR)); A = np.frombuffer(wv.readframes(int((hi-lo)*SR)), np.int16).astype(np.float32)/32768
n = int(0.04*SR); hop = int(0.005*SR)
e = [(float(np.mean(A[i:i+n]**2)), i) for i in range(0, max(1, len(A)-n), hop)]
t = lo + (min(e)[1] + n/2)/SR; f = int(round(t*FPS)); cut_src = s["src_f0"] + f - s["out_f0"]
a = dict(s, src_f1=cut_src, out_f1=f); b = dict(s, id=sid + "b", src_f0=cut_src, out_f0=f, reframe=True, split_of=sid)   # split_of: the voice track is still cut as one shot
S[k:k+1] = [a, b]; json.dump(S, open(f"{W}/shots.json", "w"), indent=1)
print(f"split {sid} at {f/FPS:.3f} s (frame {f}); {len(S)} shots")
