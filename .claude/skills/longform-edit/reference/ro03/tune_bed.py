"""Bed level check: run the shared chain on the assembled, roll-trimmed lav with a bed setting and read speech vs hold level.
usage: tune_bed.py BED_DB SWELL"""
import sys, os, json, subprocess, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro03"; bd, sw = sys.argv[1:3]
VC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py"
if os.path.exists(f"{W}/bed_full.wav"): os.remove(f"{W}/bed_full.wav")
subprocess.run(["python3", f"{W}/recipe/bed.py"], env=dict(os.environ, RO03_SWELL=sw), check=True, capture_output=True)
out = f"{W}/tmp/tune/t_{bd}_{sw}.wav"; eq = json.load(open(f"{W}/FIT.json"))["eq"]
r = subprocess.run(["python3", VC, "--in", f"{W}/tmp/tune/asm_trim.wav", "--out", out, "--eq", eq, "--tp", "-2.8", "--oversample", "4", "--work", f"{W}/tmp/tune/w", "--bed", f"{W}/bed_full.wav", "--bed-db", bd], capture_output=True, text=True)
print([l for l in r.stdout.splitlines() if " I " in l][-1])
w = wave.open(out); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2).mean(1)/32768
def rms(t0, t1): x = a[int(t0*sr):int(t1*sr)]; return round(float(20*np.log10(np.sqrt(np.mean(x*x))+1e-9)), 1)
print(bd, sw, "speech", rms(0.3, 5.6), rms(28.2, 52), rms(78.2, 105.9), rms(129.3, 150.9), "holds", [rms(h+1, h+19) for h in (7.45, 57.44, 107.45)])
x = a[int(28.2*sr):int(52*sr)]; n = int(0.05*sr); e = 20*np.log10(np.sqrt((x[:len(x)//n*n].reshape(-1, n)**2).mean(1))+1e-9); print("  rest1 frame pctl 5/10/50:", np.percentile(e, [5, 10, 50]).round(1))
