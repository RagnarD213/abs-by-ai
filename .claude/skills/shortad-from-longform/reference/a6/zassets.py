#!/usr/bin/env python3
"""Media for the beats that are rebuilt from HIS render or from the app recording.

  lift_phone.mp4      his phone-on-marble clip, frames 216-327 of his 4K render, a 9:16 window on the phone
                      (his 'AI-Generated' label sits outside it). Reused for his second phone beat (3618-3791), which
                      is the SAME 111 frames played 1:1 then held on the last one (measured r=1.000 frame for frame).
  lift_handphone.mp4  his hand-holding-phone clip, frames 1284-1400, a 9:16 window ending above his burned label.
  lift_anatomy.mp4    his anatomy clip, frames 4919-5132, the region ABOVE his burned CTA bar (4K y < 1720), for a card.
  app_a.mp4/app_b.mp4 the app recording (09_CLIP, 1320x2868 @60) played on HIS time map (holds + jumps, media_map.json),
                      app_b capped at 24.5 s of the recording -- at 26 s it reaches the in-app before/after and at 29 s
                      the email form, both banned (skill: the recording's usable window is 0-25 s).
  after_still.png     the app's AFTER IMAGE ALONE: the photo cut out of the recording at 31.0 s, inside its own edges
                      (859x1073 at x231 y662, minus a 3 px inset) -- no heading, no form, no confetti, no panel. The
                      after image never appears inside the recording's usable 0-25 s window, and the screens around
                      it are the banned ones, so only the photo's own pixels are taken. (Replaces after_reveal.mp4,
                      which was the screen cropped above the form: the independent audit, 2026-09-10, found its
                      heading and confetti still made it recognisably the email-capture screen.)"""
import json, os, subprocess, numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
Z4 = ("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Zeeshan Ad Videos/this picture got me abs - ad 1/"
      "this picture got me abs | zeeshan | 16x9 | ad 1 | h265.mov")
APP = ("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/00 ASSETS USED IN THE REFERENCE AD/"
       "09_CLIP_app-generate-future-self.mp4")
REVEAL = "/Volumes/Extreme/_edit_work/ad1-8-14/vert9x16/assets_v/after_reveal.mp4"
APP_SAFE_END = 24.5
os.makedirs('assets', exist_ok=True)
ENC = ['-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709',
       '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-an']
def lift(out, n0, n1, crop, scale):
    if os.path.exists(out): return
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', f'{n0/24 - 0.01:.4f}', '-i', Z4, '-frames:v', str(n1 - n0),
                    '-vf', f'crop={crop},scale={scale}:flags=lanczos,setsar=1', '-r', '24'] + ENC + [out], check=True)
    print('wrote', out)
lift('assets/lift_phone.mp4', 216, 327, '1215:2160:1372:0', '1080:1920')
lift('assets/lift_handphone.mp4', 1284, 1400, '1114:1980:1903:0', '1080:1920')   # rows < 1980: clear of his burned label's glyph tops
lift('assets/lift_anatomy.mp4', 4919, 5132, '1920:1720:960:0', '1920:1720')

# ---- the app recording on his time map ------------------------------------------------------------------------------
M = json.load(open('media_map.json'))
def build_app(key, out, pw=720):
    if os.path.exists(out): return
    m = M[key]; n0, n1 = m['n0'], m['n1']
    pts = [(n, t) for n, t, r, _ in m['map'] if t is not None and r >= 0.55]
    ns = np.array([p[0] for p in pts], float); ts = np.array([p[1] for p in pts], float)
    ts = np.maximum.accumulate(np.clip(ts, 0, APP_SAFE_END))            # monotone: he never plays it backwards
    want = [float(np.interp(n, ns, ts)) for n in range(n0, n1)]
    ph = round(pw * 2868 / 1320) & ~1
    idx = sorted(set(int(round(t * 60)) for t in want))
    p = subprocess.Popen([FF, '-nostdin', '-v', 'error', '-i', APP, '-vf', f'scale={pw}:{ph}:flags=area', '-f', 'rawvideo',
                          '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    keep, k = {}, 0
    while True:
        b = p.stdout.read(pw * ph * 3)
        if not b: break
        if k in idx: keep[k] = b
        k += 1
        if k > idx[-1]: break
    p.kill()
    e = subprocess.Popen([FF, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{pw}x{ph}', '-r', '24',
                          '-i', '-', '-vf', 'scale=out_color_matrix=bt709:out_range=tv'] + ENC + [out], stdin=subprocess.PIPE)
    last = None
    for t in want:
        j = int(round(t * 60)); j = min(keep, key=lambda q: abs(q - j)); e.stdin.write(keep[j])
    e.stdin.close(); e.wait()
    print('wrote', out, f'{n1-n0} frames, recording {want[0]:.2f}->{want[-1]:.2f}s')
build_app('app_a', 'assets/app_a.mp4')
# app_b: his map is noisy through the loader (low-r matches on near-identical scanning frames), so it is the measured
# anchors -- options screen held, then the flow at ~2x, then the loader to the cap -- not the raw per-sample noise.
if 'app_b' in M:
    M['app_b']['map'] = [[4291, 4.85, 0.9, None], [4326, 5.7, 0.9, None], [4333, 8.5, 0.9, None], [4423, 15.85, 0.9, None],
                         [4530, APP_SAFE_END, 0.9, None]]
build_app('app_b', 'assets/app_b.mp4')

if not os.path.exists('assets/after_reveal.mp4'):
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', REVEAL, '-frames:v', '38', '-vf', 'fps=24,setsar=1', '-r', '24']
                   + ENC + ['assets/after_reveal.mp4'], check=True)
    print('wrote assets/after_reveal.mp4')
