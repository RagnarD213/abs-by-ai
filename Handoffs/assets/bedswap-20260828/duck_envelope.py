#!/usr/bin/env python3
"""Explicit music-bed ducking under speech.

Why not sidechaincompress: on short5 the ffmpeg sidechain compressor only pulled the
bed to 68% of full under speech, which Dan heard immediately as "music too loud when I
first start talking". This applies an exact, measurable gain instead.

Input : a voice-only WAV (silence everywhere the talent is not speaking) at 44100 Hz.
Output: duckgain.npy, a per-sample gain envelope to multiply the bed by.

Key detail: the duck starts PRE seconds BEFORE speech begins. A duck that starts on the
first syllable is always audibly late -- that was the exact complaint.
"""
import numpy as np, wave, sys

SR    = 44100
DUCK  = 0.30   # 0.30 = a 70% reduction
PRE   = 0.35   # start ducking this long before speech
POST  = 0.45   # hold the duck this long after speech
RAMP_DOWN = 0.25
RAMP_UP   = 0.55
GATE_DB   = -50.0

def speech_spans(v, step_s=0.01, min_len=0.1, join_gap=0.8):
    step = int(SR*step_s); spans=[]; cur=None
    for i in range(len(v)//step):
        s = v[i*step:(i+1)*step]
        loud = 20*np.log10(np.sqrt(np.mean(s**2))+1e-12) > GATE_DB
        t = i*step_s
        if loud and cur is None: cur=[t,t]
        elif loud: cur[1]=t
        elif cur is not None:
            if cur[1]-cur[0] > min_len: spans.append(cur)
            cur=None
    if cur: spans.append(cur)
    merged=[]
    for s in spans:
        if merged and s[0]-merged[-1][1] < join_gap: merged[-1][1]=s[1]
        else: merged.append(list(s))
    return merged

def envelope(n, spans):
    g = np.ones(n, dtype=np.float32)
    for s,e in spans:
        ia, ib = int(max(0.0, s-PRE)*SR), int(min(n/SR, e+POST)*SR)
        g[ia:ib] = DUCK
        r = int(RAMP_DOWN*SR); i0 = max(0, ia-r)
        g[i0:ia] = np.minimum(g[i0:ia], np.cos(np.linspace(0,np.pi/2,ia-i0))**2*(1-DUCK)+DUCK)
        r2 = int(RAMP_UP*SR); i1 = min(n, ib+r2)
        g[ib:i1] = np.minimum(g[ib:i1], np.sin(np.linspace(0,np.pi/2,i1-ib))**2*(1-DUCK)+DUCK)
    return g

if __name__ == "__main__":
    w = wave.open(sys.argv[1], 'rb')
    v = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768.
    spans = speech_spans(v)
    g = envelope(len(v), spans)
    np.save("duckgain.npy", g)
    for s,e in spans: print(f"speech {s:8.2f} - {e:8.2f}s")
    print(f"ducked {(g<0.999).sum()/SR:.2f}s of {len(v)/SR:.1f}s at {DUCK:.2f} ({20*np.log10(DUCK):+.1f} dB)")
