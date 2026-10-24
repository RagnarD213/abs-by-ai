#!/bin/zsh
# remux.sh S NAME : swap the short's audio for build/S/audio.wav without touching the picture (frame counts asserted)
S=$1; N=$2; FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FP="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffprobe"
V=build/$S/$N.mp4; n0=$("$FP" -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 "$V")
"$FF" -nostdin -v error -y -i "$V" -i build/$S/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac_at -b:a 320k -movflags +faststart build/$S/_remux.mp4 || exit 1
n1=$("$FP" -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 build/$S/_remux.mp4)
[ "$n0" = "$n1" ] || { echo "frame count changed $n0 -> $n1"; exit 1; }
mv build/$S/_remux.mp4 "$V"; echo "$S remuxed, $n1 frames, $("$FP" -v error -show_entries format=duration -of csv=p=0 "$V") s"
