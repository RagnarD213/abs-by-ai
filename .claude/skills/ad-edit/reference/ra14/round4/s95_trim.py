#!/usr/bin/env python3
"""RA-14 round 4: end the ad on Dan's held smile instead of the last second of the take.

FOUND by the round 4 watch-pass judge: after the smile with steepled hands (frames ~1452-1481) his mouth opens at 1482
and he talks with no sound, then steps right and the crop pans after him (head 22 % off centre at 50.25 s). Round 3
showed Dan only the first 30.3 s finished, so this end hold was never in front of him. RA-07 lesson 5: the end hold is
real footage, so it is only as long as the pose lasts. Checked frame by frame (round4/look/end_mouth.jpg): 1481 is the
last frame of the smile.

  picture: the first END frames of the LOCKED round3/work/picture_9x16.mp4, stream-copied, then proved frame-identical
           (framemd5 of every decoded frame against the locked file's first END frames)
  audio:   round4/mix_bass_r4.wav cut at END frames, with a 0.50 s raised-cosine fade to silence over the last half
           second (from 48.95 s; the last word ends 48.365 s). Every sample before the fade is the r4 mix (and so the
           approved r3 mix before 48.42 s); null-tested below.
  python3 round4/s95_trim.py   (from /Volumes/Extreme/_edit_work/ra14)
"""
import hashlib, json, subprocess, sys, wave
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import ra01lib as L

END = 1482                               # frames kept: 0..1481
FPS = L.FPS; SR = 48000
FADE = 0.50
PIC = "round3/work/picture_9x16.mp4"
R4 = "round4"
OUTV = f"{R4}/work/picture_9x16_trim.mp4"
OUTA = f"{R4}/mix_bass_r4_end.wav"
MASTER = f"{R4}/the cheat code for six pack abs | claude | 9x16 | RA-14.mp4"
import os; os.makedirs(f"{R4}/work", exist_ok=True)

subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-i", PIC, "-map", "0:v", "-c", "copy", "-frames:v", str(END), OUTV], check=True)


def fmd5(path, n):
    r = subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", path, "-frames:v", str(n), "-map", "0:v", "-f", "framemd5", "-"],
                       capture_output=True, text=True, check=True).stdout
    return [ln.split(",")[-1].strip() for ln in r.splitlines() if ln and not ln.startswith("#")]


a, b = fmd5(PIC, END), fmd5(OUTV, END + 5)
assert len(b) == END, f"trimmed picture has {len(b)} frames, want {END}"
assert a == b, "trimmed picture is not frame-identical to the locked picture"

raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", f"{R4}/mix_bass_r4.wav", "-f", "s32le", "-acodec", "pcm_s32le", "-"],
                     capture_output=True, check=True).stdout
xi = np.frombuffer(raw, np.int32).reshape(-1, 2)
n = int(round(END / FPS * SR))
y = xi[:n].astype(np.float64)
f0 = n - int(FADE * SR)
k = np.arange(n - f0) / (n - f0)
y[f0:] *= (0.5 + 0.5 * np.cos(np.pi * k))[:, None]
yi = (np.clip(np.round(y / 256), -2**23, 2**23 - 1).astype(np.int64) << 8).astype(np.int32)
yi[:f0] = xi[:f0]
wv = wave.open(OUTA, "w"); wv.setnchannels(2); wv.setsampwidth(3); wv.setframerate(SR)
wv.writeframes(yi.astype("<i4").view(np.uint8).reshape(-1, 4)[:, 1:].tobytes()); wv.close()
chk = np.frombuffer(subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", OUTA, "-f", "s32le", "-acodec", "pcm_s32le", "-"],
                                   capture_output=True, check=True).stdout, np.int32).reshape(-1, 2)
r3 = np.frombuffer(subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", "mix_bass_r3.wav", "-f", "s32le", "-acodec", "pcm_s32le", "-"],
                                  capture_output=True, check=True).stdout, np.int32).reshape(-1, 2)
d4 = np.nonzero(np.any(chk != xi[:n], axis=1))[0]
d3 = np.nonzero(np.any(chk != r3[:n], axis=1))[0]
first_vs_r4 = d4[0] / SR if len(d4) else None
first_vs_r3 = d3[0] / SR if len(d3) else None
assert first_vs_r3 is None or first_vs_r3 >= 48.4, first_vs_r3

subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-i", OUTV, "-i", OUTA, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", MASTER], check=True)
assert fmd5(MASTER, END + 5) == a, "master picture is not frame-identical to the locked picture"
h = hashlib.sha256(open(MASTER, "rb").read()).hexdigest()
rep = dict(end_frames=END, end_s=round(END / FPS, 4), fade_s=FADE, fade_from_s=round(f0 / SR, 4), picture_identical_frames=END,
           first_sample_changed_vs_r4=first_vs_r4, first_sample_changed_vs_r3=first_vs_r3, master=MASTER, sha256=h)
json.dump(rep, open(f"{R4}/trim.json", "w"), indent=1)
print(json.dumps(rep, indent=1))
