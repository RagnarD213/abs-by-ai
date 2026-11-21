#!/bin/zsh
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
HIS=/Volumes/Extreme/_edit_work/ad3-vert/ref/ad3_v6hd.mp4
cd /Volumes/Extreme/_edit_work/ad3-169patch
"$FF" -nostdin -v error -y -i $HIS -i patch.mkv -filter_complex \
 "[0:v]trim=start_frame=0:end_frame=2202,setpts=PTS-STARTPTS[a];[0:v]trim=start_frame=2339,setpts=PTS-STARTPTS[c];[1:v]setpts=PTS-STARTPTS[b];[a][b][c]concat=n=3:v=1:a=0,setsar=1[v]" \
 -map "[v]" -map 0:a:0 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 30000/1001 \
 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a copy -movflags +faststart ad3_169_smokefix.mp4 && echo ENCODED
