#!/usr/bin/env python3
"""Put every filmed video from a shoot on the Abs By AI Edit Queue: one job doc each, a master-list section,
jobs.json rows (Drive status file updated by queue.py), and the export the artifact db needs.

    register_jobs.py next-ids                      # next free number per prefix (RA, RO, DS, WV, SL, AV, AS)
    register_jobs.py check  spec.json              # validate: ids free, groups visible on the page, sources listed
    register_jobs.py apply  spec.json              # write docs + master section + queue.py add + export

Run from the project root on the Mac whose repo you will push from. Then mirror to the page:
`ArtifactData batch` with the `set` entries printed by apply (new rows need no if_version), then
`queue.py mark-synced <ids>`, then `scripts/git/safe-push.sh` the docs, jobs.json and 00-MASTER.md.

spec.json (see SKILL.md for a full example):
{
  "shoot": "11:13 dan rose fitness shoot - green screen",   # exact Extreme folder name
  "label": "11/13",                                          # short date used in titles/rolls
  "report": "Docs/SHOOT_1113_FOOTAGE_REPORT.md",
  "section": "1C5 · 11/13 shoot, green screen",              # master-list heading (inserted before LIST 2)
  "jobs": [ {"id": "RA-17", "cat": "AD (Great Again T long ad)", "group": "Short-form ads", "sub": "",
             "title": "Great Again T L01: Eat More Of This, Less Of This", "task": "GAT L01 AD R1", "size": "M",
             "sources": [["C1913", "5:03-12:40", "keeper"]], "script": "script L01 in <doc name, id>",
             "orient": "landscape 3840x2160", "deliver": "One 16:9 long ad ...",
             "skill_claude": "/ad-edit", "skill_codex": "`.claude/skills/ad-edit/SKILL.md`",
             "state": "ready|blocked|needs", "note": "", "needs": "", "extra": ""} ]
}
"""
import json, os, re, subprocess, sys

ROOT = os.getcwd()
VE = os.path.join(ROOT, "Handoffs/video-editing")
JOBS = os.path.join(VE, "jobs.json")
MASTER = os.path.join(VE, "00-MASTER.md")
# Groups and Dedicated-shorts subs the Edit Queue page actually renders (artifact 1r1T8Znf96XH24zHZhybHs,
# LISTS array and the Dedicated shorts sub list). A row in any other group or sub is invisible to Dan
# (memory edit-queue-artifact-is-working-list). Change this only after the page itself renders the new group.
PAGE = {"1": ["Website VSLs", "Short-form ads", "Dedicated shorts", "Organic long-form", "Housekeeping"],
        "2": ["Shorts from long-forms"], "3": ["Ad verticals", "Ad squares"]}
DS_SUBS = ["10/15 shoot", "9/23 shoot", "Talking", "Workout"]
STATES = {"ready": "READY", "blocked": "BLOCKED", "needs": "**NEEDS DAN**"}


def jobs_now():
    return json.load(open(JOBS))["jobs"]


def next_ids():
    best = {}
    for j in jobs_now():
        p, _, n = j["id"].partition("-")
        if n.isdigit():
            best[p] = max(best.get(p, 0), int(n))
    return {p: f"{p}-{n+1}" for p, n in sorted(best.items())}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("'", "")).strip("-")[:60].rstrip("-")


def check(spec):
    errs, have = [], {j["id"] for j in jobs_now()}
    for j in spec["jobs"]:
        lst = j.get("list", "1")
        if j["id"] in have:
            errs.append(f"{j['id']} already exists in jobs.json")
        if j["group"] not in PAGE.get(lst, []):
            errs.append(f"{j['id']}: group '{j['group']}' is not shown on the Edit Queue page (list {lst}: {PAGE.get(lst)})")
        if j["group"] == "Dedicated shorts" and j.get("sub") not in DS_SUBS:
            errs.append(f"{j['id']}: Dedicated shorts sub '{j.get('sub')}' is not rendered ({DS_SUBS})")
        if not j.get("sources"):
            errs.append(f"{j['id']}: no source rolls")
        if j.get("state", "ready") == "blocked" and not j.get("needs"):
            errs.append(f"{j['id']}: blocked rows need 'needs' (what unblocks it)")
        if not re.match(r"^(AD|CONTENT)\b", j["cat"]):
            errs.append(f"{j['id']}: cat must start with AD or CONTENT (categorize before editing rule)")
    return errs


def doc_for(spec, j, fn):
    shoot, report = spec["shoot"], spec["report"]
    rolls = " + ".join(dict.fromkeys(s[0] for s in j["sources"]))
    base = (f"Read `Handoffs/video-editing/00-RULES.md` and `{report}`, then execute `Handoffs/video-editing/{fn}`: "
            f"cut \"{j['title']}\" from the {spec['label']} shoot, rolls {rolls}.")
    key = " Key with the approved house chroma key." if j.get("greenscreen", True) else ""
    cp = (f"{j['cat']}. Name this chat \"{j['task']}\". {base} Use {j['skill_claude']}.{key} Best take of every line, "
          "first-review approvals before the full render, every gate, independent audit, deliver, send me the review copy, update the queue.")
    xp = (f"{j['cat']}. Name this chat \"{j['task']}\". {base} Use {j['skill_codex']}.{key} Follow the first-review "
          "approvals before the full render. Deliver, send Dan the review copy, update `00-MASTER.md`.")
    st = j.get("state", "ready")
    status = {"ready": "Filmed source ready for editing.", "blocked": f"Blocked: {j.get('needs')}.",
              "needs": f"Needs Dan: {j.get('note')}"}[st]
    table = "\n".join(f"| `{s[0]}` | {s[1]} | {s[2] if len(s) > 2 else ''} |" for s in j["sources"])
    extra = f"- {j['extra']}\n" if j.get("extra") else ""
    gs = ("- Green screen: key with the approved house key (`.claude/skills/_shared/chroma-key/README.md`), calibrated to these rolls.\n"
          if j.get("greenscreen", True) else "")
    doc = f"""{j['cat']}. Task name: `{j['task']}`.

# {j['id']}: {j['title']}

**{status}** Registered from the {spec['label']} shoot. Not edited, rendered, approved, uploaded or scheduled.

## Read first

`00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, and the shoot report `{report}` (format, orientation, camera clock, full roll map).
Script: {j['script']}. The filmed wording wins where Dan departed from the script.

## Sources

Working copies: `/Volumes/Extreme/{shoot}/`. Verified second copy: `/Volumes/Expansion/Abs By AI Raw Footage/{shoot}/`. Never modify the originals.
Times are minutes:seconds into each roll, checked against the spoken announcements in the transcripts; read each roll's `.roll.json` sidecar (word timings, mic pick) before cutting.

| roll | range | notes |
|---|---|---|
{table}

Orientation: **{j['orient']}**.

## Build

{gs}- Pick the best take of every line across all takes listed above. Watch the whole range; hook restarts and retakes are common.
- Graphics follow the Soft Blue Light HyperFrames standard. AI clip frames, if any, go to Dan as START and END pairs first.
- First review before any full render, per `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`.
{extra}
## Deliver

{j['deliver']} Covers and upload/setup are separate tasks after Dan approves the film (Codex owns setup).

## Starter prompts

**Claude: Opus 5.5, high effort.**
> {cp}

**Codex: newest GPT Sol, high effort.**
> {xp}
"""
    return doc, cp, xp, rolls


def apply(spec):
    errs = check(spec)
    if errs:
        sys.exit("Fix these first:\n  " + "\n  ".join(errs))
    order = max(j.get("order", 0) for j in jobs_now()) + 1
    rows, lines, today = [], [], subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()
    for j in spec["jobs"]:
        fn = f"{j['id']}-{slug(j['title'])}.md"
        doc, cp, xp, rolls = doc_for(spec, j, fn)
        open(os.path.join(VE, fn), "w").write(doc)
        st = j.get("state", "ready")
        row = {"id": j["id"], "list": j.get("list", "1"), "group": j["group"], "sub": j.get("sub", ""),
               "title": j["title"], "roll": f"{spec['label']} {rolls}", "size": j["size"], "file": fn,
               "claudeModel": "Opus 5.5, high", "claude": cp, "codexModel": "GPT-6.1 Sol, high", "codex": xp,
               "state": st, "note": j.get("note") or (f"{spec['label']} shoot, " + "; ".join(f"{s[0]} {s[1]}" for s in j["sources"])),
               "order": order, "updated": today, "by": "Claude", "rev": 1}
        if j.get("needs"):
            row["needs"] = j["needs"]
        order += 1
        rows.append(row)
        lines.append(f"| [{j['id']}]({fn}) | {j['title']} | {rolls} | {STATES[st]} | {j['size']} |")
    tmp = os.path.join(ROOT, "tmp", "process-footage-new-jobs.json")
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    json.dump(rows, open(tmp, "w"), indent=1)
    m = open(MASTER).read()
    if spec["section"] not in m:
        sec = (f"\n### {spec['section']} (added {today})\nRoll map and formats: `{spec['report']}`.\n\n"
               "| job | video | rolls | status | size |\n|---|---|---|---|---|\n" + "\n".join(lines) + "\n\n---\n\n")
        k = m.index("## LIST 2")
        m = m[:k] + sec.lstrip("\n") + m[k:]
        open(MASTER, "w").write(m)
    r = subprocess.run([sys.executable, "scripts/edit-queue/queue.py", "add", tmp], capture_output=True, text=True)
    print(r.stdout[-6000:], r.stderr[-2000:])
    print("Docs:", " ".join("Handoffs/video-editing/" + x["file"] for x in rows))


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("next-ids", "check", "apply"):
        sys.exit(__doc__)
    if sys.argv[1] == "next-ids":
        print(json.dumps(next_ids(), indent=1))
    else:
        spec = json.load(open(sys.argv[2]))
        if sys.argv[1] == "check":
            e = check(spec)
            print("OK" if not e else "\n".join(e))
        else:
            apply(spec)
