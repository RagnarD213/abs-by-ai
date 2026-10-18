#!/bin/bash
mkdir -p /Volumes/Extreme/_edit_work/sl06/round3/yt/hd; cd /Volumes/Extreme/_edit_work/sl06/round3/yt/hd
Y=~/.cache/absbyai/ytdlp/yt-dlp_macos; FFD="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
dl(){ $Y -q --no-warnings --js-runtimes node --ffmpeg-location "$FFD" -f "bv*[height<=1920][vcodec^=avc1]+ba[ext=m4a]/bv*[height<=1920]+ba/b" --merge-output-format mp4 --download-sections "*$2" --force-keyframes-at-cuts -o "$1_$3.%(ext)s" "https://www.youtube.com/watch?v=$1"; echo "$1 rc=$?"; sleep 3; }
dl HcAsUbiFJyw 2:14-2:36 karli; dl Pz49hyOla6s 6:08-6:27 nursescott; dl 4v3kQNFLID8 0:38-0:54 clinical; dl Ynv8qapLCmk 1:08-1:25 krummen
echo DONE
