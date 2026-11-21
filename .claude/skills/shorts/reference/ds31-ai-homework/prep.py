"""DS-31 AI Homework SFC R1: cut list, audio (approved C1720 chain), film-time word map and captions.
Source: C1720 main take 335.28-380.20 (skips the flubbed first try of the 'young guys' line), retake 386.34-404.95.
"""
from pathlib import Path
import json, subprocess, sys, os, re
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
F = str(R/'Media/video_edit/bin/ffmpeg'); A = R/'.claude/skills/_shared/audio'; FPS = 30000/1001
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
S = '/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1720.MP4'
def ff(x): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, x)), check=True)

# Cut points measured at 20 ms on the lav (work/levels): in 335.28 is -67 dB before "If" (335.42);
# 380.20 sits in the 0.26 s gap after "this." (380.16-380.44); 386.34 is breath-floor before "I've" (386.44);
# 404.95 is room tone 0.35 s after "shape." ends (404.60).
# 367.22-369.10: a false start ("Use the paid Cl-", 367.32-368.12, then 1.0 s of silence) before the clean retake
# "Use a paid Claude plan" (369.16) is removed. Out 367.22 is -60 dB room tone after "undetectable."; the picture
# changes framing (tight to wide) on that join.
pieces = [dict(start=335.28, frames=957), dict(start=369.10, frames=333), dict(start=386.34, frames=558)]
t = 0
for p in pieces:
    p['duration'] = p['frames']/FPS; p['film0'] = t; t += p['duration']
TOTAL = sum(p['frames'] for p in pieces)
(W/'edl.json').write_text(json.dumps(dict(source=S, fps='30000/1001', total_frames=TOTAL, total_seconds=TOTAL/FPS, pieces=pieces), indent=2))

# Audio: untreated pull, then the exact approved DS-28 R3 chain for this roll (fitted tone + 120 Hz +3 dB, no expander, no dereverb).
O = W/'audio'; O.mkdir(exist_ok=True)
for i, p in enumerate(pieces):
    ff(['-ss', p['start'], '-i', S, '-t', p['duration'], '-map', '0:a:0', '-af',
        f"pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0+0.5*c1,apad,atrim=duration={p['duration']}", '-ar', 48000, '-c:a', 'pcm_s24le', O/f'raw-{i}.wav'])
cat = O/'raw-concat.txt'; cat.write_text(''.join(f"file '{O}/raw-{i}.wav'\n" for i in range(len(pieces))))
ff(['-f', 'concat', '-safe', 0, '-i', cat, '-c', 'copy', W/'untreated.wav'])
approved = json.load(open('/Volumes/Extreme/_edit_work/ds28/round3/voice.wav.voice_chain.json'))
eq = approved['eq']; assert eq.endswith('equalizer=f=120:t=q:w=0.8:g=3.0')
# R1 audit: the DS-28 curve measured duller on this take (5.5 kHz -5.3 dB vs Meal Prep's -3.1). Same method Dan approved
# (tone fitted to the recording + 120 Hz +3 dB, no expander), fitted to THIS recording by recipe/audio_refit.py.
if (W/'fit-voice-eq.json').exists(): eq = json.load(open(W/'fit-voice-eq.json'))['eq']; assert eq.endswith('equalizer=f=120:t=q:w=0.8:g=3.0')
if '--no-audio' not in sys.argv:
    subprocess.run([sys.executable, str(A/'voice_chain.py'), '--in', str(W/'untreated.wav'), '--out', str(W/'voice.wav'),
                    '--pull', 'pan=mono|c0=0.5*c0+0.5*c1', '--eq', eq,
                    '--no-expander-because', 'Same roll and mic as DS-28, whose fitted tone with bass and no expander Dan approved (R3, kept in R5); preserve word tails.',
                    '--work', str(W/'voice-work')], check=True)

# Words -> film time. Whisper medium.en on the lav; spelling fixes for words Dan said that ASR misspells.
words = json.load(open(W/'work/words_medium.json'))['words']
# medium.en ran the false start and the retake together ('a' 367.50-369.56). Words of the retake from a separate
# medium.en pass on 369.0-371.4 (audio/chk2.wav): use 369.16, a 369.34.
words = [w for w in words if not (367.3 <= w['s'] < 369.5)] + [dict(w='Use', s=369.16, e=369.34, p=1), dict(w='a', s=369.34, e=369.56, p=1)]
words.sort(key=lambda w: w['s'])
# "I've" is timed early on both tries of the 'young guys' line (380.16 and 386.24; measured onsets 380.46 and 386.44):
# the first try's word sits after the cut and is dropped, the retake's moves to its measured onset.
words = [w for w in words if abs(w['s'] - 380.16) > 0.01]
for w in words:
    if abs(w['s'] - 386.24) < 0.01: w['s'] = 386.44
FIX = {'clog': 'Claude', 'schoolwork.': 'schoolwork.'}
out = []
for p in pieces:
    a, b = p['start'], p['start'] + p['duration']
    for w in words:
        mid_in = a <= w['s'] < b - 0.02
        if not mid_in: continue
        txt = FIX.get(w['w'], w['w'])
        out.append(dict(w=txt, t0=round(w['s'] - a + p['film0'], 3), t1=round(min(w['e'], b) - a + p['film0'], 3), src=w['s']))
# "checker as your" -> heard both ways by medium/small; script and small.en both give "checkers your".
for i in range(len(out) - 1):
    if out[i]['w'] == 'checker' and out[i+1]['w'] == 'as':
        out[i]['w'] = 'checkers'; out[i+1]['w'] = ''
out = [w for w in out if w['w']]
(W/'words_out.json').write_text(json.dumps(out, indent=1))

# Captions: the approved DS-28 style (Arial Bold 86, outline 7, shadow 3, MarginV 420), two-word chunks,
# break on punctuation or a gap > 0.6 s; hold each cue to the next cue start (never overlap).
head = open('/Volumes/Extreme/_edit_work/ds28/round3/captions.ass').read().split('[Events]')[0]
# Sentence-aware chunking: two words per cue, never a lone trailing word (a sentence's last word joins the
# previous cue as a three-word cue), break on . ? ! or a gap > 0.6 s. Commas print as in DS-28: dropped.
chunks = []; sent = []
for i, w in enumerate(out):
    sent.append(w)
    nxt = out[i+1] if i + 1 < len(out) else None
    # clause break on , . ? ! or a gap > 0.6 s (R1 audit: "Listen almost" and "this but" ran two clauses together)
    if w['w'][-1] in '.?!,' or nxt is None or nxt['t0'] - w['t1'] > 0.6:
        n = len(sent); k = 0; cl = []
        while k < n:
            take = 3 if n - k == 3 else 2
            cl.append(sent[k:k+take]); k += take
        # audit 2: a cue shorter than 0.26 s flashes; merge it into its clause neighbour (max 4 words)
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
    for jn in (q['film0'] for q in pieces[1:]):   # a cue never runs across an edit join (judge, R1: 3-frame hold at 0:43.04)
        if a < jn < b: b = jn
    text = ' '.join(x['w'].rstrip(',') for x in c)
    text = re.sub(r'\bai\b', 'AI', text, flags=re.I)
    if j == 0 or chunks[j-1][-1]['w'][-1] in '.?!': text = text[0].upper() + text[1:]
    lines.append(f'Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,{text}')
(W/'captions.ass').write_text(head + '[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n' + '\n'.join(lines) + '\n')
print('PREP READY', TOTAL, round(TOTAL/FPS, 3), len(out), 'words', len(lines), 'cues')
