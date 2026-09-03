#!/usr/bin/env python3
"""Render the 9:16 picture: one output segment per beat, concat, then the overlays.

Frame counts are CUMULATIVE, not per-segment: rounding each segment on its own puts ~16 ms
of overshoot into every cut and walks the picture off the audio by the end.

V2 (2026-09-03) changes:
  * the crop-x expression is a FLAT sum of clipped ramps, not nested if()s. ffmpeg's
    expression parser refuses more than ~100 nesting levels ("Missing ')' or too many
    args"), which is exactly what a 25 s talk beat at 0.25 s breakpoints produced -- the
    render after rev 3 died on beat 12 for that reason. A sum has no nesting at all.
  * `bleed2`: two full-bleed stills in one segment with his blur-through between them.
  * a media entry may carry a RATE (4th field): the clip is stretched, never looped.
  * --plan / --only i,j,k / --selftest for checking beats before the full render.
"""
import json, os, subprocess, sys, hashlib
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
CROP_W = 608
PUSH_UP = 85.0                          # his punch recentres 85 px up in the 1080 source

# The crop FOLLOWS a smoothed face track (facetrack2.py: Apple Vision torso anchor, smoothed
# inside each source-continuous segment, zero-phase, stepping at his splices).
_TRK = json.load(open('facetrack.json'))
_EDL = json.load(open('edl_picture.json'))   # HIS picture cuts, not the audio splices
_SPLICES = [q['cut_in'] for q in _EDL[1:]]
_SEGS = [(q['cut_in'], q['cut_out']) for q in _EDL]

def _seg_range(t):
    """Sample-index range [lo, hi] of the track samples inside t's own picture segment."""
    N = _TRK['n']
    for (sa, sb) in _SEGS:
        if sa - 1e-9 <= t < sb:
            n0, n1 = int(round(sa*FPS)), int(round(sb*FPS))
            lo = next((i for i, v in enumerate(N) if v >= n0), 0)
            hi = max(lo, max((i for i, v in enumerate(N) if v < n1), default=lo))
            return lo, hi
    return 0, len(N)-1

def _x_at(t):
    """Crop x at time t: linear interpolation between the two track samples that bracket t INSIDE
    t's own picture segment (samples are at exact frame indices; every segment has a sample on its
    first and its last frame, so a cut never interpolates across itself)."""
    N, X = _TRK['n'], _TRK['x']
    lo, hi = _seg_range(t)
    f = t*FPS
    if f <= N[lo]: return X[lo]
    if f >= N[hi]: return X[hi]
    j = lo
    while j < hi and N[j+1] <= f: j += 1
    if j >= hi: return X[hi]
    a, b = N[j], N[j+1]
    return X[j] + (X[j+1]-X[j])*(f-a)/max(1, b-a)

def crop_points(t0, t1):
    """(t_rel, x) breakpoints for this beat: every track sample inside the beat (exact frame times),
    plus the pair one frame apart either side of every picture cut so the step renders as a step."""
    N = _TRK['n']
    ts = set([t0, t1])
    for v in N:
        t = v/FPS
        if t0 < t < t1: ts.add(t)
    for c in _SPLICES:
        if t0 + 0.05 < c < t1 - 0.05:
            ts.add(c - 1.0/FPS); ts.add(c)
    ts = sorted(round(x, 5) for x in ts)
    return [(x - t0, float(_x_at(x))) for x in ts]

def crop_x_expr(t0, t1):
    """Piecewise-linear crop x over this beat as an ffmpeg expression in `t` (0 at the beat
    start, because the input is seeked with -ss) -- written as x0 + sum of slope*clip(t-ta,0,dt),
    which is exactly the same function as the nested-if chain and has NO nesting."""
    pts = crop_points(t0, t1)
    if len(pts) == 1 or max(p[1] for p in pts) - min(p[1] for p in pts) < 1.0:
        return f'{pts[0][1]:.1f}'
    terms = [f'{pts[0][1]:.2f}']
    for (ta, xa), (tb, xb) in zip(pts[:-1], pts[1:]):
        dt = tb - ta
        if dt <= 1e-9 or abs(xb - xa) < 0.01: continue
        s = (xb - xa)/dt
        terms.append(f'{s:+.6f}*clip(t-{ta:.4f}\\,0\\,{dt:.6f})')
    e = ''.join(terms)
    return f'max(0\\,min({1920-CROP_W}\\,{e}))'

def _eval_crop_expr(expr, t):
    """Evaluate the expression the way ffmpeg would -- the self-test for the above."""
    py = expr.replace('\\,', ',')
    clip = lambda x, a, b: min(max(x, a), b)
    return eval(py, {'clip': clip, 'max': max, 'min': min, 't': t})

def selftest(verbose=True):
    """Every talk beat: the expression must reproduce the track at every breakpoint (<=0.5 px)
    and interpolate linearly between them. Abort the render if it does not."""
    tl, _ = beats.timeline()
    worst = 0.0
    for b in tl:
        if b['kind'] != 'talk': continue
        pts = crop_points(b['t0'], b['t1'])
        e = crop_x_expr(b['t0'], b['t1'])
        for (ta, xa), (tb, xb) in zip(pts[:-1], pts[1:]):
            for f in (0.0, 0.5, 0.999):
                t = ta + f*(tb-ta)
                want = max(0, min(1920-CROP_W, xa + (xb-xa)*f))   # linear between breakpoints, as the expression
                got = _eval_crop_expr(e, t)
                worst = max(worst, abs(got-want))
                if abs(got-want) > 0.5:
                    raise SystemExit(f'CROP EXPRESSION SELF-TEST FAILED at beat {b["t0"]:.3f} t={t:.3f}: '
                                     f'expr {got:.2f} vs track {want:.2f}')
        if verbose: print(f'  crop expr ok  beat {b["t0"]:8.3f}-{b["t1"]:8.3f}  {len(pts):4d} breakpoints  {len(e):6d} chars')
    print(f'crop expression self-test PASS (worst {worst:.3f} px)')

os.makedirs('out', exist_ok=True); os.makedirs('gfx', exist_ok=True)

# TWO vignettes, not one. The profile was fitted as his render divided by our toned conform
# ON TALKING-HEAD FRAMES, so it is the difference he added ON TOP of the room's own falloff --
# correct for the talking head and much too strong for anything else.
if not os.path.exists('vignette.png'):
    m = (vlib.vignette_mask()*255).clip(0, 255).astype('uint8')
    Image.fromarray(np.dstack([m]*3)).save('vignette.png')
if not os.path.exists('vignette_soft.png'):
    v = vlib.vignette_mask()
    m = ((1 - (1-v)*0.25)*255).clip(0, 255).astype('uint8')
    Image.fromarray(np.dstack([m]*3)).save('vignette_soft.png')

# blend must run in RGB. On yuv420p it multiplies the CHROMA planes about their 128 offset
# as if they were luma, which turns every footage frame bright green.
VIG = ('[v0]format=gbrp[v0f];[vg]format=gbrp[vgf];'
       '[v0f][vgf]blend=all_mode=multiply,format=yuv420p')

def cover_chain(w, h, ox=0.5, oy=0.5):
    """Cover-crop; ox/oy place the window inside the overflow (0 = left/top, 1 = right/bottom).
    A centred 9:16 window of a 16:9 clip slices whatever sits at the sides -- the conveyor's
    'MEAL PLANS' sign read 'ME / PLA' centred (audit, 2026-09-03)."""
    return (f'scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,'
            f"crop={w}:{h}:'(iw-{w})*{ox:.3f}':'(ih-{h})*{oy:.3f}',setsar=1")

NARROW = {'ai_women_pool': 0.80, 'ai_respect_gym': 0.80, 'ai_beachrun': 0.80,
          'ai_busydad': 0.80, 'bodybuilder': 0.80, 'outdoor_abs': 4/3}

def still_chain(w, h, nfr, amt=0.055, ox=0.5, oy=0.5):
    """A still must not sit dead-frozen: his photo cards all carry a slow push. ox/oy place the
    crop window in the overflow AND anchor the push (oy=0 keeps the top edge fixed, so a photo
    whose hair touches the top never loses the crown as it zooms)."""
    ow, oh = int(w*1.14) - int(w*1.14) % 2, int(h*1.14) - int(h*1.14) % 2
    return (f'scale={ow}:{oh}:force_original_aspect_ratio=increase:flags=lanczos,'
            f"crop={ow}:{oh}:'(iw-{ow})*{ox:.3f}':'(ih-{oh})*{oy:.3f}',setsar=1,"
            f"zoompan=z='1+{amt:.4f}*on/{max(1,nfr-1)}':x='(iw-iw/zoom)*{ox:.3f}':"
            f"y='(ih-ih/zoom)*{oy:.3f}':d=1:s={w}x{h}:fps=30000/1001")

def push_z_expr(t0, t1):
    """zoompan `z` for this beat: 1.00 wide .. 1.20 punched, smoothstepped over his ramps."""
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

def talk_chain(t0, t1):
    z = push_z_expr(t0, t1)
    base = f"crop={CROP_W}:1080:'{crop_x_expr(t0, t1)}':0"
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

def media_opts(key):
    """Optional 5th field of a MEDIA entry: dict(ox=, oy=) crop placement."""
    spec = MEDIA[key]
    return spec[4] if len(spec) > 4 and isinstance(spec[4], dict) else {}

def media_prefix(key):
    """A clip with a RATE is stretched (setpts) -- never looped to fill a beat."""
    spec = MEDIA[key]
    if spec[0] == 'vid' and len(spec) > 3 and abs(spec[3]-1.0) > 1e-6:
        return f'setpts=(PTS-STARTPTS)*{spec[3]:.4f},'
    return ''

_AR = {}
def media_ar(key):
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

def vlib_chip(label, path, y=1180):
    """AI-GENERATED chip for a full-bleed beat. NEVER over the face: it sits at the
    shorts/waistline, clear of the caption band, sized to actually read. `y` overrides the
    height per beat (the museum clip carries his lower third AND an engraved plaque below)."""
    f = font(52, 'ExtraBold')
    tw, th = text_size(label, f)
    im = Image.new('RGBA', (VW, VH), (0,0,0,0)); d = ImageDraw.Draw(im)
    bw, bh = tw+56, th+34
    bx, by = (VW-bw)//2, y
    d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=12, fill=(0,0,0,225))
    d.text((bx+28, by+17), label, font=f, fill=(255,255,255,255), anchor='lt')
    im.save(path)

def _track_sig(t0, t1):
    """The crop track slice this beat reads (plus a sample either side): a talk segment's cache
    is only valid for the track it was rendered with."""
    N, X = _TRK['n'], _TRK['x']
    f0, f1 = t0*FPS - 8, t1*FPS + 8
    sl = [(n, x) for n, x in zip(N, X) if f0 <= n <= f1]
    return hashlib.md5(json.dumps(sl).encode()).hexdigest()[:10]

def _sig(b, nfr, t0):
    v = 'v2-flat-gblur' if b['kind'] == 'bleed2' else 'v2-flat'   # only the photo beat changed; keep every other cache hit
    extra = {'_n': nfr, '_t0': round(t0, 4), '_v': v}
    if b['kind'] == 'talk': extra['_trk'] = _track_sig(t0, b['t1'])
    # ⚠ the MEDIA entry (path, in-point, rate, crop placement) is part of what was rendered: a crop
    # offset changed in assets.py served the stale segment on 2026-09-03 until this was added
    for mk in ('media', 'media_a', 'media_b'):
        if mk in b: extra['_' + mk] = repr(MEDIA[b[mk]])
    return json.dumps({k: v_ for k, v_ in sorted(b.items())} | extra, sort_keys=True, default=str)

COMMON = lambda nfr, out: ['-r','30000/1001','-frames:v',str(nfr),'-c:v','libx264','-preset','medium',
                           '-crf','16','-pix_fmt','yuv420p','-an', out]

def render_bleed_frames(key, n, out, amt=0.075):
    """A full-bleed still (slow push) or clip (cover crop), n frames, no vignette yet."""
    isimg = MEDIA[key][0] == 'img'; o = media_opts(key)
    ch = still_chain(VW, VH, n, amt=amt, **o) if isimg else \
         media_prefix(key) + cover_chain(VW, VH, **o) + ',unsharp=5:5:0.4:5:5:0.0'
    run([FF,'-v','error','-y'] + media_input(key, n) +
        ['-filter_complex', f'[0:v]{ch}[v]', '-map', '[v]'] + COMMON(n, out))

def render_segment(i, b, nfr, t0):
    out = f'out/s{i:03d}.mp4'
    man = out + '.sig'
    if os.path.exists(out) and os.path.getsize(out) > 20000 \
       and os.path.exists(man) and open(man).read() == _sig(b, nfr, t0):
        return
    k, dur = b['kind'], nfr/FPS
    common = COMMON(nfr, out)
    if k == 'talk':
        run([FF,'-v','error','-y','-ss',f'{t0:.4f}','-i',BASE,
             '-loop','1','-framerate','30000/1001','-i','vignette.png',
             '-filter_complex', f'[0:v]{talk_chain(t0, b["t1"])}[v0];'
                                f'[1:v]scale={VW}:{VH}[vg];{VIG}'] + common)
        open(man, 'w').write(_sig(b, nfr, t0))
        return
    if k == 'bleed':
        isimg = MEDIA[b['media']][0] == 'img'; o = media_opts(b['media'])
        bchain = (still_chain(VW, VH, nfr, amt=0.075, **o) if isimg
                  else media_prefix(b['media']) + cover_chain(VW, VH, **o) + ',unsharp=5:5:0.4:5:5:0.0')
        lab = b.get('label')
        if lab:
            cy = int(b.get('chip_y', 1180))
            chip = f'gfx/chip_{hashlib.md5(f"{lab}@{cy}".encode()).hexdigest()[:8]}.png'
            if not os.path.exists(chip): vlib_chip(lab, chip, y=cy)
            run([FF,'-v','error','-y'] + media_input(b['media'], nfr) +
                ['-loop','1','-framerate','30000/1001','-i','vignette_soft.png',
                 '-loop','1','-framerate','30000/1001','-i',chip,
                 '-filter_complex', f'[0:v]{bchain}[v0];'
                                    f'[1:v]scale={VW}:{VH}[vg];{VIG}[vv];'
                                    f'[vv][2:v]overlay=0:0:shortest=1'] + common)
        else:
            run([FF,'-v','error','-y'] + media_input(b['media'], nfr) +
                ['-loop','1','-framerate','30000/1001','-i','vignette_soft.png',
                 '-filter_complex', f'[0:v]{bchain}[v0];'
                                    f'[1:v]scale={VW}:{VH}[vg];{VIG}'] + common)
        open(man, 'w').write(_sig(b, nfr, t0))
        return
    if k == 'bleed2':
        # Two full-bleed stills with HIS blur-through between them (V2 149.85-155.39: photo A,
        # a ~10-frame blur-dissolve, photo B). Both halves are rendered with their push and
        # half the transition of headroom each, then joined with xfade, so the total is
        # exactly nfr and the transition is centred on `split`.
        D = 10; h = D//2
        nA = round(b['split']*FPS) - round(t0*FPS); nB = nfr - nA
        ta, tb = f'out/_{i:03d}a.mp4', f'out/_{i:03d}b.mp4'
        render_bleed_frames(b['media_a'], nA + h, ta)
        render_bleed_frames(b['media_b'], nB + h, tb)
        off = (nA - h)/FPS; dd = D/FPS
        # His blur-through is a soft GAUSSIAN blur that peaks at the midpoint of a plain dissolve
        # (xfade's hblur is a horizontal motion smear and reads as a different device). gblur has
        # no time expression, so its sigma is driven per frame through sendcmd: 0 -> 18 px -> 0
        # over the 12 frames around the split.
        cmd = f'out/_{i:03d}_blur.cmd'
        lines = ['0.0 gblur sigma 0.01;']
        K = 12
        for k in range(K + 1):
            t = (nA - K//2 + k)/FPS
            s = 0.01 + 18.0*np.sin(np.pi*k/K)
            lines.append(f'{t:.4f} gblur sigma {s:.2f};')
        lines.append(f'{(nA + K//2 + 1)/FPS:.4f} gblur sigma 0.01;')
        open(cmd, 'w').write('\n'.join(lines) + '\n')
        run([FF,'-v','error','-y','-i',ta,'-i',tb,
             '-loop','1','-framerate','30000/1001','-i','vignette_soft.png',
             '-filter_complex', f'[0:v][1:v]xfade=transition=dissolve:duration={dd:.4f}:offset={off:.4f},'
                                f'sendcmd=f={cmd},gblur=sigma=0.01:steps=2[v0];'
                                f'[2:v]scale={VW}:{VH}[vg];{VIG}'] + common)
        open(man, 'w').write(_sig(b, nfr, t0))
        return
    # ---- plated beats --------------------------------------------------------
    key = hashlib.md5(repr(sorted((kk, str(v)) for kk, v in b.items())).encode()
                      + f'|{nfr}|{dur:.4f}'.encode()).hexdigest()[:10]
    plate = f'gfx/p{i:03d}_{key}.mov'
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
        hh_ = holes[name]
        x, y = int(hh_[0]), int(hh_[1])
        w, hh = int(hh_[2]-hh_[0]), int(hh_[3]-hh_[1])
        return x, y, w - w % 2, hh - hh % 2
    if 'dan' in holes:
        x, y, w, h = hole_args('dan')
        cw, ch, cx, cy = vlib.window_crop(h)
        ins += ['-ss', f'{t0:.4f}', '-i', BASE]
        prep.append(f'[{idx}:v]setpts=PTS-STARTPTS,crop={cw}:{ch}:{cx}:{cy},'
                    f'scale={w}:{h}:flags=lanczos,unsharp=5:5:0.5:5:5:0.0,setsar=1[m{idx}]')
        over.append((idx, x, y)); idx += 1
    if 'media' in holes:
        x, y, w, h = hole_args('media')
        ins += media_input(b['media'], nfr)
        chain = still_chain(w, h, nfr) if MEDIA[b['media']][0] == 'img' else \
                'setpts=PTS-STARTPTS,' + media_prefix(b['media']) + cover_chain(w, h)
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
    open(man, 'w').write(_sig(b, nfr, t0))

def plan():
    tl, ov = beats.timeline()
    prev, out = 0, []
    for b in tl:
        cum = round(b['t1']*FPS); out.append((b, cum-prev)); prev = cum
    return out, ov

def main():
    args = sys.argv[1:]
    if '--selftest' in args: selftest(); return
    P, ov = plan()
    if '--plan' in args:
        for i, (b, nfr) in enumerate(P):
            det = b.get('media') or b.get('media_a') or b.get('header') or b.get('headline') or ''
            print(f'{i:3d} {b["kind"]:9s} {b["t0"]:8.3f} {nfr:5d}f  {det}')
        print(sum(n for _, n in P), 'frames planned'); return
    only = None
    if '--only' in args:
        only = set(int(x) for x in args[args.index('--only')+1].split(','))
    selftest(verbose=False)
    for i, (b, nfr) in enumerate(P):
        if only is not None and i not in only: continue
        render_segment(i, b, nfr, b['t0'])
        det = b.get('media') or b.get('media_a') or b.get('header') or b.get('headline') or ''
        print(f'{i:3d} {b["kind"]:9s} {nfr:5d}f  {det}', flush=True)
    if only is not None: return
    with open('out/list.txt','w') as f:
        for i in range(len(P)): f.write(f'file s{i:03d}.mp4\n')
    run([FF,'-v','error','-y','-f','concat','-safe','0','-i','out/list.txt','-c','copy','picture_raw.mp4'])

    # ---- overlays: lower thirds, CTA pills, flashes --------------------------
    ins, fc, idx, last = ['-i','picture_raw.mp4'], [], 1, '0:v'
    items = [(b['kind'], b['t0'], b['t1'], b) for b in ov] + \
            [('flash', a, b, None) for a, b in beats.FLASHES]
    items.sort(key=lambda x: x[1])
    for n, (kind, a, b, spec) in enumerate(items):
        h = hashlib.sha1(json.dumps([kind, spec, round(b-a, 4), 'v2'], sort_keys=True,
                                    default=str).encode()).hexdigest()[:10]
        mov = f'gfx/ov_{kind}_{h}.mov'          # content-addressed, not index-keyed
        d = b - a
        if not os.path.exists(mov):
            if kind == 'cta':   fr, _ = vlib.overlay_cta(spec['top'], spec['big'], d,
                                                         big_size=spec.get('big_size', 70))
            elif kind == 'lt':  fr, _ = vlib.overlay_lower_third(spec['lines'], d, y_bottom=spec.get('y_bottom', 1600))
            else:               fr, _ = vlib.overlay_flash(d)
            encode(fr, mov, alpha=True)
        ins += ['-i', mov]
        # An overlay must be SHIFTED onto the main timeline (setpts), not just gated with enable.
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
