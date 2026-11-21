"""RO-21 round 3 film voice, picture-locked (plus one 45 ms click at 143.55 s filled with room tone). Round 1's voice_r1.py joined the pieces by overlapping the next piece onto the
LAST 40 ms of the previous one, which shortened the track by 40 ms at every join: by the end the voice ran 560 ms ahead of
the picture (independent reviewer, R3, measured against the camera audio of C1724). Here every piece is placed at exactly
its film_in, and the 40 ms crossfade is centred on the join using 20 ms of real lav audio past each piece's edges, so no
time is lost. Same patched lav (round 1: "shop" -> "show"), same fades. -> audio/film/film_voice_raw_r3.wav"""
import json, numpy as np, subprocess
B = '/Volumes/Expansion/_edit_work/RO-21'; FF = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'; sr = 48000
rd = lambda p: np.frombuffer(subprocess.run([FF, '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(sr), '-'], capture_output=True, check=True).stdout, np.float32).astype(np.float64)
y = rd(f'{B}/audio/lav_patched.wav'); x = rd(f'{B}/audio/lav_full.wav')
S = lambda t: int(round(t * sr)); FPS = 30000 / 1001
E = json.load(open(f'{B}/round1/edl_r1.json')); P = json.load(open(f'{B}/round1/plan_r1.json')); END = max(p['b'] for p in P)
h = S(0.020); f = 2 * h; r = np.sin(np.linspace(0, np.pi / 2, f)) ** 2
out = np.zeros(S(END) + S(1.0))
for k, e in enumerate(E):
    s0, s1 = S(e['f_in'] / FPS), S(e['f_out'] / FPS); o0 = S(e['f_in'] / FPS - e['f_in'] / FPS + e['film_in'])
    a = s0 - (h if k else 0); b = s1 + (h if k + 1 < len(E) else 0)
    seg = y[a:b].copy()
    if k: seg[:f] *= r
    if k + 1 < len(E): seg[-f:] *= r[::-1]
    p0 = o0 - (h if k else 0); out[p0:p0 + len(seg)] += seg
last = E[-1]; tail = S(last['film_in']) + S((last['f_out'] - last['f_in']) / FPS)
c = np.concatenate([[0], np.cumsum(x[:S(560)] ** 2)]); env = (c[S(1.0):] - c[:-S(1.0)])[::480]; kq = int(np.argmin(env[S(30) // 480:])) * 480 + S(30)
tone = x[kq:kq + S(1.0)]; pos = tail
while pos < S(END):
    t = tone[:S(END) - pos].copy(); m = min(f, len(t)); t[:m] *= r[:m]; out[pos:pos + len(t)] += t; pos += len(t)
out = out[:S(END)]
# R3 review: a 45 ms mouth click in the pause after the join at 143.54 (2:23.56, 0.27 s before "That"; in the lav itself,
# 28 dB over the pause in the 3 kHz+ band). Room tone from just after it, 5 ms equal-power edges.
c0, c1 = S(143.552), S(143.605); fill = out[S(143.615):S(143.615) + (c1 - c0)].copy(); e5 = S(0.005); rr = np.sin(np.linspace(0, np.pi / 2, e5)) ** 2
fill[:e5] = fill[:e5] * rr + out[c0:c0 + e5] * (1 - rr); fill[-e5:] = fill[-e5:] * rr[::-1] + out[c1 - e5:c1] * (1 - rr[::-1]); out[c0:c1] = fill
subprocess.run([FF, '-v', 'error', '-y', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', '-', '-c:a', 'pcm_s24le', f'{B}/audio/film/film_voice_raw_r3.wav'],
               input=out.astype(np.float32).tobytes(), check=True)
# sync proof: every piece's middle second against the lav at its source time (lag must be 0)
for e in E:
    m = (e['film_in'] + e['film_out']) / 2; src = e['f_in'] / FPS + (m - e['film_in'])
    a = out[S(m - 0.5):S(m + 0.5)]; best = max(range(-S(0.1), S(0.1) + 1, 48), key=lambda d: float(np.dot(a, y[S(src - 0.5) + d:S(src - 0.5) + d + len(a)])))
    print(f"piece {e['k']:2d} at {m:6.1f}s lag {best / sr * 1000:+.0f} ms")
