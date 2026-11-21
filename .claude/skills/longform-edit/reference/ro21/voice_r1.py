"""RO-21 round 1 film voice. 1) Patch the lav in place, same total length: "start to shop" -> "show" (donor: "obliques start
to show", src 352.68-352.98) and the recap's mispronounced "calorie" (donor: the clean "track every calorie" at src 424.22-
424.68); each length change is taken out of the silent pause right after it, so every later source time is unchanged.
Both patches sit under full-screen pictures (F15 fact card, G11 recap ladder). 2) Cut the patched lav to edl_r1.json with
15 ms equal-power fades at the (measured quiet) joins; pad with room tone to the film end. -> audio/film/film_voice_raw.wav"""
import json, numpy as np, subprocess
B = '/Volumes/Expansion/_edit_work/RO-21'; FF = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'
sr = 48000
x = np.frombuffer(subprocess.run([FF, '-v', 'error', '-i', f'{B}/audio/lav_full.wav', '-f', 'f32le', '-ac', '1', '-ar', str(sr), '-'],
                                 capture_output=True, check=True).stdout, np.float32).astype(np.float64)
def write(path, a):
    subprocess.run([FF, '-v', 'error', '-y', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', '-', '-c:a', 'pcm_s24le', path],
                   input=a.astype(np.float32).tobytes(), check=True)
S = lambda t: int(round(t * sr))
def xf(n): return np.sin(np.linspace(0, np.pi / 2, n)) ** 2
def splice(y, a, b, donor, cut_a):
    """replace y[a:b] by donor (10 ms crossfades at both edges), then delete the extra length from the silence that starts at
    cut_a (original timeline), so the total length and every later source time are unchanged"""
    f = S(0.010); d = donor.copy(); r = xf(f)
    pre, post = y[:S(a)].copy(), y[S(b):].copy()
    d[:f] = d[:f] * r + pre[-f:] * (1 - r); pre = pre[:-f]
    d[-f:] = d[-f:] * r[::-1] + post[:f] * (1 - r[::-1]); post = post[f:]
    z = np.concatenate([pre, d, post]); extra = len(z) - len(y); assert extra >= 0
    k0 = S(cut_a) + (extra if cut_a > a else 0)          # absorb after the patch, or in a pause before it
    z = np.concatenate([z[:k0], z[k0 + extra:]]); assert len(z) == len(y)
    return z
y = x.copy()
y = splice(y, 317.50, 317.70, x[S(352.68):S(352.99)], 317.85)     # shop -> show
# recap "calor-ee": NOT patched. Blind listening 2026-10-28 (3 runs each, controls mixed in): his original line scored 1/1/1,
# a word swap 5/5/5 and a whole-phrase swap 4/4/5. A natural slight mispronunciation beats an audible patch.
write(f'{B}/audio/lav_patched.wav', y)
E = json.load(open(f'{B}/round1/edl_r1.json')); P = json.load(open(f'{B}/round1/plan_r1.json'))
END = max(p["b"] for p in P); f = S(0.040); r = xf(f); out = np.zeros(0)   # 40 ms equal-power joins
for e in E:
    seg = y[int(round(e['f_in'] * 1001 / 30000 * sr)):int(round(e['f_out'] * 1001 / 30000 * sr))].copy()
    if len(out):
        seg[:f] = seg[:f] * r + out[-f:] * (1 - r); out = out[:-f]
    out = np.concatenate([out, seg])
# room tone to the film end (quietest 1 s of the roll between takes)
c = np.concatenate([[0], np.cumsum(x[:S(560)] ** 2)]); env = (c[S(1.0):] - c[:-S(1.0)])[::480]; k = int(np.argmin(env[S(30) // 480:])) * 480 + S(30)
tone = x[k:k + S(1.0)]
need = S(END) - len(out)
while need > 0:
    t = tone[:need].copy(); m = min(f, len(t)); t[:m] *= r[:m]; out = np.concatenate([out, t]); need = S(END) - len(out)
out = out[:S(END)]
write(f'{B}/audio/film/film_voice_raw.wav', out)
print('film voice', round(len(out) / sr, 3), 's; film end', END)
