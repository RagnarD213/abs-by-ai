"""RO-24 round 4: plan.json for the shared delivery gate (_shared/deliver/gate.py --format longform), built only from the
build's own records. Nothing is re-rendered and nothing is re-decided. Modelled on ro28/round2/recipe/finish.py.

  python3 gateplan_r4.py            (writes round4/final/plan.json; transcribes the delivered audio once, cached by sha256)

What this film is: a green-screen composite. Dan is a keyed plate placed on a moving background (bg_plan.json), so his
talking-head window is his PLACED screen rect per run (RO24_R4_MASTER.mp4.build.json), not the full frame. Runs of kind
`presenter-reused` were copied from the earlier render final/_build/picture_v1.mp4 (same film frames), so their framing,
placement and rect are read from picture_v1.mp4.build.json.

  joins         every visible picture boundary: run edges (reframe, placement, background change, item in/out) plus the
                cut inside B1 (real rollout -> AI salmon); an edge between two covered runs under ONE full-screen item is
                hidden and is not a join
  audio_joins   only where the voice itself was joined: round 2's cut joins (edl_r3.json, already mapped through
                round3/timemap.json -- cross-checked here) = a shot whose source frame does not continue the previous
                shot's, plus both edges of every interview-clip insert (the clip plays its own sound)
  talking_head_windows  per presenter run, the placed plate rect clipped to the frame, motion `tracking`
  ai_inserts    B2 (AI clip of Dan), the AI salmon half of B1, and every presenter run on a `set` background (the studio
                set is an AI image and carries the AI-GENERATED chip top left); chip positions located on the delivered frame
"""
import re, hashlib, json, os, subprocess, sys
import numpy as np
from PIL import Image

P = '/Users/danielrose/Projects/Claude/Projects/Abs By AI'
SK = f'{P}/.claude/skills'
sys.path.insert(0, f'{SK}/_shared'); sys.path.insert(0, f'{SK}/_shared/cut')
import softblue as B   # noqa: E402
import speech          # noqa: E402

R = '/Volumes/Expansion/_edit_work/RO-24'; R2, R3, R4 = f'{R}/round2', f'{R}/round3', f'{R}/round5'   # round 5: R4 names the round 5 folder
OD = f'{R4}/final'; MASTER = f'{OD}/RO24_R5_MASTER.mp4'
FF = f'{P}/Media/video_edit/bin/ffmpeg'
FPS = 30000 / 1001
W_, H_ = 1920, 1080


def sec(f): return round(f / FPS, 3)
def fr(t): return int(round(t * FPS))


BJ = json.load(open(MASTER + '.build.json')); N = BJ['frames']
V1 = {}                                                   # round 4 v3 is one full render: no reused runs
# Reused runs chain: this render reuses from picture_v4, whose own reused runs came from picture_v3 (one full render).
# Resolve each run by walking the chain newest -> oldest until a real `presenter` run with the same span and bg is found.
CHAIN = [json.load(open(f'{OD}/_build/{_p}.mp4.build.json'))['runs'] for _p in ('picture_v4', 'picture_v3')
         if os.path.exists(f'{OD}/_build/{_p}.mp4.build.json')]
if BJ.get('g1') and any(r['kind'] == 'presenter-reused' for r in BJ['runs']):
    _idx = [{(r['o0'], r['o1']): r for r in runs_} for runs_ in CHAIN]
    for r in BJ['runs']:
        if r['kind'] != 'presenter-reused':
            continue
        for ix in _idx:
            s = ix.get((r['o0'], r['o1']))
            assert s is not None and s.get('bg') == r.get('bg'), ('reused run not in chain', r)
            if s['kind'] == 'presenter':
                V1[(r['o0'], r['o1'])] = s; break
            assert s['kind'] == 'presenter-reused', s
        else:
            raise AssertionError(('reused run unresolved through v4 -> v3', r))
MAN = json.load(open(f'{R4}/film_manifest_r5.json'))
BGS = {s['id']: s for s in json.load(open(f'{R4}/bg_plan.json'))['segments']}
EDL = json.load(open(f'{R4}/edl_r5.json'))['items']   # round 3 cut, Tracy retimed (retime_r4.py)
TM = json.load(open(f'{R3}/timemap.json'))
assert EDL[-1]['o1'] == N, (EDL[-1]['o1'], N)

# ---------------------------------------------------------------- runs, resolved
runs = []
for r in BJ['runs']:
    r = dict(r)
    if r['kind'] == 'presenter-reused':
        src = V1[(r['o0'], r['o1'])]
        assert src['kind'] == 'presenter' and src.get('bg') == r.get('bg'), r
        r.update({k: src[k] for k in ('framing', 'placement', 'rect', 'bg_type', 'key', 'src0')})
    runs.append(r)
assert runs[0]['o0'] == 0 and runs[-1]['o1'] == N and all(a['o1'] == b['o0'] for a, b in zip(runs, runs[1:]))

OPAQUE = [m for m in MAN if m['kind'] == 'opaque']


def covering(r):
    """The full-screen manifest item a covered/insert run sits under."""
    if r['kind'] == 'insert':
        return 'C_' + r['clip']
    mid = (r['o0'] + r['o1']) / 2 / FPS
    hit = [m for m in OPAQUE if m['a'] - 0.05 <= mid <= m['b'] + 0.05]
    assert len(hit) == 1, (r, [m['id'] for m in hit])
    return hit[0]['id']


def clip_rect(rc):
    x, y, w, h = rc
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W_, x + w), min(H_, y + h)
    return [int(x0), int(y0), int(x1 - x0), int(y1 - y0)]


# visible pieces: one per presenter run; consecutive covered runs under one item merge (their edge is hidden)
pieces = []
for r in runs:
    if r['kind'] in ('covered', 'insert'):
        lab = 'insert-' + covering(r)
        if pieces and pieces[-1]['cov'] and pieces[-1]['lab'] == lab:
            pieces[-1]['b'] = r['o1']; continue
        pieces.append(dict(a=r['o0'], b=r['o1'], lab=lab, cov=True))
    else:
        pieces.append(dict(a=r['o0'], b=r['o1'], lab=f"{r['framing']}-{r['placement']}", cov=False, run=r))

B1 = next(m for m in MAN if m['id'] == 'B1')
B1_CUT = B1['a'] + 2.4024          # b1_rollout.mp4 is 2.4024 s; b1_salmon.mp4 follows (round2/recipe/broll24.py)
joins = sorted({sec(p['a']) for p in pieces[1:]} | {round(B1_CUT, 3)})
punch = [[sec(p['a']), sec(p['b']), p['lab']] for p in pieces]
punch_cov = [p['cov'] for p in pieces]
covered = [[sec(p['a']), sec(p['b'])] for p in pieces if p['cov']]
CARD_IDS = {m['id'] for m in OPAQUE if m['id'].startswith('P') or m['id'] in ('G06', 'G11', 'G13')}
cards = [[sec(p['a']), sec(p['b'])] for p in pieces if p['cov'] and p['lab'][7:] in CARD_IDS]
graphics = [dict(name=m['id'], beat=[sec(fr(m['a'])), sec(fr(m['b']))], mov=m['mov'], kind=m['kind'])
            for m in MAN if (m['id'].startswith('G') or m['id'].startswith('P')) and os.path.exists(m['mov'])]
assert len(graphics) == sum(1 for m in MAN if m['id'][0] in 'GP'), 'a graphic MOV is missing on disk'

# ---------------------------------------------------------------- audio joins: where the VOICE was joined
aj = set()
prev = None
for it in EDL:
    if it['kind'] == 'insert':
        aj |= {it['o0'], it['o1']}; continue
    if prev is not None and (it['key'] != prev['key'] or it['src0'] != prev['src0'] + prev['n']):
        aj.add(it['o0'])
    prev = it
aj.discard(0); aj.discard(N)
# cross-check against round 2's own join flags mapped through the timemap (round 3 inserted the clips; nothing else moved)
flag = {it['o0'] for it in EDL if it['kind'] == 'shot' and it.get('join')} - {0}
assert flag <= aj, sorted(flag - aj)
audio_joins = [sec(f) for f in sorted(aj)]

# ---------------------------------------------------------------- talking-head windows: Dan's placed rect per run
thw = []
for r in runs:
    if r['kind'] not in ('presenter', 'presenter-reused'):
        continue
    thw.append(dict(beat=[sec(r['o0']), sec(r['o1'])], rect=clip_rect(r['rect']), motion='tracking',
                    name=f"{r['piece']}-{r['framing']}-{r['placement']}-{r['bg']}({BGS[r['bg']]['type']})"))

# ---------------------------------------------------------------- label chips (exact renderer chip: softblue.disclosure)
os.makedirs(f'{OD}/chips', exist_ok=True)


def chip_png(text, path):
    u = B.unit(W_, H_); tmp = Image.new('RGBA', (W_, 200), (0, 0, 0, 0))
    x0, y0, x1, y1 = B.disclosure(tmp, text, (100, 50), u)
    tmp.crop((int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)))).save(path); return path


def grab(t):
    raw = subprocess.run([FF, '-v', 'error', '-ss', f'{t:.3f}', '-i', MASTER, '-frames:v', '1', '-vf',
                          'scale=in_color_matrix=bt709:in_range=tv,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(H_, W_).astype(np.float32)


def locate(ref_png, t):
    import cv2
    ref = Image.open(ref_png).convert('RGBA'); flat = Image.alpha_composite(Image.new('RGBA', ref.size, (80, 80, 80, 255)), ref)
    r = np.asarray(flat.convert('L'), np.float32); g = grab(t)
    res = cv2.matchTemplate(g[:300, :900], r, cv2.TM_CCOEFF_NORMED); _, mx, _, loc = cv2.minMaxLoc(res)
    return [int(loc[0]), int(loc[1])], round(float(mx), 3)


AI = chip_png('AI-GENERATED', f'{OD}/chips/ai.png')
chips = dict(ai=AI, real=chip_png('Real picture of me. Not AI-generated.', f'{OD}/chips/real.png'))
ai_beats = [('B1-salmon', fr(B1_CUT), fr(B1['b'])), ('B2', fr(next(m for m in MAN if m['id'] == 'B2')['a']),
                                                       fr(next(m for m in MAN if m['id'] == 'B2')['b']))]
setrun = []
for r in runs:
    if r['kind'] in ('presenter', 'presenter-reused') and BGS[r['bg']]['type'] == 'set':
        if setrun and setrun[-1][0] == r['bg'] and setrun[-1][2] == r['o0']:
            setrun[-1][2] = r['o1']
        else:
            setrun.append([r['bg'], r['o0'], r['o1']])
ai_beats += [(f'set-{b}', a, z) for b, a, z in setrun]
ai_beats += [(m['id'], fr(m['a']), fr(m['b'])) for m in MAN if re.match(r'A\d', m['id'])]   # round 5 AI motion inserts
ai_ins = []
for name, a, z in ai_beats:
    pos, score = locate(AI, (a + z) / 2 / FPS)
    ai_ins.append(dict(name=name, beat=[sec(a), sec(z)], chip=AI, pos=pos, match=score))

# ---------------------------------------------------------------- words: intended (film_words_r3) and heard (delivered audio)
FW = json.load(open(f'{R4}/film_words_r5.json'))
words = [dict(w=w['w'], t=round(w['t0'], 3), e=round(w['t1'], 3)) for w in FW if w.get('t0') is not None]
heard, src = speech.transcribe(MASTER, 'small')
transcript_words = [dict(w=w['w'].strip()) for w in heard if w['w'].strip()]

h = hashlib.sha256()
with open(MASTER, 'rb') as f:
    for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
SHA = h.hexdigest()

plan = dict(target_seconds=round(N / FPS, 3), target_frames=N,
            joins=joins, audio_joins=audio_joins, covered=covered, punch=punch, punch_covered=punch_cov,
            graphics=graphics, cards=sorted(cards), ai_inserts=ai_ins, real_photos=[], label_chips=chips,
            words=words, transcript_words=transcript_words, srt=f'{OD}/RO24_R5.srt',
            source_audio=f'{R4}/audio/film_voice_r5.wav',
            banned_source='/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4',
            banned_times=[12.0, 18.0, 288.0],
            watch_log=f'{OD}/logs/watch_pass.json',
            talking_head_windows=thw, evidence_contract=dict(version=2, video_sha256=SHA))
ne = f'{OD}/negative_events_scan.json'
if os.path.exists(ne):
    d = json.load(open(ne))
    assert d['sha256'] == SHA, 'negative_events_scan.json names another render'
    plan['negative_events_scan'] = d
json.dump(plan, open(f'{OD}/plan.json', 'w'), indent=0)
print('sha', SHA[:16], '| runs', len(runs), 'pieces', len(pieces), 'joins', len(joins), 'audio_joins', len(audio_joins),
      'covered', len(covered), 'cards', len(cards), 'graphics', len(graphics), 'thw', len(thw))
print('words', len(words), 'heard', len(transcript_words), src)
print('labels:', [(x['name'], x['pos'], x['match']) for x in ai_ins])
print('audio_joins:', audio_joins)
print('negative_events_scan:', 'yes' if 'negative_events_scan' in plan else 'NOT YET')
