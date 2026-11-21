#!/bin/zsh
# DS-44 R2 build, one render-queue step: full-height re-key of the watching piece (option B), the interview card cache,
# framing, captions, assembly, then QA and the delivery gate.
cd /Volumes/Expansion/_edit_work/DS-44/r2
R="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"
[ -f key/c2_watchF/f0659.npy ] || zsh recipe/run_key_watchF.sh || { echo KEY FAIL; exit 1; }
[ -f src/card_58-74_24fps.npy ] || python3 recipe/prep_media.py --card || { echo CARD FAIL; exit 1; }
python3 recipe/framing.py > framing.log 2>&1 || { echo FRAMING FAIL; tail -5 framing.log; exit 1; }; grep -E "watch/TR" framing.log | cut -c1-160
python3 recipe/captions.py house_bass15 || { echo CAPTIONS FAIL; exit 1; }
WORKERS=4 python3 recipe/assemble.py --voice house_bass15 --look B_warmvivid > assemble.log 2>&1 || { echo ASSEMBLE FAIL; tail -5 assemble.log; exit 1; }; tail -1 assemble.log
zsh recipe/chain_qa_r2.sh
python3 "$R/.claude/skills/_shared/deliver/gate.py" "review/Hormozi Fat Guy SFC R2 - complete Short.mp4" --format short --plan gate-plan.json > deliver_gate.log 2>&1
grep -E "^\s+(FAIL|\?\?\?\?)|passed|DELIVERY GATE" deliver_gate.log
echo BUILD R2 DONE
