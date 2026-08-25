#!/usr/bin/env python3
"""Two-pass loudnorm + a spectral check that the voice fit actually landed.

Single-pass loudnorm is an estimate: the first mix measured -14.7 LUFS / -4.5 dBTP, i.e.
0.7 LU quiet with 3 dB of headroom left unused. Measure, then normalise with the measured
values."""
import json, subprocess, sys, wave
import numpy as np
sys.path.insert(0,'.')
from build_audio import spec_of, BANDS, HIS, WINS, FF, sh

r = subprocess.run([FF,'-hide_banner','-nostats','-i','audio.wav','-af',
                    'loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json','-f','null','-'],
                   capture_output=True, text=True).stderr
m = json.loads(r[r.rindex('{'):r.rindex('}')+1])
print('measured:', {k: m[k] for k in ('input_i','input_tp','input_lra','input_thresh')})
sh([FF,'-v','error','-y','-i','audio.wav','-af',
    f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
    f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
    f":offset={m['target_offset']}:linear=true",
    '-ar','48000','-ac','2','-c:a','pcm_s24le','audio_final.wav'])
r2 = subprocess.run([FF,'-hide_banner','-nostats','-i','audio_final.wav','-af',
                     'loudnorm=print_format=summary','-f','null','-'], capture_output=True, text=True).stderr
print('\n'.join(l for l in r2.split('\n') if 'Input' in l))

F, H = spec_of(HIS, 'pan=mono|c0=0.5*c0+0.5*c1', WINS)
_, O = spec_of('audio_final.wav', 'pan=mono|c0=0.5*c0+0.5*c1', WINS)
errs = [float(H[(F>=lo)&(F<hi)].mean()-O[(F>=lo)&(F<hi)].mean()) for lo,hi in BANDS]
print('\nband error vs HIS mix after fit, dB:', ' '.join(f'{e:+.1f}' for e in errs))
print(f'mean |err| {np.mean(np.abs(errs)):.2f} dB   max {np.max(np.abs(errs)):.2f} dB')
