#!/usr/bin/env python3
"""plan.json for _shared/deliver/gate.py, for the four AV-03 / AS-02 files, built from THIS build's own files (never by
hand) and bound to the delivered file's sha256 (evidence contract v2). Runs from the build root for all four:

  python3 plan9.py [--aspect 1x1] [--cut]

Everything a row needs is derived from the code that DREW the frame (skill A12.10b): caption states from the cap list
the compositor read, label chips cropped from the delivered frame at their measured position (A13.3: a 215/255 chip
over a bright picture cannot be graded against a grey reference), window rects from the renderer's own layout calls,
overlay regions from the overlay images' alpha.
"""
import datetime, hashlib, json, os, subprocess, sys
import numpy as np
from PIL import Image
args = sys.argv[1:]
ASPECT = args[args.index('--aspect')+1] if '--aspect' in args else '9x16'
SQ = ASPECT == '1x1'; CUT = '--cut' in args; SFX = '_sq' if SQ else ''
sys.argv = [sys.argv[0], '--aspect', ASPECT]
import render9 as R, beats as B, captions as CP
FF = R.FF; FPS = B.FPS; VW, VH = R.VW, R.VH
D = (f'cut{SFX}' if CUT else '.')
VID = f"{D}/ad4_{ASPECT}{'_59s' if CUT else ''}.mp4"
CAPDIR = f'{D}/cap' if CUT else f'cap{SFX}'
CROPF = f'{D}/crop.json' if CUT else f'crop{SFX}.json'
PA = f'{D}/plan_assets{SFX}'; os.makedirs(PA, exist_ok=True)
PLAN = f'{D}/plan{SFX}.json' if not CUT else f'{D}/plan.json'
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()
assert os.path.exists(VID), f'the delivered file is not on disk: {VID}'
VSHA = sha(VID)

# ---- the timeline of THIS file (cut frames for a cutdown), each beat carrying its MASTER n0 (labels are keyed on it)
mtl, mov = B.timeline()
if CUT:
    T = json.load(open(f'{D}/cut_timeline.json')); NTOT = T['NTOT']; SEAMS = [s/FPS for s in T['seams']]
    tl = []
    for b in T['beats']:
        mb = next(x for x in mtl if x['n0'] <= b['m0'] < x['n1'])
        tl.append(dict(b, t0=b['n0']/FPS, t1=b['n1']/FPS, key_n0=mb['n0'], mn0=mb['n0'], off=b['m0']-mb['n0']))
    ov = [dict(o, t0=o['n0']/FPS, t1=o['n1']/FPS) for o in T['overlays']]
else:
    NTOT = B.NTOT; SEAMS = []
    tl = [dict(b, key_n0=b['n0'], mn0=b['n0'], off=0) for b in mtl]; ov = mov
def beat(a, b): return [round(a/FPS, 3), round(b/FPS, 3)]

# ---- joins / covered / cards / punch (as reference/plan_build.py)
E = json.load(open(f'{D}/edl_picture.json'))
joins = sorted({round(s['n0']/FPS, 3) for s in E[1:]})
covered = [beat(b['n0'], b['n1']) for b in tl if b['kind'] != 'talk']
# Muhammad's light-leak strobes hide a join exactly as an insert does (his cut lands ON the flash peak: skill A3.2). The
# frames the compositor flashed are B.FLASH (master) / the cut timeline's `flashes`; each run of them is a covering beat.
_fl = sorted(T['flashes']) if CUT else sorted(B.FLASH)
_runs = []
for n in _fl:
    if _runs and n == _runs[-1][1]: _runs[-1][1] = n + 1
    else: _runs.append([n, n + 1])
covered += [beat(a - 1, z + 1) for a, z in _runs]
def is_muted(b): return b['kind'] in B.NO_CAPS_KINDS or (b['kind'] == 'window' and b.get('body') in B.NO_CAPS_BODIES)
cards = [beat(b['n0'], b['n1']) for b in tl if is_muted(b)]
C = json.load(open(CROPF)); kind_of = {}
for b in tl:
    for n in range(b['n0'], b['n1']): kind_of[n] = b['kind']
merged = []
for h in C['holds']:
    if merged and merged[-1]['level'] == h['level'] and merged[-1]['n1'] == h['n0']: merged[-1] = dict(merged[-1], n1=h['n1'])
    else: merged.append(dict(n0=h['n0'], n1=h['n1'], level=h['level']))
punch = [beat(h['n0'], h['n1']) + [h['level']] for h in merged]
punch_covered = [kind_of.get(h['n0'] - 1, 'talk') != 'talk' for h in merged]

# ---- captions: the SAME words, groups and stops the compositor used -> an SRT and the per-word PNG states
words = CP.load_words(f'{D}/words_ctc.json')
mute = [(b['t0'], b['t1']) for b in tl if is_muted(b)] + [(o['t0'], o['t1']) for o in ov if o['kind'] in B.NO_CAPS_OVERLAYS]
gs = CP.groups(words, mute)
STOPS = sorted(set([a for a, _ in mute] + SEAMS + [b['t0'] for b in tl]))
def cue_end(g, nxt):
    ws, we = g[-1][1], g[-1][2]; hold = max(we, ws + 0.12)
    end = min(nxt, max(hold, min(nxt, we + 0.8))) if nxt is not None else we + 0.3
    end = max(end, ws + 1.0/29.97)
    stop = next((s for s in STOPS if s > ws + 1e-3), None)
    if stop is not None: end = max(min(end, stop), ws + 1.0/29.97)
    return end
def ts(t):
    return f'{int(t//3600):02d}:{int(t % 3600//60):02d}:{t % 60:06.3f}'.replace('.', ',')
srt = [f"{i}\n{ts(g[0][1])} --> {ts(cue_end(g, gs[i][0][1] if i < len(gs) else None))}\n{' '.join(x[0] for x in g)}\n" for i, g in enumerate(gs, 1)]
open(f'{PA}/captions.srt', 'w').write('\n'.join(srt))
sched = [(a, b, p) for a, b, p in R.caption_schedule(f'{CAPDIR}/list.txt') if not p.endswith('_blank.png')]
flat = [w for g in gs for w in g]
assert len(sched) == len(flat), (len(sched), len(flat), 'cap list and caption groups disagree: re-run the captions')
_h = {}
def hsha(p):
    if p not in _h: _h[p] = sha(p)
    return _h[p]
caption_states = [dict(name=f'caption-{i:05d}', word=w[0], beat=[round(a, 4), round(b, 4)], speech=[round(w[1], 3), round(w[2], 3)],
                       image=os.path.abspath(p), pos=[0, 0], scale=1.0, image_sha256=hsha(p)) for i, ((a, b, p), w) in enumerate(zip(sched, flat))]

# ---- labels: each chip cropped from the DELIVERED frame at its measured position
PLACE = json.load(open('label_place.json'))
def grab(n):
    r = subprocess.run([FF, '-nostdin', '-v', 'error', '-i', VID, '-vf', f"select='eq(n\\,{n})',scale=in_color_matrix=bt709", '-fps_mode', 'passthrough',
                        '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(r, np.uint8).reshape(VH, VW, 3)
real_photos, ai_inserts, tracks = [], [], []
for b in tl:
    kind = b.get('label') or ('real' if b['kind'] == 'shot' else None)
    if not kind: continue
    p = PLACE[f"{ASPECT}:{b['key_n0']}"]; w, h = R.chip_size(kind, p['lines'], p['size'])
    name = f"{kind}_{b['key_n0']}"; mid = b['n0'] + (b['n1'] - b['n0'])//2
    img = f'{PA}/chip_{name}.png'; Image.fromarray(grab(mid)[p['y']:p['y']+h, p['x']:p['x']+w]).save(img)
    ins = dict(name=os.path.basename(str(b.get('media', ''))), beat=beat(b['n0'], b['n1']), chip=os.path.abspath(img), pos=[p['x'], p['y']])
    of_dan = 'robot' not in str(b.get('media'))
    if kind == 'real': real_photos.append(ins)
    elif of_dan: ai_inserts.append(ins)
    tracks.append(dict(name=name, kind=kind, beat=ins['beat'], image=ins['chip'], image_sha256=sha(img), pos=ins['pos'],
                       search_px=2, visibility='full'))

# ---- obstacles the captions must clear, and Dan's windows
regions = [dict(name=f'card@{a:.3f}', beat=[a, b], rect=[0, 0, VW, VH]) for a, b in cards]
for o in ov:
    bb = R.overlay_img(o, (o['n0'] + o['n1'])//2).getchannel('A').getbbox()
    if bb: regions.append(dict(name=f"{o['kind']}@{o['t0']:.3f}", beat=beat(o['n0'], o['n1']), rect=[bb[0], bb[1], bb[2]-bb[0], bb[3]-bb[1]]))
windows = []
for i, b in enumerate(tl):
    if b['kind'] == 'talk': windows.append(dict(name=f'talk-{i}', beat=beat(b['n0'], b['n1']), rect=[0, 0, VW, VH], motion='tracking'))
    elif b['kind'] == 'window':
        if b['body'] == 'bullets':
            it = [0.0 for _ in b['item_n']]
            _, th = R.G.bullets_body2(0, b['header'], b['items'], it, tails=[(tx, 0.0) for tx, _ in b.get('tails', [])])
            r = R.win_rect(th)
        else: r = (0, 0, 600, VH) if SQ else (0, 60, VW, 640)
        windows.append(dict(name=f'window-{i}', beat=beat(b['n0'], b['n1']), rect=[r[0], r[1], r[2]-r[0], r[3]-r[1]], motion='fixed-wide'))

Q = json.load(open(f'{D}/qc.json'))
plan = dict(
    target_seconds=round(NTOT/FPS, 6), target_frames=NTOT,
    joins=joins, covered=covered, cards=cards, punch=punch, punch_covered=punch_covered,
    real_photos=real_photos, ai_inserts=ai_inserts, graphics=[],
    srt=os.path.abspath(f'{PA}/captions.srt'),
    words=[dict(w=w[0], t=round(float(w[1]), 3), e=round(float(w[2]), 3)) for w in words],
    source_audio=os.path.abspath(f'{D}/his_mix.wav'),
    banned_source=Q.get('banned_source'), banned_times=Q.get('banned_times'),
    watch_log=os.path.abspath(f'{D}/logs/watch_pass{SFX}.json'),
    caption_states=caption_states, caption_highlight_rgb=list(R.G5.OLIVE),
    speech_words=[dict(w=w[0], t=round(float(w[1]), 3), e=round(float(w[2]), 3)) for w in words],
    speech_words_evidence=dict(method='delivered_asr', video_sha256=VSHA,
        timing='wav2vec2 CTC forced alignment of the ASR words to the editor mix; the delivered audio IS that mix '
               '(full length: his AAC stream copied bit for bit, md5 asserted at the mux; cutdown: the same mix cut at the seams)'),
    graphic_regions=regions, talking_head_windows=windows, label_tracks=tracks,
    evidence_contract=dict(version=2, video_sha256=VSHA, generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat()),
)
if not CUT: plan['reference_cut'] = os.path.abspath('ref/ad4_v4_hd.mp4')
if real_photos: plan.setdefault('label_chips', {})['real'] = real_photos[0]['chip']; plan.setdefault('label_pos', {})['real'] = real_photos[0]['pos']
if ai_inserts: plan.setdefault('label_chips', {})['ai'] = ai_inserts[0]['chip']; plan.setdefault('label_pos', {})['ai'] = ai_inserts[0]['pos']
old = json.load(open(PLAN)) if os.path.exists(PLAN) else {}
for k in ('transcript_words', 'negative_events_scan', 'declare'):
    if k in old: plan[k] = old[k]
tw = f"{D}/transcript_words.json"          # the delivered audio re-transcribed (ztranscribe9.py); same audio in both aspects
if os.path.exists(tw): plan['transcript_words'] = json.load(open(tw))
if isinstance(plan.get('negative_events_scan'), dict) and plan['negative_events_scan'].get('sha256') != VSHA: del plan['negative_events_scan']
json.dump(plan, open(PLAN, 'w'), indent=1)
print(f"{PLAN}: {VID} sha {VSHA[:12]}  {len(joins)} joins, {len(punch)} holds, {len(real_photos)} real photos, {len(ai_inserts)} AI-of-Dan, "
      f"{len(gs)} cues / {len(caption_states)} states, {len(regions)} regions, {len(windows)} windows, transcript {len(plan.get('transcript_words') or [])}")
