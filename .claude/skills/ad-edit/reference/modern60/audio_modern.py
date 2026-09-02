#!/usr/bin/env python3
"""SUPERSEDED by .claude/skills/_shared/audio/voice_chain.py (2026-09-02).
This script built the voice chain + ducked bed + sfxlib transition SFX + two-pass loudnorm for its
batch. The chain and the finish are now the shared module (fitted EQ, dereverb when the room
measures wet, measured gain + alimiter -- loudnorm went DYNAMIC on the website video and is banned).
Batch-specific SFX cues are still the skill's job: build them with _shared/sfxlib.py into one WAV and
pass it as --extra; the bed goes in as --bed/--bed-db. git history has the old code.
  python3 voice_chain.py --in <tight cut> --out <out.mov> --bed music.mp3 --bed-db -30 --extra sfxbed.wav
then audio_gate.py on the delivered file."""
import os, sys
os.execvp("python3", ["python3", "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py"] + sys.argv[1:])
