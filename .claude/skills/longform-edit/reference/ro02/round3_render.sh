#!/bin/zsh
# Round 3: every segment cached + first-frame scan, cutaway scan, then the whole film.
set -e
cd /Volumes/Extreme/_edit_work/ro02
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
echo "MARK dupscan $(date +%H:%M)"; nice -n 10 python3 recipe/dupscan.py
echo "MARK clipscan $(date +%H:%M)"; python3 recipe/clipscan.py
echo "MARK render $(date +%H:%M)"
nice -n 10 python3 -c "
import sys; sys.path.insert(0,'recipe'); sys.argv=['x']; import build
print('same-size joins', build.jumps()); assert not build.jumps()
build.render_range(0, build.S[-1]['out_f1']/build.FPS, 'round3/RO02_MASTER.mp4')"
echo "MARK RENDER DONE $(date +%H:%M)"
