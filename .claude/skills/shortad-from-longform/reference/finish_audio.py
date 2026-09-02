#!/usr/bin/env python3
"""The finish for the "reference's own mix" path (Dan-approved, 2026-08-27): ONE constant gain +
alimiter, NEVER loudnorm (it went DYNAMIC on the Ad-1 vertical and Dan heard the bed swell 9 dB in
every gap). Now the shared module's finish stage:  voice_chain.py --finish-only
  python3 finish_audio.py [audio.wav] [audio_final.wav]
Then audio_gate.py on the DELIVERED .mp4 -- his mix passes the reference rows by construction, and
the gate adds loudness, true peak, silence and length, and writes the stamp qc.py check 17 needs.
gain_flatness.py stays as the per-second one-sided check on top."""
import os, sys
src = sys.argv[1] if len(sys.argv) > 1 else "audio.wav"; out = sys.argv[2] if len(sys.argv) > 2 else "audio_final.wav"
os.execvp("python3", ["python3", "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py", "--finish-only", "--in", src, "--out", out])
