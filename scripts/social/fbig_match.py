#!/usr/bin/env python3
"""
Facebook followers -> Instagram follow-back candidates (Dan, 2026-10-22).

Dan's personal Facebook profile (facebook.com/danroseninja, ~2.8K followers) cannot be an ad
audience, so instead a daily routine finds which of those followers have an Instagram account,
and Dan reviews 5 a morning and decides himself whether to follow them from @danrosefit.
Claude never follows, likes or messages anyone. Runbook: Docs/FB_IG_FOLLOW_MATCH.md.

The ledger holds other people's names and profile links, so it lives OUTSIDE the repo:
~/.absbyai-fbig/ledger.json. Commands:

  fbig_match.py load <followers.json>   # add [{u, n}] scraped from the followers page (new ones only)
  fbig_match.py next [N]                # the next N unchecked followers, oldest-loaded first
  fbig_match.py record '<json>'         # one result: {u, result, ig?, igName?, why?, confidence?}
                                        #   result: match | no_account | unsure | already_following | skip
  fbig_match.py review                  # build today's review page from today's matches, print its path
  fbig_match.py stats                   # counts by result
"""
import datetime as dt
import html
import json
import os
import sys

HOME = os.path.expanduser("~/.absbyai-fbig")
LEDGER = os.path.join(HOME, "ledger.json")
RESULTS = {"match", "no_account", "unsure", "already_following", "skip"}


def today():
    return dt.datetime.now().strftime("%Y-%m-%d")


def load_ledger():
    if not os.path.exists(LEDGER):
        return {"followers": [], "results": {}}
    with open(LEDGER) as f:
        return json.load(f)


def save_ledger(led):
    os.makedirs(HOME, mode=0o700, exist_ok=True)
    tmp = LEDGER + ".tmp"
    with open(tmp, "w") as f:
        json.dump(led, f, indent=1, ensure_ascii=False)
    os.replace(tmp, LEDGER)
    os.chmod(LEDGER, 0o600)


def cmd_load(path):
    led = load_ledger()
    known = {x["u"] for x in led["followers"]}
    rows = json.load(open(path))
    added = 0
    for r in rows:
        if r.get("u") and r["u"] not in known:
            led["followers"].append({"u": r["u"], "n": r.get("n", ""), "loaded": today()})
            known.add(r["u"])
            added += 1
    save_ledger(led)
    print("added %d new followers (%d in the list)" % (added, len(led["followers"])))


def cmd_next(n=20):
    led = load_ledger()
    todo = [x for x in led["followers"] if x["u"] not in led["results"]]
    print(json.dumps(todo[:int(n)], ensure_ascii=False, indent=1))


def cmd_record(raw):
    r = json.loads(raw)
    if r.get("result") not in RESULTS:
        sys.exit("result must be one of %s" % sorted(RESULTS))
    led = load_ledger()
    if r["u"] not in {x["u"] for x in led["followers"]}:
        sys.exit("unknown follower %s (load the followers list first)" % r["u"])
    r["day"] = today()
    led["results"][r["u"]] = r
    save_ledger(led)
    print("recorded %s: %s" % (r["u"], r["result"]))


def cmd_review():
    led = load_ledger()
    names = {x["u"]: x["n"] for x in led["followers"]}
    rows = [r for r in led["results"].values() if r["result"] == "match" and r["day"] == today()]
    cards = []
    for i, r in enumerate(rows, 1):
        ig = r["ig"].lstrip("@")
        cards.append(
            '<li><div class="n">%d</div><div class="b"><div class="who">%s</div>'
            '<div class="links"><a href="%s" target="_blank">Facebook</a>'
            '<a class="ig" href="https://www.instagram.com/%s/" target="_blank">@%s</a></div>'
            '<div class="why">%s</div><div class="conf">%s</div></div></li>' % (
                i, html.escape(names.get(r["u"], "")), html.escape(r["u"]), html.escape(ig), html.escape(ig),
                html.escape(r.get("why", "")), html.escape(r.get("confidence", ""))))
    done = sum(1 for r in led["results"].values())
    page = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Follow-back review</title><style>
:root{--bg:#f6f8fb;--card:#fff;--ink:#14202e;--mute:#5b6b7d;--acc:#2f6fd6;--line:#e1e7ef}
@media (prefers-color-scheme:dark){:root{--bg:#10151c;--card:#18202a;--ink:#e8eef5;--mute:#9aabbd;--acc:#7aa7ff;--line:#2a3542}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.45 -apple-system,system-ui,sans-serif}
main{max-width:720px;margin:0 auto;padding:24px 16px}h1{font-size:22px;margin:0 0 4px}p{color:var(--mute);margin:0 0 20px}
ol{list-style:none;padding:0;margin:0;display:grid;gap:12px}li{display:flex;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.n{font-weight:700;color:var(--acc);min-width:18px}.who{font-weight:600;font-size:17px}.links{display:flex;gap:14px;margin:4px 0 6px}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}.why{font-size:14px}.conf{font-size:13px;color:var(--mute);margin-top:4px}
</style></head><body><main><h1>Follow-back review, %s</h1>
<p>%d possible matches between your Facebook followers and Instagram. Each Instagram profile is open in its own tab. Confirm it is the same person, then follow from @danrosefit if you want to. %d of %d followers checked so far.</p>
<ol>%s</ol></main></body></html>""" % (today(), len(rows), done, len(led["followers"]), "".join(cards) or "<li>No matches today.</li>")
    out = os.path.join(HOME, "review-%s.html" % today())
    with open(out, "w") as f:
        f.write(page)
    print(out)


def cmd_stats():
    led = load_ledger()
    counts = {}
    for r in led["results"].values():
        counts[r["result"]] = counts.get(r["result"], 0) + 1
    print(json.dumps({"followers": len(led["followers"]), "checked": len(led["results"]),
                      "left": len(led["followers"]) - len(led["results"]), **counts}))


if __name__ == "__main__":
    a = sys.argv[1:] or ["stats"]
    {"load": lambda: cmd_load(a[1]), "next": lambda: cmd_next(*a[1:2]), "record": lambda: cmd_record(a[1]),
     "review": cmd_review, "stats": cmd_stats}[a[0]]()
