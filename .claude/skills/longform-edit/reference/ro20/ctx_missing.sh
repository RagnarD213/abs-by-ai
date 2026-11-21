#!/bin/zsh
# re-run the context clip of every lower third that has none, ONE per call (a failing clip no longer takes its batch down)
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
W=/Volumes/Extreme/_edit_work/ro20; cd $W
M=($(python3 -c "
import json, os, sys
R=json.load(open('plan_resolved.json')); have={f.split('-context')[0] for f in os.listdir('round1/context') if f.endswith('REVIEW 540p.mp4') and not f.startswith('._')}
x=[r['id'] for r in R if r['kind']=='lt' and r['id'] not in have]; print(' '.join(x[int(sys.argv[1])::2]))" $1))
for i in $M; do python3 recipe/round1.py context $i > ctx_fix_$i.log 2>&1 && echo "OK $i" >> ctx_fix.log || echo "FAILED $i: $(grep -E 'Error|error' ctx_fix_$i.log | grep -v -E 'muxing|trailer|Broken' | tail -1 | cut -c1-200)" >> ctx_fix.log; done
echo "WORKER $1 DONE" >> ctx_fix.log
