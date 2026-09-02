#!/usr/bin/env python3
"""SUPERSEDED by .claude/skills/_shared/audio/voice_chain.py (2026-09-02). This script fitted or
audited a per-batch EQ chain against Muhammad's cut; the shared chain now fits the EQ per file on
the gate's own metric (10 bands, 20-140 s, speech frames), dereverbs when the room measures wet,
and finishes with measured gain + alimiter. finishaudio.py runs it on every rendered short.
git history has the old code and its measurements."""
import os, sys
os.execvp("python3", ["python3", "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py"] + sys.argv[1:])
