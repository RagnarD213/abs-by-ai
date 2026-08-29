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
BANDS = [(80,160),(160,320),(320,640),(640,1250),(1250,2500),(2500,5000),(5000,9000)]

def pcm(f, af='anull'):
    p = subprocess.run([FF,'-v','error','-i',f,'-vn','-af',af,'-ac','1','-ar','48000',
                        '-f','s16le','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.

def profile(x):
    n=len(x)//960; fr=x[:n*960].reshape(n,960)
    rms=np.sqrt((fr**2).mean(1))
    loud=fr[rms>np.percentile(rms,70)]
    S=(np.abs(np.fft.rfft(loud*np.hanning(960),axis=1))**2).mean(0)
    f=np.fft.rfftfreq(960,1/48000)
    return np.array([10*np.log10(max(1e-12,S[(f>=a)&(f<b)].mean())) for a,b in BANDS])

files={sid:f'out/{sid.lower()}_{slug}.mp4' for sid,slug in segs}
profs={sid:profile(pcm(f)) for sid,f in files.items()}
ref=np.median(np.stack(list(profs.values())),axis=0)
print("batch reference profile (dB):", np.round(ref,1))
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
    g=np.clip(d*0.85,-4,4)
    eq=','.join(f"equalizer=f={int(round((a*b)**0.5))}:width_type=o:width=1.0:g={gi:.1f}"
                for (a,b),gi in zip(BANDS,g))
    # two-pass loudnorm on top of the EQ so the measurement sees the final tone
    m=subprocess.run([FF,'-hide_banner','-i',f,'-af',
        f'{eq},loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],
        capture_output=True,text=True).stderr
    j=json.loads(m[m.rfind('{'):m.rfind('}')+1])
    af=(f"{eq},loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:"
        f"measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
        f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,"
        f"alimiter=level=disabled:limit=0.8414")
    tmp=f.replace('.mp4','.fin.mp4')
    r=subprocess.run([FF,'-hide_banner','-loglevel','error','-y','-i',f,'-af',af,
        '-c:v','copy','-c:a','aac','-b:a','160k','-ar','48000','-ac','2',
        '-movflags','+faststart',tmp],capture_output=True,text=True)
    if r.returncode: print(r.stderr); raise SystemExit(f'{sid} failed')
    import os; os.replace(tmp,f)
    # ⚠ this line had a malformed expression on the first run (np.sqrt(x**2).mean()**0.5),
    # which reported a rise where there was a fall. RMS is sqrt(mean(x**2)).
    dd = ref - profile(pcm(f)); dd = dd - dd.mean()
    after = float(np.sqrt((dd**2).mean()))
    print(f"{sid:3s} {before:15.2f} {after:7.2f}   {np.round(g,1)}")
    report[sid]=dict(before=round(before,2),after=round(after,2),gains=[round(float(v),2) for v in g])
json.dump(report,open('work/audiofit.json','w'),indent=1)
