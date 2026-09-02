#!/bin/zsh
# REV 2 delivery gates + copies, run on the EXACT finished master (website_video_16x9.mp4):
#   1 the audio gate (voice_ref_check.py) + the A/B clip     2 contact sheet at 1 frame / 5 s
#   3 qc.py   4 watch.py   5 540p review copy   6 silent-seconds check on master + review copy
set -e
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
cd /Volumes/Extreme/_edit_work/website-video-828
SK="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/ad-edit/reference"
M=website_video_16x9.mp4
AUD="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
echo "== 1 audio gate (stamps the master; qc.py and step 5 refuse without it)"; python3 "$AUD/audio_gate.py" $M --ab AB_his-vs-ours.mp4
echo "== 2 contact sheet 1/5s"; ffmpeg -v error -y -i $M -vf "fps=1/5,scale=384:-1,drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='%{pts\:hms}':x=4:y=4:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=6x8" -frames:v 1 pv/final_sheet_5s.jpg
echo "== 3 qc"; rm -f qc.whisper.json; python3 qc.py
echo "== 4 watch"; rm -rf watch; python3 watch.py $M
echo "== 4.5 stamp"; python3 "$AUD/require_stamp.py" $M
echo "== 5 review copy"; ffmpeg -v error -y -i $M -vf scale=960:540 -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart REVIEW_540p_website_video.mp4
echo "== 6 silence"; for f in $M REVIEW_540p_website_video.mp4; do
  n=$(ffmpeg -nostats -i $f -af silencedetect=n=-50dB:d=1 -f null - 2>&1 | grep -c silence_start || true)
  echo "  $f: $n silent run(s) >= 1 s at -50 dB"; done
echo "DELIVERY GATES DONE"
