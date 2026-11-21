#!/usr/bin/env python3
"""Regenerate plan.js's SHOTS table from the manifest, with the punch alternation.

Was done by hand and broke the build twice when the shot list changed (a dropped piece left a
stale entry). Every talk shot gets its measured torso centre; every short opens WIDE and
alternates at each join, so no join is ever naked. AI cover clips are skipped - they are
self-describing and they ARE the framing change.
"""
import json, re
man = json.load(open('shots/manifest.json'))
geom = json.load(open('work/beatgeom.json'))
by = {(v['seg'], v['beat']): v for v in geom.values()}
byname = {k: v for k, v in geom.items() if v.get('src') == 'raw'}

lines, last, tight = [], None, False
for m in man:
    if m['seg'] != last:
        lines.append(f"\n  // ---- {m['seg']} ----------------------------------------------------------------")
        last, tight = m['seg'], False
    elif m.get('src') != 'ai':
        tight = not tight
    if m.get('src') == 'ai':
        lines.append(f"  '{m['name']}': {{ t: 'ai', aiIn: {m['aiIn']} }},")
        continue
    g = byname[m['name']] if m['name'] in byname else by[(m['seg'], m['beat'])]
    extra = ", tight: true" if tight else ""
    src = ", src: 'raw'" if m['src'] == 'raw' else ""
    lines.append(f"  '{m['name']}': {{ t: 'talk', x: {g['torso']:.4f}{extra}{src} }},")

s = open('plan.js').read()
a = s.index("const SHOTS = {"); b = s.index("\n};", a)
open('plan.js', 'w').write(s[:a] + "const SHOTS = {" + "\n".join(lines) + s[b:])
n_ai = sum(1 for m in man if m.get('src') == 'ai')
print(f"plan.js: {len(man)} shots ({n_ai} AI cover clips), punch alternation assigned")
