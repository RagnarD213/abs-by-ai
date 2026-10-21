"""10 ms RMS envelope of the lav between two source times (dB), to place edges where Whisper stretched a word."""
import sys, numpy as np, subprocess
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'
a, b = float(sys.argv[1]), float(sys.argv[2])
raw = subprocess.check_output([FF, '-v', 'error', '-ss', str(a), '-t', str(b - a), '-i', '/Volumes/Expansion/_edit_work/RO-24/round1/audio/lav_full.wav', '-f', 'f32le', '-ac', '1', '-ar', '48000', '-'])
x = np.frombuffer(raw, np.float32); n = 480
e = 20 * np.log10(np.sqrt(np.mean(x[:len(x) // n * n].reshape(-1, n) ** 2, 1)) + 1e-9)
step = int(sys.argv[3]) if len(sys.argv) > 3 else 5
for i in range(0, len(e), step):
    seg = e[i:i + step]
    print(f'{a + i * .01:8.2f} {seg.max():6.1f} ' + '#' * int(max(0, seg.max() + 60) / 2))
