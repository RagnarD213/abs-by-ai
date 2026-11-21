#!/bin/zsh
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
cd /Volumes/Extreme/_edit_work/website-video-828
for r in C1650 C1651; do
  python3 whisper_chunked.py audio/$r.16k.wav tx/$r.whisper.json small 70 60 2>&1 | grep -v -i warning
done
echo TX DONE
