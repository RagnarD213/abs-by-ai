"""RO-21 music bed: the cleared Pixabay trip-hop bed 10091 (Media/music beds, no attribution; live on V5 and RO-03). The track
(311 s) is shorter than the film (452 s), so it is extended ONCE: at a point S late in the track it jumps back by a lag L chosen
where 6 s of the track around S best matches 6 s around S-L (waveform correlation, searched on bar multiples of 130 bpm, then
refined to the sample), with a 1.5 s equal-power crossfade. Fade in 1.0 s, fade out 3.0 s at the film end. Level: the shared
voice chain ducks it under the voice (--bed/--bed-db).  python3 bed_r3.py FILM_SECONDS -> audio/bed/bed_full.wav"""
import subprocess, sys, numpy as np
FF = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'
T = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/music beds/rhythmical-melodic-syncopation-triphop-130bpm-pixabay-10091.mp3'
OUT = '/Volumes/Expansion/_edit_work/RO-21/audio/bed/bed_full.wav'; sr = 48000; N = int(round(float(sys.argv[1]) * sr))
m = np.frombuffer(subprocess.run([FF, '-v', 'error', '-i', T, '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
mono = m.mean(1); bar = 4 * 60 / 130
S = int(285 * sr); W = int(6 * sr)
def score(a, b):
    x, y = mono[a - W // 2:a + W // 2], mono[b - W // 2:b + W // 2]; return float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-9))
best = max(((score(S, S - int(round(k * bar * sr))), k) for k in range(int(150 / bar), int(250 / bar))), key=lambda z: z[0])
L0 = int(round(best[1] * bar * sr))
fine = max(((score(S, S - L0 - d), d) for d in range(-480, 481, 4)), key=lambda z: z[0]); L = L0 + fine[1]
need = N - S; seg2 = m[S - L:S - L + need]; assert len(seg2) == need, ('track too short after one loop', len(seg2), need)
x = int(1.5 * sr); r = np.sin(np.linspace(0, np.pi / 2, x))[:, None] ** 2
bed = np.concatenate([m[:S - x // 2], m[S - x // 2:S + x // 2] * (1 - r) + m[S - L - x // 2:S - L + x // 2] * r, m[S - L + x // 2:S - L + x // 2 + need - x // 2]])[:N]
fi, fo = int(1.0 * sr), int(3.0 * sr); bed[:fi] *= np.linspace(0, 1, fi)[:, None]; bed[-fo:] *= np.linspace(1, 0, fo)[:, None]
subprocess.run([FF, '-v', 'error', '-y', '-f', 'f32le', '-ar', str(sr), '-ac', '2', '-i', '-', '-c:a', 'pcm_s24le', OUT], input=bed.astype(np.float32).tobytes(), check=True)
print(f'bed {len(bed) / sr:.2f}s; loop at {S / sr:.1f}s back {L / sr:.3f}s (corr {fine[0]:.3f}, bar match {best[0]:.3f})')
