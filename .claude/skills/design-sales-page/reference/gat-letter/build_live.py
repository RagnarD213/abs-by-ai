#!/usr/bin/env python3
"""Builds the LIVE Great Again T funnel for shop.sixpackabs.com from the approved generator (gen.py).

    python3 build_live.py            export both Docs, then write the theme files and a local preview
    python3 build_live.py --no-export
    python3 build_live.py check      the copy checks on the built live pages (run after a build)

Writes:
  <theme>/layout/gat.liquid                      one bare layout for all twelve pages (no shop header or footer)
  <theme>/templates/page.gat-quiz.liquid         /pages/great-again-t-quiz
  <theme>/templates/page.gat-sales.liquid        /pages/great-again-t          (before and after the offer, one page)
  <theme>/templates/page.gat-order.liquid        /pages/great-again-t-order    (our order page, hands off to Shopify checkout)
  <theme>/templates/page.gat-info.liquid         the nine information pages, picked by page handle
  <theme>/snippets/gat-info-<key>.liquid
  <theme>/assets/gat.css, gat-quiz.css, gat.js, gat-*.(jpg|png|svg)
  live-preview/*.html                            the same pages as plain files, for checking without the shop

NEVER hand-edit the theme's gat files: a change made there is lost on the next build. Change gen.py, page.css,
live/gat.js or this file. Letter and page copy come only from Dan's two Google Docs.
"""
import html, json, pathlib, re, shutil, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
_argv, sys.argv = sys.argv, [sys.argv[0]]
import gen  # noqa: E402
import onepage  # noqa: E402
sys.argv = _argv

THEME = pathlib.Path.home() / 'Projects/Claude/Projects/SixPackAbs Shop Theme'
PREVIEW = HERE / 'live-preview'

# ---------------------------------------------------------------- settings
LAUNCHED = False          # False: every page carries noindex. Flip to True the day ads start, rebuild, push.
HANDLES = {'quiz': 'great-again-t-quiz', 'sales': 'great-again-t', 'order': 'great-again-t-order',
           'thanks': 'great-again-t-thank-you', 'account': 'great-again-t-account',
           'questions': 'great-again-t-questions', 'how': 'great-again-t-how-it-works',
           'ingredients': 'great-again-t-ingredients', 'shipping': 'great-again-t-shipping-and-returns',
           'contact': 'great-again-t-contact', 'about': 'great-again-t-about',
           'privacy': 'great-again-t-privacy-policy', 'terms': 'great-again-t-terms',
           'disclaimer': 'great-again-t-disclaimer'}
TITLES = {'quiz': 'Great Again T | 4 Quick Questions', 'sales': 'Great Again T | SixPackAbs.com',
          'order': 'Great Again T | Your Order', 'thanks': 'Great Again T | Thank You', 'account': 'Great Again T | Your Account'}
POSTHOG_KEY = 'phc_s3ZXKWHRFQVqK6pYRBRBKtc2ex7LL78CFMHtCfENEQrU'   # the project's public browser key
CFG = {
    'product': '/products/great-again-t.js',
    'singlePrice': 9700,      # cents. The order page only sells when the live shop shows exactly these prices.
    'trialPlanPrice': 5701,   # the plan is $57.01 and Shopify repeats the $9.99 shipping on each refill: $67.00 in total (fix A, 2026-11-17)
    'shipping': 999,
    'discount': 'FREEMONTH',  # Shopify code (id 1565132063042): 100% off Great Again T, subscription only, first payment only, one per customer
    'trialOpen': True,        # False: the free-month button only works with ?preview=1 (see RECEIPT: Shopify adds $9.99
                              # shipping to each $67 refill until the shop's shipping is fixed). True opens it to everyone.
    'video': None,            # {'phone': url, 'desk': url, 'poster': url} once Great Again T VSL (WV-03) is approved
    'revealAt': 0,            # seconds into the film where Dan says "So if you already know you want this"
    'onePage': 'on',          # the one-page order form (pay on our page through Stripe; server: gat-checkout.js in the app repo).
                              # 'off': never. 'preview': only at /pages/great-again-t-order?onepage=1. 'on': for everyone, and
                              # ?classic=1 brings back the two-step Shopify checkout (the fallback).
    'api': 'https://absbyai.com',   # where gat-checkout.js runs
    'monthly': 6700,          # the one-page form's monthly charge: $67.00, shipping included
    'ads': {'id': 'AW-18361229851', 'label': 'RurWCMWDwbodEJvEqLNE'},   # Google Ads conversion "Great Again T Purchase"
    'support': gen.SUPPORT,
    'quiz': gen.QUIZ_Q,
    'links': {},
}

for k, h in HANDLES.items():
    gen.LINKS[k] = f'/pages/{h}'
CFG['links'] = {k: gen.LINKS[k] for k in ('quiz', 'sales', 'order', 'thanks', 'account')}

# ---------------------------------------------------------------- live versions of the pieces that are static in the mockup
def hero_live():
    return ('<section class="hero"><div class="hero-bg" aria-hidden="true"></div><div class="stage">'
            '<h1>Eat More Of These Foods And Less Of Those Foods To Naturally Boost Your T</h1>'
            '<div class="player" id="player"><div class="player-fill" aria-hidden="true"></div>'
            f'<img class="poster" src="{gen.A}poster.jpg" alt="Daniel Rose presenting whole eggs and egg whites">'
            + gen.SOUND.replace('<div class="sound">', '<button type="button" class="sound" id="soundBox">').replace('</span></div>', '</span></button>')
            + '</div></div></section>'
            '<p class="watch">This is a science-based presentation backed by real research. To see the research supporting the food swaps in this video, see the studies below.</p>')


def sales_body():
    gen.USED.clear()
    letter = gen.letter().replace('<img ', '<img loading="lazy" decoding="async" ')   # everything in the letter is below the first screen
    return (gen.header(True) + '<main>' + hero_live() + gen.READ + gen.ARROWS + gen.offer_card(idattr=' id="offer"')
            + gen.studies() + letter + '</main>' + gen.footer())


def order_body():
    """Our order page. One template carries both flows (see onepage.py): the two-step hand-off to Shopify checkout,
    and the one-page form where the buyer pays on this page through Stripe (CFG['onePage'])."""
    return onepage.order_body(gen)


def quiz_parts():
    h = gen.quiz()
    css = re.search(r'<style>(.*?)</style>', h, re.S).group(1)
    body = h[h.index('<body>') + 6:h.index('</body>')]
    body = re.sub(r'<script>.*?</script>', '', body, flags=re.S)     # the quiz logic lives in gat.js on the live page
    return css, body


LIVE_CSS = '''
/* ---------- live page states (build_live.py) ---------- */
.pre .offerbar,.pre .arrows,.pre #offer{display:none}
.revealed .read{display:none}
.player video{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#0e1615}
button.sound{font:inherit;border:0;cursor:pointer;text-align:left}
.sound[hidden]{display:none}
.sound[aria-hidden=true]{cursor:default}
.opt{cursor:pointer;position:relative}
.opt input,.check input{position:absolute;opacity:0;width:1px;height:1px;margin:0}
.opt:has(input:focus-visible){outline:3px solid var(--gold);outline-offset:-3px}
.check{cursor:pointer;position:relative}
.check input:checked+.box{background:var(--win);border-color:var(--win)}
.check input:checked+.box::after{content:"";display:block;width:11px;height:6px;border:solid #fff;border-width:0 0 3px 3px;transform:rotate(-45deg);margin:4px 0 0 3px}
.check input:focus-visible+.box{outline:3px solid var(--gold);outline-offset:2px}
.co-err{margin-top:12px;padding:12px 14px;border-radius:6px;background:#fbeeec;border:1px solid #ecc9c3;color:#8f2f25;font-weight:600;font-size:15px;line-height:1.45}
.co-err[hidden]{display:none}
.co-next{text-align:center;font-size:14px;color:var(--muted);margin-top:12px}
button.cta{width:100%;font-family:inherit;cursor:pointer}
button.cta[disabled]{opacity:.6;cursor:wait}
.co.is-trial .single-only,.co.is-single .trial-only{display:none}
@media (max-width:420px){.cta-order{font-size:18px;padding-left:8px;padding-right:8px}}
.co-right .step:first-child{margin-top:0}
@media (max-width:1023px){.co-left+.co-right .step:first-child{margin-top:26px}}
@media (min-width:1024px){.co-right>.step.classic-only{margin-top:0}}
.co-right>.op-only~.op-only .step{margin-top:26px}
''' + onepage.CSS

# ---------------------------------------------------------------- assets
ASSET_RE = re.compile(r'(src|href)="assets/([^"]+)"')
IMG_MAX = {'swap-shake-bar.jpg': 1100, 'food/': 520, 'film/': 1000, 'story-': 932, 'yt-3min-abs.jpg': 1440, 'bottle-transparent.png': 500,
           'label-supplement-facts.png': 1040}


def flat(name):
    return 'gat-' + name.replace('/', '-')


def used_assets(*htmls):
    names = set()
    for h in htmls:
        names.update(m.group(2) for m in ASSET_RE.finditer(h))
    names.add('poster.jpg')    # page.css uses it as the blurred player and desktop backdrop
    return sorted(names)


def write_asset(name, outdir):
    src, dst = HERE / 'assets' / name, outdir / flat(name)
    limit = next((v for k, v in IMG_MAX.items() if name.startswith(k) or name == k), None)
    if src.suffix.lower() in ('.jpg', '.jpeg', '.png') and limit:
        im = Image.open(src)
        if im.width > limit:
            im = im.resize((limit, round(im.height * limit / im.width)), Image.LANCZOS)
        if src.suffix.lower() == '.png':
            im.save(dst, optimize=True)
        else:
            im.convert('RGB').save(dst, quality=76 if name.startswith('film/') else 82, optimize=True, progressive=True)
    else:
        shutil.copyfile(src, dst)


# ---------------------------------------------------------------- output
PH = ("!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(\".\");2==o.length&&(t=t[o[0]],e=o[1]);"
      "t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement(\"script\")).type=\"text/javascript\",p.async=!0,"
      "p.src=s.api_host+\"/static/array.js\",(r=t.getElementsByTagName(\"script\")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a=\"posthog\","
      "u.people=u.people||[],u.toString=function(t){var e=\"posthog\";return\"posthog\"!==a&&(e+=\".\"+a),t||(e+=\" (stub)\"),e},u.people.toString=function(){"
      "return u.toString(1)+\" (stub)\"},o=\"capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing "
      "has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group "
      "updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys onSessionId\".split(\" \"),n=0;n<o.length;n++)g(u,o[n]);"
      "e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);"
      f"posthog.init('{POSTHOG_KEY}',{{api_host:'https://us.i.posthog.com',person_profiles:'identified_only',mask_all_text:false}});"
      "posthog.register({site:'shop.sixpackabs.com',funnel:'great-again-t',funnel_variant:'letter-d-v1'});")
EARLY = ("try{if(document.body.getAttribute('data-gat')==='sales'&&(localStorage.getItem('gat_revealed')||/[?&]offer=1(&|$)/.test(location.search)))"
         "{document.body.classList.remove('pre');document.body.classList.add('revealed')}}catch(e){}"
         # the one-page order form is chosen before first paint, so the page never flashes the other flow
         "try{if(document.body.getAttribute('data-gat')==='order'){var gq=location.search,gm='" + CFG['onePage'] + "';"
         "if(gm==='on'?!/[?&]classic=1(&|$)/.test(gq):gm==='preview'&&/[?&]onepage=1(&|$)/.test(gq))document.body.classList.add('op')}}catch(e){}")
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;650;700;750;800;850&display=swap" rel="stylesheet">')
ROBOTS = '' if LAUNCHED else '<meta name="robots" content="noindex">'
BODY_CLASS = {'quiz': '', 'sales': 'pre bar-top', 'order': 'checkout', 'info': 'info-page', 'thanks': 'checkout', 'account': 'checkout'}
PAY_PAGES = ('order', 'thanks', 'account')     # the pages that load gat-pay.js

LAYOUT = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
          '<title>{{ page.title | escape }} | SixPackAbs.com</title>\n{% if page_description %}<meta name="description" content="{{ page_description | escape }}">{% endif %}\n'
          '<link rel="canonical" href="{{ canonical_url }}">\n' + ROBOTS + '\n'
          '<link rel="icon" type="image/png" href="{{ \'favicon-32.png\' | asset_url }}">\n' + FONTS + '\n'
          '{% assign gat = template.suffix | remove: \'gat-\' %}\n'
          '{% if gat == \'quiz\' %}{{ \'gat-quiz.css\' | asset_url | stylesheet_tag }}{% else %}{{ \'gat.css\' | asset_url | stylesheet_tag }}{% endif %}\n'
          '<script>{% raw %}' + PH + '{% endraw %}</script>\n'
          '{{ content_for_header }}\n</head>\n'
          '<body data-gat="{{ gat }}" class="{% case gat %}{% when \'sales\' %}pre bar-top{% when \'order\' or \'thanks\' or \'account\' %}checkout{% when \'info\' %}info-page{% endcase %}">\n'
          '<script>{% raw %}' + EARLY + '{% endraw %}</script>\n'
          '{{ content_for_layout }}\n'
          '<script src="{{ \'gat.js\' | asset_url }}" defer></script>\n'
          '{% if gat == \'order\' or gat == \'thanks\' or gat == \'account\' %}<script src="{{ \'gat-pay.js\' | asset_url }}" defer></script>{% endif %}\n'
          '</body>\n</html>\n')


def liquid(body):
    assert '{{' not in body and '{%' not in body, 'page HTML would be read as Liquid'
    return ASSET_RE.sub(lambda m: f'{m.group(1)}="{{{{ \'{flat(m.group(2))}\' | asset_url }}}}"', body)


def contact_liquid(body):
    """The Contact page's form posts through Shopify's own contact form on the live site."""
    a, b = body.index('<form class="info-form"'), body.index('</form>') + 7
    form = body[a:b]
    inner = form[form.index('>') + 1:-7]
    inner = (inner.replace('name="Name"', 'name="contact[Name]" required').replace('name="Email"', 'name="contact[email]" required')
             .replace('name="Order number"', 'name="contact[Order number]"').replace('name="Topic"', 'name="contact[Topic]"')
             .replace('name="Message"', 'name="contact[body]" required'))
    assert inner.count('name="contact[') == 5, inner
    live = ("{% form 'contact', class: 'info-form', id: 'ContactForm' %}"
            "{% if form.posted_successfully? %}<p class=\"info-formok\" role=\"status\">Thank you. Your message was sent.</p>{% endif %}"
            "{% if form.errors %}<p class=\"info-formerr\" role=\"alert\">Please check your email address and message, then send again.</p>{% endif %}"
            + inner + "{% endform %}")
    return liquid(body[:a]) + live + liquid(body[b:])


def preview(body):
    body = ASSET_RE.sub(lambda m: f'{m.group(1)}="{flat(m.group(2))}"', body)
    for k, h in HANDLES.items():
        body = body.replace(f'href="/pages/{h}"', f'href="{h}.html"')
    return body


def preview_doc(kind, title, body, info=None):
    css = 'gat-quiz.css' if kind == 'quiz' else 'gat.css'
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)}</title>{ROBOTS}{FONTS}<link rel="stylesheet" href="{css}"></head>'
            f'<body data-gat="{kind}" class="{BODY_CLASS[kind]}"><script>{EARLY}</script>{preview(body)}'
            '<script src="gat.js" defer></script>' + ('<script src="gat-pay.js" defer></script>' if kind in PAY_PAGES else '') + '</body></html>')


def build():
    if '--no-export' not in sys.argv:
        gen.export_doc()
        gen.export_info_doc()
    sales, order = sales_body(), order_body()
    thanks, account = onepage.thanks_body(gen), onepage.account_body(gen)
    quiz_css, quiz = quiz_parts()
    infos = gen.info_pages()                         # [(key, name, file, title, main)]
    info_bodies = {key: gen.header(False, current=key) + main + gen.footer() for key, _, _, _, main in infos}
    assets = used_assets(sales, order, thanks, account, quiz, *info_bodies.values())

    css = (HERE / 'page.css').read_text() + LIVE_CSS
    css = re.sub(r'url\(assets/([^)]+)\)', lambda m: f'url({flat(m.group(1))})', css)
    quiz_css = re.sub(r'url\(assets/([^)]+)\)', lambda m: f'url({flat(m.group(1))})', quiz_css)
    js = (HERE / 'live/gat.js').read_text()
    pay_js = (HERE / 'live/gat-pay.js').read_text()
    assert '/*CFG*/{}' in js and '/*CFG*/{}' in pay_js

    def cfg(links, src=None, **over):
        return (src or js).replace('/*CFG*/{}', json.dumps(dict(CFG, links=links, **over), ensure_ascii=False, separators=(',', ':')))

    # ---- the theme
    for d in ('layout', 'templates', 'snippets', 'assets'):
        assert (THEME / d).is_dir(), THEME / d
    for old in list((THEME / 'assets').glob('gat-*')) + list((THEME / 'snippets').glob('gat-info-*.liquid')):
        old.unlink()
    (THEME / 'layout/gat.liquid').write_text(LAYOUT)
    head = "{% layout 'gat' %}\n"
    (THEME / 'templates/page.gat-sales.liquid').write_text(head + liquid(sales) + '\n')
    (THEME / 'templates/page.gat-order.liquid').write_text(head + liquid(order) + '\n')
    (THEME / 'templates/page.gat-thanks.liquid').write_text(head + liquid(thanks) + '\n')
    (THEME / 'templates/page.gat-account.liquid').write_text(head + liquid(account) + '\n')
    (THEME / 'templates/page.gat-quiz.liquid').write_text(head + liquid(quiz) + '\n')
    case = head + '{% case page.handle %}\n'
    for key, body in info_bodies.items():
        (THEME / f'snippets/gat-info-{key}.liquid').write_text((contact_liquid(body) if key == 'contact' else liquid(body)) + '\n')
        case += f"{{% when '{HANDLES[key]}' %}}{{% render 'gat-info-{key}' %}}\n"
    (THEME / 'templates/page.gat-info.liquid').write_text(case + '{% endcase %}\n')
    (THEME / 'assets/gat.css').write_text(css)
    (THEME / 'assets/gat-quiz.css').write_text(quiz_css)
    (THEME / 'assets/gat.js').write_text(cfg(CFG['links']))
    (THEME / 'assets/gat-pay.js').write_text(cfg(CFG['links'], pay_js))
    for a in assets:
        write_asset(a, THEME / 'assets')

    # ---- the local preview: the same pages as plain files
    if PREVIEW.exists():
        shutil.rmtree(PREVIEW)
    PREVIEW.mkdir()
    for a in assets:
        shutil.copyfile(THEME / 'assets' / flat(a), PREVIEW / flat(a))
    (PREVIEW / 'gat.css').write_text(css)
    (PREVIEW / 'gat-quiz.css').write_text(quiz_css)
    plinks = {k: HANDLES[k] + '.html' for k in ('quiz', 'sales', 'order', 'thanks', 'account')}
    (PREVIEW / 'gat.js').write_text(cfg(plinks))
    (PREVIEW / 'gat-pay.js').write_text(cfg(plinks, pay_js, api=''))      # the local proof server answers /api/gat itself
    (PREVIEW / f'{HANDLES["sales"]}.html').write_text(preview_doc('sales', TITLES['sales'], sales))
    (PREVIEW / f'{HANDLES["order"]}.html').write_text(preview_doc('order', TITLES['order'], order))
    (PREVIEW / f'{HANDLES["thanks"]}.html').write_text(preview_doc('thanks', TITLES['thanks'], thanks))
    (PREVIEW / f'{HANDLES["account"]}.html').write_text(preview_doc('account', TITLES['account'], account))
    (PREVIEW / f'{HANDLES["quiz"]}.html').write_text(preview_doc('quiz', TITLES['quiz'], quiz))
    for key, name, fn, title, main in infos:
        (PREVIEW / f'{HANDLES[key]}.html').write_text(preview_doc('info', f'{title} | SixPackAbs.com', info_bodies[key]))
    json.dump({'handles': HANDLES, 'titles': dict(TITLES, **{k: f'{t} | SixPackAbs.com' for k, _, _, t, _ in infos}),
               'templates': {k: ('gat-' + k if k in ('quiz', 'sales', 'order', 'thanks', 'account') else 'gat-info') for k in HANDLES},
               'assets': [flat(a) for a in assets]}, open(HERE / 'live/pages.json', 'w'), indent=1)
    kb = sum((THEME / 'assets' / flat(a)).stat().st_size for a in assets) // 1024
    print(f'live build: 14 pages, {len(assets)} pictures ({kb} KB), theme at {THEME}, preview at {PREVIEW}')


def check():
    """The same proof as gen.py check, on what the live build wrote."""
    gen.render_letter()
    P = lambda k: (PREVIEW / f'{HANDLES[k]}.html').read_text()
    sales = P('sales')
    ltext, _ = gen.page_text(sales[sales.index('<div class="letter"'):sales.index('<footer')])
    pos, missing, seq = 0, [], []
    for c in gen.COPY:
        m = gen.NUMBERED.match(c)
        seq.extend([m.group(1), m.group(2)] if m else [c])
    for c in seq:
        k = ltext.find(c, pos)
        if k < 0:
            missing.append(c[:70])
        else:
            pos = k + len(c)
    assert not missing, ('letter paragraphs missing or out of order on the live page', missing)
    assert '[' not in ltext, 'bracket text'
    assert sales.count('<a class="cta" ') == 6, sales.count('<a class="cta" ')    # five in the letter, one under the video
    pages, _ = gen.info_split(gen.info_blocks())
    n = 0
    for key in pages:
        raw = P(key)
        main = raw[raw.index('<main class="info"'):raw.index('</main>')]
        text = gen.page_text(main)[0]
        pos = 0
        for b in pages[key]:
            k = text.find(b['text'], pos)
            assert k >= 0, (key, 'missing or out of order', b['text'][:70])
            pos = k + len(b['text'])
            n += 1
        for sales_el in ('class="cta', 'class="offer', 'offerbar', 'class="seal', 'class="study', 'class="player'):
            assert sales_el not in raw, (key, sales_el)
    files = sorted(PREVIEW.glob('*.html'))
    assert len(files) == 14, len(files)
    for f in files:
        raw = f.read_text()
        assert 'dan@sixpackabs.com' not in raw, (f.name, 'old contact address')
        t, a = gen.page_text(raw)
        bad = sorted(set(m.group(0) for m in gen.BANNED.finditer(t + ' ' + a)))
        assert not bad, (f.name, 'Google Ads words', bad)
        assert not [c for c in '—–' if c in t + a], (f.name, 'dash')
        for h in set(re.findall(r'href="([^"#:/]+\.html)"', raw)):
            assert (PREVIEW / h).exists(), (f.name, 'dead link', h)
        for h in [HANDLES[k] + '.html' for k in pages]:
            assert raw.count(f'href="{h}"') >= 2, (f.name, 'not in both menu and footer', h)
        for src in re.findall(r'(?:src|href)="(gat-[^"]+)"', raw):
            assert (PREVIEW / src).exists(), (f.name, 'missing file', src)
    for name in ('gat.js', 'gat-pay.js'):
        js = (THEME / 'assets' / name).read_text()
        bad = sorted(set(m.group(0) for m in gen.BANNED.finditer(js)))
        assert not bad, (name, bad)
        assert not [c for c in '—–' if c in js], (name, 'dash')
    for f in list((THEME / 'templates').glob('page.gat-*.liquid')) + list((THEME / 'snippets').glob('gat-info-*.liquid')):
        raw = f.read_text()
        assert 'src="assets/' not in raw and 'href="assets/' not in raw and '.html"' not in raw, f.name
        assert f.stat().st_size < 250_000, (f.name, f.stat().st_size)
    order = P('order')
    for need in ('Then $67 a month, cancel any time', '$9.99', '$97.00', 'How this FREE Trial Offer Works', 'id="agree"',
                 'SIXPACKABS.COM', 'Terms and Conditions</a>', 'Privacy Policy</a>', 'Shipping and Returns</a>',
                 'id="op-form"', 'id="op-card-number"', 'id="op-pay"', 'id="co-go"', 'Complete My Order', 'Continue To Secure Checkout'):
        assert need in order, need
    print(f'PASS (live build): {len(gen.COPY)} letter paragraphs and {n} information-page paragraphs on the live pages in order, '
          'word for word; 14 pages free of Google Ads words and dashes; every link and picture resolves; '
          'order page shows both options, the terms box, the tick box and the three policy links.')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        check()
    else:
        build()
        check()
