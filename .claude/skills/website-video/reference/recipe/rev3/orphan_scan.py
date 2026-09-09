#!/usr/bin/env python3
"""Find SPEECH that Whisper assigned no words to -- abandoned takes it silently dropped.

Whisper stitches a segment's text across an abandoned re-attempt and drops the attempt,
so the transcript reads clean while the audio stutters. Detect it from the ENVELOPE:
any run of speech-level energy >=MINLEN long that no word interval covers.
  orphan_scan.py <wav16k> <whisper.json> [edl.json]
"""
import json, sys, wave
import numpy as np
w=wave.open(sys.argv[1]); sr=w.getframerate()
a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float64)/32768
HOP=0.02; N=int(HOP*sr)
n=len(a)//N
db=20*np.log10(np.sqrt((a[:n*N].reshape(n,N)**2).mean(1))+1e-9)
wh=json.load(open(sys.argv[2])); WS=[x for s in wh['segments'] for x in s.get('words',[])]
cov=np.zeros(n,bool)
for x in WS:
    cov[max(0,int((x['start']-0.12)/HOP)):int((x['end']+0.12)/HOP)+1]=True
RANGES=None
if len(sys.argv)>3:
    RANGES=[(r['start'],r['end']) for r in json.load(open(sys.argv[3]))['ranges']]
THRESH=-38.0; MINLEN=0.30
runs=[];cur=None
for i in range(n):
    hot = db[i]>THRESH and not cov[i]
    if hot: cur=(cur[0],i) if cur else (i,i)
    elif cur: runs.append(cur); cur=None
if cur: runs.append(cur)
print(f"{'start':>8}{'end':>8}{'len':>7}{'peak dB':>9}  in-EDL")
hits=0
for s,e in runs:
    t0,t1=s*HOP,(e+1)*HOP
    if t1-t0<MINLEN: continue
    ine = RANGES is None or any(a0<=t0<a1 for a0,a1 in RANGES)
    if not ine: continue
    hits+=1
    print(f"{t0:8.2f}{t1:8.2f}{t1-t0:7.2f}{db[s:e+1].max():9.1f}  {'YES' if ine else 'no'}")
print(f"\n{hits} orphan speech runs inside the EDL")
