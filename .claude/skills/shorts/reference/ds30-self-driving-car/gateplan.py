"""DS-30 R1 gate evidence for the delivered master: delivered-audio ASR in windows split at the edit joins (DS-31 lesson),
and gate-plan.json in the DS-28/DS-31 schema. Graphics are the HyperFrames renders (lower thirds: their own alpha; the opaque
cost card: its transparent evidence twin K1e, same template/timing, field left out)."""
from pathlib import Path
import subprocess, json, hashlib, os, sys
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; Q = W/'review'
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001; NAME = sys.argv[1] if len(sys.argv) > 1 else 'Self-Driving Car SFC R1'
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
master = Q/f'{NAME} - complete Short.mp4'; sha = hashlib.sha256(master.read_bytes()).hexdigest()
man = json.load(open(W/'graphics-manifest.json'))
gmani = [dict(name=m['id'], beat=[m['a'], m['b']], mov=m.get('evidence_mov', m['mov'])) for m in man]
asr = W/'finished-asr.json'
if not asr.exists() or json.load(open(asr)).get('video_sha256') != sha:
    import whisper
    m = whisper.load_model('medium.en'); edl0 = json.load(open(W/'edl.json')); cuts = [0] + [p['film0'] for p in edl0['pieces'][1:]] + [edl0['total_frames']/FPS]
    ws = []; texts = []
    for a_, b_ in zip(cuts, cuts[1:]):
        wav = W/'audio'/f'delivered_{a_:.2f}.wav'
        subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', f'{a_:.4f}', '-i', str(master), '-t', f'{b_ - a_:.4f}', '-ac', '1', '-ar', '16000', str(wav)], check=True)
        r = m.transcribe(str(wav), language='en', fp16=False, word_timestamps=True, condition_on_previous_text=False,
                         initial_prompt='Tesla, Model 3, Camry, Kelley Blue Book, robotaxis, Austin.'); texts.append(r['text'].strip())
        ws += [dict(w=x['word'].strip(), t=round(x['start'] + a_, 3), e=round(x['end'] + a_, 3)) for s_ in r['segments'] for x in s_['words']]
    asr.write_text(json.dumps(dict(video_sha256=sha, model='medium.en', method='delivered audio, four windows split at the edit joins', text=' '.join(texts), words=ws), indent=1))
A = json.load(open(asr)); shots = json.load(open(W/'shots.json')); fr = {r['id']: r for r in json.load(open(W/'framing-report.json'))}
edl = json.load(open(W/'edl.json')); words = json.load(open(W/'words_out.json'))
old = json.load(open('/Volumes/Extreme/_edit_work/ds31/round2/gate-plan.json'))
plan = dict(
    target_seconds=edl['total_frames']/FPS, target_frames=edl['total_frames'],
    joins=[s['a'] for s in shots[1:]], audio_joins=[p['film0'] for p in edl['pieces'][1:]],
    punch=[[s['a'], s['b'], s['id']] for s in shots], punch_covered=[s['kind'] != 'talk' for s in shots],
    covered=[[s['a'], s['b']] for s in shots if s['kind'] != 'talk'],
    source_picture=str(W/'base.mp4'), source_audio=str(W/'untreated.wav'),
    captions_ass=str(W/'captions.ass'), srt=str(Q/f'{NAME}.srt'),
    words=[dict(w=x['w'], t=x['t0'], e=x['t1']) for x in words], graphics=gmani,
    ai_inserts=[], real_photos=[], cards=[],
    label_chips=old['label_chips'], label_pos=old['label_pos'],
    watch_log=str(W/'qa/watch_pass.json'), evidence_contract=dict(version=2, video_sha256=sha),
    transcript_words=[dict(w=x['w']) for x in A['words']], speech_words=A['words'],
    speech_words_evidence=dict(method='delivered_asr', video_sha256=sha),
    # banned-screen reference recovered per deliver/README (2026-11-11, DS-38): library recording, sha256 73d6b0f3..., corpus times
    banned_source=str(W/'ref'/'banned-screen-app-flow-generate-future-self.mp4'), banned_times=[26.5, 27.5, 29.5, 31.0],
    # windows labelled by size (tight = the tracked punch-in, even when it never had to move; wide = the camera's
    # original frame, fixed), each kept 2 frames inside its shot so no sample lands on the neighbouring shot's frame
    talking_head_windows=[dict(name=s['id'], beat=[(s['n0'] + 2)/FPS, (s['n1'] - 2)/FPS], rect=[0, 0, 1080, 1920],
                               motion='tracking' if s['size'] == 'tight' else 'fixed-wide') for s in shots if s['kind'] == 'talk'],
)
neg = W/'negative-events.json'
if neg.exists():
    n = json.load(open(neg))
    if n.get('sha256') == sha: plan['negative_events_scan'] = n
(W/'gate-plan.json').write_text(json.dumps(plan, indent=1))
print('GATE PLAN', sha, len(plan['joins']), 'joins', A['text'])
