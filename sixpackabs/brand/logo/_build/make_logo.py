"""SixPackAbs.com logo kit, built from the locked label lockup (2026-11-05).
Symbol: existing SixPackAbs.com abs-grid shield + swoosh (smoothed trace of public/img/sixpackabs-icon-192.png).
Wordmark: SIXPACKABS.COM in Archivo SemiExpanded Bold (wdth 112.5, wght 700), tracking +3.5%.
Run: python3 sixpackabs/brand/logo/_build/make_logo.py   (rebuilds every file in sixpackabs/brand/logo/)"""
import os, json, shutil
import fitz, uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image

B = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(B)
SYM = json.load(open(B + '/symbol-master.json'))
FONT = B + '/fonts/Archivo-ExpandedBold.ttf'
GOLD, BLACK, WHITE, IVORY = '#C9A766', '#1C1A17', '#FFFFFF', '#F2ECDF'
C = 100.0                      # cap height unit
TRACK = 0.035

tt = TTFont(FONT); gs = tt.getGlyphSet(); order = tt.getGlyphOrder(); upm = tt['head'].unitsPerEm
CAPR = tt['OS/2'].sCapHeight / upm
face = hb.Font(hb.Face(open(FONT, 'rb').read()))


def text_path(s, size, x, y):
    buf = hb.Buffer(); buf.add_str(s); buf.guess_segment_properties(); hb.shape(face, buf, {'kern': True})
    k = size / upm; pen = SVGPathPen(gs); cx = 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gs[order[info.codepoint]].draw(TransformPen(pen, (k, 0, 0, -k, x + cx + pos.x_offset * k, y)))
        cx += pos.x_advance * k + TRACK * size
    return pen.getCommands(), cx - TRACK * size


SIZE = C / CAPR
_, TW = text_path('SIXPACKABS.COM', SIZE, 0, 0)
SH = 1.595 * C                 # symbol height relative to cap height (same as the label band)
SW = SH * SYM['w'] / SYM['h']


def sym(x, y, h, color):
    k = h / SYM['h']
    return f'<path transform="translate({x:.2f},{y:.2f}) scale({k:.6f})" d="{SYM["d"]}" fill="{color}" fill-rule="evenodd"/>'


def word(x, baseline, color):
    d, _ = text_path('SIXPACKABS.COM', SIZE, x, baseline)
    return f'<path d="{d}" fill="{color}"/>'


def layout(kind, color):
    """returns (elements, width, height) tight-cropped artwork in units"""
    if kind == 'horizontal':
        gap = SH * 0.34; H = SH; W = SW + gap + TW
        return [sym(0, 0, SH, color), word(SW + gap, H / 2 + C / 2, color)], W, H
    if kind == 'stacked':
        sh = 3.4 * C; sw = sh * SYM['w'] / SYM['h']; gap = 0.95 * C
        W = max(TW, sw); H = sh + gap + C
        return [sym((W - sw) / 2, 0, sh, color), word((W - TW) / 2, H, color)], W, H
    if kind == 'symbol':
        return [sym(0, 0, SYM['h'], color)], SYM['w'], SYM['h']
    if kind == 'wordmark':
        return [word(0, C, color)], TW, C


def svg(kind, color, bg=None, pad=None, square=False):
    els, w, h = layout(kind, color)
    if pad is None:
        pad = 0.02 * max(w, h)            # transparent files: tight crop with a hair of margin
    W, H = w + 2 * pad, h + 2 * pad
    ox, oy = pad, pad
    if square:
        S = max(W, H); ox += (S - W) / 2; oy += (S - H) / 2; W = H = S
    body = ''.join(els)
    rect = f'<rect width="{W:.2f}" height="{H:.2f}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {H:.2f}" width="{W:.0f}" height="{H:.0f}">'
            f'<title>SixPackAbs.com logo</title>{rect}<g transform="translate({ox:.2f},{oy:.2f})">{body}</g></svg>'), W, H


def render(svgtext, W, width_px, alpha):
    d = fitz.open(stream=svgtext.encode(), filetype='svg')
    z = width_px / d[0].rect.width
    pix = d[0].get_pixmap(matrix=fitz.Matrix(z, z), alpha=alpha)
    mode = 'RGBA' if alpha else 'RGB'
    return Image.frombytes(mode, (pix.width, pix.height), pix.samples)


def pdf(svgtext, path):
    d = fitz.open(stream=svgtext.encode(), filetype='svg')
    out = fitz.open('pdf', d.convert_to_pdf())
    out.set_metadata(dict(title='SixPackAbs.com logo', author='SixPackAbs.com'))
    out.save(path, garbage=4, deflate=True)


TRANSPARENT = {'gold': GOLD, 'black': BLACK, 'white': WHITE}
SOLID = {'gold-on-black': (GOLD, BLACK), 'black-on-white': (BLACK, WHITE), 'black-on-ivory': (BLACK, IVORY)}
HQ = {'horizontal': 4000, 'stacked': 2400, 'symbol': 2048, 'wordmark': 4000}
WEB = {'horizontal': 800, 'stacked': 600, 'symbol': 512, 'wordmark': 800}
SOLID_PAD = {'horizontal': 0.9 * C, 'stacked': 1.4 * C, 'symbol': 0.22 * 1000, 'wordmark': 0.8 * C}

for sub in ('svg', 'pdf', 'png', 'png-web', 'jpg', 'icons'):
    os.makedirs(f'{OUT}/{sub}', exist_ok=True)

n = 0
for kind in HQ:
    for cname, col in TRANSPARENT.items():
        s, W, H = svg(kind, col)
        base = f'sixpackabs-logo-{kind}-{cname}'
        open(f'{OUT}/svg/{base}.svg', 'w').write(s); pdf(s, f'{OUT}/pdf/{base}.pdf')
        render(s, W, HQ[kind], True).save(f'{OUT}/png/{base}.png', optimize=True)
        render(s, W, WEB[kind], True).save(f'{OUT}/png-web/{base}.png', optimize=True)
        n += 4
    for cname, (fg, bg) in SOLID.items():
        s, W, H = svg(kind, fg, bg, pad=SOLID_PAD[kind], square=(kind == 'symbol'))
        base = f'sixpackabs-logo-{kind}-{cname}'
        open(f'{OUT}/svg/{base}.svg', 'w').write(s); pdf(s, f'{OUT}/pdf/{base}.pdf')
        render(s, W, HQ[kind], False).save(f'{OUT}/png/{base}.png', optimize=True)
        render(s, W, max(WEB[kind], 1200 if kind in ('horizontal', 'wordmark') else WEB[kind]), False).save(
            f'{OUT}/jpg/{base}.jpg', quality=82, optimize=True, progressive=True)
        n += 4

# icons: gold symbol on black square (favicon, app icons, social avatar)
s, W, H = svg('symbol', GOLD, BLACK, pad=0.2 * 1000, square=True)
open(f'{OUT}/icons/sixpackabs-icon-gold-on-black.svg', 'w').write(s)
big = render(s, W, 1024, False)
for px in (16, 32, 48, 180, 192, 512, 1024):
    big.resize((px, px), Image.LANCZOS).save(f'{OUT}/icons/sixpackabs-icon-{px}.png', optimize=True); n += 1
big.resize((256, 256), Image.LANCZOS).save(f'{OUT}/icons/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)]); n += 1
# social profile avatar (round-crop safe: symbol inside 70% circle)
s2, W2, _ = svg('symbol', GOLD, BLACK, pad=0.32 * 1000, square=True)
render(s2, W2, 1080, False).save(f'{OUT}/icons/sixpackabs-social-avatar-1080.png', optimize=True); n += 1
# link-preview / Open Graph banner 1200x630, horizontal lockup centred on black
els, w, h = layout('horizontal', GOLD)
k = 900 / w
og = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630"><rect width="1200" height="630" fill="{BLACK}"/>'
      f'<g transform="translate({(1200 - w * k) / 2:.2f},{(630 - h * k) / 2:.2f}) scale({k:.5f})">{"".join(els)}</g></svg>')
open(f'{OUT}/svg/sixpackabs-og-1200x630.svg', 'w').write(og)
render(og, 1200, 1200, False).save(f'{OUT}/jpg/sixpackabs-og-1200x630.jpg', quality=86, optimize=True, progressive=True); n += 2
print('files', n)
