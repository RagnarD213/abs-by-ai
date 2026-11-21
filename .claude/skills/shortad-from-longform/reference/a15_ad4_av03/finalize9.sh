#!/bin/zsh
# After the watch judge has written the four findings_part2 files: merge with the carried verdicts, fold them into each
# watch log, record the negative-events look, run THE gate on each delivered file, then deliver.
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
W="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/watch.py"
cd /Volumes/Extreme/_edit_work/AV-03
BY="independent reviewers, rounds 3 and 4 (carried where the image is pixel-identical) and the round-5 watch judge"
for k in v vc s sc; do python3 zcarry9.py $k --merge || exit 1; done
python3 "$W" --judge logs/watch_pass.json --findings logs/findings.json --by "$BY" | tail -2
( cd cut && python3 "$W" --judge logs/watch_pass.json --findings logs/findings.json --by "$BY" | tail -2 )
python3 "$W" --judge logs/watch_pass_sq.json --findings logs/findings_sq.json --by "$BY" | tail -2
( cd cut_sq && python3 "$W" --judge logs/watch_pass_sq.json --findings logs/findings_sq.json --by "$BY" | tail -2 )
python3 zneg9.py || exit 1
for a in 9x16 1x1; do ./gates9b.sh $a | grep -E "FAIL|\?\?\?\?|passed|GATE"; ./gates9b.sh $a cut | grep -E "FAIL|\?\?\?\?|passed|GATE"; done
echo "FINALIZE DONE $(date +%H:%M:%S)"
