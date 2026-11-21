#!/usr/bin/env python3
"""Build the reaction-clips review page from a JSON file, and check it before Dan sees it.

page.py DATA.json OUT_DIR            check the data, write OUT_DIR/index.html, print the serve command
page.py DATA.json OUT_DIR --no-net   same, without asking YouTube whether each video still answers

DATA.json: see reference/data-format.md. One card per item. A clip item has id + segs (a list of [start, end]
second pairs, played in order). An idea item has no id (title, bullets, B-roll).

The checks are Dan's rules, so a failure here means the idea is not ready to show him:
  - a clip longer than 25 seconds is an ERROR; longer than 15 is listed as a warning
  - a clip card with no lesson bullet ("Lesson:" or "Do this") is an ERROR
  - an em dash or en dash anywhere is an ERROR
  - a video id that does not answer is an ERROR; one whose owner turned off embedding gets noembed set, so its
    button opens YouTube instead of showing a broken player
"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_CLIP, IDEAL_CLIP = 25, 15


def oembed(vid):
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except OSError:
        return 0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    net = "--no-net" not in sys.argv
    data_path, out = Path(args[0]), Path(args[1])
    raw = data_path.read_text()
    data = json.loads(raw)
    errors, warns = [], []
    if chr(8212) in raw or chr(8211) in raw:
        errors.append("em dash or en dash in the data")
    for key in ("title", "sub", "port", "decisions", "sections", "reply_title", "reply_help"):
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    seen = {}
    for sec in data.get("sections", []):
        for key in ("id", "heading", "label", "items"):
            if key not in sec:
                errors.append(f"section missing {key}: {sec.get('id')}")
        if sec.get("pick") and not sec.get("reply_label"):
            errors.append(f"section {sec.get('id')} has pick but no reply_label")
        for n, it in enumerate(sec.get("items", []), 1):
            where = f"{sec.get('id')} {n} ({it.get('t', '')[:40]})"
            if not it.get("id"):
                continue
            for key in ("segs", "src", "views", "words", "what", "pts"):
                if key not in it:
                    errors.append(f"{where}: missing {key}")
            total = sum(b - a for a, b in it.get("segs", []))
            if total > MAX_CLIP:
                errors.append(f"{where}: clip is {total} s, over the {MAX_CLIP} s maximum")
            elif total > IDEAL_CLIP:
                warns.append(f"{where}: clip is {total} s (ideal is {IDEAL_CLIP} or less)")
            if not any(p.startswith(("Lesson:", "Do this")) for p in it.get("pts", [])):
                errors.append(f"{where}: no lesson bullet")
            if net:
                code = seen.get(it["id"]) or oembed(it["id"])
                seen[it["id"]] = code
                if code == 401:
                    it["noembed"] = True
                    warns.append(f"{where}: owner turned off embedding, button will open YouTube")
                elif code != 200:
                    errors.append(f"{where}: video {it['id']} did not answer ({code})")
    for w in warns:
        print("warning:", w)
    if errors:
        for e in errors:
            print("ERROR:", e)
        sys.exit(1)
    tpl = (HERE / "page_template.html").read_text()
    html = tpl.replace("__TITLE__", data["title"]).replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(html)
    clips = sum(1 for s in data["sections"] for it in s["items"] if it.get("id"))
    print(f"wrote {out / 'index.html'}: {clips} clips, {len(warns)} warnings")
    print(f"serve:  python3 .claude/skills/_shared/review_server.py {data['port']} \"{out.resolve()}\"")
    print(f"give Dan:  http://127.0.0.1:{data['port']}/   (never the file path)")


if __name__ == "__main__":
    main()
