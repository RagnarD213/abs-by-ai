"""DS-40 R6 film audio: the locked clip audio (R4 clip_only.wav, -14 LUFS) for the clip's 581 frames, then Dan's
scripted take through voice chain E (dan_E.wav, starts at roll frame ROLLF0) with the two ad-libs cut out.
Every join sits in measured silence (-46 dB or lower) and gets an 8 ms fade each side, so no click and no length change.

    python3 mix.py   -> film.wav (48 kHz stereo, exactly F_END frames long)
"""
import json, subprocess, numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real"
P = json.load(open("../plan.json")); FPS = 30000 / 1001; SR = 48000
ROLL0 = P["rollf0"] / FPS


def load(path):
    b = subprocess.run([FF, "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.float32).reshape(-1, 2).copy()


def fade(x, n_in, n_out):
    if n_in: x[:n_in] *= np.linspace(0, 1, n_in)[:, None] ** 2
    if n_out: x[-n_out:] *= np.linspace(1, 0, n_out)[:, None] ** 2
    return x


S = lambda t: int(round(t * SR))
clip = load("/Volumes/Expansion/_edit_work/ds40/r4/audio/clip_only.wav")
n_clip = S(P["n_clip"] / FPS)
clip = np.pad(clip, ((0, max(0, n_clip - len(clip))), (0, 0)))[:n_clip]
dan = load("dan_E.wav")
c1o, c1n = P["cut1"]; c2o, c2n = P["cut2"]
segs = [(0.0, c1o - ROLL0), (c1o + c1n / FPS - ROLL0, c2o - ROLL0), (c2o + c2n / FPS - ROLL0, (P["rollf0"] + P["j_end"] + 1) / FPS - ROLL0)]
f8 = S(0.008)
parts = []
for i, (a, b) in enumerate(segs):
    x = dan[S(a):S(b)].copy()
    parts.append(fade(x, S(0.025) if i == 0 else f8, f8 if i < 2 else S(0.15)))
out = np.concatenate([clip] + parts)
want = S(P["f_end"] / FPS)
assert abs(len(out) - want) <= 2, (len(out), want)
out = np.pad(out, ((0, max(0, want - len(out))), (0, 0)))[:want]
subprocess.run([FF, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s24le", "film.wav"],
               input=out.astype(np.float32).tobytes(), check=True)
print("film.wav", round(len(out) / SR, 3), "s; joins at film s",
      [round(P["n_clip"] / FPS + (segs[0][1] - segs[0][0]), 3), round(P["n_clip"] / FPS + (segs[0][1] - segs[0][0]) + (segs[1][1] - segs[1][0]), 3)])
