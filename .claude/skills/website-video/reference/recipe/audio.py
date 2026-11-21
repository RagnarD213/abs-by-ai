#!/usr/bin/env python3
"""SUPERSEDED (2026-09-02). This was the rev-1 website-video chain Dan rejected on floor (bed at
-23 dB + 3:1 compressor with makeup + two air shelves buried the gaps 9.5 dB under his) and, in
audio2.py, the measured-gain + alimiter finish that replaced loudnorm. Both lessons live in
.claude/skills/_shared/audio/voice_chain.py, which is the one chain now. git history has the code.
Same env interface as audio3.py; this shim forwards to it."""
import os, sys
os.execvp("python3", ["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio3.py")] + sys.argv[1:])
