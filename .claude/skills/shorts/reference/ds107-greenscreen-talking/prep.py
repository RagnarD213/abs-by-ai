"""DS-107 R1 prep: edit list, audio options and the film-time word map.   python3 prep.py [--no-audio]
"Your Metabolism Is Not The Reason You're Fat" (B08), 11/13 green screen, roll C1908 (portrait, lav a:0 c0 single-live).
Every cut sits in measured quiet (audio/takes_db10ms.npy + takes_hf10ms.npy, medium.en words audio/talk_words.json; Whisper runs
up to 0.5 s early on this roll, so the level map decides). Last clean take of every line:
  P1 110.55-131.42  hook take 2 (take 1 100.84-109.86 is the same words; the last clean read wins) and the study, one continuous read:
                    "Your metabolism at 45 is the same as it was at 25. I'll prove it to you and show you the real reason why people
                    gain weight as they age. A study published in Science in 2021 looked at 6,421 people in 29 countries. Adjusted
                    for body size, calories burned stayed flat from 20 to 60."
  P3 173.87-176.52  "After 60, it drops less than 1% a year."  (fourth read; reads 1-2 say "drops by", the script says "drops less";
                    read 3 is followed by "Is my position good?")
  P4 182.62-187.52  "So, what changed since you were 25? Four things, and they were all hit after 40."  (third read)
  P5 206.32-236.42  "You have more stress, a career, a mortgage, and kids. ... Bottom line, it's not your age,"  (the first try at
                    188.06 stops after "A career." and an aside; 205.92 is a lip click, the voice starts 206.36)
  P6 244.86-250.80  "Which means you can fix it. Subscribe to my channel and go to SixPackAbs.com for all my newest videos."
                    (his retake of the close; the first close 236.54-242.46 says "which means that you can fix it"; 'videos'
                    fricative ends 250.55, then 0.25 s of room and a 30 ms fade)
"""
from pathlib import Path
import json, subprocess, sys, os
import numpy as np
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
F = str(R/'Media/video_edit/bin/ffmpeg'); A = R/'.claude/skills/_shared/audio'; FPS = 30000/1001
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
SRC = '/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/C1908.MP4'
O = W/'main'; O.mkdir(exist_ok=True); (O/'audio').mkdir(exist_ok=True)
def ff(x): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, x)), check=True)
def fr(t): return int(round(t*FPS))
TALK = [('P1', 110.88, 131.42), ('P3', 173.87, 176.52), ('P4', 182.62, 187.52), ('P5', 206.32, 234.47), ('P5b', 234.70, 236.42), ('P6', 244.86, 250.80)]
# R1 review: P1 starts after the inhale (110.55-110.88, about -36 dBFS; 'Your' from 110.95); the 0.51 s pause before 'Bottom line' loses 0.23 s
# at the cut to the before photo (P5 ends 234.47 in the quiet, P5b starts 234.70).
XF = 0.010
_subs = json.load(open(Path(__file__).resolve().parent/'key_subs.json')) if (Path(__file__).resolve().parent/'key_subs.json').exists() else {}
KEY = dict(T=[[k, a, d] for k, (a, d) in _subs.items()])
pieces = []; n = 0
for pid, a, b in TALK:
    k = fr(b - a); pieces.append(dict(id=pid, key='T', source=SRC, start=a, frames=k, duration=k/FPS, n0=n, film0=n/FPS)); n += k
TOTAL = n
edl = dict(version='main', fps='30000/1001', total_frames=TOTAL, total_seconds=TOTAL/FPS, pieces=pieces, key=KEY)
(O/'edl.json').write_text(json.dumps(edl, indent=1))

# Voice options (VIDEO-RULES 2026-10-16: level-matched choices in round 1). House = the DS-41 Kevin James voice on the same green
# screen set and mic layout (DS-40 house EQ + half bass lift, expander on); per-take tone fitted below only if the voice-alone gate
# rows ask for it.
E_EQ = ('highpass=f=70,equalizer=f=110:t=q:w=1.3:g=-5.89,equalizer=f=194:t=q:w=1.3:g=+0.46,equalizer=f=316:t=q:w=1.3:g=+1.95,'
        'equalizer=f=490:t=q:w=1.3:g=+2.44,equalizer=f=735:t=q:w=1.3:g=+1.63,equalizer=f=1122:t=q:w=1.3:g=+1.21,'
        'equalizer=f=1755:t=q:w=1.3:g=+1.12,equalizer=f=2775:t=q:w=1.3:g=+0.55,equalizer=f=4387:t=q:w=1.3:g=-3.65,'
        'treble=g=-1.65:f=6500:width_type=q:width=0.6,equalizer=f=120:t=q:w=0.8:g=+1.5')
BAL = 'highpass=f=70,equalizer=f=110:t=q:w=0.8:g=-1.5,equalizer=f=550:t=q:w=0.8:g=1.3,equalizer=f=1100:t=q:w=0.8:g=1.6,equalizer=f=3200:t=q:w=0.8:g=-0.7'
TAKE_EQ = ''   # (house voice: unchanged)
# the Balanced voice (blind-listening winner) fitted per take to the reference voice's bands (audio_gate --reference-rows-only); take_eq.json
BAL_EQ = os.environ.get('BAL_EQ', json.load(open(W/'take_eq.json'))['balanced'] if (W/'take_eq.json').exists() else '')
VOICES = {'house_bass15': dict(eq=E_EQ + TAKE_EQ, expander=True, label='House voice (DS-41 green screen) + bass lift'),
          'fitted': dict(eq=None, expander=True, label='Chain default: EQ fitted to the reference voice'),
          'balanced': dict(eq=BAL + BAL_EQ, expander=False, label='Balanced (lighter EQ, no expander), tone fitted to this take'),
          'untreated': dict(eq='highpass=f=40', expander=False, label='Untreated lav, level matched only')}

if '--no-audio' not in sys.argv:
    parts = []
    for i, p in enumerate(pieces):
        last = i == len(pieces) - 1
        d = p['duration'] + (0 if last else XF)
        af = 'pan=mono|c0=c0' + (f",afade=t=out:st={d-0.03}:d=0.03" if last else '')
        ff(['-ss', p['start'], '-i', SRC, '-t', d, '-map', '0:a:0', '-af', af, '-ar', 48000, '-c:a', 'pcm_s24le', O/'audio'/f"lav-{p['id']}.wav"])
        parts.append(O/'audio'/f"lav-{p['id']}.wav")
    ins = []; fc = ''; prev = '0:a'
    for i in range(1, len(parts)):
        ins += ['-i', parts[i]]; fc += f'[{prev}][{i}:a]acrossfade=d={XF}:c1=tri:c2=tri[x{i}];'; prev = f'x{i}'
    fc += f'[{prev}]apad,atrim=duration={TOTAL/FPS:.6f}[lav]'
    ff(['-i', parts[0]] + ins + ['-filter_complex', fc, '-map', '[lav]', '-ar', 48000, '-c:a', 'pcm_s24le', O/'lav.wav'])
    only = os.environ.get('VOICES_ONLY', '').split(',') if os.environ.get('VOICES_ONLY') else list(VOICES)
    for name in only:
        v = VOICES[name]
        cmd = [sys.executable, str(A/'voice_chain.py'), '--in', str(O/'lav.wav'), '--out', str(O/f'voice-{name}.wav'), '--work', str(O/'audio'/f'chain-{name}'),
               '--target', '-14.1', '--tp', '-1.5', '--oversample', '4', '--pull', 'pan=mono|c0=c0']
        if v['eq']: cmd += ['--eq', v['eq']]
        if not v['expander']:
            cmd += ['--no-expander-because', f"{v['label']}: a round-1 voice option, no expander so complete word tails stay."]
        subprocess.run(cmd, check=True)
    (O/'audio-options.json').write_text(json.dumps(VOICES, indent=1))

# ---- words on the film timeline (Dan only)
out = []
dw = json.load(open(W/'audio/talk_words.json'))
DW_FIX = json.load(open(W/'audio/wordfix.json')) if (W/'audio/wordfix.json').exists() else {}
drop = set(DW_FIX.get('drop', [])); text = DW_FIX.get('text', {})
dw = [dict(x, w=text.get(f"{round(x['t'], 2):.2f}", x['w'])) for x in dw if round(x['t'], 2) not in drop]
dw += [dict(w=w, t=t, e=e, fixed=True) for w, t, e in DW_FIX.get('add', [])]
dw.sort(key=lambda x: x['t'])
# Whisper runs early on this roll (up to 0.5 s): snap each word's start to the lav's speech onset (first 10 ms bin over -42 dB inside the word)
_db = np.load(W/'audio/takes_db10ms.npy'); _T0 = float(open(W/'audio/takes_db10ms.t0').read())
for x in dw:
    i0, i1 = int((x['t'] - _T0)*100), int((x['e'] - _T0)*100)
    if 0 <= i0 < i1 <= len(_db) and not x.get('fixed'):
        hit = np.where(_db[i0:i1] > -42)[0]
        if len(hit) and hit[0]/100 > 0.12: x['t'] = round(_T0 + (i0 + hit[0])/100 - 0.03, 3)
for p in pieces:
    a, b = p['start'], p['start'] + p['duration']
    for w in dw:
        if w['e'] <= a or w['t'] >= b or (min(w['e'], b) - max(w['t'], a)) < 0.5*max(w['e'] - w['t'], 1e-3): continue
        out.append(dict(w=w['w'], t0=round(max(w['t'], a) - a + p['film0'], 3), t1=round(min(w['e'], b) - a + p['film0'], 3), src=w['t'], piece=p['id'], speaker='dan', fixed=bool(w.get('fixed'))))
FIX = {'6packabs': 'SixPackAbs', 'sixpackapps': 'SixPackAbs', 'sixbackapps': 'SixPackAbs', 'sixpackabs': 'SixPackAbs'}
for w in out:
    k_ = w['w'].lower().rstrip('.,')
    if k_ in FIX: w['w'] = FIX[k_]
k = 0
while k < len(out) - 1:          # "6" ",421" -> "6,421", "1" "%" -> "1%", "SixPackAbs" ".com"
    nx = out[k + 1]['w']
    if (nx[:1] in ',.%' or nx.startswith('.com')) and out[k]['piece'] == out[k + 1]['piece']:
        out[k]['w'] += nx; out[k]['t1'] = out[k + 1]['t1']; del out[k + 1]
    else: k += 1
(O/'words_out.json').write_text(json.dumps(out, indent=1))
print('PREP frames', TOTAL, round(TOTAL/FPS, 3), 's', [(p['id'], p['frames'], round(p['film0'], 2)) for p in pieces], len(out), 'words')
