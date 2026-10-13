#!/usr/bin/env python3
"""Build teleprompter-only Google Docs from a shoot doc, one per filming set (used 2026-10-11, 10/17 shoot).

    python3 tp_from_shoot_doc.py doc.json out_dir "10-17 Shoot"

doc.json is the saved output of the Docs connector's read_doc on the shoot doc (the source is only ever read).
Writes one HTML file per set into out_dir, named "<prefix> - Teleprompter N - <Set>.html", plus built_seq.json for
the check afterwards. Upload and verify: SKILL.md, "No Chrome: upload with rclone".

How it reads the shoot doc (the 10/17 format):
- A script starts at the paragraph just before a line that begins "Filming script" or "Teleprompter script".
- It ends at the next script, the first bulleted paragraph (the next outline), an outline title (a plain line followed
  by a bullet), or a section heading (LONG FORM..., SHORT FORM..., B-ROLL SHOT LIST).
- A paragraph that starts with [ and ends with ] is a cue and is dropped. So is the "Filming script..." note line.
  Everything else is spoken. A soft line break inside a paragraph (shift+enter) starts a new teleprompter paragraph.
- No blank line between spoken paragraphs (Dan, 2026-10-13, his second ruling that day: it saves space on the
  prompter). This replaces the blank line after every paragraph that was added that morning.
- Pending suggestions are read as accepted. Check there are none before building (the script prints the count).

SETS decides which doc a script goes in, by the start of its title. Edit it for each shoot; anything not matched goes
to the first set. A set longer than MAX_WORDS (about 45 pages) is split into parts at a script boundary, because Dan
wants no teleprompter script over 50 pages. Count the real pages after upload (SKILL.md) all the same. In a follow-along workout a blank line is left wherever a [ROUND ...] cue stood, so the rest
scripts stay apart without adding a word.
"""
import json, re, html, sys, os

SETS = [  # (label for the file name, title prefixes that go here, blank line at round cues?)
    ("Dark Green Backdrop", (), False),                       # the default: everything not matched below
    ("Green Screen", ("Reacting To", "A Doctor Says", "Clavicular", "What Every Body Fat Percentage",
                      "I Ranked Every Ab Exercise", "How Losing Fat Changed My Face",
                      # the 15 reaction shorts locked 2026-10-12
                      "Cristiano Ronaldo Sells", "Surgeons Now Carve", "Women Say They Love The Dad Bod", "Bill Maher",
                      "Dr. Mike Says", "TikTok Says Blended Oats", "He Hired ChatGPT", "There's Now A Card",
                      "Bert Kreischer", "Kevin James", "Post Malone", "Terry Crews", "Alex Hormozi", "Mr. Olympia Shows"), False),
    ("Outside By The Pool", ("The 5-Minute No-Equipment Workout", "10-Minute Jump Rope", "20-Minute Jump Rope",
                             "15-Minute Jump Rope",
                             # the 11 outdoor shirtless shorts locked 2026-10-12
                             "How To Do Towel Rows", "How To Do Reverse Lunges", "How To Do Bodyweight Squats",
                             "How To Do Goblet Squats", "How To Do Overhead Tricep Extensions", "3 Rules For Every Rep",
                             "Why I Only Do 3 Sets", "Why Cables Beat Dumbbells", "Why I Do A Total Body Workout",
                             "Why I Work Out First Thing", "Why You Must Train Your Abs"), True),
]
MAX_WORDS = 25000   # Dan, 2026-10-11: at most 50 pages per teleprompter script. With no blank lines a Google Doc of these runs
                    # about 570 words a page (12,615 words = 22 pages, 2026-10-13), so 25,000 words is about 44. A longer set is split in two.
SEC = re.compile(r'^(LONG FORM|SHORT FORM|B-ROLL SHOT LIST)')
GAP = re.compile(r'\[(ROUND|CIRCUIT|TIMER ENDS|NO TALKING)')
PST = 'style="color:#000000;font-weight:normal;font-style:normal"'
BREAK = '<p><br clear="all" style="page-break-before:always"></p>'
BLANK = '<p %s><br></p>' % PST   # an empty paragraph: only used where a round cue stood in a follow-along workout

def load(path):
    P, pend = [], 0
    for el in json.load(open(path))['content']['tabs'][0]['documentTab']['body']['content']:
        if 'paragraph' not in el: continue
        acc, has = '', False
        for r in el['paragraph']['elements']:
            tr = r.get('textRun', {})
            if tr.get('suggestedInsertionIds') or tr.get('suggestedDeletionIds'): pend += 1
            if not tr.get('suggestedDeletionIds'): acc += tr.get('content', ''); has = True
        if has: P.append({'t': acc.rstrip('\n').replace('\x0b', '\n'), 'bullet': bool(el['paragraph'].get('bullet'))})
    return P, pend

def scripts(P):
    nb = [k for k, p in enumerate(P) if p['t'].strip()]
    titles = [a for a, b in zip(nb, nb[1:]) if P[b]['t'].startswith(('Filming script ', 'Filming script.', 'Filming script,', 'Teleprompter script'))
              and not P[a]['bullet'] and not SEC.match(P[a]['t'].strip())]
    out = []
    for n, k in enumerate(titles):
        end = titles[n + 1] if n + 1 < len(titles) else len(P); paras = []; j = k + 1
        while j < end:
            t = P[j]['t']
            if P[j]['bullet'] or SEC.match(t.strip()): break
            nxt = next((q for q in range(j + 1, min(end, j + 4)) if P[q]['t'].strip()), None)
            if t.strip() and nxt is not None and P[nxt]['bullet'] and not t.strip().startswith('['): break
            for part in t.split('\n'):
                s = part.strip()
                if not s or s.startswith(('Filming script', 'Teleprompter script')): continue
                paras.append(('CUE' if s.startswith('[') and s.endswith(']') else 'SAY', s))
            j += 1
        out.append({'title': re.sub(r'^(FILMING )?SCRIPT:\s*', '', P[k]['t'].strip()), 'paras': paras})
    return out

if __name__ == '__main__':
    P, pend = load(sys.argv[1]); out_dir, prefix = sys.argv[2], sys.argv[3]; os.makedirs(out_dir, exist_ok=True)
    print('pending suggestion runs in the source (read as accepted):', pend)
    S = scripts(P); groups = [[] for _ in SETS]
    for s in S:
        g = next((i for i, (_, pre, _) in enumerate(SETS) if pre and s['title'].startswith(pre)), 0); groups[g].append(s)
    built = {}; docs = []
    for i, ((label, _, gaps), lst) in enumerate(zip(SETS, groups)):
        wc = lambda s: sum(len(t.split()) for k, t in s['paras'] if k == 'SAY')
        total = sum(wc(s) for s in lst); nparts = max(1, -(-total // MAX_WORDS)); parts_, cur, run = [], [], 0
        for s in lst:                                   # split at script boundaries, parts about equal
            if cur and len(parts_) < nparts - 1 and run + wc(s) / 2 > total / nparts: parts_.append(cur); cur, run = [], 0
            cur.append(s); run += wc(s)
        parts_.append(cur)
        for n, part in enumerate(parts_):
            docs.append(('%s - Teleprompter %d - %s%s' % (prefix, i + 1, label, ' (Part %d of %d)' % (n + 1, len(parts_)) if len(parts_) > 1 else ''), gaps, part))
    for name, gaps, lst in docs:
        seq = []
        parts = ['<html><head><meta charset="utf-8"></head><body>']
        for n, s in enumerate(lst):
            if n: parts.append(BREAK)
            parts.append('<h2>%s</h2>' % html.escape(s['title'])); seq.append(s['title']); gap = False; first = True
            for kind, t in s['paras']:
                if kind == 'CUE':
                    gap = gap or (gaps and bool(GAP.match(t))); continue
                if gap and not first: parts.append(BLANK)  # one blank line where a round cue stood; none anywhere else (Dan, 2026-10-13)
                gap = False; first = False
                parts.append('<p %s>%s</p>' % (PST, html.escape(t))); seq.append(t)
        parts.append('</body></html>'); open(os.path.join(out_dir, name + '.html'), 'w').write('\n'.join(parts)); built[name] = seq
        words = sum(len(t.split()) for s in lst for k, t in s['paras'] if k == 'SAY')
        print('%s: %d scripts, %d words, about %d pages' % (name, len(lst), words, round(words / 565)))
        for s in lst: print('    ', s['title'])
    json.dump(built, open(os.path.join(out_dir, 'built_seq.json'), 'w'), ensure_ascii=False)
    flat = ' '.join(t for seq in built.values() for t in seq)
    print('must all be 0: brackets', flat.count('[') + flat.count(']'), '| http', flat.count('http'), '| "spoken words"', flat.count('spoken words'))
