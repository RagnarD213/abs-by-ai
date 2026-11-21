#!/bin/bash
mkdir -p /Volumes/Extreme/_edit_work/sl06/round3/yt/hd; cd /Volumes/Extreme/_edit_work/sl06/round3/yt/hd
Y=~/.cache/absbyai/ytdlp/yt-dlp_macos; FFD="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
dl(){ $Y -q --no-warnings --js-runtimes node --ffmpeg-location "$FFD" -f "bv*[height<=2160][vcodec^=avc1]+ba[ext=m4a]/bv*[height<=2160]+ba/b" --merge-output-format mp4 --download-sections "*$2" --force-keyframes-at-cuts -o "$1_$3.%(ext)s" "https://www.youtube.com/watch?v=$1"; echo "$1 rc=$?"; sleep 3; }
dl FeweDb3Xfxg 1:34-1:48 synergenx; dl e0wDPZ0D9Wk 5:55-6:06 uiowa; dl 7TP0rTlQVao 6:55-7:05 seattle
echo DONE
