#!/bin/bash
cd /Volumes/Extreme/_edit_work/sl06/round3/yt/raw
Y=~/.cache/absbyai/ytdlp/yt-dlp_macos; FFD="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
dl(){ if [ -n "$2" ]; then $Y -q --no-warnings --js-runtimes node --ffmpeg-location "$FFD" -f "bv*[height<=360]+ba/b[height<=360]" --merge-output-format mp4 --download-sections "*$2" -o "$1_s.%(ext)s" "https://www.youtube.com/watch?v=$1"; else $Y -q --no-warnings --js-runtimes node --ffmpeg-location "$FFD" -f "bv*[height<=360]+ba/b[height<=360]" --merge-output-format mp4 -o "$1_s.%(ext)s" "https://www.youtube.com/watch?v=$1"; fi; echo "$1 rc=$?"; sleep 3; }
dl d1aG2dvI6NU; dl 4RNrMEdZrYo; dl ukVsKSf14XI; dl 4v3kQNFLID8; dl GncFgoqRmwo
echo DONE
