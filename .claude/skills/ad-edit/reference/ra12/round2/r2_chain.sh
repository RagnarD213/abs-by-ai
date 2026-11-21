#!/bin/bash
# RA-12 round 2 (Dan 2026-10-17): prospect everywhere, C1/L1/C2 under the captions, W1 = B0427, D1 = C1546 salad. round1/ untouched.
cd /Volumes/Expansion/_edit_work/ra12
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
export K1_CHIP_Y=1720
echo "START $(date +%T)"
set -x
python3 r2_s84_plan.py > round2/logs/plan.log 2>&1 || exit 4
python3 r2_s84b_sheet.py > round2/logs/sheet.log 2>&1 || exit 7
python3 "$SH/hyperframes/vertical.py" --sheet round2/gfx_sheet.json --out round2/gfx --render --snap --force > round2/logs/gfx.log 2>&1 || exit 8
python3 r2_s83_phone.py > round2/logs/s83.log 2>&1 || exit 9
python3 r2_s83b_clips.py > round2/logs/s83b.log 2>&1 || exit 10
python3 r2_s85_captions.py 9x16 > round2/logs/s85.log 2>&1 || exit 11
python3 r2_s82_holds.py dan08 dan09 dan10 > round2/logs/s82.log 2>&1 || exit 12
python3 r2_s86_assemble.py work > round2/logs/s86w.log 2>&1 || exit 13
python3 r2_s86_assemble.py cuts > round2/logs/s86c.log 2>&1 || exit 15
echo "R2_CHAIN_COMPLETE $(date +%T)"
