"""DS-40 R6 delivery inputs: the untreated timeline mix, the SRT, delivered-audio ASR on this exact file, and the gate plan
(DS-44 / DS-33 schema).    python3 gateplan_r6.py MASTER.mp4"""
from pathlib import Path
import subprocess, json, hashlib, os, sys
import numpy as np
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path('/Volumes/Expansion/_edit_work/ds40/r6')
F = str(R / 'Media/video_edit/bin/ffmpeg'); FPS = 30000 / 1001; SR = 48000
os.environ['PATH'] = str(R / 'Media/video_edit/bin') + ':' + os.environ['PATH']
master = Path(sys.argv[1]); sha = hashlib.sha256(master.read_bytes()).hexdigest()
P = json.load(open(W / 'plan.json')); cues = json.load(open(W / 'cues.json')); man = json.load(open(W / 'gfx/hf/manifest.json'))
words = json.load(open(W / 'words_film.json'))
ROLL0 = P['rollf0'] / FPS

# ---- untreated timeline: the clip's original sound (R3 clip_raw, same 581 frames) + the raw lav, cut exactly like the film
def load(path, mono=False):
    b = subprocess.run([F + '.real', '-v', 'error', '-i', str(path), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.float32).reshape(-1, 2).copy()
S = lambda t: int(round(t * SR))
clip = load('/Volumes/Expansion/_edit_work/ds40/r3/audio/clip_raw.wav'); n = S(P['n_clip'] / FPS)
clip = np.pad(clip, ((0, max(0, n - len(clip))), (0, 0)))[:n]
raw = load(W / 'audio/dan_raw.wav'); raw[:, 1] = raw[:, 0]
c1o, c1n = P['cut1']; c2o, c2n = P['cut2']
segs = [(0.0, c1o - ROLL0), (c1o + c1n / FPS - ROLL0, c2o - ROLL0), (c2o + c2n / FPS - ROLL0, (P['rollf0'] + P['j_end'] + 1) / FPS - ROLL0)]
un = np.concatenate([clip] + [raw[S(a):S(b)] for a, b in segs])
want = S(P['f_end'] / FPS); un = np.pad(un, ((0, max(0, want - len(un))), (0, 0)))[:want]
subprocess.run([F + '.real', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a', 'pcm_s24le', str(W / 'mix-untreated.wav')],
               input=un.astype(np.float32).tobytes(), check=True)
audio_joins = [P['n_clip'] / FPS, P['n_clip'] / FPS + segs[0][1], P['n_clip'] / FPS + segs[0][1] + (segs[1][1] - segs[1][0])]

# ---- SRT (the burned cues, as text)
def stamp(t): h, r = divmod(t, 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"
srt = master.parent / f'{master.stem.replace(" - complete Short", "")}.srt'
srt.write_text(''.join(f"{i + 1}\n{stamp(c['a'])} --> {stamp(c['b'])}\n{chr(10).join(c['lines'])}\n\n" for i, c in enumerate(cues)))

# ---- delivered-audio ASR on this exact file, windows split at the audio joins
asr = W / 'finished-asr.json'
if not asr.exists() or json.load(open(asr)).get('video_sha256') != sha:
    import whisper
    m = whisper.load_model('medium.en'); ws = []; texts = []
    cuts = [0.0] + audio_joins + [P['f_end'] / FPS]
    for a_, b_ in zip(cuts, cuts[1:]):
        wav = W / 'audio' / f'delivered_{a_:.2f}.wav'
        subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', f'{a_:.4f}', '-i', str(master), '-t', f'{b_ - a_:.4f}', '-ac', '1', '-ar', '16000', str(wav)], check=True)
        r = m.transcribe(str(wav), language='en', fp16=False, word_timestamps=True, temperature=0); texts.append(r['text'].strip())
        ws += [dict(w=x['word'].strip(), t=round(x['start'] + a_, 3), e=round(x['end'] + a_, 3)) for s_ in r['segments'] for x in s_['words']]
    asr.write_text(json.dumps(dict(video_sha256=sha, model='medium.en', method='delivered audio, windows split at every audio join', text=' '.join(texts), words=ws), indent=1))
A = json.load(open(asr))
old = json.load(open('/Volumes/Extreme/_edit_work/ds31/round2/gate-plan.json'))
t_clip, t_settle = P['n_clip'] / FPS, (P['n_clip'] + P['move']) / FPS
b0, b1, end = P['f_bmi0'] / FPS, P['f_bmi1'] / FPS, P['f_end'] / FPS
card_cuts = [s['f0'] / FPS for s in P['card'][1:3]]
g3 = next(m for m in man if m['id'] == 'G3')
plan = dict(
    scope='CONTENT SFC R6 (DS-40). The Bill Maher clip (Real Time, HBO) first, full screen, Dan keyed small lower left at 0.40 '
          'watching it (C1730, locked B format); a 0.5 s move into the R2 layout (card at the top playing silent footage from the '
          'same episode, large keyed Dan, C1730 scripted take); full-screen BMI table covering two ad-lib cuts. House key (R2).',
    target_seconds=P['f_end'] / FPS, target_frames=P['f_end'],
    joins=sorted([t_clip, b0, b1] + card_cuts), audio_joins=audio_joins,
    punch=[[0.0, t_clip, 'S0-clip-corner'], [t_clip, t_settle, 'M-move'], [t_settle, b0, 'L1-layout'], [b0, b1, 'G3-bmi'], [b1, end, 'L2-layout']],
    punch_covered=[True, True, False, True, False],
    covered=[[0.0, t_clip], [t_clip, t_settle], [b0, b1]],
    source_audio=str(W / 'mix-untreated.wav'), srt=str(srt),
    words=[dict(w=x['w'], t=x['t'], e=x['e']) for x in words],
    graphics=[dict(name=m['id'], beat=[m['a'], m['b']], mov=m['mov']) for m in man],
    graphic_regions=[dict(name=m['id'], beat=[m['a'], m['b']], rect=[m['box'][0], m['box'][1], m['box'][2] - m['box'][0], m['box'][3] - m['box'][1]]) for m in man if 'box' in m]
                    + [dict(name='G3-table', beat=[b0, b1], rect=[36, 182, 1008, 1196])],
    ai_inserts=[], real_photos=[], cards=[],
    label_chips=old['label_chips'], label_pos=old['label_pos'],
    watch_log=str(W / 'qa/watch_pass.json'), evidence_contract=dict(version=2, video_sha256=sha),
    transcript_words=[dict(w=x['w']) for x in A['words']], speech_words=A['words'],
    speech_words_evidence=dict(method='delivered_asr', video_sha256=sha),
    banned_source=old['banned_source'], banned_times=old['banned_times'],
    talking_head_windows=[dict(name='S0-corner', beat=[0.0, t_clip], rect=[0, 1152, 432, 768], motion='fixed-wide'),
                          dict(name='L1', beat=[t_settle, b0], rect=[0, 175, 1080, 1745], motion='fixed-wide'),
                          dict(name='L2', beat=[b1, end], rect=[0, 175, 1080, 1745], motion='fixed-wide')],
    junk_report=str(W / 'junk_report.json'),
)
(W / 'gate-plan.json').write_text(json.dumps(plan, indent=1))
print('GATE PLAN', sha[:16], 'joins', [round(j, 2) for j in plan['joins']], 'audio joins', [round(j, 2) for j in audio_joins], '|', A['text'][:160])
