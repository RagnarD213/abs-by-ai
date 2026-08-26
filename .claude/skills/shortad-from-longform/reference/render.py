#!/usr/bin/env python3
"""Render the 9:16 picture: one output segment per beat, concat, then the overlays.

Two things attempt 1 did not do:
  * the talking head PUSHES IN AND OUT fourteen times (beats.PUSHES). Attempt 1 rendered
    every talk segment at one fixed crop, which is what made a locked-off tripod shot
    read as a static webcam recording with 72 bare trims in it.
  * ten of his beat changes are covered by a WHITE LIGHT-LEAK FLASH, not a hard cut.

Frame counts are CUMULATIVE, not per-segment: rounding each segment on its own puts ~16 ms
of overshoot into every cut and walks the picture off the audio by the end.
"""
import json, os, subprocess, sys
sys.path.insert(0, '.')
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared')
import vlib, beats
from assets import MEDIA
from motionlib import encode, font, text_size
from PIL import Image, ImageDraw
import numpy as np

FF  = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001
VW, VH = 1080, 1920
BASE = 'base.mp4'
CROP_W, CROP_X = 608, 918-304          # Dan's head centre, measured at x=918 (sd 18 px)
PUSH_UP = 85.0                          # his punch recentres 85 px up in the 1080 source
os.makedirs('out', exist_ok=True); os.makedirs('gfx', exist_ok=True)

# TWO vignettes, not one. The profile in grade.py was fitted as his render divided by our
# toned conform ON TALKING-HEAD FRAMES, so it is the difference he added ON TOP of the
# room's own falloff -- correct for the talking head, and much too strong for anything
# else. Measured on his own b-roll (living-room abs) the corner sits at 0.95 of centre,
# i.e. he barely vignettes footage at all; at full strength ours turned the beach and the
# salad shots into portholes.
if not os.path.exists('vignette.png'):
    m = (vlib.vignette_mask()*255).clip(0, 255).astype('uint8')
    Image.fromarray(np.dstack([m]*3)).save('vignette.png')
if not os.path.exists('vignette_soft.png'):
    v = vlib.vignette_mask()
    m = ((1 - (1-v)*0.25)*255).clip(0, 255).astype('uint8')
    Image.fromarray(np.dstack([m]*3)).save('vignette_soft.png')

# blend must run in RGB. On yuv420p it multiplies the CHROMA planes about their 128
# offset as if they were luma, which turns every footage frame bright green.
VIG = ('[v0]format=gbrp[v0f];[vg]format=gbrp[vgf];'
       '[v0f][vgf]blend=all_mode=multiply,format=yuv420p')

def cover_chain(w, h):
    return (f'scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,'
            f'crop={w}:{h},setsar=1')

# A 16:9 clip in a 9:16 card leaves two-thirds of the phone empty. Cropping these four to
# 4:5 first makes the card 992x1240 -- a 1.72x upscale, the same as the talking head's own
# 1.78x -- instead of 992x558 floating in a field. (His run full frame; ours are 1280x720
# and full bleed would be 2.67x.)
NARROW = {'ai_women_pool': 0.80, 'ai_respect_gym': 0.80, 'ai_beachrun': 0.80,
          'ai_busydad': 0.80, 'bodybuilder': 0.80, 'outdoor_abs': 4/3}
# dad_kids stays at its native 4:3: a 4:5 crop of it cuts the top of Dan's head off, which
# is exactly what the 'match the hole to the MEDIA' rule exists to prevent.

def still_chain(w, h, nfr, amt=0.055):
    """A still in a card must not sit dead-frozen: his photo cards all carry a slow push
    (measured on his 0:48 fitness-model card, which grows over its 2.5 s). The watch pass
    on attempt 2's first render found twelve card beats frozen solid; this is the fix."""
    ow, oh = int(w*1.14) - int(w*1.14) % 2, int(h*1.14) - int(h*1.14) % 2
    return (f'scale={ow}:{oh}:force_original_aspect_ratio=increase:flags=lanczos,'
            f'crop={ow}:{oh},setsar=1,'
            f"zoompan=z='1+{amt:.4f}*on/{max(1,nfr-1)}':x='(iw-iw/zoom)/2':"
            f"y='(ih-ih/zoom)/2':d=1:s={w}x{h}:fps=30000/1001")

def push_z_expr(t0, t1):
    """zoompan `z` for this beat: 1.00 wide .. 1.20 punched, smoothstepped over his ramps.
    Only the pushes that actually touch the beat are compiled in."""
    T = f'({t0:.4f}+on/{FPS:.6f})'
    rs = []
    for a1, a2, b1, b2 in beats.PUSHES:
        if b2 <= t0 or a1 >= t1: continue
        kin  = '1' if a2 <= a1 else f'clip(({T}-{a1:.3f})/{a2-a1:.4f},0,1)'
        kout = '0' if b2 <= b1 else f'clip(({T}-{b1:.3f})/{b2-b1:.4f},0,1)'
        rs.append(f'(if(lt({T},{a1:.3f}),0,min({kin},1-{kout})))')
    if not rs: return None
    r = rs[0] if len(rs) == 1 else 'max(' + ','.join(rs) + ')' if len(rs) == 2 else \
        'max(' + rs[0] + ',' + ','.join(rs[1:]) + ')'
    if len(rs) > 2:
        r = rs[0]
        for x in rs[1:]: r = f'max({r},{x})'
    return f'1+{beats.PUSH_Z-1:.3f}*({r})*({r})*(3-2*({r}))'

def talk_chain(t0, t1):
    """9:16 crop of the conform + his push schedule. Crop first at native resolution, so
    zoompan only ever works inside the 608x1080 window we actually use."""
    z = push_z_expr(t0, t1)
    base = f'crop={CROP_W}:1080:{CROP_X}:0'
    if z is None:
        return f'{base},scale={VW}:{VH}:flags=lanczos,unsharp=5:5:0.85:5:5:0.0'
    return (f"{base},zoompan=z='{z}':x='(iw-iw/zoom)/2':"
            f"y='(ih-ih/zoom)/2-{PUSH_UP:.1f}*(zoom-1)/{beats.PUSH_Z-1:.3f}':"
            f"d=1:s={VW}x{VH}:fps=30000/1001,unsharp=5:5:0.85:5:5:0.0")

def media_input(key, nfr):
    spec = MEDIA[key]
    if spec[0] == 'img':
        return ['-loop', '1', '-framerate', f'{FPS:.6f}', '-t', f'{nfr/FPS+0.25:.4f}', '-i', spec[1]]
    return ['-ss', f'{spec[2]:.3f}', '-stream_loop', '4', '-i', spec[1]]

_AR = {}
def media_ar(key):
    """Aspect ratio from the FILE. A fixed 16:9 hole cover-crops a portrait photo, and
    what it crops off a photo of a person is their head."""
    if key in _AR: return _AR[key]
    o = subprocess.run([FF.replace('ffmpeg','ffprobe'), '-v','error','-select_streams','v',
                        '-show_entries','stream=width,height','-of','csv=p=0:s=x', MEDIA[key][1]],
                       capture_output=True, text=True).stdout.strip().split('\n')[0]
    w, h = (int(x) for x in o.split('x')[:2])
    _AR[key] = NARROW.get(key, w/h)
    return _AR[key]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(' '.join(str(c) for c in cmd[:60]), '\n', r.stderr[-1800:]); raise SystemExit(1)

def render_segment(i, b, nfr, t0):
    out = f'out/s{i:03d}.mp4'
    if os.path.exists(out) and os.path.getsize(out) > 20000: return
    k, dur = b['kind'], nfr/FPS
    common = ['-r','30000/1001','-frames:v',str(nfr),'-c:v','libx264','-preset','medium',
              '-crf','16','-pix_fmt','yuv420p','-an', out]
    if k == 'talk':
        run([FF,'-v','error','-y','-ss',f'{t0:.4f}','-i',BASE,
             '-loop','1','-framerate','30000/1001','-i','vignette.png',
             '-filter_complex', f'[0:v]{talk_chain(t0, b["t1"])}[v0];'
                                f'[1:v]scale={VW}:{VH}[vg];{VIG}'] + common)
        return
    if k == 'bleed':
        run([FF,'-v','error','-y'] + media_input(b['media'], nfr) +
            ['-loop','1','-framerate','30000/1001','-i','vignette_soft.png',
             '-filter_complex', f'[0:v]{cover_chain(VW,VH)},unsharp=5:5:0.4:5:5:0.0[v0];'
                                f'[1:v]scale={VW}:{VH}[vg];{VIG}'] + common)
        return
    # ---- plated beats --------------------------------------------------------
    plate = f'gfx/p{i:03d}.mov'
    meta  = plate + '.json'
    if not os.path.exists(plate):
        if k == 'window':
            fr, hole = vlib.plate_window(b.get('header'), b['bullets'], dur)
            holes = {'dan': hole}
        elif k == 'stmt':
            fr, hole = vlib.plate_stmt_window(b['parts'], dur)
            holes = {'dan': hole}
        elif k == 'winmedia':
            fr, rect, mh = vlib.plate_window_media(dur, media_ar(b['media']))
            holes = {'dan': rect, 'media': mh}
        elif k == 'card':
            fr, hole = vlib.plate_card(dur, caption=b.get('caption'), label=b.get('label'),
                                       top_kicker=b.get('kicker'), media_ar=media_ar(b['media']))
            holes = {'media': hole}
        elif k == 'title':
            fr, hole = vlib.plate_title_card(b['headline'], b.get('sub'), dur)
            holes = {}
        else:
            raise ValueError(k)
        encode(fr[:nfr] + [fr[-1]]*max(0, nfr-len(fr)), plate, alpha=True)
        json.dump(holes, open(meta, 'w'))
    holes = json.load(open(meta))
    ins, prep, over, idx = [], [], [], 0
    def hole_args(name):
        h = holes[name]
        x, y = int(h[0]), int(h[1])
        w, hh = int(h[2]-h[0]), int(h[3]-h[1])
        return x, y, w - w % 2, hh - hh % 2
    if 'dan' in holes:
        x, y, w, h = hole_args('dan')
        cw, ch, cx, cy = vlib.window_crop(h)
        # setpts=PTS-STARTPTS is not optional here. A seeked input's first frame carries a
        # pts a little above zero, so overlay's frame 0 has only the black background to
        # composite and the segment opens on ONE BLACK FRAME. It cost five of them.
        ins += ['-ss', f'{t0:.4f}', '-i', BASE]
        prep.append(f'[{idx}:v]setpts=PTS-STARTPTS,crop={cw}:{ch}:{cx}:{cy},'
                    f'scale={w}:{h}:flags=lanczos,unsharp=5:5:0.5:5:5:0.0,setsar=1[m{idx}]')
        over.append((idx, x, y)); idx += 1
    if 'media' in holes:
        x, y, w, h = hole_args('media')
        ins += media_input(b['media'], nfr)
        # setpts=PTS-STARTPTS again: a seeked VIDEO in a card hole arrives one frame late
        # and the card opens on a black hole with only its AI-GENERATED chip in it.
        chain = still_chain(w, h, nfr) if MEDIA[b['media']][0] == 'img' else \
                'setpts=PTS-STARTPTS,' + cover_chain(w, h)
        prep.append(f'[{idx}:v]{chain}[m{idx}]')
        over.append((idx, x, y)); idx += 1
    ins += ['-i', plate]
    fc = [f'color=black:s={VW}x{VH}:r=30000/1001[bg]']
    fc += prep
    last = 'bg'
    for n, (j, x, y) in enumerate(over):
        fc.append(f'[{last}][m{j}]overlay={x}:{y}[u{n}]'); last = f'u{n}'
    fc.append(f'[{last}][{idx}:v]overlay=0:0:shortest=1')
    run([FF,'-v','error','-y'] + ins + ['-filter_complex', ';'.join(fc)] + common)

def main():
    tl, ov = beats.timeline()
    prev, plan = 0, []
    for b in tl:
        cum = round(b['t1']*FPS); plan.append((b, cum-prev)); prev = cum
    for i, (b, nfr) in enumerate(plan):
        render_segment(i, b, nfr, b['t0'])
        det = b.get('media') or b.get('header') or b.get('headline') or ''
        print(f'{i:3d} {b["kind"]:9s} {nfr:5d}f  {det}', flush=True)
    with open('out/list.txt','w') as f:
        for i in range(len(plan)): f.write(f'file s{i:03d}.mp4\n')
    run([FF,'-v','error','-y','-f','concat','-safe','0','-i','out/list.txt','-c','copy','picture_raw.mp4'])

    # ---- overlays: lower thirds, CTA pills, flashes --------------------------
    ins, fc, idx, last = ['-i','picture_raw.mp4'], [], 1, '0:v'
    items = [(b['kind'], b['t0'], b['t1'], b) for b in ov] + \
            [('flash', a, b, None) for a, b in beats.FLASHES]
    items.sort(key=lambda x: x[1])
    for n, (kind, a, b, spec) in enumerate(items):
        mov = f'gfx/ov{n:02d}_{kind}.mov'
        d = b - a
        if not os.path.exists(mov):
            if kind == 'cta':   fr, _ = vlib.overlay_cta(spec['top'], spec['big'], d)
            elif kind == 'lt':  fr, _ = vlib.overlay_lower_third(spec['lines'], d)
            else:               fr, _ = vlib.overlay_flash(d)
            encode(fr, mov, alpha=True)
        ins += ['-i', mov]
        # ⚠ AN OVERLAY MUST BE SHIFTED ONTO THE MAIN TIMELINE, NOT JUST GATED ONTO IT.
        # `enable=between(t,a,b)` alone gates by the MAIN clock while overlay keeps
        # consuming the secondary stream from ITS OWN t=0 -- so by the time the window
        # opens the overlay has already run out, repeatlast pins its last (transparent)
        # frame, and NOTHING EVER APPEARS. Attempt 2's first render lost all seven lower
        # thirds, all three CTA pills and all eleven flashes this way, and every metric
        # in qc.py still passed. Found by the watch pass.
        fc.append(f"[{idx}:v]setpts=PTS+{a:.4f}/TB[s{n}];"
                  f"[{last}][s{n}]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'"
                  f":eof_action=pass[o{n}]")
        last = f'o{n}'; idx += 1
    run([FF,'-v','error','-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', f'[{last}]',
         '-r','30000/1001','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',
         '-an','picture.mp4'])
    print('picture.mp4 done')

if __name__ == '__main__':
    main()
