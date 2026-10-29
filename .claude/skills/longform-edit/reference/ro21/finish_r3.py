"""RO-21 round 3 finish (adapted from RO-28's finish.py): SRT sidecar from Whisper on the DELIVERED audio (proofread fixes),
label-chip references located on the delivered frames, and plan.json for the delivery gate.
usage: finish_r3.py MASTER.mp4   (needs MASTER's merged build.json and final.whisper.json next to it)"""
import sys, os, json, re, subprocess, hashlib
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/greenscreen-bg'); import gsbg as G
B = '/Volumes/Expansion/_edit_work/RO-21'; R1 = f'{B}/round1'; R3 = f'{B}/round3'; FPS = 30000 / 1001
FF = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'
master = os.path.abspath(sys.argv[1]); od = os.path.dirname(master); NAME = 'RO21'
BJ = json.load(open(master + '.build.json')); total_f = BJ['frames']; total = total_f / FPS
fr = lambda t: int(round(t * FPS)); tt = lambda f: round(f / FPS, 3)
P = json.load(open(f'{R3}/plan_r3.json')); M = json.load(open(f'{R3}/film_manifest_cut.json'))   # after the recap false-start cut (cut_r3.py)
E = json.load(open(f'{R3}/edl_r3.json')); W = json.load(open(f'{R3}/film_words_r3.json')); CUT = json.load(open(f'{R3}/cut_r3.json'))

# ---------------------------------------------------------------- SRT from the delivered audio's own words
wh = json.load(open(f'{od}/final.whisper.json'))
mw = [dict(w=x['word'].strip(), t0=x['start'], t1=x['end']) for s in wh['segments'] for x in s.get('words', []) if x['word'].strip()]
# Whisper sometimes skips a stretch it hears (RO-21 R3: 139.3-143.0, "guys stay fat. Your action step is to cut every liquid
# calorie.", measured at speech level in the delivered audio): fill any whisper gap over 0.8 s from the film's own word timings.
_m = []
for x in mw:
    if _m and x['w'].startswith('-') and len(x['w']) > 1: _m[-1] = dict(_m[-1], w=_m[-1]['w'] + x['w'], t1=x['t1']); continue
    _p = re.sub(r'[^a-z]', '', _m[-1]['w'].lower()) if _m else ''
    if _p and len(_p) > 3 and re.sub(r'[^a-z]', '', x['w'].lower()).startswith(_p) and x['t0'] - _m[-1]['t1'] < 0.6:   # "workout. workouts": one word
        _m[-1] = dict(x, t0=_m[-1]['t0']); continue
    _m.append(x)
mw = _m
raw_mw = list(mw)
import difflib
_n = lambda w: re.sub(r"[^a-z0-9]", '', w.lower())
sm = difflib.SequenceMatcher(None, [_n(x['w']) for x in mw], [_n(w['w']) for w in W], autojunk=False)
filled = []
for op, i1, i2, j1, j2 in sm.get_opcodes():          # a run of intended words whisper did not write, at least 3 long
    run = ''.join(_n(w['w']) for w in W[j1:j2])
    if op == 'replace' and _n(''.join(x['w'] for x in mw[i1:i2])) == run: continue      # "2pm" vs "2 p .m.": same words
    if op in ('insert', 'replace') and (j2 - j1) >= 3 and (i2 - i1) <= 1:
        filled += [dict(w=w['w'], t0=w['t0'], t1=w['t1']) for w in W[j1:j2]]
        if i2 - i1 == 1: mw[i1]['t1'] = min(mw[i1]['t1'], W[j1]['t0'] - 0.02)
for x in mw: x['t1'] = min(x['t1'], x['t0'] + 1.5)
mw += filled
mw.sort(key=lambda x: x['t0']); print('srt words filled from the film timings:', ' '.join(f['w'] for f in filled))
FIX = [(r'(\d) %', r'\1%'), (r'(\d) \.(\d)', r'\1.\2'), (r'\bsix pack abs\.com\b', 'SixPackAbs.com'), (r'\babsbyai ?\.com\b', 'AbsByAI.com'),
       (r'\bApps by AI\b', 'Abs By AI'), (r'\bapps by AI\b', 'Abs By AI')]
FIX += json.load(open(f'{R3}/srt_fixes.json')) if os.path.exists(f'{R3}/srt_fixes.json') else []
def fix(s):
    for a, b in FIX: s = re.sub(a, b, s)
    return s
cues, cur = [], []
def flush():
    global cur
    if cur: cues.append([cur[0]['t0'], cur[-1]['t1'], fix(' '.join(w['w'] for w in cur))]); cur = []
for w in mw:
    if cur:
        gap = w['t0'] - cur[-1]['t1']; txt = ' '.join(x['w'] for x in cur + [w])
        if gap >= 0.45 or len(txt) > 84 or w['t1'] - cur[0]['t0'] > 5.5: flush()
    cur.append(w)
    if w['w'][-1:] in '.?!' and (cur[-1]['t1'] - cur[0]['t0']) > 1.2: flush()
flush()
def wrap(s):
    if len(s) <= 45: return s
    ws = s.split(); best = None
    for k in range(1, len(ws)):
        a, b = ' '.join(ws[:k]), ' '.join(ws[k:]); m = max(len(a), len(b))
        if best is None or m < best[0]: best = (m, a + '\n' + b)
    return best[1]
def ts(t):
    t = max(0, t); ms = int(round((t - int(t)) * 1000)); ms = min(ms, 999)
    return f'{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{ms:03d}'
out = []
if cues and cues[-1][2][-1:] not in '.?!': cues[-1][2] += '.'
for i, (a, b, s) in enumerate(cues):
    b = max(b, a + 0.9)
    if i + 1 < len(cues): b = min(b, cues[i + 1][0] - 0.02)
    b = min(b, total - 0.05)
    out.append(f'{i + 1}\n{ts(a)} --> {ts(b)}\n{wrap(s)}\n')
srt = f'{od}/{NAME}.srt'; open(srt, 'w').write('\n'.join(out))

# ---------------------------------------------------------------- picture timeline
opaque = sorted([m for m in M if m['kind'] == 'opaque'], key=lambda m: m['a'])
covered = [[tt(fr(m['a'])), tt(fr(m['b']))] for m in opaque]
cards = [[tt(fr(m['a'])), tt(fr(m['b']))] for m in opaque if m['template'] != 'local:broll']
graphics = [dict(name=m['id'], beat=[tt(fr(m['a'])), tt(fr(m['b']))], mov=m['mov']) for m in M if m['template'] != 'local:broll']
runs = BJ['runs']
pieces = []
for r in runs:
    if r['kind'] == 'presenter': lab = f"{r['piece']}-{r['framing']}-{r['bg']}"; cov = False
    else:
        it = next((m for m in opaque if fr(m['a']) <= r['o0'] < fr(m['b']) + 1), None); lab = f"insert-{it['id'] if it else 'covered'}"; cov = True
    if pieces and pieces[-1]['lab'] == lab and pieces[-1]['b'] == r['o0']: pieces[-1]['b'] = r['o1']; continue
    pieces.append(dict(a=r['o0'], b=r['o1'], lab=lab, cov=cov, rect=r.get('rect')))
joins = sorted(set(tt(p['a']) for p in pieces[1:]))
punch = [[tt(p['a']), tt(p['b']), p['lab']] for p in pieces]; punch_cov = [p['cov'] for p in pieces]
audio_joins = sorted([round(e['film_in'], 3) for e in E[1:]] + [CUT['audio_cut'][0]])
thw = [dict(beat=[tt(p['a']), tt(p['b'])], rect=[max(0, p['rect'][0]), max(0, p['rect'][1]), min(1920, p['rect'][2]), min(1080, p['rect'][3])], name=p['lab'])
       for p in pieces if not p['cov'] and p['b'] - p['a'] >= 15 and p.get('rect')]

# ---------------------------------------------------------------- AI labels: the renderer's chip, located on the delivered frame
def grab(t):
    raw = subprocess.run([FF, '-v', 'error', '-ss', f'{t:.3f}', '-i', master, '-frames:v', '1', '-vf', 'scale=in_color_matrix=bt709:in_range=tv,format=gray',
                          '-f', 'rawvideo', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1080, 1920).astype(np.float32)
os.makedirs(f'{od}/chips', exist_ok=True)
im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); G.SB.disclosure(im, 'AI-GENERATED', xy=(56, 48))
bb = im.getbbox(); chip = im.crop(bb); chip.save(f'{od}/chips/ai.png')
def mov_crop(mov, t, box, path):          # a chip exactly as its own graphic's renderer drew it (cards and ladders use HF chips)
    raw = subprocess.run([FF, '-v', 'error', '-ss', f'{t}', '-i', mov, '-frames:v', '1', '-vf', 'format=rgb24', '-f', 'rawvideo', '-'], capture_output=True).stdout
    x0, y0, x1, y1 = box; Image.fromarray(np.frombuffer(raw, np.uint8).reshape(1080, 1920, 3)[y0:y1, x0:x1]).save(path); return path
REFS = {'broll': f'{od}/chips/ai.png',
        'fact': mov_crop(f'{R1}/hf/tpl/renders/F35.mov', 3.0, (326, 982, 724, 1045), f'{od}/chips/ai_card.png'),
        'real': mov_crop(f'{R1}/hf/tpl/renders/R08.mov', 3.0, (328, 970, 1212, 1046), f'{od}/chips/real_card.png'),
        'ladder': mov_crop(f'{R1}/hf/ladder/G01.mov', 5.0, (1627, 209, 1836, 242), f'{od}/chips/ai_ladder.png')}
def locate(t, png):
    im = Image.open(png).convert('RGBA'); ref = np.asarray(Image.alpha_composite(Image.new('RGBA', im.size, (80, 80, 80, 255)), im).convert('L'), np.float32)
    res = cv2.matchTemplate(grab(t), ref, cv2.TM_CCOEFF_NORMED); _, mx, _, loc = cv2.minMaxLoc(res); return [int(loc[0]), int(loc[1])], round(float(mx), 3)
ai_ins = []
for p in P:
    is_ai = p.get('label') == 'AI-GENERATED' or p['kind'] == 'ladder' or p['id'] in ('B01', 'B10')
    if not is_ai: continue
    a, z = tt(fr(p['a'])), tt(fr(p['b'])); png = REFS[p['kind']]; pos, sc = locate((a + z) / 2, png)
    ai_ins.append(dict(name=p['id'], beat=[a, z], chip=png, pos=pos, match=sc))

real = []
for p in P:
    if p['id'] == 'R08':                          # the one real photo ("Real photo of me, not AI-generated"), Dan's me-today card
        a, z = tt(fr(p['a'])), tt(fr(p['b'])); pos, sc = locate((a + z) / 2, REFS['real'])
        real.append(dict(name='R08', beat=[a, z], chip=REFS['real'], pos=pos, match=sc))
_hair = [x[1] for x in BJ['hair'] if x[1] is not None]
DECLARE = {
 'framing:hair_top': f"green-screen composite: the face detector also finds the faces in the AI pictures behind Dan and fails its own agreement test (49% valid). The assembler measured hair clearance on every one of {len(_hair)} presenter frames: min {min(_hair)} px, median {int(np.median(_hair))}, 0 under 20 (build.json 'hair'); the watch judges found no hair at the edge.",
 'framing:headroom': "same detector failure on the composite; the presenter framing is the locked green-screen template's (greenscreen-bg, Dan 2026-10-27) and Dan approved it in round 1; assembler hair clearance as in framing:hair_top.",
 'framing:no_wide_level': "same detector failure on the composite; the template's wide/tight levels were approved by Dan in round 1 and the watch judge measured the wide shots' head at about 31% of frame height.",
 'framing:push_coverage': "same detector failure on the composite; tight/wide alternation comes from the locked green-screen template (shots_r1.py: W/T alternate on cuts), approved by Dan in round 1.",
 'style:static_run': "6:42-7:32 is the recap picture row G11 that Dan approved in round 1: one full-screen HyperFrames scene whose highlight moves tile to tile and whose band line changes on each level; its motion is small next to a cut, which this row counts.",
 'cut:splice_visibility': "the four joins over the ceiling (0:33.1, 1:35.2, 1:45.2, 6:27.9) are deliberate background changes on the cut by the locked green-screen template (Dan 2026-10-27: the background changes on cuts); the watch judges passed each boundary strip.",
 'captions:burned': "no captions are burned (organic long-form, .srt sidecar only); the detector reads the lower thirds, side cards and level cards as caption text, as on the approved RO-28.",
 'captions:card_collision': "organic sidecar subtitles: Dan speaks over the full-screen level cards by design (the card shows what he says); on YouTube the viewer's own CC sits over them, as on the approved RO-28.",
}
h = hashlib.sha256()
with open(master, 'rb') as f:
    for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
plan = dict(target_seconds=round(total, 3), target_frames=total_f, ai_inserts=ai_ins, real_photos=real, label_chips=dict(ai=f'{od}/chips/ai.png', real=REFS['real']), declare=DECLARE,
            joins=joins, audio_joins=audio_joins, covered=covered, punch=punch, punch_covered=punch_cov, graphics=graphics, cards=sorted(cards),
            words=[dict(w=w['w'], t=w['t0'], e=w['t1']) for w in W], transcript_words=[dict(w=w['w']) for w in raw_mw], srt=srt,
            source_audio=f'{B}/audio/film/film_voice_raw_r3.wav',
            banned_source='/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4',
            banned_times=[12.0, 18.0, 288.0], watch_log=f'{od}/logs/watch_pass.json', talking_head_windows=thw,
            evidence_contract=dict(version=2, video_sha256=h.hexdigest()))
ne = f'{od}/negative_events_scan.json'
if os.path.exists(ne): plan['negative_events_scan'] = json.load(open(ne))
json.dump(plan, open(f'{od}/plan.json', 'w'), indent=0)
print('cues', len(out), 'joins', len(joins), 'pieces', len(pieces), 'graphics', len(graphics), 'thw', len(thw))
print('labels:', [(x['name'], x['pos'], x['match']) for x in ai_ins + real])
