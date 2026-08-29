#!/usr/bin/env python3
"""Is the CLEAN master's audio really right-channel-only mono?

The handoff asserted it was ("already the fixed single-mic chain"), and rev 1 and rev 2 both
took that on trust. Dan now says the audio still does not sound as good as Muhammad's and
asks specifically whether we are using the right channel only, in mono. Measure it.

The standing finding on this shoot (2026-08-22/23): the camera records TWO microphones, not
stereo. The LEFT input is a room mic ~7.5ms late; summing them combs the voice. The repair is
right channel only, as mono.
"""
import subprocess, sys
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FILES = {
 'CLEAN master (what we cut from)': "/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/03 - The Supplements I Actually Take/CUT_v1_graded_NO-GRAPHICS.mp4",
 'DELIVERED master (audio-fixed 8/23)': "/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/03 - The Supplements I Actually Take/FINAL_supplements.mp4",
 'PRE_AUDIOFIX master (known bad)': "/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/03 - The Supplements I Actually Take/FINAL_supplements_PRE_AUDIOFIX.mp4",
 'RAW roll C1514 (two mics)': "/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/C1514.MP4",
}
T, D = 1000.0, 30.0
for lab, f in FILES.items():
    t = 1492.0 if 'RAW' in lab else T
    p = subprocess.run([FF,'-v','error','-ss',str(t),'-i',f,'-t',str(D),'-vn',
                        '-ac','2','-ar','48000','-f','s16le','-'],capture_output=True)
    x = np.frombuffer(p.stdout,np.int16).astype(np.float64).reshape(-1,2)
    L,R = x[:,0], x[:,1]
    if L.std()<1 or R.std()<1:
        print(f"{lab}: a channel is silent"); continue
    corr = float(np.corrcoef(L,R)[0,1])
    mid, side = (L+R)/2, (L-R)/2
    sdb = 20*np.log10(max(1e-9, side.std())/max(1e-9, mid.std()))
    # best alignment lag between the two channels
    n=min(len(L),240000); best=(-2,0)
    for lag in range(-600,601,4):
        a=L[max(0,lag):max(0,lag)+n-abs(lag)]; b=R[max(0,-lag):max(0,-lag)+n-abs(lag)]
        if len(a)<10000: continue
        d=np.linalg.norm(a)*np.linalg.norm(b)
        if d:
            c=float(np.dot(a,b)/d)
            if c>best[0]: best=(c,lag)
    snr=lambda v: 20*np.log10(max(1e-9,np.percentile(np.abs(v),99))/max(1e-9,np.percentile(np.abs(v),5)))
    print(f"{lab}:")
    print(f"   L/R corr {corr:+.4f}   side under mid {-sdb:5.1f} dB   "
          f"best lag {best[1]/48:+.2f} ms (corr {best[0]:+.3f})")
    print(f"   dynamic range  L {snr(L):5.1f} dB   R {snr(R):5.1f} dB   "
          f"{'IDENTICAL CHANNELS (true mono)' if corr>0.9999 else 'CHANNELS DIFFER'}")
