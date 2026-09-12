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
    """watch:pass -- somebody actually looked at the moving picture.

    ⚠ WHY THIS ROW OUTRANKS EVERY METRIC HERE. `watch.py`'s own docstring records it: "Ad 1 attempt
    1 passed 11/11 on a metric gate and Dan rejected it: every check measured format, none ever
    looked at the moving picture." That file is corpus entry `ad1-vertical-attempt1` and Dan's words
    on it are "truly awful... definitely won't work."

    ⚠ PHASE 3 OF handoff-20260911-video-quality-engine.md OWNS TURNING THIS ON EVERYWHERE. Today it
    is a hard gate in /shortad-from-longform only; /shorts mentions a watch pass zero times. A
    format whose config sets `required: false` here is carrying a DATED note saying so, and the
    gate prints it as a pending row -- never as a pass.
    """
    sha = plan.get("_sha256")
    if not cfg.get("required", True):
        return Row(key, None, f"PENDING -- {cfg.get('pending', 'not yet enforced for this format')}")
    d, tied_by, why = _log_for(plan.get("watch_log"), sha, video, "watch_log")
    if why:
        return unmeasured(key, why)
    reviewed, total = d.get("reviewed", 0), d.get("boundaries", 0)
    if not total:
        return unmeasured(key, "the watch log records no boundaries, so nothing was reviewed")
    ok = d.get("inspected") is True and reviewed >= total
    return Row(key, ok,
               f"{reviewed}/{total} boundaries reviewed as consecutive frames (tied to this file "
               f"by {tied_by})"
               f"{'' if d.get('inspected') is True else '; `inspected` is not true'}",
               dict(reviewed=reviewed, boundaries=total, tied_by=tied_by))


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
