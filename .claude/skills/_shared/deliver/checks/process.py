#!/usr/bin/env python3
"""Rows that prove a step HAPPENED on this exact file, rather than measuring the picture.

Everything here is keyed on the delivered file's sha256. A watch pass on the previous render, a
caption-sync stamp from a test cut, a subtitle file from the version before the re-cut -- each one
reads as done and is not.
"""
import json
import os
import re

from ..common import Row, unmeasured


def _log_for(path, sha, video, what):
    """Read a build log and confirm it names THIS file.

    A sha256 is the only real proof, because a re-render keeps the path and the filename. A log that
    names only a filename is accepted with that weaker check and says so; a log that names neither
    is refused outright, since it could have been written for anything.
    """
    if not path:
        return None, None, f"the plan gives no `{what}`"
    if not os.path.exists(path):
        return None, None, f"`{what}` is not on disk: {path}"
    try:
        d = json.load(open(path))
    except Exception as e:                                   # noqa: BLE001
        return None, None, f"`{what}` is not readable json ({e})"
    named = d.get("sha256") or d.get("file_sha256")
    if named:
        if named != sha:
            return None, None, (f"`{what}` is for {str(named)[:12]}, this file is {str(sha)[:12]} "
                                f"-- it was written for a different render")
        return d, "sha256", None
    base = d.get("video") or d.get("file")
    if not base:
        return None, None, (f"`{what}` names neither a sha256 nor a video, so it cannot be tied to "
                            f"this render and proves nothing")
    if os.path.basename(base) != os.path.basename(video):
        return None, None, (f"`{what}` is for {os.path.basename(base)}, not "
                            f"{os.path.basename(video)}")
    return d, "filename", None


def watch_pass(key, pr, cfg, plan, video, work):
    """watch:pass -- somebody actually looked at the moving picture, and found nothing left open.

    ⚠ WHY THIS ROW OUTRANKS EVERY METRIC HERE. `watch.py`'s own docstring records it: "Ad 1 attempt
    1 passed 11/11 on a metric gate and Dan rejected it: every check measured format, none ever
    looked at the moving picture." That file is corpus entry `ad1-vertical-attempt1` and Dan's words
    on it are "truly awful... definitely won't work."

    A HARD GATE FOR EVERY FORMAT since 2026-09-16 (Phase 3). The log is written by
    `_shared/deliver/watch.py` for THIS file's sha256, and passes only when:
      * `inspected` is true and `reviewed` covers every boundary the pass wrote a strip for;
      * every sheet and every strip the pass wrote carries a verdict in `judged` (the judge cannot
        skip an image);
      * no `defect` verdict is left open (a defect is closed only by a re-render -- which changes
        the sha256 and voids the log -- or by `disposition: accepted_by_dan` with his words).
    A log from one of the retired per-skill forks (no `watch_version`) is refused: it was never
    judged image by image and it cannot say what it looked at.
    """
    sha = plan.get("_sha256")
    if not cfg.get("required", True):
        return Row(key, None, f"PENDING -- {cfg.get('pending', 'not yet enforced for this format')}")
    d, tied_by, why = _log_for(plan.get("watch_log"), sha, video, "watch_log")
    if why:
        return unmeasured(key, why)
    if not d.get("watch_version"):
        return unmeasured(key, "the watch log was not written by _shared/deliver/watch.py (no "
                               "`watch_version`); the per-skill forks are retired -- re-run the shared pass")
    if tied_by != "sha256":
        return unmeasured(key, "the watch log names no sha256; the shared watch.py always writes one, "
                               "so this log was edited or written by something else")
    reviewed, total = int(d.get("reviewed") or 0), int(d.get("boundaries") or 0)
    if not total:
        return unmeasured(key, "the watch log records no boundaries, so nothing was reviewed")
    images = set(d.get("sheets") or []) | set(d.get("strips") or [])
    if not images:
        return unmeasured(key, "the watch log lists no sheets or strips, so there was nothing to judge")
    judged = d.get("judged") or []
    covered = {os.path.basename(str(e.get("image", ""))) for e in judged}
    missing = sorted(images - covered)
    open_defects = [e for e in judged
                    if e.get("verdict") == "defect" and e.get("disposition") != "accepted_by_dan"]
    accepted = [e for e in judged
                if e.get("verdict") == "defect" and e.get("disposition") == "accepted_by_dan"]
    inspected = d.get("inspected") is True
    ok = inspected and reviewed >= total and not missing and not open_defects
    problems = []
    if not inspected:
        problems.append("`inspected` is not true")
    if reviewed < total:
        problems.append(f"only {reviewed}/{total} boundaries reviewed")
    if missing:
        problems.append(f"{len(missing)} image(s) without a verdict (first: {missing[:3]})")
    if open_defects:
        problems.append(f"{len(open_defects)} open defect(s): " + "; ".join(
            f"{e.get('item')} @ {e.get('t', e.get('image'))}" for e in open_defects[:4]))
    return Row(key, ok,
               f"{reviewed}/{total} boundaries reviewed as consecutive frames, {len(covered)}/{len(images)} "
               f"images judged by {d.get('judged_by') or '?'} (tied to this file by sha256)"
               f"{'; ' + str(len(accepted)) + ' defect(s) accepted by Dan' if accepted else ''}"
               f"{'; ' + ', '.join(problems) if problems else ''}",
               dict(reviewed=reviewed, boundaries=total, images=len(images), judged=len(covered),
                    open_defects=len(open_defects), accepted=len(accepted), tied_by=tied_by,
                    watch_version=d.get("watch_version")))


def srt_present(key, pr, cfg, plan, video, work):
    """srt:present -- the sidecar exists and is the deliverable this format promises."""
    srt = plan.get("srt")
    if not cfg.get("required", True):
        return Row.na(key, cfg.get("why", "this format ships no subtitle sidecar"))
    if not srt or not os.path.exists(srt):
        return Row(key, False, f"no subtitle sidecar on disk ({srt!r})")
    return Row(key, True, f"{os.path.basename(srt)}", dict(srt=srt))


def srt_shape(key, pr, cfg, plan, video, work):
    """srt:shape -- line length, line count, and the spellings this project keeps re-breaking."""
    srt = plan.get("srt")
    if not srt or not os.path.exists(srt):
        return unmeasured(key, f"no subtitle sidecar on disk ({srt!r})")
    body = open(srt, errors="replace").read()
    cues = [c for c in re.split(r"\n\s*\n", body.strip()) if "-->" in c]
    lines = [l for c in cues for l in c.split("\n")[2:] if l.strip()]
    longest = max((len(l) for l in lines), default=0)
    three = [c.split("\n")[0] for c in cues if len([l for l in c.split("\n")[2:] if l.strip()])
             > cfg["max_lines"]]
    wrong = [p for p in cfg.get("banned_spellings", []) if p in body]
    ok = longest <= cfg["max_line_chars"] and not three and not wrong
    return Row(key, ok,
               f"{len(cues)} cues, longest line {longest} chars (max {cfg['max_line_chars']}), "
               f"{len(three)} cue(s) over {cfg['max_lines']} lines, "
               f"{len(wrong)} banned spelling(s) {wrong}",
               dict(cues=len(cues), longest=longest, over=three[:10], spellings=wrong))
