#!/usr/bin/env python3
"""Render the 9:16 picture: one output segment per beat, concat, then the overlays.

Frame counts are cumulative for the same reason build_base.py's are -- per-segment
rounding across 48 segments walks the picture off the audio.
"""
import json, os, subprocess, sys, math
sys.path.insert(0, '.')
import vlib, beats
from assets import MEDIA
from motionlib import encode
from PIL import Image
import numpy as np

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001
VW, VH = 1080, 1920
BASE = 'base.mp4'
os.makedirs('out', exist_ok=True); os.makedirs('gfx', exist_ok=True)

# --- vignette mask (his radial falloff, in the vertical frame's coordinates) ---
if not os.path.exists('vignette.png'):
    m = (vlib.vignette_mask()*255).clip(0,255).astype('uint8')
    Image.fromarray(np.dstack([m]*3)).save('vignette.png')

# Dan's full-bleed crop: 608x1080 centred on his head (measured at x=918, sd 18px).
FULL_CROP = f'crop=608:1080:{918-304}:0,scale={VW}:{VH}:flags=lanczos,unsharp=5:5:0.85:5:5:0.0'
# blend must run in RGB. On yuv420p it multiplies the CHROMA planes about their 128
# offset as if they were luma, which turns every footage frame bright green.
VIG = f'[v0]format=gbrp[v0f];[vg]format=gbrp[vgf];[v0f][vgf]blend=all_mode=multiply,format=yuv420p'

def cover_chain(w, h):
    return f'scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},setsar=1'

def media_input(key, nfr):
    """(ffmpeg input args, needs_loop) for a media key, trimmed to nfr frames."""
    spec = MEDIA[key]
    if spec[0] == 'img':
        return ['-loop','1','-framerate',f'{FPS:.6f}','-t',f'{nfr/FPS+0.2:.4f}','-i',spec[1]]
    return ['-ss', f'{spec[2]:.3f}', '-stream_loop', '3', '-i', spec[1]]

_AR = {}
def media_ar(key):
    """Aspect ratio of a media key, from the file itself -- never assumed."""
    if key in _AR: return _AR[key]
    p = MEDIA[key][1]
    o = subprocess.run([FF.replace('ffmpeg','ffprobe'),'-v','error','-select_streams','v',
                        '-show_entries','stream=width,height','-of','csv=p=0:s=x',p],
                       capture_output=True, text=True).stdout.strip().split('\n')[0]
    w, h = (int(x) for x in o.split('x')[:2])
    _AR[key] = w/h
    return _AR[key]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(' '.join(cmd[:40]), '\n', r.stderr[-1500:]); raise SystemExit(1)

def seg_out(i): return f'out/s{i:03d}.mp4'

def render_segment(i, b, nfr, t0):
    out = seg_out(i)
    if os.path.exists(out) and os.path.getsize(out) > 20000: return
    k = b['kind']; dur = nfr/FPS
    common = ['-r','30000/1001','-frames:v',str(nfr),'-c:v','libx264','-preset','medium',
              '-crf','16','-pix_fmt','yuv420p','-an', out]
    if k == 'talk':
        run([FF,'-v','error','-y','-ss',f'{t0:.4f}','-i',BASE,
             '-loop','1','-framerate','30000/1001','-i','vignette.png',
             '-filter_complex', f'[0:v]{FULL_CROP}[v0];[1:v]scale={VW}:{VH}[vg];{VIG}'] + common)
        return
    if k == 'bleed':
        run([FF,'-v','error','-y'] + media_input(b['media'], nfr) +
            ['-loop','1','-framerate','30000/1001','-i','vignette.png',
             '-filter_complex', f'[0:v]{cover_chain(VW,VH)},unsharp=5:5:0.4:5:5:0.0[v0];'
                                f'[1:v]scale={VW}:{VH}[vg];{VIG}'] + common)
        return
    # --- plated beats ---------------------------------------------------------
    plate = f'gfx/p{i:03d}.mov'
    if not os.path.exists(plate):
        if k == 'window':
            fr, hole = vlib.plate_window(b.get('header'), b['bullets'], dur)
        elif k == 'card':
            fr, hole = vlib.plate_card(dur, caption=b.get('caption'), label=b.get('label'),
                                       portrait=b.get('portrait', False), top_kicker=b.get('kicker'),
                                       media_ar=media_ar(b['media']))
        elif k == 'title':
            fr, hole = vlib.plate_title(b['headline'], b.get('sub'), dur)
        elif k == 'statement':
            fr, hole = vlib.plate_statement(b['parts'], dur)
        else:
            raise ValueError(k)
        encode(fr[:nfr] + [fr[-1]]*max(0, nfr-len(fr)), plate, alpha=True)
        json.dump(hole, open(plate + '.hole.json', 'w'))
    hole = json.load(open(plate + '.hole.json'))
    if hole is None:
        run([FF,'-v','error','-y','-i',plate,
             '-filter_complex',f'color=black:s={VW}x{VH}:r=30000/1001[bg];[bg][0:v]overlay=0:0:shortest=1'] + common)
        return
    hx, hy = int(hole[0]), int(hole[1])
    hw, hh = int(hole[2]-hole[0]), int(hole[3]-hole[1])
    hw -= hw % 2; hh -= hh % 2
    if k == 'window':
        cw, ch, cx, cy = vlib.window_crop(hh)
        src = ['-ss',f'{t0:.4f}','-i',BASE]
        prep = f'[0:v]crop={cw}:{ch}:{cx}:{cy},scale={hw}:{hh}:flags=lanczos,setsar=1[m]'
    else:
        src = media_input(b['media'], nfr)
        prep = f'[0:v]{cover_chain(hw,hh)}[m]'
    run([FF,'-v','error','-y'] + src + ['-i',plate,
        '-filter_complex', f'color=black:s={VW}x{VH}:r=30000/1001[bg];{prep};'
                           f'[bg][m]overlay={hx}:{hy}[u];[u][1:v]overlay=0:0:shortest=1'] + common)

def main():
    tl, ov = beats.timeline()
    prev, plan = 0, []
    for b in tl:
        cum = round(b['t1']*FPS); plan.append((b, cum-prev)); prev = cum
    for i, (b, nfr) in enumerate(plan):
        render_segment(i, b, nfr, b['t0'])
        print(f'{i:3d} {b["kind"]:10s} {nfr:5d}f  {b.get("media") or b.get("header") or ""}', flush=True)
    with open('out/list.txt','w') as f:
        for i in range(len(plan)): f.write(f'file s{i:03d}.mp4\n')
    run([FF,'-v','error','-y','-f','concat','-safe','0','-i','out/list.txt','-c','copy','picture_raw.mp4'])
    # --- overlays (CTA pill, callout box) sit ON the picture ------------------
    ins, fc, idx = ['-i','picture_raw.mp4'], [], 1
    last = '0:v'
    for n, b in enumerate(ov):
        mov = f'gfx/ov{n:02d}.mov'
        d = b['t1']-b['t0']
        if not os.path.exists(mov):
            if b['kind'] == 'cta':
                fr, _ = vlib.overlay_cta(b['top'], b['big'], d)
            else:
                x0,y0,x1,y1 = b['rect_src']            # source-frame coords -> vertical frame
                sx = VW/608.0; ox = 918-304
                fr, _ = vlib.overlay_callout(((x0-ox)*sx, y0*(VH/1080.0),
                                              (x1-ox)*sx, y1*(VH/1080.0)), d)
            encode(fr, mov, alpha=True)
        ins += ['-i', mov]
        fc.append(f'[{last}][{idx}:v]overlay=0:0:enable=\'between(t,{b["t0"]:.3f},{b["t1"]:.3f})\''
                  f':eof_action=pass[o{n}]')
        last = f'o{n}'; idx += 1
    run([FF,'-v','error','-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', f'[{last}]',
         '-r','30000/1001','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',
         '-an','picture.mp4'])
    print('picture.mp4 done')

if __name__ == '__main__':
    main()
