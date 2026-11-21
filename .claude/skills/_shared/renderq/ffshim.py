"""Entry point for the ffmpeg wrapper at Media/video_edit/bin/ffmpeg: `python3 ffshim.py REAL_FFMPEG ARGS...`.
Kept tiny on purpose. If the queue code cannot even load, ffmpeg still runs (ungated) rather than failing a build."""
import os
import sys

real, args = sys.argv[1], sys.argv[2:]
try:
    import renderq
except Exception:
    os.execv(real, [real] + args)
renderq.ffmpeg_main(real, args)
