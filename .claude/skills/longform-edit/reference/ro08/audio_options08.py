"""RO-08 round 2 voice options (Dan, 2026-10-12: "one sounds the best, but I want a few new options ... with a little bit less
echo than that. The bass is good, the warmth is good."). Same tone as voice 1 (voice 4's fixed EQ + 1 dB at 120 Hz); only the
dereverb gets stronger. The window is taken from the CUT (film 143.2 s, "Alright so let's talk about why intermittent fasting is
superior..."), 31 s, refused unless it starts on speech and has no pause over 1.5 s. Each option: dereverb (shared module) ->
fixed EQ -> the shared finisher (level matched). Prints room decay and the gate's two damage measures against the untreated lav
and the reference. From reference/ro19/audio_options19r2.py."""
import sys, os, subprocess, wave, json, numpy as np
A = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"; sys.path.insert(0, A)
from dereverb import dereverb
import common as C
W = "/Volumes/Extreme/_edit_work/ro08"; O = f"{W}/round2/audio"; os.makedirs(O, exist_ok=True)
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SR = 48000; D = 31.0; T0 = 143.2
wv = wave.open(f"{W}/voice/film_voice.untreated.wav"); assert wv.getframerate() == SR and wv.getnchannels() == 1
wv.setpos(int(round(T0*SR))); x = np.frombuffer(wv.readframes(int(D*SR)), np.int16).astype(np.float32)/32768
_db = [20*np.log10(np.sqrt(np.mean(x[i:i+2400]**2))+1e-9) for i in range(0, len(x)-2400, 2400)]
_q = [d < -45 for d in _db]; _run = 0; _worst = 0
for q in _q: _run = _run+1 if q else 0; _worst = max(_worst, _run)
assert not all(_q[:10]) and _worst*0.05 <= 1.5, "audition window: no speech in the first 0.5 s or a long pause"
EQ = "highpass=f=70,equalizer=f=140:t=q:w=1.0:g=+1.5,equalizer=f=450:t=q:w=1.2:g=-3.0,equalizer=f=3200:t=q:w=1.5:g=-1.0,equalizer=f=120:t=q:w=0.8:g=+1.0"
OPT = {
 "1-current":     dict(derev=dict(alpha=0.30, floor_db=-10.0), what="Voice 1 as you heard it in round 1."),
 "1a-less-echo":  dict(derev=dict(alpha=0.35, floor_db=-11.0), what="Voice 1 with a step more echo removed."),
 "1b-less-echo":  dict(derev=dict(alpha=0.40, floor_db=-12.0), what="Voice 1 with two steps more echo removed."),
 "1c-less-echo":  dict(derev=dict(alpha=0.45, floor_db=-13.0), what="Voice 1 with three steps more echo removed."),
 "1d-less-echo":  dict(derev=dict(alpha=0.50, floor_db=-14.0), what="Voice 1 with four steps more echo removed."),
}
REF = json.load(open(f"{A}/reference/reference.json"))
def wav(path, y):
    o = wave.open(path, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(y, -1, 1)*32767).astype("<i2").tobytes()); o.close()
def measure(path):
    y = C.pcm(path); b, fl, dry, sp = C.analyse(y); a = C.artifacts(y)
    return dict(edt=round(C.edt(y), 1), flux=round(a["flux"], 4), swirl=round(a["swirl"], 3), tone=round(float(np.abs(b - np.array(REF["bands"])).mean()), 2), low=round(float(b[0]), 1), dry=round(dry, 2))
wav(f"{O}/_untreated.mono.wav", x); U = measure(f"{O}/_untreated.mono.wav"); print("untreated", U, flush=True)
out = {"untreated": U}
for k, o in OPT.items():
    y = dereverb(x, sr=SR, **o["derev"]); wav(f"{O}/_{k}.mono.wav", y)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{O}/_{k}.mono.wav", "-af", EQ + ",pan=stereo|c0=c0|c1=c0", "-c:a", "pcm_s16le", f"{O}/_{k}.st.wav"], check=True)
    r = subprocess.run(["python3", f"{A}/voice_chain.py", "--in", f"{O}/_{k}.st.wav", "--out", f"{O}/{k}.wav", "--finish-only", "--work", f"{O}/_{k}.work"], capture_output=True, text=True)
    assert os.path.exists(f"{O}/{k}.wav"), (k, r.stdout[-400:], r.stderr[-400:])
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{O}/{k}.wav", "-c:a", "libmp3lame", "-b:a", "192k", f"{O}/{k}.mp3"], check=True)
    m = measure(f"{O}/{k}.wav"); m["flux_vs_ref"] = round(m["flux"]/REF["flux"], 2); m["swirl_vs_untreated"] = round(m["swirl"]/U["swirl"], 2)
    m["inside_limits"] = bool(m["flux_vs_ref"] <= 1.10 and m["swirl_vs_untreated"] <= 1.35); print(k, m, flush=True); out[k] = dict(what=o["what"], derev=o["derev"], **m)
print("reference: edt", REF["edt_ms"], "flux", REF["flux"], "swirl", REF["swirl"], "| limits: flux <= reference x1.10, swirl <= untreated x1.35")
json.dump(out, open(f"{O}/options.json", "w"), indent=1)
