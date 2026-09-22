#!/usr/bin/env python3
"""Turn one article file (sixpackabs/articles/<youtube-id>.md) into WordPress block markup.

Front matter (between --- lines): id, post_id, slug, excerpt. The excerpt is the page's meta
description (the theme feeds it to Yoast), so keep it under 155 characters.
Body: '## ' = H2, '### ' = H3, '- ' = bullet, '1. ' = numbered, '_text_' line = italic note,
[text](url) links, **bold**. Blank line between blocks.

  python3 build.py <file.md>            -> prints JSON {post_id, excerpt, content, words}
  python3 build.py --check <file.md>... -> word counts + the rule checks, no output file
"""
import html, json, re, sys

CTA_UTM = 'utm_source=sixpackabs&utm_medium=blog&utm_campaign=video-article&utm_content='

def parse(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', raw, re.S)
    meta = dict(l.split(': ', 1) for l in m.group(1).strip().splitlines())
    return meta, m.group(2).strip()

def inline(t, vid):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    def link(mm):
        url = mm.group(2).replace('{CTA}', 'https://try.sixpackabs.com/?' + CTA_UTM + vid)
        return '<a href="%s">%s</a>' % (html.escape(url.replace('&amp;', '&')), mm.group(1))
    return re.sub(r'\[(.+?)\]\((.+?)\)', link, t)

def blocks(body, vid):
    out = []
    for chunk in re.split(r'\n\s*\n', body):
        lines = chunk.strip().splitlines()
        if not lines:
            continue
        first = lines[0]
        if first.startswith('### '):
            out.append('<!-- wp:heading {"level":3} -->\n<h3 class="wp-block-heading">%s</h3>\n<!-- /wp:heading -->' % inline(first[4:], vid))
        elif first.startswith('## '):
            out.append('<!-- wp:heading -->\n<h2 class="wp-block-heading">%s</h2>\n<!-- /wp:heading -->' % inline(first[3:], vid))
        elif first.startswith('- ') or re.match(r'\d+\. ', first):
            ordered = not first.startswith('- ')
            items = ''.join('<!-- wp:list-item -->\n<li>%s</li>\n<!-- /wp:list-item -->' % inline(re.sub(r'^(- |\d+\. )', '', l), vid) for l in lines)
            tag = 'ol' if ordered else 'ul'
            attr = ' {"ordered":true}' if ordered else ''
            out.append('<!-- wp:list%s -->\n<%s class="wp-block-list">%s</%s>\n<!-- /wp:list -->' % (attr, tag, items, tag))
        elif first.startswith('_') and chunk.strip().endswith('_'):
            out.append('<!-- wp:paragraph -->\n<p><em>%s</em></p>\n<!-- /wp:paragraph -->' % inline(' '.join(lines).strip('_'), vid))
        else:
            out.append('<!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph -->' % inline(' '.join(lines), vid))
    return '\n\n'.join(out)

def check(path):
    meta, body = parse(path)
    raw = open(path, encoding='utf-8').read()
    words = len(re.sub(r'\[(.+?)\]\(.+?\)', r'\1', body).split())
    problems = []
    if '—' in raw: problems.append('EM DASH')
    if '–' in raw: problems.append('EN DASH')
    if len(meta['excerpt']) > 155: problems.append('excerpt %d chars' % len(meta['excerpt']))
    if body.count('{CTA}') != 1: problems.append('%d CTA links (want 1)' % body.count('{CTA}'))
    internal = len(re.findall(r'\]\(/', body)) + len(re.findall(r'\]\(https://sixpackabs\.com', body))
    if not 1 <= internal <= 3: problems.append('%d internal links' % internal)
    if re.search(r'\bmy wife\b', raw, re.I): problems.append('"my wife"')
    return meta, body, words, problems

if __name__ == '__main__':
    if sys.argv[1] == '--check':
        for p in sys.argv[2:]:
            meta, body, words, problems = check(p)
            print('%-14s %5d words  excerpt %3d  %s' % (meta['id'], words, len(meta['excerpt']), ', '.join(problems) or 'OK'))
        sys.exit(0)
    meta, body, words, problems = check(sys.argv[1])
    if problems:
        sys.exit('refusing: ' + ', '.join(problems))
    content = blocks(body.replace('](/', '](https://sixpackabs.com/'), meta['id'])
    print(json.dumps({'post_type': 'spa_video', 'id': int(meta['post_id']), 'excerpt': meta['excerpt'], 'content': content, 'words': words}))
