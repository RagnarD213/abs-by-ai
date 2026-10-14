"""RO-08 round 3: fold the watch-pass verdicts into the log. logs/findings_carried.json (r3_carry.py: verdicts on unchanged frames, from the
films already judged) plus logs/findings_new.json (the fresh independent reviewer on the images that changed) -> logs/findings.json -> watch.py --judge.
A `hair_top` defect on Dan's camera frames is the as-shot framing of this roll (his hair at the top edge; the picture is never cropped at the top).
Dan was asked about exactly that on the round 1 page and answered; his words are attached to those entries as `accepted_by_dan`. Nothing else is
ever given a disposition here: any other defect stays open and blocks the gate. usage: r3_judge.py"""
import json, subprocess, sys
W = "/Volumes/Extreme/_edit_work/ro08/round3"; P = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
ASK = ("Dan's words, 2026-10-12, replying to the round 1 page (recorded in round2-plan/decisions.json): \"Everything else is looking good.\" The page had put it to him "
       "as a numbered decision: \"The camera framed your hair right at the top of the picture: about 14 pixels of room on average, and it touches the edge for a moment in "
       "most shots. I never crop the top (both sizes keep the camera's own top row), but there is no spare picture above your head.\" He then reviewed the round 2 film, "
       "which has the same framing in 60 of 103 talking shots, and listed three revisions, none about framing. The round 3 page lists these newly visible frames with their times.")
new = json.load(open(f"{W}/logs/findings_new.json"))["entries"]; car = json.load(open(f"{W}/logs/findings_carried.json"))["entries"]; other = []
for e in new:
    if e.get("verdict") == "defect":
        if e.get("item") == "hair_top": e["disposition"] = "accepted_by_dan"; e["note"] = (e.get("note", "") + " | " + ASK).strip(" |")
        else: other.append(e)
json.dump(dict(entries=car + new), open(f"{W}/logs/findings.json", "w"), indent=0)
print(len(car), "carried +", len(new), "fresh entries;", sum(e.get("disposition") == "accepted_by_dan" for e in new), "hair entries carry Dan's words;", len(other), "other defect(s) left open:")
for e in other: print("  OPEN", e["image"], e.get("item"), "|", e.get("note", "")[:300])
sys.exit(subprocess.run([sys.executable, f"{P}/.claude/skills/_shared/deliver/watch.py", "--judge", f"{W}/logs/watch_pass.json", "--findings", f"{W}/logs/findings.json",
                         "--by", "independent reviewers (ra-reviewer, Claude Opus 5.5): fresh on every changed image, carried by frame comparison on the rest"]).returncode)
