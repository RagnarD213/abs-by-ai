#!/usr/bin/env python3
"""Build the 10/23 pool shoot documents from the shoot doc (used 2026-10-20).

    python3 tp_from_1023_doc.py doc.json out_dir "10-23 Pool Shoot"

doc.json is the saved output of the Docs connector's read_doc on the shoot doc (the source is only ever read).
Writes four HTML files into out_dir, plus built_seq.json (every non-empty line of each document, in order) for the
check after upload. Upload and verify: SKILL.md, "No Chrome: upload with rclone".

  Teleprompter 1 - Long Form                   the 7 "SCRIPT:" long-forms, then the 4 follow-along cue tracks
  Teleprompter 2 - Short Form (Part 1 of 2)    shorts 1 to 15
  Teleprompter 3 - Short Form (Part 2 of 2)    shorts 16 to 29
  Filming Document                             shoot notes, every script with its cues and notes, B-roll shot list

How it reads the 10/23 format (tp_from_shoot_doc.py reads the 10/17 one):
- A short is a Heading 3 "N. TITLE"; a follow-along is a Heading 3 under the FOLLOW-ALONG Heading 2; a long-form is a
  Heading 3 "SCRIPT: ...". Each runs to the next Heading 3 or Heading 2. The outlines section is left out entirely.
- "-" lines, "N spoken words..." note lines and "RO-33." id lines are notes. A paragraph that starts with [ and ends
  with ] is a cue (it may hold several [..] cues). "HOOK TAKES (alternate openers):" is a label; the bulleted lines
  under it are alternate first lines Dan films, so they go on the prompter (after the Subscribe line, label dropped).
- An empty paragraph inside a follow-along marks where a round cue stood: one blank line on the prompter (the source
  has two), none anywhere else (Dan, 2026-10-13). A soft line break starts a new paragraph.
- Titles stay as typed (shorts in CAPS with their number). Pending suggestions are read as accepted: the count printed
  must be 0.
"""
import json, re, html, sys, os

PST = 'style="color:#000000;font-weight:normal;font-style:normal"'
BST = 'style="color:#000000;font-weight:bold;font-style:normal"'
IST = 'style="color:#000000;font-weight:normal;font-style:italic"'
BREAK = '<p><br clear="all" style="page-break-before:always"></p>'
BLANK = '<p %s><br></p>' % PST
HOOK_LABEL = 'HOOK TAKES (alternate openers):'

def load(path):
    P, pend = [], 0
    for el in json.load(open(path))['content']['tabs'][0]['documentTab']['body']['content']:
        if 'paragraph' not in el: continue
        p, acc = el['paragraph'], ''
        for r in p['elements']:
            tr = r.get('textRun', {})
            if tr.get('suggestedInsertionIds') or tr.get('suggestedDeletionIds'): pend += 1
            if not tr.get('suggestedDeletionIds'): acc += tr.get('content', '')
        P.append({'i': el['startIndex'], 'style': p.get('paragraphStyle', {}).get('namedStyleType', ''),
                  'bullet': bool(p.get('bullet')), 't': acc.rstrip('\n')})
    return P, pend

def kind(p):
    t = p['t'].strip()
    if p['bullet']: return 'HOOK'
    if t == '': return 'EMPTY'
    if t == '-': return 'SEP'
    if re.match(r'^\d+ spoken words', t): return 'NOTE'
    if re.match(r'^RO-\d+\.$', t): return 'ID'
    if t == HOOK_LABEL: return 'LABEL'
    if t.startswith('[') and t.endswith(']'): return 'CUE'
    return 'SAY'

def parse(P):
    h2 = [k for k, p in enumerate(P) if p['style'] == 'HEADING_2']
    fa_h2 = next(k for k in h2 if P[k]['t'].startswith('LONG-FORM: FOLLOW-ALONG'))
    out_h2 = next(k for k in h2 if P[k]['t'].startswith('LONG-FORM OUTLINES'))
    first_h3 = next(k for k, p in enumerate(P) if p['style'] == 'HEADING_3')
    intro = [p for p in P[1:first_h3] if p['t'].strip() not in ('', '-')]
    items = []
    for k, p in enumerate(P):
        if p['style'] != 'HEADING_3' or not p['t'].strip(): continue
        t = p['t'].strip()
        if re.match(r'^\d+\. ', t): typ = 'short'
        elif t.startswith('SCRIPT: '): typ = 'long'
        elif fa_h2 < k < out_h2: typ = 'follow'
        else: continue                                   # an outline title: not filming material
        end = next((j for j in range(k + 1, len(P)) if P[j]['style'] in ('HEADING_2', 'HEADING_3')), len(P))
        paras = []
        for q in P[k + 1:end]:
            kd = kind(q)
            if kd in ('SAY', 'HOOK', 'CUE'):
                for part in q['t'].split('\x0b'):
                    s = part.strip()
                    if s: paras.append((kd, s))
            else: paras.append((kd, q['t'].strip()))
        while paras and paras[-1][0] in ('EMPTY', 'SEP'): paras.pop()
        items.append({'type': typ, 'title': t, 'tp_title': t[len('SCRIPT: '):] if typ == 'long' else t, 'paras': paras})
    return intro, P[fa_h2]['t'], P[fa_h2 + 1]['t'].strip(), P[h2[-1]]['t'], items

def words(it): return sum(len(t.split()) for k, t in it['paras'] if k in ('SAY', 'HOOK'))

def teleprompter(lst):
    parts, seq = ['<html><head><meta charset="utf-8"></head><body>'], []
    for n, it in enumerate(lst):
        if n: parts.append(BREAK)
        parts.append('<h2>%s</h2>' % html.escape(it['tp_title'])); seq.append(it['tp_title'])
        gap, said = False, False
        for kd, t in it['paras']:
            if kd == 'EMPTY' and it['type'] == 'follow': gap = True; continue
            if kd not in ('SAY', 'HOOK'): continue
            if gap and said: parts.append(BLANK)     # one blank line where a round cue stood
            gap, said = False, True
            parts.append('<p %s>%s</p>' % (PST, html.escape(t))); seq.append(t)
    parts.append('</body></html>')
    return '\n'.join(parts), seq

def linkify(t):
    return re.sub(r'(https?://[^\s,\]]+)', lambda m: '<a href="%s">%s</a>' % (m.group(1), m.group(1)), html.escape(t))

def filming(intro, fa_h2, fa_note, lf_h2, items, broll):
    parts, seq = ['<html><head><meta charset="utf-8"></head><body>'], []
    def para(t, st=PST, blank=True):
        parts.append('<p %s>%s</p>' % (st, linkify(t))); seq.append(t)
        if blank: parts.append(BLANK)
    def head(tag, t): parts.append('<%s>%s</%s>' % (tag, html.escape(t), tag)); seq.append(t)
    def bullets(lst):
        parts.append('<ul>')
        for b in lst:
            if isinstance(b, tuple):
                parts.append('<li %s>%s<ul>%s</ul></li>' % (PST, linkify(b[0]), ''.join('<li %s>%s</li>' % (PST, linkify(c)) for c in b[1])))
                seq.append(b[0]); seq.extend(b[1])
            else: parts.append('<li %s>%s</li>' % (PST, linkify(b))); seq.append(b)
        parts.append('</ul>'); parts.append(BLANK)
    head('h1', DOC_TITLE)
    pending_b = []
    for p in intro:
        if p['bullet']: pending_b.append(p['t'].strip()); continue
        if pending_b: bullets(pending_b); pending_b = []
        para(p['t'].strip(), BST if p['t'].strip().endswith(':') else PST)
    if pending_b: bullets(pending_b)
    def script(it):
        head('h3', it['title']); hooks = []; gap = 0
        for kd, t in it['paras']:
            if kd == 'HOOK': hooks.append(t); continue
            if hooks: bullets(hooks); hooks = []
            if kd == 'EMPTY':
                if it['type'] == 'follow':
                    gap += 1
                    parts.append(BLANK)               # the source's empty paragraphs, on top of the usual blank line
                continue
            if kd == 'SEP': continue
            para(t, {'NOTE': IST, 'ID': IST, 'CUE': BST, 'LABEL': BST}.get(kd, PST))
        if hooks: bullets(hooks)
    head('h2', 'SHORT FORM: THE %d DEDICATED SHORTS' % sum(1 for it in items if it['type'] == 'short'))
    for it in items:
        if it['type'] == 'short': script(it)
    head('h2', fa_h2); para(fa_note)
    for it in items:
        if it['type'] == 'follow': script(it)
    head('h2', lf_h2)
    for it in items:
        if it['type'] == 'long': script(it)
    head('h2', 'B-ROLL SHOT LIST')
    for title, lst in broll:
        head('h3', title); bullets(lst)
    parts.append('</body></html>')
    return '\n'.join(parts), seq

def cues(t): return [c.strip() for c in re.findall(r'\[([^\]]*)\]', t)]

def shots_in(t):
    """B-roll shots in one cue paragraph. "ALL FOUR" or "EACH MACHINE" points at the on-screen text in the same line,
    so that text goes with it."""
    cs = cues(t); text = next((c.split(':', 1)[1].strip() for c in cs if c.startswith('ON SCREEN TEXT:')), None)
    out = []
    for c in cs:
        m = re.match(r'^(?:OPEN ON )?B-ROLL:\s*(.*)$', c)
        if not m: continue
        s = m.group(1)
        if text and re.match(r'^(ALL|EACH)\b', s): s = '%s (on screen: %s)' % (s, text)
        out.append(s)
    return out

def broll_list(items):
    shorts = [it for it in items if it['type'] == 'short']
    longs = [it for it in items if it['type'] == 'long']
    gym_shorts = []
    for it in shorts:
        film, shots = None, []
        for kd, t in it['paras']:
            if kd != 'CUE': continue
            for c in cues(t):
                m = re.match(r'^FILM AT THE GYM ON FRIDAY, 16:9:\s*(.*)$', c)
                if m: film = m.group(1).rstrip('.')
            for sh in shots_in(t):
                if sh not in shots: shots.append(sh)
        gym_shorts.append(('%s: %s' % (it['title'], film), shots))
    lf_shots = {}
    for it in longs:
        for kd, t in it['paras']:
            if kd != 'CUE': continue
            for sh in shots_in(t):
                ts = lf_shots.setdefault(sh, [])
                if it['tp_title'] not in ts: ts.append(it['tp_title'])
    gym_long = [('%s' % s, ['For: %s' % t for t in ts]) for s, ts in lf_shots.items()]
    cold = lambda lst: [it['tp_title'] for it in lst if any(kd == 'CUE' and c.startswith('COLD OPEN') for kd, t in it['paras'] for c in cues(t))]
    nhooks = sum(1 for it in shorts if any(kd == 'LABEL' for kd, _ in it['paras']))
    pool = ['The talking parts of all %d shorts: by the pool, shirtless, camera turned vertical like the 10/15 pool shorts. '
            '%d of them list two HOOK TAKES: film all three openers.' % (len(shorts), nhooks),
            ('Shorts that open cold on you by the pool (no B-roll before your first line):', cold(shorts)),
            'The %d long-form scripts: read by the pool, shirtless; Friday\'s gym B-roll cut in.' % len(longs),
            ('Long-forms that open cold on you by the pool:', cold(longs)),
            'The %d follow-along cue tracks: the spoken parts only. The 10/15 demo clips cover the exercises.'
            % sum(1 for it in items if it['type'] == 'follow')]
    editor = []
    for it in items:
        ps = it['paras']
        for n, (kd, t) in enumerate(ps):
            if kd != 'CUE': continue
            for c in cues(t):
                if re.match(r'^(AI |PLAY CLIP|SHOW CLIP)', c):
                    sub = ['For: %s' % it['tp_title']]
                    if c == 'AI CLIP TO ILLUSTRATE THIS':
                        nxt = next((s for k2, s in ps[n + 1:] if k2 == 'SAY'), None)
                        prv = next((s for k2, s in reversed(ps[:n]) if k2 == 'SAY'), None)
                        sub.append('Comes between "%s" and "%s"' % (prv, nxt))
                    editor.append((c, sub))
    return [('Film at the gym on Friday (16:9): the shorts', gym_shorts),
            ('Film at the gym on Friday (16:9): the long-forms (many are the same shots as the shorts)', gym_long),
            ('By the pool', pool),
            ('Editor: AI clips and outside clips', editor)]

if __name__ == '__main__':
    P, pend = load(sys.argv[1]); out_dir, prefix = sys.argv[2], sys.argv[3]; os.makedirs(out_dir, exist_ok=True)
    DOC_TITLE = '%s - Filming Document' % prefix
    print('pending suggestion runs in the source (read as accepted):', pend)
    intro, fa_h2, fa_note, lf_h2, items = parse(P)
    for it in items:
        for kd, t in it['paras']:
            if kd in ('SAY', 'HOOK') and ('[' in t or ']' in t): print('BRACKET IN SPOKEN LINE:', it['title'], t)
            if kd == 'EMPTY' and it['type'] != 'follow': pass
            if kd == 'HOOK' and it['type'] != 'short': print('BULLET OUTSIDE A SHORT:', it['title'], t)
    shorts = [it for it in items if it['type'] == 'short']
    num = lambda it: int(it['title'].split('.')[0])
    assert [num(s) for s in shorts] == list(range(1, len(shorts) + 1)), 'shorts not numbered 1..N in order'
    docs = [('%s - Teleprompter 1 - Long Form' % prefix, [it for it in items if it['type'] == 'long'] + [it for it in items if it['type'] == 'follow']),
            ('%s - Teleprompter 2 - Short Form (Part 1 of 2)' % prefix, [s for s in shorts if num(s) <= 15]),
            ('%s - Teleprompter 3 - Short Form (Part 2 of 2)' % prefix, [s for s in shorts if num(s) >= 16])]
    built = {}
    for name, lst in docs:
        h, seq = teleprompter(lst); open(os.path.join(out_dir, name + '.html'), 'w').write(h); built[name] = seq
        w = sum(words(it) for it in lst)
        print('%s: %d scripts, %d words, about %d pages' % (name, len(lst), w, round(w / 570)))
        for it in lst: print('    %5d  %s' % (words(it), it['tp_title']))
    flat = ' '.join(t for seq in built.values() for t in seq)
    print('teleprompter, must all be 0: brackets', flat.count('[') + flat.count(']'), '| http', flat.count('http'),
          '| "spoken words"', flat.count('spoken words'), '| HOOK TAKES', flat.count('HOOK TAKES'),
          '| id lines', len(re.findall(r'\bRO-\d+\.', flat)), '| "-" lines', sum(1 for s in built.values() for t in s if t == '-'))
    h, seq = filming(intro, fa_h2, fa_note, lf_h2, items, broll_list(items))
    open(os.path.join(out_dir, DOC_TITLE + '.html'), 'w').write(h); built[DOC_TITLE] = seq
    print('%s: %d lines, %d words' % (DOC_TITLE, len(seq), sum(len(t.split()) for t in seq)))
    json.dump(built, open(os.path.join(out_dir, 'built_seq.json'), 'w'), ensure_ascii=False, indent=0)
