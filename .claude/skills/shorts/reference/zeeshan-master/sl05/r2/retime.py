#!/usr/bin/env python3
"""retime.py [--apply]: where a SOURCE word's CTC time (work/words_aligned.json) disagrees by > 100 ms with the same
word's CTC time measured on the DELIVERED audio (gate/<S>_speech_ctc.json, mapped back to source time), take the
delivered measurement. The two passes differ where the source pass aligned across a music swell or a number. Every
change is logged in work/retime_log.json. Only words inside a piece are touched; the piece audio is identical in both."""
import json, re, sys, subprocess, difflib
segs = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./segments.js').SEGMENTS))"]))
d = json.load(open('work/words_aligned.json')); W = d['chunks']
nz = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
log = []
for s in segs:
    sp = json.load(open(f"gate/{s['id']}_speech_ctc.json")); off = 0.0; src = []
    for p in s['pieces']:
        for i, w in enumerate(W):
            a, b = w['timestamp']
            if b <= p['start'] or a >= p['end']: continue
            if (min(b, p['end']) - max(a, p['start'])) / max(1e-6, b - a) <= 0.5: continue
            src.append((i, off + max(0, a - p['start']), p, off))
        off += p['end'] - p['start']
    A = [nz(W[i]['text']) for i, _, _, _ in src]; B = [nz(x['w']) for x in sp]
    for a0, b0, n in difflib.SequenceMatcher(None, A, B, autojunk=False).get_matching_blocks():
        for j in range(n):
            i, t, p, po = src[a0 + j]; dv = sp[b0 + j]['t']; dlt = dv - t
            if abs(dlt) > 0.10 and abs(dlt) < 0.8:
                na = p['start'] + (dv - po); old = list(W[i]['timestamp'])
                nb = max(old[1] + dlt if dlt > 0 else old[1], na + 0.06)
                log.append({'seg': s['id'], 'word': W[i]['text'].strip(), 'old': old, 'new': [round(na, 3), round(nb, 3)], 'delivered_t': dv, 'delta': round(dlt, 3)})
                if '--apply' in sys.argv: W[i]['timestamp'] = [round(na, 3), round(nb, 3)]
for l in log: print(l['seg'], l['word'], l['old'], '->', l['new'], l['delta'])
print(len(log), 'words')
if '--apply' in sys.argv:
    # keep onsets monotonic after a shift
    json.dump(d, open('work/words_aligned.json', 'w')); json.dump(log, open('work/retime_log.json', 'w'), indent=1)
