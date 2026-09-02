#!/usr/bin/env python3
"""HARD GATE: do the burned captions match the delivered audio?

The one check that measures what a viewer experiences. Everything upstream - word
timestamps, speech gaps, cut points - is computed on an extracted WAV; the cuts and the
picture come from `-ss` on the source MP4. If those timelines disagree by even a fraction of
a second the captions drift, and NOTHING ELSE IN THE PIPELINE NOTICES: on 2026-08-28 this
batch passed 12/12 QC, the splice test, loudness, duration and the centring audit while
shipping captions up to 650 ms late and clipping the first word off two shorts.

Method: transcribe the DELIVERED file, match each caption's first word to the nearest
occurrence of that word in the heard audio, and report the median offset.
"""
import json, re, subprocess, sys
from difflib import SequenceMatcher
import numpy as np, whisper
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
TOL = 0.120                     # 120 ms: below one caption chunk, and imperceptible on screen

# ⚠ CALIBRATION, NOT A FUDGE. This gate transcribes with base.en (fast) while the captions
# come from medium.en, and the two models do not agree on where a word starts: measured on
# the SAME source audio over three spans (n=414 words), base.en reports onsets a median of
# exactly -80 ms earlier than medium.en, and the figure was -80 ms in all three spans
# independently. Without correcting for it the gate reads a lag that is not on screen - it
# flagged two shorts at -120/-140 ms whose real offset is -40/-60 ms. Re-measure this if the
# gate model or the analysis model ever changes.
#   work/modelbias.py reproduces the measurement.
MODEL_BIAS = -0.080

segs = json.loads(subprocess.check_output(
    ['node', '-e', "const {SEGMENTS}=require('./segments.js');"
     "console.log(JSON.stringify(SEGMENTS.map(s=>[s.id,s.slug])))"]).decode())
only = sys.argv[1:]
m = whisper.load_model('base.en')
bad = 0
results = {}
for sid, slug in segs:
    if only and sid not in only: continue
    f = f'out/{sid.lower()}_{slug}.mp4'
    p = subprocess.run([FF, '-v', 'error', '-i', f, '-vn', '-ac', '1', '-ar', '16000',
                        '-f', 's16le', '-'], capture_output=True)
    x = np.frombuffer(p.stdout, dtype=np.int16).astype(np.float32) / 32768.0
    r = m.transcribe(x, language='en', word_timestamps=True, verbose=False)
    heard = [(re.sub(r'[^a-z0-9]', '', w['word'].lower()), w['start'])
             for s in r['segments'] for w in s.get('words', [])]
    def t(s):
        h, mm, rest = s.split(':'); return int(h) * 3600 + int(mm) * 60 + float(rest)
    cues = [(t(re.match(r'Dialogue: 0,([^,]+),', l).group(1)), l.rsplit(',,', 1)[1].strip())
            for l in open(f'build/{sid}/{sid}.ass') if l.startswith('Dialogue:')]
    errs = []
    for ct, txt in cues:
        first = re.sub(r'[^a-z0-9]', '', txt.split()[0].lower())
        cands = [ws for w, ws in heard if w == first]
        if not cands: continue
        near = min(cands, key=lambda s: abs(s - ct))
        if abs(near - ct) < 2.5: errs.append((near - ct) - MODEL_BIAS)
    if len(errs) < 8:
        print(f"  ✗ {sid}: only {len(errs)} cues could be matched - cannot judge"); bad += 1; continue
    e = np.array(errs)
    ok = abs(np.median(e)) <= TOL
    if not ok: bad += 1
    # Did the first word survive the in-point?
    # ⚠ WHISPER HALLUCINATES A LEAD-IN when a clip starts mid-sentence. Short B opens on
    # "You're taking nothing right now"; base.en invented "So let's say" in front of it and
    # compressed the real words to make room, so a strict first-word test failed a correct
    # build. Measured directly, speech starts 0.1s in and "How should you get started" lands
    # at 2.31s, exactly where the source puts it. So: accept the caption's first word if it is
    # heard anywhere in the opening second, not only as token zero.
    first_cap = re.sub(r'[^a-z0-9]', '', cues[0][1].split()[0].lower())
    early = [w for w, ws in heard if ws < 1.0]
    heard_first = heard[0][0] if heard else ''
    # ⚠ base.en and medium.en TOKENISE DIFFERENTLY, and the difference is not a clipped word.
    # This gate transcribes with base.en; the captions come from medium.en. base.en writes
    # "All right," as the single token "alright", so caption 'all' is absent from the heard
    # list and the check fires on a short whose first word is provably intact (measured on
    # B: speech starts 0.360 s, caption starts 0.380 s). Treat a caption word that PREFIXES
    # an early heard token, or vice versa, as the same word.
    def same(a, b):
        return a == b or (len(a) >= 3 and b.startswith(a)) or (len(b) >= 3 and a.startswith(b))
    # ⚠ ...and a prefix test is NOT enough, because the two models also SPELL it differently:
    # the caption reads "All right," -> "allright" while base.en hears "alright" (one l), so
    # neither prefixes the other. Compare the opening ~12 letters as a similarity ratio, which
    # absorbs both the tokenisation and the spelling. 'allright' vs 'alright' scores 0.93.
    letters = lambda xs: re.sub(r'[^a-z0-9]', '', ' '.join(xs).lower())[:12]
    cap_open = letters(' '.join(c[1] for c in cues[:2]).split()[:3])
    heard_open = letters([w for w, _ in heard[:3]])
    ratio = SequenceMatcher(None, cap_open, heard_open).ratio() if cap_open and heard_open else 0.0
    cands = ([heard_first] if heard_first else []) + early[:6]
    clipped = not any(same(first_cap, w) for w in cands) and ratio < 0.80
    if clipped: bad += 1
    results[sid] = {'median_ms': round(float(np.median(e))*1000, 1),
                    'sd_ms': round(float(e.std())*1000, 1), 'n': len(e),
                    'clipped': bool(clipped), 'ok': bool(ok and not clipped)}
    print(f"  {'OK ' if ok and not clipped else '✗  '} {sid}: caption vs audio median "
          f"{np.median(e)*1000:+6.0f} ms (mean {e.mean()*1000:+.0f}, sd {e.std()*1000:.0f}, "
          f"n={len(e)})   opens on {heard_first!r} vs caption {first_cap!r}"
          f"{'  <- FIRST WORD CLIPPED' if clipped else ''}")
# Stamp the result so qc.js can refuse to pass a file this gate has not seen. Keyed on the
# delivered file's mtime, so re-rendering a short invalidates its stamp.
import os
stamp = {}
if os.path.exists('build/syncgate.json'):
    stamp = json.load(open('build/syncgate.json'))
for sid, slug in segs:
    if only and sid not in only: continue
    if sid in results:
        stamp[sid] = {'mtime': os.path.getmtime(f'out/{sid.lower()}_{slug}.mp4'), **results[sid]}
json.dump(stamp, open('build/syncgate.json', 'w'), indent=1)
print('\nSYNC GATE PASS' if bad == 0 else f'\nSYNC GATE: {bad} problem(s)')
sys.exit(0 if bad == 0 else 1)
