"""Round 3 voice: at 4:47.9 the take join kept a stray second "portant than" (287.96-288.33, a viewer hears "than ... than working out longer").
It becomes the pause already there (room tone from the 0.26 s before the join, mirrored), crossfaded 15 ms; length and every other sample unchanged."""
import numpy as np, subprocess
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; sr = 48000
x = np.frombuffer(subprocess.run([FF, "-v", "error", "-i", "../round1/voice_A_full.wav", "-f", "f64le", "-ac", "2", "-ar", str(sr), "-"], capture_output=True).stdout, np.float64).reshape(-1, 2)
a, b = int(287.80 * sr), int(288.325 * sr); cut = int(round(12 * 1001 / 30000 * sr))       # 0.525 s out, 0.125 s of room tone in: 12 frames shorter
src = x[int(287.70 * sr):int(287.88 * sr)]; n = int(.015 * sr); f = np.sin(np.linspace(0, np.pi / 2, n))[:, None] ** 2
need = b - a - cut; fill = np.concatenate([src, src[::-1]])[:need + 2 * n]
y = np.concatenate([x[:a], fill[:need], x[b:]])
y[a:a + n] = x[a:a + n] * (1 - f) + fill[:n] * f
y[a + need - n:a + need] = fill[need - n:need] * (1 - f) + x[b - n:b] * f
subprocess.run([FF, "-v", "error", "-y", "-f", "f64le", "-ac", "2", "-ar", str(sr), "-i", "-", "-c:a", "pcm_s24le", "voice_A_r3.wav"], input=y.tobytes(), check=True); print("ok", len(y) / sr)
