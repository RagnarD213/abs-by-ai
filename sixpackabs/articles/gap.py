#!/usr/bin/env python3
"""Which public videos still have no article on sixpackabs.com?

  python3 sixpackabs/articles/gap.py           -> the list, plain text
  python3 sixpackabs/articles/gap.py --json    -> the same as JSON (for a routine)

Reads the public video feed (absbyai.com/api/sixpackabs/channel.json) and the live video pages
(sixpackabs.com REST, no login). A video is DONE when its live page holds an article: the notes
carry the article CTA link (utm_campaign=video-article with this video's id). A file in this
folder does not count on its own, because a file can be written and never published.

A video is a GAP when it is public, not in skips.json, and its live page has no article:
  publish         <id>.md exists here and passes for this video; it was never published
  write           long-form with no file (a TBD-*.md draft that looks like a match is named)
  needs judgment  a Short with no file: write 300 to 500 words, or add it to skips.json with a
                  reason (brag or teaser, or the same topic as a page that already has an article)
  hand-edited     the notes are neither the YouTube description nor an article: read the page
                  before replacing anything
  no page yet     the site has not imported the video (normal for about 15 minutes after release)

Exit code: 0 = no gap older than 24 hours; 1 = at least one gap older than 24 hours (this system
has failed and the count goes in the morning brief); 2 = the feed or the site could not be read.
"""
import datetime, glob, html, json, os, random, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FEED = 'https://absbyai.com/api/sixpackabs/channel.json'
PAGES = 'https://sixpackabs.com/wp-json/wp/v2/spa_video?per_page=100&page=%d&_fields=id,slug,link,content,meta&cb=%d'
LATE_HOURS = 24
STOP = set('a an and are at be by do for from how i if in is it my not of on or so the this to try '
           'what when why with you your heres here just every single way right'.split())


def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'absbyai-article-gap/1.0', 'Cache-Control': 'no-cache'})
    return json.loads(urllib.request.urlopen(req, timeout=40).read().decode('utf-8'))


def live_pages():
    pages, n = {}, 1
    while True:
        batch = get_json(PAGES % (n, random.randint(1, 10**9)))
        for p in batch:
            yt = (p.get('meta') or {}).get('_spa_youtube_id')
            if yt:
                pages[yt] = p
        if len(batch) < 100:
            return pages
        n += 1


def words(text):
    text = re.sub(r"[’']", '', html.unescape(text).lower())
    return re.findall(r'[a-z0-9]+', text)


def keys(text):
    out = set()
    for w in words(text):
        if w in STOP or len(w) < 3:
            continue
        out.add(re.sub(r'(ing|es|s)$', '', w) if len(w) > 4 else w)
    return out


def notes_are_description(rendered, description):
    """True when the page notes are still the imported YouTube description."""
    page = set(words(re.sub(r'<[^>]+>', ' ', rendered)))
    desc = [w for w in words(re.sub(r'https?://\S+', ' ', description)) if len(w) > 2]
    if not desc:
        return not page
    return sum(w in page for w in desc) / len(desc) >= 0.9


def front_matter(path):
    m = re.match(r'---\n(.*?)\n---\n', open(path, encoding='utf-8').read(), re.S)
    return dict(l.split(': ', 1) for l in m.group(1).strip().splitlines() if ': ' in l) if m else {}


def draft_candidates(title):
    """TBD-*.md drafts that look like this long-form: exact front-matter title, else filename words."""
    want, found = keys(title), []
    for path in sorted(glob.glob(os.path.join(HERE, 'TBD-*.md'))):
        name = os.path.basename(path)
        meta = front_matter(path)
        if meta.get('title') and words(meta['title']) == words(title):
            return [name]
        have = keys(name[4:-3].replace('-', ' '))
        if have and len(have & want) / len(have) >= 0.6:
            found.append((len(have & want) / len(have), len(have & want), name))
    return [n for _, _, n in sorted(found, reverse=True)]


def main():
    as_json = '--json' in sys.argv
    try:
        feed = get_json(FEED)
        pages = live_pages()
    except Exception as e:  # network or site trouble is not "zero gaps"
        print('gap.py could not read the feed or the site: %s' % e, file=sys.stderr)
        return 2
    skips = json.load(open(os.path.join(HERE, 'skips.json'), encoding='utf-8'))
    now = datetime.datetime.now(datetime.timezone.utc)

    rows, done_titles = [], {}
    for v in feed['videos']:
        vid, page = v['id'], pages.get(v['id'])
        rendered = page['content']['rendered'] if page else ''
        live = 'utm_campaign=video-article' in rendered and ('utm_content=' + vid) in rendered
        has_file = os.path.exists(os.path.join(HERE, vid + '.md'))
        age = (now - datetime.datetime.fromisoformat(v['publishedAt'].replace('Z', '+00:00'))).total_seconds() / 3600
        row = {'id': vid, 'title': v['title'], 'type': v['type'], 'age_hours': round(age, 1),
               'post_id': page['id'] if page else None, 'slug': page['slug'] if page else None,
               'url': page['link'] if page else None, 'file': vid + '.md' if has_file else None}
        if live:
            row['state'] = 'done'
            done_titles[vid] = v['title']
            if not has_file:
                row['note'] = 'live article has no file in this folder'
        elif vid in skips:
            row['state'], row['note'] = 'skip', skips[vid]
        elif not page:
            row['state'], row['action'] = 'gap', 'no page yet'
        elif has_file:
            row['state'], row['action'] = 'gap', 'publish'
        elif not notes_are_description(rendered, v['description']):
            row['state'], row['action'] = 'gap', 'hand-edited'
        elif v['type'] == 'short':
            row['state'], row['action'] = 'gap', 'needs judgment'
        else:
            row['state'], row['action'] = 'gap', 'write'
            row['drafts'] = draft_candidates(v['title'])
        rows.append(row)

    for row in rows:  # overlap hint for Shorts: an article on a page with a similar title
        if row.get('action') == 'needs judgment':
            mine = keys(row['title'])
            hits = sorted(((len(mine & keys(t)), i) for i, t in done_titles.items()), reverse=True)
            row['overlaps'] = [i for n, i in hits[:2] if n >= 2]

    gaps = [r for r in rows if r['state'] == 'gap']
    late = [r for r in gaps if r['age_hours'] > LATE_HOURS]
    summary = {'public': len(rows), 'done': sum(r['state'] == 'done' for r in rows),
               'skipped': sum(r['state'] == 'skip' for r in rows), 'gaps': len(gaps), 'late': len(late),
               'feed_stale': bool(feed.get('stale')), 'checked_at': now.strftime('%Y-%m-%dT%H:%M:%SZ')}

    if as_json:
        print(json.dumps({'summary': summary, 'gaps': gaps,
                          'notes': [r for r in rows if r['state'] == 'done' and r.get('note')]}, indent=1))
    else:
        print('%(public)d public videos: %(done)d with an article, %(skipped)d skipped on purpose, %(gaps)d gaps (%(late)d older than 24 hours)' % summary)
        if feed.get('stale'):
            print('WARNING: the video feed is serving a stale copy; a new release may be missing from this list.')
        for r in gaps:
            extra = ''
            if r.get('drafts'):
                extra = '  draft: ' + ', '.join(r['drafts'])
            if r.get('overlaps'):
                extra = '  may overlap: ' + ', '.join(r['overlaps'])
            print('GAP%s %-11s %-5s %6.1f h  %-14s post %s  %s%s' % (
                ' LATE' if r['age_hours'] > LATE_HOURS else '     ', r['id'], r['type'], r['age_hours'],
                r['action'], r['post_id'], r['title'], extra))
        for r in rows:
            if r['state'] == 'done' and r.get('note'):
                print('NOTE     %-11s %s' % (r['id'], r['note']))
    return 1 if late else 0


if __name__ == '__main__':
    sys.exit(main())
