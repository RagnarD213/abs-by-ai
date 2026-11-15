"""DS-107 R1 gate plan (from DS-41 R1): delivered-audio ASR on this exact file (windows split at every take join), graphics = the
HyperFrames renders, joins/covered from shots.json, the title band and the study card's plot as caption obstacles, AI inserts and
real photos with the exact chips the assembly drew, talking-head windows, junk report, watch log.
The study card (K1) is laid out with a caption zone under its plot (the line-graph template keeps the plot above the caption line),
so it is declared as graphic regions the captions must clear, not as a caption-free card."""
from pathlib import Path
import subprocess, json, hashlib, os, sys
import numpy as np
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); RW = Path(__file__).resolve().parents[1]
W = RW/'main'; Q = W/'review'
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001; NAME = 'Metabolism Not The Reason SFC R1'
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image
master = Q/f'{NAME}.mp4'; sha = hashlib.sha256(master.read_bytes()).hexdigest()
shots = json.load(open(W/'shots.json')); edl = json.load(open(W/'edl.json')); words = json.load(open(W/'words_out.json'))
man = json.load(open(W/'graphics-manifest.json'))
asr = W/'finished-asr.json'
cuts = sorted(set([0.0] + [p['film0'] for p in edl['pieces']] + [edl['total_frames']/FPS]))
if not asr.exists() or json.load(open(asr)).get('video_sha256') != sha:
    import whisper
    m = whisper.load_model('medium.en'); ws = []; texts = []
    for a_, b_ in zip(cuts, cuts[1:]):
        if b_ - a_ < 0.6: continue
        wav = W/'audio'/f'delivered_{a_:.2f}.wav'
        subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', f'{a_:.4f}', '-i', str(master), '-t', f'{b_ - a_:.4f}', '-ac', '1', '-ar', '16000', str(wav)], check=True)
        r = m.transcribe(str(wav), language='en', fp16=False, word_timestamps=True, temperature=0); texts.append(r['text'].strip())
        ws += [dict(w=x['word'].strip(), t=round(x['start'] + a_, 3), e=round(x['end'] + a_, 3)) for s_ in r['segments'] for x in s_['words']]
    asr.write_text(json.dumps(dict(video_sha256=sha, model='medium.en', method='delivered audio, windows split at every take join', text=' '.join(texts), words=ws), indent=1))
A = json.load(open(asr))
fr = {r['id']: r for r in json.load(open(W/'framing-report.json'))}
# the chips exactly as the assembly drew them (assemble.chip), cropped to their boxes
os.environ.setdefault('LOOK', 'r5warm'); sys.argv = [sys.argv[0]]
import assemble as AS
def chip_png(key, out):
    col, al, box = AS.get_chip(key)
    rgba = np.dstack([(col*255).astype(np.uint8), (al*255).astype(np.uint8)])[box[1]:box[3], box[0]:box[2]]
    Image.fromarray(rgba).save(out); return [box[0], box[1]]
ai_pos = {}; real_pos = {}
for s in shots:
    if s.get('ai'): ai_pos[s['clip']] = chip_png(s['clip'], W/f"chip_{s['clip']}.png")
    if s['kind'] == 'still': real_pos[s['photo']] = chip_png(s['photo'], W/f"chip_{s['photo']}.png")
talk = [s for s in shots if s['kind'] == 'talk']
K1 = next(m for m in man if m['id'] == 'K1')
plan = dict(
    scope='CONTENT SFC R1 (DS-107 "Your Metabolism Is Not The Reason You\'re Fat"). Dan keyed (house key) on the moving Soft Blue field under the Soft Blue shorts title band, zoom cuts, a full-screen study line-graph card with a caption zone, library cutaways (AI A0063, A0242, A0072, A0182 with chips; stock B0559, B0042; real B0448), two real photos with the real-photo chip, lower thirds.',
    target_seconds=edl['total_frames']/FPS, target_frames=edl['total_frames'],
    joins=sorted(set(s['a'] for s in shots[1:])), audio_joins=sorted(set(p['film0'] for p in edl['pieces'][1:])),
    punch=[[s['a'], s['b'], s['id'] + '-' + s.get('size', s['kind'])] for s in shots], punch_covered=[s['kind'] != 'talk' for s in shots],
    covered=[[s['a'], s['b']] for s in shots if s['kind'] != 'talk'],
    source_picture=str(W/'base.mp4'), source_audio=str(W/'mix-untreated.wav'),
    captions_ass=str(W/'captions.ass'), srt=str(Q/f'{NAME}.srt'),
    words=[dict(w=x['w'], t=x['t0'], e=x['t1']) for x in words],
    graphics=[dict(name=m['id'], beat=[m['a'], m['b']], mov=m['mov']) for m in man],
    graphic_regions=[dict(name=m['id'], beat=[m['a'], m['b']], rect=[m['box'][0], m['box'][1], m['box'][2] - m['box'][0], m['box'][3] - m['box'][1]]) for m in man if 'box' in m]
                    + [dict(name='title_band', beat=[0.0, edl['total_frames']/FPS], rect=[0, 0, 1080, 310]),
                       dict(name='K1-plot', beat=[K1['a'], K1['b']], rect=[0, 310, 1080, 1390 - 310])],
    ai_inserts=[dict(name=s['id'] + '-' + s['clip'], beat=[s['a'], s['b']], chip=str(W/f"chip_{s['clip']}.png"), pos=ai_pos[s['clip']]) for s in shots if s.get('ai')],
    real_photos=[dict(name=s['id'] + '-' + s['photo'], beat=[s['a'], s['b']], chip=str(W/f"chip_{s['photo']}.png"), pos=real_pos[s['photo']]) for s in shots if s['kind'] == 'still'],
    cards=[],
    label_chips=dict(ai=str(W/'chip_A0063.png'), real=str(W/'chip_before.png')), label_pos=dict(ai=ai_pos.get('A0063'), real=real_pos.get('before')),
    watch_log=str(W/'qa/watch_pass.json'), evidence_contract=dict(version=2, video_sha256=sha),
    transcript_words=[dict(w=x['w']) for x in A['words']], speech_words=A['words'],
    speech_words_evidence=dict(method='delivered_asr', video_sha256=sha),
    banned_source='/Volumes/Expansion/_edit_work/DS-41/r1/src/app-flow-generate-future-self.mp4', banned_times=[26.5, 27.5, 29.5, 31.0],
    talking_head_windows=[dict(name=s['id'], beat=[s['a'], s['b']], rect=[0, 310, 1080, 1610],
                               motion='tracking' if fr[s['id']].get('travel_px', 0) > 0 else 'fixed-wide') for s in talk],
    junk_report=str(W/'prerender-junk.json'),
)
neg = W/'negative-events.json'
if neg.exists():
    n = json.load(open(neg))
    if n.get('sha256') == sha: plan['negative_events_scan'] = n
(W/'gate-plan.json').write_text(json.dumps(plan, indent=1))
print('GATE PLAN', sha, len(plan['joins']), 'joins |', A['text'][:200])
