#!/bin/zsh
# REV 6 delivery gates + copies, run on the EXACT finished master. PARAMETERISED (rev 6 ships TWO masters):
#   ./deliver.sh website_video_16x9_A_tan-corrected.mp4      ./deliver.sh website_video_16x9_B_tan-as-is.mp4
#   1 the audio gate (_shared/audio/audio_gate.py) + the A/B clip     2 contact sheet from EXACT -ss grabs (lesson 94)
#   3 qc.py (14 checks + caption clearance in pixels + hair on the delivered frames)   4 watch.py   5 540p review copy
#   6 silent-seconds check on master + review copy.  Every gate is per-file (the stamp is keyed to the file's sha256).
set -e
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
# Whisper thread-thrashes on a loaded box (12 % CPU, 2 min CPU in 20 min wall); capped at 6 it runs ~4x faster
export OMP_NUM_THREADS=6 MKL_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6
cd /Volumes/Extreme/_edit_work/website-video-828
M=${1:-website_video_16x9.mp4}; TAG=${M#website_video_16x9}; TAG=${TAG%.mp4}     # "" | "_A_tan-corrected" | "_B_tan-as-is"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
echo "== 1 audio gate (the shared gate, on the EXACT delivered file $M)"
python3 "$SH/audio_gate.py" $M --ab AB_his-vs-ours$TAG.mp4 && echo "audio gate PASSED"
echo "== 1.5 stamp"; python3 "$SH/require_stamp.py" $M
echo "== 2 contact sheet, exact grabs every 5 s"; python3 sheet.py $M pv/final_sheet_5s$TAG.jpg 5
echo "== 3 qc"; rm -f qc.whisper.json; QCIN=$M python3 qc.py
echo "== 4 watch"; rm -rf watch; python3 watch.py $M
cp pv/hair_tight*.png pv/hair_loose*.png pv/hairgate_sheet.jpg pv/hairtrack_proof.jpg watch/strip/ 2>/dev/null || true
rm -rf watch$TAG; [ -n "$TAG" ] && mv watch watch$TAG || true
echo "== 5 review copy"; ffmpeg -v error -y -i $M -vf scale=960:540 -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart REVIEW_540p_website_video$TAG.mp4
echo "== 6 silence"; for f in $M REVIEW_540p_website_video$TAG.mp4; do
  n=$(ffmpeg -nostats -i $f -af silencedetect=n=-50dB:d=1 -f null - 2>&1 | grep -c silence_start || true)
  echo "  $f: $n silent run(s) >= 1 s at -50 dB"; done
echo "DELIVERY GATES DONE $M"
