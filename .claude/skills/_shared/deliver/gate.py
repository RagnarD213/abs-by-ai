#!/usr/bin/env python3
"""THE DELIVERY GATE. One gate, called by all six video skills, run on the DELIVERED FILE.

  gate.py <file> --format ad9x16|ad16x9|ad1x1|longform|short|website|exercise-demo [--plan plan.json]
  gate.py --audit                 every format answers for every row, or say what is missing
  gate.py --formats               list the formats and their notes

WHY THIS FILE EXISTS. Across the six video skills there were 485 Python scripts, 60 of them
QC/gate/delivery scripts, and exactly one shared module (`_shared/audio`). `_shared/` had no
picture, framing, cut, caption or compliance module at all, so a fix landed in one of six pipelines
and the other five kept the bug. Dan's eleven recorded rejections are 5 audio, 4 framing, 2
wholesale and 1 junk -- and they repeat, because ours are REGRESSIONS rather than rule misses. A
pre-flight checklist fixes a human editor's class of defect. Only shared code fixes ours.

THE FOUR RULES THIS GATE IS BUILT ON
  1 A MISSING INPUT IS "NOT MEASURED", WHICH FAILS. Never [SKIP]. The ancestor of this gate passed
    11/11 on a video Dan called "truly awful" because every check measured format and none watched
    the picture; a second one printed [SKIP] for every check whose flag a session forgot to type.
  2 NO FREE DIALS. Named per-format profiles only. A bound that can be passed on the command line
    is not a bound.
  3 A ROW A FORMAT HAS NOT ANSWERED FOR IS UNCONFIGURED, WHICH FAILS. If a check genuinely does not
    apply, that is an explicit entry in `formats.py` carrying a reason a reader can audit.
  4 THE GATE IS VERSIONED. Any change to a check or a bound bumps GATE_VERSION and every stamp at
    an older version becomes invalid. ⚠ The baseline proves why: Docs/VQC_baseline_20260909.md
    found 20 delivered files carrying a PASS stamp that would fail a re-gate today -- including 16
    Zepbound and supplements Shorts stamped 2026-09-02 on the dereverb Dan rejected a week later --
    and 139 of 166 masters carrying no stamp at all. Nothing re-checks a stamp when the standard
    moves. Versioning is what makes that automatic.

THE PLAN. Rows that need to know what the build intended read `--plan plan.json`. Its keys are
documented in PLAN_KEYS below. Every path in it resolves against the plan file's own directory
unless absolute. A row whose plan key is absent reads NOT MEASURED -- it does not quietly pass.
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))                    # so `_shared.deliver` imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

from _shared.deliver import common as C                      # noqa: E402
from _shared.deliver import formats as FMT                   # noqa: E402
from _shared.deliver.checks import audio as A                # noqa: E402
from _shared.deliver.checks import captions as CAP           # noqa: E402
from _shared.deliver.checks import container as CON          # noqa: E402
from _shared.deliver.checks import compliance as COMP        # noqa: E402
from _shared.deliver.checks import picture as PIC            # noqa: E402
from _shared.deliver.checks import process as PROC           # noqa: E402
from _shared.deliver.common import Row                       # noqa: E402

# ⚠ BUMP THIS ON ANY CHANGE TO A CHECK OR A BOUND. Every stamp at an older version is invalid.
#   1.0.0  2026-09-11  first version. Folds in the rows of the seventeen per-video QC forks, adds
#                      audio:lipsync and the compliance rows, and moves every bound into formats.py
#                      with the file and date it was measured on.
GATE_VERSION = "1.1.0"        # 1.1.0: an insert may declare its own label chip + position
                              # (a card hangs its chip off the card, not at the full-bleed waistline)

STAMP_SUFFIX = ".deliver_gate.json"

PLAN_KEYS = """
  target_seconds / target_frames   what the build meant to deliver  (container:duration, :frames)
  reference_cut                    the cut this one reproduces; sets target_seconds if absent
  joins            [t, ...]        splice times on the DELIVERED timeline
  covered          [[a, b], ...]   beats that hide a join
  punch            [[a, b, LEVEL]] framing segments;  punch_covered [bool] marks the hidden ones
  graphics         [{name, beat:[a,b], mov}]        lower thirds and cards, with their own MOVs
  ai_inserts       [{name, beat:[a,b], chip?, pos?}] AI imagery of Dan
  real_photos      [{name, beat:[a,b], chip?, pos?}] REAL photographs of Dan
  cards            [[a, b], ...]   full-screen beats a caption may not sit on
  label_chips      {ai: png, real: png}             label_pos {ai: [x,y], real: [x,y]}
                                   -- an insert's own `chip`/`pos` override these
  captions_ass / srt               the caption file as delivered
  words            [{w, t, e}]     what the cut intended to say
  transcript_words [{w}]           what the FINISHED render actually says (re-transcribed)
  source_audio                     the mix the picture was cut against, BEFORE the loudness finish
  banned_source / banned_times     the recording that contains the banned app screens
  watch_log                        logs/watch_pass.json, naming this file's sha256
  negative_events_scan             {sha256, when, frames_checked, findings}
  declare          {row: reason}   this BUILD declares one row inapplicable, with a written reason
"""

# ---------------------------------------------------------------------------- the registry
# key -> (what the check is handed, the callable). Nothing here decides WHICH rows run -- the
# format's config in formats.py does, and a row it has not answered for fails as UNCONFIGURED.
#   "probe"    (key, probe_dict, cfg, plan, video)
#   "picture"  (key, Picture, cfg, plan)          -- shares one set of decodes across every row
#   "work"     (key, probe_dict, cfg, plan, video, workdir)
ROWS = {
    "container:size":             ("probe", CON.size),
    "container:fps":              ("probe", CON.fps),
    "container:codec":            ("probe", CON.codec),
    "container:duration":         ("probe", CON.duration),
    "container:frames":           ("probe", CON.frames),
    "audio:stamp":                ("probe", A.stamp),
    "audio:stream_integrity":     ("probe", A.stream_integrity),
    "audio:lipsync":              ("probe", A.lipsync),
    "audio:click_at_joins":       ("probe", A.click_at_joins),
    "style:coverage":             ("picture", PIC.coverage),
    "style:static_run":           ("picture", PIC.static_run),
    "style:change_rate":          ("picture", PIC.change_rate),
    "cut:uncovered_joins":        ("picture", PIC.uncovered_joins),
    "cut:black_frames":           ("picture", PIC.black_frames),
    "cut:min_segment":            ("picture", PIC.min_segment),
    "cut:jump_cut":               ("picture", PIC.jump_cut),
    "cut:splice_visibility":      ("picture", PIC.splice_visibility),
    "captions:graphic_clearance": ("work", CAP.graphic_clearance),
    "captions:card_collision":    ("work", CAP.card_collision),
    "captions:burned":            ("work", CAP.burned),
    "captions:within_runtime":    ("work", CAP.within_runtime),
    "captions:sync":              ("work", CAP.sync),
    "compliance:banned_screen":   ("work", COMP.banned_screen),
    "compliance:labels":          ("work", COMP.labels),
    "compliance:drug_names":      ("work", COMP.drug_names),
    "compliance:negative_events": ("work", COMP.negative_events),
    "compliance:script_fidelity": ("work", COMP.script_fidelity),
    "watch:pass":                 ("work", PROC.watch_pass),
    "srt:present":                ("work", PROC.srt_present),
    "srt:shape":                  ("work", PROC.srt_shape),
}

# Every row formats.py knows about must have an implementation, and vice versa. A row named in one
# and not the other is the "SKILL.md asserts a check nothing performs" failure, caught at import.
_missing = set(FMT.ALL_ROWS) - set(ROWS)
_extra = set(ROWS) - set(FMT.ALL_ROWS)
if _missing or _extra:
    raise SystemExit(f"gate.py and formats.py disagree about the row set: "
                     f"formats-only {sorted(_missing)}, gate-only {sorted(_extra)}")


# ---------------------------------------------------------------------------- the plan
def load_plan(path, video):
    """Read plan.json and resolve every path in it against the plan's own directory."""
    plan = {}
    if path:
        if not os.path.exists(path):
            raise SystemExit(f"--plan {path} is not on disk")
        plan = json.load(open(path))
        base = os.path.dirname(os.path.abspath(path))
        for k in ("reference_cut", "captions_ass", "srt", "source_audio", "banned_source",
                  "watch_log", "his_mix"):
            if plan.get(k) and not os.path.isabs(plan[k]):
                plan[k] = os.path.normpath(os.path.join(base, plan[k]))
        for g in (plan.get("graphics") or []):
            if g.get("mov") and not os.path.isabs(g["mov"]):
                g["mov"] = os.path.normpath(os.path.join(base, g["mov"]))
        chips = plan.get("label_chips") or {}
        for k, v in list(chips.items()):
            if v and not os.path.isabs(v):
                chips[k] = os.path.normpath(os.path.join(base, v))
        for b in (plan.get("ai_inserts") or []) + (plan.get("real_photos") or []):
            if b.get("chip") and not os.path.isabs(b["chip"]):
                b["chip"] = os.path.normpath(os.path.join(base, b["chip"]))
    plan["_sha256"] = C.sha256(video)
    plan["_dir"] = os.path.dirname(os.path.abspath(path)) if path else os.path.dirname(
        os.path.abspath(video))
    return plan


# ---------------------------------------------------------------------------- running
def run(video, fmt, plan_path=None, only=None):
    F = FMT.config_for(fmt)
    rows_cfg, na = F["rows"], F.get("not_applicable", {})
    plan = load_plan(plan_path, video)
    declared = plan.get("declare") or {}
    pr = C.probe(video)
    if pr["vdur"] is None:
        raise SystemExit("the video stream reports no duration; this file is not deliverable")
    pic = PIC.Picture(video, pr["vdur"])
    work = plan["_dir"]

    out = []
    for key in FMT.ALL_ROWS:
        if only and key not in only:
            continue
        # 1. the FORMAT says it does not apply -- a written, dated reason in formats.py
        if key in na and key not in rows_cfg:
            out.append(Row.na(key, na[key]))
            continue
        # 2. this BUILD says it does not apply -- a written reason in its own plan.json
        if key in declared:
            out.append(Row.na(key, f"declared by this build: {declared[key]}"))
            continue
        # 3. the format never answered for it. That is the bug, and it fails.
        if key not in rows_cfg:
            out.append(Row(key, False, f"UNCONFIGURED -- format {fmt!r} neither configures this "
                                       f"row nor declares it not applicable in formats.py"))
            continue
        cfg = rows_cfg[key]
        kind, fn = ROWS[key]
        try:
            if kind == "picture":
                r = fn(key, pic, cfg, plan)
            elif kind == "probe":
                r = fn(key, pr, cfg, plan, video)
            else:
                r = fn(key, pr, cfg, plan, video, work)
        except Exception as e:                               # noqa: BLE001
            import traceback
            r = Row(key, False, f"the check itself raised {type(e).__name__}: {e}",
                    dict(traceback=traceback.format_exc()[-800:]))
        out.append(r)
    return pr, plan, out


def verdict(rows):
    """PASS only when every row was measured and passed. PENDING rows never make a PASS."""
    fails = [r for r in rows if r.ok is False]
    unmeasured = [r for r in rows if r.ok is None and "PENDING" not in r.detail]
    pending = [r for r in rows if r.ok is None and "PENDING" in r.detail]
    return ("PASS" if not fails and not unmeasured else "FAIL"), fails, unmeasured, pending


def stamp(video, fmt, rows, v, pr):
    d = dict(gate_version=GATE_VERSION, format=fmt, verdict=v,
             sha256=C.sha256(video), bytes=os.path.getsize(video),
             when=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
             size=pr["size"], fps=pr["fps_str"], duration=pr["vdur"],
             rows={r.key: dict(ok=r.ok, detail=r.detail, **({"na": r.na_reason} if r.na_reason else {}),
                               **({"value": r.value} if r.value else {})) for r in rows})
    json.dump(d, open(video + STAMP_SUFFIX, "w"), indent=1)
    return video + STAMP_SUFFIX


def require_stamp(video, quiet=False):
    """For callers: raise unless THIS file carries a PASS stamp at THIS gate version."""
    p = video + STAMP_SUFFIX
    if not os.path.exists(p):
        raise SystemExit(f"no delivery-gate stamp: run _shared/deliver/gate.py on {video}")
    d = json.load(open(p))
    if d.get("gate_version") != GATE_VERSION:
        raise SystemExit(f"stamp is gate version {d.get('gate_version')}, this is {GATE_VERSION} "
                         f"-- the standard moved; re-gate the file")
    if d.get("sha256") != C.sha256(video):
        raise SystemExit("stamp is for a different render of this path (sha256 differs)")
    if d.get("verdict") != "PASS":
        raise SystemExit(f"delivery gate verdict on this file is {d.get('verdict')}")
    if not quiet:
        print(f"delivery gate {GATE_VERSION}: PASS ({d.get('format')}, {d.get('when')})")
    return d


# ---------------------------------------------------------------------------- cli
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", nargs="?")
    ap.add_argument("--format", dest="fmt", choices=sorted(FMT.FORMATS))
    ap.add_argument("--plan")
    ap.add_argument("--row", action="append", help="run only these rows (debugging; never delivery)")
    ap.add_argument("--json", help="write the full result here as well as stamping the file")
    ap.add_argument("--no-stamp", action="store_true",
                    help="measure without writing the stamp. For the regression corpus, which must "
                         "never change a file's delivery state -- NOT for a delivery run")
    ap.add_argument("--audit", action="store_true", help="every format answers for every row")
    ap.add_argument("--formats", action="store_true")
    ap.add_argument("--plan-keys", action="store_true")
    A_ = ap.parse_args()

    if A_.plan_keys:
        print(PLAN_KEYS)
        return 0
    if A_.formats:
        for n, f in sorted(FMT.FORMATS.items()):
            print(f"\n{n}\n  {f['note']}")
        return 0
    if A_.audit:
        holes = FMT.audit()
        for n, h in holes.items():
            for r in h["unconfigured"]:
                print(f"  UNCONFIGURED   {n:14s} {r}")
            for r in h["contradictory"]:
                print(f"  CONTRADICTORY  {n:14s} {r}  (both configured and declared n/a)")
        print(f"\n{len(FMT.ALL_ROWS)} rows x {len(FMT.FORMATS)} formats; "
              f"{'every format answers for every row' if not holes else f'{len(holes)} format(s) with holes'}")
        return 1 if holes else 0

    if not A_.video or not A_.fmt:
        ap.error("a video and --format are required (or use --audit / --formats / --plan-keys)")
    if not os.path.exists(A_.video):
        raise SystemExit(f"not on disk: {A_.video}")

    t0 = time.time()
    pr, plan, rows = run(A_.video, A_.fmt, A_.plan, set(A_.row) if A_.row else None)
    v, fails, unmeasured, pending = verdict(rows)

    print(f"\nDELIVERY GATE {GATE_VERSION}   {os.path.basename(A_.video)}")
    print(f"  format {A_.fmt}   {pr['size']} @ {pr['fps_str']}   {C.mmss(pr['vdur'])}"
          f"   plan {os.path.basename(A_.plan) if A_.plan else 'NONE'}\n")
    for r in rows:
        print(f"  {r.tag}  {r.key:28s} {r.detail}")
    print(f"\n  {sum(1 for r in rows if r.passed)} passed, {len(fails)} failed, "
          f"{len(unmeasured)} NOT MEASURED, {len(pending)} pending, "
          f"{sum(1 for r in rows if r.na_reason)} declared not applicable")
    if pending:
        print("  ⚠ a PENDING row is not a pass: " + ", ".join(r.key for r in pending))
    if A_.row:
        print("  ⚠ --row was used: this is a partial run and must not be treated as a verdict")

    if not A_.no_stamp and not A_.row:
        print(f"  stamp -> {os.path.basename(stamp(A_.video, A_.fmt, rows, v, pr))}")
    if A_.json:
        json.dump(dict(gate_version=GATE_VERSION, format=A_.fmt, verdict=v,
                       rows=[dict(key=r.key, ok=r.ok, detail=r.detail, value=r.value,
                                  na=r.na_reason) for r in rows]),
                  open(A_.json, "w"), indent=1)
    print(f"\nDELIVERY GATE {v}   ({time.time()-t0:.0f}s)\n")
    return 0 if v == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
