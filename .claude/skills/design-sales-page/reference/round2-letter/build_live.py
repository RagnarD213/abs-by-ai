# Builds the LIVE /start page (public/start.html) from the approved Round 2 generator (gen.py).
#
# One responsive page: the phone boards are the layout below 900 px, the desktop boards above it. Every section
# comes from gen.py, rendered twice (phone and desktop). The two renders must have the same tags and text; where an
# inline style differs, it becomes a class with the phone value as the base and the desktop value in a media query,
# so the page reproduces both approved boards exactly. Fixed board widths become fluid (width 100% + max-width +
# aspect-ratio) so it fits every phone.
#
# Dan's build decisions (2026-09-30): both plan pickers cut (the cart has its own plan choice; gen.py no longer
# draws them), the FAQ note "(Change when the stores list the app.)" cut, WV-01 A 1.2x self-hosted with the
# tap-for-sound box. 2026-10-03: the cart's 365-day guarantee (gen.gcard, gen.gline, the FAQ item), hidden inside
# the native apps with the rest of the purchase UI.
#
# NEVER hand-edit public/start.html. A change made there is lost on the next build: make it in gen.py or here.
#
#   python3 build_live.py <repo root>          writes <repo>/public/start.html
#   python3 verify_live.py blocks.json <repo>/public/start.html --allow allow_live.txt
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen  # noqa: E402

LIVE = json.load(open(os.path.join(HERE, 'assets_live.json')))  # slot -> [/img/letter/<file>, width, height]
gen.ASSETS.update({k: v[0] for k, v in LIVE.items()})
gen.ASPECT.update({k: v[1] / v[2] for k, v in LIVE.items()})
# Dan cut his note to himself from the FAQ (2026-09-30).
FAQ_NOTE = ' (Change when the stores list the app.)'
assert gen.B[178]['html'].endswith(FAQ_NOTE)
gen.B[178]['html'] = gen.B[178]['html'][:-len(FAQ_NOTE)]

BP = 900  # px: phone layout below, desktop layout at or above
VARIANT = 'letter-v1'
CHECKOUT = f'/?join=1&amp;from=vsl&amp;v={VARIANT}'
POSTER = '/img/letter/video-poster-wv01.jpg'
VIDEO_PHONE = '/video/wv01-a-720.mp4'
VIDEO_DESK = '/video/wv01-a-1080.mp4'
FOOT_LINKS = {'Terms': '/terms', 'Privacy': '/privacy', 'Refunds': '/refunds', 'Disclaimer': '/disclaimer', 'Contact': '/contact'}
SOUND_ICON = gen.ICON['mute']


class Live(gen.Build):
    """gen.Build with the live-page changes: real links, fluid images, no plan pickers, the real video."""

    def wide(s, key, alt):
        return s.pic(key, alt, 720)  # a full-column image: fills the column on every phone (350 at the 390 board)

    def top(s):
        parts = super().top()
        if s.D:
            parts[1] = parts[1].replace('padding: 28px 0 24px', 'padding: 28px 20px 24px', 1)
        parts[0] = ('<header data-k="stripe" class="stripe"><div class="stripe-in">'
                    '<img src="/img/logo.png" alt="Abs by AI" class="stripe-logo" width="360" height="111">'
                    '<div class="stripe-right app-hide-purchase"><p class="stripe-txt">7-Day Free Trial<br><span>$0 today</span></p>'
                    f'<a class="stripe-cta js-cta" data-pos="stripe" href="{CHECKOUT}">Start Free Trial</a></div></div></header>')
        parts[2] = ('<div data-k="video" class="vwrap"><div class="vbox" id="vbox">'
                    f'<video id="vsl" muted autoplay playsinline preload="metadata" poster="{POSTER}" '
                    'aria-label="Video: Dan Rose, founder of Abs By AI">'
                    f'<source src="{VIDEO_PHONE}" type="video/mp4" media="(max-width: {BP - 1}px)">'
                    f'<source src="{VIDEO_DESK}" type="video/mp4"></video>'
                    '<div class="vdim" id="vdim"></div>'
                    '<button type="button" class="soundbox" id="soundBox">'
                    f'<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{SOUND_ICON}</svg>'
                    '<span class="sb-top" id="sbTop">Your video is playing</span><span class="sb-main">Tap to turn on sound</span></button>'
                    '</div></div>')
        # Inside the Android app the purchase UI is hidden; this is what shows instead.
        parts[4] = parts[4].replace('</div></section>', f'{APP_NOTE}</div></section>', 1)
        return parts

    def dadbod(s):
        a1, a2, a3 = gen.ASSETS['before1'], gen.ASSETS['before2'], gen.ASSETS['before3']
        alt1 = 'Real picture of Dan before, shirtless, in a deck chair with sunglasses'
        alt2 = 'Real picture of Dan before, shirt on, with his daughter'
        grid = (f'<div class="before-grid"><img src="{a1}" alt="{alt1}" class="b1"><img src="{a2}" alt="{alt2}" class="b2">'
                f'<img src="{a3}" alt="{alt2}" class="b3"></div>')
        inner = '\n'.join([s.h2(gen.plain(29)), s.p(gen.T(30), 'letter lead'), grid, s.ps(33, 34, 35, 36, 37, 38, lead_last=True)])
        return s.section('dadbod', gen.WHITE, inner)

    def final(s):
        out = super().final()
        return out.replace('<div style="display: flex; flex-direction: column; align-items: center; gap: 2px;',
                           f'{APP_NOTE}<div style="display: flex; flex-direction: column; align-items: center; gap: 2px;', 1)

    def footer(s):
        out = super().footer()
        out = out.replace('(<a href="#">sources</a>)', '(<a href="/sources">sources</a>)')
        for name, href in FOOT_LINKS.items():
            out = out.replace(f'<a href="#">{name}</a>', f'<a href="{href}">{name}</a>')
        assert 'href="#"' not in out
        return out

    def sections(s):
        out = []
        for sec in s.all_sections():
            key = re.search(r'data-k="([^"]+)"', sec).group(1)
            sec = sec.replace('@GROW@', '').replace('/_blob/bf9335dac3fc2f8d33819a110ab2cce3', '/img/logo.png')  # the logo
            for k, v in gen.MEASURE.items():
                sec = sec.replace(k, v)
            sec = sec.replace('<button type="button" class="cta" style="background: #15803D">Start My 7-Day Free Trial</button>',
                              f'<a class="cta js-cta app-hide-purchase" data-pos="{key}" href="{CHECKOUT}">Start My 7-Day Free Trial</a>')
            sec = sec.replace('<p class="terms"', '<p class="terms app-hide-purchase"').replace('<p class="caps"', '<p class="caps app-hide-purchase"')
            for c in ('gline', 'gcard', 'gfaq'):  # the guarantee covers web purchases: hidden in the native apps
                sec = sec.replace(f'class="{c}"', f'class="{c} app-hide-purchase"')
            sec = re.sub(r'<sc-if [^>]*>', '', sec).replace('</sc-if>', '')
            assert '<button type="button" class="cta"' not in sec and not re.search(r'@[A-Z]+@', sec), key
            out.append(fluid(sec))
        return out


APP_NOTE = '<a class="app-only-note app-open" href="/">Open Abs By AI</a>'


def fluid(h):
    """Board-fixed sizes become fluid: big images and the closing figure scale down on narrow phones."""
    def img(m):
        tag = m.group(0)
        mm = re.search(r'width: (\d+)px; height: (\d+)px;', tag)
        if not mm or int(mm.group(1)) < 150 or 'float: left' in tag:
            return tag
        w, hh = mm.groups()
        tag = tag.replace(mm.group(0), f'width: 100%; max-width: {w}px; height: auto; aspect-ratio: {w} / {hh}; min-width: 0;')
        return tag.replace(' flex-shrink: 0;', '')
    h = re.sub(r'<img [^>]*>', img, h)
    h = re.sub(r'(<figure style="[^"]*?)width: (\d+)px;', r'\1width: 100%; max-width: \2px;', h)
    return h


def tokens(h):
    return [t for t in re.split(r'(<[^>]+>)', h) if t != '']


ATTR = re.compile(r'([\w:-]+)="([^"]*)"')


def merge(phone, desk):
    """Same markup, two sets of inline styles: differing styles become classes (phone base, desktop in @media)."""
    tp, td = tokens(phone), tokens(desk)
    assert len(tp) == len(td), (len(tp), len(td))
    classes, rules, out = {}, [], []
    for a, b in zip(tp, td):
        if a == b:
            out.append(a); continue
        assert a.startswith('<') and b.startswith('<'), ('text differs', a[:80], b[:80])
        na, nb = re.match(r'<(\w+)', a).group(1), re.match(r'<(\w+)', b).group(1)
        assert na == nb, (na, nb)
        pa, pb = dict(ATTR.findall(a)), dict(ATTR.findall(b))
        assert pa.keys() == pb.keys(), (a[:120], b[:120])
        diff = {k for k in pa if pa[k] != pb[k]}
        assert diff <= {'style', 'width', 'height'}, (diff, a[:120])
        ps, ds = (pa['style'], pb['style']) if 'style' in diff else ('', '')
        for k in ('width', 'height'):  # svg size attributes: the desktop size comes from CSS
            if k in diff:
                ps = f'{ps}; {k}: {pa[k]}px'.lstrip('; ')
                ds = f'{ds}; {k}: {pb[k]}px'.lstrip('; ')
        key = (ps, ds)
        if key not in classes:
            classes[key] = f'r{len(classes) + 1}'
            rules.append((classes[key], ps, ds))
        cls = classes[key]
        attrs = {k: v for k, v in pa.items() if k not in diff}
        attrs['class'] = (pa.get('class', '') + ' ' + cls).strip()
        selfclose = a.rstrip().endswith('/>')
        out.append(f'<{na} ' + ' '.join(f'{k}="{v}"' for k, v in attrs.items()) + ('/>' if selfclose else '>'))
    css_p = '\n'.join(f'#p .{c}{{{p}}}' for c, p, d in rules)
    css_d = '\n'.join(f'#p .{c}{{{d}}}' for c, p, d in rules)
    return ''.join(out), css_p, css_d


def base_css(bp, bd):
    lp, ld = bp.css().split('\n'), bd.css().split('\n')
    assert len(lp) == len(ld)
    return '\n'.join(lp), '\n'.join(d for p, d in zip(lp, ld) if p != d)


CSS_LIVE = f'''
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%;text-size-adjust:100%}}
img,video{{max-width:100%}}
.page{{display:flex;flex-direction:column;min-height:100vh;background:#FFFFFF;overflow-x:clip}}
.cta{{background:#15803D;text-decoration:none;text-align:center}}
.cta:hover,.stripe-cta:hover{{background:#116A33;color:#FFFFFF}}
.cta:focus-visible,.stripe-cta:focus-visible,.soundbox:focus-visible{{outline:3px solid #FFD23F;outline-offset:2px}}
/* Top stripe, pinned (locked layout). Phone 60 px, desktop 64 px. */
.stripe{{position:sticky;top:env(safe-area-inset-top,0px);z-index:50;flex-shrink:0;display:flex;height:60px;padding:0 12px 0 16px;background:#05070B;color:#FFFFFF}}
.stripe-in{{display:flex;align-items:center;justify-content:space-between;gap:10px;width:100%}}
.stripe-logo{{height:26px;width:auto;flex-shrink:0;filter:invert(1)}}
.stripe-right{{display:flex;align-items:center;gap:10px}}
.stripe-txt{{font-size:13px;font-weight:800;line-height:1.25;text-align:right}}
.stripe-txt span{{font-weight:600;color:#C9CDD3}}
.stripe-cta{{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border-radius:10px;background:#15803D;color:#FFFFFF;font-size:14px;font-weight:800;white-space:nowrap;text-decoration:none}}
@media (max-width:359px){{.stripe{{padding:0 8px 0 10px}}.stripe-logo{{height:22px}}.stripe-txt{{font-size:11px}}.stripe-cta{{padding:0 10px;font-size:13px}}.stripe-right{{gap:8px}}}}
/* Video: WV-01, muted autoplay under the tap-for-sound box (yellow, the approved default). */
.vwrap{{flex-shrink:0;display:flex;justify-content:center}}
.vbox{{position:relative;width:100%;aspect-ratio:16/9;flex-shrink:0;background:#05070B;overflow:hidden}}
.vbox video{{position:absolute;inset:0;display:block;width:100%;height:100%;object-fit:contain;background:#05070B}}
.vdim{{position:absolute;inset:0;background:rgba(5,7,11,0.28);cursor:pointer}}
.soundbox{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;gap:4px;padding:14px 22px;border:0;border-radius:14px;background:#FFD23F;color:#05070B;font-family:inherit;cursor:pointer;box-shadow:0 10px 24px rgba(5,7,11,0.35)}}
.sb-top{{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}}
.sb-main{{font-size:17px;font-weight:800;white-space:nowrap}}
.vbox.live .vdim,.vbox.live .soundbox{{display:none}}
/* Before pictures: natural shape, same crop as the boards. */
.before-grid{{display:grid;grid-template-columns:128fr 214fr;gap:8px}}
.before-grid img{{display:block;width:100%;height:auto;min-width:0;border-radius:12px;object-fit:cover;object-position:center}}
.before-grid .b1{{grid-column:1/-1;aspect-ratio:350/467}}
.before-grid .b2{{aspect-ratio:128/160}}
.before-grid .b3{{aspect-ratio:214/160}}
/* Dan's note photo: smaller on the narrowest phones so the letter keeps a readable column beside it. */
@media (max-width:359px){{#p img.note-av{{width:96px;height:112px;margin-right:12px}}}}
/* Guarantee card title: one size down on the narrowest phones so "100% Money Back Guarantee" stays on one line. */
@media (max-width:359px){{#p .gcard h3{{font-size:16px}}}}
/* Inside the Android app: no purchase UI (memory native-app-iap-gating). */
.app-only-note{{display:none}}
html.native-app #p .app-hide-purchase{{display:none !important}}
html.native-app #p .app-only-note{{display:flex}}
.app-open{{align-items:center;justify-content:center;width:100%;min-height:58px;border-radius:12px;background:#05070B;color:#FFFFFF;font-size:18px;font-weight:800;text-decoration:none}}
.app-open:hover{{color:#FFFFFF}}
[data-k="final"] .app-open{{max-width:350px;align-self:center}}
'''

CSS_LIVE_DESK = '''
.stripe{height:64px;padding:0 40px}
.stripe-in{max-width:1080px;margin:0 auto}
.stripe-logo{height:34px}
.stripe-right{gap:18px}
.stripe-txt{font-size:16px}
.stripe-cta{padding:0 22px;font-size:15px}
.vbox{max-width:800px;border-radius:16px;box-shadow:0 18px 40px rgba(5,7,11,0.18)}
.soundbox{padding:18px 30px}
.sb-main{font-size:19px}
.before-grid{grid-template-columns:182fr 194fr 324fr;gap:10px}
.before-grid .b1{grid-column:auto;aspect-ratio:182/243}
.before-grid .b2{aspect-ratio:194/243}
.before-grid .b3{aspect-ratio:324/243}
[data-k="final"] .app-open{max-width:480px}
'''


def head(css):
    title = 'I Fired My Personal Trainer And Used AI To Get Abs Instead | Abs By AI'
    desc = gen.plain(6).replace('SUBHEADLINE: ', '', 1)
    tracking = open(os.path.join(HERE, 'tracking_head.html')).read()
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<!-- Paid-traffic landing page: kept out of the organic index so it never competes with / . -->
<meta name="robots" content="noindex,follow" />
<link rel="canonical" href="https://absbyai.com/start" />
<meta property="og:title" content="{gen.plain(5)}" />
<meta property="og:description" content="{desc}" />
<meta property="og:image" content="https://absbyai.com{POSTER}" />
<meta property="og:url" content="https://absbyai.com/start" />
<meta name="theme-color" content="#05070B" />
<link rel="icon" type="image/png" href="/img/icon-192.png" />
<link rel="apple-touch-icon" href="/img/icon-192.png" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="{POSTER}" />
<script>
  // Inside the Android app (TWA) or the iOS app the purchase UI is hidden, same check as index.html.
  (function () {{
    if ((document.referrer || '').indexOf('android-app://com.absbyai.app') === 0) {{ try {{ sessionStorage.setItem('absbyai_twa', '1'); }} catch (e) {{}} }}
    var nativeApp = !!(window.Capacitor && window.Capacitor.isNativePlatform && window.Capacitor.isNativePlatform());
    try {{ nativeApp = nativeApp || sessionStorage.getItem('absbyai_twa') === '1'; }} catch (e) {{}}
    if (nativeApp) document.documentElement.classList.add('native-app');
    window.VSL = {{ variant: '{VARIANT}', nativeApp: nativeApp }};
  }})();
</script>
{tracking}
<style>
{css}
</style>
</head>
'''


SCRIPT = f'''<script>
(function () {{
  var VSL = window.VSL;
  var $ = function (id) {{ return document.getElementById(id); }};
  function ph(ev, props) {{
    try {{ if (window.posthog && typeof posthog.capture === 'function') posthog.capture(ev, Object.assign({{ variant: VSL.variant }}, props || {{}})); }} catch (e) {{}}
  }}

  // Every buy button goes into the web checkout and carries the ad click ids and UTMs, so the
  // trial conversion that fires in the app (handleCartComplete) is still credited to the ad.
  var query; try {{ query = new URLSearchParams(location.search); }} catch (e) {{ query = null; }}
  function checkoutUrl() {{
    var out = new URLSearchParams();
    out.set('join', '1'); out.set('from', 'vsl'); out.set('v', VSL.variant);
    if (query) query.forEach(function (val, key) {{ if (/^(utm_|gclid$|gbraid$|wbraid$|fbclid$|ttclid$|msclkid$)/.test(key)) out.set(key, val); }});
    return '/?' + out.toString();
  }}
  var href = checkoutUrl();
  Array.prototype.forEach.call(document.querySelectorAll('.js-cta'), function (a) {{
    a.href = href;
    a.addEventListener('click', function () {{ ph('vsl_trial_cta_clicked', {{ position: a.dataset.pos }}); }});
  }});

  // Video: plays muted under the sound box; a tap turns the sound on and restarts it from 0:00.
  var v = $('vsl'), box = $('vbox'), live = false, fired = {{}};
  function soundOn() {{
    if (live) return;
    live = true;
    box.classList.add('live');
    v.muted = false; v.controls = true;
    try {{ v.currentTime = 0; }} catch (e) {{}}
    var p = v.play(); if (p && p.catch) p.catch(function () {{}});
    ph('vsl_sound_on', {{}});
  }}
  $('soundBox').addEventListener('click', soundOn);
  $('vdim').addEventListener('click', soundOn);
  v.muted = true;
  var auto = v.play();
  // Autoplay refused (iOS low power mode, data saver): the box no longer claims the video is playing.
  if (auto && auto.catch) auto.catch(function (e) {{ if (e && e.name === 'NotAllowedError') $('sbTop').style.display = 'none'; }});
  v.addEventListener('playing', function () {{
    $('sbTop').style.display = '';
    if (!live && !fired.auto) {{ fired.auto = 1; ph('vsl_video_play', {{ kind: 'mp4', autoplay: true, muted: true }}); }}
  }});
  // Progress counts only watching with sound (after the tap), so muted autoplay does not inflate it.
  v.addEventListener('timeupdate', function () {{
    if (!live || !v.duration) return;
    var pct = v.currentTime / v.duration * 100;
    [25, 50, 75, 100].forEach(function (m) {{ if (pct >= m - (m === 100 ? 1.5 : 0) && !fired[m]) {{ fired[m] = 1; ph('vsl_video_progress', {{ pct: m, sound: true }}); }} }});
  }});
  v.addEventListener('ended', function () {{ if (live && !fired[100]) {{ fired[100] = 1; ph('vsl_video_progress', {{ pct: 100, sound: true }}); }} }});
  // The muted preview pauses while scrolled away (saves the reader's data) and resumes when back.
  if ('IntersectionObserver' in window) {{
    new IntersectionObserver(function (es) {{
      es.forEach(function (e) {{
        if (live) return;
        if (e.isIntersecting) {{ var p = v.play(); if (p && p.catch) p.catch(function () {{}}); }} else v.pause();
      }});
    }}, {{ threshold: 0.25 }}).observe(box);
  }}

  ph('vsl_landing_seen', {{ video_live: true, native_app: VSL.nativeApp }});
}})();
</script>'''


def lazy(h):
    """Everything below the video loads lazily."""
    first = h.index('data-k="note"')
    head_, tail = h[:first], h[first:]
    tail = re.sub(r'<img (?![^>]*loading=)', '<img loading="lazy" decoding="async" ', tail)
    return head_ + tail


def build(repo):
    bp, bd = Live(False), Live(True)
    sp, sd = bp.sections(), bd.sections()
    body, css_rp, css_rd = merge('\n'.join(sp), '\n'.join(sd))
    base_p, base_d = base_css(bp, bd)
    css = (f'{base_p}\n{CSS_LIVE}\n{css_rp}\n'
           f'@media (min-width: {BP}px) {{\n{base_d}\n{CSS_LIVE_DESK}\n{css_rd}\n}}')
    # Phone headline + subheadline scale with the screen so they keep the board's line breaks on every phone.
    body = body.replace('<h1 class="', '<h1 class="fit-h1 ', 1)
    css += ('\n@media (max-width: %dpx) { #p .fit-h1{font-size:clamp(22px,6.9vw,27px)} #p .fit-sub{font-size:clamp(14px,4.1vw,16px)} }' % (BP - 1))
    body = re.sub(r'(<h1 [^>]*>.*?</h1><p )class="', r'\1class="fit-sub ', body, count=1, flags=re.S)
    body = lazy(body)
    html = head(css) + f'<body>\n<div id="p" class="page">\n{body}\n</div>\n{SCRIPT}\n</body>\n</html>\n'
    assert '\u2014' not in html and '\u2013' not in html, 'em or en dash'
    assert 'href="#"' not in html and '/_blob/' not in html
    out = os.path.join(repo, 'public', 'start.html')
    open(out, 'w').write(html)
    print('wrote', out, len(html), 'bytes;', len(re.findall(r'#p \.r\d+\{', css)) // 2, 'responsive classes')


if __name__ == '__main__':
    build(sys.argv[1])
