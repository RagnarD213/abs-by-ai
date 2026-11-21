#!/bin/zsh
# Render 11 (= 10 + the post-unsharp trim, zgrade4.py): Dan rejected render 9's COLOUR (2026-09-13, VLC side by side: "Muhammad's look brighter, like the colors are
# more vivid. I look more tan."). Root cause: his file has no colour tags; ffmpeg reads untagged video as BT.601, VLC and
# browsers read untagged HD as BT.709, and the grade was fitted to the 601 reading. zlut.py now reads 709 (base rebuilt),
# zgrade2.py --post matches each channel after the vignette, zgrade3.py matches his grade section by section (his opening
# 0-43 s is warmer than the rest). Also: the "Real picture of me" label moved OFF HIS BODY on all four stills (Dan 09-12).
# EDL, crop and captions are unchanged from render 9.
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ad3-vert
while true; do n=$(for p in $(pgrep -f "whisper|ffmpeg|render|zbase|scan.py"); do lsof -a -p $p -d cwd -Fn 2>/dev/null | grep ^n | cut -c2-; done | grep -v ad3-vert | grep -E "_edit_work|Abs By AI" | sort -u | wc -l); [ $n -lt 2 ] && break; echo "waiting: $n other builds"; sleep 30; done
echo "master14 start $(date)"
render_chunk () {
  python3 render3.py --from $1 --to $2 --out picture_$1.mp4 > logs/render14_$1.log 2>&1 \
    && echo "chunk $1-$2 ok $(date)" || { echo "CHUNK $1 FAILED"; tail -5 logs/render14_$1.log; exit 1; }
}
render_chunk 0 2845    || exit 1
render_chunk 2845 5640 || exit 1
render_chunk 5640 7948 || exit 1
ffmpeg -nostdin -v error -y -f concat -safe 0 -i cat12.txt -c copy picture.mp4 || { echo CONCAT FAILED; exit 1; }
python3 zmux.py > logs/mux14.log 2>&1 && cat logs/mux14.log || { echo MUX FAILED; tail logs/mux14.log; exit 1; }
echo "MASTER14 DONE $(date)"
