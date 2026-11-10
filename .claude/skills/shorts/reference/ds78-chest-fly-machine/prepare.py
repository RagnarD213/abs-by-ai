"""DS-78 R1: edit plan, caption word map, cut audio and the four voice auditions.
Source C1882 (portrait, lav = stream 0 channel 0, measured pick_lav). Take choice in records/take-choice.json."""
from pathlib import Path
import subprocess, json, os, sys
import numpy as np
from scipy.io import wavfile
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
F = R/'Media/video_edit/bin/ffmpeg'; os.environ['PATH'] = str(F.parent)+':'+os.environ['PATH']
S = Path('/Volumes/Extreme/10:23 dan rose fitness shoot - pool shorts and long form content/C1882.MP4'); A = R/'.claude/skills/_shared/audio'
sys.path.insert(0, str(R/'.claude/skills/_shared/renderq')); import renderq
renderq.hold_until_exit('DS-78 R1 audio prepare', pool='light', group='DS-78')
def ff(a): subprocess.run([str(F), '-nostdin', '-v', 'error', '-y']+list(map(str, a)), check=True)
fps = 30000/1001; fr = lambda t: round(t*fps)
# Source seconds, each edge inside measured silence (RMS < -44 dBFS, 0.1 s steps; evidence/takes).
ranges = [(268.75, 278.75, 'Take 23 hook (the only filmed hook; takes 19 and 22 at 244.0/264.5 are slates) through "I would pick the machine. First," (first read; its "set the s-" restart at 278.85-279.3 is cut).'),
          (280.67, 293.80, 'Restart "set the seat in the right position" (the word "first" of the restart, 280.3-280.6, is not used: listener preferred "First," from read 1 joined to this, 2 of 2) through "you risk tearing a pec."'),
          (297.45, 300.10, 'Second read of "That way you still get the stretch and it stays low risk." Read 1 (293.8-296.6) says "low as risk" (listener 2 of 2).'),
          (304.25, 314.30, 'Second read of the ad-lib "As far back as you can go, but no farther." (listener preferred it over the read at 300.3, 2 of 2), continuous through "let them back slowly to the stretch." Ends at 314.30, before a breath at 314.35 that made the join sound like "f-For" (join listen 1, measured 20 ms levels).'),
          (317.85, 333.45, 'Sets paragraph after the false start "Four sets." (315.0-315.7, removed): one clean read through "for all my newest videos." Ends 0.2 s after the last "s" (it was still sounding at 333.24; review r1 item 5).')]
words = json.load(open(S.with_suffix('.roll')/'words.json'))['words']
# Roll ASR timing fixes, from the 50 ms lav level profile (evidence/takes/levels.json) and the disfluency pass (evidence/takes/disfluency-asr.json):
# the restart's "set the" (280.75/280.94) are missing from the roll words (it timed the stumbled read's "set the" instead, outside the kept audio);
# the roll "as" at 300.00 is read 1 of the ad-lib, outside piece 3; onsets of "Chest", "As" and "For" sit later than the roll times.
src_words = [dict(w=x['word'].strip(), s=x['start'], e=x['end']) for x in words if 260 < x['start'] < 334 and abs(x['start']-300.00) > 0.01]
for x in src_words:
    for t, new in ((268.60, 268.85), (304.08, 304.45), (317.68, 318.05)):
        if abs(x['s']-t) < 0.01: x['s'] = new
src_words += [dict(w='set', s=280.75, e=280.92), dict(w='the', s=280.94, e=281.06)]
src_words.sort(key=lambda x: x['s'])
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
mix[:round(0.05*SR)] *= np.linspace(0, 1, round(0.05*SR))
mix[-round(0.08*SR):] *= np.linspace(1, 0, round(0.08*SR))   # the file ends in room tone, not on the tail of "videos" (independent review r1 item 5)
cut = np.clip(np.round(mix), -32768, 32767).astype(np.int16)
# Caption spelling: hyphen/dot fragments join the word before; filmed words otherwise unchanged.
out = []
for m in mapped:
    if m['w'][:1] in '-.' and out: out[-1]['w'] += m['w']; out[-1]['t1'] = m['t1']
    else: out.append(m)
fix = {'peck': 'pec', '6packabs.com': 'sixpackabs.com', '6backabs.com': 'sixpackabs.com', 'sixpackabs.com': 'sixpackabs.com'}
for m in out:
    k = m['w'].lower().strip(',.'); tail = m['w'][len(m['w'].rstrip(',.')):]
    if k in fix: m['w'] = fix[k]+tail
wavfile.write(W/'audio/cut-raw.wav', 48000, cut)
plan = dict(category='CONTENT', type='SFC', title="How To Do Chest Flies On The Machine", round=1, duration=o, frames=sum(p['frames'] for p in pieces),
            source=str(S), fps=fps, pieces=pieces, audio_joins=[p['out'] for p in pieces[1:]])
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
    if v['eq']: cmd += ['--eq', v['eq'], '--no-expander-because', 'Dry outdoor lav; keep natural word tails (same as the approved DS-76/DS-77 treatment of this roll).']
    with (W/f'evidence/{dst.stem}.log').open('w') as log: subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True)
for k, v in opts.items():
    out_ = W/f'audio/voice-{k}.wav'; chain(W/'audio/audition-raw.wav', out_, k, v)
    ff(['-i', out_, '-t', 30, '-c:a', 'libmp3lame', '-b:a', '160k', W/f'review/media/voice-{k}.mp3']); print('VOICE', k, flush=True)
chain(W/'audio/cut-raw.wav', W/'audio/voice-selected.wav', 'B', opts['B'])   # recommended: Dan's pick on T-Bar Rows (DS-77), same roll and lav
(W/'audio/options.json').write_text(json.dumps(dict(options=opts, recommended='B', why='Dan chose Fuller Bass B on How To Do T-Bar Rows (DS-77), same roll C1882 and lav, filmed minutes before this; A on Pull-Ups (DS-76)'), indent=2))
print('PREPARED', round(o, 3), flush=True)
