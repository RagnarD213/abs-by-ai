#!/usr/bin/env python3
"""Moved to .claude/skills/_shared/audio/audio_gate.py (2026-09-02). This shim keeps old calls working.
The gate now also measures the ROOM (early decay), comb ripple, loudness, true peak, silence and
length, and STAMPS the file; every QC and deliver script requires that stamp. Same args:
  voice_ref_check.py <mix> [--ref x.mp4] [--ab out.mp4]"""
import os, sys
os.execvp("python3", ["python3", "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py"] + sys.argv[1:])
