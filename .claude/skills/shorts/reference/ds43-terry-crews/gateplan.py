"""DS-43 R1 gate plan for ONE version (python3 gateplan.py scripted|offcuff), from DS-44B R2 (the DS-31 / DS-33 schema): delivered-audio ASR on this exact file, graphics = the HyperFrames renders,
joins/covered from shots.json + the clip's own edits, talking-head windows, the AI insert (A0197 with its chip), junk report,
watch log."""
from pathlib import Path
import subprocess, json, hashlib, os, sys
import numpy as np
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); RW = Path(__file__).resolve().parents[1]
VERSION = sys.argv[1]; W = RW/VERSION; Q = W/'review'
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001; NAME = {'scripted': 'Terry Crews Fasting SFC R1 - scripted', 'offcuff': 'Terry Crews Fasting SFC R1 - off the cuff'}[VERSION]
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
sys.path.insert(0, str(R/'.claude/skills/_shared')); import softblue as B
from PIL import Image
master = Q/f'{NAME}.mp4'; sha = hashlib.sha256(master.read_bytes()).hexdigest()
shots = json.load(open(W/'shots.json')); edl = json.load(open(W/'edl.json')); words = json.load(open(W/'words_out.json'))
man = json.load(open(W/'graphics-manifest.json'))
asr = W/'finished-asr.json'
cuts = sorted(set([0.0] + [s['film0'] for s in edl['clip']['segs']] + [p['film0'] for p in edl['pieces']] + [edl['total_frames']/FPS]))
if not asr.exists() or json.load(open(asr)).get('video_sha256') != sha:
    import whisper
    m = whisper.load_model('medium.en'); ws = []; texts = []
    for a_, b_ in zip(cuts, cuts[1:]):
        if b_ - a_ < 0.6: continue
        wav = W/'audio'/f'delivered_{a_:.2f}.wav'
        subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', f'{a_:.4f}', '-i', str(master), '-t', f'{b_ - a_:.4f}', '-ac', '1', '-ar', '16000', str(wav)], check=True)
        r = m.transcribe(str(wav), language='en', fp16=False, word_timestamps=True, temperature=0); texts.append(r['text'].strip())
        ws += [dict(w=x['word'].strip(), t=round(x['start'] + a_, 3), e=round(x['end'] + a_, 3)) for s_ in r['segments'] for x in s_['words']]
    asr.write_text(json.dumps(dict(video_sha256=sha, model='medium.en', method='delivered audio, windows split at every clip edit and every take join', text=' '.join(texts), words=ws), indent=1))
A = json.load(open(asr))
fr = {r['id']: r for r in json.load(open(W/'framing-report.json'))}
old = json.load(open('/Volumes/Extreme/_edit_work/ds31/round2/gate-plan.json'))
# the AI-GENERATED chip exactly as drawn (softblue.disclosure, u 1.6, size 23), cropped to its box
base = Image.new('RGB', (1080, 1920), (0, 0, 0)); wh = Image.new('RGB', (1080, 1920), (255, 255, 255))
B.disclosure(base, 'AI-GENERATED', (0, 0), 1.6, anchor='lt', size=23); B.disclosure(wh, 'AI-GENERATED', (0, 0), 1.6, anchor='lt', size=23)
x = np.asarray(base).astype(np.int32); y = np.asarray(wh).astype(np.int32); al = 255 - (y - x).max(2).clip(0, 255)
rgba = np.dstack([np.where(al[..., None] > 0, (x*255//np.maximum(al[..., None], 1)).clip(0, 255), 0), al]).astype(np.uint8)
ys, xs = np.where(al > 0); cb = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
Image.fromarray(rgba[cb[1]:cb[3], cb[0]:cb[2]]).save(W/'ai_chip.png')
cx, cy = 40, 120          # the AI-GENERATED chip on A0210 (assemble.CHIP_XY)
talk = [s for s in shots if s['kind'] == 'talk']
clip_joins = [s['film0'] for s in edl['clip']['segs'][1:]]
corner = shots[0]['corner']; CH_Y = int(fr['S0']['corner_hair_y'])
plan = dict(
    scope=f'CONTENT SFC R1 (DS-43 {VERSION}). The Terry Crews clip (Business Insider) first, full screen, Dan keyed small in the corner watching it; then the titled panel (Bill Maher Codex R5 reaction format) with Dan large watching, his response in front of the silent panel, then Soft Blue field with zoom cuts, cutaways (AI A0210 with its chip, stock B0317, the clip photo of Terry) and lower thirds. House key.',
    target_seconds=edl['total_frames']/FPS, target_frames=edl['total_frames'],
    joins=sorted(set(clip_joins + [s['a'] for s in shots[1:]])), audio_joins=sorted(set(clip_joins + [p['film0'] for p in edl['pieces']])),
    punch=[[s['a'], s['b'], s['id'] + ('-' + s.get('size', s['kind']))] for s in shots], punch_covered=[s['kind'] != 'talk' for s in shots],
    covered=[[s['a'], s['b']] for s in shots if s['kind'] != 'talk'],
    source_picture=str(W/'base.mp4'), source_audio=str(W/'mix-untreated.wav'),
    captions_ass=str(W/'captions.ass'), srt=str(Q/f'{NAME}.srt'),
    words=[dict(w=x['w'], t=x['t0'], e=x['t1']) for x in words],
    graphics=[dict(name=m['id'], beat=[m['a'], m['b']], mov=m['mov']) for m in man],
    graphic_regions=[dict(name=m['id'], beat=[m['a'], m['b']], rect=[m['box'][0], m['box'][1], m['box'][2] - m['box'][0], m['box'][3] - m['box'][1]]) for m in man if 'box' in m]
                    ,
    ai_inserts=[dict(name=s['id'] + '-' + s['clip'], beat=[s['a'], s['b']]) for s in shots if s.get('ai')], real_photos=[],
    cards=[],   # R5: the titled panel is a partial frame with captions over Dan (as DS-44B); its spans are in `covered`, no full-screen card
    label_chips=dict(ai=str(W/'ai_chip.png'), real=old['label_chips']['real']), label_pos=dict(ai=[cx + cb[0], cy + cb[1]], real=old['label_pos']['real']),
    watch_log=str(W/'qa/watch_pass.json'), evidence_contract=dict(version=2, video_sha256=sha),
    transcript_words=[dict(w=x['w']) for x in A['words']], speech_words=A['words'],
    speech_words_evidence=dict(method='delivered_asr', video_sha256=sha),
    banned_source=old['banned_source'], banned_times=old['banned_times'],
    # R2: the corner Dan is the full-height key at 0.40 (432 x 768, laptop kept): his window starts 60 px above his hair;
    # card shots: Dan's hair sits at y 540 under the interview frame, so his window starts at y 480 (the card above is background)
    talking_head_windows=[dict(name='S0-corner', beat=[shots[0]['a'], shots[0]['b']], rect=[0, CH_Y - 60, 432, 1920 - (CH_Y - 60)], motion='fixed-wide')]
                         + [dict(name=s['id'], beat=[s['a'], s['b']], rect=[0, int(fr[s['id']]['hair_y_min']) - 60, 1080, 1920 - (int(fr[s['id']]['hair_y_min']) - 60)], motion='fixed-wide')
                            for s in shots if s['kind'] in ('panelwatch', 'panelresp')]
                         + [dict(name=s['id'], beat=[s['a'], s['b']], rect=[0, 0, 1080, 1920],
                                 motion='tracking' if fr[s['id']]['travel_px'] > 0 else 'fixed-wide') for s in talk],
    junk_report=str(W/'prerender-junk.json'),
)
neg = W/'negative-events.json'
if neg.exists():
    n = json.load(open(neg))
    if n.get('sha256') == sha: plan['negative_events_scan'] = n
(W/'gate-plan.json').write_text(json.dumps(plan, indent=1))
print('GATE PLAN', sha, len(plan['joins']), 'joins |', A['text'][:200])
