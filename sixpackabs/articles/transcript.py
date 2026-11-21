#!/usr/bin/env python3
"""Print the spoken words of one PUBLIC YouTube video, for writing its article.

  python3 sixpackabs/articles/transcript.py <youtube-id>

Gemini watches the public YouTube URL (the YouTube OAuth token has no captions scope, so this is
the way to get the words when no .srt or .transcript.json sits next to the final). Prefer the
local file when there is one: it is free and exact. Cost here is a few cents per video.
The key comes from ~/.absbyai-secrets.env (GEMINI_API_KEY) or the environment; it is never printed.
"""
import json, os, re, sys, urllib.error, urllib.request

MODEL = 'gemini-flash-latest'
PROMPT = ('Transcribe every word spoken in this video, word for word, in order. Plain text, short '
          'paragraphs, no timestamps, no speaker labels, no summary. After the transcript add a '
          'section headed ON SCREEN listing any text, numbers, exercise names, sets and reps shown '
          'on screen that are not spoken, and whether any AI-generated image or clip appears.')


def api_key():
    if os.environ.get('GEMINI_API_KEY'):
        return os.environ['GEMINI_API_KEY']
    for line in open(os.path.expanduser('~/.absbyai-secrets.env'), encoding='utf-8'):
        if line.startswith('GEMINI_API_KEY='):
            return line.split('=', 1)[1].strip().strip('"\'')
    sys.exit('GEMINI_API_KEY not found')


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r'[A-Za-z0-9_-]{11}', sys.argv[1]):
        sys.exit(__doc__)
    body = {'contents': [{'parts': [
        {'file_data': {'file_uri': 'https://www.youtube.com/watch?v=' + sys.argv[1]}},
        {'text': PROMPT}]}]}
    req = urllib.request.Request(
        'https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent' % MODEL,
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'x-goog-api-key': api_key()})
    try:
        out = json.loads(urllib.request.urlopen(req, timeout=600).read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        sys.exit('Gemini error %d: %s' % (e.code, e.read().decode('utf-8', 'replace')[:300]))
    parts = (out.get('candidates') or [{}])[0].get('content', {}).get('parts', [])
    text = ''.join(p.get('text', '') for p in parts).strip()
    if not text:
        sys.exit('Gemini returned no transcript: %s' % json.dumps(out)[:300])
    print(text)
    usage = out.get('usageMetadata', {})
    print('tokens in %s, out %s' % (usage.get('promptTokenCount'), usage.get('candidatesTokenCount')), file=sys.stderr)


if __name__ == '__main__':
    main()
