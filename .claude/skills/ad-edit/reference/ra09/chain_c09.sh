#!/bin/bash
# RA-09 round 1: graphics, cards, captions, Dan holds, composite, review cuts.
cd /Volumes/Expansion/_edit_work/RA-09
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
mkdir -p r1/logs
echo "START $(date +%T)"
set -x
[ "$SKIP_GFX" = 1 ] || python3 "$SH/hyperframes/vertical.py" --sheet r1/gfx_sheet.json --out r1/gfx --render --snap --force > r1/logs/gfx.log 2>&1 || { echo FAIL_gfx; exit 8; }
[ "$SKIP_CARDS" = 1 ] || python3 r1_cards.py > r1/logs/cards.log 2>&1 || { echo FAIL_cards; exit 9; }
[ "$SKIP_CAPS" = 1 ] || python3 r1_s85_captions.py 9x16 > r1/logs/s85.log 2>&1 || { echo FAIL_caps; exit 11; }
rm -f r1/seg/*.mp4 r1/seg/holds.json
python3 r1_s82_holds.py > r1/logs/s82.log 2>&1 || { echo FAIL_holds; exit 12; }
N=$(python3 -c "import json;print(json.load(open('beats.json'))['total_frames'])"); D=$(python3 -c "print(f'{$N*1001/30000:.6f}')")
"$FF" -nostdin -v error -y -i mix_b15.wav -af "apad,atrim=0:$D" -c:a pcm_s16le mix_r1.wav || { echo FAIL_pad; exit 14; }
python3 r1_s86_assemble.py work > r1/logs/s86w.log 2>&1 || { echo FAIL_work; exit 13; }
python3 r1_s86_assemble.py cuts > r1/logs/s86c.log 2>&1 || { echo FAIL_cuts; exit 15; }
echo "CHAIN_C_COMPLETE $(date +%T)"
