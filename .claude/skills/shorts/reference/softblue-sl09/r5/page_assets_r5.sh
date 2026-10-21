#!/bin/zsh
cd /Volumes/Extreme/_edit_work/sl09/round2
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
REV="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/oura-ring-review REVIEW"
DEL="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content"
K=oura-short4_youre-not-sleeping-as-well-as-you-think
cat "$REV/$K - REVIEW 540p.mp4" > "review/shorts/R5 $K - REVIEW 540p.mp4"; cat "$REV/AB_film-vs-short_$K.mp4" > "review/shorts/R5 AB_film-vs-short_$K.mp4"
cut() { "$FF" -nostdin -v error -y -ss $2 -i "$REV/$1 - REVIEW 540p.mp4" -t $3 -c:v libx264 -crf 20 -preset veryfast -c:a aac -b:a 128k -movflags +faststart "review/context/$4"; }
cut $K 0 5.80 "R5_K_k1-context - REVIEW 540p.mp4"; cut $K 0 2.80 "R5_K_k1-alone - REVIEW 540p.mp4"
"$FF" -nostdin -v error -y -ss 1.60 -i "$DEL/$K.mp4" -frames:v 1 -vf "scale=in_color_matrix=bt709:in_range=tv" -q:v 2 "review/stills/R5_K_k1.jpg"
echo ASSETS_DONE
