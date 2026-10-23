#!/bin/zsh
# waits for the key jobs and the graphics, then renders the full R6 draft and its pink key check
set -e
cd /Volumes/Expansion/_edit_work/ds40/r6
RQ="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq/renderq.py"
until grep -qE "KEY DONE|Traceback|Error" run_key.log && grep -qE "FIX DONE|Traceback|Error" r4fix/run_fix.log; do sleep 30; done
grep -q "KEY DONE" run_key.log || { echo "KEY FAILED"; exit 1; }
grep -q "FIX DONE" r4fix/run_fix.log || { echo "FIX FAILED"; exit 1; }
until [[ -f gfx/hf/renders/G1.mov && -f gfx/hf/renders/G2_mask.mov && -f gfx/hf/renders/G3.mov && -f gfx/hf/renders/G4_mask.mov ]] && ! pgrep -f "gfx.*build.py --render" >/dev/null; do sleep 30; done
cd key
python3 "$RQ" run --group ds40 --label "ds40 r6 full draft" -- python3 comp_r6.py "../renders/DS40 R6 draft.mp4"
python3 "$RQ" run --group ds40 --label "ds40 r6 pink" -- python3 comp_r6.py "../renders/DS40 R6 pink.mp4" --pink
echo CHAIN DONE
