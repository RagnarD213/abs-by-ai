"""DS-30 R1 look and voice options for the review page.
voice: V1 fitted tone + 120 Hz +3 dB (the house default, recommended; = voice.wav), V2 fitted + 1.5 dB, V3 fitted, no lift,
       V4 untreated (level matched). Each option is the full mix; the page plays the SAME passage of each, level matched
       (-14 LUFS by the chain), taken from a kept piece's own speech (film 7.25-17.15: "The average American ... yours again.").
colour: the three looks (C recommended, Dan's pick on DS-31) on the same tight/wide frames + a 6 s moving sample each.
"""
from pathlib import Path
import json, subprocess, sys, os
import numpy as np
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; A = R/'.claude/skills/_shared/audio'
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001; O = W/'options'; O.mkdir(exist_ok=True)
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
def ff(a): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, a)), check=True)
fit = json.load(open(W/'fit-voice-eq.json')); eq0 = fit['eq_fitted']
VO = {'V1': ('Fitted tone + bass lift (+3 dB at 120 Hz), house default', W/'voice.wav', None),
      'V2': ('Fitted tone + lighter bass lift (+1.5 dB)', O/'voice-V2.wav', eq0 + ',equalizer=f=120:t=q:w=0.8:g=1.5'),
      'V3': ('Fitted tone, no bass lift', O/'voice-V3.wav', eq0)}
for k, (name, out, eq) in VO.items():
    if eq and not out.exists():
        subprocess.run([sys.executable, str(A/'voice_chain.py'), '--in', str(W/'untreated.wav'), '--out', str(out), '--pull', 'pan=mono|c0=0.5*c0+0.5*c1', '--eq', eq,
                        '--no-expander-because', 'Option for Dan: same chain as V1 with a different bass lift.', '--work', str(O/f'work-{k}')], check=True)
V4 = O/'voice-V4.wav'
if not V4.exists(): ff(['-i', W/'untreated.wav', '-af', 'pan=mono|c0=0.5*c0+0.5*c1,volume=15.399999999999999dB,alimiter=limit=0.79', '-ar', 48000, '-c:a', 'pcm_s24le', V4])
VO['V4'] = ('Untreated lav, level matched', V4, None)
a, b = 7.25, 17.15
# refuse a window that does not start on speech or holds a long pause (VIDEO-RULES 2026-10-11)
ff(['-ss', a, '-t', b - a, '-i', W/'voice.wav', '-ac', 1, '-ar', 16000, '-f', 's16le', O/'_win.raw'])
x = np.fromfile(O/'_win.raw', '<i2').astype(np.float32)/32768; hop = 160; n = len(x)//hop
db = 20*np.log10(np.sqrt((x[:n*hop].reshape(n, hop)**2).mean(1)) + 1e-9)
first = np.where(db > -35)[0][0]*0.01; quiet = db < -45; runs = []; r = 0
for q in quiet: r = r + 1 if q else 0; runs.append(r)
assert first <= 0.5, ('window starts late', first); assert max(runs)*0.01 <= 1.5, ('pause in window', max(runs)*0.01)
print('voice window', a, b, 'speech at', first, 's, longest pause', max(runs)*0.01, 's', [round(float(v)) for v in db[::100]])
master = [p for p in sorted((W/'review').glob('*complete Short.mp4')) if not p.name.startswith('._')][0]
voices = []
for k, (name, wav, _) in VO.items():
    out = O/f'voice-{k}.mp4'
    ff(['-ss', a, '-t', b - a, '-i', master, '-ss', a, '-t', b - a, '-i', wav, '-map', '0:v', '-map', '1:a', '-vf', 'scale=540:960',
        '-c:v', 'libx264', '-crf', 22, '-preset', 'fast', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out])
    voices.append(dict(id=k, name=name, clip=out.name, recommended=k == 'V1'))
# colour
CO = json.load(open(W/'col/options.json')); EDL = json.load(open(W/'edl.json')); S = EDL['source']
def src_t(film):
    for p in EDL['pieces']:
        if p['film0'] <= film < p['film0'] + p['duration']: return p['start'] + film - p['film0']
frames = {'tight': (4.5, '1056:1878:552:780'), 'wide': (12.0, None)}
cols = []
for k, c in CO.items():
    row = dict(id=k, name=c['name'], recommended=k == 'C', stills={})
    for fname, (t, crop) in frames.items():
        out = O/f'col-{k}-{fname}.jpg'
        vf = (f'crop={crop},' if crop else '') + f"scale=1080:1920:flags=lanczos,{c['filter']},scale=540:960"
        ff(['-ss', src_t(t), '-i', S, '-frames:v', 1, '-vf', vf, '-q:v', 3, out]); row['stills'][fname] = out.name
    smp = O/f'col-{k}-sample.mp4'
    ff(['-ss', src_t(10.3), '-t', 3.8, '-i', S, '-an', '-vf', f"scale=1080:1920:flags=lanczos,{c['filter']},scale=540:960", '-c:v', 'libx264', '-crf', 21, '-preset', 'fast', '-movflags', '+faststart', smp])
    row['sample'] = smp.name; cols.append(row)
(O/'options.json').write_text(json.dumps(dict(voice_window=[a, b], voices=voices, colours=cols), indent=1))
print('OPTIONS READY', len(voices), 'voices', len(cols), 'looks')
