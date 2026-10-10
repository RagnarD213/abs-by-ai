"""RO-07 round 1b: voice AUDITIONS for Dan (he rejected the first minute's sound). The same 31 s of the cut, lav only,
four ways, each finished by the shared chain's own finisher (voice_chain.py --finish-only: measured gain + limiter to
-14 LUFS), so they are level matched. Auditions only: the option he picks becomes a flag on voice_chain.py next round
(the delivered file still goes through the shared chain and the audio gate)."""
import sys, os, subprocess, wave, json, numpy as np
A = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"; sys.path.insert(0, A)
from dereverb import dereverb
W = "/Volumes/Extreme/_edit_work/ro07"; O = f"{W}/round1b/audio"; os.makedirs(O, exist_ok=True)
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FM = f"{W}/round1/first-minute/DRAFT - RO-07 round 1 - first minute.mp4"; T0, D = 13.8, 31.0; SR = 48000
wv = wave.open(FM + ".untreated.wav"); x = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
x = x[int(T0*SR):int((T0+D)*SR)]
def wav(path, y):
    o = wave.open(path, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(y, -1, 1)*32767).astype("<i2").tobytes()); o.close()
WARM = "highpass=f=70,equalizer=f=140:t=q:w=1.0:g=+1.5,equalizer=f=450:t=q:w=1.2:g=-3.0,equalizer=f=3200:t=q:w=1.5:g=-1.0"
OPTS = {
 "2-natural":        dict(af="highpass=f=70", derev=None, what="The lav as recorded. Only the rumble below your voice is removed."),
 "3-warm":           dict(af=WARM, derev=None, what="A gentle tone shape: a little more body, less boxiness, the top end left alone. Nothing between words is touched."),
 "4-warm-less-room": dict(af=WARM, derev=dict(alpha=0.30, floor_db=-10.0), what="Option 3 plus a light pass that takes some of the kitchen echo off (the same light setting you approved on the website video)."),
}
out = {}
for k, o in OPTS.items():
    y = dereverb(x, sr=SR, **o["derev"]) if o["derev"] else x
    wav(f"{O}/_{k}.mono.wav", y)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{O}/_{k}.mono.wav", "-af", o["af"] + ",pan=stereo|c0=c0|c1=c0", "-c:a", "pcm_s16le", f"{O}/_{k}.st.wav"], check=True)
    r = subprocess.run(["python3", f"{A}/voice_chain.py", "--in", f"{O}/_{k}.st.wav", "--out", f"{O}/{k}.wav", "--finish-only", "--work", f"{O}/_{k}.work"], capture_output=True, text=True)
    assert os.path.exists(f"{O}/{k}.wav"), (k, r.stdout[-400:], r.stderr[-400:])
    out[k] = o["what"]; print("built", k, flush=True)
subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", str(T0), "-t", str(D), "-i", FM, "-vn", "-c:a", "pcm_s16le", f"{O}/1-as-delivered.wav"], check=True)
out["1-as-delivered"] = "What you heard in the first minute: fitted tone curve (it added 5 dB of treble) and a gate between words."
json.dump(out, open(f"{O}/options.json", "w"), indent=1)
