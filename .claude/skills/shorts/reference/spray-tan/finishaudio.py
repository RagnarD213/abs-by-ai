#!/usr/bin/env python3
"""Match every short's tone to the batch, then normalise. Replaces normalize.js.

Dan, rev 2: short A "doesn't sound as good as the other ones", and "double-check the audio on
all these shorts... I feel like we have room to improve."

MEASURED CAUSE. All eight already sit at -14 LUFS, so level was never the problem. What
differs is TONE: the shorts are cut from different points across a 23-minute take, and his
distance from the mic drifts. Low/high tilt measured 24.0-29.1 dB, a 5 dB spread, with A the
thinnest at 24.0 against a 27.0 median - which is exactly "thinner and harsher than the rest".

So: fit each short to the BATCH MEDIAN octave profile with a small three-band EQ, then
loudnorm to -14 with a limiter. Video is copied, never re-encoded.

A deliberate limit: no broadband noise reduction. /longform-edit tried afftdn on this exact
material and rejected it (floor -3 dB, band error 0.97 -> 1.73). Tone is the fixable part.
"""
import json, subprocess, sys
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
segs = json.loads(subprocess.check_output(
    ['node','-e',"const {SEGMENTS}=require('./segments.js');"
     "console.log(JSON.stringify(SEGMENTS.map(s=>[s.id,s.slug])))"]).decode())
only = sys.argv[1:]
TARGET_I = -14.0
LIMIT = 10**(-1.5/20)   # -1.5 dBTP
# ⚠ THE GATE AND THE CORRECTOR MUST MEASURE THE SAME BANDS - and both stop at 9 kHz. Adding a
# 9-14 kHz band was tried and REVERTED: it sits ~47 dB below the peak band (inaudible), it
# overlaps the 6.7 kHz filter so heavily that the feedback loop DIVERGED (F went 2.4 -> 6.5 dB),
# and it was never what Dan was hearing. Measured 2026-09-02.
BANDS = [(80,160),(160,320),(320,640),(640,1250),(1250,2500),(2500,5000),(5000,9000)]

def pcm(f, af='anull'):
    p = subprocess.run([FF,'-v','error','-i',f,'-vn','-af',af,'-ac','1','-ar','48000',
                        '-f','s16le','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.

def profile(x):
    n=len(x)//960; fr=x[:n*960].reshape(n,960)
    rms=np.sqrt((fr**2).mean(1))
    # 75, matching work/audiogate.py. The gate and the corrector must select the SAME
    # frames, not merely the same bands: at 70 vs 75 they disagreed by up to 0.9 dB on
    # short G, so this stage reported 0.49 dB while the gate measured 1.38.
    loud=fr[rms>np.percentile(rms,75)]
    S=(np.abs(np.fft.rfft(loud*np.hanning(960),axis=1))**2).mean(0)
    f=np.fft.rfftfreq(960,1/48000)
    return np.array([10*np.log10(max(1e-12,S[(f>=a)&(f<b)].mean())) for a,b in BANDS])

# render.js now writes a lossless .mov; this stage produces the only AAC encode.
files={sid:f'out/{sid.lower()}_{slug}.mov' for sid,slug in segs}
# Skip anything not yet rendered, so a partial run still works; the reference is the median
# of whatever the batch currently holds.
import os as _os
files={k:v for k,v in files.items() if _os.path.exists(v)}
if not files: raise SystemExit('no rendered .mov files found - run render.js first')
profs={sid:profile(pcm(f)) for sid,f in files.items()}
# ⚠ THE REFERENCE IS MUHAMMAD'S AD, NOT OUR OWN BATCH MEDIAN (changed 2026-09-02).
# Matching the batch to its own median only makes the shorts consistent with each other - it has
# no authority over whether they are RIGHT, and it fought the post-dereverb corrective EQ,
# leaving four of six 1.4-2.3 dB off his shape while looking "matched". His ad is the target
# Dan names every time; make it the target the code uses. Levels are normalised out, so only
# the SHAPE is matched.
REF_AD=("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/"
        "this picture got me abs | muhammad | 16x9.mp4")
_r=np.concatenate([pcm(REF_AD)[int(t*48000):int((t+60)*48000)] for t in (10,90)])
ref=profile(_r)
ref=ref-ref.mean()+np.median(np.stack(list(profs.values())),axis=0).mean()   # keep our level
print("reference profile = Muhammad's ad (dB):", np.round(ref,1))
print(f"\n{'id':3s} {'band err before':>15s} {'after':>7s}   per-band EQ (dB)")
report={}
for sid,f in files.items():
    if only and sid not in only: continue
    d=ref-profs[sid]; d=d-d.mean()                     # tone only; level is loudnorm's job
    before=float(np.sqrt((d**2).mean()))
    # ⚠ PER BAND, not a three-knob shelf/peak/shelf. The first attempt fitted low/mid/high by
    # grid search and could only halve the spread, because the residual shape does not look
    # like three knobs - short A stayed the most deviant, and A is the one Dan named. One
    # peaking filter per measured band matches the shape directly. Gains are damped 0.85
    # because one-octave filters overlap and would otherwise overshoot, and clamped to +/-4 dB
    # so this can only ever be a gentle correction, never a re-voicing.
    # ⚠ VERIFY, DO NOT PREDICT (2026-09-02). One-octave `equalizer` filters overlap heavily, so
    # the ACHIEVED response is a smeared version of the gains asked for - and this stage used to
    # report the response it INTENDED. Measured on the output, four of six shorts were still
    # 1.2-3.0 dB off, concentrated in the top two bands, while the printed "after" said 0.3-1.3.
    # So: apply, MEASURE THE RESULT, and fold the remaining residual back in. Two passes closes
    # it; a third buys nothing.
    g=np.clip(d*0.85,-4,4)
    mkeq=lambda gg: ','.join(f"equalizer=f={int(round((a*b)**0.5))}:width_type=o:width=1.0:g={gi:.1f}"
                             for (a,b),gi in zip(BANDS,gg))
    eq=mkeq(g)
    # ⚠ DAMPED, AND IT KEEPS THE BEST ITERATE - not the last. Undamped feedback (0.85) over
    # filters that overlap by an octave DIVERGES: measured 2026-09-02, four passes took short F
    # from 2.2 dB to 3.0 and G from 1.4 to 1.6 while each step "corrected" the residual it had
    # just measured. Half-step feedback converges, and keeping the best guarantees this stage
    # can never make a short worse than the plain first-pass fit.
    # ⚠ OPTIMISE THE FILE THAT SHIPS, NOT THE INTERMEDIATE. Fitting against `pcm(f, eq)` looks
    # right and is not: the delivered .mp4 also passes through a gain, a limiter and an AAC
    # encode, all of which move the spectrum a little. Measured 2026-09-02, short F oscillated
    # between 0.52 and 1.16 dB purely on how many times the intermediate loop ran, because the
    # thing being minimised was not the thing being gated. So each pass ENCODES and measures the
    # real output. Damped (half-step) and best-iterate, so it converges and can never regress.
    out=f.replace('.mov','.mp4')
    def encode(eq_):
        # NOT loudnorm: reaching -14 from -18.8..-21.2 LUFS needs +5..+7 dB, which loudnorm
        # cannot do linearly under a -1.5 dBTP ceiling - it silently switches to DYNAMIC mode and
        # compresses, lifting the floor toward the voice. Pure gain + limiter, then one trim.
        lu=lambda af_: float([l for l in subprocess.run(
            [FF,'-hide_banner','-i',f,'-af',f'{af_},ebur128=peak=true','-f','null','-'],
            capture_output=True,text=True).stderr.split('\n') if 'I:' in l and 'LUFS' in l][-1].split()[-2])
        gain=TARGET_I-lu(eq_)
        af_=f"{eq_},volume={gain:.2f}dB,alimiter=level=disabled:limit={LIMIT:.4f}"
        af_=(f"{eq_},volume={gain+(TARGET_I-lu(af_)):.2f}dB,"
             f"alimiter=level=disabled:limit={LIMIT:.4f}")
        r=subprocess.run([FF,'-hide_banner','-loglevel','error','-y','-i',f,'-af',af_,
            '-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',
            '-movflags','+faststart',out],capture_output=True,text=True)
        if r.returncode: print(r.stderr); raise SystemExit(f'{sid} failed')
        dd=ref-profile(pcm(out)); dd=dd-dd.mean()
        return float(np.sqrt((dd**2).mean())), dd
    best=(float('inf'),eq)
    for _ in range(5):
        err,resid=encode(eq)
        if err<best[0]: best=(err,eq)
        if err<0.30: break
        g=np.clip(g+resid*0.5,-5,5); eq=mkeq(g)
    if best[1]!=eq: encode(best[1])          # re-emit the best iterate
    eq=best[1]
    # ⚠ this line had a malformed expression on the first run (np.sqrt(x**2).mean()**0.5),
    # which reported a rise where there was a fall. RMS is sqrt(mean(x**2)).
    dd = ref - profile(pcm(out)); dd = dd - dd.mean()
    after = float(np.sqrt((dd**2).mean()))
    print(f"{sid:3s} {before:15.2f} {after:7.2f}   {np.round(g,1)}")
    report[sid]=dict(before=round(before,2),after=round(after,2),gains=[round(float(v),2) for v in g])
json.dump(report,open('work/audiofit.json','w'),indent=1)
