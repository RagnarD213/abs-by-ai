"""DS-30 Self-Driving Car SFC R1: cut list, audio (C1720 approved method: tone fitted to this take + 120 Hz +3 dB,
no expander, no dereverb), film-time word map and captions. Built from the DS-31 AI Homework recipe (same roll, same set).

Pieces (cut points measured on the 10 ms lav level map, work/lev10.npy; Whisper runs up to 0.35 s early after a pause):
  P1 205.47-229.18  "If you're too busy to work out ... before you get to the office."  (in: -79 dB before "If" at 205.57;
                    out: -52 dB room after "office." tail, before the breath of the false start "The Tesla does..." 229.51)
  P2 253.00-260.86  final take of the look-away line, first sentence: "The Tesla does check you're watching the road, but you
                    can look away from the road for significant amounts of time and go on your phone or look at another screen."
                    (in: -81 dB, "The" onset 253.07; out: -61 dB after "screen." decay, before the breath of "You can go on your laptop")
  P3 267.60-269.80  "And a Tesla isn't a rich guy's car." (in: inside the breath before "And" 267.78 so the join keeps a natural
                    sentence gap; out: -71 dB after "car." 269.75, before the false KBB takes)
  P4 296.40-324.30  final KBB take "$47,000 ... $48,000" through "Subscribe ... get in shape." (in: -80 dB, "Kelly" onset 296.45;
                    out: room tone 0.3 s after "shape.")
Skipped: the slate, the first two tries of the look-away line (229.5-252.9), the second sentence of the final look-away take
(laptop / 30 seconds / glance, 261.1-267.4, cut for length: the Short would run 67 s against the 66 s ceiling) and the four
earlier KBB tries ($57,000 and garbled, 270.2-296.4).
"""
from pathlib import Path
import json, subprocess, sys, os, re
import numpy as np
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
F = str(R/'Media/video_edit/bin/ffmpeg'); A = R/'.claude/skills/_shared/audio'; FPS = 30000/1001
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
S = '/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1720.MP4'
def ff(x): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, x)), check=True)

# R1 audit fixes: P2 runs on through the breath after "screen." (out 261.04, -80 dB before "You" 261.11); P3 starts at the dip
# just before "And" (267.75; the old 267.60 in-point landed mid-inhale and clicked) and runs to 269.94 (breath, then quiet);
# P4 starts at 296.27 so "Kelley Blue Book" gets a natural sentence pause (it had ~90 ms). 20 ms fades at every piece edge.
CUTS = [(205.47, 229.18), (253.00, 261.04), (267.75, 269.83), (296.16, 324.30)]   # re-check: P3 ends before the inhale after "car."; the pause comes from P4's head
pieces = [dict(start=a, frames=int(round((b - a)*FPS))) for a, b in CUTS]
t = 0
for p in pieces:
    p['duration'] = p['frames']/FPS; p['film0'] = t; t += p['duration']
TOTAL = sum(p['frames'] for p in pieces)
(W/'edl.json').write_text(json.dumps(dict(source=S, fps='30000/1001', total_frames=TOTAL, total_seconds=TOTAL/FPS, pieces=pieces), indent=2))

O = W/'audio'; O.mkdir(exist_ok=True)
if '--no-audio' not in sys.argv:
    for i, p in enumerate(pieces):
        ff(['-ss', p['start'], '-i', S, '-t', p['duration'], '-map', '0:a:0', '-af',
            f"pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0+0.5*c1,apad,atrim=duration={p['duration']},afade=t=in:d=0.02,afade=t=out:st={p['duration'] - 0.02:.4f}:d=0.02", '-ar', 48000, '-c:a', 'pcm_s24le', O/f'raw-{i}.wav'])
    cat = O/'raw-concat.txt'; cat.write_text(''.join(f"file '{O}/raw-{i}.wav'\n" for i in range(len(pieces))))
    ff(['-f', 'concat', '-safe', 0, '-i', cat, '-c', 'copy', W/'untreated.wav'])
    # Tone fitted to THIS take with the shared fitter (the method Dan approved on DS-28 and kept on DS-31), then the
    # standard +3 dB at 120 Hz. Variants for the voice options are made by voice_options.py from the same fit.
    sys.path.insert(0, str(A)); import voice_chain as V; import reference as Ref
    ref_audio, ref = Ref.resolve(); work = W/'voice-refit'; work.mkdir(exist_ok=True)
    lav, x, how = V.pull(str(W/'untreated.wav'), None, 'pan=mono|c0=0.5*c0+0.5*c1', str(work))
    eq0, gains, step = V.fit_eq(lav, ref, str(work))
    (W/'fit-voice-eq.json').write_text(json.dumps(dict(eq_fitted=eq0, eq=eq0 + ',equalizer=f=120:t=q:w=0.8:g=3.0', gains=gains), indent=1))
    subprocess.run([sys.executable, str(A/'voice_chain.py'), '--in', str(W/'untreated.wav'), '--out', str(W/'voice.wav'),
                    '--pull', 'pan=mono|c0=0.5*c0+0.5*c1', '--eq', eq0 + ',equalizer=f=120:t=q:w=0.8:g=3.0',
                    '--no-expander-because', 'Same roll and mic as DS-28/DS-31, whose fitted tone with bass and no expander Dan approved; preserve word tails.',
                    '--work', str(W/'voice-work')], check=True)

# Words -> film time. medium.en on the lav, with two garbled stretches re-read in windows (work/words_windows.json):
# 304.8-310.8 (first pass dropped "car that drives you everywhere. And if you") and 252.5-262.0.
words = json.load(open(W/'work/words_medium.json'))['words']
win = json.load(open(W/'work/words_windows.json'))
for key, a, b in [('w1.wav', 304.8, 310.78), ('w3.wav', 252.5, 261.98)]:
    words = [w for w in words if not (a <= w['s'] < b)] + [dict(w=x['w'], s=x['s'], e=x['e'], p=1) for x in win[key] if a <= x['s'] < b]
words.sort(key=lambda w: w['s'])
for w in words:
    if w['w'] == 'The' and abs(w['s'] - 252.50) < 0.01: w['s'] = 253.07   # the window pass stretched 'The' back over the breath; onset measured 253.07
    w['w'] = w['w'].replace('...', '')
# Snap each word that follows a pause to its measured onset (first 10 ms frame above -40 dB within +-0.5 s): Whisper put
# "If" at 205.22, the voice starts 205.57.
lev = np.load(W/'work/lev10.npy'); OFF = 194.0
def onset(s, lo):
    i0 = max(0, int((max(s - 0.5, lo) - OFF)*100)); i1 = int((s + 0.5 - OFF)*100)
    hit = np.where(lev[i0:i1] > -40)[0]   # first voiced frame after the previous word (its tail is skipped by lo)
    return round(OFF + (i0 + hit[0])/100, 3) if len(hit) else s
prev_e = -9
for w in words:
    if w['s'] - prev_e > 0.15:
        o = onset(w['s'], prev_e + 0.10)
        # a snap may move a word later only after a real pause (Whisper stretches the first word back over silence);
        # inside running speech it can land on a dip within the word (re-check: "Subscribe" and "A base" ran 0.14-0.27 s late)
        if abs(o - w['s']) <= 0.5 and o < w['e'] and (o <= w['s'] + 0.12 or w['s'] - prev_e > 0.45): w['s'] = o
    prev_e = w['e']
# A long word that holds a silence (Whisper stretched it back over the pause: "Take" 222.66 really 223.17, "So" 304.80 really
# 305.50) starts at the onset after that silence (>= 0.04 s under -62 dB).
for w in words:
    if w['e'] - w['s'] > 0.45:
        i0 = int((w['s'] - OFF)*100); i1 = int((w['e'] - OFF)*100); seg = lev[i0:i1]
        q = np.where(seg < -62)[0]
        if len(q) >= 4:
            last = q[-1]; hit = np.where(seg[last:] > -40)[0]
            if len(hit): w['s'] = round(OFF + (i0 + last + hit[0])/100, 3)
out = []
for p in pieces:
    a, b = p['start'], p['start'] + p['duration']
    for w in words:
        if a <= w['s'] < b - 0.02:
            out.append(dict(w=w['w'], t0=round(w['s'] - a + p['film0'], 3), t1=round(min(w['e'], b) - a + p['film0'], 3), src=w['s']))
# Spelling: Dan's words as he said them, in the script's spelling.
i = 0; fixed = []
while i < len(out):
    w = dict(out[i]); nx = out[i+1] if i + 1 < len(out) else None
    if nx and re.fullmatch(r'\$\d+', w['w']) and nx['w'].startswith(',000'):
        w['w'] = w['w'] + nx['w']; w['t1'] = nx['t1']; i += 2; fixed.append(w); continue
    if nx and w['w'].lower() == 'robo' and nx['w'].startswith('-taxi'):
        w['w'] = 'robotaxis' + nx['w'][len('-taxis'):]; w['t1'] = nx['t1']; i += 2; fixed.append(w); continue
    if nx and w['w'].lower() == 'self' and nx['w'].startswith('-driving'):
        w['w'] = 'self-driving' + nx['w'][len('-driving'):]; w['t1'] = nx['t1']; i += 2; fixed.append(w); continue
    if nx and w['w'].lower() == 'five' and nx['w'].lower() == 'year':
        w['w'] = 'five-year'; w['t1'] = nx['t1']; i += 2; fixed.append(w); continue
    FIX = {'Kelly': 'Kelley', 'model': 'Model', 'three': '3', 'camry': 'Camry', 'camry.': 'Camry.'}
    w['w'] = FIX.get(w['w'], w['w']); fixed.append(w); i += 1
out = fixed
(W/'words_out.json').write_text(json.dumps(out, indent=1))
print(' '.join(w['w'] for w in out))

# Captions: the approved DS-28/DS-31 style (Arial Bold 86, outline 7, shadow 3, MarginV 420), DS-31's chunking.
head = open('/Volumes/Extreme/_edit_work/ds31/round2/captions.ass')  # the DS-28 header, as DS-31 carried it
head = head.read().split('[Events]')[0]
chunks = []; sent = []
for i, w in enumerate(out):
    sent.append(w)
    nxt = out[i+1] if i + 1 < len(out) else None
    if w['w'][-1] in '.?!,' or nxt is None or nxt['t0'] - w['t1'] > 0.6:
        n = len(sent); k = 0; cl = []
        while k < n:
            take = 3 if n - k == 3 else 2
            cl.append(sent[k:k+take]); k += take
        j = 0
        while j < len(cl):
            if cl[j][-1]['t1'] - cl[j][0]['t0'] < 0.26 and len(cl) > 1:
                nbs = [x for x in (j + 1, j - 1) if 0 <= x < len(cl) and len(cl[j]) + len(cl[x]) <= 4]
                if nbs:
                    a_, b_ = sorted((j, nbs[0])); cl[a_:b_+1] = [cl[a_] + cl[b_]]; continue
            j += 1
        chunks += cl
        sent = []
def ts(x): cs = round(x*100); return f'{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}'
lines = []
for j, c in enumerate(chunks):
    a = c[0]['t0']; b = c[-1]['t1'] + 0.12
    if j + 1 < len(chunks): b = min(max(b, a + 0.30), chunks[j+1][0]['t0'])
    for jn in (q['film0'] for q in pieces[1:]):
        if a < jn < b + 0.034: b = min(b, jn - 0.034)
    text = ' '.join(x['w'].rstrip(',') for x in c)
    text = re.sub(r'\bai\b', 'AI', text, flags=re.I)
    if j == 0 or chunks[j-1][-1]['w'][-1] in '.?!': text = text[0].upper() + text[1:]
    lines.append(f'Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,{text}')
(W/'captions.ass').write_text(head + '[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n' + '\n'.join(lines) + '\n')
print('PREP READY', TOTAL, round(TOTAL/FPS, 3), len(out), 'words', len(lines), 'cues')
