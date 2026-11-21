"""RO-37 voice options (PRE-RENDER-APPROVAL step 3): the film's first 30 s of assembled voice, four ways, level matched by
the shared chain. A/B/C/D are the pool set's options from DS-76 (Dan chose A, Natural Warmth, on DS-84, DS-47 and DS-76).
Reference for the blind listener: 30 s of the approved DS-84 Short (same pool, same day, same lav)."""
import sys, os, subprocess, wave, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
W = B.W; O = f"{W}/options/voice"; os.makedirs(O, exist_ok=True); FF = B.FF; SR = 48000
T0, D = 0.0, 30.0
wv = wave.open(f"{W}/assembled_untreated.wav"); wv.setpos(int(T0*SR)); x = np.frombuffer(wv.readframes(int(D*SR)), np.int16).astype(np.float32)/32768
lv = [20*np.log10(np.sqrt(np.mean(x[i:i+960]**2))+1e-9) for i in range(0, len(x)-960, 960)]
first = next(i for i, v in enumerate(lv) if v > -40) * 0.02; run = best = 0
for v in lv: run = run + 1 if v < -45 else 0; best = max(best, run)
print("speech starts", round(first, 2), "s; longest pause", round(best*0.02, 2), "s"); assert first <= 0.5 and best*0.02 <= 1.5
o = wave.open(f"{O}/_raw.wav", "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(x, -1, 1)*32767).astype("<i2").tobytes()); o.close()
out = {}
for k, (name, eq) in B.VOICES.items():
    B.voice(f"{O}/_raw.wav", f"{O}/{k}.wav", k)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{O}/{k}.wav", "-c:a", "libmp3lame", "-b:a", "192k", f"{O}/{k}.mp3"], check=True)
    out[k] = name; print("built", k, name, flush=True)
REF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content/DS-84 How To Do Hamstring Curls/How To Do Hamstring Curls SFC R3 - complete Short.mp4"
subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", "8", "-t", "30", "-i", REF, "-vn", "-c:a", "libmp3lame", "-b:a", "192k", f"{O}/_reference.mp3"], check=True)
json.dump(out, open(f"{O}/options.json", "w"), indent=1)
