#!/bin/bash
# Render ONE variant end to end: segments -> graded cut -> J2 chips -> composite -> SRT.
# One render per variant, after all its cuts are final (per the handoff).
set -e
V="$1"
W="/Volumes/Seagate 4TB/_edit_work/invest-health-cutdowns"
export PATH="$W/bin:$PATH"
cd "$W/$V"
NAME=$( [ "$V" = "cons" ] && echo INVEST_HEALTH_conservative || echo INVEST_HEALTH_sub30 )
echo "=== [$V] render.py -> out/CUT_${V}_graded.mp4"
python3 ~/Developer/video-use/helpers/render.py edl.json -o "out/CUT_${V}_graded.mp4" --no-subtitles
echo "=== [$V] build_gfx.py"
python3 build_gfx.py
echo "=== [$V] composite.py -> out/${NAME}.mp4"
python3 composite.py
echo "=== [$V] make_srt.py"
python3 make_srt.py "out/${NAME}.mp4"
echo "=== [$V] DONE"
ffprobe -v error -show_entries format=duration -of csv=p=0 "out/${NAME}.mp4"
