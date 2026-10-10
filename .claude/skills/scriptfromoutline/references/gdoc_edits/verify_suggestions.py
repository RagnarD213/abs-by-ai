"""After sending suggestions: python3 verify_suggestions.py before.json after.json [ops_module]

Prints the number of pending suggestions in after.json and checks two things: with every suggestion REJECTED the doc
is identical to before.json (nothing was typed in directly), and with every suggestion ACCEPTED each op's new text is
there. before.json and after.json are saved read_doc outputs.
"""
import json, sys, collections, importlib, os
TR = {'’': "'", '‘': "'", '“': '"', '”': '"', ' ': ' ', '\x0b': ' '}
def norm(s): return ''.join(TR.get(c, c) for c in s)
def views(path):
    acc, rej, ids = [], [], collections.Counter()
    for el in json.load(open(path))['content']['tabs'][0]['documentTab']['body']['content']:
        if 'paragraph' not in el: continue
        a = r_ = ''
        for r in el['paragraph']['elements']:
            tr = r.get('textRun')
            if not tr: continue
            ins, dele, c = tr.get('suggestedInsertionIds'), tr.get('suggestedDeletionIds'), tr.get('content', '')
            for i in (ins or []) + (dele or []): ids[i] += 1
            if not dele: a += c
            if not ins: r_ += c
        acc.append(a); rej.append(r_)
    return acc, rej, ids
before, _, pre = views(sys.argv[1]); acc, rej, ids = views(sys.argv[2])
print('pending suggestions:', len(ids), '(before this pass: %d)' % len(pre))
print('reject-all view equals the doc before:', before == rej)
if len(sys.argv) > 3:
    sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[3])) or '.')
    ops = importlib.import_module(os.path.basename(sys.argv[3])).ops; A = norm('\n'.join(acc))
    print('new text missing after accept-all:', [(n, new[:50]) for n, (s, o, new) in enumerate(ops) if norm(new) not in A])
