#!/usr/bin/env python3
"""Client ledger: every instruction a client gives, tracked until the finished film passes it.

Why this exists (Joint Vigor, 2026-11-19): the client's written feedback on the trial lead lived only in his
Google Doc and an Upwork reply. Four handoffs later it was gone from every brief, the old lead was labelled
"approved by" the client, six independent reviews checked the film against our own plan, and the full film
shipped without his notes. Prose rules did not stop that. This tool makes it a gate that exits non-zero.

The ledger is `<job>/CLIENT-LEDGER.json` in the PRIVATE client job folder. No client data lives in this file.

  init     JOB --client NAME
  source   JOB --kind brief|doc|message|picks|ours --date YYYY-MM-DD --ref URL_OR_ID --copy FILE [--title T]
  recheck  JOB SID NEWCOPY          a client doc was fetched again: has it changed since we itemized it?
  add      JOB --source SID --type note|rule|promise|approval|question --where W --quote "verbatim words"
  itemized JOB SID                  every instruction in this source now has an item
  done     JOB ID --at T --evidence FILE [--fix TEXT]
  waive    JOB ID --source SID --client-words "verbatim"     only the client's own words can drop an item
  supersede JOB ID --by ID2
  review   JOB ID --result pass|fail --at T --by NAME        the independent reviewer's verdict
  sweep    JOB --through REF --client-messages N              the whole thread was read to its newest message
  lint     JOB FILE...              "approved by <client>" claims must cite an approval item, e.g. [L12]
  gate     JOB --stage plan|build|review|deliver [--brief FILE ...] [--max-age-hours 24]
  report   JOB --for dan|reviewer|client
"""
import argparse, datetime, hashlib, json, os, re, sys

TYPES = ("note", "rule", "promise", "approval", "question")
KINDS = ("brief", "doc", "message", "picks", "ours")


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def lpath(job):
    return os.path.join(job, "CLIENT-LEDGER.json")


def load(job):
    p = lpath(job)
    if not os.path.exists(p):
        sys.exit(f"NO LEDGER: {p} does not exist. Run: client_ledger.py init JOB --client NAME")
    return json.load(open(p))


def save(job, L):
    tmp = lpath(job) + ".tmp"
    json.dump(L, open(tmp, "w"), indent=1, ensure_ascii=False)
    os.replace(tmp, lpath(job))


def src(L, sid):
    for s in L["sources"]:
        if s["id"] == sid:
            return s
    sys.exit(f"unknown source {sid}")


def item(L, iid):
    for i in L["items"]:
        if i["id"] == iid:
            return i
    sys.exit(f"unknown item {iid}")


def copy_abs(job, s):
    return os.path.join(job, s["copy"])


def quote_in(job, s, quote):
    return norm(quote) in norm(open(copy_abs(job, s), encoding="utf-8", errors="replace").read())


def cmd_init(a):
    if os.path.exists(lpath(a.job)):
        sys.exit("ledger already exists")
    save(a.job, {"client": a.client, "sources": [], "items": [], "sweeps": []})
    print("ledger created:", lpath(a.job))


def cmd_source(a):
    L = load(a.job)
    cp = os.path.abspath(a.copy)
    if not os.path.isfile(cp) or not cp.startswith(os.path.abspath(a.job) + os.sep):
        sys.exit("--copy must be a word-for-word text copy saved inside the job folder")
    sid = f"S{len(L['sources']) + 1}"
    L["sources"].append({"id": sid, "kind": a.kind, "date": a.date, "ref": a.ref, "title": a.title or "",
                         "copy": os.path.relpath(cp, a.job), "sha256": sha(cp), "itemized": False,
                         "added": now().isoformat()})
    save(a.job, L)
    print(sid, "registered. Now add one item per instruction in it, then: itemized JOB", sid)


def cmd_recheck(a):
    L = load(a.job)
    s = src(L, a.sid)
    new = sha(a.newcopy)
    if new == s["sha256"]:
        s["rechecked"] = now().isoformat()
        save(a.job, L)
        print(a.sid, "unchanged")
        return
    old = set(norm(x) for x in open(copy_abs(a.job, s), encoding="utf-8", errors="replace").read().splitlines())
    added = [x for x in open(a.newcopy, encoding="utf-8", errors="replace").read().splitlines()
             if x.strip() and norm(x) not in old]
    os.replace(a.newcopy, copy_abs(a.job, s))
    s.update(sha256=new, itemized=False, rechecked=now().isoformat())
    save(a.job, L)
    print(f"CLIENT CHANGED {a.sid} since we itemized it. {len(added)} new or changed lines:")
    for x in added:
        print("  +", x.strip()[:200])
    print("Add an item for each new instruction, then: itemized JOB", a.sid)
    sys.exit(2)


def cmd_add(a):
    L = load(a.job)
    s = src(L, a.source)
    if a.type in ("note", "rule", "approval", "question") and s["kind"] == "ours":
        sys.exit("a note, rule, approval or question must come from the CLIENT's own source, not ours")
    if a.type == "promise" and s["kind"] != "ours":
        sys.exit("a promise is something WE wrote: register our sent message with --kind ours")
    if not quote_in(a.job, s, a.quote):
        sys.exit(f"QUOTE NOT FOUND in {a.source}. Items carry the source's exact words, never a paraphrase.")
    iid = f"L{len(L['items']) + 1}"
    L["items"].append({"id": iid, "source": a.source, "type": a.type, "where": a.where, "quote": a.quote.strip(),
                       "status": "open"})
    save(a.job, L)
    print(iid, "added")


def cmd_itemized(a):
    L = load(a.job)
    s = src(L, a.sid)
    if not any(i["source"] == a.sid for i in L["items"]) and not a.empty:
        sys.exit("no items cite this source. If it truly holds no instruction, pass --empty")
    s["itemized"] = True
    save(a.job, L)
    print(a.sid, "marked fully itemized")


def cmd_done(a):
    L = load(a.job)
    i = item(L, a.id)
    if not os.path.isfile(a.evidence):
        sys.exit("--evidence must be a real file (a frame or clip pulled from the finished master)")
    i.update(status="done", film_time=a.at, evidence=os.path.abspath(a.evidence), fix=a.fix or "")
    i.pop("review", None)
    save(a.job, L)
    print(a.id, "done at", a.at, "(reviewer verdict cleared; it must be re-verified)")


def cmd_waive(a):
    L = load(a.job)
    i = item(L, a.id)
    s = src(L, a.source)
    if s["kind"] == "ours":
        sys.exit("only the client's own written words can waive an item")
    if not quote_in(a.job, s, a.client_words):
        sys.exit("CLIENT WORDS NOT FOUND in that source. Dan's approval or our judgement cannot waive a client item.")
    i.update(status="waived", waived_by=a.source, client_words=a.client_words.strip())
    save(a.job, L)
    print(a.id, "waived by the client's own words")


def cmd_supersede(a):
    L = load(a.job)
    i, j = item(L, a.id), item(L, a.by)
    if src(L, j["source"])["date"] < src(L, i["source"])["date"]:
        sys.exit("the superseding item must come from a later source")
    i.update(status="superseded", superseded_by=a.by)
    save(a.job, L)
    print(a.id, "superseded by", a.by)


def cmd_review(a):
    L = load(a.job)
    i = item(L, a.id)
    i["review"] = {"result": a.result, "at": a.at, "by": a.by, "when": now().isoformat()}
    save(a.job, L)
    print(a.id, "review:", a.result)


def cmd_sweep(a):
    L = load(a.job)
    L["sweeps"].append({"when": now().isoformat(), "through": a.through, "client_messages": a.client_messages})
    save(a.job, L)
    print("sweep recorded")


CLAIM = re.compile(r"(?i)\b(approved by|approved these|approved this|client[- ]approved|signed off)\b")


def lint_files(L, files):
    bad = []
    approvals = {i["id"] for i in L["items"] if i["type"] == "approval"}
    who = re.compile(r"(?i)\b(%s|client)\b" % re.escape(L["client"]))
    for f in files:
        for n, line in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
            if CLAIM.search(line) and who.search(line):
                cited = set(re.findall(r"\[(L\d+)\]", line))
                if not cited or not cited <= approvals:
                    bad.append(f"{f}:{n}: claims client approval without citing an approval item: {line.strip()[:140]}")
    return bad


def cmd_lint(a):
    bad = lint_files(load(a.job), a.files)
    print("\n".join(bad) if bad else "lint clean")
    sys.exit(1 if bad else 0)


def cmd_gate(a):
    L = load(a.job)
    fail = []
    if not L["sources"]:
        fail.append("no client source registered (brief, feedback docs, every client message with an instruction)")
    for s in L["sources"]:
        p = copy_abs(a.job, s)
        if not os.path.isfile(p):
            fail.append(f"{s['id']}: word-for-word copy missing ({s['copy']})")
        elif sha(p) != s["sha256"]:
            fail.append(f"{s['id']}: copy edited after registration; use recheck")
        if not s["itemized"]:
            fail.append(f"{s['id']} ({s['title'] or s['ref']}): not fully itemized")
    last = L["sweeps"][-1] if L["sweeps"] else None
    if not last:
        fail.append("the client thread has never been swept (read to its newest message, linked docs fetched again)")
    else:
        age = (now() - datetime.datetime.fromisoformat(last["when"])).total_seconds() / 3600
        if age > a.max_age_hours:
            fail.append(f"last thread sweep was {age:.0f} h ago (limit {a.max_age_hours} h): sweep again")
    live = [i for i in L["items"] if i["status"] != "superseded"]
    if a.stage == "build":
        if not a.brief:
            fail.append("build stage needs --brief FILE for every brief the builders read")
        else:
            text = "\n".join(open(f, encoding="utf-8", errors="replace").read() for f in a.brief)
            for i in live:
                if i["status"] == "open" and i["type"] in ("note", "rule", "promise") \
                        and not re.search(r"\b%s\b" % i["id"], text):
                    fail.append(f"{i['id']} is not carried in any brief: {i['quote'][:90]}")
            fail += lint_files(L, a.brief)
    if a.stage in ("review", "deliver"):
        for i in live:
            if i["type"] == "approval":
                continue
            if i["status"] == "open":
                fail.append(f"{i['id']} OPEN ({i['where']}): {i['quote'][:90]}")
            elif i["status"] == "done" and not (i.get("film_time") and os.path.isfile(i.get("evidence", ""))):
                fail.append(f"{i['id']} marked done without a film time and an existing evidence frame")
    if a.stage == "deliver":
        for i in live:
            if i["status"] == "done" and i.get("review", {}).get("result") != "pass":
                fail.append(f"{i['id']} has no PASS from the independent reviewer ({i['where']})")
    if fail:
        print(f"CLIENT LEDGER GATE FAILED ({a.stage}), {len(fail)} problem(s):")
        for f in fail:
            print("  -", f)
        sys.exit(1)
    print(f"CLIENT LEDGER GATE PASSED ({a.stage}): {len(live)} live items, {len(L['sources'])} sources")


def cmd_report(a):
    L = load(a.job)
    rows = [i for i in L["items"] if i["status"] != "superseded"]
    S = {s["id"]: s for s in L["sources"]}
    if a.to == "reviewer":
        print(f"# What {L['client']} asked for, in his own words. Mark every row PASS or FAIL with a film time.\n")
        print("| # | Source | Where | His words | Our claimed film time |\n|---|---|---|---|---|")
        for i in rows:
            if i["type"] != "approval":
                print(f"| {i['id']} | {S[i['source']]['title'] or i['source']} ({S[i['source']]['date']}) | "
                      f"{i['where']} | {i['quote']} | {i.get('film_time', '')} |")
    elif a.to == "client":
        print("Your notes, one by one:\n")
        for n, i in enumerate([r for r in rows if r["type"] in ("note", "rule")], 1):
            what = i.get("fix") or ("kept as you asked" if i["status"] == "waived" else "NOT DONE")
            print(f"{n}. {i['where']}: {what}" + (f" (now at {i['film_time']})" if i.get("film_time") else ""))
    else:
        print(f"# Client ledger: {L['client']}\n")
        print("| # | Type | Source | Where | Words | Status | Film time | Reviewer |\n|---|---|---|---|---|---|---|---|")
        for i in rows:
            print(f"| {i['id']} | {i['type']} | {i['source']} {S[i['source']]['date']} | {i['where']} | "
                  f"{i['quote'][:120]} | {i['status'].upper()} | {i.get('film_time', '')} | "
                  f"{i.get('review', {}).get('result', '')} |")
        n_open = sum(1 for i in rows if i["status"] == "open")
        print(f"\n{n_open} open of {len(rows)}.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)

    def c(name, fn, *args):
        q = sp.add_parser(name)
        q.add_argument("job")
        for names, kw in args:
            q.add_argument(*names, **kw)
        q.set_defaults(fn=fn)

    c("init", cmd_init, (["--client"], dict(required=True)))
    c("source", cmd_source, (["--kind"], dict(required=True, choices=KINDS)), (["--date"], dict(required=True)),
      (["--ref"], dict(required=True)), (["--copy"], dict(required=True)), (["--title"], {}))
    c("recheck", cmd_recheck, (["sid"], {}), (["newcopy"], {}))
    c("add", cmd_add, (["--source"], dict(required=True)), (["--type"], dict(required=True, choices=TYPES)),
      (["--where"], dict(required=True)), (["--quote"], dict(required=True)))
    c("itemized", cmd_itemized, (["sid"], {}), (["--empty"], dict(action="store_true")))
    c("done", cmd_done, (["id"], {}), (["--at"], dict(required=True)), (["--evidence"], dict(required=True)),
      (["--fix"], {}))
    c("waive", cmd_waive, (["id"], {}), (["--source"], dict(required=True)),
      (["--client-words"], dict(required=True)))
    c("supersede", cmd_supersede, (["id"], {}), (["--by"], dict(required=True)))
    c("review", cmd_review, (["id"], {}), (["--result"], dict(required=True, choices=("pass", "fail"))),
      (["--at"], dict(required=True)), (["--by"], dict(required=True)))
    c("sweep", cmd_sweep, (["--through"], dict(required=True)),
      (["--client-messages"], dict(required=True, type=int)))
    c("lint", cmd_lint, (["files"], dict(nargs="+")))
    c("gate", cmd_gate, (["--stage"], dict(required=True, choices=("plan", "build", "review", "deliver"))),
      (["--brief"], dict(nargs="*")), (["--max-age-hours"], dict(type=float, default=24)))
    c("report", cmd_report, (["--for"], dict(dest="to", default="dan", choices=("dan", "reviewer", "client"))))
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
