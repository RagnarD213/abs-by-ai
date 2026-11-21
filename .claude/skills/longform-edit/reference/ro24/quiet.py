"""Quietest 40 ms of the lav inside [a, b] (source s) -> its centre and the nearest frame; used to place reframe-only cuts."""
import sys, numpy as np, subprocess
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'; FPS = 30000 / 1001
def quiet(a, b):
    raw = subprocess.check_output([FF, '-v', 'error', '-ss', str(a), '-t', str(b - a), '-i', '/Volumes/Expansion/_edit_work/RO-24/round1/audio/lav_full.wav', '-f', 'f32le', '-ac', '1', '-ar', '48000', '-'])
    x = np.frombuffer(raw, np.float32); w = 1920
    e = np.convolve(x ** 2, np.ones(w) / w, 'valid'); i = int(np.argmin(e)); t = a + (i + w / 2) / 48000
    return t, int(round(t * FPS)), 10 * np.log10(e[i] + 1e-12)
if __name__ == '__main__':
    for spec in sys.argv[1:]:
        a, b = map(float, spec.split(':')); t, f, db = quiet(a, b); print(spec, round(t, 3), f, round(db, 1))
