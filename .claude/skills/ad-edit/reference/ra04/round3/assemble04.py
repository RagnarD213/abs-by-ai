"""RA-04 round 3: the AI broken-arm clip (AI1) for slot A, exactly the card's frame count at 29.97, from the chosen Veo takes.
  shots 1+2 (39.139-42.509, 101 frames): ONE continuous action across two takes that share Dan's approved frame F2:
            AI1-1_b frames 56..95 (last steps, stops, eyes the barbell, lips pressed) then AI1-2_d frames 1..51 (hand to the
            pocket, phone out, reading; frame 0 is F2 again and is skipped). The phone comes out on "use Abs By AI to".
  shot 3   (42.509-43.443, 28 frames): AI1-3_a frames 60..84, one push of the leg press from the bottom of the rep to almost
            straight, phone lowered to his chest, on "adjust your plan."
Frames are picked from the raw YUV planes (no colour conversion; the takes are untagged and are read as BT.709, memory
`untagged-video-bt601-trap`), evenly spread over each window: speed 1.12x and 1.11x, a slight speed-up, never a hold or a slow-down.
usage: assemble04.py   -> media/ai1.mp4 (+ .json with every output frame's source)"""
import json, subprocess, numpy as np
W = "/Volumes/Extreme/_edit_work/ra04"; FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
B = json.load(open(f"{W}/beats.json")); card = next(c for c in B["cards"] if c["name"] == "brokenarm"); N = card["frames"]
FPS = 30000/1001; fr = lambda t: int(round(t*FPS)); a0 = fr(card["beat"][0]); cut3 = fr(42.509) - a0; assert N == 129 and cut3 == 101, (N, cut3)
SZ = 1080*1920*3//2
def load(tag):
    raw = subprocess.run([FF, "-v", "error", "-i", f"{W}/round3/motion/{tag}.mp4", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-"], capture_output=True, check=True).stdout
    F = [raw[i:i+SZ] for i in range(0, len(raw), SZ)]; assert len(F) in (96, 144, 192), (tag, len(F)); return F
# v2 (independent review 1 failed v1's two-take join: the walk take did not land on F2, so the man jumped 21-37 px in one frame,
# the floor grain changed and an earring vanished). Shots 1+2 are now ONE 6 s take from S1 to F3b, and every output frame is a
# distinct source frame (1:1, 1.25x): v1's 1.12x repeated 13 frames, which made the sled pause three times.
T12, T3 = load("AI1-12_c"), load("AI1-3_b")
src12 = [("AI1-12_c", i, T12[i]) for i in range(4, 105)]
src3 = [("AI1-3_b", i, T3[i]) for i in range(60, 88)]
def spread(src, n): return [src[int(round(j*(len(src)-1)/(n-1)))] for j in range(n)]
seq = spread(src12, cut3) + spread(src3, N - cut3)
sp12 = (len(src12)-1)/(cut3-1)*FPS/24; sp3 = (len(src3)-1)/(N-cut3-1)*FPS/24
assert 1.0 <= sp12 <= 1.25 and 1.0 <= sp3 <= 1.25, (sp12, sp3)   # never slowed or held
enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-s", "1080x1920", "-framerate", "30000/1001", "-i", "-",
                        "-c:v", "libx264", "-crf", "10", "-preset", "slow", "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
                        "-color_primaries", "bt709", "-color_trc", "bt709", f"{W}/media/ai1.mp4"], stdin=subprocess.PIPE)
for _, _, f in seq: enc.stdin.write(f)
enc.stdin.close(); assert enc.wait() == 0
json.dump({"frames": N, "shot3_starts_at_frame": cut3, "speed_shots12": round(sp12, 3), "speed_shot3": round(sp3, 3),
           "source": [[t, i] for t, i, _ in seq]}, open(f"{W}/media/ai1.json", "w"), indent=0)
print("media/ai1.mp4", N, "frames; shots 1+2 speed", round(sp12, 3), "shot 3 speed", round(sp3, 3), "| shot 3 from output frame", cut3)
