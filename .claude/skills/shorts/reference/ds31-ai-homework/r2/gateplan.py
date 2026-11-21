"""Gate evidence for the delivered master: graphic alpha MOVs (same draw routine on black/white), delivered-audio ASR,
and gate-plan.json in the DS-28 schema."""
from pathlib import Path
import subprocess, json, hashlib, os, sys, importlib.util
import numpy as np
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; Q = W/'review'
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001; NAME = 'AI Homework SFC R2'
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
master = Q/f'{NAME} - complete Short.mp4'; sha = hashlib.sha256(master.read_bytes()).hexdigest()
O = W/'graphic-evidence'; O.mkdir(exist_ok=True)
# graphics: reuse finish.py's draw() without rendering the film
src = (W/'recipe/finish.py').read_text().split('# Composite:')[0]
G = {'__file__': str(W/'recipe/finish.py')}; exec(compile(src, 'finish_head', 'exec'), G)
black = np.zeros((1920, 1080, 3), np.uint8); white = np.full_like(black, 255); gmani = []
for g in G['graphics']:
    out = O/f"{g['id']}.mov"; n0, n1 = round(g['t0']*FPS), round(g['t1']*FPS)
    if not out.exists():
        p = subprocess.Popen([F, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', '1080x1920', '-framerate', '30000/1001', '-i', '-', '-an', '-c:v', 'qtrle', '-pix_fmt', 'argb', str(out)], stdin=subprocess.PIPE)
        for n in range(n0, n1):
            t = n/FPS; lo = G['draw'](black, g, t).astype(np.float32); hi = G['draw'](white, g, t).astype(np.float32)
            al = np.clip(1 - np.mean(hi - lo, axis=2)/255, 0, 1); rgb = np.clip(lo/np.maximum(al[:, :, None], 1e-9), 0, 255)
            p.stdin.write(np.concatenate([rgb, (al*255)[:, :, None]], axis=2).astype(np.uint8).tobytes())
        p.stdin.close(); assert p.wait() == 0
    gmani.append(dict(name=g['id'], beat=[g['t0'], g['t1']], mov=str(out)))
# delivered ASR (fresh, on this exact file)
asr = W/'finished-asr.json'
if not asr.exists() or json.load(open(asr)).get('video_sha256') != sha:
    import whisper
    # Delivered audio in three windows split at the two edit joins (both sit in pauses). A single whole-file pass
    # hallucinated the last two sentences on this cut ('You'll be more likely to use AI...') although a window
    # transcription of the same delivered audio reads them correctly.
    m = whisper.load_model('medium.en'); edl0 = json.load(open(W/'edl.json')); cuts = [0] + [p['film0'] for p in edl0['pieces'][1:]] + [edl0['total_frames']/FPS]
    ws = []; texts = []
    for a_, b_ in zip(cuts, cuts[1:]):
        wav = W/'audio'/f'delivered_{a_:.2f}.wav'
        subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', f'{a_:.4f}', '-i', str(master), '-t', f'{b_ - a_:.4f}', '-ac', '1', '-ar', '16000', str(wav)], check=True)
        r = m.transcribe(str(wav), language='en', fp16=False, word_timestamps=True); texts.append(r['text'].strip())
        ws += [dict(w=x['word'].strip(), t=round(x['start'] + a_, 3), e=round(x['end'] + a_, 3)) for s_ in r['segments'] for x in s_['words']]
    asr.write_text(json.dumps(dict(video_sha256=sha, model='medium.en', method='delivered audio, three windows split at the edit joins', text=' '.join(texts), words=ws), indent=1))
A = json.load(open(asr)); shots = json.load(open(W/'shots.json')); fr = {r['id']: r for r in json.load(open(W/'framing-report.json'))}
edl = json.load(open(W/'edl.json')); words = json.load(open(W/'words_out.json'))
old = json.load(open('/Volumes/Extreme/_edit_work/ds28/round5/gate-plan.json'))
plan = dict(
    target_seconds=edl['total_frames']/FPS, target_frames=edl['total_frames'],
    joins=[s['a'] for s in shots[1:]], audio_joins=[p['film0'] for p in edl['pieces'][1:]],
    punch=[[s['a'], s['b'], s['id']] for s in shots], punch_covered=[s['kind'] != 'talk' for s in shots],
    covered=[[s['a'], s['b']] for s in shots if s['kind'] != 'talk'],
    source_picture=str(W/'base.mp4'), source_audio=str(W/'untreated.wav'),
    captions_ass=str(W/'captions.ass'), srt=str(Q/f'{NAME}.srt'),
    words=[dict(w=x['w'], t=x['t0'], e=x['t1']) for x in words], graphics=gmani,
    ai_inserts=[dict(name=s['f'].replace('.mp4', ''), beat=[s['a'], s['b']], chip=str(Q/'ai-label.png'), pos=list(json.load(open(W/'ai-chip.json'))['pos'])) for s in shots if s.get('ai')],
    real_photos=[], cards=[],
    label_chips=old['label_chips'], label_pos=old['label_pos'],
    watch_log=str(W/'qa/watch_pass.json'), evidence_contract=dict(version=2, video_sha256=sha),
    transcript_words=[dict(w=x['w']) for x in A['words']], speech_words=A['words'],
    speech_words_evidence=dict(method='delivered_asr', video_sha256=sha),
    banned_source=old['banned_source'], banned_times=old['banned_times'],
    talking_head_windows=[dict(name=s['id'], beat=[s['a'], s['b']], rect=[0, 0, 1080, 1920],
                               motion='tracking' if fr[s['id']]['stats'].get('travel_px', 0) > 0 else 'fixed-wide') for s in shots if s['kind'] == 'talk'],
)
neg = W/'negative-events.json'
if neg.exists():
    n = json.load(open(neg))
    if n.get('sha256') == sha: plan['negative_events_scan'] = n
(W/'gate-plan.json').write_text(json.dumps(plan, indent=1))
print('GATE PLAN', sha, len(plan['joins']), 'joins', A['text'][:120])
