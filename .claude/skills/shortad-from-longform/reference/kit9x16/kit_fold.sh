#!/bin/zsh
# fold three judges' findings into one, stamp the watch pass, record the negscan, re-run the delivery gate
# usage: ./fold.sh <build dir> <video> [<judge label>]
set -e
B="$1"; V="$2"; WHO="${3:-Claude Opus 5 x3 (independent watch judges, thirds)}"; cd "$B"
python3 - <<'PY'
import json, glob
parts=[json.load(open(p)) for p in sorted(glob.glob('logs/findings_part*.json'))]
ent=[e for p in parts for e in p['entries'] if 'negscan' not in str(e.get('image',''))]   # the negscan sheet is recorded by kit_negscan, not the watch pass
json.dump(dict(judge=' | '.join(p.get('judge','?') for p in parts), video=parts[0]['video'], method=' || '.join(p.get('method','') for p in parts), entries=ent), open('logs/findings.json','w'), indent=1)
d=[e for e in ent if e.get('verdict')=='defect']; print(len(ent),'entries,',len(d),'defects', [(x.get('t'),x.get('item')) for x in d])
PY
D="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver"; K="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shortad-from-longform/reference/kit9x16"
python3 "$D/watch.py" --judge logs/watch_pass.json --findings logs/findings.json --by "$WHO" | tail -4
python3 "$K/kit_negscan.py" record --build "$B" --video "$V" --findings "$(cat logs/negscan_findings.json)" --by "$WHO (part 1)"
python3 "$D/gate.py" "$V" --format ad9x16 --plan plan.json --json gate_final.json > gate_final.log 2>&1 || true
python3 -c "
import json;g=json.load(open('gate_final.json'));print('GATE', g['verdict']);[print(' ',r['key'],r.get('detail','')[:200]) for r in g['rows'] if r.get('ok') is not True]"
