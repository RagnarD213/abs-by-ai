#!/bin/zsh
# Exact portrait crops of the approved master. Each clip gets a 0.25 s held tail
# so frame rounding can never wrap to its first frame during a kit beat.
set -e
B="/Volumes/Extreme/_edit_work/kit9x16/ad10-master"
M="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/my dad bod at 38 my dad bod at 40 | muhammad | 16x9 | ad 10.mp4"
F="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
mkdir -p "$B/assets_ad10"

make_clip() {
  local name="$1" start="$2" dur="$3"
  "$F" -nostdin -v error -y -ss "$start" -t "$dur" -i "$M" -an \
    -vf "crop=608:1080:656:0,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.25" \
    -r 30000/1001 -c:v libx264 -preset medium -crf 16 -pix_fmt yuv420p \
    -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
    "$B/assets_ad10/$name.mp4"
}

make_clip app1_before 121.822 1.001
make_clip app1_form 122.823 2.735
make_clip app2_before 172.839 1.035
make_clip app2_form 173.874 2.835

# The source phone sequence animates its disclosure on late and off early. Use
# its first fully opaque, readable disclosure frame as an intentional still so
# the physique is labeled continuously for the entire phone-goal card.
"$F" -nostdin -v error -y -ss 93.726967 -i "$M" -an \
  -vf "crop=608:1080:656:0" -frames:v 1 \
  "$B/assets_ad10/phone_goal_labeled.png"

# Only the clean 151.585-155.550 food action is used. Stretch those frames
# gently across the 5.005-second card instead of freezing the last frame or
# leaking into the following look-down/refrigerator shot.
"$F" -nostdin -v error -y -ss 151.585 -t 3.965 -i "$M" -an \
  -vf "setpts=1.262295082*(PTS-STARTPTS)" -frames:v 150 \
  -r 30000/1001 -c:v libx264 -preset medium -crf 16 -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  "$B/assets_ad10/food_snap_hold.mp4"
