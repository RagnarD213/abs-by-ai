#!/usr/bin/env python3
"""Make the RAW INSERT sound like the short it sits inside.

The master's voice went through the 2026-08-23 single-mic repair (RIGHT channel only, per-roll
EQ, gate, loudnorm), so a line lifted off the raw roll would otherwise sound like a different
microphone next to it.

⚠ FIT AGAINST THE CONTENT IT WILL NEIGHBOUR, NOT AGAINST A SHARED TAKE. The first attempt
fitted the raw roll to the master over a passage present in BOTH (the take the editor kept)
and left a 1.45 dB seam on the finished short - because the INSERT is a different take, taken
10 seconds earlier, and Dan's delivery and mic distance differ between takes. Fitting the
insert's own span against the master audio that follows it removes that assumption.
"""
import subprocess
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
RAW = "/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/C1514.MP4"
MASTER = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/03 - The Supplements I Actually Take/CUT_v1_graded_NO-GRAPHICS.mp4"
INS_T, INS_D = 1477.90, 4.48        # the abandoned take, exactly as segments.js cuts it
NBR_T, NBR_D = 1000.35, 40.10       # the master content that follows it inside short E

def pcm(src, t, d, af):
    p = subprocess.run([FF,'-v','error','-ss',f'{t:.3f}','-i',src,'-t',f'{d:.3f}','-vn',
                        '-af',af,'-ac','1','-ar','48000','-f','s16le','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.
BANDS=[(80,160),(160,320),(320,640),(640,1250),(1250,2500),(2500,5000),(5000,9000)]
def profile(x, pct=65):
    n=len(x)//960; fr=x[:n*960].reshape(n,960); rms=np.sqrt((fr**2).mean(1))
    loud=fr[rms>np.percentile(rms,pct)]
    S=(np.abs(np.fft.rfft(loud*np.hanning(960),axis=1))**2).mean(0)
    f=np.fft.rfftfreq(960,1/48000)
    return np.array([10*np.log10(max(1e-12,S[(f>=a)&(f<b)].mean())) for a,b in BANDS])

VOICE = open('work/voicechain.txt').read().strip()
nbr = profile(pcm(MASTER, NBR_T, NBR_D, VOICE))
ins = profile(pcm(RAW, INS_T, INS_D, VOICE))
gain = float(np.mean(nbr - ins))
g = np.clip((nbr - ins - gain) * 0.9, -9, 9)
print("band      insert   neighbour    diff")
for (a,b),i,n_ in zip(BANDS,ins,nbr): print(f" {a:5d}-{b:5d} {i:8.1f} {n_:11.1f} {n_-i:+8.1f}")
print(f"\nbroadband gain {gain:+.1f} dB, per-band correction {np.round(g,1)}")
eq=','.join(f"equalizer=f={int(round((a*b)**0.5))}:width_type=o:width=1.0:g={gi:.1f}"
            for (a,b),gi in zip(BANDS,g))
# ⚠ NO `pan` HERE. render.js applies the voice chain first, which already folds to mono on the
# RIGHT channel; a second pan=mono|c0=c1 asks for a channel that no longer exists and ffmpeg
# renders SILENCE rather than erroring - it blanked the first 4.48s of the short.
af=f"{eq},volume={gain:.1f}dB"
open('work/rawfit.txt','w').write(af)
chk = profile(pcm(RAW, INS_T, INS_D, f'{VOICE},{af}'))
d = chk - nbr; d = d - d.mean()
print(f"predicted seam after correction: {float(np.sqrt((d**2).mean())):.2f} dB")
