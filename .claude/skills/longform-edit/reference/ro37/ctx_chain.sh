#!/bin/bash
# RO-37 round 1: internal full-length source for the context clips (never delivered; Dan sees only the first minute and
# per-item context clips), then one 540p context clip (item +/- 4 s, voice A) and one graded still per plan item.
set -e
W=/Volumes/Expansion/_edit_work/RO-37/round1; R=$W/recipe; C=$W/review/context; mkdir -p $C
FF="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
T1=$(python3 -c "import json;S=json.load(open('$W/shots.json'));print(S[-1]['out_f1']/(30000/1001))")
[ -s $W/field_full.mp4 ] || (cd $R && python3 -c "import build as B; B.field($T1 + 1, '$W/field_full.mp4')")
mv -f $W/field.mp4 $W/field_90.mp4 2>/dev/null || true; ln -sf $W/field_full.mp4 $W/field.mp4
rm -rf $W/internal_base.mp4.segs; python3 $R/build.py range 0 $T1 $W/internal_base.mp4
cd $R && python3 -c "import build as B; B.voice('$W/assembled_untreated.wav', '$W/voice_A_full.wav', 'A')"
python3 "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes/composite.py" $W/hf/manifest.json --base $W/internal_base.mp4 --base-t0 0 --out $W/internal_full.mp4 --audio $W/voice_A_full.wav
python3 $R/context.py
echo CONTEXT_DONE
