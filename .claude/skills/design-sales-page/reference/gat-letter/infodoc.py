# The nine compliance pages from Dan's Google Doc (Great Again T Compliance Pages - Draft v3).
# Exec'd inside gen.py so it shares its helpers. Black text is page copy, word for word, in Doc order.
# Gold text is notes and never reaches a page (the one gold bracket inside black text is the date line).
from html.parser import HTMLParser as _HP

INFO_DOC_ID = '1QErPnqlCvhgdwfXYut6JL-h6O_iLspkjw2FFznYQeLs'
INFODIR = ROOT / 'compliance/docx'
PUBLISHED = 'November 17, 2026'
GOLD = '#9a7b1c'

# Doc page number, key, menu and footer name, mockup file. Listed in footer order (Doc Part D).
INFO_PAGES = [
    (1, 'questions', 'Questions', 'p-questions.html'),
    (2, 'how', 'How It Works', 'p-how-it-works.html'),
    (8, 'ingredients', 'Ingredients', 'p-ingredients.html'),
    (6, 'shipping', 'Shipping and Returns', 'p-shipping-returns.html'),
    (3, 'contact', 'Contact', 'p-contact.html'),
    (7, 'about', 'About Us', 'p-about.html'),
    (4, 'privacy', 'Privacy Policy', 'p-privacy.html'),
    (5, 'terms', 'Terms and Conditions', 'p-terms.html'),
    (9, 'disclaimer', 'Disclaimer', 'p-disclaimer.html'),
]
INFO_KEY = {n: k for n, k, _, _ in INFO_PAGES}
BOXED = {'how': '6.', 'terms': '5.'}   # the list under this numbered section sits in the bordered box
# Phrases in the copy that link to another page (never to the page they are on).
XREF = [('Contact Us page', 'contact'), ('Privacy Policy', 'privacy'), ('Ingredients and Label page', 'ingredients'),
        ('Shipping and Returns page', 'shipping')]


def export_info_doc():
    x = INFODIR / 'x'
    if x.exists():
        shutil.rmtree(x)
    x.mkdir(parents=True)
    subprocess.run(['rclone', 'backend', 'copyid', 'gdrive:', INFO_DOC_ID, str(x) + '/', '--drive-export-formats', 'zip'],
                   check=True, capture_output=True)
    zipfile.ZipFile(glob.glob(str(x / '*.zip'))[0]).extractall(x)


class _Doc(_HP):
    """Blocks with what parse_doc.py drops: font size and colour per run, so headings and gold notes are certain."""
    def __init__(s, css):
        super().__init__(convert_charrefs=True)
        s.cls = {}
        for m in re.finditer(r'\.(c\d+)\{([^}]*)\}', css):
            d = m.group(2)
            size = re.search(r'font-size:(\d+(?:\.\d+)?)pt', d)
            s.cls[m.group(1)] = {'size': float(size.group(1)) if size else None, 'bold': 'font-weight:700' in d,
                                 'gold': GOLD in d}
        s.blocks, s.cur, s.run = [], None, None

    def handle_starttag(s, t, a):
        a = dict(a)
        if t in ('p', 'h1', 'h2', 'h3', 'li'):
            s.cur = {'tag': t, 'runs': []}
        elif t == 'span' and s.cur is not None:
            st = {'size': None, 'bold': False, 'gold': False}
            for c in (a.get('class') or '').split():
                for k, v in s.cls.get(c, {}).items():
                    st[k] = st[k] or v
            s.run = dict(st, text='')
            s.cur['runs'].append(s.run)

    def handle_endtag(s, t):
        if t == 'span':
            s.run = None
        elif t in ('p', 'h1', 'h2', 'h3', 'li') and s.cur is not None:
            c, s.cur = s.cur, None
            runs = [r for r in c['runs'] if r['text'].strip()]
            if runs:
                s.blocks.append({'tag': c['tag'], 'runs': runs})

    def handle_data(s, d):
        if s.run is not None:
            s.run['text'] += d


def info_blocks():
    h = open(glob.glob(str(INFODIR / 'x' / '*.html'))[0], encoding='utf-8').read()
    p = _Doc(re.search(r'<style[^>]*>(.*?)</style>', h, re.S).group(1))
    p.feed(h)
    out = []
    for b in p.blocks:
        runs = b['runs']
        gold = all(r['gold'] for r in runs)
        text = ''
        for r in runs:
            t = r['text']
            if r['gold'] and not gold:      # a gold bracket inside black copy: only the date line is allowed
                assert t.strip() == '[date this page is published]', ('gold text inside page copy', t)
                t = t.replace('[date this page is published]', PUBLISHED)
            text += t
        text = re.sub(r'\s+', ' ', text.replace('\xa0', ' ')).strip()
        black = [r for r in runs if not r['gold']]
        out.append({'tag': b['tag'], 'text': text, 'gold': gold,
                    'size': max((r['size'] or 0) for r in runs),
                    'bold': bool(black) and all(r['bold'] for r in black)})
    return out


def info_split(blocks):
    """{key: [black blocks]}, plus the gold notes per page (only the Contact form note is used)."""
    pages, notes, cur = {}, {}, None
    for b in blocks:
        m = re.match(r'PAGE (\d+) · ', b['text'])
        if m and b['gold']:
            cur = INFO_KEY[int(m.group(1))]
            pages[cur], notes[cur] = [], []
            continue
        if b['text'].startswith('PART ') and b['gold'] and cur:
            cur = None
        if cur is None:
            continue
        if b['gold']:
            notes[cur].append((len(pages[cur]), b['text']))
        else:
            pages[cur].append(b)
    assert set(pages) == set(INFO_KEY.values()), sorted(pages)
    return pages, notes


def _level(b):
    if b['tag'] == 'li':
        return 'li'
    if b['bold'] and b['size'] >= 19:
        return 'h1'
    if b['bold'] and b['size'] >= 14:
        return 'h2'
    if b['bold']:
        return 'h3'
    return 'p'


def _inline(s, key):
    """Escape, then link emails, web addresses and the named pages. The words stay exactly as written."""
    h = esc(s)
    h = re.sub(r'(?<![\w@.])([\w.+-]+@[\w-]+(?:\.[\w-]+)+)', r'<a href="mailto:\1">\1</a>', h)
    h = re.sub(r'(https://[^\s<]*[^\s<.,;)])', r'<a href="\1" rel="noopener">\1</a>', h)
    for phrase, target in XREF:
        if target != key:
            h = h.replace(phrase, f'<a href="{LINKS[target]}">{phrase}</a>')
    return h


def contact_form(note):
    m = re.match(r'\[Form fields: (.*?)\. Button: (.*?)\. Line under the button: (.*?)\]$', note)
    assert m, note
    fields, button, line = m.group(1).split(' · '), m.group(2), m.group(3)
    rows = []
    for f in fields:
        opt = re.match(r'(.*?) \((.*)\)$', f)
        name, extra = (opt.group(1), opt.group(2)) if opt else (f, '')
        fid = 'cf-' + re.sub(r'[^a-z]+', '-', name.lower()).strip('-')
        if ' / ' in extra:
            ctrl = (f'<select id="{fid}" name="{esc(name)}"><option value="">Choose a topic</option>'
                    + ''.join(f'<option>{esc(o)}</option>' for o in extra.split(' / ')) + '</select>')
            lab = name
        elif name == 'Message':
            ctrl, lab = f'<textarea id="{fid}" name="{esc(name)}" rows="6"></textarea>', name
        else:
            typ = 'email' if name == 'Email' else 'text'
            ctrl = f'<input id="{fid}" name="{esc(name)}" type="{typ}" autocomplete="{"email" if typ == "email" else "on"}">'
            lab = name + (f' <span>({esc(extra)})</span>' if extra else '')
        rows.append(f'<div class="info-field"><label for="{fid}">{lab}</label>{ctrl}</div>')
    return ('<form class="info-form" action="#" method="post" data-contact-form>' + ''.join(rows)
            + f'<button type="submit" class="info-send">{esc(button)}</button><p class="info-formline">{esc(line)}</p></form>')


INFO_COPY = {}   # key -> the black paragraphs in Doc order, for the check


def info_body(key, blocks, notes):
    """The page's <main>: the Doc's black blocks in order, each rendered by its level in the Doc."""
    INFO_COPY[key] = [b['text'] for b in blocks]
    form_at = {i: n for i, n in notes if n.startswith('[Form fields:')}
    out, i, n = [], 0, len(blocks)
    box_open = False
    while i < n:
        if i in form_at:
            out.append(contact_form(form_at.pop(i)))
        b = blocks[i]
        lv, s = _level(b), b['text']
        if lv == 'li':
            lis = []
            while i < n and _level(blocks[i]) == 'li' and (i not in form_at or not lis):
                lis.append(f'<li>{_inline(blocks[i]["text"], key)}</li>')
                i += 1
            ul = '<ul>' + ''.join(lis) + '</ul>'
            if box_open:
                ul = f'<div class="info-box">{ul}</div>'
                box_open = False
            out.append(ul)
            continue
        if lv == 'h1':
            out.append(f'<h1>{esc(s)}</h1><hr class="info-rule">')
        elif lv == 'h2':
            box_open = key in BOXED and s.startswith(BOXED[key])
            out.append(f'<h2>{esc(s)}</h2>')
            if key == 'about' and s == 'Our Founder':
                out.append(f'<figure class="info-founder"><img src="{A}founder-kitchen.jpg" alt="Daniel Rose, founder of SixPackAbs.com" width="480" height="480"></figure>')
        elif lv == 'h3':
            out.append(f'<h3>{esc(s)}</h3>')
        else:
            st = re.match(r'(Step \d+\.) (.*)$', s)
            if st:
                out.append(f'<p class="info-step"><b>{st.group(1)}</b> {_inline(st.group(2), key)}</p>')
            elif re.match(r'(Effective date|Last updated): ', s):
                out.append(f'<p class="info-date">{esc(s)}</p>')
            elif s.startswith('These statements have not been evaluated'):
                out.append(f'<p class="info-fda">{esc(s)}</p>')
            else:
                out.append(f'<p>{_inline(s, key)}</p>')
            if key == 'ingredients' and i == 1:   # the real label, right under the title and its opening line
                out.append(f'<figure class="info-label"><img src="{A}label-supplement-facts.png" width="1040" height="1282" '
                           'alt="Great Again T Supplement Facts panel as printed on the bottle"></figure>')
        i += 1
    assert not form_at, form_at
    return f'<main class="info" data-info="{key}"><div class="info-col">' + ''.join(out) + '</div></main>'


def info_pages():
    """[(key, name, file, title, main html)] for the nine pages, from the exported Doc."""
    pages, notes = info_split(info_blocks())
    out = []
    for _, key, name, fn in INFO_PAGES:
        title = next(b['text'] for b in pages[key] if _level(b) == 'h1')
        out.append((key, name, fn, title, info_body(key, pages[key], notes[key])))
    return out
