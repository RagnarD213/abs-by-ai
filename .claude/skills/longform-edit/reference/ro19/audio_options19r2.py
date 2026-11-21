"""RO-19 round 2 voice options (Dan, 2026-10-11: "four warm, less room-echo options, and ... a few options for slightly more bass
in my voice to make it sound more authoritative"). The window is taken from the CUT (the film's assembled untreated lav at the
start of the kept piece 'photos', film 25.99 s: "if you guys want to look good in photos"), 31 s, refused unless it starts on
speech and has no pause over 1.5 s. Each option: dereverb (shared module) -> fixed EQ -> the shared finisher (level matched).
Prints room decay (EDT), the two gated damage measures against the untreated lav and the reference, and tone distance.
usage: audio_options19r2.py warm | bass <warm key>"""
import sys, os, subprocess, wave, json, numpy as np
A = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"; sys.path.insert(0, A)
from dereverb import dereverb
import common as C
W = "/Volumes/Extreme/_edit_work/ro19"; O = f"{W}/audio/opts2"; os.makedirs(O, exist_ok=True)
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001; SR = 48000; D = 31.0
S = json.load(open(f"{W}/shots.json")); T0 = next(s["out_f0"] for s in S if s["id"] == "photos.0r0")/FPS
wv = wave.open(f"{W}/voice/film_voice.untreated.wav"); assert wv.getframerate() == SR and wv.getnchannels() == 1
wv.setpos(int(round(T0*SR))); x = np.frombuffer(wv.readframes(int(D*SR)), np.int16).astype(np.float32)/32768
_db = [20*np.log10(np.sqrt(np.mean(x[i:i+2400]**2))+1e-9) for i in range(0, len(x)-2400, 2400)]            # 50 ms steps
_q = [d < -45 for d in _db]; _run = 0; _worst = 0
for q in _q: _run = _run+1 if q else 0; _worst = max(_worst, _run)
print("window: film", round(T0, 2), "to", round(T0+D, 2), "s; level in 1 s steps (dB):", [int(round(max(_db[i:i+20]))) for i in range(0, len(_db), 20)])
print("first 0.5 s peak level", round(max(_db[:10]), 1), "dB; longest pause", round(_worst*0.05, 2), "s")
assert not all(_q[:10]) and _worst*0.05 <= 1.5, f"audition window {T0}-{T0+D} s: no speech in the first 0.5 s or a {_worst*0.05:.1f} s pause"
def wav(path, y):
    o = wave.open(path, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(y, -1, 1)*32767).astype("<i2").tobytes()); o.close()
def warm(cut450=-3.0, body=1.5): return f"highpass=f=70,equalizer=f=140:t=q:w=1.0:g=+{body},equalizer=f=450:t=q:w=1.2:g={cut450},equalizer=f=3200:t=q:w=1.5:g=-1.0"
WARM = {
 "W1-light":       dict(af=warm(), derev=dict(alpha=0.30, floor_db=-10.0), what="Warm tone, light echo removal. This is the exact voice you picked on Work Out Every Day."),
 "W2-lightest":    dict(af=warm(), derev=dict(alpha=0.20, floor_db=-8.0),  what="Warm tone, the lightest echo removal. Closest to the microphone as recorded."),
 # alpha 0.40 / floor -12 measured flux 0.0802 = 1.11x the reference (limit 1.10) and swirl 1.35x untreated: past the line, not offered
 "W3-more":        dict(af=warm(), derev=dict(alpha=0.35, floor_db=-11.0), what="Warm tone, a step more echo removed than W1."),
 "W4-less-boxy":   dict(af=warm(cut450=-5.0), derev=dict(alpha=0.30, floor_db=-10.0), what="W1 with more of the boxy kitchen tone taken out (a deeper dip at 450 Hz)."),
}
def bass(base, g): return dict(af=WARM[base]["af"] + f",equalizer=f=120:t=q:w=0.8:g=+{g}", derev=WARM[base]["derev"], what=f"{base.split('-')[0]} with {g} dB more bass (a wide lift around 120 Hz).")
REF = json.load(open(f"{A}/reference/reference.json"))
def measure(path):
    y = C.pcm(path); b, fl, dry, sp = C.analyse(y); a = C.artifacts(y)
    low = float(20*np.log10(np.sqrt(np.mean(np.abs(np.fft.rfft(y))[: int(60*len(y)/SR)]**2)) / (np.sqrt(np.mean(np.abs(np.fft.rfft(y))[int(100*len(y)/SR): int(4000*len(y)/SR)]**2)) + 1e-12) + 1e-12))
    return dict(edt=round(C.edt(y), 1), flux=round(a["flux"], 4), swirl=round(a["swirl"], 3), tone=round(float(np.abs(b - np.array(REF["bands"])).mean()), 2),
                bands=[round(float(v), 1) for v in b], sub60=round(low, 1), dry=round(dry, 2))
def build(k, o):
    y = dereverb(x, sr=SR, **o["derev"]) if o["derev"] else x
    wav(f"{O}/_{k}.mono.wav", y)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{O}/_{k}.mono.wav", "-af", o["af"] + ",pan=stereo|c0=c0|c1=c0", "-c:a", "pcm_s16le", f"{O}/_{k}.st.wav"], check=True)
    r = subprocess.run(["python3", f"{A}/voice_chain.py", "--in", f"{O}/_{k}.st.wav", "--out", f"{O}/{k}.wav", "--finish-only", "--work", f"{O}/_{k}.work"], capture_output=True, text=True)
    assert os.path.exists(f"{O}/{k}.wav"), (k, r.stdout[-400:], r.stderr[-400:])
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{O}/{k}.wav", "-c:a", "libmp3lame", "-b:a", "192k", f"{O}/{k}.mp3"], check=True)
    m = measure(f"{O}/{k}.wav"); print(k, m, flush=True); return dict(what=o["what"], af=o["af"], derev=o["derev"], **m)
if __name__ == "__main__":
    P = f"{O}/options.json"; out = json.load(open(P)) if os.path.exists(P) else {}
    if sys.argv[1] == "warm":
        out["0-untreated"] = build("0-untreated", dict(af="highpass=f=70", derev=None, what="Your microphone as recorded, only the rumble below the voice removed. For comparison."))
        for k, o in WARM.items(): out[k] = build(k, o)
    if sys.argv[1] == "bass":
        base = sys.argv[2]
        for g in (1.5, 3.0, 4.5): k = f"B{'123'[int(g/1.5)-1]}-{base.split('-')[0]}-bass+{g}"; out[k] = build(k, bass(base, g))
    print("reference: edt", REF["edt_ms"], "flux", REF["flux"], "swirl", REF["swirl"])
    json.dump(out, open(P, "w"), indent=1)
