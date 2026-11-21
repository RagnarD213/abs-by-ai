#!/usr/bin/env python3
"""Fit our lav against the REFERENCE EDIT'S VOICE -- with its music bed subtracted.

Two corrections over the earlier longform fitvoice, both of which mattered here:

 1. THE REFERENCE CARRIES A MUSIC BED. Normalising each spectrum by its own total then
    makes his bass-heavy bed push every other band of HIS spectrum down, and our voice
    reads as +6.9 dB at 5 kHz and +7.8 dB at 8 kHz when an absolute peak-relative check
    puts us within 1-3 dB of him from 4 kHz to 13 kHz. Fix: sample his bed on its own in
    speech GAPS (found from his word timings), then subtract it in the POWER domain from
    the speech-window spectrum. What is left is his voice.
 2. HIS FILE IS A 125 kbps AAC that brickwalls at ~15 kHz (-80 dB at 15 k, -112 at 16 k).
    That is the codec, not a tonal decision, so nothing above 10.5 kHz is a fit target.

Frames are kept only above the 55th percentile of RMS so the comparison is made on
speech, and each spectrum is normalised on the 700-2000 Hz voice core rather than on its
whole-spectrum total, so a difference down at 100 Hz cannot move every other band.
usage: fitvoice.py ["<af chain>" ...]
"""
import json, subprocess, sys, wave
import numpy as np
FF   = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
B    = "/Volumes/Extreme/_edit_work/abwheel"
REF  = f"{B}/ref_muhammad/muhammad_organic.mp4"
OURS = f"{B}/r2/audio/voice_raw.wav"
SR   = 22050
BANDS = [(80,150),(150,250),(250,400),(400,700),(700,1200),(1200,2000),
         (2000,3200),(3200,5000),(5000,8000),(8000,10500)]
CORE  = (700, 2000)
# TALKING ONLY. Output 305-500 s is the three live sets: near-silent, with hard
# breathing between reps. Breath is broadband, so any window inside a set drags the
# fit bright -- the first pass read +10 dB at 3-8 kHz purely from that.
OUR_WINS = [(6.0,6),(30.0,6),(70.0,6),(120.0,6),(150.0,6),(190.0,6),(215.0,6),
            (265.0,6),(292.0,5),(505.0,6),(520.0,6)]

def pcm(src, af, ss, d):
    raw = subprocess.run([FF,"-nostdin","-v","error","-ss",f"{ss}","-t",f"{d}","-i",src,
        "-af",af or "anull","-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(float)

N = 2048
def frames(a):
    if len(a) < N: return np.zeros((0,N))
    return np.array([a[i:i+N]*np.hanning(N) for i in range(0,len(a)-N,512)])

def power(fr, pct=55):
    if not len(fr): return None
    rms = np.sqrt((fr**2).mean(1))
    keep = rms > np.percentile(rms, pct) if pct else np.ones(len(fr), bool)
    P = (np.abs(np.fft.rfft(fr[keep],axis=1))**2).mean(0)
    return P

F = np.fft.rfftfreq(N, 1/SR)

# ---- his bed, sampled in speech gaps
wh = json.load(open(f"{B}/ref_muhammad/m.whisper.json"))
W = [w for s in wh["segments"] for w in s.get("words",[])]
gaps = []
for a,b in zip(W, W[1:]):
    if b["start"] - a["end"] >= 0.85 and a["end"] > 4:
        gaps.append((a["end"]+0.18, min(b["start"]-0.12, a["end"]+1.4)))
gaps = [g for g in gaps if g[1]-g[0] >= 0.45][:26]
bedP, nb = np.zeros(N//2+1), 0
for a,b in gaps:
    P = power(frames(pcm(REF,"pan=mono|c0=0.5*c0+0.5*c1",a,b-a)), pct=0)
    if P is not None: bedP += P; nb += 1
bedP /= max(nb,1)

# ---- his speech windows
spwins = []
for a,b in zip(W, W[1:]):
    if b["start"]-a["end"] < 0.25 and a["end"] > 4: spwins.append(a["start"])
spwins = spwins[::max(1,len(spwins)//40)][:40]
spP, ns = np.zeros(N//2+1), 0
for t in spwins:
    P = power(frames(pcm(REF,"pan=mono|c0=0.5*c0+0.5*c1",t,1.2)))
    if P is not None: spP += P; ns += 1
spP /= max(ns,1)

voiceP = np.maximum(spP - bedP, spP*0.02)      # bed removed in the power domain
def norm(P):
    db = 10*np.log10(P + 1e-20)
    return db - db[(F>=CORE[0])&(F<CORE[1])].mean()
HIS = norm(voiceP)
bed_under = 10*np.log10((bedP[(F>=60)&(F<400)].mean())/(spP[(F>=60)&(F<400)].mean()))
print(f"his bed sampled in {nb} speech gaps; it carries {-bed_under:.1f} dB less than "
      f"his speech at 60-400 Hz\nhis speech windows: {ns}")

def test(chain, label):
    P, n = np.zeros(N//2+1), 0
    for ss,d in OUR_WINS:
        Q = power(frames(pcm(OURS, chain, ss, d)))
        if Q is not None: P += Q; n += 1
    O = norm(P/max(n,1))
    errs = [float(O[(F>=lo)&(F<hi)].mean()-HIS[(F>=lo)&(F<hi)].mean()) for lo,hi in BANDS]
    print(f"{label:42s} mean|err| {np.mean(np.abs(errs)):5.2f} dB   max {np.max(np.abs(errs)):5.2f}")
    print("       " + " ".join(f"{e:+5.1f}" for e in errs))
    return float(np.mean(np.abs(errs))), errs

print("\nbands: " + " ".join(f"{lo:>5}" for lo,_ in BANDS))
if len(sys.argv) > 1:
    for c in sys.argv[1:]: test(c, c[:40])
else:
    test("", "RAW right-channel lav (no EQ)")
