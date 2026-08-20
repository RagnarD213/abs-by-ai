#!/usr/bin/env python3
"""Validate an SRT against the FINISHED render's own audio (longform-edit Step 8).
Never validate against the source transcript - that only proves the mapping matches
itself. Samples N windows, re-transcribes each from the delivered file, and measures
token overlap with the SRT text covering the same window.
usage: srt_validate.py <slug> <video.mp4> <file.srt> [n_windows]"""
import json, re, subprocess, sys, random
from pathlib import Path
slug, vid, srtname = sys.argv[1], sys.argv[2], sys.argv[3]
N = int(sys.argv[4]) if len(sys.argv) > 4 else 12
B = Path(f"/Volumes/Seagate 4TB/_edit_work/{slug}")
V = B / "roughcuts" / vid
def secs(s):
    return sum(float(x)*m for x, m in zip(re.split('[:,]', s), [3600, 60, 1, .001]))
cues = []
for blk in open(B / "roughcuts" / srtname).read().strip().split("\n\n"):
    L = blk.split("\n"); a, b = [secs(x) for x in L[1].split(" --> ")]
    cues.append((a, b, " ".join(L[2:])))
dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
    "-of","csv=p=0",str(V)],capture_output=True,text=True).stdout.strip())
import whisper
m = whisper.load_model("small")
random.seed(11)
starts = [10 + i*(dur-50)/N for i in range(N)]
norm = lambda t: set(re.findall(r"[a-z0-9']+", t.lower()))
scores = []
for st in starts:
    w = B / "_srtval.wav"
    subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-ss",f"{st:.2f}","-i",str(V),
        "-t","30","-vn","-ac","1","-ar","16000",str(w)],check=True)
    heard = norm(m.transcribe(str(w), fp16=False, language="en")["text"])
    said = norm(" ".join(t for a,b,t in cues if b > st and a < st+30))
    w.unlink(missing_ok=True)
    if not heard: continue
    ov = len(heard & said)/len(heard)
    scores.append(ov)
    print(f"  t={int(st//60):02d}:{int(st%60):02d}  overlap {ov*100:5.1f}%  "
          f"{'OK' if ov>=0.75 else 'LOW'}")
good = sum(1 for s in scores if s >= 0.75)
print(f"\n{good}/{len(scores)} windows >=75% overlap, mean {sum(scores)/len(scores)*100:.1f}%")
print("SRT ALIGNED" if good == len(scores) else "SRT NEEDS REVIEW")
