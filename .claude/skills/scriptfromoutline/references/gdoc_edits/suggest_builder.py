"""Build tracked-change requests for a polish pass on a Google Doc (used 2026-10-10 on the 10/17 shoot doc, 90 edits).

    python3 suggest_builder.py doc.json ops_module [--show] [--batch 22] [--skip 3,7]

doc.json     the saved output of the Docs connector's read_doc
ops_module   a .py file (no extension on the command line) with `ops = [(section, old, new), ...]`
             section = how the script's title paragraph starts; old = text that occurs exactly once in that script
             (straight or curly quotes both match); new = what it should say.

What it does that build.py does not: each edit is cut down to the words that differ, so the suggestion card shows
"single" struck out and not a whole sentence; `old` must match exactly once inside its own script or the op is
reported and skipped; offsets are UTF-16 (what the Docs API counts in); an apostrophe typed straight is inserted
curly when the text it replaces is curly (Dan's own typing).

Send the batches it prints with update_doc, writeControl {"writeMode": "SUGGEST", "requiredRevisionId": <revision>},
HIGHEST index first: batch 0, then 1, and so on, each with the revision id the last call returned. Send two or three
ops alone first, read the doc back and run verify_suggestions.py before the rest. An insert next to a delete comes
back as one suggestion with one id.
"""
import json, re, sys, importlib, os
TR = {'’': "'", '‘': "'", '“': '"', '”': '"', ' ': ' ', '\x0b': ' '}   # \x0b is a soft line break (shift+enter)
def norm(s): return ''.join(TR.get(c, c) for c in s)
def u16(s): return len(s.encode('utf-16-le')) // 2
TITLE = re.compile(r"^((FILMING )?SCRIPT:|LONG FORM|SHORT FORM|B-ROLL SHOT LIST)")

def load(path):
    d = json.load(open(path))['content']
    paras = []
    for el in d['tabs'][0]['documentTab']['body']['content']:
        if 'paragraph' not in el: continue
        txt = ''; pend = False
        for r in el['paragraph']['elements']:
            tr = r.get('textRun')
            if tr is None: raise SystemExit('non-text element at %d: offsets would be wrong' % r['startIndex'])
            pend = pend or bool(tr.get('suggestedInsertionIds') or tr.get('suggestedDeletionIds'))
            txt += tr.get('content', '')
        paras.append({'s': el['startIndex'], 't': txt, 'bullet': bool(el['paragraph'].get('bullet')), 'pend': pend})
    return d['revisionId'], paras

def worddiff(old, new):
    a, b = re.findall(r'\S+|\s+', old), re.findall(r'\S+|\s+', new); i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]: i += 1
    j = 0
    while j < len(a) - i and j < len(b) - i and a[-1 - j] == b[-1 - j]: j += 1
    pre, om, nm = ''.join(a[:i]), ''.join(a[i:len(a) - j]), ''.join(b[i:len(b) - j])
    if om and nm.startswith(om) and re.fullmatch(r'[.,;:]+', nm[len(om):]):    # added punctuation: insert only
        pre += om; nm = nm[len(om):]; om = ''
    return pre, om, nm

def build(path, ops, skip=(), extra_titles=()):
    rev, paras = load(path); N = [norm(p['t']) for p in paras]
    tix = [k for k, t in enumerate(N) if not paras[k]['bullet'] and
           (TITLE.match(t.strip()) or any(t.strip().startswith(x) for x in extra_titles))]
    out, errs = [], []
    for n, (sec, old, new) in enumerate(ops):
        if n in skip: continue
        c = [k for k in tix if N[k].strip().startswith(norm(sec))]
        if len(c) != 1: errs.append((n, 'section matches %d' % len(c), sec)); continue
        k1 = min([k for k in tix if k > c[0]] + [len(paras)])
        hits = [(k, m.start()) for k in range(c[0], k1) for m in re.finditer(re.escape(norm(old)), N[k])]
        if len(hits) != 1: errs.append((n, 'old matches %d' % len(hits), old[:60])); continue
        k, i = hits[0]; raw = paras[k]['t']
        pre, om, nm = worddiff(norm(old), new)
        a = i + len(pre); b = a + len(om); rawold = raw[a:b]
        if "'" in nm and ('’' in rawold or ("'" not in rawold and '’' in raw and "'" not in raw)):
            nm = nm.replace("'", '’')
        s = paras[k]['s'] + u16(raw[:a]); e = s + u16(rawold); reqs = []
        if nm: reqs.append({"insertText": {"location": {"index": e}, "text": nm}})
        if om: reqs.append({"deleteContentRange": {"range": {"startIndex": s, "endIndex": e}}})
        out.append({'n': n, 's': s, 'e': e, 'reqs': reqs, 'pend': paras[k]['pend'], 'sec': sec,
                    'ctx': (raw[max(0, a - 30):a] + '[-' + rawold + '-]{+' + nm + '+}' + raw[b:b + 30]).replace('\n', ' ')})
    out.sort(key=lambda x: -x['s'])
    for x, y in zip(out, out[1:]):
        if y['e'] > x['s']: errs.append((x['n'], 'overlaps op %d' % y['n'], ''))
    return rev, out, errs

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[2])) or '.')
    m = importlib.import_module(os.path.basename(sys.argv[2]))
    arg = lambda f, d: sys.argv[sys.argv.index(f) + 1] if f in sys.argv else d
    skip = {int(x) for x in arg('--skip', '').split(',') if x}
    rev, out, errs = build(sys.argv[1], m.ops, skip, getattr(m, 'extra_titles', ()))
    print('REVISION', rev); print('ops', len(m.ops), 'built', len(out), 'errors', len(errs))
    for e in errs: print('  ERROR', e)
    if any(o['pend'] for o in out): print('  NOTE: ops', [o['n'] for o in out if o['pend']], 'sit in a paragraph that already has a pending suggestion')
    if '--show' in sys.argv:
        for o in sorted(out, key=lambda x: x['s']): print(o['n'], o['ctx'])
    size = int(arg('--batch', '22'))
    for k in range(0, len(out), size):
        print('BATCH', k // size, json.dumps([r for o in out[k:k + size] for r in o['reqs']], ensure_ascii=False, separators=(',', ':')))
