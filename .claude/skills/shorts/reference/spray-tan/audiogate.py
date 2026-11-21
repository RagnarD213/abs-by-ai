#!/usr/bin/env python3
"""Moved to .claude/skills/_shared/audio/audio_gate.py (2026-09-02). The EDT (room) row this file
introduced is now row 2 of the one gate, next to comb, tone, floor, dryness, loudness, spread,
true peak, silence and length -- and the gate STAMPS the file, which qc.js and deliver.js require.
  audiogate.py [IDS...]   gates out/<id>_<slug>.mp4 for the batch's segments.js"""
import json, os, subprocess, sys
segs = json.loads(subprocess.check_output(['node', '-e',
  "const {SEGMENTS}=require('./segments.js');console.log(JSON.stringify(SEGMENTS.map(s=>[s.id,s.slug])))"]).decode())
only = [a.upper() for a in sys.argv[1:]]; bad = 0
for sid, slug in segs:
    if only and sid not in only: continue
    f = f"out/{sid.lower()}_{slug}.mp4"
    if not os.path.exists(f): print(f"{sid}: missing {f}"); bad += 1; continue
    bad += subprocess.run(["python3", "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py", f]).returncode != 0
print("\nAUDIO GATE", "PASS" if not bad else f"{bad} FAILURE(S)"); sys.exit(1 if bad else 0)
