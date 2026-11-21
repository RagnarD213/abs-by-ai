"""DS-76 R1: edit plan, caption word map, cut audio and the four voice auditions.
Source C1882 (portrait, lav = stream 0 channel 0, measured pick_lav). Take choice in records/take-choice.json."""
from pathlib import Path
import subprocess, json, os, sys
import numpy as np
from scipy.io import wavfile
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
F = R/'Media/video_edit/bin/ffmpeg'; os.environ['PATH'] = str(F.parent)+':'+os.environ['PATH']
S = Path('/Volumes/Extreme/10:23 dan rose fitness shoot - pool shorts and long form content/C1882.MP4'); A = R/'.claude/skills/_shared/audio'
sys.path.insert(0, str(R/'.claude/skills/_shared/renderq')); import renderq
renderq.hold_until_exit('DS-76 R1 audio prepare', pool='light', group='DS-76')
def ff(a): subprocess.run([str(F), '-nostdin', '-v', 'error', '-y']+list(map(str, a)), check=True)
fps = 30000/1001; fr = lambda t: round(t*fps)
# Source seconds, each edge inside measured silence (RMS < -44 dBFS, 0.1 s steps; evidence/takes).
ranges = [(76.30, 102.40, 'Take 9 hook (won 3 of 3 blind listens over take 8) through "no swinging."'),
          (104.12, 129.50, 'Clean "Your body should stay still"; false start 102.52-103.34 removed (disfluency ASR)'),
          (131.10, 135.40, 'Second "Subscribe to my channel" read, continuous into the URL; first read removed, no picture cut')]
words = json.load(open(S.with_suffix('.roll')/'words.json'))['words']
# Words the roll ASR merged into the removed false start / first subscribe; timed from the 0.1 s level profile.
inject = [('Your', 104.26, 104.42), ('body', 104.42, 104.66), ('should', 104.66, 104.88), ('stay', 104.88, 105.14), ('Subscribe', 131.48, 131.80)]
src_words = [dict(w=x['word'].strip(), s=x['start'], e=x['end']) for x in words if not (103.0 < x['start'] < 103.2 or 131.0 < x['start'] < 131.1)]
src_words += [dict(w=w, s=a, e=b) for w, a, b in inject]; src_words.sort(key=lambda x: x['s'])
pieces, mapped, o = [], [], 0
for i, (a0, b0, why) in enumerate(ranges):
    n0, n1 = fr(a0), fr(b0); a, b = n0/fps, n1/fps; d = (n1-n0)/fps
    pieces.append(dict(source=str(S), source_in=a, source_out=b, out=o, duration=d, frames=n1-n0, n0=n0, n1=n1, why=why))
    for x in src_words:
        if a <= x['s'] < b: mapped.append(dict(w=x['w'], t0=o+x['s']-a, t1=min(o+d, o+x['e']-a)))
    o += d
# Equal-power 40 ms crossfade centred on each join, from source audio either side (all edges sit in room tone), so the
# room never dips to silence at a join (review 2: 25 ms fade-through at both joins). Length and sync unchanged.
SR = 48000; H = 0.02; total = round(o*SR); mix = np.zeros(total)
for i, p in enumerate(pieces):
    pre = H if i else 0.0; post = H if i < len(pieces)-1 else 0.0
    path = W/f'audio/piece-{i}.wav'
    ff(['-ss', p['source_in']-pre, '-i', S, '-t', p['duration']+pre+post, '-vn', '-af', 'pan=mono|c0=c0', '-ar', SR, '-c:a', 'pcm_s16le', path])
    sr, x = wavfile.read(path); x = x.astype(float); n = round((p['duration']+pre+post)*SR); x = np.pad(x[:n], (0, max(0, n-len(x))))
    g = np.ones(n); k = round(2*H*SR); ramp = np.sin(np.linspace(0, np.pi/2, k))
    if pre: g[:k] = ramp
    if post: g[-k:] = ramp[::-1]
    s0 = round((p['out']-pre)*SR); seg = (x*g)[:max(0, min(n, total-s0))]; mix[s0:s0+len(seg)] += seg
mix[:round(0.07*SR)] *= np.linspace(0, 1, round(0.07*SR))  # soften a lip tick 0.045 s in, 90 ms before the first word (review 4)
cut = np.clip(np.round(mix), -32768, 32767).astype(np.int16)
# Caption spelling: hyphen/dot fragments join the word before; filmed words otherwise unchanged.
out = []
for m in mapped:
    if m['w'][:1] in '-.' and out: out[-1]['w'] += m['w']; out[-1]['t1'] = m['t1']
    else: out.append(m)
for i in range(len(out)-1):
    if out[i]['w'].lower() == 'pull' and out[i+1]['w'].lower().rstrip(',.') == 'up': out[i+1]['w'] = 'pull-'+out[i+1]['w']; out[i+1]['t0'] = out[i]['t0']; out[i]['w'] = ''
out = [m for m in out if m['w']]
fix = {'pullups': 'Pull-ups', '6packapps.com': 'sixpackabs.com', 'v-taper': 'V-taper'}
for m in out:
    k = m['w'].lower().strip(',.'); tail = m['w'][len(m['w'].rstrip(',.')):]
    if k in fix: m['w'] = fix[k]+tail
wavfile.write(W/'audio/cut-raw.wav', 48000, cut)
plan = dict(category='CONTENT', type='SFC', title="How To Do Pull-Ups (And What To Do If You Can't Do One)", round=1, duration=o, frames=sum(p['frames'] for p in pieces),
            source=str(S), fps=fps, pieces=pieces, audio_joins=[pieces[1]['out'], pieces[2]['out']])
(W/'edit-plan.json').write_text(json.dumps(plan, indent=2)); (W/'records/words.json').write_text(json.dumps(out, indent=2))
# Audition window starts on the cut's first spoken word (VIDEO-RULES 2026-10-11); refuse a window that fails.
ff(['-i', W/'audio/cut-raw.wav', '-t', 30, '-c:a', 'pcm_s16le', W/'audio/audition-raw.wav'])
sr, x = wavfile.read(W/'audio/audition-raw.wav'); x = x/32768.
lv = [float(20*np.log10(np.sqrt(np.mean(x[int(i*sr/2):int((i+1)*sr/2)]**2))+1e-12)) for i in range(60)]
assert lv[0] > -35, lv[:3]
quiet = 0; longest = 0
for v in lv: quiet = quiet+1 if v < -40 else 0; longest = max(longest, quiet)
assert longest*0.5 <= 1.5, 'audition has a pause over 1.5 s'
(W/'evidence/audition-levels.json').write_text(json.dumps(dict(source='first 30 s of the cut', rms_per_half_second=lv), indent=2))
base = 'highpass=f=70,equalizer=f=140:t=q:w=1:g=1.5,equalizer=f=450:t=q:w=1.2:g=-1.5,equalizer=f=3200:t=q:w=1.5:g=-0.5'
opts = {'A': dict(name='Natural Warmth', eq=base+',equalizer=f=120:t=q:w=0.8:g=1.5'),
        'B': dict(name='Fuller Bass', eq=base+',equalizer=f=120:t=q:w=0.8:g=3'),
        'C': dict(name='Original Mic, Matched Volume', eq='anull'),
        'D': dict(name='Automatic Reference Match', eq=None)}
def chain(src, dst, k, v):
    cmd = [sys.executable, str(A/'voice_chain.py'), '--in', str(src), '--out', str(dst), '--no-dereverb', '--work', str(W/f'audio/work-{k}-{dst.stem}')]
    if v['eq']: cmd += ['--eq', v['eq'], '--no-expander-because', 'Dry outdoor lav; keep natural word tails (same as the approved DS-84 pool set).']
    with (W/f'evidence/{dst.stem}.log').open('w') as log: subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True)
for k, v in opts.items():
    out_ = W/f'audio/voice-{k}.wav'; chain(W/'audio/audition-raw.wav', out_, k, v)
    ff(['-i', out_, '-t', 30, '-c:a', 'libmp3lame', '-b:a', '160k', W/f'review/media/voice-{k}.mp3']); print('VOICE', k, flush=True)
chain(W/'audio/cut-raw.wav', W/'audio/voice-selected.wav', 'A', opts['A'])
(W/'audio/options.json').write_text(json.dumps(dict(options=opts, recommended='A', why='Dan chose Natural Warmth A on DS-84 and DS-47, same October 23 pool set and lav'), indent=2))
print('PREPARED', round(o, 3), flush=True)
