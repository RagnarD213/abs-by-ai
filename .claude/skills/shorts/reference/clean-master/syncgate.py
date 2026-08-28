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
            for l in open(f'build/{sid}.ass') if l.startswith('Dialogue:')]
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
    # also: did the first word survive the in-point?
    first_cap = re.sub(r'[^a-z0-9]', '', cues[0][1].split()[0].lower())
    heard_first = heard[0][0] if heard else ''
    clipped = first_cap != heard_first and first_cap not in [w for w, _ in heard[:3]]
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
