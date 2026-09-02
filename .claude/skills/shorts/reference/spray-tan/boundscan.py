#!/usr/bin/env python3
"""Does any piece boundary run past a source splice?

⚠ The trap that put a 1-9 frame flash of a DIFFERENT take before 11 of 20 cuts on the Zepbound
batch. The long-form cut its pauses tight, so the pause after a beat's last word IS the join,
and snapOut's 0.34s tail walks straight through it. Run on every batch.
"""
import json, subprocess
sp = [r['cut'] for r in json.load(open('work/splices.json')) if r.get('cut')]
pieces = json.loads(subprocess.check_output(
    ['node','-e',"const{SEGMENTS}=require('./segments.js');console.log(JSON.stringify(SEGMENTS.flatMap(s=>s.pieces.map(p=>({id:s.id,...p})))))"]).decode())
bad = 0
for p in pieces:
    for lab, t in (('IN', p['start']), ('OUT', p['end'])):
        near = [c for c in sp if abs(c - t) < 0.60]
        for c in near:
            past = (t > c) if lab == 'OUT' else (t < c)
            if past and abs(t - c) > 0.001:
                print(f"  ⚠ {p['id']} {lab} {t:8.3f} is {abs(t-c)*1000:5.0f} ms "
                      f"{'PAST' if lab=='OUT' else 'BEFORE'} the splice at {c:.3f}")
                bad += 1
            else:
                print(f"    {p['id']} {lab} {t:8.3f} sits {abs(t-c)*1000:5.0f} ms inside its own take "
                      f"(splice {c:.3f}) - ok")
print(f"\n{len(pieces)} pieces, {bad} boundary/boundaries crossing a splice")
