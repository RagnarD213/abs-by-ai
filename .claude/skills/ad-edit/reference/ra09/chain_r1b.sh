#!/bin/bash
# RA-09 round 1 rebuild after the independent review: audio/align/track (chain A), plan, then the picture chain (C, queued).
cd /Volumes/Expansion/_edit_work/RA-09
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
bash chain_a09.sh > logs/chain_a.out 2>&1; grep -q OPTIONS_COMPLETE logs/chain_a.out || { echo FAIL_A; exit 1; }
python3 r1_plan.py > logs/plan_b1.log 2>&1 || { echo FAIL_plan1; exit 2; }
python3 s04b_holdstart.py beats.json > logs/holdstart_b.log 2>&1 || { echo FAIL_hs; exit 3; }
python3 r1_plan.py > logs/plan_b2.log 2>&1 || { echo FAIL_plan2; exit 4; }
python3 r1_s84b_sheet.py > logs/sheet_b.log 2>&1 || { echo FAIL_sheet; exit 5; }
echo "PREP_DONE $(date +%T)"
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq/renderq.py" run --group RA-09 -- bash chain_c09.sh > logs/chain_c.out 2>&1
grep -q CHAIN_C_COMPLETE logs/chain_c.out || { echo FAIL_C; exit 6; }
echo "R1B_COMPLETE $(date +%T)"
