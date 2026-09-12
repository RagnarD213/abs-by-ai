#!/usr/bin/env python3
"""Render the 1:1 SQUARE picture for Ad 1: one output segment per beat, concat, overlays.

This is the approved 9:16 `render.py` with the GEOMETRY changed and nothing else. The beat
sheet, the push schedule, the flash windows, the lower thirds, the CTA pills and the grade
are the ones Dan approved in the vertical; `sqlib.py` holds the 1:1 layouts and
`sqassets.py` decides each media's square treatment and its label.

Three things this file does that the vertical's did not:

  * THE TALKING HEAD IS A 1080x1080 CROP OF THE 1080p SOURCE AT 1.00x. The vertical is
    forced into a 1.78x upscale (608x1080 -> 1080x1920); the square needs no upscale at
    all, which also halves the on-screen amplification of Dan's lean.
  * EVERY CACHE IS CONTENT-ADDRESSED -- segments AND plates. The vertical's `out/s{i}.mp4`
    and `gfx/p{i}.mov` are keyed by INDEX, which is the bug that shipped an 8,265-frame
    Ad 2 master against a 8,275-frame plan (a stale plate is short, and `shortest=1`
    truncates the beat) and served the previous beat's picture after two beats were
    removed. The key here is a hash of the beat spec + duration + frame count + start.
  * FULL-BLEED AND FULL-HEIGHT BEATS CARRY A LABEL. The vertical had no label mechanism
    outside the olive card, which is how the photoshop gag ran 5 s unlabelled (A6.19b).

Frame counts are CUMULATIVE, never per-segment: rounding each segment on its own puts
~16 ms of overshoot into every cut and walks the picture off the audio by the end.
"""
import hashlib, json, os, subprocess, sys
sys.path.insert(0, '.')
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared')
import sqlib as V, beats, sqassets
from assets import MEDIA
from motionlib import encode
from PIL import Image
import numpy as np

# ⚠⚠ THE CACHE KEY MUST COVER THE LAYOUT LIBRARY, NOT JUST THE BEAT SPEC.
# The first square master shipped its FIRST bullet screen at the rejected "whole room"
# geometry while the other three carried the fixed one: `sqlib.window_rect` changed after
# a test render had already written that beat's plate, the beat spec had not changed, and
# the content-addressed key handed back the stale plate AND its stale hole rectangle.
# Dan's ear-to-ear width came out 176 px in that window against 226-229 px in the rest --
# found by the independent audit, invisible to every gate (finding F3, 2026-09-11). This is
# the fourth cache-key lesson in this skill: index, media spec, media aspect, and now the
# LAYOUT the plate was drawn with.
LAYOUT_SIG = hashlib.md5(
    b''.join(open(f, 'rb').read() for f in ('sqlib.py', 'sqassets.py'))).hexdigest()[:8]

FF  = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP  = FF.replace('ffmpeg', 'ffprobe')
FPS = 30000/1001
VW, VH = 1080, 1080
BASE = 'base.mp4'
SRC_W, SRC_H = 1920, 1080
CROP_W = 1080                      # 1.00x -- the whole point of the square
PUSH_UP = 85.0                     # his punch recentres 85 px up in the 1080 source
for d in ('out', 'gfx', 'logs', '_sq'): os.makedirs(d, exist_ok=True)

# --- vignettes, re-derived in the SQUARE frame's own coordinates -------------
if not os.path.exists('vignette_sq.png'):
    m = (V.vignette_mask()*255).clip(0, 255).astype('uint8')
    Image.fromarray(np.dstack([m]*3)).save('vignette_sq.png')
if not os.path.exists('vignette_sq_soft.png'):
    v = V.vignette_mask()
    m = ((1 - (1-v)*0.25)*255).clip(0, 255).astype('uint8')
    Image.fromarray(np.dstack([m]*3)).save('vignette_sq_soft.png')
if not os.path.exists('field_sq.png'):
    V.field().save('field_sq.png')

# blend must run in RGB. On yuv420p it multiplies the CHROMA planes about their 128 offset
# as if they were luma, which turns every footage frame bright green.
VIG = ('[v0]format=gbrp[v0f];[vg]format=gbrp[vgf];'
       '[v0f][vgf]blend=all_mode=multiply,format=yuv420p')


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(' '.join(str(c) for c in cmd[:60]), '\n', r.stderr[-2000:]); raise SystemExit(1)


def nframes_of(path):
    j = json.loads(subprocess.run([FP, '-v', 'error', '-select_streams', 'v', '-count_frames',
        '-show_entries', 'stream=nb_read_frames', '-of', 'json', path],
        capture_output=True, text=True).stdout)['streams'][0]
    return int(j['nb_read_frames'])


# ---------------------------------------------------------------- chains
def cover_chain(w, h, ox=0.5, oy=0.5):
    """Fill (w,h) cropping the overflow, with the crop window placed by ox/oy -- a centred
    window slices whatever sits at the sides, and on a standing photo that is his head."""
    return (f'scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,'
            f"crop={w}:{h}:'(iw-{w})*{ox:.3f}':'(ih-{h})*{oy:.3f}',setsar=1")

def still_chain(w, h, nfr, amt=0.055, ox=0.5, oy=0.5, anchor_top=False):
    """A still must never sit dead-frozen: his own title card measures 0/101 static frames.
    `ox`/`oy` place the crop window -- a centred window on a standing photo takes his head.

    ⚠ `anchor_top` ANCHORS THE PUSH AT THE TOP. A centred push eats the frame equally from
    every side, so on a photo whose subject already sits near the top edge it takes his
    crown: measured on `today_trees`, the person mask's top went 14 px -> 1 px -> 0 px
    (CUT) across the beat's 29 frames, on a REAL after picture (audit finding F4). Anchored
    at the top the headroom is fixed for the whole beat and the push eats the bottom, where
    there is slack."""
    ow, oh = int(w*1.14) - int(w*1.14) % 2, int(h*1.14) - int(h*1.14) % 2
    ye = "0" if anchor_top else "(ih-ih/zoom)/2"
    return (f'scale={ow}:{oh}:force_original_aspect_ratio=increase:flags=lanczos,'
            f"crop={ow}:{oh}:'(iw-{ow})*{ox:.3f}':'(ih-{oh})*{oy:.3f}',setsar=1,"
            f"zoompan=z='1+{amt:.4f}*on/{max(1,nfr-1)}':x='(iw-iw/zoom)/2':"
            f"y='{ye}':d=1:s={w}x{h}:fps=30000/1001")

def push_z_expr(t0, t1):
    T = f'({t0:.4f}+on/{FPS:.6f})'
    rs = []
    for a1, a2, b1, b2 in beats.PUSHES:
        if b2 <= t0 or a1 >= t1: continue
        kin  = '1' if a2 <= a1 else f'clip(({T}-{a1:.3f})/{a2-a1:.4f},0,1)'
        kout = '0' if b2 <= b1 else f'clip(({T}-{b1:.3f})/{b2-b1:.4f},0,1)'
        rs.append(f'(if(lt({T},{a1:.3f}),0,min({kin},1-{kout})))')
    if not rs: return None
    r = rs[0]
    for x in rs[1:]: r = f'max({r},{x})'
    return f'1+{beats.PUSH_Z-1:.3f}*({r})*({r})*(3-2*({r}))'

# Dan LEANS through this locked-off roll (face x wanders 835..1037 in the 1920 conform), so
# a fixed crop leaves him off-centre. The crop follows the same smoothed face track the
# approved vertical uses -- at 1.00x its excursion on screen is 1920/1080 = 1.78x SMALLER
# than in the vertical, which is the square's second free advantage.
CXT = json.load(open('cx_track.json'))
def cx_at(t):
    a = CXT['cx']
    i = min(len(a)-1, max(0, t*CXT['fps']))
    j = int(i)
    return a[j] + (a[min(j+1, len(a)-1)]-a[j])*(i-j)

def crop_x_knots(t0, t1, w=CROP_W):
    ts = [t0 + k*0.75 for k in range(int((t1-t0)/0.75)+2)]
    xs = [max(0.0, min(float(SRC_W-w), cx_at(t)-w/2)) for t in ts]
    return ts, xs

def crop_x_expr(t0, t1, w=CROP_W):
    """Piecewise-linear crop x over the beat (local time), knots every 0.75 s.

    ⚠ THE CHAIN IS WRAPPED IN REVERSE. Assembled forwards, the LAST interval becomes the
    OUTERMOST test and every earlier frame evaluates the last line equation extrapolated
    backwards -- 316 px off for twelve seconds on Ad 2, and nothing upstream can see it.
    `selftest()` below evaluates the string the way ffmpeg does and diffs it against the
    track."""
    ts, xs = crop_x_knots(t0, t1, w)
    if max(xs)-min(xs) < 3: return f'{xs[0]:.1f}'
    expr = f'{xs[-1]:.1f}'
    for k in range(len(ts)-2, -1, -1):
        a, b = ts[k]-t0, ts[k+1]-t0
        xa, xb = xs[k], xs[k+1]
        expr = f'if(lt(t,{b:.3f}),{xa:.1f}+({xb-xa:.1f})*(t-{a:.3f})/{b-a:.3f},{expr})'
    return expr

def talk_chain(t0, t1):
    """1080x1080 crop of the conform at 1.00x + his push schedule. No upscale."""
    z = push_z_expr(t0, t1)
    base = f"crop={CROP_W}:{SRC_H}:'{crop_x_expr(t0, t1)}':0"
    if z is None:
        return f'{base},setsar=1'
    return (f"{base},zoompan=z='{z}':x='(iw-iw/zoom)/2':"
            f"y='(ih-ih/zoom)/2-{PUSH_UP:.1f}*(zoom-1)/{beats.PUSH_Z-1:.3f}':"
            f"d=1:s={VW}x{VH}:fps=30000/1001,unsharp=5:5:0.35:5:5:0.0,setsar=1")


# ---------------------------------------------------------------- media
def media_input(key, nfr):
    spec = MEDIA[key]
    if spec[0] == 'img':
        return ['-loop', '1', '-framerate', f'{FPS:.6f}', '-t', f'{nfr/FPS+0.25:.4f}', '-i', spec[1]]
    return ['-ss', f'{spec[2]:.3f}', '-stream_loop', '4', '-i', spec[1]]

_AR = {}
def media_ar(key):
    """Aspect ratio from the FILE. A fixed 16:9 hole cover-crops a portrait photo, and what
    it crops off a photo of a person is their head."""
    if key in _AR: return _AR[key]
    o = subprocess.run([FP, '-v', 'error', '-select_streams', 'v', '-show_entries',
                        'stream=width,height', '-of', 'csv=p=0:s=x', MEDIA[key][1]],
                       capture_output=True, text=True).stdout.strip().split('\n')[0]
    w, h = (int(x) for x in o.split('x')[:2])
    _AR[key] = w/h
    return _AR[key]


# ---------------------------------------------------------------- label chips
def chip_png(label_kind, cover_box=None):
    """One static PNG per label, content-addressed. `cover_box` forces the chip to fully
    cover a chip that is already burned into the media (the hook's goal video)."""
    txt = V.REAL_LABEL if label_kind == 'real' else V.AI_LABEL
    sig = hashlib.md5(repr((txt, cover_box, V.CAP_Y)).encode()).hexdigest()[:8]
    p = f'gfx/chip_{label_kind}_{sig}.png'
    if os.path.exists(p): return p
    if cover_box:
        from PIL import ImageDraw
        from motionlib import font, text_size
        x0, y0, x1, y1 = cover_box
        lay = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
        f = font(40, "SemiBold")
        while f.size > 22 and text_size(txt, f)[0] + 40 > VW - 2*40:
            f = font(f.size-2, "SemiBold")
        lw, lh = text_size(txt, f)
        bw, bh = max(lw + 40, x1 - x0 + 24), max(lh + 26, y1 - y0 + 8)
        bx, by = (VW - bw)//2, int((y0 + y1)/2 - bh/2)
        assert bx <= x0 and bx + bw >= x1 and by <= y0 and by + bh >= y1, \
            f'chip {bx},{by},{bx+bw},{by+bh} does not cover the burned chip {cover_box}'
        d = ImageDraw.Draw(lay)
        d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=10, fill=(0, 0, 0, 255))
        d.text(((VW-lw)//2, by + (bh-lh)//2), txt, font=f, fill=V.INK, anchor="lt")
    else:
        lay = V.bleed_chip(txt)
    lay.save(p)
    return p


# ---------------------------------------------------------------- one segment
def seg_key(b, nfr, t0):
    spec = {k: v for k, v in sorted(b.items())}
    if b.get('media'):
        spec['_sq'] = sorted(sqassets.treat(b['media']).items())
        spec['_ar'] = round(media_ar(b['media']), 5)
    return hashlib.md5(repr((spec, nfr, round(t0, 4), 'sq2', LAYOUT_SIG)).encode()).hexdigest()[:12]


def render_segment(i, b, nfr, t0):
    """⚠ CONTENT-ADDRESSED, not index-keyed: the cache key covers the beat spec, its square
    treatment, the media's aspect, the frame count and the start time."""
    key = seg_key(b, nfr, t0)
    out = f'out/s_{key}.mp4'
    if not (os.path.exists(out) and os.path.getsize(out) > 20000):
        _render(out, b, nfr, t0)
    got = nframes_of(out)
    assert got == nfr, f'beat {i} ({b["kind"]}) is {got} frames, planned {nfr}'
    return out


def _render(out, b, nfr, t0):
    k, dur = b['kind'], nfr/FPS
    common = ['-r', '30000/1001', '-frames:v', str(nfr), '-c:v', 'libx264', '-preset', 'medium',
              '-crf', '16', '-pix_fmt', 'yuv420p', '-an',
              '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', out]

    if k == 'talk':
        run([FF, '-nostdin', '-v', 'error', '-y', '-ss', f'{t0:.4f}', '-i', BASE,
             '-loop', '1', '-framerate', '30000/1001', '-i', 'vignette_sq.png',
             '-filter_complex', f'[0:v]{talk_chain(t0, b["t1"])}[v0];'
                                f'[1:v]scale={VW}:{VH}[vg];{VIG}'] + common)
        return

    T = sqassets.treat(b['media']) if b.get('media') else None

    # ---- full-bleed 1:1 cover -------------------------------------------------
    if T and T['mode'] == 'cover':
        ch = (still_chain(VW, VH, nfr, amt=0.045, ox=T['ox'], oy=T['oy'],
                          anchor_top=T.get('anchor_top', False))
              if MEDIA[b['media']][0] == 'img'
              else 'setpts=PTS-STARTPTS,' + cover_chain(VW, VH, T['ox'], T['oy']))
        ins = media_input(b['media'], nfr) + \
              ['-loop', '1', '-framerate', '30000/1001', '-i', 'vignette_sq_soft.png']
        fc = f'[0:v]{ch},unsharp=5:5:0.4:5:5:0.0[v0];[1:v]scale={VW}:{VH}[vg];{VIG}[vv]'
        idx = 2
        if T['label']:
            ins += ['-loop', '1', '-framerate', '30000/1001', '-i', chip_png(T['label'])]
            fc += f';[vv][{idx}:v]overlay=0:0:shortest=1'
        else:
            fc += ';[vv]null'
        run([FF, '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', fc] + common)
        return

    # ---- full HEIGHT on the field (square rule 4) -----------------------------
    if T and T['mode'] == 'fith':
        ar = media_ar(b['media'])
        w = int(round(VH*ar)); w -= w % 2
        x = (VW - w)//2
        chain = (still_chain(w, VH, nfr, amt=0.05) if MEDIA[b['media']][0] == 'img'
                 else f'setpts=PTS-STARTPTS,scale={w}:{VH}:flags=lanczos,setsar=1')
        ins = ['-loop', '1', '-framerate', '30000/1001', '-t', f'{dur+0.25:.4f}', '-i', 'field_sq.png'] \
              + media_input(b['media'], nfr)
        fc = (f'[1:v]{chain},unsharp=5:5:0.4:5:5:0.0[m];'
              f'[0:v]scale={VW}:{VH},setsar=1[bg];[bg][m]overlay={x}:0[vv]')
        idx = 2
        if T['label']:
            ins += ['-loop', '1', '-framerate', '30000/1001', '-i',
                    chip_png(T['label'], T.get('cover_chip'))]
            fc += f';[vv][{idx}:v]overlay=0:0:shortest=1'
        else:
            fc += ';[vv]null'
        run([FF, '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', fc] + common)
        return

    # ---- plated beats ---------------------------------------------------------
    pkey = hashlib.md5(repr((sorted(b.items()),
                             round(media_ar(b['media']), 5) if b.get('media') else None,
                             nfr, 'sq2', LAYOUT_SIG)).encode()).hexdigest()[:12]
    plate = f'gfx/p_{pkey}.mov'
    meta  = plate + '.json'
    if not os.path.exists(plate) or not os.path.exists(meta):
        lbl = T['label'] if T else None
        lbl_txt = (V.REAL_LABEL if lbl == 'real' else V.AI_LABEL) if lbl else None
        if k == 'window':
            fr, hole = V.plate_window(b.get('header'), b['bullets'], dur)
            holes = {'dan': hole}
        elif k == 'stmt':
            fr, hole = V.plate_stmt_window(b['parts'], dur)
            holes = {'dan': hole}
        elif k in ('winmedia',) or (T and T['mode'] == 'sbs'):
            fr, rect, mh = V.plate_window_media(dur, media_ar(b['media']), dan_left=False)
            holes = {'dan': rect, 'media': mh}
        elif k in ('card', 'bleed'):
            fr, hole = V.plate_card(dur, caption=b.get('caption'), label=lbl_txt,
                                    top_kicker=b.get('kicker'), media_ar=media_ar(b['media']))
            holes = {'media': hole}
        elif k == 'title':
            fr, hole = V.plate_title_card(b['headline'], b.get('sub'), dur)
            holes = {}
        else:
            raise ValueError(k)
        # ⚠ pad to the PLANNED frame count. A plate 10 frames short TRUNCATES the beat,
        # because a card is muxed with shortest=1 -- and every duration check still passes.
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
        bcx = float(np.median([cx_at(t0 + q*0.25) for q in range(int((b['t1']-t0)/0.25)+1)]))
        cw, ch, cx, cy = V.window_crop(w, h, cx=bcx)
        # setpts=PTS-STARTPTS is not optional: a seeked input's first frame carries a pts
        # above zero, so overlay's frame 0 composites only the background and the segment
        # OPENS ON ONE BLACK FRAME.
        ins += ['-ss', f'{t0:.4f}', '-i', BASE]
        prep.append(f'[{idx}:v]setpts=PTS-STARTPTS,crop={cw}:{ch}:{cx}:{cy},'
                    f'scale={w}:{h}:flags=lanczos,unsharp=5:5:0.4:5:5:0.0,setsar=1[m{idx}]')
        over.append((idx, x, y)); idx += 1
    if 'media' in holes:
        x, y, w, h = hole_args('media')
        ins += media_input(b['media'], nfr)
        chain = (still_chain(w, h, nfr) if MEDIA[b['media']][0] == 'img'
                 else 'setpts=PTS-STARTPTS,' + cover_chain(w, h))
        prep.append(f'[{idx}:v]{chain}[m{idx}]')
        over.append((idx, x, y)); idx += 1
    ins += ['-i', plate]
    fc = [f'color=black:s={VW}x{VH}:r=30000/1001[bg]']
    fc += prep
    last = 'bg'
    for n, (j, x, y) in enumerate(over):
        fc.append(f'[{last}][m{j}]overlay={x}:{y}[u{n}]'); last = f'u{n}'
    if k == 'title':
        fc.append(f'[{last}][{idx}:v]overlay=0:0:shortest=1,'
                  f"zoompan=z='1+0.028*on/{max(1,nfr-1)}':x='(iw-iw/zoom)/2':"
                  f"y='(ih-ih/zoom)/2':d=1:s={VW}x{VH}:fps=30000/1001")
    else:
        fc.append(f'[{last}][{idx}:v]overlay=0:0:shortest=1')
    run([FF, '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc)] + common)


# ---------------------------------------------------------------- self-test
def selftest():
    """Evaluate crop_x_expr the way ffmpeg does and diff it against the track. This is the
    check whose absence cost two rejected Ad-2 versions."""
    import re
    def ev(expr, t):
        expr = expr.strip()
        while expr.startswith('if(lt(t,'):
            m = re.match(r'if\(lt\(t,([\d.]+)\),(.*)', expr)
            cut = float(m.group(1)); rest = m.group(2)
            depth = 0
            for i, c in enumerate(rest):
                if c == '(': depth += 1
                elif c == ')': depth -= 1
                elif c == ',' and depth == 0:
                    then, els = rest[:i], rest[i+1:-1]; break
            if t < cut: return eval(then.replace('t', f'({t})'))
            expr = els.strip()
        return float(eval(expr.replace('t', f'({t})')))
    tl, _ = beats.timeline()
    worst = 0.0; where = None
    for b in tl:
        if b['kind'] != 'talk': continue
        e = crop_x_expr(b['t0'], b['t1'])
        ts, xs = crop_x_knots(b['t0'], b['t1'])
        n = int((b['t1']-b['t0'])*FPS)
        for f in range(0, n, 3):
            t = f/FPS
            want = np.interp(b['t0']+t, ts, xs)
            got = ev(e, t)
            if abs(got-want) > worst: worst, where = abs(got-want), (b['t0'], t)
    print(f'crop-expression self-test: worst |expr - track| = {worst:.2f} px at {where}')
    assert worst < 1.0, 'the crop expression does not evaluate to the track'
    return worst


def main():
    if '--selftest' in sys.argv:
        selftest(); return
    selftest()
    tl, ov = beats.timeline()
    prev, plan = 0, []
    for b in tl:
        cum = round(b['t1']*FPS); plan.append((b, cum-prev)); prev = cum
    total = sum(n for _, n in plan)
    print(f'{len(plan)} beats, {total} frames planned ({total/FPS:.3f}s)')
    paths = []
    for i, (b, nfr) in enumerate(plan):
        paths.append(render_segment(i, b, nfr, b['t0']))
        det = b.get('media') or b.get('header') or b.get('headline') or ''
        print(f'{i:3d} {b["kind"]:9s} {nfr:5d}f  {det}', flush=True)
    # the concat list names the CONTENT-ADDRESSED files: nothing is keyed on an index, so a
    # changed beat can never serve its neighbour's picture (the Ad 2 cache bug, twice)
    with open('out/list.txt', 'w') as f:
        for p_ in paths: f.write(f'file {os.path.basename(p_)}\n')
    run([FF, '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'out/list.txt',
         '-c', 'copy', 'picture_raw.mp4'])
    got = nframes_of('picture_raw.mp4')
    assert got == total, f'concat is {got} frames, plan is {total}'

    # ---- overlays: lower thirds and CTA pills (alpha), then HIS flash (screen) ----
    tmpl = 'gfx/flash_tmpl_sq.mp4'
    if not os.path.exists(tmpl):
        run([FF, '-nostdin', '-v', 'error', '-y', '-framerate', '30000/1001',
             '-i', '_flash/final/L%02d.png', '-vf', f'scale={VW}:{VH}:flags=lanczos',
             '-c:v', 'libx264', '-preset', 'medium', '-crf', '12', '-pix_fmt', 'yuv420p', tmpl])
    ins, fc, idx, last = ['-i', 'picture_raw.mp4'], [], 1, '0:v'
    items = sorted([(b['kind'], b['t0'], b['t1'], b) for b in ov], key=lambda x: x[1])
    for n, (kind, a, b2, spec) in enumerate(items):
        sig = hashlib.md5(repr((kind, round(b2-a, 3), sorted(spec.items()), 'sq2', LAYOUT_SIG))
                          .encode()).hexdigest()[:8]
        mov = f'gfx/ov_{kind}_{sig}.mov'
        d = b2 - a
        if not os.path.exists(mov):
            if kind == 'cta':     fr, _ = V.overlay_cta(spec['top'], spec['big'], d)
            elif kind == 'inset': fr, _ = V.overlay_inset_photo(MEDIA[spec['media']][1], d)
            else:                 fr, _ = V.overlay_lower_third(spec['lines'], d)
            encode(fr, mov, alpha=True)
        ins += ['-i', mov]
        # ⚠ SHIFTED onto the main timeline, not just gated onto it. `enable=between(t,a,b)`
        # alone gates by the MAIN clock while overlay keeps consuming the secondary stream
        # from ITS own t=0, so by the time the window opens the overlay has run out and
        # NOTHING EVER APPEARS -- seven lower thirds, three pills and eleven flashes, with
        # every metric still green.
        fc.append(f"[{idx}:v]setpts=PTS+{a:.4f}/TB[s{n}];"
                  f"[{last}][s{n}]overlay=0:0:enable='between(t,{a:.3f},{b2:.3f})'"
                  f":eof_action=pass[o{n}]")
        last = f'o{n}'; idx += 1
    dur = sum(b['t1']-b['t0'] for b in tl)
    fc.insert(0, f'color=black:s={VW}x{VH}:r=30000/1001:d={dur:.4f}[lk0]')
    lk = 'lk0'
    for m, (a, b2) in enumerate(beats.FLASHES):
        t0 = a + 0.11 - 8/FPS               # template peak (idx 8) lands at a+0.11
        ins += ['-i', tmpl]
        fc.append(f"[{idx}:v]setpts=PTS+{t0:.4f}/TB[f{m}];"
                  f"[{lk}][f{m}]overlay=0:0:enable='between(t,{t0:.3f},{t0+32/FPS:.3f})'"
                  f":eof_action=pass[lk{m+1}]")
        lk = f'lk{m+1}'; idx += 1
    fc.append(f'[{last}]format=gbrp[px];[{lk}]format=gbrp[lx];'
              f'[px][lx]blend=all_mode=screen,format=yuv420p[outv]')
    run([FF, '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc),
         '-map', '[outv]', '-r', '30000/1001', '-c:v', 'libx264', '-preset', 'medium',
         '-crf', '16', '-pix_fmt', 'yuv420p', '-frames:v', str(total),
         '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
         '-an', 'picture.mp4'])
    got = nframes_of('picture.mp4')
    assert got == total, f'picture.mp4 is {got} frames, plan is {total}'
    print(f'picture.mp4 done -- {got} frames')


if __name__ == '__main__':
    main()
