#!/usr/bin/env python3
"""Guard against the two ways a cleanup chain makes things WORSE.

  PUMPING       - a gate that opens and closes audibly. Measured as the variability of the
                  short-term level inside passages that should be steady room tone.
  LOST TAILS    - a gate that eats the ends of words. Measured by transcribing the processed
                  audio and diffing the word sequence against the unprocessed reference.
Neither shows up in a floor or tone measurement, which is how an over-aggressive chain gets
shipped sounding "underwater".
"""
import subprocess, sys, re
import numpy as np, whisper
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC="/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/03 - The Supplements I Actually Take/CUT_v1_graded_NO-GRAPHICS.mp4"
AIR=("equalizer=f=1800:width_type=o:width=1.2:g=-2.0,equalizer=f=3500:width_type=o:width=1.2:g=3.0,"
     "highshelf=f=6000:g=7.5,equalizer=f=11000:width_type=o:width=1.0:g=4.0,deesser=i=0.40")
HP="pan=mono|c0=c1,highpass=f=75:p=2"
CANDS={
 'plain (no cleanup)': f"{HP},{AIR}",
 'M1 afftdn24 gate.026 r4 rg.30': f"{HP},afftdn=nr=24:nf=-42:tn=1,agate=threshold=0.026:ratio=4:range=0.30:attack=6:release=260:knee=8,{AIR}",
 'M2 afftdn28 gate.030 r6 rg.22': f"{HP},afftdn=nr=28:nf=-40:tn=1,agate=threshold=0.030:ratio=6:range=0.22:attack=6:release=260:knee=8,{AIR}",
 'K  afftdn35 gate.035 r8 rg.18': f"{HP},afftdn=nr=35:nf=-38:tn=1,agate=threshold=0.035:ratio=8:range=0.18:attack=5:release=260:knee=8,{AIR}",
}
def load(af,t,d):
    p=subprocess.run([FF,'-v','error','-ss',str(t),'-i',SRC,'-t',str(d),'-vn','-af',af,
                      '-ac','1','-ar','16000','-f','s16le','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.int16).astype(np.float32)/32768.
m=whisper.load_model('base.en')
def words(x):
    r=m.transcribe(x,language='en',verbose=False)
    return [w for w in re.sub(r'[^a-z0-9 ]',' ',r['text'].lower()).split() if w]
ref=words(load(f"{HP},{AIR}",300,45))
def wer(a,b):
    import difflib
    sm=difflib.SequenceMatcher(None,a,b)
    return 1-sm.ratio()
print(f"{'chain':32s} {'pumping':>9s} {'word match':>11s}")
for lab,af in CANDS.items():
    x=load(af,300,45)
    # pumping: std of the 100ms level inside the quietest third of the passage
    hop=1600; n=len(x)//hop
    e=20*np.log10(np.maximum(1e-7,np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))))
    quiet=e[e<np.percentile(e,33)]
    pump=float(np.std(quiet))
    w=words(x)
    print(f"{lab:32s} {pump:8.1f}dB {100*(1-wer(ref,w)):10.1f}%")
print("\n(pumping: the plain chain is the baseline - a cleanup that raises it much above that")
print(" is audibly opening and closing. word match: below ~95% means tails are being eaten.)")
