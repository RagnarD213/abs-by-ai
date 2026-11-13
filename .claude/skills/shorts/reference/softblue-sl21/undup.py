"""The lip-synced clips are 25 fps because LatentSync works at 25: the take's 24 fps frames were resampled, which shows one take frame
twice every second. Drop exactly those repeats (found in the unsynced twin, where a repeat is pixel-identical) and write the rest at
24 fps, the take's own rate and timing. The mouth keeps its sync: frame k of the 25 fps file sits within one frame of its 24 fps time.
usage: undup.py TWIN_TRIM_25.mp4 SYNCED_25.mp4 OUT_24.mp4"""
import subprocess, sys, json, numpy as np
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
twin, synced, out = sys.argv[1:4]
raw = subprocess.run([FF, "-v", "error", "-i", twin, "-vf", "scale=270:480:flags=area,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
G = np.frombuffer(raw, np.uint8).reshape(-1, 480, 270).astype(np.int16)
d = np.array([999.0] + [float(np.abs(G[i] - G[i - 1]).mean()) for i in range(1, len(G))])
cand = [i for i in range(1, len(G)) if d[i] < 0.15 * np.median(d[1:])]
# a 24 -> 25 resample repeats one frame every 25: keep only the candidates on that rhythm (a still moment in the take is not a repeat,
# and dropping it would slide the mouth two frames ahead of the voice)
res = max(set(i % 25 for i in cand), key=lambda r: sum(1 for i in cand if i % 25 == r)) if cand else 0
dups = [i for i in cand if i % 25 == res]
sel = "*".join(f"not(eq(n\\,{i}))" for i in dups) or "1"
subprocess.run([FF, "-v", "error", "-y", "-i", synced, "-vf", f"select='{sel}',setpts=N/24/TB", "-r", "24", "-an", "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], check=True)
n = int(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", out],
                       capture_output=True, text=True).stdout.strip() or 0)
print(json.dumps(dict(out=out, frames_in=len(G), repeats_dropped=dups, frames_out=n, seconds=round(n / 24, 3), median_step=round(float(np.median(d[1:])), 2))))
