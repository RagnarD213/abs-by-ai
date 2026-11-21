#!/usr/bin/env python3
"""Moved to .claude/skills/_shared/audio/pick_lav.py (2026-09-02). This shim forwards to it.
pick_lav probes EVERY stream and channel (2-channel rolls AND the 8/28 four-mono-track rolls),
cross-correlates all live candidates within +/-20 ms, scores arrival / floor / decay / clipping,
and writes <file>.audio_source.json that every build script reads. "Right channel" is no longer
a rule anywhere -- the lav is whatever measures as the lav on THIS file.
  chancheck.py <file>            # analyse + write the JSON
  chancheck.py <file> --analyse  # print only"""
import os, sys
os.execvp("python3", ["python3", "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/pick_lav.py"] + sys.argv[1:])
