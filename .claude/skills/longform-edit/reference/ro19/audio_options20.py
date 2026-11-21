"""RO-20 sound bake-off BEFORE the first minute (PRE-RENDER-APPROVAL, 'run the look and sound bake-off yourself'): the same 31 s
of the roll's lav five ways, each finished by the shared chain's finisher (level matched), plus blind copies named by letter for
the Gemini ranking. New set: the raw room measures 83 to 88 ms early decay (wet)."""
import sys, os, subprocess, wave, json, random, numpy as np
A = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"; sys.path.insert(0, A)
from dereverb import dereverb
W = "/Volumes/Extreme/_edit_work/ro19"; O = f"{W}/audio/opts"; os.makedirs(O, exist_ok=True)
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
T0, D, SR = 166.0, 31.0, 48000
wv = wave.open(f"{W}/lav/C1512.wav"); wv.setpos(int(T0*SR)); x = np.frombuffer(wv.readframes(int(D*SR)), np.int16).astype(np.float32)/32768
# Dan, 2026-10-11: an audition clip starts on speech. Refuse a window with no speech in its first 0.5 s or a pause over 1.5 s.
_db = [20*np.log10(np.sqrt(np.mean(x[i:i+2400]**2))+1e-9) for i in range(0, len(x)-2400, 2400)]            # 50 ms steps
_q = [d < -45 for d in _db]; _run = 0; _worst = 0
for q in _q: _run = _run+1 if q else 0; _worst = max(_worst, _run)
assert not all(_q[:10]) and _worst*0.05 <= 1.5, f"audition window {T0}-{T0+D} s: no speech in the first 0.5 s or a {_worst*0.05:.1f} s pause; take the window from a kept piece"
def wav(path, y):
    o = wave.open(path, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(y, -1, 1)*32767).astype("<i2").tobytes()); o.close()
WARM = "highpass=f=70,equalizer=f=140:t=q:w=1.0:g=+1.5,equalizer=f=450:t=q:w=1.2:g=-3.0,equalizer=f=3200:t=q:w=1.5:g=-1.0"
LIGHT = dict(alpha=0.30, floor_db=-10.0)
OPTS = {
 "1-untreated":         dict(af="highpass=f=70", derev=None, what="The lav as recorded. Only the rumble below the voice is removed."),
 "3-warm":              dict(af=WARM, derev=None, what="A gentle fixed tone shape (more body, less boxiness). Nothing between words is touched."),
 "4-warm-less-room":    dict(af=WARM, derev=LIGHT, what="The voice Dan picked on RO-07 (2026-10-10): the warm tone shape plus a light pass that takes some room echo off. No gate between words."),
 "5-natural-less-room": dict(af="highpass=f=70", derev=LIGHT, what="The lav with only the light room pass. No tone shaping."),
}
out = {}
for k, o in OPTS.items():
    y = dereverb(x, sr=SR, **o["derev"]) if o["derev"] else x
    wav(f"{O}/_{k}.mono.wav", y)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{O}/_{k}.mono.wav", "-af", o["af"] + ",pan=stereo|c0=c0|c1=c0", "-c:a", "pcm_s16le", f"{O}/_{k}.st.wav"], check=True)
    r = subprocess.run(["python3", f"{A}/voice_chain.py", "--in", f"{O}/_{k}.st.wav", "--out", f"{O}/{k}.wav", "--finish-only", "--work", f"{O}/_{k}.work"], capture_output=True, text=True)
    assert os.path.exists(f"{O}/{k}.wav"), (k, r.stdout[-400:], r.stderr[-400:])
    out[k] = o["what"]; print("built", k, flush=True)
# 2: the shared chain's DEFAULT on the same raw (fitted tone match + expander between words, no dereverb)
wav(f"{O}/_2.raw.wav", x)
r = subprocess.run(["python3", f"{A}/voice_chain.py", "--in", f"{O}/_2.raw.wav", "--pull", "anull", "--out", f"{O}/2-chain-default.wav", "--work", f"{O}/_2.work"], capture_output=True, text=True)
print(r.stdout[-700:], r.stderr[-500:]); assert os.path.exists(f"{O}/2-chain-default.wav")
out["2-chain-default"] = "The shared chain's default: tone matched automatically to the reference mix, plus a gate that turns the room down between words."
json.dump(out, open(f"{O}/options.json", "w"), indent=1)
keys = sorted(out); random.Random(20).shuffle(keys); blind = {}
for L, k in zip("PQRST", keys):
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{O}/{k}.wav", "-c:a", "libmp3lame", "-b:a", "192k", f"{O}/clip_{L}.mp3"], check=True)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{O}/{k}.wav", "-c:a", "libmp3lame", "-b:a", "192k", f"{O}/{k}.mp3"], check=True); blind[L] = k
json.dump(blind, open(f"{O}/blind.json", "w"), indent=1); print(blind)
