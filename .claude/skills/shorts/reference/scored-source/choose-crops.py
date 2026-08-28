#!/usr/bin/env python3
"""Pick the crop window per shot and render a review sheet of the ACTUAL vertical frames
(crop / zoom-crop / card, with cardCrop applied), so the framing is checked by eye rather
than assumed. Full-resolution frames are pulled from the source, not the 480px thumbs, so
what the sheet shows is what render.js will encode."""
import json, os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, 'shots')
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = '/Volumes/Extreme/_edit_work/abwheel/mrepro/ref_hd.mp4'
man = json.load(open(os.path.join(SHOTS, 'manifest.json')))
plan = json.loads(subprocess.check_output(
    ['node', '-e', "const p=require('./plan.js');console.log(JSON.stringify({SHOTS:p.SHOTS,TALK_X:p.TALK_X}))"],
    cwd=HERE, stderr=subprocess.DEVNULL).decode())
SPEC, TALK_X = plan['SHOTS'], plan['TALK_X']
L = json.load(open(os.path.join(HERE, 'layout.json')))
SRC_W, SRC_H = 1920, 1080
CW, CH = L['canvas']


def auto_x(im):
    """Centre of the most detailed 9:16-wide column band - where the subject is."""
    g = im.convert('L').filter(ImageFilter.GaussianBlur(1.2))
    edges = ImageChops.difference(g, g.filter(ImageFilter.GaussianBlur(4)))
    px = edges.load(); w, h = edges.size
    col = [sum(px[x, y] for y in range(0, h, 3)) for x in range(w)]
    k = 9
    sm = [sum(col[max(0, i - k):min(w, i + k + 1)]) for i in range(w)]
    win = max(8, int(w * 0.3164))
    best, bi, run = -1, 0, sum(sm[:win])
    for i in range(w - win):
        if run > best: best, bi = run, i
        run += sm[i + win] - sm[i]
    return (bi + win / 2) / w


chosen = {}
for m in man:
    spec = SPEC[m['name']]
    if spec['t'] in ('card', 'extern'):
        x = 0.5
    elif spec.get('x') is not None:
        x = spec['x']                      # explicit per-shot value wins over the default
    elif spec['t'] == 'talk':
        x = TALK_X
    else:
        x = auto_x(Image.open(os.path.join(SHOTS, m['name'] + '.jpg')).convert('RGB'))
    frac = (L['talk']['dropZoomW'] if spec.get('zoom') else L['talk']['dropW']) / SRC_W
    chosen[m['name']] = round(min(max(x, frac / 2), 1 - frac / 2), 4)
json.dump(chosen, open(os.path.join(SHOTS, 'crops.json'), 'w'), indent=1)


def full_frame(t):
    p = f'/tmp/_cc_{t:.2f}.png'
    if not os.path.exists(p):
        subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', SRC,
                        '-frames:v', '1', p], check=True)
    return Image.open(p).convert('RGB')


def render_preview(m, spec):
    """Reproduce render.js's geometry exactly."""
    PH = CH - L['dropTop']
    if spec['t'] == 'extern':
        p = f"/tmp/_ext_{spec['file']}_{m['dur']:.2f}.png"
        if not os.path.exists(p):
            subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss',
                            f"{spec.get('in', 0) + m['dur'] / 2:.2f}", '-i',
                            os.path.join(HERE, 'broll', spec['file']),
                            '-frames:v', '1', p], check=True)
        im = Image.open(p).convert('RGB')
        w = CW
        h = round(im.height * CW / im.width)
        im = im.resize((w, h), Image.LANCZOS)
        top = max(0, (h - PH) // 2)
        pic = im.crop((0, top, CW, top + PH))
        out = Image.open(os.path.join(HERE, 'assets', 'j2-bg.png')).convert('RGB')
        out.paste(pic, (0, L['dropTop']))
        return out
    im = full_frame(m['absStart'] + m['dur'] / 2)
    if spec['t'] in ('talk', 'broll'):
        cw = L['talk']['dropZoomW'] if spec.get('zoom') else L['talk']['dropW']
        ch = L['talk']['zoomH'] if spec.get('zoom') else SRC_H
        x = round(min(max(chosen[m['name']] * SRC_W - cw / 2, 0), SRC_W - cw))
        if spec.get('minX0') is not None:
            x = max(x, spec['minX0'])
        pic = im.crop((x, 0, x + cw, ch)).resize((CW, PH), Image.LANCZOS)
        out = Image.open(os.path.join(HERE, 'assets', 'j2-bg.png')).convert('RGB')
        out.paste(pic, (0, L['dropTop']))
        return out
    bg = Image.open(os.path.join(HERE, 'assets', 'j2-bg.png')).convert('RGB')
    c = L['card']
    src = im
    if spec.get('cardCrop'):
        x0, x1, y0, y1 = spec['cardCrop']
        src = im.crop((round(x0 * SRC_W), round(y0 * SRC_H), round(x1 * SRC_W), round(y1 * SRC_H)))
    s = min(c['w'] / src.width, c['h'] / src.height)
    fit = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
    out = bg.copy()
    out.paste(fit, (c['x'] + (c['w'] - fit.width) // 2, c['y'] + (c['h'] - fit.height) // 2))
    return out


TH_W = 170; TH_H = round(TH_W * 16 / 9); COLS = 12
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 13)
rows = (len(man) + COLS - 1) // COLS
sheet = Image.new('RGB', (COLS * (TH_W + 6), rows * (TH_H + 34)), (16, 16, 16))
d = ImageDraw.Draw(sheet)
for i, m in enumerate(man):
    spec = SPEC[m['name']]
    th = render_preview(m, spec).resize((TH_W, TH_H), Image.LANCZOS)
    px, py = (i % COLS) * (TH_W + 6), (i // COLS) * (TH_H + 34)
    sheet.paste(th, (px, py + 30))
    tag = spec['t'].upper() if not spec.get('zoom') else 'ZOOM'
    d.text((px + 2, py + 2), f"{m['name']} {tag}", fill=(255, 220, 120), font=font)
    d.text((px + 2, py + 16), f"x={chosen[m['name']]}  {m['absStart']:.1f}s +{m['dur']:.1f}",
           fill=(150, 200, 255), font=font)
p = os.path.join(SHOTS, 'crop_review.jpg')
sheet.save(p, quality=88)
print(f'{len(man)} shots -> {p}  {sheet.size}')
