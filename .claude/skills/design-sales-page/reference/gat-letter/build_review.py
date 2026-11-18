#!/usr/bin/env python3
"""Builds review/index.html + review/img/ from caps/, and copies the live pages + assets into review/ for publishing."""
import pathlib, shutil, glob, html
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'review'
IMG = OUT / 'img'
IMG.mkdir(parents=True, exist_ok=True)
CAP = HERE / 'caps'
OLD = HERE.parent / 'gallery/img/D-after-fold.jpg'

def save(src, name, width):
    im = Image.open(src).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(IMG / name, quality=80, optimize=True, progressive=True)
    return f'img/{name}', im.width, im.height

def stack(srcs, name, width):
    ims = [Image.open(s).convert('RGB') for s in srcs]
    ims = [i.resize((width, round(i.height * width / i.width)), Image.LANCZOS) for i in ims]
    c = Image.new('RGB', (width, sum(i.height for i in ims)), 'white')
    y = 0
    for i in ims:
        c.paste(i, (0, y)); y += i.height
    c.save(IMG / name, quality=78, optimize=True, progressive=True)
    return f'img/{name}', width, c.height

def fig(img, cap, cls='', tall=False):
    src, w, h = img
    crop = ' crop' if tall else ''
    more = '<span class="more">Tap to see it all</span>' if tall else ''
    return (f'<figure class="shot {cls}"><button type="button" class="zoom{crop}" data-src="{src}" aria-label="{html.escape(cap)}, full size">'
            f'<img src="{src}" width="{w}" height="{h}" alt="{html.escape(cap)}" loading="lazy">{more}</button><figcaption>{cap}</figcaption></figure>')

def segs(prefix):
    return sorted(glob.glob(str(CAP / f'{prefix}-full-*.jpg')))

# images
old = save(OLD, 'bar-old.jpg', 390)
new = save(CAP / 'p-after-fold.jpg', 'bar-new-top.jpg', 390)
newread = save(CAP / 'p-after-view1.jpg', 'bar-new-top-reading.jpg', 390)
dock = save(CAP / 'p-bottom-view0.jpg', 'bar-alt-bottom.jpg', 390)
p_before = save(CAP / 'p-before-fold.jpg', 'p-before.jpg', 390)
p_full = [save(s, f'p-full-{i:02d}.jpg', 390) for i, s in enumerate(segs('p-after'))]
p_studies = save(CAP / 'p-after-view0.jpg', 'p-studies.jpg', 390)
t_fold = save(CAP / 't-after-fold.jpg', 't-fold.jpg', 768)
t_offer = save(CAP / 't-after-view0.jpg', 't-offer.jpg', 768)
t_letter = save(CAP / 't-after-view1.jpg', 't-letter.jpg', 768)
t_full = stack(segs('t-after')[:3], 't-full-top.jpg', 768)
d_fold = save(CAP / 'd-after-fold.jpg', 'd-fold.jpg', 1440)
d_before = save(CAP / 'd-before-fold.jpg', 'd-before.jpg', 1440)
d_offer = save(CAP / 'd-after-view0.jpg', 'd-offer.jpg', 1440)
d_studies = save(CAP / 'd-after-view1.jpg', 'd-studies.jpg', 1440)
d_letter = save(CAP / 'd-after-view2.jpg', 'd-letter.jpg', 1440)
d_dock = save(CAP / 'd-bottom-view0.jpg', 'd-dock.jpg', 1440)
c_phone = stack(segs('p-checkout'), 'c-phone.jpg', 390)
c_tab = stack(segs('t-checkout'), 'c-tablet.jpg', 768)
c_desk = stack(segs('d-checkout'), 'c-desktop.jpg', 1440)

HB = HERE.parent.parent / 'gat-sales-page-research-20261116/shots/hbi-order-ot-stitched.jpg'
hb = Image.open(HB).convert('RGB')
hb.crop((0, 0, 780, 2000)).save(IMG / 'hb-top-src.jpg', quality=82)
hb.crop((0, 6184, 780, 8075)).save(IMG / 'hb-legal-src.jpg', quality=82)
hb_top = save(IMG / 'hb-top-src.jpg', 'hb-top.jpg', 390)
hb_legal = save(IMG / 'hb-legal-src.jpg', 'hb-legal.jpg', 390)
hb_full = save(HB, 'hb-full.jpg', 390)
for f in ['hb-top-src.jpg', 'hb-legal-src.jpg']:
    (IMG / f).unlink()
p_dock_fold = save(CAP / 'p-bottom-fold.jpg', 'p-dock-fold.jpg', 390)
c_top = save(CAP / 'p-checkout-fold.jpg', 'c-phone-top.jpg', 390)

parts = {}
parts['HB'] = (fig(hb_top, 'Healthy Back: one big bottle, then two plain option rows') + fig(c_top, 'Ours now: no big bottle, a small bottle in each option')
               + fig(hb_legal, 'Healthy Back: offer terms, tick box and fine print under the button') + fig(hb_full, 'Healthy Back checkout, whole page', tall=True))
parts['BAR'] = (fig(old, 'Before: the cream bar with a white background') + fig(new, 'New: the bar is part of the dark header')
                + fig(newread, 'New, while reading: it stays with him') + fig(p_dock_fold, 'Bottom bar on a phone, first screen') + fig(dock, 'Bottom bar on a phone, while reading'))
parts['PHONE'] = ''.join(fig(s, f'Part {i + 1} of {len(p_full)}', tall=True) for i, s in enumerate(p_full))
seal_v = save(CAP / 'seal1.jpg', 'seal.jpg', 390)
parts['PHONEKEY'] = fig(seal_v, 'New gold seal on the product reveal') + fig(p_before, 'Before the offer appears') + fig(p_studies, 'The study list right under the video')
parts['TABLET'] = fig(t_fold, 'Tablet, first screen', 'wide') + fig(t_offer, 'Tablet, the offer', 'wide') + fig(t_letter, 'Tablet, the letter', 'wide')
parts['DESK'] = (fig(d_fold, 'Desktop, first screen after the offer appears', 'desk') + fig(d_before, 'Desktop, before the offer appears', 'desk')
                 + fig(d_offer, 'Desktop, the offer', 'desk') + fig(d_studies, 'Desktop, the studies in two journal columns', 'desk')
                 + fig(d_letter, 'Desktop, the letter in a reading column', 'desk') + fig(d_dock, 'Desktop with the bottom bar alternative', 'desk'))
parts['CHECKOUT'] = (fig(c_phone, 'Phone checkout, whole page', tall=True) + fig(c_tab, 'Tablet checkout, whole page', 'wide', tall=True)
                     + fig(c_desk, 'Desktop checkout, whole page', 'desk', tall=True))

import sys; sys.path.insert(0, str(HERE)); import gen
import json as _j
parts['COMPLIANCE'] = ''.join(f'<li><span class="was">{html.escape(o)}</span> <span class="arrow" aria-hidden="true">to</span> <span class="now">{html.escape(n)}</span></li>' for o, n in _j.load(open(HERE.parent / 'docx/compliance_edits.json')))
parts['EDITS'] = ''.join(f'<li><span class="was">{html.escape(o)}</span> <span class="arrow" aria-hidden="true">to</span> <span class="now">{html.escape(n)}</span><small>{html.escape(w)}</small></li>' for _, o, n, w in gen.EDITS)
t = (HERE / 'review_template.html').read_text()
for k, v in parts.items():
    t = t.replace('{{' + k + '}}', v)
(OUT / 'index.html').write_text(t)

# live pages
BACK = ('<a id="back-to-review" href="index.html" style="position:fixed;left:12px;bottom:{b}px;z-index:99;display:flex;align-items:center;'
        'gap:6px;min-height:44px;padding:8px 14px 8px 12px;border-radius:999px;background:#ffffff;color:#141a19;border:1px solid #c9d0cd;'
        'box-shadow:0 4px 14px rgba(0,0,0,.25);font:600 14px Archivo,Arial,sans-serif;text-decoration:none">'
        '<svg width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4l-6 6 6 6"/></svg>Back to the review</a>'
        '<script>try{if(window.self!==window.top&&new URLSearchParams(location.search).has("frame"))document.getElementById("back-to-review").remove()}catch(e){}</script>')
for f in ['1-quiz.html', '2-before-offer.html', '3-after-offer.html', '3b-after-offer-bottom-bar.html', '4-checkout.html']:
    h = (HERE / f).read_text()
    h = h.replace('</body>', BACK.replace('{b}', '96' if f.startswith('3b') else '14') + '</body>')
    (OUT / f).write_text(h)
if (OUT / 'assets').exists():
    shutil.rmtree(OUT / 'assets')
shutil.copytree(HERE / 'assets', OUT / 'assets')
print('review built', sum(1 for _ in IMG.iterdir()), 'images')
