"""DS-76 R1 exact-file checks, staged: voice | picture | watch | gate.  python3 check.py voice picture watch
voice: delivered ASR + audio gate (reference) + verbatim preservation against the selected Natural Warmth mix.
picture: libass caption states, hair top on EVERY presenter frame (>=20 px; and clear of the 90 px header), insert sheets.
watch: gate plan + shared watch.py.  gate: shared delivery gate (needs evidence/independent/negative-events-scan.json)."""
from pathlib import Path
import os, sys, json, subprocess, hashlib, shutil, numpy as np, cv2
from PIL import Image, ImageDraw
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; F = R/'Media/video_edit/bin/ffmpeg'
os.environ['PATH'] = str(F.parent)+':'+os.environ['PATH']; sys.path.insert(0, str(R/'.claude/skills/_shared/renderq')); import renderq
stages = sys.argv[1:] or ['voice', 'picture', 'watch']
renderq.hold_until_exit('DS-76 R1 checks '+'+'.join(stages), pool='light', group='DS-76')
sys.path.insert(0, str(R/'.claude/skills/_shared')); from cut import speech as S; from audio import common as A
m = json.load(open(W/'records/assembly.json')); v = Path(m['master']); sha = hashlib.sha256(v.read_bytes()).hexdigest(); fps = 30000/1001; fr = lambda t: round(t*fps)
P = json.load(open(W/'edit-plan.json')); EV = W/'evidence'; scratch = Path('/tmp/absbyai-scratch/DS-76/check'); scratch.mkdir(parents=True, exist_ok=True)
def ff(a): subprocess.run([str(F), '-nostdin', '-v', 'error', '-y']+list(map(str, a)), check=True)
assets = m['assets']; gfx = m['graphics']
covered = [[u['fa']/fps, u['fb']/fps] for u in assets]+[[g['a'], g['b']] for g in gfx if g['kind'] == 'opaque']
hidden = [(fr(a), fr(b)) for a, b in covered]; talk = []; st = None
for i in range(m['frames']+1):
    show = i < m['frames'] and not any(a <= i < b for a, b in hidden)
    if show and st is None: st = i
    if not show and st is not None: talk.append([st/fps, i/fps]); st = None
ajoins = [p['out'] for p in P['pieces'][1:]]
for a in ajoins: assert any(x <= a <= y for x, y in covered), ('audio join on Dan uncovered', a)

if 'voice' in stages:
    ws, src = S.transcribe(str(v), model='small'); (W/'records/delivered-asr.json').write_text(json.dumps(dict(video_sha256=sha, source=src, words=ws), indent=2)); print('ASR_DONE', len(ws), flush=True)
    ss, d = A.analysis_window(str(v)); A.stash_untreated(str(v), A.pcm(str(W/'audio/cut-raw.wav'), ss=ss, dur=d, ac=1), 'Exact untreated cut samples (lav ch0); Natural Warmth A chain.')
    with (EV/'audio-gate.log').open('w') as log: r = subprocess.run([sys.executable, str(R/'.claude/skills/_shared/audio/audio_gate.py'), str(v), '--ab', str(EV/'voice-A-B.wav')], stdout=log, stderr=subprocess.STDOUT)
    print('AUDIO_GATE', r.returncode, flush=True); shutil.copy2(str(v)+'.audio_gate.json', EV/'reference-audio-gate.json')

if 'picture' in stages:
    cu = json.load(open(W/'records/caption-cues.json')); cd = scratch/'caps'; shutil.rmtree(cd, ignore_errors=True); cd.mkdir()
    ids = [fr((c['a']+c['b'])/2) for c in cu]; sel = '+'.join(f'eq(n\\,{i})' for i in ids)
    ff(['-f', 'lavfi', '-i', f'color=c=black@0.0:s=1080x1920:r=30000/1001:d={m["duration"]},format=rgba', '-vf', f'ass={W}/captions.ass:alpha=1,select={sel}', '-vsync', 0, cd/'cap-%03d.png'])
    pngs = sorted(cd.glob('cap-*.png')); assert len(pngs) == len(cu), (len(pngs), len(cu)); states = []; dest = EV/'caption-states'; dest.mkdir(exist_ok=True)
    for i, (c, p) in enumerate(zip(cu, pngs)):
        im = Image.open(p).convert('RGBA'); box = im.getchannel('A').getbbox(); assert box and box[2]-box[0] < 1080 and box[3]-box[1] < 150, (i, box, c['text'])
        out = dest/f'C{i:03d}.png'; im.crop(box).save(out)
        states.append(dict(name=f'C{i:03d}', beat=[c['a'], c['b']], image=str(out), image_sha256=hashlib.sha256(out.read_bytes()).hexdigest(), pos=[box[0], box[1]], word=c['text'].split()[0]))
    (W/'records/caption-states.json').write_text(json.dumps(states, indent=2)); print('CAPTIONS', len(states), flush=True)
    fd = scratch/'frames'; shutil.rmtree(fd, ignore_errors=True); fd.mkdir(); ff(['-i', v, '-vf', 'scale=540:960:in_color_matrix=bt709:in_range=tv', fd/'f-%04d.jpg'])
    paths = sorted(fd.glob('f-*.jpg')); assert len(paths) == m['frames'], (len(paths), m['frames'])
    keep = [(i, p) for i, p in enumerate(paths) if any(fr(a) <= i < fr(b) for a, b in talk)]; md = scratch/'masks'; md.mkdir(exist_ok=True)
    for j in range(0, len(keep), 150): subprocess.run([str(R/'.claude/skills/shorts/reference/recentre/personmask'), str(md)]+[str(p) for _, p in keep[j:j+150]], check=True, stdout=subprocess.PIPE)
    rows = []; bad = []
    for i, p in keep:
        mask = np.array(Image.open(md/(p.stem+'.mask.png')).convert('L')); n, lab, stt, _ = cv2.connectedComponentsWithStats((mask > 127).astype('uint8'), 8)
        if n < 2: bad.append((i, 'empty mask')); continue
        c = 1+int(np.argmax(stt[1:, cv2.CC_STAT_AREA])); ys = np.where((lab == c).sum(1) >= 10)[0]; top = int(ys[0])*2
        rows.append(dict(frame=i, t=round(i/fps, 3), hair_top_px=top))
        if top < 20 or top <= 90: bad.append((i, top))
    rep = dict(video_sha256=sha, presenter_frames=len(keep), measured=len(rows), minimum=min(r['hair_top_px'] for r in rows), header_bottom_px=90, failures=bad[:40], n_fail=len(bad))
    (EV/'hair.json').write_text(json.dumps(dict(rep, rows=rows), indent=2)); print('HAIR', json.dumps(rep), flush=True)
    worst = sorted(rows, key=lambda r: r['hair_top_px'])[:6]
    for r in worst: ff(['-ss', round(r['frame']/fps+0.5/fps, 4), '-i', v, '-frames:v', 1, '-vf', 'crop=1080:420:0:0', EV/f"hair-worst-{r['frame']:04d}.png"])
    nd = EV/'insert-sheets'; nd.mkdir(exist_ok=True)
    for u in assets:
        a, b = u['fa'], u['fb']; tiles = []
        for i in range(a, b, 3):
            im = Image.open(paths[i]).convert('RGB'); im.thumbnail((135, 240)); t = Image.new('RGB', (135, 258)); t.paste(im, (0, 18)); ImageDraw.Draw(t).text((3, 3), f"{u['id']} +{i-a}", fill='white'); tiles.append(t)
        sh = Image.new('RGB', (135*10, 258*((len(tiles)+9)//10)))
        for k, im in enumerate(tiles): sh.paste(im, ((k % 10)*135, (k//10)*258))
        sh.save(nd/f"{u['id']}.jpg")
    (EV/'picture-check-sha256.txt').write_text(sha); print('PICTURE_DONE', flush=True)

def plan():
    segs = sorted([[a, b, 'Original Portrait', False] for a, b in talk]+[[a, b, 'cutaway', True] for a, b in covered])
    d = json.load(open(W/'records/delivered-asr.json')); assert d['video_sha256'] == sha; ws = d['words']
    states = json.load(open(W/'records/caption-states.json')); L = json.load(open(W/'records/library.json'))
    joins = sorted(set([u['fa']/fps for u in assets]+[u['fb']/fps for u in assets]+[g['a'] for g in gfx]+[g['b'] for g in gfx]+ajoins)); joins = [t for t in joins if 0 < t < m['duration']-0.01]
    regions = [dict(name='Large title '+u['id'], beat=[u['fa']/fps, u['fb']/fps], rect=[0, 0, 1080, 350]) for u in assets]
    regions += [dict(name=g['id'], beat=[g['a'], g['b']], rect=[0, 90, 1080, 1500] if g['kind'] == 'opaque' else [g['box'][0], g['box'][1]-12, g['box'][2]-g['box'][0], g['box'][3]-g['box'][1]+24]) for g in gfx]
    return dict(target_seconds=m['duration'], target_frames=m['frames'], joins=joins, audio_joins=ajoins, covered=covered, punch=[x[:3] for x in segs], punch_covered=[x[3] for x in segs],
                graphics=[dict(name=g['id'], beat=[g['a'], g['b']], mov=g['mov']) for g in gfx], cards=[[g['a'], g['b']] for g in gfx if g['kind'] == 'opaque'],
                source_audio=str(W/'audio/voice-selected.wav'), srt=str(next((W/'review').glob('*.srt'))), captions_ass=str(W/'captions.ass'), watch_log=str(EV/'watch/full-watch.json'),
                source_map=[dict(source_id=u['lib'], source_file=L[u['lib']]['path'], source_in=u['start'], beat=[u['fa']/fps, u['fb']/fps], crop=u['crop']) for u in assets],
                words=[dict(w=x['w'], t=x['t0'], e=x['t1']) for x in json.load(open(W/'records/words.json'))], transcript_words=ws, evidence_contract=dict(version=2, video_sha256=sha),
                speech_words=ws, speech_words_evidence=dict(method='delivered_asr', video_sha256=sha, source=d['source']), caption_states=states, graphic_regions=regions,
                talking_head_windows=[dict(beat=t, rect=[0, 0, 1080, 1920], motion='fixed-wide') for t in talk], label_tracks=[], ai_inserts=[], real_photos=[],
                banned_source='/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4', banned_times=[26.5, 27.5, 29.5, 31.0])

if 'watch' in stages:
    assert (EV/'picture-check-sha256.txt').read_text() == sha, 'picture checks are for another render'
    (EV/'watch').mkdir(exist_ok=True); (W/'records/gate-plan.json').write_text(json.dumps(plan(), indent=2))
    r = subprocess.run([sys.executable, str(R/'.claude/skills/_shared/deliver/watch.py'), str(v), '--plan', str(W/'records/gate-plan.json'), '--out', str(EV/'watch/full'), '--log', str(EV/'watch/full-watch.json'), '--clips'])
    print('WATCH', r.returncode, flush=True)

if 'gate' in stages:
    p = W/'records/gate-plan.json'; pl = json.load(open(p)); assert pl['evidence_contract']['video_sha256'] == sha
    rec = json.load(open(EV/'independent/negative-events-scan.json')); assert rec['sha256'] == sha and rec['frames_checked'] >= 24; pl['negative_events_scan'] = rec; p.write_text(json.dumps(pl, indent=2))
    r = subprocess.run([sys.executable, str(R/'.claude/skills/_shared/deliver/gate.py'), str(v), '--format', 'short', '--plan', str(p), '--json', str(EV/'delivery-gate.json')]); print('GATE', r.returncode, flush=True)
