#!/bin/zsh
# RO-20 round 4: picture renders, one lane per call (behind the two-build cap). usage: chain_r4_picture.sh v1 v2
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ro20
for v in "$@"; do
  python3 -c 'import sys; sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"); import buildcap; buildcap.wait("RO-20 R4 picture '$v'")'
  echo "START $v $(date)"; mkdir -p round4/$v
  nice -n 5 python3 recipe/films_r4.py picture $v > round4/$v/picture.log 2>&1 && echo "PICTURE DONE $v $(date)" || { echo "PICTURE FAILED $v"; tail -5 round4/$v/picture.log; }
done
