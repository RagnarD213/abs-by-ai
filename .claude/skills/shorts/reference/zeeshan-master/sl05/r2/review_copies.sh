#!/bin/zsh
# 540p phone review copies of the delivered SL-05 shorts: r2/review_copies.sh [short1_... names]
cd "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
mkdir -p "stop-deadlifting REVIEW"
for f in stop-deadlifting-short*.mp4; do
  n=${f:r}; [[ $# -gt 0 && ! " $* " == *" ${n#stop-deadlifting-} "* ]] && continue
  nice -n 20 "$FF" -v error -y -i "$f" -vf "scale=540:960:flags=lanczos" -c:v libx264 -preset fast -crf 22 -pix_fmt yuv420p -c:a copy -movflags +faststart "stop-deadlifting REVIEW/REVIEW_540p_$f" && echo "REVIEW_540p_$f"
done
