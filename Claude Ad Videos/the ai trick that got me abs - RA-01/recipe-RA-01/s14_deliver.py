#!/usr/bin/env python3
"""Mux the master, gate it, and lay the delivery out.  s14_deliver.py mux|review 9x16|16x9"""
import json, os, shutil, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
REPO = L.REPO
DEST = f"{REPO}/Claude Ad Videos/the ai trick that got me abs - RA-01"
NAME = {"9x16": "the ai trick that got me abs | claude | 9x16 | RA-01.mp4",
        "16x9": "the ai trick that got me abs | claude | 16x9 | RA-01.mp4"}
REV  = {"9x16": "the ai trick that got me abs | REVIEW 540p 9x16 | RA-01.mp4",
        "16x9": "the ai trick that got me abs | REVIEW 540p 16x9 | RA-01.mp4"}
AB   = "the ai trick that got me abs | AB audio ref-vs-ours | RA-01.mp4"
MODE, KEY = sys.argv[1], sys.argv[2]
os.makedirs(DEST, exist_ok=True)

if MODE == "mux":
    out = f"master_{KEY}.mp4"
    subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-i", f"picture_{KEY}.mp4",
                    "-i", "mix.wav", "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
                    "-movflags", "+faststart", out], check=True)
    # carry the do-no-harm baseline the voice chain recorded, onto the file the gate measures
    sys.path.insert(0, f"{REPO}/.claude/skills/_shared/audio")
    import common as AC
    AC.carry_untreated("mix.wav", out)
    pr = subprocess.run([L.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries",
                         "format=duration:stream=width,height,nb_frames,r_frame_rate,codec_name",
                         "-of", "default=nw=1", out], capture_output=True, text=True).stdout
    print(out); print(pr)

elif MODE == "review":
    src = f"{DEST}/{NAME[KEY]}"
    h = 540 if KEY == "16x9" else 960
    vf = "scale=960:540" if KEY == "16x9" else "scale=540:960"
    subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-i", src, "-vf", vf,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "24",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
                    f"{DEST}/{REV[KEY]}"], check=True)
    print(f"{DEST}/{REV[KEY]}")
