#!/usr/bin/env python3
"""Put a revision-doc markdown file on the macOS clipboard as rich HTML, ready to cmd+v into a
Google Doc (append-a-section workflow, /revisions lesson 20).

    python3 md_to_docs_clipboard.py "revision docs/ad5-revisions-muhammad-round1-9-3-26.md"

Handles exactly the /revisions doc dialect: `## ` H2, paragraphs, 4-space-indented `- ` bullets to
any depth, `**bold**`, Dan's literal `\\*\\*HEADER\\*\\*` look inside bold, and `<https://…>` links.
The `markdown` package is NOT installed on this Mac and Google Docs wants real nested <ul>, so this
builds the tree itself. Set the clipboard IMMEDIATELY before the paste (a concurrent session can
overwrite it) and check the B button is off in the Docs toolbar before cmd+v (lesson 24).
"""
import html, re, subprocess, sys

def inline(s):
    s = html.escape(s, quote=False).replace('\\*', '\x00')
    s = re.sub(r'&lt;(https?://[^&]+)&gt;', r'<a href="\1">\1</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return s.replace('\x00', '*')

def parse(lines):
    blocks, cur = [], None
    for line in lines:
        if not line.strip():
            continue
        m = re.match(r'^(\s*)- (.*)$', line)
        if m:
            depth = len(m.group(1)) // 4
            if cur is None:
                cur = []
                blocks.append(('list', cur))
            lvl = cur
            for _ in range(depth):
                lvl = lvl[-1][1]
            lvl.append([m.group(2), []])
        else:
            cur = None
            if line.startswith('## '):
                blocks.append(('h2', line[3:]))
            else:
                blocks.append(('p', line))
    return blocks

def render_list(nodes):
    return '<ul>' + ''.join('<li>' + inline(t) + (render_list(ch) if ch else '') + '</li>'
                            for t, ch in nodes) + '</ul>'

def to_html(md):
    out = ''
    for kind, val in parse(md.split('\n')):
        out += render_list(val) if kind == 'list' else f'<{kind}>{inline(val)}</{kind}>'
    return out

if __name__ == '__main__':
    h = to_html(open(sys.argv[1]).read())
    subprocess.run(['osascript', '-e', 'set the clipboard to «data HTML%s»' % h.encode().hex()], check=True)
    print('clipboard set:', len(h), 'bytes of HTML;', h.count('<li>'), 'bullets;', h.count('<a '), 'links')
