#!/usr/bin/env python3
"""Moved to .claude/skills/_shared/audio/voice_chain.py (2026-09-02) -- this WAS the approved chain
(rev 2, "you got it nailed") and it is now the one chain every skill uses, with the EQ fitted per
roll instead of the rev-2 curve pasted in. Same env interface, translated:
  VIN=<video-or-wav> VOUT=<out> [MUSIC_DB=-30|none] [COMP=0|1] [TARGET_I=-14] python3 audio3.py
The source must carry <VIN>.audio_source.json from pick_lav.py (a WAV input is taken as the lav)."""
import os, sys
a = ["python3", "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py", "--in", os.environ.get("VIN", "nocap.mov"),
     "--out", os.environ.get("VOUT", "nocap_audio.mov"), "--target", os.environ.get("TARGET_I", "-14")]
m = os.environ.get("MUSIC_DB", "-30")
if m.lower() not in ("none", "off", ""):
    a += ["--bed", os.environ.get("MUSIC", "/Volumes/Extreme/_edit_work/ad1-8-14/rev5/music/acoustic_bg.mp3"), "--bed-db", m]
if os.environ.get("COMP", "0") == "1": a.append("--comp")
os.execvp("python3", a + sys.argv[1:])
