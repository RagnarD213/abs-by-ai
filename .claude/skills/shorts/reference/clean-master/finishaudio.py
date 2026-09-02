#!/usr/bin/env python3
"""FINISH STAGE = the shared chain, per short (2026-09-02). Replaces the per-batch tone-match.

render.js writes lossless out/<id>_<slug>.mov whose audio is the LAV TRACK pulled per the source's
audio_source.json (pick_lav) -- no EQ, no pan. This stage runs, on each .mov:
  pick_lav      proves the intermediate is one signal (dual-mono) and refuses if it is not
  voice_chain   dereverb if the room measures > 55 ms, EQ fitted to Muhammad's ad on the gate's own
                metric, expander, centred stereo, measured gain + alimiter -> -14 LUFS (never loudnorm)
  audio_gate    the nine rows on the delivered .mp4, and the STAMP qc.js and deliver.js require
Video is copied, never re-encoded. This is the only AAC encode.
  python3 finishaudio.py [IDS...]"""
import json, os, subprocess, sys
A = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
segs = json.loads(subprocess.check_output(['node', '-e',
  "const {SEGMENTS}=require('./segments.js');console.log(JSON.stringify(SEGMENTS.map(s=>[s.id,s.slug])))"]).decode())
only = [a.upper() for a in sys.argv[1:]]; bad = 0
for sid, slug in segs:
    if only and sid not in only: continue
    mov = f"out/{sid.lower()}_{slug}.mov"; mp4 = mov[:-4] + ".mp4"
    if not os.path.exists(mov): print(f"{sid}: no {mov} -- run render.js first"); continue
    print(f"\n=== {sid} {slug}")
    if subprocess.run(["python3", f"{A}/pick_lav.py", mov]).returncode: bad += 1; continue
    if subprocess.run(["python3", f"{A}/voice_chain.py", "--in", mov, "--out", mp4, "--work", f"work/_vc_{sid.lower()}"]).returncode: bad += 1; continue
    if subprocess.run(["python3", f"{A}/audio_gate.py", mp4]).returncode: bad += 1
print("\nFINISH", "OK" if not bad else f"{bad} FAILURE(S) -- not deliverable"); sys.exit(1 if bad else 0)
