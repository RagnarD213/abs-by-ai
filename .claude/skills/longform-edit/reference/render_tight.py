#!/usr/bin/env python3
"""Render the tightened, punched-in picture + its matching clean voice.

Per-piece rather than one 85-branch filter_complex: referencing [0:v] 85 times makes
ffmpeg split the decoded stream 85 ways and buffer every branch until concat gets to
it, which is a memory cliff on a 9-minute 1080p source. Each piece is encoded on its
own (so the job is resumable and parallel) and then joined with the concat demuxer,
which is lossless.

Video and audio for a piece are cut in the SAME command from the same -ss/-t, so a
piece can never drift internally, and every duration is snapped to a whole frame so
they cannot drift cumulatively either.
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

FF   = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
FFP  = FF.replace("ffmpeg","ffprobe")
B    = Path("/Volumes/Extreme/_edit_work/abwheel")
R2   = B / "r2"
VID  = B / "roughcuts" / "CUT_v2_graded.mp4"
AUD  = R2 / "audio" / "voice_raw.wav"
OUT  = R2 / "tight.mov"
PIECES = R2 / "pieces"; PIECES.mkdir(exist_ok=True)
FD   = 1001/30000
FPS  = "30000/1001"

P = json.load(open(R2/"plan.json"))["framed"]

def vf_for(f):
    k = f["crop"]
    if k >= 0.999: return "scale=1920:1080:flags=lanczos,setsar=1"
    cw = int(1920*k)//2*2; ch = int(1080*k)//2*2
    x = int(min(max(f["cx"]*1920 - cw/2, 0), 1920-cw))
    y = int(min(max(f["cy"]*1080 - ch/2, 0), 1080-ch))
    return f"crop={cw}:{ch}:{x}:{y},scale=1920:1080:flags=lanczos,setsar=1"

def one(i):
    f = P[i]
    # EXACT frame count, not -t. With `-t d` ffmpeg emits ceil() frames on some pieces
    # and floor() on others: 27 of these 85 came out one frame long, which drifted the
    # audio 0.9 s behind the picture by the end of the concat. `-frames:v N` on the
    # video and an `atrim` of exactly N frames' worth on the audio makes both streams
    # the same length by construction.
    n = int(round((f["b"]-f["a"])/FD))
    d = n * FD
    dst = PIECES / f"p{i:03d}.mov"
    if dst.exists() and dst.stat().st_size > 1000: return dst, d
    cmd = [FF,"-nostdin","-v","error","-y","-ss",f"{f['a']:.6f}","-i",str(VID),
           "-ss",f"{f['a']:.6f}","-i",str(AUD),
           "-vf",vf_for(f),"-af",f"atrim=end={d:.6f},asetpts=N/SR/TB",
           "-map","0:v","-map","1:a","-frames:v",str(n),
           "-c:v","libx264","-preset","medium","-crf","16","-pix_fmt","yuv420p",
           "-r",FPS,"-c:a","pcm_s24le","-ar","48000",str(dst)]
    r = subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: raise SystemExit(f"piece {i} failed: {r.stderr[-400:]}")
    return dst, d

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=6) as ex:
        res = list(ex.map(one, range(len(P))))
    lst = R2/"pieces.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p,_ in res))
    subprocess.run([FF,"-nostdin","-v","error","-y","-f","concat","-safe","0","-i",str(lst),
                    "-c","copy",str(OUT)],check=True)
    def dur(p,sel):
        return float(subprocess.run([FFP,"-v","error","-select_streams",sel,"-show_entries",
            "stream=duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip())
    dv, da = dur(OUT,"v:0"), dur(OUT,"a:0")
    plan = sum(d for _,d in res)
    print(f"{len(res)} pieces -> {OUT.name}   video {dv:.3f}s  audio {da:.3f}s  plan {plan:.3f}s")
    print(f"  a/v drift {da-dv:+.3f}s   vs plan {dv-plan:+.3f}s")
    assert abs(da-dv) < 0.10, "audio/video drift"
