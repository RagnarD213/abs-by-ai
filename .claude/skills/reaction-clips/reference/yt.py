#!/usr/bin/env python3
"""Find a reaction clip and the exact second it starts. Needs the yt_dlp Python module (python3 -m yt_dlp).

yt.py s "query" [n]         search YouTube: id | length | views | channel | title
yt.py t ID [regex] [ctx]    the video's captions with times; with a regex, only matching lines and ctx lines around them
yt.py m ID                  one line: id | seconds | views | upload date | channel | title
yt.py c ID [ID ...]         does each video still answer? 200 plays in the page, 401 = embedding off, else gone

Captions come from YouTube's android client. YouTube answers HTTP 429 after roughly 40 caption downloads in a row
and stays that way for an hour or more; "NO TRANSCRIPT" on a video that plainly has speech means that. Use the
transcript panel in the browser instead (reference/transcript_panel.js). Search and the c check are not limited.
Downloads are cached, so asking twice costs nothing."""
import sys, os, json, re, subprocess, glob, tempfile, urllib.request, urllib.error
D = os.environ.get("REACTION_CLIPS_CACHE") or os.path.join(tempfile.gettempdir(), "reaction-clips-cache")
os.makedirs(D, exist_ok=True)
BASE = [sys.executable, "-W", "ignore", "-m", "yt_dlp", "--no-warnings"]


def mmss(s):
    s = int(s)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def search(q, n=8):
    out = subprocess.run(BASE + [f"ytsearch{n}:{q}", "--flat-playlist", "--print",
                                 "%(id)s | %(duration)s | %(view_count)s | %(channel)s | %(title)s"],
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        p = line.split(" | ")
        try:
            p[1] = mmss(float(p[1]))
            p[2] = f"{int(p[2]):,}"
        except Exception:
            pass
        print(" | ".join(p))


def fetch(vid):
    f = glob.glob(os.path.join(D, vid + ".*.json3"))
    if not f:
        subprocess.run(BASE + ["--skip-download", "--ignore-no-formats-error", "--write-auto-subs", "--write-subs",
                               "--sub-langs", "en,en-US,en-GB,en-orig", "--sub-format", "json3",
                               "--extractor-args", "youtube:player_client=android",
                               "-o", os.path.join(D, "%(id)s"), "https://www.youtube.com/watch?v=" + vid],
                       capture_output=True, text=True)
        f = glob.glob(os.path.join(D, vid + ".*.json3"))
    if not f:
        return None
    f.sort(key=lambda p: ("orig" in p, len(p)))
    ev = json.load(open(f[0])).get("events", [])
    lines = []
    for e in ev:
        txt = "".join(s.get("utf8", "") for s in e.get("segs", []) or []).replace("\n", " ").strip()
        if txt:
            lines.append((e.get("tStartMs", 0) / 1000, txt))
    return lines


def transcript(vid, rx=None, ctx=2):
    lines = fetch(vid)
    if lines is None:
        print("NO TRANSCRIPT", vid)
        return
    if not rx:
        for t, x in lines:
            print(f"{mmss(t)} {x}")
        return
    r = re.compile(rx, re.I)
    show = set()
    for i, (t, x) in enumerate(lines):
        if r.search(x):
            show.update(range(max(0, i - ctx), min(len(lines), i + ctx + 1)))
    last = -2
    for i in sorted(show):
        if i != last + 1:
            print("--")
        print(f"{mmss(lines[i][0])} {lines[i][1]}")
        last = i


def meta(vid):
    out = subprocess.run(BASE + ["--skip-download", "--ignore-no-formats-error",
                                 "--extractor-args", "youtube:player_client=android", "--print",
                                 "%(id)s | %(duration)s | %(view_count)s | %(upload_date)s | %(channel)s | %(title)s",
                                 "https://www.youtube.com/watch?v=" + vid], capture_output=True, text=True).stdout
    print(out.strip())


def check(ids):
    for vid in ids:
        url = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=" + vid + "&format=json"
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                print(vid, r.status, json.load(r).get("title", ""))
        except urllib.error.HTTPError as e:
            print(vid, e.code, "embedding off: link out to YouTube" if e.code == 401 else "does not answer")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "c":
        check(a[1:])
    elif a[0] == "s":
        search(a[1], int(a[2]) if len(a) > 2 else 8)
    elif a[0] == "t":
        transcript(a[1], a[2] if len(a) > 2 else None, int(a[3]) if len(a) > 3 else 2)
    elif a[0] == "m":
        meta(a[1])
