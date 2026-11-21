"""Build the requests for a polish pass on a Google Doc: direct edits and tracked suggestions.

    python3 suggest_builder.py doc.json ops_module --only direct [--show] [--batch 40] [--skip 3,7]
    python3 suggest_builder.py doc.json ops_module --only track  [--show]

doc.json     the saved output of the Docs connector's read_doc
ops_module   a .py file (no extension on the command line) with
             ops = [(section, old, new), (section, old, new, 'direct'), ...]
             section = how the script's title paragraph starts; old = text that occurs exactly once in that script
             (straight or curly quotes both match); new = what it should say.
             The fourth item says how the edit is delivered: 'direct' goes straight into the doc, 'track' (the
             default) becomes a tracked suggestion Dan reviews. Which edits are which: `/copy-edit`, "Straight in,
             or tracked" (Dan, 2026-10-11).

Each edit is cut down to the words that differ, so a change shows as "single" struck out and not a whole sentence.
An `old` that does not match exactly once inside its own script is reported and skipped. Offsets are UTF-16 (what
the Docs API counts in). An apostrophe typed straight is inserted curly when the text it replaces is curly (Dan's
own typing).

Sending (update_doc), in this order:
1. `--only direct`: writeControl {"writeMode": "EDIT", "targetRevisionId": <REVISION it printed>}.
2. read_doc again, run verify_suggestions.py before.json after.json --diff, and read the changed lines.
3. `--only track`, built from that fresh read: {"writeMode": "SUGGEST", "targetRevisionId": <its REVISION>}.
4. read_doc and verify again. An insert next to a delete comes back as one suggestion with one id.
Requests inside one call run highest index first (the builder orders them).

Use targetRevisionId, not requiredRevisionId: with targetRevisionId the doc merges the edit with whatever Dan typed
since the read, so it is safe while he works in the doc (tested 2026-10-11, 46 direct edits and 5 suggestions while
he was accepting others). requiredRevisionId fails the whole call if he changed anything.
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

def build(path, ops, skip=(), extra_titles=(), only=None):
    rev, paras = load(path); N = [norm(p['t']) for p in paras]
    tix = [k for k, t in enumerate(N) if not paras[k]['bullet'] and
           (TITLE.match(t.strip()) or any(t.strip().startswith(x) for x in extra_titles))]
    out, errs = [], []
    for n, op in enumerate(ops):
        sec, old, new = op[:3]; mode = op[3] if len(op) > 3 else 'track'
        if n in skip or (only and mode != only): continue
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
        out.append({'n': n, 's': s, 'e': e, 'reqs': reqs, 'pend': paras[k]['pend'], 'sec': sec, 'mode': mode,
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
    only = arg('--only', None)
    if only not in ('direct', 'track'): raise SystemExit("--only direct or --only track: they are sent in separate calls")
    rev, out, errs = build(sys.argv[1], m.ops, skip, getattr(m, 'extra_titles', ()), only)
    print('REVISION', rev); print('ops', len(m.ops), only, 'built', len(out), 'errors', len(errs))
    print('writeMode:', 'EDIT' if only == 'direct' else 'SUGGEST')
    for e in errs: print('  ERROR', e)
    if any(o['pend'] for o in out): print('  NOTE: ops', [o['n'] for o in out if o['pend']], 'sit in a paragraph that already has a pending suggestion')
    if '--show' in sys.argv:
        for o in sorted(out, key=lambda x: x['s']): print(o['n'], o['ctx'])
    size = int(arg('--batch', '40'))
    for k in range(0, len(out), size):
        print('BATCH', k // size, json.dumps([r for o in out[k:k + size] for r in o['reqs']], ensure_ascii=False, separators=(',', ':')))
