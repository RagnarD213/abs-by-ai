"""RO-15 voice bake-off (from RO-28/RO-31) (PRE-RENDER-APPROVAL step 3): the same 30 s of the assembled voice (the film's opening, speech from its
first half second) four ways, each finished by the shared chain to the same loudness, plus mp3s for the blind ranking.
Reference: 30 s of the approved RO-17 film (same 9/23 studio set and lav)."""
import sys, os, subprocess, wave, json, numpy as np
A = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
W = "/Volumes/Extreme/_edit_work/RO-15/round1"; O = f"{W}/options/voice"; os.makedirs(O, exist_ok=True)
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
T0, D, SR = 0.45, 30.0, 48000
wv = wave.open(f"{W}/assembled_untreated.wav"); wv.setpos(int(T0*SR)); x = np.frombuffer(wv.readframes(int(D*SR)), np.int16).astype(np.float32)/32768
# window check: speech in the first 0.5 s, no pause over 1.5 s (VIDEO-RULES 2026-10-11)
lv = [20*np.log10(np.sqrt(np.mean(x[i:i+960]**2))+1e-9) for i in range(0, len(x)-960, 960)]
first = next(i for i, v in enumerate(lv) if v > -40) * 0.02; run = best = 0
for v in lv: run = run + 1 if v < -45 else 0; best = max(best, run)
print("speech starts", round(first, 2), "s; longest pause", round(best*0.02, 2), "s"); assert first <= 0.5 and best*0.02 <= 1.5
def wav(path, y):
    o = wave.open(path, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(y, -1, 1)*32767).astype("<i2").tobytes()); o.close()
wav(f"{O}/_raw.wav", x)
EQB = open(f"{W}/fit/eq_B.txt").read().strip()
OPTS = {
 "1-untreated": ("finish", "highpass=f=70", "The microphone as recorded, only the rumble below the voice removed, brought to the same loudness."),
 "2-chain-default": ("chain", None, "The shared chain's default: tone matched automatically to the reference voice, a light gate between words."),
 "3-studio-B": ("chain", EQB, "The approved 9/23 studio voice (audio B from the website video, used on RO-10 to RO-18): the chain's fit on this roll plus 0.9 dB at 150 Hz."),
 "4-studio-B-bass": ("chain", EQB + ",equalizer=f=120:t=q:w=0.8:g=+3.0", "Studio B plus your standard bass lift (+3 dB at 120 Hz), as on RO-14, RO-17 and RO-18. Recommended."),
 "5-studio-B-bass-no-gate": ("finish", EQB + ",equalizer=f=120:t=q:w=0.8:g=+3.0", "The same tone as 4 on the untreated microphone, with no gate between words."),
}
out = {}
ONLY = sys.argv[1:]
for k, (mode, eq, what) in OPTS.items():
    if ONLY and k not in ONLY: out[k] = what; continue
    if mode == "finish":
        subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{O}/_raw.wav", "-af", eq + ",pan=stereo|c0=c0|c1=c0", "-c:a", "pcm_s16le", f"{O}/_{k}.st.wav"], check=True)
        cmd = ["python3", f"{A}/voice_chain.py", "--in", f"{O}/_{k}.st.wav", "--out", f"{O}/{k}.wav", "--finish-only", "--work", f"{O}/_{k}.work"]
    else:
        cmd = ["python3", f"{A}/voice_chain.py", "--in", f"{O}/_raw.wav", "--pull", "anull", "--out", f"{O}/{k}.wav", "--work", f"{O}/_{k}.work"] + (["--eq", eq] if eq else [])
    r = subprocess.run(cmd, capture_output=True, text=True); assert os.path.exists(f"{O}/{k}.wav"), (k, r.stdout[-500:], r.stderr[-500:])
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{O}/{k}.wav", "-c:a", "libmp3lame", "-b:a", "192k", f"{O}/{k}.mp3"], check=True)
    out[k] = what; print("built", k, flush=True)
REF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/claude edited long form content/17 - 3 Healthy Foods That Made Me Fat/3 Healthy Foods That Made Me Fat | claude round 5 | 16x9 | RO-17.mp4"
subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", "120", "-t", "30", "-i", REF, "-vn", "-c:a", "libmp3lame", "-b:a", "192k", f"{O}/_reference.mp3"], check=True)
json.dump(out, open(f"{O}/options.json", "w"), indent=1)
