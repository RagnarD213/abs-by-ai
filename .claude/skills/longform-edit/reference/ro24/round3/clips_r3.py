"""RO-24 round 3: the six interview clips as full-screen inserts that play WITH their own sound (the script's [PLAY CLIP]
cues), trimmed to the script's first and last words (edges on measured quiet points), 1920x1080 at 29.97, exact frame
counts, a small source chip top left (the AI-chip style). Audio: 48 kHz stereo, measured gain to -15 LUFS (his voice runs
at about -14 with pauses), 25 ms fades. Writes clips/<name>_insert.mp4 + .wav and clips/inserts.json.

  python3 clips_r3.py [--check]      (--check: levels of every trimmed clip, then exit)
"""
import json, subprocess, sys, re, numpy as np
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import softblue as B
from PIL import Image
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'; FPS = 30000 / 1001
R3 = '/Volumes/Expansion/_edit_work/RO-24/round3'; S = f'{R3}/clips/src'; O = f'{R3}/clips'
# name: (file start, file end, source chip, YouTube id, what the trim says)
CLIPS = {
 'sharon': (0.00, 26.90, 'E! News', 'oZTHGIoqwI4', '"Why Sharon Osbourne is cautioning others..." to "I\'m under 100 pounds and I don\'t want to be."'),
 'fatjoe': (0.00, 17.85, 'Page Six', 'XkGHIKXLShA', '"It looks like Fat Joe is now Skinny Joe" to "...two pieces of your favorite stuff."'),
 'amy':    (12.42, 28.84, 'The Howard Stern Show', 'unx1EuJ8t9s', '"I tried it and I was vomiting" to "...head off the pillow. So what\'s the point?"'),
 'meghan': (7.70, 24.30, 'Entertainment Tonight', 'DNTlfd8Cbk4', '"She writes, no, I don\'t look like I did 10 years ago" to "...after my second pregnancy."'),
 'oprah':  (8.66, 23.40, 'Oprah', 'g7pw3MJ7QVE', '"Yeah, I tried to beat this" to "And I gained 15 pounds."'),
 'tracy':  (11.30, 24.64, 'The Tonight Show Starring Jimmy Fallon', 'qAJziET5X6g', '"You look great. How are you staying in shape these days?" to "Yeah, I gained 40."'),
}

def loud(path, a=None, d=None):
    cmd = [FF, '-v', 'info', '-nostats'] + (['-ss', str(a), '-t', str(d)] if a is not None else []) + ['-i', path, '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-']
    err = subprocess.run(cmd, capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', err)[-1]); tp = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', err)[-1])
    return I, tp

def levels(path, a, d):
    raw = subprocess.check_output([FF, '-v', 'error', '-ss', str(a + d / 2), '-i', path, '-frames:v', '1', '-vf', 'scale=480:270', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    x = np.frombuffer(raw, np.uint8).reshape(270, 480, 3) / 255.0
    y = x @ [.2126, .7152, .0722]; mx, mn = x.max(2), x.min(2); s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    return np.percentile(y, 1), np.median(y), np.median(s)

if '--check' in sys.argv:
    for n, (a, b, *_ ) in CLIPS.items():
        print(n, 'black %.3f median %.3f sat %.3f' % levels(f'{S}/{n}.mp4', a, b - a), 'loud I %.1f TP %.1f' % loud(f'{S}/{n}.mp4', a, b - a))
    sys.exit()

out = {}
for n, (a, b, src, yid, says) in CLIPS.items():
    N = int(round((b - a) * FPS)); dur = N / FPS
    chip = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); B.disclosure(chip, src, xy=(56, 48)); chip.save(f'{O}/{n}_chip.png')
    subprocess.run([FF, '-y', '-v', 'error', '-ss', f'{a:.3f}', '-i', f'{S}/{n}.mp4', '-i', f'{O}/{n}_chip.png', '-filter_complex',
                    '[0:v]fps=30000/1001,scale=1920:1080:flags=lanczos,setsar=1[v];[v][1:v]overlay=0:0[o]', '-map', '[o]', '-frames:v', str(N), '-an',
                    '-c:v', 'libx264', '-crf', '14', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    '-colorspace', 'bt709', f'{O}/{n}_insert.mp4'], check=True)
    I, tp = loud(f'{S}/{n}.mp4', a, dur); g = -15.0 - I
    subprocess.run([FF, '-y', '-v', 'error', '-ss', f'{a:.3f}', '-t', f'{dur:.6f}', '-i', f'{S}/{n}.mp4', '-vn', '-af',
                    f'aresample=48000,volume={g:.2f}dB,alimiter=limit=0.70:attack=5:release=60:level=disabled,atrim=start_sample=240,asetpts=N/SR/TB,apad,atrim=end_sample={int(round(dur * 48000))},'
                    f'afade=t=in:d=0.025,afade=t=out:st={dur - 0.025:.4f}:d=0.025', '-ac', '2', '-c:a', 'pcm_s16le', f'{O}/{n}_insert.wav'], check=True)
    I2, tp2 = loud(f'{O}/{n}_insert.wav')
    out[n] = dict(file=f'clips/{n}_insert.mp4', wav=f'clips/{n}_insert.wav', frames=N, dur=round(dur, 4), src=f'clips/src/{n}.mp4', a=a, b=round(a + dur, 4),
                  source=src, youtube=f'https://www.youtube.com/watch?v={yid}', says=says, lufs=round(I2, 1), tp=round(tp2, 1), gain_db=round(g, 2))
    print(n, N, 'frames', round(dur, 2), 's', 'LUFS', round(I, 1), '->', round(I2, 1), 'TP', round(tp2, 1), flush=True)
json.dump(out, open(f'{O}/inserts.json', 'w'), indent=1)
print('CLIPS DONE')
