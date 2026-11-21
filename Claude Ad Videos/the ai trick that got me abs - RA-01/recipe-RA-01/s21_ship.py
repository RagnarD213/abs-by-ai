#!/usr/bin/env python3
"""Lay the delivery out under the exact names the plan gives.  s21_ship.py"""
import json, os, shutil, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
REPO = L.REPO
DEST = f"{REPO}/Claude Ad Videos/the ai trick that got me abs - RA-01"
os.makedirs(DEST, exist_ok=True)
PAIRS = [("master_9x16.mp4", "the ai trick that got me abs | claude | 9x16 | RA-01.mp4"),
         ("master_16x9.mp4", "the ai trick that got me abs | claude | 16x9 | RA-01.mp4"),
         ("AB_ref-vs-ours.mp4", "the ai trick that got me abs | AB audio ref-vs-ours | RA-01.mp4"),
         ("notes-RA-01.md", "notes-RA-01.md"),
         ("measurements-RA-01.json", "measurements-RA-01.json")]
for src, dst in PAIRS:
    if not os.path.exists(src):
        print(f"  MISSING {src}"); continue
    shutil.copy2(src, f"{DEST}/{dst}")
    for ext in (".audio_gate.json", ".deliver_gate.json", ".audio_untreated.json"):
        if os.path.exists(src + ext):
            shutil.copy2(src + ext, f"{DEST}/{dst}{ext}")
    print(f"  {dst}")
if os.path.isdir("recipe-RA-01"):
    shutil.rmtree(f"{DEST}/recipe-RA-01", ignore_errors=True)
    shutil.copytree("recipe-RA-01", f"{DEST}/recipe-RA-01")
    print("  recipe-RA-01/")
print(DEST)
