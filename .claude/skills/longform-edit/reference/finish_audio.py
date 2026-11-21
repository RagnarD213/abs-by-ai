#!/usr/bin/env python3
"""Moved to .claude/skills/_shared/audio/voice_chain.py (2026-09-02). This was the spray-tan rev-2
finish (fitted EQ + gate + 3:1 compressor + two-pass loudnorm). The shared chain fits the EQ per
roll the same way, runs the compressor OFF by default (his LRA is 3.5), and finishes with measured
gain + alimiter because loudnorm went DYNAMIC on the website video. git history has the old code.
  VOICE=voice_raw.wav VIDEO=CUT_v3_gfx.mp4 OUT=FINAL.mp4 python3 finish_audio.py
then audio_gate.py on OUT."""
import os, sys
os.execvp("python3", ["python3", "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py", "--in", os.environ.get("VOICE", "voice_raw.wav"),
                      "--video", os.environ.get("VIDEO", "roughcuts/CUT_v3_gfx.mp4"),
                      "--out", os.environ.get("OUT", "roughcuts/FINAL.mp4")] + sys.argv[1:])
