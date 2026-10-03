# Builds the sales-letter boards (phone + desktop) from Dan's doc blocks, verbatim.
# Round 3 (2026-10-03): the cart's 365-day guarantee, the Lifetime wording, and the 2026-10-01 live edits folded in.
import json, math, re, sys, os, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
B = json.load(open(os.path.join(HERE, 'blocks.json')))
ASSETS_RAW = json.load(open(os.path.join(HERE, 'assets.json')))  # key -> [/_blob/<id>, width, height]
ASSETS = {k: v[0] for k, v in ASSETS_RAW.items()}
ASPECT = {k: v[1] / v[2] for k, v in ASSETS_RAW.items()}

def T(i):
    return B[i]['html'].replace('\xa0', ' ').strip()

def paras(i):
    return [x.strip() for x in re.split(r'\n+', T(i)) if x.strip()]

def plain(i):
    return re.sub(r'<[^>]+>', '', T(i)).strip()

INK, PAPER, WHITE, DARK = '#05070B', '#F6F4F0', '#FFFFFF', '#05070B'
HAIR = '#E4E1DB'
SEAL_INK = '#3D2A05'  # the dark brown lettering on the gold guarantee seal (Dan, 2026-10-03: gold, not the cart's navy circle)

# The 365-day guarantee. Dan approved these lines on the cart (Docs/cart-design-20261002/README.md, 2026-10-02).
# They are not in the letter doc. Use them as written; write no new guarantee copy.
G_TITLE = '365-Day No Risk<br>100% Money Back Guarantee'
G_P1 = "We guarantee you'll love Abs By AI or we'll refund your money."
G_P2 = ("If you're not happy for any reason, email us within 365 days of your first payment for a full refund. "
        "No questions asked.")
G_SHORT = '365-Day Money Back Guarantee'
G_FAQ_Q = "What if I don't like it?"

# Wording that changed after the doc was locked on 2026-09-30. Each old line is in allow.txt / allow_live.txt.
#   130: Dan, 2026-10-01 (past tense). 166 and 173: the web cart sells Monthly and Lifetime since 2026-10-03.
EDITS = {
    130: ('AI Tracks My Calories For Me', 'AI Tracked My Calories For Me'),
    166: ('Renews automatically at the plan price until you cancel.',
          'Monthly renews automatically at $19.99 until you cancel. Lifetime is a one-time charge of $69.99, no recurring billing.'),
    173: ('$19.99 a month or $69.99 a year.', '$19.99 a month, or a one-time charge of $69.99 for lifetime access.'),
}
for _i, (_old, _new) in EDITS.items():
    for _f in ('html', 'text'):
        assert B[_i][_f].count(_old) == 1, (_i, _f)
        B[_i][_f] = B[_i][_f].replace(_old, _new)

ICON = {
    'check': '<polyline points="20 6 9 17 4 12"></polyline>',
    'x': '<line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>',
    'dumbbell': '<path d="M6 7v10M18 7v10M3 9.5v5M21 9.5v5M6 12h12"></path>',
    'camera': '<path d="M4 8h3l2-3h6l2 3h3v11H4z"></path><circle cx="12" cy="13" r="3.5"></circle>',
    'fork': '<path d="M7 3v7a2 2 0 0 0 2 2v9M11 3v7M9 3v7"></path><path d="M17 3c-1.7 1.3-2.5 3.3-2.5 6v4H17v8"></path>',
    'moon': '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"></path>',
    'play': '<circle cx="12" cy="12" r="10"></circle><polygon points="10 8 16 12 10 16 10 8"></polygon>',
    'arrow': '<line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline>',
    'mute': '<path d="M11 5 6 9H2v6h4l5 4V5z"></path><line x1="23" y1="9" x2="17" y2="15"></line><line x1="17" y1="9" x2="23" y2="15"></line>',
    'sound': '<path d="M11 5 6 9H2v6h4l5 4V5z"></path><path d="M15.5 8.5a5 5 0 0 1 0 7"></path><path d="M19 5a10 10 0 0 1 0 14"></path>',
}

def burst(cx, cy, r1, r2, n):
    """Points of an n-tooth serrated circle (the edge of the seal) or, with n=5, a star."""
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append(f'{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}')
    return ' '.join(pts)


def svg(name, size, color, sw=2, extra=''):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex-shrink: 0{extra}">{ICON[name]}</svg>')


class Build:
    def __init__(s, D):
        s.D = D
        s.W = 1280 if D else 390
        s.n = 0  # counter for unique gradient ids in the inline seal SVGs

    def uid(s):
        s.n += 1
        return str(s.n)

    # ---------- primitives ----------
    def section(s, key, bg, inner, dark=False, gap=None, pad=None, center=False):
        D = s.D
        gap = gap if gap is not None else (22 if D else 18)
        pad = pad or ('72px 0' if D else '40px 20px')
        cls = ' class="dark"' if dark else ''
        col_align = ' align-items: center; text-align: center;' if center else ''
        color = f' color: {WHITE};' if dark else ''
        return (f'<section data-k="{key}"{cls} style="@GROW@flex-shrink: 0; display: flex; flex-direction: column; padding: {pad}; background: {bg};{color}">\n'
                f'<div style="display: flex; flex-direction: column; gap: {gap}px; width: 100%; max-width: 720px; margin: 0 auto;{col_align}">\n{inner}\n</div>\n</section>')

    def h2(s, text, extra=''):
        return f'<h2 class="h2"{extra}>{text}</h2>'

    def p(s, h, cls='letter'):
        return f'<p class="{cls}">{h}</p>'

    def ps(s, *idx, lead_last=False):
        out = []
        for i in idx:
            for x in paras(i):
                out.append(x)
        html_ = [s.p(x) for x in out]
        if lead_last:
            html_[-1] = s.p(out[-1], 'letter lead')
        return '\n'.join(html_)

    def ph(s, label, h, radius=12, dark=False, extra=''):
        cls = 'ph phd' if dark else 'ph'
        return f'<div class="{cls}" style="height: {h}px; border-radius: {radius}px{extra}">{label}</div>'

    def chip(s, text, pos='top: 10px; left: 10px'):
        return (f'<span style="position: absolute; {pos}; padding: 5px 9px; border-radius: 999px; background: rgba(5,7,11,0.82); '
                f'color: #FFFFFF; font-size: 11px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase">{text}</span>')

    def pic(s, key, alt, w, radius=12):
        h = round(w / ASPECT[key])
        return f'<img src="{ASSETS[key]}" alt="{alt}" style="display: block; width: {w}px; height: {h}px; flex-shrink: 0; border-radius: {radius}px; align-self: center">'

    def wide(s, key, alt):
        return s.pic(key, alt, 720 if s.D else 350)

    def screen(s, key, alt, w=None, maxh=None, dark=False):
        D = s.D
        maxh = maxh or (620 if D else 470)
        w = w or min(380 if D else 280, round(maxh * ASPECT[key]))
        h = round(w / ASPECT[key])
        border = '#2A2F38' if dark else HAIR
        return (f'<img src="{ASSETS[key]}" alt="{alt}" style="display: block; width: {w}px; height: {h}px; flex-shrink: 0; box-sizing: border-box; '
                f'border: 1px solid {border}; border-radius: 16px; background: #FFFFFF; box-shadow: 0 14px 30px rgba(5,7,11,0.14); align-self: center">')

    def phone1(s, key, alt):
        return s.pic(key, alt, 267 if s.D else 210, 0)

    def phone2(s, a, alt_a, b, alt_b, dark=False):
        D = s.D
        w = 267 if D else 155
        col = '#C9CDD3' if dark else INK
        return (f'<div style="display: flex; align-items: center; justify-content: center; gap: {18 if D else 8}px; padding: 4px 0">'
                f'{s.pic(a, alt_a, w, 0)}{svg("arrow", 26 if D else 20, col, 2.5)}{s.pic(b, alt_b, w, 0)}</div>')

    def option_tag(s, text):
        return (f'<sc-if value="@SLAB@" hint-placeholder-val="@TRUE@"><p style="align-self: center; padding: 5px 12px; border-radius: 999px; '
                f'background: #FFE8CC; color: #7A3E00; font-size: 12px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase">{text}</p></sc-if>')

    def screen_pair(s, a, alt_a, b, alt_b, dark=False):
        D = s.D
        w = 300 if D else 150
        col = '#C9CDD3' if dark else INK
        return (f'<div style="display: flex; align-items: center; justify-content: center; gap: {18 if D else 8}px; padding: 4px 0">'
                f'{s.screen(a, alt_a, w=w, dark=dark)}{svg("arrow", 26 if D else 20, col, 2.5)}{s.screen(b, alt_b, w=w, dark=dark)}</div>')

    def numbered(s, items, dark=False):
        numbg, numfg = ('#FFFFFF', INK) if dark else (INK, '#FFFFFF')
        lis = ''.join(
            f'<li style="display: flex; gap: 14px; align-items: flex-start"><span style="flex-shrink: 0; display: flex; align-items: center; justify-content: center; '
            f'width: 30px; height: 30px; margin-top: 1px; border-radius: 50%; background: {numbg}; color: {numfg}; font-size: 15px; font-weight: 800">{n}</span>'
            f'<p class="letter" style="min-width: 0">{t}</p></li>' for n, t in enumerate(items, 1))
        return f'<ol style="display: flex; flex-direction: column; gap: 16px; padding: 4px 0">{lis}</ol>'

    def cta_block(s, key, bg, terms, dark=False):
        mw = 480 if s.D else 350
        tcol = ' style="text-align: center; color: #C9CDD3"' if dark else ' style="text-align: center"'
        return (f'<section data-k="{key}" style="@GROW@flex-shrink: 0; display: flex; flex-direction: column; align-items: center; padding: {"0 0 72px" if s.D else "0 20px 40px"}; background: {bg}">'
                f'<div style="display: flex; flex-direction: column; gap: 8px; width: 100%; max-width: {mw}px">'
                f'<button type="button" class="cta" style="background: @CTA@">Start My 7-Day Free Trial</button>'
                f'<p class="terms"{tcol}>{terms}</p></div></section>')

    def seal(s):
        # The gold guarantee seal, drawn as inline SVG so it stays sharp at every size. Every word on it comes from
        # the approved title ("365-Day No Risk 100% Money Back Guarantee").
        u, size = s.uid(), (132 if s.D else 116)
        star = lambda x: f'<polygon points="{burst(x, 100, 6, 2.5, 5)}" fill="{SEAL_INK}"></polygon>'
        return (f'<svg width="{size}" height="{size}" viewBox="0 0 200 200" role="img" aria-label="365 day money back guarantee seal" '
                f'style="flex-shrink: 0; display: block; filter: drop-shadow(0 5px 9px rgba(61,42,5,0.30))">'
                f'<defs><linearGradient id="ga{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FCF1B8"></stop><stop offset="0.28" stop-color="#E3B64B"></stop>'
                f'<stop offset="0.52" stop-color="#C08A22"></stop><stop offset="0.76" stop-color="#F4DA82"></stop><stop offset="1" stop-color="#A9741A"></stop></linearGradient>'
                f'<linearGradient id="gb{u}" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF6CC"></stop><stop offset="0.45" stop-color="#EBC45C"></stop>'
                f'<stop offset="1" stop-color="#D2A036"></stop></linearGradient>'
                f'<radialGradient id="gc{u}" cx="0.38" cy="0.30" r="0.85"><stop offset="0" stop-color="#FFF8D6"></stop><stop offset="0.55" stop-color="#F0CD6A"></stop>'
                f'<stop offset="1" stop-color="#C9952C"></stop></radialGradient>'
                f'<path id="gt{u}" d="M 29,100 A 71,71 0 0 1 171,100"></path><path id="gu{u}" d="M 17,100 A 83,83 0 0 0 183,100"></path></defs>'
                f'<polygon points="{burst(100, 100, 99, 92, 36)}" fill="url(#ga{u})"></polygon>'
                f'<circle cx="100" cy="100" r="89" fill="url(#gb{u})" stroke="#8A5E12" stroke-width="1.5"></circle>'
                f'<circle cx="100" cy="100" r="62" fill="url(#gc{u})" stroke="#8A5E12" stroke-width="1.5"></circle>'
                f'<circle cx="100" cy="100" r="57" fill="none" stroke="#8A5E12" stroke-width="1" stroke-dasharray="2 3"></circle>'
                f'<text font-size="15.5" font-weight="800" letter-spacing="1.6" fill="{SEAL_INK}" text-anchor="middle"><textPath href="#gt{u}" startOffset="50%">100% MONEY BACK</textPath></text>'
                f'<text font-size="15.5" font-weight="800" letter-spacing="3" fill="{SEAL_INK}" text-anchor="middle"><textPath href="#gu{u}" startOffset="50%">GUARANTEE</textPath></text>'
                f'{star(23.5)}{star(176.5)}'
                f'<text x="100" y="112" font-size="50" font-weight="800" letter-spacing="-1" fill="{SEAL_INK}" text-anchor="middle">365</text>'
                f'<text x="102" y="134" font-size="17" font-weight="800" letter-spacing="4" fill="{SEAL_INK}" text-anchor="middle">DAY</text></svg>')

    def gcard(s, bg=PAPER):
        # The guarantee block: the cart's title and two sentences beside the gold seal. Phone: seal on top, centred.
        # Desktop: seal on the left. bg is paper on a white section, white with a hairline on a paper section.
        D = s.D
        border = f' border: 1px solid {HAIR};' if bg == WHITE else ''
        lay = 'flex-direction: row; gap: 28px; padding: 28px 32px; text-align: left' if D else 'flex-direction: column; gap: 14px; padding: 24px 20px; text-align: center'
        return (f'<div class="gcard" style="display: flex; align-items: center; {lay}; border-radius: 16px; background: {bg};{border}">{s.seal()}'
                f'<div style="display: flex; flex-direction: column; gap: 10px; min-width: 0">'
                f'<h3 style="font-size: {24 if D else 18}px; line-height: 1.3; font-weight: 800">{G_TITLE}</h3>'
                f'<p style="font-size: {17 if D else 15}px; line-height: 1.55; color: #3F444C">{G_P1}</p>'
                f'<p style="font-size: {17 if D else 15}px; line-height: 1.55; color: #3F444C">{G_P2}</p></div></div>')

    def gline(s, center=False):
        # The short form: one row under a button's terms line, with a small gold check badge.
        u = s.uid()
        badge = (f'<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" style="flex-shrink: 0">'
                 f'<defs><linearGradient id="gm{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FCF1B8"></stop><stop offset="0.45" stop-color="#E3B64B"></stop>'
                 f'<stop offset="1" stop-color="#B07A1E"></stop></linearGradient></defs>'
                 f'<polygon points="{burst(12, 12, 12, 10.4, 14)}" fill="url(#gm{u})"></polygon>'
                 f'<circle cx="12" cy="12" r="8.6" fill="none" stroke="#8A5E12" stroke-width="0.7"></circle>'
                 f'<polyline points="7.6 12.4 10.7 15.3 16.4 9.2" fill="none" stroke="{SEAL_INK}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"></polyline></svg>')
        return (f'<p class="gline" style="display: flex; align-items: center; justify-content: {"center" if center else "flex-start"}; gap: 8px; '
                f'font-size: {15 if s.D else 14}px; line-height: 1.4; font-weight: 800; color: {INK}">{badge}<span>{G_SHORT}</span></p>')

    # ---------- sections ----------
    def top(s):
        D = s.D
        inner_w = 'max-width: 1080px; margin: 0 auto; width: 100%;' if D else ''
        stripe = (f'<div data-k="stripe" style="flex-shrink: 0; display: flex; height: {64 if D else 60}px; padding: 0 {"40px" if D else "12px 0 16px"}; background: {INK}; color: #FFFFFF">'
                  f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 10px; width: 100%; {inner_w}">'
                  f'<img src="/_blob/bf9335dac3fc2f8d33819a110ab2cce3" alt="Abs by AI" style="height: {34 if D else 26}px; width: auto; flex-shrink: 0; filter: invert(1)">'
                  f'<div style="display: flex; align-items: center; gap: {18 if D else 10}px">'
                  f'<p style="font-size: {16 if D else 13}px; font-weight: 800; line-height: 1.25; text-align: right">7-Day Free Trial<br><span style="font-weight: 600; color: #C9CDD3">$0 today</span></p>'
                  f'<button type="button" style="min-height: 44px; padding: 0 {22 if D else 14}px; border: 0; border-radius: 10px; background: @CTA@; color: #FFFFFF; '
                  f'font-family: inherit; font-size: {15 if D else 14}px; font-weight: 800; white-space: nowrap; cursor: pointer">Start Free Trial</button></div></div></div>')
        head = plain(5)
        hl = 'Used AI To Get Abs Instead'
        head_html = head.replace(hl, f'<span class="hl">{hl}</span>')
        sub = plain(6).replace('SUBHEADLINE: ', '', 1)
        hero = (f'<div data-k="hero" style="flex-shrink: 0; display: flex; flex-direction: column; align-items: center; gap: {14 if D else 10}px; '
                f'padding: {"28px 0 24px" if D else "14px 20px 14px"}; text-align: center">'
                f'<h1 style="max-width: {900 if D else 350}px; font-size: {48 if D else 27}px; line-height: {1.12 if D else 1.16}; font-weight: 800; letter-spacing: -.015em; text-wrap: balance">{head_html}</h1>'
                f'<p style="max-width: {760 if D else 350}px; font-size: {21 if D else 16}px; line-height: 1.45; font-weight: 600; color: #2B2F36; text-wrap: balance">{sub}</p></div>')
        vw = 800 if D else 390
        vh = round(vw * 9 / 16)
        vrad = 'border-radius: 16px; box-shadow: 0 18px 40px rgba(5,7,11,0.18);' if D else ''
        video = (f'<div data-k="video" style="flex-shrink: 0; display: flex; justify-content: center">'
                 f'<div style="position: relative; width: {vw}px; height: {vh}px; flex-shrink: 0; background: {INK}; overflow: hidden; {vrad}">'
                 f'<img src="/_blob/818cf8f3f239f5e2a1a071908f085ba2" alt="Video: Dan Rose, founder of Abs By AI" style="display: block; width: 100%; height: 100%; object-fit: cover">'
                 f'<div style="position: absolute; inset: 0; background: rgba(5,7,11,0.28)"></div>'
                 f'<button type="button" style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); display: flex; flex-direction: column; align-items: center; gap: 4px; '
                 f'padding: {"18px 30px" if D else "14px 22px"}; border: @OVBORDER@; border-radius: 14px; background: @OVBG@; color: @OVFG@; font-family: inherit; cursor: pointer; box-shadow: 0 10px 24px rgba(5,7,11,0.35)">'
                 f'<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON["mute"]}</svg>'
                 f'<span style="font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase">Your video is playing</span>'
                 f'<span style="font-size: {19 if D else 17}px; font-weight: 800">Tap to turn on sound</span></button></div></div>')
        sline = plain(9)
        a, b = sline.split('. ', 1)
        sound = (f'<p data-k="soundline" style="flex-shrink: 0; display: flex; align-items: flex-start; justify-content: center; gap: 8px; padding: {"16px 0" if D else "12px 20px"}; '
                 f'font-size: {16 if D else 14}px; line-height: 1.45; font-weight: 600; background: {WHITE if D else PAPER}">'
                 f'{svg("sound", 18, INK, 2, "; margin-top: 1px")}<span><strong style="font-weight: 800">{a}.</strong> {b}</span></p>')
        # offer card 1
        lis = []
        for i in range(13, 18):
            lis.append(f'<li class="chk">{svg("check", 20, "#C9302D", 3, "; margin-top: 3px")}<span style="min-width: 0">{T(i).replace("<strong>[Start My 7-Day Free Trial]</strong>", "")}</span></li>')
        card = (f'<section data-k="offer1" style="flex-shrink: 0; display: flex; justify-content: center; padding: {"28px 0 72px" if D else "20px 20px 36px"}">'
                f'<div style="display: flex; flex-direction: column; gap: 16px; width: 100%; max-width: 720px; box-sizing: border-box; padding: {"32px 36px" if D else "22px 20px"}; '
                f'border: 2px solid {INK}; border-radius: 16px; background: #FFFFFF; box-shadow: 0 14px 30px rgba(5,7,11,0.10)">'
                f'<div style="display: flex; flex-direction: column; gap: 6px"><h2 class="h2">{plain(11)}</h2>'
                f'<p style="font-size: {18 if D else 16}px; line-height: 1.45; font-weight: 700; color: #2B2F36">{plain(12)}</p></div>'
                f'<ul style="display: flex; flex-direction: column; gap: 14px">{"".join(lis)}</ul>'
                f'<button type="button" class="cta" style="background: @CTA@">Start My 7-Day Free Trial</button>'
                f'<p class="terms"><em>{plain(18)}</em></p>{s.gline()}</div></section>')
        return [stripe, hero, video, sound, card]

    def note(s):
        D = s.D
        img = (f'<img src="{ASSETS["avatar"]}" alt="Dan Rose" class="note-av" style="float: left; width: {156 if D else 126}px; height: {182 if D else 147}px; '
               f'margin: {"7px 22px 10px 0" if D else "6px 16px 8px 0"}; border-radius: 14px; object-fit: cover; object-position: center top">')
        out = [x for i in (23, 24, 25, 26) for x in paras(i)]
        gap = f' style="margin-top: {22 if D else 18}px"'
        body = ''.join(f'<p class="letter"{gap if n else ""}>{x}</p>' for n, x in enumerate(out))
        return s.section('note', PAPER, f'<div style="display: flow-root">{img}{body}</div>\n' + s.p(T(27), 'letter lead'))

    def dadbod(s):
        D = s.D
        a1, a2, a3 = ASSETS['before1'], ASSETS['before2'], ASSETS['before3']
        def im(src, alt, w, h, pos='center'):
            return (f'<img src="{src}" alt="{alt}" style="display: block; width: {w}px; height: {h}px; flex-shrink: 0; '
                    f'object-fit: cover; object-position: {pos}; border-radius: 12px">')
        alt1 = 'Real picture of Dan before, shirtless, in a deck chair with sunglasses'
        alt2 = 'Real picture of Dan before, shirt on, with his daughter'
        if D:
            grid = (f'<div style="display: flex; gap: 10px">{im(a1, alt1, 182, 243)}{im(a2, alt2, 194, 243)}{im(a3, alt2, 324, 243)}</div>')
        else:
            grid = (f'<div style="display: flex; flex-direction: column; gap: 8px">{im(a1, alt1, 350, 467)}'
                    f'<div style="display: flex; gap: 8px">{im(a2, alt2, 128, 160)}{im(a3, alt2, 214, 160)}</div></div>')
        inner = '\n'.join([s.h2(plain(29)), s.p(T(30), 'letter lead'), grid, s.ps(33, 34, 35, 36, 37, 38, lead_last=True)])
        return s.section('dadbod', WHITE, inner)

    def portrait(s, key, alt, video=False):
        w, h = (460, 571) if s.D else (350, 420)
        img = (f'<img src="{ASSETS[key]}" alt="{alt}" style="display: block; width: {w}px; height: {h}px; object-fit: cover; '
               f'object-position: center 25%; border-radius: 12px">')
        play = (f'<span style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); display: flex; width: 68px; height: 68px; '
                f'align-items: center; justify-content: center; border-radius: 50%; background: rgba(5,7,11,0.72)">{svg("play", 42, "#FFFFFF", 1.8)}</span>') if video else ''
        return f'<div style="position: relative; align-self: center; width: {w}px">{img}{play}</div>'

    def millions(s):
        inner = '\n'.join([
            s.h2(plain(39)), s.ps(40),
            s.wide('m100s', 'YouTube page of the SixPackAbs.com M-100s video at 4:37, right after Dan\'s set'),
            s.ps(42),
            s.wide('abshot', 'YouTube page of the SixPackAbs.com Crazy 3 Min Home Abs Workout video'),
            s.ps(44, 45, lead_last=True)])
        return s.section('millions', DARK, inner, dark=True)

    def oldway(s):
        q = paras(53)
        callout = (f'<div style="padding: {"24px 28px" if s.D else "20px"}; border-radius: 16px; background: {PAPER}">'
                   f'<p style="font-size: {24 if s.D else 20}px; line-height: 1.35; font-weight: 800; text-wrap: balance">{q[1]}</p></div>')
        inner = '\n'.join([
            s.h2(plain(46)), s.ps(47, 48), s.p(T(49), 'letter lead'),
            s.numbered([T(50), T(51), T(52)]),
            s.p(q[0]), callout, s.p(q[2]),
            s.ps(54, 55, 56, 57, lead_last=True)])
        return s.section('oldway', WHITE, inner)

    def revolution(s):
        inner = '\n'.join([
            s.h2(plain(58)),
            f'<p style="font-size: {25 if s.D else 21}px; line-height: 1.35; font-weight: 800; text-wrap: balance">{T(59)}</p>',
            s.ps(60, 61, 62, 63, lead_last=True)])
        return s.section('revolution', PAPER, inner)

    def whynot(s):
        q = paras(67)
        rows = ''.join(
            f'<p style="padding: 16px 0; {"border-top: 1px solid " + HAIR + ";" if n else ""} font-size: {21 if s.D else 18}px; line-height: 1.4; font-weight: 800; text-wrap: balance">{x}</p>'
            for n, x in enumerate(q[:3]))
        card = (f'<div style="display: flex; flex-direction: column; padding: {"8px 28px" if s.D else "4px 20px"}; border: 2px solid {INK}; border-radius: 16px">{rows}</div>')
        inner = '\n'.join([s.h2(plain(64)), s.ps(65, 66), card, s.p(q[3], 'letter lead')])
        return s.section('whynot', WHITE, inner)

    def awful(s):
        rows = ''.join(
            f'<li style="display: flex; gap: 12px; align-items: flex-start; padding: 14px 0; {"border-top: 1px solid " + HAIR + ";" if n else ""}">'
            f'{svg("x", 22, "#C9302D", 3, "; margin-top: 3px")}<p class="letter" style="min-width: 0">{T(i)}</p></li>'
            for n, i in enumerate([71, 72, 73]))
        fails = f'<ul style="display: flex; flex-direction: column; padding: {"6px 28px" if s.D else "4px 18px"}; border-radius: 16px; background: #FFFFFF; border: 1px solid {HAIR}">{rows}</ul>'
        inner = '\n'.join([
            s.h2(plain(68)),
            s.wide('chatgpt', 'AI-generated image: Dan at a laptop while ChatGPT writes a generic fitness plan'),
            s.p(T(70), 'letter lead'), fails, s.ps(74, 75, lead_last=True)])
        return s.section('awful', PAPER, inner)

    def devoted(s):
        D = s.D
        icons = ['dumbbell', 'camera', 'fork', 'moon']
        cards = ''.join(
            f'<div style="display: flex; flex-direction: column; gap: 10px; padding: {"20px" if D else "16px 14px"}; border-radius: 14px; background: #11151B; border: 1px solid #2A2F38">'
            f'{svg(ic, 26, "#FFFFFF", 2)}<p style="font-size: {17 if D else 15}px; line-height: 1.5; color: #E4E6EA">{T(i)}</p></div>'
            for ic, i in zip(icons, [82, 83, 84, 85]))
        grid = f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px">{cards}</div>'
        big = (f'<p style="padding: {"26px 0" if D else "20px 0"}; border-top: 1px solid #2A2F38; border-bottom: 1px solid #2A2F38; '
               f'font-size: {26 if D else 21}px; line-height: 1.35; font-weight: 800; color: #FFFFFF; text-wrap: balance">{plain(86)}</p>')
        inner = '\n'.join([
            s.h2(plain(76)), s.wide('fivemodels', 'AI-generated image: Dan at his monitors prompting five AI models'), s.ps(77, 78, 79, 80),
            f'<h3 style="font-size: {24 if D else 20}px; line-height: 1.3; font-weight: 800; color: #FFFFFF; text-wrap: balance">{plain(81)}</h3>',
            grid, big, s.ps(87), s.p(T(88), 'letter lead'),
            s.numbered([T(89), T(90), T(91)], dark=True),
            s.ps(92, 93, 94, lead_last=True)])
        return s.section('devoted', DARK, inner, dark=True)

    def friends(s):
        inner = '\n'.join([s.h2(plain(95)), s.ps(96), s.p(T(97), 'letter lead'), s.ps(98, 99)])
        return s.section('friends', WHITE, inner)

    def introducing(s):
        D = s.D
        head = plain(100)
        a, b = head.split(': ', 1)
        h = (f'<h2 class="h2" style="text-align: center">{a}:<br><span class="hl">{b}</span></h2>')
        inner = '\n'.join([
            f'<img src="/_blob/bf9335dac3fc2f8d33819a110ab2cce3" alt="" style="height: {30 if D else 24}px; width: auto; align-self: center">',
            h, s.phone1('home', 'The Abs By AI home screen'),
            s.ps(102, 103, 104, 105, lead_last=True)])
        return s.section('introducing', PAPER, inner)

    def fiveways(s):
        inner = '\n'.join([s.h2(plain(106)), s.ps(107), s.p(T(108), 'letter lead'), s.ps(109)])
        return s.section('fiveways', WHITE, inner)

    def hackhead(s, i):
        t = plain(i)
        a, b = t.split(': ', 1)
        return (f'<div style="display: flex; flex-direction: column; gap: 8px"><p class="eyebrow">{a}</p>{s.h2(b)}</div>')

    def hack1(s):
        D = s.D
        t = T(117)
        c1_end = t.index('" A picture of YOU') + 1
        c1, rest = t[:c1_end], t[c1_end:].strip()
        c2_end = rest.index('" And once') + 1
        c2, c3 = rest[:c2_end], rest[c2_end:].strip()
        pair = (f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px">'
                f'<p style="padding: 16px; border-radius: 14px; background: #FFFFFF; border: 1px solid {HAIR}; font-size: {17 if D else 15}px; line-height: 1.5; color: #3F444C">{c1}</p>'
                f'<p style="padding: 16px; border-radius: 14px; background: {INK}; color: #FFFFFF; font-size: {17 if D else 15}px; line-height: 1.5; font-weight: 700">{c2}</p></div>')
        st = T(118)
        cite_i = st.index(' (Fox')
        study = (f'<div style="display: flex; flex-direction: column; gap: 8px; padding: {"24px 28px" if D else "18px 20px"}; border-radius: 16px; background: #FFFFFF; border: 1px solid {HAIR}">'
                 f'<p class="letter">{st[:cite_i]}</p><p style="font-size: 13px; font-weight: 700; letter-spacing: .02em; color: #4A4F57">{st[cite_i + 1:]}</p></div>')
        inner = '\n'.join([
            s.hackhead(110), s.ps(111),
            s.pic('goallock', "AI-generated: Dan's goal picture as his phone lock screen", 267 if s.D else 210, 0),
            s.ps(113, 114, 115),
            f'<p style="font-size: {25 if D else 21}px; line-height: 1.35; font-weight: 800; text-wrap: balance">{T(116)}</p>',
            pair, s.p(c3), study, s.ps(119)])
        return s.section('hack1', PAPER, inner)

    def hack2(s):
        inner = '\n'.join([
            s.hackhead(120), s.ps(121),
            s.numbered([T(123), T(124), T(125)]),
            s.phone2('workday', 'A workout day with AI exercise videos', 'exercise', 'An exercise page with its demo video'),
            s.ps(127, 128), s.p(T(129), 'letter lead')])
        return s.section('hack2', WHITE, inner)

    def hack3(s):
        inner = '\n'.join([
            s.hackhead(130), s.ps(131, 132, 133),
            s.pic('salmongif', 'Animated: snapping a salmon plate and logging its calories and protein', 267 if s.D else 210, 0),
            s.ps(135),
            f'<p style="font-size: {23 if s.D else 20}px; line-height: 1.35; font-weight: 800; text-wrap: balance">{T(136)}</p>',
            s.ps(137)])
        return s.section('hack3', PAPER, inner)

    def hack4(s):
        inner = '\n'.join([
            s.hackhead(138), s.ps(139, 140),
            s.phone2('foods', 'The AI nutritionist asking which foods you love', 'tacos', 'The meal prep recipes with taco bowls picked'),
            s.ps(142, 143, 144)])
        return s.section('hack4', WHITE, inner)

    def hack5(s):
        inner = '\n'.join([
            s.hackhead(145).replace('class="eyebrow"', 'class="eyebrow" style="color: #F07A77"'), s.ps(146, 147, 148),
            s.phone2('oura', 'A sleep tracker readout of last night', 'briefing', 'The morning sleep briefing', dark=True),
            s.ps(150), s.p(T(151), 'letter lead')])
        return s.section('hack5', DARK, inner, dark=True)

    def trysec(s):
        caps = (f'<p class="caps" style="font-size: 12px; line-height: 1.6; font-weight: 700; letter-spacing: .06em; color: #3F444C; text-align: center">'
                f'<em>{plain(158)}</em></p>')
        mw = 480 if s.D else 350
        buy = (f'<div style="display: flex; flex-direction: column; gap: 10px; align-self: center; width: 100%; max-width: {mw}px">'
               f'<button type="button" class="cta" style="background: @CTA@">Start My 7-Day Free Trial</button>{caps}</div>')
        inner = '\n'.join([s.h2(plain(152)), s.ps(153, 154, 155), buy, s.gcard(WHITE)])
        return s.section('try', PAPER, inner)

    def s10(s):
        D = s.D
        card = (f'<div style="display: flex; flex-direction: column; gap: 16px; padding: {"32px 36px" if D else "22px 20px"}; border: 2px solid {INK}; border-radius: 16px; '
                f'background: #FFFFFF; box-shadow: 0 14px 30px rgba(5,7,11,0.10)">'
                f'<div style="display: flex; flex-direction: column; gap: 6px"><h2 class="h2">{plain(160)}</h2>'
                f'<p style="font-size: {18 if D else 16}px; line-height: 1.45; font-weight: 700; color: #2B2F36">{plain(161)}</p></div>'
                f'<button type="button" class="cta" style="background: @CTA@">Start My 7-Day Free Trial</button>'
                f'<p class="terms">{plain(166)}</p></div>')
        return s.section('s10', WHITE, card, pad=('64px 0 72px' if D else '28px 20px 40px'))

    def straight(s):
        D = s.D
        a = (f'<div style="padding: {"22px 26px" if D else "18px 20px"}; border-radius: 16px; background: #FFFFFF; border: 1px solid {HAIR}">'
             f'<p class="letter" style="color: #3F444C">{T(168)}</p></div>')
        b = (f'<div style="padding: {"22px 26px" if D else "18px 20px"}; border-radius: 16px; background: #FFFFFF; border: 2px solid {INK}; box-shadow: 0 10px 24px rgba(5,7,11,0.08)">'
             f'<p class="letter">{T(169)}</p></div>')
        inner = '\n'.join([s.h2(plain(167).replace('S11 · ', '')), a, b])
        return s.section('straight', PAPER, inner)

    def after_photo(s):
        D = s.D
        return (f'<figure style="display: flex; flex-direction: column; gap: 8px; align-self: center; width: {520 if D else 350}px; text-align: left"><div style="position: relative">'
                f'<img src="{ASSETS["after"]}" alt="Dan Rose at 40, smiling, by the pool" style="display: block; width: {520 if D else 350}px; height: {520 if D else 350}px; object-fit: cover; border-radius: 14px">'
                f'{s.chip("Real photo", "top: 12px; left: 12px")}</div>'
                f'<figcaption style="font-size: 13px; line-height: 1.5; color: #4A4F57"><em>{plain(171)}</em></figcaption></figure>')

    def faq(s):
        items = []
        for n, i in enumerate(range(173, 180)):
            t = T(i)
            m = re.match(r'<strong>(.*?)</strong>\s*(.*)', t, re.S)
            q, a = m.group(1).strip(), m.group(2).strip()
            last = ' border-bottom: 1px solid ' + HAIR + ';' if i == 179 else ''
            items.append(f'<div style="display: flex; flex-direction: column; gap: 6px; padding: 16px 0; border-top: 1px solid {HAIR};{last}">'
                         f'<h3 class="q">{q}</h3><p class="a">{a}</p></div>')
            if i == 174:
                items.append(f'<div class="gfaq" style="display: flex; flex-direction: column; gap: 6px; padding: 16px 0; border-top: 1px solid {HAIR};">'
                             f'<h3 class="q">{G_FAQ_Q}</h3><p class="a">{G_P1} {G_P2}</p></div>')
        inner = '\n'.join([s.h2(plain(172).replace('S12 · ', ''), ' style="padding-bottom: 6px"'), '<div style="display: flex; flex-direction: column">' + ''.join(items) + '</div>'])
        return s.section('faq', WHITE, inner, gap=12)

    def final(s):
        D = s.D
        mw = 480 if D else 350
        see, dan = plain(184).rsplit(' ', 1)
        sign = (f'<div style="display: flex; flex-direction: column; align-items: center; gap: 2px; padding-top: {28 if D else 20}px">'
                f'<p style="font-size: {18 if D else 16}px; color: #3F444C">{see}</p>'
                f'<p style="font-size: {28 if D else 24}px; font-weight: 800; letter-spacing: -.01em">{dan}</p></div>')
        inner = '\n'.join([
            s.h2(plain(181), ' style="text-align: center"'),
            f'<div style="display: flex; flex-direction: column; gap: 8px; align-self: center; width: 100%; max-width: {mw}px">'
            f'<button type="button" class="cta" style="background: @CTA@">Start My 7-Day Free Trial</button>'
            f'<p class="terms" style="text-align: center">{plain(183)}</p>{s.gline(center=True)}</div>', sign, s.after_photo()])
        return s.section('final', PAPER, inner, center=True)

    def footer(s):
        D = s.D
        disc = plain(185).replace('(sources)', '(<a href="#">sources</a>)')
        links = ' · '.join(f'<a href="#">{x}</a>' for x in plain(186).split(' · '))
        return (f'<footer data-k="footer" class="foot" style="@GROW@flex-shrink: 0; display: flex; flex-direction: column; padding: {"36px 0 44px" if D else "28px 20px 32px"}; background: {INK}; color: #A9AEB6; font-size: 12px; line-height: 1.6">'
                f'<div style="display: flex; flex-direction: column; gap: 12px; width: 100%; max-width: 720px; margin: 0 auto">'
                f'<p><em>{disc}</em></p><p>{links}</p><p>© 2026 Abs By AI</p></div></footer>')

    def all_sections(s):
        terms = plain(183)
        out = s.top()
        out += [s.note(), s.dadbod(), s.millions(), s.oldway(), s.revolution(), s.whynot(), s.awful(), s.devoted(),
                s.friends(), s.introducing(), s.fiveways(), s.hack1(), s.hack2(), s.cta_block('cta_h2', WHITE, terms),
                s.hack3(), s.hack4(), s.cta_block('cta_h4', WHITE, terms), s.hack5(), s.trysec(), s.s10(), s.straight(),
                s.cta_block('cta_s11', PAPER, terms), s.faq(), s.final(), s.footer()]
        return out

    def css(s):
        D = s.D
        return f'''body{{margin:0;font-family:'Manrope',system-ui,sans-serif;color:#05070B;background:#FFFFFF;-webkit-font-smoothing:antialiased}}
a{{color:#C9302D}}a:hover{{color:#9E2522}}
h1,h2,h3,p,ul,ol,figure,blockquote{{margin:0}}
ul,ol{{padding:0;list-style:none}}
.eyebrow{{font-size:{14 if D else 13}px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:#C9302D}}
.hl{{box-shadow:inset 0 -{12 if D else 9}px 0 rgba(201,48,45,.22)}}
.h2{{font-size:{36 if D else 26}px;line-height:{1.16 if D else 1.2};font-weight:800;letter-spacing:-.01em;text-wrap:balance}}
.cta{{display:flex;align-items:center;justify-content:center;width:100%;min-height:58px;padding:0 18px;border:0;border-radius:12px;color:#FFFFFF;font-family:inherit;font-size:18px;font-weight:800;cursor:pointer;box-shadow:0 8px 18px rgba(5,7,11,.16)}}
.terms{{font-size:14px;line-height:1.5;color:#3F444C}}
.ph{{display:flex;align-items:center;justify-content:center;box-sizing:border-box;padding:14px;text-align:center;background:repeating-linear-gradient(135deg,#EDEBE6 0 10px,#E4E1DB 10px 20px);color:#3F444C;font-size:12px;font-weight:700;line-height:1.4}}
.phd{{background:repeating-linear-gradient(135deg,#171B22 0 10px,#1E232B 10px 20px);color:#A9AEB6}}
.q{{font-size:{19 if D else 17}px;font-weight:800;line-height:1.35}}
.a{{font-size:{17 if D else 15}px;line-height:1.55;color:#3F444C}}
.letter{{font-size:{19 if D else 17}px;line-height:{1.7 if D else 1.65};color:#1D2127}}
.letter strong{{font-weight:800;color:#05070B}}
.lead{{font-weight:700;color:#05070B}}
.dark .h2{{color:#FFFFFF}}
.dark .letter{{color:#D5D8DD}}
.dark .letter strong,.dark .lead{{color:#FFFFFF}}
.chk{{display:flex;gap:12px;align-items:flex-start;font-size:{17 if D else 15}px;line-height:1.5;color:#1D2127}}
.chk strong{{font-weight:800;color:#05070B}}
.foot a{{color:#D5D8DD}}'''


SCRIPT = r'''class Component extends DCLogic {
renderVals() {
const looks = {
dark: { bg: 'rgba(5,7,11,0.85)', fg: '#FFFFFF', border: '1px solid rgba(255,255,255,0.35)' },
yellow: { bg: '#FFD23F', fg: '#05070B', border: '0' },
white: { bg: '#FFFFFF', fg: '#05070B', border: '0' },
blue: { bg: '#1D4ED8', fg: '#FFFFFF', border: '0' },
red: { bg: 'rgba(201,48,45,0.95)', fg: '#FFFFFF', border: '0' }
};
const plan = (this.state && this.state.plan) || 'monthly';
const on = { border: '2px solid #05070B', dot: '#05070B', checked: 'true' };
const off = { border: '2px solid #D6D2CB', dot: 'transparent', checked: 'false' };
return {
cta: this.props.cta ?? '#15803D',
ov: looks[this.props.overlay ?? 'yellow'] || looks.dark,
pm: plan === 'monthly' ? on : off,
pa: plan === 'annual' ? on : off,
pickM: () => this.setState({ plan: 'monthly' }),
pickA: () => this.setState({ plan: 'annual' }),
showGif: (this.props.salmon ?? 'both') !== 'slideshow',
showSlide: (this.props.salmon ?? 'both') !== 'animated',
showLabels: (this.props.salmon ?? 'both') === 'both'
};
}
}'''

HOLES = {'@SGIF@': '{{showGif}}', '@SSLIDE@': '{{showSlide}}', '@SLAB@': '{{showLabels}}', '@CTA@': '{{cta}}', '@OVBG@': '{{ov.bg}}', '@OVFG@': '{{ov.fg}}', '@OVBORDER@': '{{ov.border}}',
         '@EYEBROW@': '{{eyebrow}}', '@TRUE@': '{{true}}',
         '@PMB@': '{{pm.border}}', '@PMD@': '{{pm.dot}}', '@PMC@': '{{pm.checked}}', '@PICKM@': '{{pickM}}',
         '@PAB@': '{{pa.border}}', '@PAD@': '{{pa.dot}}', '@PAC@': '{{pa.checked}}', '@PICKA@': '{{pickA}}'}
MEASURE = {'@CTA@': '#15803D', '@OVBG@': '#FFD23F', '@OVFG@': '#05070B', '@OVBORDER@': '0',
           '@PMB@': '2px solid #05070B', '@PMD@': '#05070B', '@PMC@': 'true', '@PICKM@': '',
           '@PAB@': '2px solid #D6D2CB', '@PAD@': 'transparent', '@PAC@': 'false', '@PICKA@': ''}


def board(b, title, sections, H_, first, props_first):
    body = '\n\n'.join(sections)
    body = body.replace('@GROW@', '', body.count('@GROW@') - 1).replace('@GROW@', 'flex-grow: 1; ') if '@GROW@' in body else body
    body = re.sub(r' data-k="[^"]*"', '', body)
    for k, v in HOLES.items():
        body = body.replace(k, v)
    props = {"cta": {"editor": "color", "default": "#15803D", "options": ["#15803D", "#16A34A", "#0F6B34"], "section": "Test levers"}}
    if props_first:
        props["overlay"] = {"editor": "enum", "options": ["dark", "yellow", "white", "blue", "red"], "default": "yellow", "section": "Test levers"}
    if '{{showGif}}' in body:
        props["salmon"] = {"editor": "enum", "options": ["both", "animated", "slideshow"], "default": "both", "section": "Hack 3 salmon"}
    props["$preview"] = {"width": b.W, "height": H_}
    pj = json.dumps(props, separators=(',', ':')).replace("'", '&#39;')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
{b.css()}
</style>
</helmet>
<div style="width: {b.W}px; height: {H_}px; display: flex; flex-direction: column; background: #FFFFFF; overflow: hidden">

{body}

</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{pj}'>
{SCRIPT}
</script>
</body>
</html>
'''


def measure_page(b, sections):
    body = '\n\n'.join(sections).replace('@GROW@', '')
    body = re.sub(r'<sc-if [^>]*>', '', body).replace('</sc-if>', '')
    for k, v in MEASURE.items():
        body = body.replace(k, v)
    body = body.replace('onClick=""', '')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>{b.css()}</style></head><body>
<div id="root" style="width: {b.W}px; display: flex; flex-direction: column; background: #FFFFFF">{body}</div>
<pre id="out"></pre>
<script>
document.fonts.ready.then(() => {{ setTimeout(() => {{
const r = [...document.querySelectorAll('#root > [data-k]')].map(e => [e.dataset.k, Math.ceil(e.getBoundingClientRect().height)]);
document.getElementById('out').textContent = 'MEASURE' + JSON.stringify(r) + 'END';
}}, 300); }});
</script></body></html>'''


if __name__ == '__main__':
    mode = sys.argv[1]
    outdir = sys.argv[2]
    for D in (False, True):
        b = Build(D)
        secs = b.all_sections()
        tag = 'desk' if D else 'phone'
        if mode == 'measure':
            open(os.path.join(outdir, f'measure_{tag}.html'), 'w').write(measure_page(b, secs))
        else:
            # optional 3rd argument: another split prefix, e.g. split_r3 for a round that shows only the changed parts
            plan = json.load(open(os.path.join(HERE, f'{sys.argv[3] if len(sys.argv) > 3 else "split"}_{tag}.json')))
            keys = [re.search(r'data-k="([^"]+)"', x).group(1) for x in secs]
            for part in plan['parts']:
                idx = [keys.index(k) for k in part['keys']]
                chunk = [secs[i] for i in idx]
                html_ = board(b, part['title'], chunk, part['h'], idx[0] == 0, idx[0] == 0)
                assert '\u2014' not in html_ and '\u2013' not in html_
                open(os.path.join(outdir, part['file']), 'w').write(html_)
                print('wrote', part['file'], part['h'])
