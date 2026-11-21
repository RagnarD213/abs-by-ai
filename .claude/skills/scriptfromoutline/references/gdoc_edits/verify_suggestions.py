"""After sending edits: python3 verify_suggestions.py before.json after.json [ops_module] [--diff]

before.json and after.json are saved read_doc outputs. Prints the number of pending suggestions in after.json, whether
the doc with every suggestion REJECTED is identical to before.json, and (with an ops module) whether each op's new
text is there once everything is accepted.

After a tracked-only send, "reject-all view equals the doc before" must be True: nothing was typed in directly.
After a direct send it is False by design: add --diff to print every paragraph that changed, and read the list. Each
line must be one you meant to change. A line you did not plan is either Dan typing at the same moment or a mistake:
look before sending anything else.
"""
import json, sys, collections, importlib, os
TR = {'’': "'", '‘': "'", '“': '"', '”': '"', ' ': ' ', '\x0b': ' '}
def norm(s): return ''.join(TR.get(c, c) for c in s)
def views(path):
    acc, rej, ids = [], [], collections.Counter()
    for el in json.load(open(path))['content']['tabs'][0]['documentTab']['body']['content']:
        if 'paragraph' not in el: continue
        a = r_ = ''; kept = gone = False
        for r in el['paragraph']['elements']:
            tr = r.get('textRun')
            if not tr: continue
            ins, dele, c = tr.get('suggestedInsertionIds'), tr.get('suggestedDeletionIds'), tr.get('content', '')
            for i in (ins or []) + (dele or []): ids[i] += 1
            if not dele: a += c; kept = True
            if not ins: r_ += c; gone = True
        if kept: acc.append(a)        # a paragraph that is only a suggested deletion is not in the accept-all view
        if gone: rej.append(r_)       # a paragraph that is only a suggested insertion is not in the reject-all view
    return acc, rej, ids
args = [a for a in sys.argv[1:] if not a.startswith('--')]
before, _, pre = views(args[0]); acc, rej, ids = views(args[1])
print('pending suggestions:', len(ids), '(before this pass: %d)' % len(pre))
print('reject-all view equals the doc before:', before == rej)
if '--diff' in sys.argv:
    import difflib
    sm = difflib.SequenceMatcher(None, before, rej, autojunk=False); n = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal': continue
        n += 1
        for l in before[i1:i2]:
            if l.strip(): print('  - ', l.rstrip()[:170])
        for l in rej[j1:j2]:
            if l.strip(): print('  + ', l.rstrip()[:170])
    print('changed blocks:', n)
if len(args) > 2:
    sys.path.insert(0, os.path.dirname(os.path.abspath(args[2])) or '.')
    ops = importlib.import_module(os.path.basename(args[2])).ops; A = norm('\n'.join(acc))
    print('new text missing after accept-all:', [(n, op[2][:50]) for n, op in enumerate(ops) if norm(op[2]) not in A])
