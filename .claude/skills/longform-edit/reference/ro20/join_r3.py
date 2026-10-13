"""RO-20 round 3: join film context clips and pickup segments into the review cuts (12 ms audio fades at every join). usage: join_r3.py"""
import subprocess, os
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; W = "/Volumes/Extreme/_edit_work/ro20"
P, C, O = f"{W}/round3/pickups", f"{W}/round3/context", f"{W}/round3/first-minute"
def dur(p): return float(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
def cat(out, *ins):
    a, f = [], ""
    for i, x in enumerate(ins):
        a += ["-i", x]; d = dur(x)
        f += f"[{i}:v]fps=30000/1001,scale=1920:1080,setsar=1,format=yuv420p[v{i}];[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.012,afade=t=out:st={d-0.03:.3f}:d=0.012[a{i}];"
    f += "".join(f"[v{i}][a{i}]" for i in range(len(ins))) + f"concat=n={len(ins)}:v=1:a=1[v][a]"
    subprocess.run([FF, "-v", "error", "-y"] + a + ["-filter_complex", f, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-colorspace", "bt709",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-i", out, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out[:-4] + " - REVIEW 540p.mp4"], check=True)
    print("joined", os.path.basename(out), round(dur(out), 2), "s; joins at", [round(sum(dur(x) for x in ins[:k]), 2) for k in range(1, len(ins))], flush=True)
cat(f"{O}/DRAFT - RO-20B round 3 - video 2 first minute.mp4", f"{C}/v2open-context.mp4", f"{P}/P2.mp4", f"{C}/v2film-context.mp4")
cat(f"{O}/DRAFT - RO-20C round 3 - video 3 first minute.mp4", f"{P}/P4.mp4", f"{C}/v3film-context.mp4")
cat(f"{O}/DRAFT - RO-20 round 3 - video 1 ending.mp4", f"{C}/v1end-context.mp4", f"{P}/P1.mp4", f"{C}/v1-signoff.mp4")
