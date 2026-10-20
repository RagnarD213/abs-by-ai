#!/bin/zsh
# R4 page media: whole-short review copies, A/B clips, each new clip alone and in context, a full-quality still of each
cd /Volumes/Extreme/_edit_work/sl09/round2
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
REV="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/oura-ring-review REVIEW"
DEL="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content"
K=oura-short4_youre-not-sleeping-as-well-as-you-think; J=oura-short5_oura-ring-or-whoop-which-one-to-buy
for n in $K $J; do cat "$REV/$n - REVIEW 540p.mp4" > "review/shorts/R4 $n - REVIEW 540p.mp4"; cat "$REV/AB_film-vs-short_$n.mp4" > "review/shorts/R4 AB_film-vs-short_$n.mp4"; done
cut() { "$FF" -nostdin -v error -y -ss $2 -i "$REV/$1 - REVIEW 540p.mp4" -t $3 -c:v libx264 -crf 20 -preset veryfast -c:a aac -b:a 128k -movflags +faststart "review/context/$4"; }
cut $K 0 7.30 "R4_K_k1-context - REVIEW 540p.mp4"; cut $K 0 4.30 "R4_K_k1-alone - REVIEW 540p.mp4"
cut $J 0 6.70 "R4_J_j1-context - REVIEW 540p.mp4"; cut $J 0 3.70 "R4_J_j1-alone - REVIEW 540p.mp4"
cut $J 13.32 10.27 "R4_J_j2-context - REVIEW 540p.mp4"; cut $J 16.32 4.27 "R4_J_j2-alone - REVIEW 540p.mp4"
st() { "$FF" -nostdin -v error -y -ss $2 -i "$DEL/$1.mp4" -frames:v 1 -vf "scale=in_color_matrix=bt709:in_range=tv" -q:v 2 "review/stills/$3.jpg"; "$FF" -nostdin -v error -y -i "review/stills/$3.jpg" -vf scale=540:960 -q:v 3 "review/stills/$3_sm.jpg"; }
st $K 2.20 R4_K_k1; st $J 1.90 R4_J_j1; st $J 18.40 R4_J_j2
echo ASSETS_DONE
