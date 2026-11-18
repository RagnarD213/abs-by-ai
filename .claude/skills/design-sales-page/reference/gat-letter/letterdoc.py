# Letter from Dan's Google Doc (Great Again T Sales Letter - Draft v2). Exec'd inside gen.py so it shares its helpers.
# Every black paragraph of Part B is placed in Doc order; gold [bracketed] lines only drive layout.
import subprocess, zipfile, glob, shutil

DOC_ID = '1klwTUdTl5q_17MTA5c1Dtv-Agm_-B3rBpxGQPOj1SCI'
DOCDIR = ROOT / 'docx'
PROJ = ROOT.parents[2]
PARSER = PROJ / '.claude/skills/design-sales-page/scripts/parse_doc.py'

def export_doc():
    x = DOCDIR / 'x'
    if x.exists():
        shutil.rmtree(x)
    x.mkdir(parents=True)
    subprocess.run(['rclone', 'backend', 'copyid', 'gdrive:', DOC_ID, str(x) + '/', '--drive-export-formats', 'zip'],
                   check=True, capture_output=True)
    z = glob.glob(str(x / '*.zip'))[0]
    zipfile.ZipFile(z).extractall(x)
    h = glob.glob(str(x / '*.html'))[0]
    subprocess.run(['python3', str(PARSER), h, str(DOCDIR / 'blocks.json')], check=True, capture_output=True)

def load_blocks():
    return json.load(open(DOCDIR / 'blocks.json'))

def is_gold(s):
    s = s.strip()
    return s.startswith('[') and s.endswith(']')

def clean(s):
    return re.sub(r'\s*\[P\]\s*$', '', s.strip()).replace(' ', ' ')

def part_b(blocks):
    i0 = next(i for i, b in enumerate(blocks) if b['tag'] == 'h2' and b['text'].startswith('PART B'))
    i1 = next(i for i, b in enumerate(blocks) if b['tag'] == 'h3' and b['text'].startswith('A7'))
    secs = []
    for b in blocks[i0 + 1:i1]:
        if b['tag'] == 'h3':
            m = re.match(r'(L\d+b?) · (.*)', b['text'])
            secs.append({'id': m.group(1), 'name': m.group(2), 'items': []})
        elif secs:
            secs[-1]['items'].append(b)
    return secs

def c4_leadins(blocks):
    for b in blocks:
        if b['tag'] == 'li' and 'bold lead-in' in b['text'] and 'Treat these the same way' in b['text']:
            return set(re.findall(r'“([^”]+)”', b['text'].split('Treat these the same way')[1]))
    return set()

LABEL = re.compile(r'^(Eyebrow|HEADLINE|SUBHEADLINE|Founder card|Label under the photos|Caption on each (?:before|after) photo|Sign-off): (.*)$')
NUMBERED = re.compile(r'^((?:Food Swap|T Boosting Nutrient|T Boosting Root) #\d+): (.*)$')
FAQQ = re.compile(r'^\d+\. .+\?$')

def is_subhead(s):
    if NUMBERED.match(s):
        return True
    words = re.findall(r'[A-Za-z][A-Za-z’\']*', s)
    if len(words) < 3:
        return False
    up = sum(1 for w in words if w[0].isupper())
    return up / len(words) >= 0.85

# Text-prefix styles from the Doc's gold notes (kept by prefix so Dan's edits elsewhere never break them).
STYLE = [
    ('If you want to naturally increase your T, eat more', 'swapline'),
    ('And you should stop cooking with this', 'swapline'),
    ('And you should eat less of this meat', 'swapline'),
    ('I’ve listed every one of those studies', 'strong'),
    ('T is the hormone that makes you a man', 'pair-hi'),
    ('But when your T is low', 'pair-lo'),
    ('Eating the right foods changed everything', 'pull'),
    ('That advice is terrible for your T', 'big'),
    ('The only difference was the yolk', 'big'),
    ('If you want more T, eat less of this', 'reveal-line'),
    ('…and more of this', 'reveal-line'),
    ('That’s right. A potato.', 'big'),
    ('But what’s even more powerful', 'big'),
    ('But every supplement I found had problems', 'xlist'),
    ('And the whole thing takes about seven seconds', 'strong'),
    ('Why am I spending my own money', 'q'),
    ('Why am I offering you this discount', 'q'),
    ('NO.', 'no-big'),
    ('Now, it’s your turn.', 'big'),
]
STYLE_HIT = set()
def style_of(s):
    for pre, cls in STYLE:
        if s.startswith(pre):
            STYLE_HIT.add(pre)
            return cls
    return ''

def esc(s):
    return html.escape(s, quote=False)

GREY = lambda what: f'<figure class="todo-img" role="img" aria-label="Picture to come"><span>{esc(what)}</span></figure>'

def tagimg(srcs, tag, alt):
    imgs = ''.join(f'<img src="{A}film/{s}" alt="{alt}">' for s in srcs)
    return f'<figure class="tagimg {tag}{" two" if len(srcs) > 1 else ""}">{imgs}<span class="tag">{tag.title()}</span></figure>'

def swapcard(*sides):
    """Food-only MORE / LESS card (Dan, round 6: no video frame, no head)."""
    tiles = ''.join(f'<figure class="sc-tile {tag}"><span class="tag">{tag.title()}</span>'
                    f'<img src="{A}food/{f}" alt="{name}"><figcaption>{name}</figcaption></figure>' for f, tag, name in sides)
    return f'<div class="swapcard">{tiles}</div>'

def image_for(d, sec):
    t = d.lower()
    if 'egg whites' in t:
        return swapcard(('food-egg-whites.jpg', 'less', 'Egg Whites'), ('food-whole-eggs.jpg', 'more', 'Whole Eggs'))
    if 'butter' in t:
        return swapcard(('food-olive-oil.jpg', 'more', 'Olive Oil'), ('food-butter.jpg', 'less', 'Butter'))
    if 'chicken breast' in t:
        s = swapcard(('food-steak.jpg', 'more', 'Steak'), ('food-chicken.jpg', 'less', 'Chicken Breast'))
        if '5x' in d:
            s += '<p class="statline"><b>5x</b> the zinc in sirloin steak, ounce for ounce</p>'
        return s
    if 'protein shake' in t:
        return tagimg(['shake.jpg', 'bar.jpg'], 'less', 'Protein shake and protein bar')
    if 'baked potato' in t:
        return tagimg(['potato.jpg'], 'more', 'Big baked potato')
    if 'tongkat' in t:
        return f'<figure class="rootimg"><img src="{A}film/tongkat.jpg" alt="Tongkat ali root"></figure>'
    if 'ginseng' in t:
        return f'<figure class="rootimg"><img src="{A}film/ginseng.jpg" alt="Panax ginseng root"></figure>'
    if 'maca' in t:
        return f'<figure class="rootimg"><img src="{A}film/maca.jpg" alt="Maca root in the Andes"></figure>'
    if 'youtube channel' in t:
        return (f'<figure class="ytshot"><img src="{A}yt-3min-abs.jpg" alt="Crazy 3 Min Home Abs Workout on the SixPackAbs.com '
                f'YouTube channel: 4.47M subscribers, 2.6M views"><img class="ytzoom" src="{A}yt-3min-abs-counts.jpg" alt=""></figure>')
    if 'store listing' in t:
        return GREY('Picture to come: the Great Again T store listing at $97 (the live shop shows $47 today)')
    if 'before photos' in t:
        return {'photos': 'before'}
    if 'after photos' in t:
        return {'photos': 'after'}
    raise ValueError('unknown IMAGE direction: ' + d)

def study_from(d):
    body = d.strip()[1:-1].split(':', 1)[1].strip()
    parts = body.split(' · ')
    n = int(re.match(r'Study (\d+)', parts[0]).group(1))
    src = parts[1]
    finding = ' · '.join(parts[2:])
    chart = ''
    m = re.split(r'\s*[Bb]ar chart:?\s*', finding, maxsplit=1)
    if len(m) == 2:
        finding, rest = m
        cap = ''
        if 'Caption:' in rest:
            rest, cap = rest.split('Caption:', 1)
            cap = cap.strip()
        rows = []
        for lab, v, unit, col in re.findall(r'([A-Za-z][A-Za-z0-9 ]*?) ([\d.]+) ?(ng/dL|nmol/L|%) \((grey|green|red)\)', rest):
            rows.append((lab.strip(), float(v), {'grey': 'dim', 'green': 'win', 'red': 'bad'}[col], unit))
        unit = rows[0][3]
        chart = bars([(l, v, c) for l, v, c, _ in rows], unit if unit == '%' else ' ' + unit, esc(cap))
    return (f'<aside class="study"><div class="study-k"><span class="study-n">Study {n}</span>'
            f'<span class="study-src">{esc(src)}</span></div>'
            + (f'<p class="study-f">{esc(finding.strip())}</p>' if finding.strip() else '') + chart + '</aside>')

def bg_of(sec):
    note = next((b['text'] for b in sec['items'] if is_gold(b['text'])), '')
    if sec['id'] == 'L15':
        return 'dark'
    if sec['id'] == 'L19':
        return 'cream'
    if re.search(r'Light tint background|Tint background|Same tint section', note):
        return 'tint'
    return ''

def para(s, cls):
    if cls == 'xlist':
        first, rest = s.split('. ', 1)
        rows = [r.strip() for r in re.split(r'(?<=\.)\s+', rest) if r.strip()]
        return (f'<div class="xlist"><p class="strong">{esc(first)}.</p><ul>'
                + ''.join(f'<li>{esc(r)}</li>' for r in rows) + '</ul></div>')
    if cls == 'pair-hi':
        k = 'When your T is high'
        a, b = s.split(k, 1)
        return f'<p class="paircard hi">{esc(a)}<b>{k}</b>{esc(b)}</p>'
    if cls == 'pair-lo':
        k = 'But when your T is low'
        return f'<p class="paircard lo"><b>{k}</b>{esc(s[len(k):])}</p>'
    if cls == 'leadin' and s.endswith('…') and '. ' in s[:-1]:
        k = s[:-1].rfind('. ') + 2
        return f'<p class="leadin-soft">{esc(s[:k])}<b>{esc(s[k:])}</b></p>'
    c = f' class="{cls}"' if cls else ''
    return f'<p{c}>{esc(s)}</p>'

def subhead(s):
    m = NUMBERED.match(s)
    if m:
        return f'<h2><span class="eyebrow">{esc(m.group(1))}</span>{esc(m.group(2))}</h2>'
    return f'<h2>{esc(s)}</h2>'

COPY = []      # every black Part B paragraph in Doc order (for the check)
LABELS = []    # photo label and caption values: checked for presence (they render inside the photo row)
BUTTONS = [0]

def render_letter():
    blocks = load_blocks()
    secs = part_b(blocks)
    leadset = c4_leadins(blocks)
    COPY.clear(); LABELS.clear(); STYLE_HIT.clear(); BUTTONS[0] = 0
    # flatten to a stream so lead-ins can look ahead across sections
    stream = []
    for si, sec in enumerate(secs):
        for b in sec['items']:
            stream.append((si, b))
    def next_copy(k):
        for j in range(k + 1, len(stream)):
            if not is_gold(stream[j][1]['text']):
                return stream[j]
        return None
    out_secs = [[] for _ in secs]
    carry = {}           # section index -> lead-in html moved to the top of that section
    pending_photos = {}
    first_para_lead = {si for si, s in enumerate(secs)
                       if any(is_gold(b['text']) and re.search(r'first (paragraph|line) is (the|a bold) lead-in', b['text']) for b in s['items'])}
    seen_first = set()
    prev_offer = False
    faq_open = False
    guar_left = 0
    for k, (si, b) in enumerate(stream):
        sec = secs[si]
        o = out_secs[si]
        s = b['text'].strip()
        if is_gold(s):
            d = s
            if d.startswith('[IMAGE:'):
                r = image_for(d, sec)
                if isinstance(r, dict):
                    r = dict(r, label='', cap='')
                    pending_photos[si] = r
                o.append(r)
            elif d.startswith('[STUDY CARD:'):
                o.append(study_from(d))
            elif d.startswith('[OFFER CARD'):
                o.append(offer_card(note=False)); BUTTONS[0] += 1; prev_offer = True; continue
            elif d.startswith('[BUTTON:'):
                if not prev_offer:
                    o.append(cta(d[len('[BUTTON:'):-1].strip())); BUTTONS[0] += 1
            elif d.startswith('[CALLOUT:'):
                n, w = d[len('[CALLOUT:'):-1].strip().split(' · ', 1)
                o.append(f'<div class="dosecall"><b>{esc(n)}</b><span>{esc(w)}</span></div>')
            elif d.startswith('[INGREDIENT CARDS'):
                o.append(ingredients())
            elif d.startswith('[BADGES'):
                o.append(BADGES)
            prev_offer = False
            continue
        prev_offer = False
        s = clean(s)
        m = LABEL.match(s)
        if m:
            key, val = m.group(1), m.group(2)
            if key == 'Eyebrow':
                COPY.append(val); o.append(f'<p class="lh-eyebrow">{esc(val)}</p>')
            elif key == 'HEADLINE':
                COPY.append(val); o.append(f'<h1 class="lh">{esc(val)}</h1>')
            elif key == 'SUBHEADLINE':
                COPY.append(val); o.append(f'<p class="lh-sub">{esc(val)}</p><hr class="lh-rule">')
            elif key == 'Founder card':
                n, t_ = [x.strip() for x in val.split(' / ')]
                COPY.extend([n, t_])
                o.append(f'<div class="founder"><img src="{A}founder-aged-full.jpg" alt="{esc(n)}"><div>'
                         f'<p class="founder-n">{esc(n)}</p><p class="founder-t">{esc(t_)}</p></div></div>')
            elif key == 'Label under the photos':
                LABELS.append(val); pending_photos[si]['label'] = val
            elif key.startswith('Caption on each'):
                LABELS.append(val); pending_photos[si]['cap'] = val
            elif key == 'Sign-off':
                n, t_ = [x.strip() for x in val.split(' / ')]
                COPY.extend([n, t_])
                o.append(f'<div class="signoff"><img src="{A}founder-aged-full.jpg" alt="{esc(n)}"><p><b>{esc(n)}</b>{esc(t_)}</p></div>')
            continue
        COPY.append(s)
        if b['tag'] == 'li':
            o.append({'li': s})
            continue
        if sec['id'] == 'L15':
            o.append(f'<h2>{esc(s)}</h2>' if not any('<h2>' in x for x in o if isinstance(x, str)) else f'<p class="big">{esc(s)}</p>')
            continue
        if sec['id'] == 'L21' and FAQQ.match(s):
            o.append({'faq_q': s})
            continue
        if is_subhead(s):
            if 'Money Back Guarantee' in s:
                o.append({'guar_h': s}); guar_left = 3
            else:
                o.append(subhead(s))
            continue
        cls = style_of(s)
        nxt = next_copy(k)
        lead = (s.endswith('…') or s in leadset or (si in first_para_lead and si not in seen_first)) and nxt and is_subhead(clean(nxt[1]['text']))
        seen_first.add(si)
        if lead:
            cls = 'leadin'
        h_ = para(s, cls)
        if lead and nxt[0] != si:
            carry[nxt[0]] = carry.get(nxt[0], '') + h_
        elif guar_left:
            o.append({'guar_p': h_}); guar_left -= 1
        else:
            o.append(h_)
    # assemble
    html_secs = []
    for si, sec in enumerate(secs):
        items = out_secs[si]
        parts = [carry.get(si, '')]
        i = 0
        while i < len(items):
            x = items[i]
            if isinstance(x, dict) and 'photos' in x:
                parts.append(photos(x['photos'], x['label'], x['cap']))
            elif isinstance(x, dict) and 'li' in x:
                lis = []
                while i < len(items) and isinstance(items[i], dict) and 'li' in items[i]:
                    lis.append(f'<li>{esc(items[i]["li"])}</li>'); i += 1
                parts.append('<ul class="imagine">' + ''.join(lis) + '</ul>'); continue
            elif isinstance(x, dict) and 'faq_q' in x:
                body = [f'<h3>{esc(x["faq_q"])}</h3>']
                i += 1
                while i < len(items) and not (isinstance(items[i], dict) and 'faq_q' in items[i]):
                    body.append(items[i]); i += 1
                parts.append('<article class="faqcard">' + ''.join(body) + '</article>'); continue
            elif isinstance(x, dict) and 'guar_h' in x:
                ps = []
                i += 1
                while i < len(items) and isinstance(items[i], dict) and 'guar_p' in items[i]:
                    ps.append(items[i]['guar_p']); i += 1
                parts.append(f'<div class="guarblock"><div class="guar-head">{seal_svg()}<h3>{esc(x["guar_h"])}</h3></div>'
                             f'<div class="guar-card">{"".join(ps)}</div></div>'); continue
            elif isinstance(x, str) and x.startswith('<p class="paircard hi"') and i + 1 < len(items) and str(items[i + 1]).startswith('<p class="paircard lo"'):
                parts.append(f'<div class="pair">{x}{items[i + 1]}</div>'); i += 2; continue
            elif isinstance(x, str) and x.startswith('<p class="swapline"'):
                row = []
                while i + 1 < len(items) and isinstance(items[i], str) and items[i].startswith('<p class="swapline"'):
                    row.append(f'<div class="swappair">{items[i]}{items[i + 1]}</div>'); i += 2
                parts.append('<div class="swaprow">' + ''.join(row) + '</div>'); continue
            else:
                parts.append(x)
            i += 1
        body = ''.join(p for p in parts if p)
        if sec['id'] == 'L21':
            body = re.sub(r'(<article class="faqcard">.*</article>)', r'<div class="faq">\1</div>', body, flags=re.S)
        if sec['id'] == 'L15':
            body = f'<div class="reveal"><img src="{A}bottle-transparent.png" alt="Great Again T bottle">{seal_svg()}</div>' + body
        if sec['id'] == 'L20b':
            html_secs.append('<section class="lsec reviews" hidden aria-hidden="true"><div class="lcol"><div class="review-cards"></div></div></section>')
            continue
        cls = ' '.join(c for c in [bg_of(sec), 'first' if si == 0 else '', 'last' if si == len(secs) - 1 else ''] if c)
        html_secs.append(f'<section class="lsec {cls}" data-sec="{sec["id"]}"><div class="lcol">{body}</div></section>')
    return '<div class="letter" id="letter">' + ''.join(html_secs) + '</div>'
