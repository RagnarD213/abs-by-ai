#!/bin/zsh
# fold three judges' findings into one, stamp the watch pass, record the negscan, re-run the delivery gate
# usage: ./fold.sh <build dir> <video> [<judge label>]
set -e
B="$1"; V="$2"; WHO="${3:-Claude Opus 5 x3 (independent watch judges, thirds)}"; cd "$B"
python3 - <<'PY'
import json, glob
parts=[json.load(open(p)) for p in sorted(glob.glob('logs/findings_part*.json'))]
ent=[e for p in parts for e in p['entries']
     if 'negscan' not in str(e.get('image','')) and str(e.get('image','')) != 'sheet.jpg']
# a verdict on an image this pass did not write (a stale strip left in the folder by an earlier pass) is not part of
# the pass: watch.py refuses the whole judgment over it, so it is left out here and named
import os
wp=json.load(open('logs/watch_pass.json'))
names={os.path.basename(x) for k in ('sheets','strips','pairs','clips') for x in wp.get(k,[])}
stale=[e for e in ent if os.path.basename(str(e.get('image',''))) not in names]
if names and stale:
    print('left out (not an image of this pass):', sorted({os.path.basename(str(e.get('image',''))) for e in stale}))
    ent=[e for e in ent if e not in stale]
# The negative-event sheet is recorded by kit_negscan, not the watch pass. Judges use
# basenames, so accept either a negscan path or its bare sheet.jpg basename here.
json.dump(dict(judge=' | '.join(p.get('judge','?') for p in parts), video=parts[0]['video'], method=' || '.join(p.get('method','') for p in parts), entries=ent), open('logs/findings.json','w'), indent=1)
d=[e for e in ent if e.get('verdict')=='defect']; print(len(ent),'entries,',len(d),'defects', [(x.get('t'),x.get('item')) for x in d])
PY
K="${0:A:h}"; D="${K:h:h:h}/_shared/deliver"   # this checkout's own gate tools (never a hard-wired main checkout)
python3 "$D/watch.py" --judge logs/watch_pass.json --findings logs/findings.json --by "$WHO" | tail -4
python3 "$K/kit_negscan.py" record --build "$B" --video "$V" --findings "$(cat logs/negscan_findings.json)" --by "$WHO (part 1)"
python3 "$D/gate.py" "$V" --format ad9x16 --plan plan.json --json gate_final.json > gate_final.log 2>&1 || true
python3 -c "
import json;g=json.load(open('gate_final.json'));print('GATE', g['verdict']);[print(' ',r['key'],r.get('detail','')[:200]) for r in g['rows'] if r.get('ok') is not True]"
