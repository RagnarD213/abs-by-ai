#!/usr/bin/env python3
"""Mux the square master: the picture, plus the APPROVED 9:16 master's AAC stream COPIED.

The audio is not re-encoded and not re-mixed: it is the stream Dan approved on 2026-09-18 (9:16
master sha256 02d03218...3e51). The md5 of the audio packets is asserted equal before and after.
"""
import hashlib, json, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01-sq")
import ra01lib as L
APPROVED = f"{L.REPO}/Claude Ad Videos/the ai trick that got me abs - RA-01/the ai trick that got me abs | claude | 9x16 | RA-01.mp4"
APPROVED_SHA = "02d032180a3eb42dc81d1857613df55ef4b715ab4d31e315834baf2a63003e51"
OUT = "master_1x1.mp4"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def amd5(p):
    r = subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", p, "-map", "0:a:0", "-c", "copy", "-f", "md5", "-"],
                       capture_output=True, text=True, check=True)
    return r.stdout.strip()

assert sha(APPROVED) == APPROVED_SHA, "the 9:16 in the delivery folder is not the approved file"
subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-i", "picture_1x1.mp4", "-i", APPROVED,
                "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-movflags", "+faststart", OUT], check=True)
a, b = amd5(APPROVED), amd5(OUT)
assert a == b, (a, b)
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared/audio")
import shutil
shutil.copy2("master_9x16.mp4.audio_untreated.json", OUT + ".audio_untreated.json")
pr = subprocess.run([L.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries",
                     "format=duration:stream=codec_name,width,height,nb_frames,r_frame_rate,bit_rate",
                     "-of", "default=nw=1", OUT], capture_output=True, text=True).stdout
json.dump({"approved_9x16_sha256": APPROVED_SHA, "audio_packets_md5_approved": a, "audio_packets_md5_square": b,
           "square_sha256": sha(OUT)}, open("audio_identity.json", "w"), indent=1)
print(OUT, "| audio packets", b, "== approved 9:16"); print(pr)
