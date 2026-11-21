#!/usr/bin/env python3
"""Check published articles on the live site: python3 verify.py <file.md>...

For each article: the page answers 200, the notes hold the article (word count within 10%), the
meta description equals the excerpt, the CTA link carries this video's utm_content, the player
points at this video, and the notes contain no em or en dash.
"""
import html, random, re, sys, urllib.request
sys.path.insert(0, __import__('os').path.dirname(__file__))
from build import check

ok_all = True
for path in sys.argv[1:]:
    meta, body, words, _ = check(path)
    url = 'https://sixpackabs.com/videos/%s/?v=%d' % (meta['slug'], random.randint(1, 10**9))
    page = urllib.request.urlopen(url).read().decode('utf-8')
    i = page.find('spa-notes')
    notes = page[i:page.find('spa-subcta', i)]
    live_words = len(html.unescape(re.sub(r'<[^>]+>', ' ', notes)).split()) - 2
    desc = re.search(r'<meta name="description" content="([^"]*)"', page)
    desc = html.unescape(desc.group(1)) if desc else None
    checks = {
        'article': abs(live_words - words) <= max(15, words * 0.1),
        'meta': desc == meta['excerpt'],
        'cta': ('utm_content=' + meta['id']) in notes,
        'player': meta['id'] in page[:i],
        'no dash': '\u2014' not in notes and '\u2013' not in notes,
    }
    bad = [k for k, v in checks.items() if not v]
    ok_all &= not bad
    print('%-14s %-5s live %4d / file %4d words  %s' % (meta['id'], 'OK' if not bad else 'FAIL', live_words, words, ', '.join(bad)))
sys.exit(0 if ok_all else 1)
