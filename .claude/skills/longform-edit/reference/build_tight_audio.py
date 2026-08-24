#!/usr/bin/env python3
"""Cut the clean voice to the plan in ONE sample-accurate pass, then mux it to the
already-concatenated picture.

Cutting audio inside each video piece looked simpler and was wrong twice: with `-t` the
video came out 27 frames long, and with `-frames:v` + a per-piece `atrim` the audio came
out 1.109 s short (~13 ms a piece). Both are per-piece rounding, and per-piece rounding
is exactly what accumulates over 85 pieces. Doing the whole audio in one graph -- 85
atrims off a single asplit, concatenated -- has no per-piece boundary to round at, and
every atrim is expressed in the SAME frame-snapped durations the picture actually got.
"""
import json, subprocess
from pathlib import Path
FF  = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
FFP = FF.replace("ffmpeg","ffprobe")
R2  = Path("/Volumes/Extreme/_edit_work/abwheel/r2")
FD  = 1001/30000
P   = json.load(open(R2/"plan.json"))["framed"]

parts = [f"[0:a]asplit={len(P)}" + "".join(f"[s{i}]" for i in range(len(P)))]
cat = ""
for i, f in enumerate(P):
    n = int(round((f["b"]-f["a"])/FD)); d = n*FD
    parts.append(f"[s{i}]atrim=start={f['a']:.6f}:end={f['a']+d:.6f},asetpts=PTS-STARTPTS[a{i}]")
    cat += f"[a{i}]"
fc = ";".join(parts) + f";{cat}concat=n={len(P)}:v=0:a=1[aout]"
subprocess.run([FF,"-nostdin","-v","error","-y","-i",str(R2/"audio"/"voice_raw.wav"),
                "-filter_complex",fc,"-map","[aout]","-c:a","pcm_s24le","-ar","48000",
                str(R2/"audio"/"voice_tight.wav")],check=True)

def dur(p,sel):
    return float(subprocess.run([FFP,"-v","error","-select_streams",sel,"-show_entries",
        "stream=duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip())

plan = sum(int(round((f["b"]-f["a"])/FD))*FD for f in P)
da = dur(R2/"audio"/"voice_tight.wav","a:0")
print(f"voice_tight.wav {da:.4f}s   plan {plan:.4f}s   error {da-plan:+.4f}s")
assert abs(da-plan) < 0.01

# picture: concat the video streams only
lst = R2/"pieces_v.txt"
lst.write_text("".join(f"file '{(R2/'pieces'/f'p{i:03d}.mov').resolve()}'\n" for i in range(len(P))))
subprocess.run([FF,"-nostdin","-v","error","-y","-f","concat","-safe","0","-i",str(lst),
                "-map","0:v","-c:v","copy",str(R2/"_picture.mp4")],check=True)
dv = dur(R2/"_picture.mp4","v:0")
print(f"picture {dv:.4f}s   a/v drift {da-dv:+.4f}s")
assert abs(da-dv) < 0.05, "audio/video drift"
subprocess.run([FF,"-nostdin","-v","error","-y","-i",str(R2/"_picture.mp4"),
                "-i",str(R2/"audio"/"voice_tight.wav"),"-map","0:v","-map","1:a",
                "-c:v","copy","-c:a","pcm_s24le",str(R2/"tight.mov")],check=True)
print("tight.mov ->", dur(R2/"tight.mov","v:0"), dur(R2/"tight.mov","a:0"))
