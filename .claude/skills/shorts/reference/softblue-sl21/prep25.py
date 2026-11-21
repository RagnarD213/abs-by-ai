"""Prepare a take for LatentSync: it works at 25 fps in blocks of 16 frames and drops the remainder, and it can open the mouth on
the first frames, so give it N25 frames (a multiple of 16) resampled to 25 fps from the take's start, and audio that starts LEAD
seconds before the slot (the edit then starts the clip LEAD seconds in).
usage: prep25.py TAKE.mp4 FILM_SLOT_START LEAD N25 TAG   -> round2/lipsync/<TAG>.trim.mp4 (25 fps) + <TAG>.wav"""
import subprocess, sys, wave
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
VOICE = "/Volumes/Expansion/_edit_work/ro20/round4/v2/untreated.wav"; OUT = "/Users/danielrose/Projects/_edit_work/SL-21/round2/lipsync"
take, t0, lead, n, tag = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]; assert n % 16 == 0
dur = n / 25
subprocess.run([FF, "-v", "error", "-y", "-i", take, "-vf", "fps=25,format=yuv420p", "-frames:v", str(n), "-an", "-c:v", "libx264", "-crf", "12", "-preset", "slow",
                "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", f"{OUT}/{tag}.trim.mp4"], check=True)
w = wave.open(VOICE); sr = w.getframerate(); w.setpos(int(round((t0 - lead) * sr))); pcm = w.readframes(int(round(dur * sr))); w.close()
o = wave.open(f"{OUT}/{tag}.wav", "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(pcm); o.close()
print(tag, n, "frames at 25 fps =", dur, "s; audio from film", round(t0 - lead, 3), "to", round(t0 - lead + dur, 3))
