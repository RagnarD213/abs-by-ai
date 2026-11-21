#!/bin/bash
cd /Volumes/Expansion/_edit_work/ra12
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
set -x
python3 r2_s84_plan.py > round2/logs/plan.log 2>&1 || exit 4
python3 r2_s84b_sheet.py > round2/logs/sheet.log 2>&1 || exit 7
python3 "$SH/hyperframes/vertical.py" --sheet round2/gfx_sheet.json --out round2/gfx --render --snap --force --only C1,L1,C2 > round2/logs/gfx4.log 2>&1 || exit 8
python3 r2_s85_captions.py 9x16 > round2/logs/s85.log 2>&1 || exit 11
python3 r2_s86_assemble.py work > round2/logs/s86w.log 2>&1 || exit 13
python3 r2_s86_assemble.py cuts > round2/logs/s86c.log 2>&1 || exit 15
bash r2_gate_seq.sh
