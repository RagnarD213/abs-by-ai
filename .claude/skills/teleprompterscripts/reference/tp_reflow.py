#!/usr/bin/env python3
"""Re-flow an existing teleprompter Google Doc in place, without rebuilding it from the shoot doc.

    python3 tp_reflow.py live.json out_dir "<exact doc name>"            # from the Docs connector's read_doc
    python3 tp_reflow.py live.txt  out_dir "<exact doc name>" --titles "Title one|Title two" --no-gaps   # from a text export

Use it when the teleprompter document itself is the master (Dan edited it directly) or when only the spacing has to
change. It keeps every word and every title and writes "<doc name>.html" for the same rclone upload the builder uses
(SKILL.md, "No Chrome: upload with rclone", with --ignore-times so the existing doc is replaced and keeps its id).

Spacing rule (Dan, 2026-10-13, second ruling): NO blank line between paragraphs in a teleprompter document, to save
space on the prompter. A single blank line is taken out. Where two blank lines stood (a round cue in a follow-along
workout), one is kept. A soft line break he typed inside a paragraph (shift+enter) becomes a paragraph break.
Refuses to run on a doc with pending suggestions. Prints the word count before and after: they must match.
"""
import json, html, sys, os, re

PST = 'style="color:#000000;font-weight:normal;font-style:normal"'
BREAK = '<p><br clear="all" style="page-break-before:always"></p>'
BLANK = '<p %s><br></p>' % PST

def from_json(path):
    out = []
    for el in json.load(open(path))['content']['tabs'][0]['documentTab']['body']['content']:
        p = el.get('paragraph')
        if not p: continue
        t = ''
        for r in p['elements']:
            tr = r.get('textRun')
            if tr is None: continue
            if tr.get('suggestedInsertionIds') or tr.get('suggestedDeletionIds'):
                raise SystemExit('pending suggestion in the doc: Dan rules on them first')
            t += tr['content']
        head = p['paragraphStyle'].get('namedStyleType', '').startswith('HEADING')
        for part in t.rstrip('\n').split('\x0b') if not head else [t.strip()]:
            out.append(('H' if head else 'P', part.strip()))
    return out

def from_txt(path, titles):
    return [('H' if l.strip() in titles else 'P', l.strip()) for l in open(path, encoding='utf-8-sig').read().split('\n')]

if __name__ == '__main__':
    src, out_dir, name = sys.argv[1:4]
    titles = set(sys.argv[sys.argv.index('--titles') + 1].split('|')) if '--titles' in sys.argv else set()
    gaps = '--no-gaps' not in sys.argv     # a text export doubles every blank line, so pass --no-gaps with a .txt source
    seq = from_txt(src, titles) if src.endswith('.txt') else from_json(src)
    words_in = sum(len(t.split()) for _, t in seq)
    parts = ['<html><head><meta charset="utf-8"></head><body>']; kept = []; blanks = 0; n_h = 0
    for kind, t in seq:
        if not t: blanks += 1; continue
        if kind == 'H':
            if n_h: parts.append(BREAK)
            n_h += 1; parts.append('<h2>%s</h2>' % html.escape(t))
        else:
            if blanks >= 2 and gaps and kept and kept[-1][0] == 'P': parts.append(BLANK); kept.append(('B', ''))
            parts.append('<p %s>%s</p>' % (PST, html.escape(t)))
        kept.append((kind, t)); blanks = 0
    parts.append('</body></html>'); os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, name + '.html'), 'w').write('\n'.join(parts))
    json.dump(kept, open(os.path.join(out_dir, name + '.seq.json'), 'w'), ensure_ascii=False)
    words_out = sum(len(t.split()) for _, t in kept)
    print('%s: %d titles, %d paragraphs, %d blank lines kept, words %d -> %d %s' % (
        name, n_h, sum(1 for k, _ in kept if k == 'P'), sum(1 for k, _ in kept if k == 'B'), words_in, words_out,
        'OK' if words_in == words_out else 'MISMATCH'))
