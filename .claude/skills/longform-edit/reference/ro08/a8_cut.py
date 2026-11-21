"""RO-08 round 3: the cell clean-up cartoon (A8) with the stretch where the heaps of junk clear by themselves taken out, so the change from
the cluttered cell to the clean one happens on a hard cut (the 2026-10-13 rule: a jump in time or state is a CUT between two natural shots).
Take frames 0..123 (the crew shovels and wheels the junk toward the furnace), CUT, 164..191 (the cell is clean and bright, they tip the barrows
into the furnace). The second part starts at 164, not at 142 where the big sweep ends: the last rubble on the floor keeps thinning out by
itself until about 154 and a few bits are still going at the edges until 163 (read frame by frame; the background outside the crew goes on
changing until then). 24 fps laid on 29.97 by repeating frames, never retimed. 40 frames leave the take and its unused tail has 14 spare, so
the clip is 32 frames (1.07 s) shorter: it starts 32 frames later, on "breaking down", and ends where it ended. The cut falls on "and makes
you younger", so the cluttered cell plays under "renews your cells" and the clean one under "makes you younger".
usage: a8_cut.py OUT.mp4 N_FRAMES"""
import sys, subprocess
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; SRC = "/Volumes/Extreme/_edit_work/ro08/round2/motion/A8-t1.mp4"
out = sys.argv[1]; N = int(sys.argv[2]); FPS = 30000/1001; SZ = 1920*1080*3//2; PRE_END = 123; POST_START = 164
raw = subprocess.run([FF, "-v", "error", "-i", SRC, "-pix_fmt", "yuv420p", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
F = [raw[i:i+SZ] for i in range(0, len(raw), SZ)]; assert len(F) == 192
a = F[:PRE_END+1]; b = F[POST_START:]; n1 = int(round(len(a)*FPS/24)); n2 = N - n1
assert int((n2-1)*24/FPS) < len(b), f"the second part runs out of source ({n2} frames asked): never hold a frame"
seq = [a[min(len(a)-1, int(j*24/FPS))] for j in range(n1)] + [b[int(j*24/FPS)] for j in range(n2)]
enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-s", "1920x1080", "-framerate", "30000/1001", "-i", "-", "-an", "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                        "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], stdin=subprocess.PIPE)
for f in seq: enc.stdin.write(f)
enc.stdin.close(); assert enc.wait() == 0
print(out, N, "frames; the cut is at output frame", n1, f"({n1/FPS:.3f} s); second part uses take frames {POST_START}..{POST_START + int((n2-1)*24/FPS)} of 191")
