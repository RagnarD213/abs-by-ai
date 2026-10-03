#!/usr/bin/env python3
"""SPLIT THE WATCH PASS AMONG FRESH JUDGES, one brief per judge, each naming exactly the images it must open.

  python3 kit_judges.py --build B [--audit B/cut_audit] [--per 110] [--min 3] [--notes NOTES.md]

The watch pass (`_shared/deliver/watch.py`) writes one strip and one -1|0 pair per boundary and a contact sheet per
25 frames. A 4 minute ad has about 170 boundaries (350 images) and three judges; an 8:38 film has twice that, and a
judge handed twice the images runs out of room before the last third. So the number of judges follows the film:
ceil(images / --per), never fewer than --min. Parts are contiguous in time (a judge sees a stretch of the film, its
sheets included), part 1 also reads the negative-events sheet.

Writes <watch>/JUDGE_PART_<k>.md (k = 1..N) and prints N. Each judge writes <logs>/findings_part<k>.json
({"judge", "video", "method", "entries": [...]}); part 1 also writes <logs>/negscan_findings.json (a JSON list, [] when
there is nothing). `kit_fold.sh` folds any number of parts.

What a judge is told about the build is read from the build itself (beats.json, plan.json), never typed: which zoom
changes are ramps and which are hard level steps, where captions pause, which pictures carry a label, whether returns
flash. --notes appends Dan's own decisions that change what counts as a defect (a crop he asked for, a camera he chose).
"""
import argparse
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SHARED = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_shared"))


def mmss(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


def strip_time(name):
    m = re.match(r"(?:strip|pair)_(\d+)_(\d+)-(\d+\.\d+)", name)
    return int(m.group(2)) * 60 + float(m.group(3)) if m else 0.0


def sheet_span(name):
    m = re.match(r"sheet_\d+_(\d+)-(\d+\.\d+)_to_(\d+)-(\d+\.\d+)", name)
    return (int(m.group(1)) * 60 + float(m.group(2)), int(m.group(3)) * 60 + float(m.group(4))) if m else (0.0, 0.0)


def declarations(B, audit):
    """What the build itself declares, in plain sentences a judge can check a strip against."""
    out = []
    bj = json.load(open(os.path.join(B, "beats.json")))
    plan = json.load(open(os.path.join(audit, "plan.json")))
    sbl = bj.get("style") == "softblue"
    out.append("Graphics are Soft Blue Light (navy field, glass cards, cyan accents), drawn with HyperFrames." if sbl else
               "Graphics are the editor's olive kit (olive field, cards, lower thirds, CTA pill).")
    if not audit.endswith("cut_audit"):
        steps = [p for p in bj.get("pushes", []) if abs(p[1] - p[0]) < 1e-6 or abs(p[3] - p[2]) < 1e-6]
        ramps = [p for p in bj.get("pushes", []) if p not in steps]
        out.append(f"Zoom changes (strips labelled `punch:NEAR` / `punch:FAR`): {len(ramps)} are RAMPS (about half a second of "
                   f"gradual push in or out; the strip shows a slow zoom, never a step) and {len(steps)} have a HARD edge (a "
                   f"punch-in or punch-out on a cut, on purpose: it is what hides the cut). A hard zoom change at a labelled "
                   f"boundary is `expected`; a same-size jump of his head with no zoom change is a `naked_splice`.")
    else:
        out.append("This is the <= 0:59 cut. Its seams (strips labelled `join`) are where two parts of the full film meet: each "
                   "must be a change of picture or of zoom level. Same shot both sides with his head jumping is a `naked_splice`.")
    out.append("Returns from a picture " + ("flash white for a few frames (the editor's transition)." if bj.get("flashes") else
                                            "are HARD CUTS. There is no white flash and no dissolve in this build."))
    caps = plan.get("cards") or []
    out.append(f"Captions are burned in (one line, the spoken word lit). They PAUSE on purpose under {len(caps)} stretches: every "
               f"lower third, every full-screen graphic, phone screens, and any side card too tall to lift them above. Over a "
               f"short bottom card they are LIFTED above the card instead. A caption printed ON a graphic is a defect "
               f"(`label_over_face` covers a caption on a card); a caption missing where nothing covers it is `graphic_missing`.")
    if sbl:
        out.append("A horizontal clip is cropped at the sides to what it is about and shown either full screen or in a card. A "
                   "TALL card runs down past the caption line on purpose, so captions sit inside its picture exactly as they do "
                   "on a full-screen clip: that is not a collision. Blank field above and below a wide card is by design.")
        out.append("The crop that follows him is the standard camera (Dan, 2026-10-03): it lands on him at each cut, then holds "
                   "still until he drifts a little off centre, then follows slowly. A slow drift of the frame is `expected`. "
                   "His head or hair leaving the frame, or an arm cut with space on the other side, is a defect.")
    lab = [(t["name"], t["beat"], t["kind"]) for t in plan.get("label_tracks") or []]
    if lab:
        out.append("Pictures that must carry a label chip for their whole time on screen: "
                   + "; ".join(f"{n.split('-', 2)[-1]} {mmss(b[0])} to {mmss(b[1])} ({'AI-GENERATED' if k == 'ai' else 'Real picture of me'})"
                               for n, b, k in lab)
                   + ". The chip must be readable and clear of any face and any abs. A missing or wrong chip is a defect.")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True)
    ap.add_argument("--audit", help="the cutdown's audit dir (B/cut_audit); default: the build itself")
    ap.add_argument("--per", type=int, default=110, help="images per judge (an ad's three judges read about 115 each)")
    ap.add_argument("--min", type=int, default=3)
    ap.add_argument("--notes", help="a file of Dan's decisions that change what counts as a defect; appended to every brief")
    ap.add_argument("--rejudge", help="after carry_verdicts.py: logs/rejudge.json. ONE brief (part 2) for exactly those images; "
                                      "part 1 is the carried verdicts. The judge also reads the negscan sheet when it was not carried")
    a = ap.parse_args()
    B = os.path.abspath(a.build)
    A = os.path.abspath(a.audit) if a.audit else B
    wd, logs = os.path.join(A, "watch"), os.path.join(A, "logs")
    wp = json.load(open(os.path.join(logs, "watch_pass.json")))
    strips = sorted(wp["strips"], key=strip_time)
    pair_of = {re.match(r"strip_(\d+)_", s).group(1): None for s in strips}
    for p in wp.get("pairs", []):
        pair_of[re.match(r"pair_(\d+)_", p).group(1)] = p
    sheets = sorted(wp["sheets"], key=lambda s: sheet_span(s)[0])
    only = set(json.load(open(a.rejudge))) if a.rejudge else None
    if only is not None:
        # a strip and its pair are read together: either one changed, the judge gets both
        idx = {re.match(r"(?:strip|pair)_(\d+)_", x).group(1) for x in only if re.match(r"(?:strip|pair)_(\d+)_", x)}
        strips = [s_ for s_ in strips if re.match(r"strip_(\d+)_", s_).group(1) in idx]
        sheets = [s_ for s_ in sheets if s_ in only]
    total = len(strips) + (len(strips) if only is not None else len(wp.get("pairs", []))) + len(sheets)
    n = 1 if only is not None else max(a.min, math.ceil(total / a.per))
    first = 1 if only is not None else 0                      # a re-judge writes part 2 (part 1 holds the carried verdicts)
    need_neg = only is None or not os.path.exists(os.path.join(logs, "negscan_findings.json"))
    dur = float(wp["duration"])
    decl = declarations(B, A)
    notes = open(a.notes).read().strip() if a.notes else ""
    checklist = open(os.path.join(wd, "CHECKLIST.md")).read()
    for old in os.listdir(wd):
        if old.startswith("JUDGE_PART_"):
            os.remove(os.path.join(wd, old))
    for k in range(n):
        t0, t1 = dur * k / n, dur * (k + 1) / n
        st = [s for s in strips if t0 <= strip_time(s) < t1 or (k == n - 1 and strip_time(s) >= t1)]
        sh = [s for s in sheets if t0 <= sum(sheet_span(s)) / 2 < t1 or (k == n - 1 and sum(sheet_span(s)) / 2 >= t1)]
        part = k + 1 + first
        lines = [f"# Judge part {part}{'' if only is not None else f' of {n}'}: the watch pass on `{wp['path']}`", "",
                 (f"You are an independent judge of {len(st) * 2 + len(sh)} images taken from across this video "
                  f"({mmss(dur)} long). Judge them exactly as you would a whole film. Nothing "
                  if only is not None else
                  f"You are an independent judge of one stretch of this video ({mmss(t0)} to {mmss(t1)} of {mmss(dur)}). Nothing ")
                 + "about this file has been looked at by a person yet; you are that person. Be skeptical: the session that built "
                 "it believes it is fine. Do not read the build's notes, handoffs or any other judge's findings.", "",
                 "## What to do", "",
                 f"1. Open EVERY image listed below with the Read tool, one at a time, and give EVERY image a verdict: `clean`, "
                 f"`defect` (name the checklist item) or `expected` (say what the build declares there). There are {len(sh)} "
                 f"contact sheets, {len(st)} boundary strips and {len(st)} pairs in your part. Do not sample. Do not stop early. "
                 "An image you did not open cannot be `clean`.",
                 "2. A strip is five CONSECUTIVE frames at -2/-1/0/+1/+2 around a boundary; its `pair_*` image is the -1|0 "
                 "frames at half resolution. A jump cut is visible ONLY there: same scene both sides and the subject moves. "
                 "Sheets are for framing, cards, labels and junk; a sheet cannot show a cut.",
                 "3. When something looks wrong on a sheet or a strip, grab the exact frames at full size before you call it a "
                 "defect (put `-ss` AFTER `-i`, or seek at least two seconds early): "
                 f"`'{os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))), 'Media/video_edit/bin/ffmpeg')}' "
                 f"-v error -i '{wp['path']}' -ss <t> -frames:v 1 <scratch>.png`. Write scratch files only under "
                 f"`{os.path.join(A, 'judge_scratch', f'part{part}')}`. Never judge a defect from a downscaled tile.",
                 f"4. Write `{os.path.join(logs, f'findings_part{part}.json')}`:",
                 '   `{"judge": "<who you are>", "video": "' + wp["video"] + '", "method": "<what you opened and measured>", '
                 '"entries": [{"image": "<file name>", "verdict": "clean"|"defect"|"expected", "item": "<checklist key, for a '
                 'defect>", "t": <seconds>, "note": "<what you saw; for expected, what the build declares there>"}, ...]}`',
                 "   At least one entry per image (use the bare file name); several for an image with several findings."]
        if k == 0 and need_neg:
            lines += [f"5. You also judge the negative-events sheet `{os.path.join(A, 'negscan', 'sheet.jpg')}` (evenly spaced "
                      "frames of the whole film): look for body-shame framing only (a close-up of an out-of-shape body part "
                      "framed with shame, a 'before' shot lingered on with contempt). Write "
                      f"`{os.path.join(logs, 'negscan_findings.json')}`: a JSON list, `[]` when there is nothing, otherwise "
                      '`[{"t": <seconds>, "what": "...", "disposition": "cleared"|"confirmed_violation"|"needs_review"}]`. '
                      f"Do NOT put the negscan sheet in findings_part{part}.json."]
        lines += [f"{6 if k == 0 and need_neg else 5}. Report back in a few lines: the count of clean / expected / defect, every defect with its "
                  "time and item, and your plain opinion of any trade-off you saw.", "",
                  "## What this build declares (use it to tell `expected` from `defect`)", ""] + [f"- {d}" for d in decl]
        if notes:
            lines += ["", "## Dan's own decisions on this video (these are not defects)", "", notes]
        lines += ["", "## " + checklist.lstrip("# ").strip(), "", "## Your images", "",
                  f"Folder: `{wd}`", "", "Contact sheets (`sheets/`):"] + [f"- sheets/{s}" for s in sh] + \
                 ["", "Boundary strips (`strips/`), each with its pair beside it in the same folder:"]
        for s in st:
            idx = re.match(r"strip_(\d+)_", s).group(1)
            lines.append(f"- strips/{s}" + (f"  +  strips/{pair_of[idx]}" if pair_of.get(idx) else ""))
        open(os.path.join(wd, f"JUDGE_PART_{part}.md"), "w").write("\n".join(lines) + "\n")
        print(f"part {part}: {mmss(t0)} to {mmss(t1)}  {len(sh)} sheets, {len(st)} strips + pairs")
    print(f"{n} judge(s) for {total} images -> {wd}/JUDGE_PART_{1 + first}..{n + first}.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
