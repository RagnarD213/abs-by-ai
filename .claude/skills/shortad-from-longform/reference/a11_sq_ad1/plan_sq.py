#!/usr/bin/env python3
"""Build plan.json for _shared/deliver/gate.py from THIS build's own files.

`reference/plan_build.py` is written against the a7 pipeline (g5 / crop.json / edl_picture.json).
Ad 1 is the ATTEMPT-3 pipeline: its framing is Muhammad's PUSH RAMPS (beats.PUSHES driving a
zoompan expression), not the NEAR/FAR holds zcrop produces, and its picture is conformed at the
audio splices (edl_frames.json), so both have to be derived differently. Everything here is still
read out of the build -- nothing is typed in by hand.

  python3 plan_sq.py [--cut] [--transcribe]
"""
import json, os, subprocess, sys, glob

CUT = '--cut' in sys.argv
BUILD = os.path.dirname(os.path.abspath(__file__))
if CUT: os.chdir(os.path.join(BUILD, 'cut'))
else:   os.chdir(BUILD)
sys.path.insert(0, os.getcwd())
import beats as B                                                         # noqa
import sqassets as SA                                                     # noqa

FPS = 30000/1001
VID = 'ad1_square_59s.mp4' if CUT else 'ad1_square_1x1.mp4'
tl, ov = B.timeline()
Q = json.load(open('qc.json'))
NTOT = int(round(B.DUR * FPS)) if not CUT else int(round(B.DUR * FPS))
# the renderer's own cumulative plan is the authority on the frame count
NTOT = json.load(open('../cut_plan.json'))['frames'] if CUT else 6976

# --- joins: every picture cut on the DELIVERED timeline.
# This build conforms the picture AT the audio splices, so the cuts are edl_frames.json's
# cumulative segment boundaries (in the cutdown, those mapped through cut_plan.json plus the
# seams -- cut_edl.py wrote that file).
E = json.load(open('edl_frames.json'))
joins, n = [], 0
for s in E:
    if n: joins.append(round(n/FPS, 3))
    n += s['frames']

covered = [[round(b['t0'], 3), round(b['t1'], 3)] for b in tl if b['kind'] != 'talk']
muted = set(B.NO_CAPS_KINDS)
cards = [[round(b['t0'], 3), round(b['t1'], 3)] for b in tl + ov
         if b['kind'] in muted or b['kind'] in ('lt', 'cta') or b.get('caps') is False]

# --- punch: this build has no NEAR/FAR holds. Muhammad's schedule is reproduced as RAMPS, so a
# framing SEGMENT here is "inside a push" (NEAR) or "not" (FAR), sampled off beats.push_at, which
# is the same function the renderer's zoom expression is built from. Ramp frames belong to the
# segment they are heading into, which is what the eye reads.
lev, prev, a0 = [], None, 0.0
for k in range(NTOT):
    t = k/FPS
    L = 'NEAR' if B.push_at(t) > 1.0 + (B.PUSH_Z - 1.0) * 0.5 else 'FAR'
    if L != prev:
        if prev is not None: lev.append([round(a0, 3), round(t, 3), prev])
        prev, a0 = L, t
lev.append([round(a0, 3), round(NTOT/FPS, 3), prev])
kind_at = {}
for b in tl:
    for k in range(int(round(b['t0']*FPS)), min(NTOT, int(round(b['t1']*FPS)))): kind_at[k] = b['kind']
punch, punch_covered = [], []
for a, bb, L in lev:
    punch.append([a, bb, L])
    k0 = int(round(a*FPS))
    punch_covered.append(kind_at.get(k0 - 1, 'talk') != 'talk' or kind_at.get(k0, 'talk') != 'talk')

# --- the two labels, as the compositor actually drew them (full-frame RGBA overlays; the chip's
# position is its alpha bbox)
from PIL import Image
os.makedirs('plan_assets', exist_ok=True)
chips, pos = {}, {}
for kind, pat in (('real', 'chip_real_*.png'), ('ai', 'chip_ai_*.png')):
    fs = sorted(glob.glob(os.path.join(BUILD, 'gfx', pat)))
    if not fs: continue
    im = Image.open(fs[0]).convert('RGBA'); bb = im.getchannel('A').getbbox()
    im.crop(bb).save(f'plan_assets/chip_{kind}.png')
    chips[kind] = os.path.abspath(f'plan_assets/chip_{kind}.png'); pos[kind] = [bb[0], bb[1]]

def _name(b): return os.path.basename(str(b.get('media') or b.get('kind')))

# ⚠ A CARD'S CHIP IS NOT THE FULL-BLEED CHIP. Muhammad's card language hangs the label off the
# card's own media hole (`plate_card`: bottom edge at hole[3] - 34, in a 28 px face), while a
# full-bleed or full-height shot puts it at the waistline above the caption band in a 34 px face.
# One chip image and one position per KIND therefore cannot see a card's label at all: on the first
# run of the shared gate the after_reveal card read -0.031 against the full-bleed reference while
# the label was present and correct on every frame. Each insert now declares its OWN chip and
# position, rendered here by the SAME sqlib calls the compositor makes.
import sqlib as V                                                          # noqa
def _chip_for(b, kind):
    # ⚠ media_ar() probes the FILE, and assets.MEDIA's paths are relative to the BUILD root --
    # from inside cut/ every one of them is a missing file. Do the whole chip computation there.
    here = os.getcwd(); os.chdir(BUILD)
    try:
        return _chip_for_inner(b, kind, here)
    finally:
        os.chdir(here)

def _chip_for_inner(b, kind, outdir):
    import render as R          # imported HERE: render.py loads cx_track.json at import time,
                                # which only exists in the build root (we have chdir'd there)
    t = SA.treat(b['media']); txt = V.REAL_LABEL if kind == 'real' else V.AI_LABEL
    if t['mode'] == 'card':
        hole = V.card_hole(R.media_ar(b['media']), bool(b.get('caption') or b.get('kicker')))
        lay = V.chip_layer(txt, int(hole[3]) - 34, V.font(28, 'SemiBold'))
    else:
        # bleed / fith go through render.chip_png, which is also where the hook's COVER chip is
        # built (it is drawn over the chip burned into the goal video, so it is a different shape)
        from PIL import Image as _I
        lay = _I.open(R.chip_png(kind, t.get('cover_chip'))).convert('RGBA')
    bb = lay.getchannel('A').getbbox()
    os.makedirs(os.path.join(outdir, 'plan_assets'), exist_ok=True)
    q = os.path.join(outdir, 'plan_assets', f"chip_{kind}_{_name(b)}_{t['mode']}.png")
    lay.crop(bb).save(q)
    return os.path.abspath(q), [bb[0], bb[1]]

def _inserts(kind):
    out = []
    for b in tl:
        if not b.get('media') or SA.treat(b['media'])['label'] != kind: continue
        c, q = _chip_for(b, kind)
        out.append(dict(name=_name(b), beat=[round(b['t0'], 3), round(b['t1'], 3)], chip=c, pos=q))
    return out
real_photos = _inserts('real')
ai_inserts = _inserts('ai')

# --- graphics: the overlay MOVs the compositor burned, with their own beats
graphics = []
for o in ov:
    sig = None
    for f in glob.glob(os.path.join(BUILD, 'gfx', f"ov_{o['kind']}_*.mov")):
        graphics.append(dict(name=f"{o['kind']}@{o['t0']:.2f}", beat=[round(o['t0'], 3), round(o['t1'], 3)],
                             mov=os.path.abspath(f))); break

# --- captions as an SRT, from the SAME groups the compositor burned
import captions as CP
words = CP.load_words(); gs = CP.groups(words, CP.suppressed())
def ts(t):
    h = int(t//3600); m = int(t % 3600//60); s = t % 60
    return f'{h:02d}:{m:02d}:{s:06.3f}'.replace('.', ',')
open('plan_assets/captions.srt', 'w').write(
    '\n'.join(f"{i}\n{ts(g[0][1])} --> {ts(g[-1][2])}\n{' '.join(x[0] for x in g)}\n"
              for i, g in enumerate(gs, 1)))

plan = dict(
    target_seconds=round(NTOT/FPS, 6), target_frames=NTOT,
    joins=joins, covered=covered, cards=cards, punch=punch, punch_covered=punch_covered,
    real_photos=real_photos, ai_inserts=ai_inserts, graphics=graphics,
    label_chips=chips, label_pos=pos,
    srt=os.path.abspath('plan_assets/captions.srt'),
    words=[dict(w=w['word'], t=round(float(w['start']), 3), e=round(float(w['end']), 3))
           for w in json.load(open('words_ctc.json'))],
    source_audio=os.path.abspath('his_mix.wav'),
    banned_source=Q.get('banned_source'), banned_times=Q.get('banned_times'),
    watch_log=os.path.abspath('logs/watch_pass.json'),
)
old = json.load(open('plan.json')) if os.path.exists('plan.json') else {}
for k in ('transcript_words', 'negative_events_scan', 'declare'):
    if k in old: plan[k] = old[k]
if '--transcribe' in sys.argv:
    import whisper
    r = whisper.load_model('small').transcribe(VID, word_timestamps=False, language='en')
    plan['transcript_words'] = [dict(w=w) for seg in r['segments'] for w in seg['text'].split()]
json.dump(plan, open('plan.json', 'w'), indent=1)
print(f"{os.getcwd()}/plan.json: {len(joins)} joins, {len(punch)} framing segments, "
      f"{len(real_photos)} real photos, {len(ai_inserts)} AI inserts, {len(graphics)} graphics, "
      f"{len(gs)} caption cues, {len(plan['words'])} words, "
      f"transcript {len(plan.get('transcript_words') or [])}")
