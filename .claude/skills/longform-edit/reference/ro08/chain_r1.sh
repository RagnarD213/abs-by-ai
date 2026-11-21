#!/bin/zsh
# round 1 chain, worker A: changed lower thirds -> first minute -> audio gate -> stills -> context clips (list A)
cd /Volumes/Extreme/_edit_work/ro08
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
HF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes/from_plan.py"
python3 "$HF" --plan plan_resolved.json --words words_out.json --out hf --shots shots.json --render > hf_r2.log 2>&1 || { echo "HF FAILED"; exit 1; }
echo "HF DONE $(ls hf/renders/*.mov | grep -v mask | wc -l)"; touch hf_r2.done
python3 recipe/round1.py first > round1/first.log 2>&1 || { echo "FIRST FAILED"; tail -5 round1/first.log; exit 1; }
( cd round1/first-minute && python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py" "DRAFT - RO-08 round 1 - first minute.mp4" --ab AB_reference-vs-ours.mp4 > audio_gate.log 2>&1; tail -2 audio_gate.log )
echo "FIRST DONE"
python3 recipe/stills.py > round1/stills.log 2>&1 || { echo "STILLS FAILED"; tail -5 round1/stills.log; exit 1; }
echo "STILLS DONE"
python3 recipe/round1.py context $(cat ctx_a.txt) > round1/context_a.log 2>&1 || { echo "CONTEXT A FAILED"; tail -5 round1/context_a.log; exit 1; }
touch ctx_a.done; echo "CONTEXT A DONE $(ls round1/context | grep -c 'REVIEW 540p.mp4')"
