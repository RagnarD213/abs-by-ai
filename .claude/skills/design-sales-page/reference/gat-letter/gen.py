#!/usr/bin/env python3
"""Great Again T sales page, refinement of contest design D.

Builds, into this folder:
  2-before-offer.html   video page before the offer appears (phone, tablet, desktop in one responsive file)
  3-after-offer.html    after the reveal: integrated top bar, offer card, studies, full sales letter
  3b-after-offer-bottom-bar.html   same page with the alternative bottom bar
  4-checkout.html       checkout modelled on the Healthy Back order page

Every letter line comes from Dan's VSL script by index (L[i]); EDITS lists each spoken-to-written change.
`python3 gen.py` builds; `python3 gen.py check` proves every script line is used once, in order.
"""
import html, re, sys, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SCRIPT = ROOT.parent / 'gat-sales-page-research-20261116/reference/Great Again T VSL Script - DAN.txt'
raw = SCRIPT.read_text(encoding='utf-8-sig')
L = [l.strip() for l in raw.split('\n') if l.strip() and not l.strip().startswith('[')]

# Spoken-to-written changes. (line, old, new, why)
EDITS = [
    (3, 'In today’s video,', 'In this presentation,', 'a reader is not watching a video'),
    (4, 'discover in this video', 'discover in this presentation', 'same'),
    (5, 'I’ve put links to every one of those studies right below this video.',
        'I’ve listed every one of those studies right above this presentation.',
        'the studies sit above the letter, and the list is not clickable'),
    (6, 'If you’re watching this right now', 'If you’re reading this right now', 'reader'),
    (100, 'if you look at the links below this video', 'if you look at the studies listed above', 'the list sits above'),
    (116, 'tap the button below this video right now', 'tap the button below right now', 'no video in the letter'),
    (123, 'If you’re still here,', 'If you’re still reading,', 'reader'),
    (147, 'Still here?', 'Still reading?', 'reader'),
    (157, 'Still here?', 'Still reading?', 'reader'),
    (179, 'supply,, and', 'supply, and', 'double comma in the script'),
]
T = list(L)
for i, old, new, _ in EDITS:
    assert old in T[i], (i, old)
    T[i] = T[i].replace(old, new)

USED = []
def t(i):
    USED.append(i)
    return html.escape(T[i], quote=False)

# ---------- studies ----------
CITES_FULL = [l for l in (ROOT / 'citations-final.txt').read_text().split('\n') if l.strip()]
assert len(CITES_FULL) == 31
def _au(authors):
    names = [a.strip() for a in authors.split(',') if a.strip() and a.strip() != 'et al']
    return ', '.join(names[:3]) + (', et al.' if len(names) > 3 or 'et al' in authors else '.')

def _no_title(line):
    """Google Ads (Dan, 2026-11-17): the study list shows no paper titles. Authors (first three, et al.),
    journal, year;volume(issue):pages, DOI, PMID."""
    authors = line.split('. ', 1)[0]
    m = re.search(r'[.?] ([^.?]+)\. (\d{4}[;:.].*)$', line)
    assert m, line[:60]
    if re.search(r'steroid', m.group(1), re.I):   # journal name holds a C10 word: DOI and PMID still identify it
        return f'{_au(authors)} {m.group(2)}'
    return f'{_au(authors)} {m.group(1)}. {m.group(2)}'
CITES = [_no_title(l) for l in CITES_FULL]
def cite_short(n):
    c = CITES[n - 1]
    authors = c.split('. ')[0].split(', ')[0]
    yr = re.search(r'\. (\d{4});', c).group(1)
    jour = re.search(r'\. ([^.]+(?:\. [A-Z][^.]*)*?)\. \d{4};', c)
    return authors, yr

STUDY = {  # number in the list: (journal as Dan named it, finding from his on-screen notes)
    1: ('Bagheri et al., 2021, Journal of Strength and Conditioning Research', '30 men, 12 weeks. Whole eggs raised testosterone more than egg whites.'),
    3: ('Anderson et al., 1987, Life Sciences', 'Same men, two diets, 10 days each.'),
    4: ('Whittaker and Harris, 2022, Nutrition and Health', '27 studies, 309 men. High-protein, low-carb diets caused a large drop in testosterone.'),
    9: ('Prasad et al., 1996, Nutrition', 'Zinc restricted for 20 weeks.'),
    10: ('Naghii et al., 2011, Journal of Trace Elements in Medicine and Biology', 'One week of boron. Free testosterone up, estrogen down.'),
    11: ('Chinnappan et al., 2021, Food and Nutrition Research', '105 men aged 50 to 70 with low T. 12 weeks, placebo controlled. Total testosterone and muscle strength up.'),
    12: ('Tambi et al., 2012, Andrologia', '76 men with low T. Men with normal testosterone:'),
    13: ('Talbott et al., 2013, Journal of the International Society of Sports Nutrition', '4 weeks. Cortisol down 16%, testosterone up 37%.'),
    14: ('Leisegang et al., 2022, Medicina', 'Review of 9 studies. Significant increase in total testosterone.'),
    16: ('Jang et al., 2008, British Journal of Clinical Pharmacology', '6 placebo controlled trials, 349 men. Improvement 2.4 times more likely with ginseng.'),
    18: ('Gonzales et al., 2002, Andrologia', '12 weeks, double blind, placebo controlled. Maca increased men’s desire.'),
    19: ('Zenico et al., 2009, Andrologia', '50 men, 12 weeks. Maca beat placebo on performance scores.'),
    23: ('Araujo et al., 2011, Journal of Clinical Endocrinology and Metabolism', ''),
    24: ('Ding et al., 2006, JAMA', ''),
}

def study(n, chart=''):
    src, finding = STUDY[n]
    return (f'<aside class="study"><div class="study-k"><span class="study-n">Study {n}</span>'
            f'<span class="study-src">{html.escape(src)}</span></div>'
            + (f'<p class="study-f">{html.escape(finding)}</p>' if finding else '') + chart + '</aside>')

def bars(rows, unit, note=''):
    mx = max(v for _, v, _ in rows)
    out = '<div class="bars">'
    for label, v, cls in rows:
        out += (f'<div class="bar-row"><span class="bar-l">{label}</span><span class="bar-t">'
                f'<span class="bar-f {cls}" style="width:{v / mx * 100:.1f}%"></span></span>'
                f'<span class="bar-v">{v:g}{unit}</span></div>')
    return out + (f'<p class="bar-note">{note}</p>' if note else '') + '</div>'

# ---------- shared pieces ----------
A = 'assets/'
MENU = ['Questions', 'Contact', 'Shipping and Returns', 'Privacy Policy', 'Terms and Conditions']
CTA_TXT = 'Claim My Free Month’s Supply'
CHECKOUT = '4-checkout.html'
ARROW = '<svg class="chev" aria-hidden="true" viewBox="0 0 20 20"><path d="M7 4l6 6-6 6"/></svg>'
NOTES = ['1 year money back guarantee', '$9.99 shipping today', 'Cancel any time']

def cta(label=CTA_TXT, notes=True, cls=''):
    n = ''
    if notes:
        n = '<ul class="cta-notes">' + ''.join(f'<li>{x}</li>' for x in NOTES) + '</ul>'
    return f'<div class="cta-wrap {cls}"><a class="cta" href="{CHECKOUT}">{label}{ARROW}</a>{n}</div>'

LOCK = '<svg aria-hidden="true" viewBox="0 0 20 20"><rect x="4" y="9" width="12" height="9" rx="2"/><path d="M7 9V6.5a3 3 0 016 0V9"/></svg>'

def header(revealed, bar='top', checkout=False):
    links = ''.join(f'<a role="link" aria-disabled="true" tabindex="0">{m}</a>' for m in MENU)
    right = (f'<span class="secure">{LOCK}Secure checkout</span>' if checkout else
             f'<nav class="inline-nav" aria-label="Site">{links}</nav>'
             f'<details class="menu"><summary aria-label="Menu"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18"/></svg></summary>'
             f'<nav class="menu-panel" aria-label="Main menu">{links}</nav></details>')
    offer = ''
    if revealed and bar == 'top':
        offer = ('<div class="offerbar"><div class="offerbar-in">'
                 f'<img class="ob-bottle" src="{A}bottle-transparent.png" alt="">'
                 '<p class="ob-txt"><span class="ob-k">Great Again T</span><strong>First month FREE</strong></p>'
                 f'<a class="cta cta-sm" href="{CHECKOUT}">Claim My Free Bottle{ARROW}</a></div></div>')
    return (f'<header class="site-top"><div class="strip"><div class="strip-in">'
            f'<img class="logo" src="{A}logo/sixpackabs-logo-horizontal-gold.svg" alt="SixPackAbs.com">{right}</div></div>{offer}</header>')

def dock():
    return ('<div class="dock"><div class="dock-in">'
            f'<img class="dk-bottle" src="{A}bottle-transparent.png" alt="">'
            '<p class="dk-txt"><span class="ob-k">Great Again T</span><strong>First month FREE</strong><span class="dk-s">Just $9.99 shipping</span></p>'
            f'<a class="cta cta-sm" href="{CHECKOUT}">Claim My Free Bottle{ARROW}</a></div></div>')

SOUND = ('<div class="sound"><svg aria-hidden="true" viewBox="0 0 32 32" fill="none"><path d="M4 12h6l8-6v20l-8-6H4z" fill="currentColor"/>'
         '<path d="M23 10c4 3 4 9 0 12M27 6c7 6 7 14 0 20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
         '<span>Your video is playing<strong>Tap for sound</strong></span></div>')

def hero():
    return ('<section class="hero"><div class="hero-bg" aria-hidden="true"></div><div class="stage">'
            '<h1>Eat More Of These Foods And Less Of Those Foods To Naturally Boost Your T</h1>'
            f'<div class="player"><div class="player-fill" aria-hidden="true"></div>'
            f'<img class="poster" src="{A}poster.jpg" alt="Daniel Rose presenting whole eggs and egg whites">{SOUND}</div>'
            '</div></section>'
            '<p class="watch">This is a science-based presentation backed by real research. To see the research supporting the food swaps in this video, see the studies below.</p>')

import math
_SEAL_N = [0]
def _burst(cx, cy, r1, r2, n):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append(f'{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}')
    return ' '.join(pts)

def seal_svg():
    """The gold guarantee seal from the approved Abs By AI sales page (design-sales-page Build.seal), worded for this
    offer: 1 YEAR / 100% MONEY BACK / GUARANTEE (script: "good for a full YEAR", "100% money back refund")."""
    _SEAL_N[0] += 1
    u, ink = _SEAL_N[0], '#3D2A05'
    star = lambda x: f'<polygon points="{_burst(x, 100, 6, 2.5, 5)}" fill="{ink}"></polygon>'
    return (f'<svg class="seal" viewBox="0 0 200 200" role="img" aria-label="1 year 100% money back guarantee">'
            f'<defs><linearGradient id="ga{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FCF1B8"/><stop offset="0.28" stop-color="#E3B64B"/>'
            f'<stop offset="0.52" stop-color="#C08A22"/><stop offset="0.76" stop-color="#F4DA82"/><stop offset="1" stop-color="#A9741A"/></linearGradient>'
            f'<linearGradient id="gb{u}" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF6CC"/><stop offset="0.45" stop-color="#EBC45C"/><stop offset="1" stop-color="#D2A036"/></linearGradient>'
            f'<radialGradient id="gc{u}" cx="0.38" cy="0.30" r="0.85"><stop offset="0" stop-color="#FFF8D6"/><stop offset="0.55" stop-color="#F0CD6A"/><stop offset="1" stop-color="#C9952C"/></radialGradient>'
            f'<path id="gt{u}" d="M 29,100 A 71,71 0 0 1 171,100"/><path id="gu{u}" d="M 17,100 A 83,83 0 0 0 183,100"/></defs>'
            f'<polygon points="{_burst(100, 100, 99, 92, 36)}" fill="url(#ga{u})"/>'
            f'<circle cx="100" cy="100" r="89" fill="url(#gb{u})" stroke="#8A5E12" stroke-width="1.5"/>'
            f'<circle cx="100" cy="100" r="62" fill="url(#gc{u})" stroke="#8A5E12" stroke-width="1.5"/>'
            f'<circle cx="100" cy="100" r="57" fill="none" stroke="#8A5E12" stroke-width="1" stroke-dasharray="2 3"/>'
            f'<g font-family="Archivo,Arial,sans-serif" font-weight="800" fill="{ink}" text-anchor="middle">'
            f'<text font-size="15.5" letter-spacing="1.6"><textPath href="#gt{u}" startOffset="50%">100% MONEY BACK</textPath></text>'
            f'<text font-size="15.5" letter-spacing="3"><textPath href="#gu{u}" startOffset="50%">GUARANTEE</textPath></text>'
            f'{star(23.5)}{star(176.5)}'
            f'<text x="100" y="117" font-size="62" letter-spacing="-1">1</text>'
            f'<text x="102" y="138" font-size="18" letter-spacing="4">YEAR</text></g></svg>')

TERMS = ('<div class="trial"><h3>How Your Free Month Works</h3>'
         '<p>Today you pay only $9.99 for shipping. Your first month’s supply of Great Again T (60 tablets) is free.</p>'
         '<p>If you love it, you’ll get a new bottle every month for $67, starting about 30 days after your order. That’s 31% off the regular $97 price.</p>'
         '<p>Don’t like it? Cancel any time before then, keep your free bottle, and you won’t be billed again.</p>'
         '<p>Return any unopened bottles within one year for a 100% refund.</p></div>')

def offer_card(note=True, idattr=''):
    n = ('<p class="offer-note">If you try Great Again T today, I’ll send you your first month’s supply for FREE. '
         'Just cover the shipping costs, and your first month’s supply is on me.</p>') if note else ''
    return (f'<section class="offer"{idattr}><div class="offer-grid"><div class="free-bottle">'
            f'<img src="{A}bottle-transparent.png" alt="Great Again T, 60 tablets"><div class="burst">FREE<br>BOTTLE</div></div>'
            f'<div class="offer-body">{n}<div class="prices"><p class="regular">Regular price $97</p>'
            '<h2>First month FREE, just $9.99 shipping</h2><p class="then">Then $67 a month</p></div>'
            f'{TERMS}{cta()}</div></div></section>')

ARROWS = '<div class="arrows" aria-hidden="true"><svg viewBox="0 0 160 55"><path d="M25 6l12 33M22 32l15 12 7-18M80 3v42M68 32l12 13 12-13M135 6l-12 33M116 26l7 18 15-12"/></svg></div>'

def studies():
    lis = ''.join(f'<li id="ref-{i + 1}">{html.escape(c)}</li>' for i, c in enumerate(CITES))
    return f'<section class="studies" id="studies"><div class="studies-in"><h2>Studies referenced in this video</h2><ol>{lis}</ol></div></section>'

FOOTER = ('<footer><div class="foot-in">'
          f'<img src="{A}logo/sixpackabs-logo-horizontal-gold.svg" alt="SixPackAbs.com" class="foot-logo">'
          '<p>SixPackAbs.com is owned and operated by Rose Digital Holdings LLC</p><p>3520 Cavu Rd, Georgetown, TX 78628</p>'
          '<p>Support: dan@sixpackabs.com</p><div class="footer-links">'
          + ''.join(f'<span>{m}</span>' for m in MENU) +
          '</div><p>These statements have not been evaluated by the Food and Drug Administration. '
          'This product is not intended to diagnose, treat, cure, or prevent any disease.</p>'
          '<p>© 2026 SixPackAbs.com. All rights reserved.</p></div></footer>')

def photos(kind, label='Real photos of me, not AI-generated', cap=None):
    if kind == 'before':
        items = [('story-before-1-standing.jpg', ''), ('story-before-2-poolside.jpg', 'pp-mid'), ('story-before-3-ride.jpg', '')]
        cap = cap or 'Before 40'
    else:
        items = [('story-after-1-aged.jpg', ''), ('story-after-2-aged.jpg', 'pp-mid'), ('story-after-3-aged.jpg', '')]
        cap = cap or 'Today, at 41'
    figs = ''.join(f'<figure class="{c}"><img src="{A}{f}" alt="Daniel Rose, {cap}"><figcaption>{cap}</figcaption></figure>' for f, c in items)
    return f'<div class="photos3 photos-{kind}">{figs}</div><p class="disclosure">{label}</p>'

def swapimg(name, alt):
    return f'<figure class="swapimg"><img src="{A}{name}" alt="{alt}"></figure>'

INGR = [('Tongkat ali', '400 mg', 'Tongkat ali is a root that grows in the rainforests of Malaysia and Indonesia. Men there have used it for centuries for strength, stamina and male vitality.'),
        ('Zinc', '50 mg', 'Your body literally cannot make T without zinc.'),
        ('Maca root', '250 mg', 'Maca is a root that grows over 13,000 feet up in the Andes mountains of Peru.'),
        ('L-arginine', '250 mg', ''),
        ('Panax ginseng and eleuthero', '125 mg', 'In Chinese, ginseng means ‘man root.’'),
        ('Men’s vitality blend', '745 mg', 'Blend includes tribulus, boron, pumpkin seed, nettle root, oyster extract and more.')]

def ingredients():
    cards = ''.join(f'<article class="ingredient"><header><h3>{n}</h3><span class="dose">{d}</span></header>' + (f'<p>{p}</p>' if p else '') + '</article>' for n, d, p in INGR)
    return f'<div class="ingr"><p class="ingr-k">What’s in Great Again T <span>Per 2-tablet serving</span></p><div class="ingredient-list">{cards}</div></div>'

BADGES = ('<ul class="badges"><li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18v14H3z"/><path d="M3 9h18M3 13h18M3 17h18M3 5h8v8H3z"/></svg>Made in the USA</li>'
          '<li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>FDA-registered facility</li>'
          '<li><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 9.8"/></svg>GMP certified</li></ul>')

# ---------- the letter (from Dan's Doc) ----------
exec(compile((HERE / 'letterdoc.py').read_text(), str(HERE / 'letterdoc.py'), 'exec'))

def sec(body, cls=''):
    return f'<section class="lsec {cls}"><div class="lcol">{body}</div></section>'

def letter():
    return render_letter()

# ---------- CSS ----------
CSS = (HERE / 'page.css').read_text()

def page(title, body, cls=''):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body class="{cls}">{body}</body></html>')

READ = '<p class="read"><a href="#letter">Prefer to read? Read the presentation instead.</a></p>'

def video_page(revealed, bar='top'):
    USED.clear()
    body = header(revealed, bar) + '<main>' + hero()
    if revealed:
        body += ARROWS + offer_card(idattr=' id="offer"')
    else:
        body += READ
    body += studies() + letter() + '</main>' + FOOTER
    if revealed and bar == 'bottom':
        body += dock()
    cls = ('revealed ' if revealed else '') + ('bar-bottom' if bar == 'bottom' else 'bar-top')
    return page('Great Again T', body, cls)

# ---------- checkout ----------
def field(label, ph='', half=False, req=True, sel=None):
    star = '<i>*</i>' if req else ''
    ctrl = (f'<div class="select"><span>{sel}</span><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 8l5 5 5-5"/></svg></div>'
            if sel is not None else f'<div class="input">{ph}</div>')
    return f'<label class="field{" half" if half else ""}"><span>{label}{star}</span>{ctrl}</label>'

def step(n, title):
    return f'<h2 class="step"><span>{n}</span>{title}</h2>'

def checkout():
    choose = ('<div class="choose">'
              '<div class="opt on"><span class="radio"></span>' + f'<img src="{A}bottle-transparent.png" alt="">' +
              '<div><b>Free Month’s Supply</b><span>60 tablets. Just pay $9.99 shipping today</span><span class="then">Then $67 a month, cancel any time</span></div><em>$0.00</em></div>'
              '<div class="opt"><span class="radio"></span>' + f'<img src="{A}bottle-transparent.png" alt="">' +
              '<div><b>One bottle, one time</b><span>60 tablets. No monthly shipments</span></div><em>$97.00</em></div></div>')
    summary = ('<table class="sum"><tr><td>Great Again T, free month’s supply</td><td>$0.00</td></tr>'
               '<tr><td>Subtotal</td><td>$0.00</td></tr><tr><td>Shipping and handling</td><td>$9.99</td></tr>'
               '<tr><td>Sales tax</td><td>$0.00</td></tr><tr class="tot"><td>Order total</td><td>$9.99</td></tr></table>')
    cards = ('<div class="cardlogos" aria-label="We accept Visa, Mastercard, American Express and Discover">'
             '<span>VISA</span><span>Mastercard</span><span>AMEX</span><span>DISCOVER</span></div>')
    form_ship = (step(1, 'Shipping information') + '<div class="fields">'
                 + field('First name', half=True) + field('Last name', half=True) + field('Email') + field('Phone')
                 + '<label class="toggle"><span class="sw"></span><span>Text me order updates and exclusive offers</span></label>'
                 + field('Country', sel='United States') + field('Address') + field('Apt, suite, building', req=False)
                 + field('City') + field('State', half=True, sel='Select') + field('ZIP code', half=True) + '</div>'
                 + '<label class="check"><span class="box"></span>My billing address is different from my shipping address</label>')
    form_pay = (step(3, 'Payment information') + f'<p class="secure-row">{LOCK}Secure checkout, 256-bit encryption</p>' + cards
                + '<div class="fields">' + field('Name on card') + field('Card number', '•••• •••• •••• ••••')
                + field('Expiration', 'MM / YY', half=True) + field('CVV', '123', half=True) + '</div>')
    terms = ('<div class="trial"><h3>How this FREE Trial Offer Works</h3>'
             '<p>With your order today, you will receive a full 60-count bottle of Great Again T at no cost… you just pay $9.99 shipping &amp; handling plus any applicable tax.</p>'
             '<p>You will automatically be enrolled in our Monthly Savings program and will have 30 days to try Great Again T. If you choose to continue after the first free bottle we will ship you a fresh bottle every 30 days (beginning 30 days from your initial order date). Any future bottles will be billed $67 plus tax per bottle, with free shipping, until you decide to cancel.</p>'
             '<p>You can pause, change the frequency or cancel your Monthly Savings subscription quickly and easily anytime by emailing dan@sixpackabs.com.</p></div>'
             '<label class="check agree"><span class="box"></span>By checking this box, you are agreeing to the terms of the offer stated above.</label>'
             f'<a class="cta cta-order" href="#">Complete My Order{ARROW}<small>{LOCK}Secure 256-bit encryption</small></a>'
             '<p class="support"><b>Ask Questions By Email</b><br><a href="mailto:dan@sixpackabs.com">dan@sixpackabs.com</a></p>'
             '<p class="legal">By requesting your free bottle today, you agree to our terms and conditions. Charge will appear as “SIXPACKABS.COM” on your credit card/bank statement.</p>'
             '<p class="fine">Important: Please read all supporting material before use.</p>'
             '<p class="fine">†These statements have not been evaluated by the Food and Drug Administration. Individual results may vary. '
             'This product is not intended to diagnose, treat, cure, or prevent any disease.</p>')
    helps = ('<section class="co-more"><div class="co-more-in"><h2>Great Again T</h2>'
             '<p class="sub">Designed exclusively for men over 40, and built to make your body great again.</p><ul class="checks">'
             + ''.join(f'<li>{x}</li>' for x in ['A full 400 milligrams of tongkat ali, the full research studied dose',
                                               'The full 50 milligrams of zinc your body actually needs',
                                               '14 ingredients that studies have shown support T',
                                               'Takes about seven seconds a day. Just take two tablets',
                                               'Made right here in the USA, in FDA-registered facilities that are GMP certified'])
             + f'</ul><div class="guar co-guar">{seal_svg()}<div><h3>I guarantee you’ll love it, or you don’t pay.</h3>'
             '<p>Just return any unopened bottles, and I’ll happily give you a 100% money back refund. '
             'Your money back guarantee is good for a full YEAR after you receive your shipment.</p></div></div></div></section>')
    body = (header(False, checkout=True) + '<main class="co"><div class="co-grid">'
            '<div class="co-left">' + choose + '<p class="newonly">Your first bottle is free. You pay only $9.99 shipping today.</p></div>'
            '<div class="co-right">' + form_ship + step(2, 'Order summary') + summary + form_pay + terms + '</div></div></main>' + helps + FOOTER)
    return page('Great Again T | Checkout', body, 'checkout')

def build():
    if '--no-export' not in sys.argv:
        export_doc()
    (HERE / '2-before-offer.html').write_text(video_page(False))
    (HERE / '3-after-offer.html').write_text(video_page(True))
    (HERE / '3b-after-offer-bottom-bar.html').write_text(video_page(True, 'bottom'))
    (HERE / '4-checkout.html').write_text(checkout())
    print('built 4 pages')

BANNED = re.compile(r'testosterone|\bdrugs?\b(?! Administration)|needle|prescription|inject|\bTRT\b|estrogen|aromatase|diabetes|cardiovascular|osteoporosis|\bdie\b|passing away|depress|steroid', re.I)

def page_text(h):
    h = re.sub(r'<(style|script)[^>]*>.*?</\1>', ' ', h, flags=re.S)
    attrs = ' '.join(re.findall(r'(?:alt|aria-label|title)="([^"]*)"', h))
    h = re.sub(r'</?(b|strong|em|i|span|a|small)(\s[^>]*)?>', '', h)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', h))
    return re.sub(r'\s+', ' ', t), attrs

def check():
    blocks = load_blocks()
    pg = (HERE / '3-after-offer.html').read_text()
    text, attrs = page_text(pg)
    letter_html = pg[pg.index('<div class="letter"'):pg.index('<footer')]
    ltext, _ = page_text(letter_html)
    pos, missing = 0, []
    seq = []
    for c in COPY:
        m = NUMBERED.match(c)
        seq.extend([m.group(1), m.group(2)] if m else [c])
    missing += [l for l in LABELS if ltext.count(l) < 1]
    for c in seq:
        k = ltext.find(c, pos)
        if k < 0:
            missing.append(c[:70])
        else:
            pos = k + len(c)
    assert not missing, ('Doc paragraphs missing or out of order', missing)
    body_copy = [c for c in seq if len(c) > 25]
    dup = [c[:50] for c in body_copy if ltext.count(c) != 1]
    assert not dup, ('paragraph on the page more than once', dup)
    gold = [b['text'] for b in blocks if is_gold(b['text']) and len(b['text']) > 30]
    leaked = [g[:50] for g in gold if g[1:40] in ltext]
    assert not leaked, ('gold text on the page', leaked)
    assert '[P]' not in text and '[' not in ltext, 'bracket text on the page'
    n_btn = letter_html.count('<a class="cta" ')
    assert n_btn == 5, ('buttons in the letter', n_btn)
    for f in ['2-before-offer.html', '3-after-offer.html', '3b-after-offer-bottom-bar.html', '1-quiz.html', '4-checkout.html']:
        t_, a_ = page_text((HERE / f).read_text())
        raw = (HERE / f).read_text()
        scripts = ' '.join(re.findall(r'<script[^>]*>(.*?)</script>', raw, flags=re.S))
        bad = sorted(set(m.group(0) for m in BANNED.finditer(t_ + ' ' + a_ + ' ' + scripts)))
        assert not bad, (f, 'Google Ads words', bad)
        dash = [c for c in '—–' if c in t_ + a_]
        assert not dash, (f, 'dashes', dash)
    unused = [p for p, _ in STYLE if p not in STYLE_HIT]
    print(f'PASS: {len(COPY)} Doc paragraphs on the page in order, word for word; no gold or [P] text; 5 buttons; '
          f'no Google Ads words or em/en dashes on 5 pages.' + (f' Unmatched style prefixes: {unused}' if unused else ''))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        render_letter()
        check()
    else:
        build()
