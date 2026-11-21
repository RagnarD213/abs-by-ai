#!/usr/bin/env python3
"""THE PICTURE REFERENCE -- Muhammad's two finished 16:9 edits, pinned by fingerprint, measured with
the delivery gate's OWN instruments, with a LOW and a HIGH for every number.

  python3 picture_ref.py build                       measure both masters, write picture.json
  python3 picture_ref.py check <file> --format F     measure one file, report each number vs lo/hi
                                                     [--beats beats.py --beats-cwd DIR] adds the hand-count rows
  python3 picture_ref.py prove                       both masters pass every bound; ad1-vertical-attempt1
                                                     fails push_spread and naked_splices (writes picture_proof.json)

WHY THIS FILE EXISTS (VQC-C item 6 / engine Phase 4 step 0, 2026-09-16). `_shared/audio/reference/
reference.json` pins Muhammad's AUDIO by sha256 and every audio bound is measured against it. There was
no picture equivalent: "The Muhammad Standard" (2026-09-11) measured the gap between his edits and
our from-raw builds by hand (21.7 / 18.7 picture changes per minute against 9.5 / 8.9) and the number
lived in a report. This file is where the kit (`shortad-from-longform/reference/kit9x16/`) reads his
pacing, his insert coverage, his push schedule, his same-scene cut rate and his talking-head luma from.

THE THREE RULES
  1 THE NUMBERS ARE THE GATE'S NUMBERS. Every automatic row here calls the same function
    `_shared/deliver/gate.py` calls (checks/picture.py, checks/framing.py, watch.py), with the same
    decode settings, so a kit that targets these values is targeting what the gate will measure.
  2 EVERY NUMBER HAS lo AND hi. Dan called the dereverb that went PAST Muhammad's early decay
    "underwater" (memory `audio-never-over-strip`). Overshooting a reference is a warning, not a win.
    lo/hi = [min - margin, max + margin] over the two edits, margin = max(0.5 x (max - min),
    0.10 x mean), floored at 0 -- the dispersion of two edits plus a tenth of their mean, so a number
    the two edits agree on still carries a readable band. `defect_side` says which side a build's
    departure is a defect on and which side is the overshoot warning.
  3 THIS IS A REFERENCE, NOT A GATE. It is not registered in the regression corpus and it adds no row
    to formats.py; the kit consumes it and `check` reports against it. The bounds that BLOCK a file
    stay in formats.py, beside the files they were measured on.

The hand-count rows (graphic density, insert coverage by beat, his pushes and flashes) come from the
beat sheets that were read off his frames one second at a time (`shortad-from-longform/reference/
beats.py` for Ad 1, `/Volumes/Extreme/_edit_work/ad2-vert-v2/beats.py` for Ad 2); their timestamps
are written into picture.json so `check` never needs the build dirs again.
"""
import argparse
import datetime
import importlib.util
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))                     # _shared/reference
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))            # .claude/skills
from _shared.deliver import common as C                               # noqa: E402
from _shared.deliver import formats as FMT                            # noqa: E402
from _shared.deliver import watch as W                                # noqa: E402
from _shared.deliver.checks import framing as FR                      # noqa: E402
from _shared.deliver.checks import picture as PIC                     # noqa: E402

REPO = C.REPO
OUT = os.path.join(HERE, "picture.json")
PROOF = os.path.join(HERE, "picture_proof.json")
VERSION = 1
SSD = "/Volumes/Extreme/_edit_work"

MASTERS = {
    "ad1": dict(path=os.path.join(REPO, "Muhammad Ad Videos/this picture got me abs - ad 1/"
                                        "this picture got me abs | muhammad | 16x9 | ad 1.mp4"),
                beats=os.path.join(REPO, ".claude/skills/shortad-from-longform/reference/beats.py"),
                beats_cwd=os.path.join(SSD, "ad1-8-14/vert9x16"),
                beats_note="his cut stepped at 1 s (233 contact-sheet frames, boundaries pinned to a "
                           "10 fps frame-difference peak); the only deviations are the banned "
                           "before/after card cut sequentially and the app recording capped at 25 s"),
    "ad2": dict(path=os.path.join(REPO, "Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/"
                                        "stop wasting money on nutritionists | muhammad | 16x9 | ad 2.mp4"),
                beats=os.path.join(SSD, "ad2-vert-v2/beats.py"),
                beats_cwd=os.path.join(SSD, "ad2-vert-v2"),
                beats_note="his V2 beat sheet, boundaries read at the frame off his render; pushes from "
                           "the per-0.25 s framing fit of his own render (cover.json)"),
}
ATTEMPT1 = dict(path=os.path.join(SSD, "ad1-8-14/vert9x16/ad1_vertical_59s.mp4"), fmt="ad9x16",
                corpus_id="ad1-vertical-attempt1", dan="truly awful... definitely won't work.")
FORMAT_OF_MASTERS = "ad16x9"

TEXT_KINDS = ("window", "title", "stmt")           # base-layer plates that carry words
INSERT_KINDS = ("card", "bleed", "bleed2", "winmedia")
OVERLAY_TEXT = ("lt", "cta")

# defect_side: which side of the band a departure is a DEFECT on. The other side is the overshoot
# warning ("past the target").
NUMBERS = {
    "change_rate_per_min": dict(unit="/min", side="low",
                                instrument="checks/picture.py change_events (6 fps, 64x36 gray, med+6*MAD) -- style:change_rate"),
    "coverage": dict(unit="fraction", side="low",
                     instrument="checks/picture.py palette distance > 0.12 (2 fps, 48x27) -- style:coverage"),
    "static_run_s": dict(unit="s", side="high",
                         instrument="checks/picture.py longest gap between change_events -- style:static_run"),
    "naked_splices_per_min": dict(unit="/min", side="both",
                                  instrument="watch.py naked_splices (native rate, peak block + alignment test), no plan -- cut:naked_splices; HIS pose-matched same-scene cuts, a range not a defect"),
    "push_spread": dict(unit="x", side="low",
                        instrument="checks/framing.py push_coverage spread of per-hold median head heights -- framing:push_coverage"),
    "push_off_frac": dict(unit="fraction", side="low",
                          instrument="checks/framing.py push_coverage: fraction of talk >= 6 % off the dominant level"),
    "pushed_holds_per_min": dict(unit="/min", side="low",
                                 instrument="checks/framing.py talk_holds: holds >= 6 % off the dominant level, per minute"),
    "events_per_min": dict(unit="/min", side="low",
                           instrument="watch.py analyse merged events (p99 / med+6*MAD threshold, merged inside 0.4 s), no plan"),
    "shot_len_median_s": dict(unit="s", side="high",
                              instrument="watch.py merged events: median gap between consecutive events"),
    "shot_len_p90_s": dict(unit="s", side="high",
                           instrument="watch.py merged events: 90th-percentile gap"),
    "shot_len_max_s": dict(unit="s", side="high",
                           instrument="watch.py merged events: longest gap"),
    "talking_head_luma": dict(unit="0-255", side="both",
                              instrument="watch.py scan: median frame-mean gray (160x90) over ON-SCENE frames (palette distance <= 0.12 from the programme median)"),
    "on_scene_frac": dict(unit="fraction", side="high",
                          instrument="watch.py scan: fraction of frames on the main scene (palette distance <= 0.12)"),
    "opening_changes_15s": dict(unit="count", side="low",
                                instrument="checks/picture.py change_events in the first 15 s (the ramp's opening)"),
    "closing_changes_15s": dict(unit="count", side="low",
                                instrument="checks/picture.py change_events in the last 15 s"),
    # hand-count rows (need a beat sheet)
    "graphics_per_min": dict(unit="/min", side="both", hand=True,
                             instrument="hand count: lower thirds + CTA pills + text plates (window/title/stmt) per minute, off his frames"),
    "lower_thirds_per_min": dict(unit="/min", side="both", hand=True,
                                 instrument="hand count: lower thirds per minute"),
    "cta_count": dict(unit="count", side="both", hand=True, instrument="hand count: CTA pills"),
    "inserts_per_min": dict(unit="/min", side="low", hand=True,
                            instrument="hand count: cards + full-bleed inserts + window-media beats per minute"),
    "insert_coverage_hand": dict(unit="fraction", side="low", hand=True,
                                 instrument="hand count: non-talk time / runtime from the beat sheet"),
    "flashes_per_min": dict(unit="/min", side="both", hand=True,
                            instrument="hand count: white light-leak transitions per minute"),
    "pushes_hand_per_min": dict(unit="/min", side="low", hand=True,
                                instrument="hand count: his zoom pushes (ramp in / hold / ramp out) per minute"),
    "longest_talk_hand_s": dict(unit="s", side="high", hand=True,
                                instrument="hand count: longest talk beat with no insert or text plate"),
}


# ---------------------------------------------------------------------------- beat sheets
def load_beats(path, cwd):
    """Import a build's beats.py with the cwd it expects (they read m.whisper.json / cover.json)."""
    here = os.getcwd()
    os.chdir(cwd)
    try:
        spec = importlib.util.spec_from_file_location("beats_" + os.path.basename(cwd).replace("-", "_"), path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        os.chdir(here)
    return mod


def hand_count(mod, dur):
    """Counts and timestamps off a beat sheet that was read off his frames."""
    tl, ov = mod.timeline()
    rows = dict(text_plates=[], inserts=[], lower_thirds=[], ctas=[], talk=[])
    for b in tl:
        k = b["kind"]
        det = b.get("media") or b.get("media_a") or b.get("header") or b.get("headline") or ""
        if k in TEXT_KINDS:
            rows["text_plates"].append([round(b["t0"], 2), round(b["t1"], 2), k, str(det)[:40]])
        elif k in INSERT_KINDS:
            rows["inserts"].append([round(b["t0"], 2), round(b["t1"], 2), k, str(det)[:40]])
        elif k == "talk":
            rows["talk"].append([round(b["t0"], 2), round(b["t1"], 2)])
    for o in ov:
        if o["kind"] == "lt":
            rows["lower_thirds"].append([round(o["t0"], 2), round(o["t1"], 2), " / ".join(o.get("lines", []))[:60]])
        elif o["kind"] == "cta":
            rows["ctas"].append([round(o["t0"], 2), round(o["t1"], 2)])
    pushes = [list(p) for p in getattr(mod, "PUSHES", [])]
    flashes = [list(f) for f in getattr(mod, "FLASHES", [])]
    non_talk = sum(b - a for a, b, *_ in rows["inserts"] + rows["text_plates"])
    longest_talk = max((b - a for a, b in rows["talk"]), default=0.0)
    mins = dur / 60.0
    nums = dict(
        graphics_per_min=(len(rows["lower_thirds"]) + len(rows["ctas"]) + len(rows["text_plates"])) / mins,
        lower_thirds_per_min=len(rows["lower_thirds"]) / mins,
        cta_count=len(rows["ctas"]),
        inserts_per_min=len(rows["inserts"]) / mins,
        insert_coverage_hand=non_talk / dur,
        flashes_per_min=len(flashes) / mins,
        pushes_hand_per_min=len(pushes) / mins,
        longest_talk_hand_s=longest_talk,
    )
    return nums, dict(rows, pushes=pushes, flashes=flashes, push_z=getattr(mod, "PUSH_Z", None))


# ---------------------------------------------------------------------------- measuring
def measure(video, fmt, quiet=False):
    """Every automatic number, with the gate's own functions. Returns (numbers, extras)."""
    t0 = time.time()
    say = (lambda *a: None) if quiet else (lambda *a: print(*a, flush=True))
    pr = C.probe(video)
    pic = PIC.Picture(video, pr["vdur"], pr["fps"], pr["width"], pr["height"])
    cfg = FMT.config_for(fmt)["rows"]
    plan = {"_sha256": None, "_dir": os.path.dirname(os.path.abspath(video))}
    dur = pic.dur
    m, x = {}, {}

    r = PIC.change_rate("style:change_rate", pic, cfg["style:change_rate"], plan)
    m["change_rate_per_min"] = r.value.get("per_min")
    r = PIC.coverage("style:coverage", pic, cfg["style:coverage"], plan)
    m["coverage"] = r.value.get("coverage")
    r = PIC.static_run("style:static_run", pic, cfg["style:static_run"], plan)
    m["static_run_s"] = r.value.get("worst")
    ev = pic.change_events()
    m["opening_changes_15s"] = int(sum(1 for t in ev if t <= 15.0))
    m["closing_changes_15s"] = int(sum(1 for t in ev if t >= dur - 15.0))
    nb = int(np.ceil(dur / 10.0))
    per10 = [0] * nb
    for t in ev:
        per10[min(nb - 1, int(t // 10))] += 1
    dec = [0] * 10
    for t in ev:
        dec[min(9, int(10 * t / dur))] += 1
    x["ramp"] = dict(per_10s=per10, deciles=dec, changes=len(ev))
    say(f"  change events {len(ev)} = {m['change_rate_per_min']:.2f}/min; coverage {m['coverage']:.3f}; "
        f"static run {m['static_run_s']:.1f}s")

    sc = pic.stream()
    rep = W.analyse(sc, [], [])
    jumps = sorted(e["t"] for e in rep["jumps"])
    edges = [0.0] + jumps + [dur]
    gaps = np.diff(edges)
    m["events_per_min"] = len(jumps) / (dur / 60.0)
    m["shot_len_median_s"] = float(np.median(gaps)) if len(gaps) else dur
    m["shot_len_p90_s"] = float(np.percentile(gaps, 90)) if len(gaps) else dur
    m["shot_len_max_s"] = float(gaps.max()) if len(gaps) else dur
    x["shot_lengths"] = dict(n=int(len(gaps)), p10=round(float(np.percentile(gaps, 10)), 2),
                             p50=round(m["shot_len_median_s"], 2), p90=round(m["shot_len_p90_s"], 2),
                             max=round(m["shot_len_max_s"], 2), events=[round(t, 2) for t in jumps])
    H = sc["hist"]
    pal = np.abs(H - np.median(H, axis=0)).sum(1) / 2.0
    on = pal <= FR.SCENE_D
    lum = sc["lum"]
    m["on_scene_frac"] = float(on.mean())
    m["talking_head_luma"] = float(np.median(lum[on])) if on.any() else None
    x["luma"] = dict(on_scene_median=m["talking_head_luma"],
                     on_scene_mean=round(float(lum[on].mean()), 2) if on.any() else None,
                     all_median=round(float(np.median(lum)), 2))
    say(f"  watch events {len(jumps)} = {m['events_per_min']:.2f}/min; shot median {m['shot_len_median_s']:.2f}s "
        f"p90 {m['shot_len_p90_s']:.2f}s max {m['shot_len_max_s']:.2f}s; on-scene {m['on_scene_frac']:.2f}; "
        f"luma {m['talking_head_luma']}")

    r = PIC.naked_splices("cut:naked_splices", pic, cfg["cut:naked_splices"], plan)
    m["naked_splices_per_min"] = r.value.get("per_min")
    x["naked_splices"] = dict(naked=r.value.get("naked"), candidates=r.value.get("candidates"),
                              times=r.value.get("times"))
    say(f"  naked splices {r.value.get('naked')} of {r.value.get('candidates')} = {m['naked_splices_per_min']}/min")

    r = FR.push_coverage("framing:push_coverage", pic, cfg["framing:push_coverage"], plan)
    m["push_spread"] = r.value.get("spread")
    m["push_off_frac"] = r.value.get("off_frac")
    x["push_coverage"] = dict(detail=r.detail, holds=r.value.get("holds"), dominant_frac=r.value.get("dominant_frac"))
    tr = getattr(pic, "_framing", None)
    m["pushed_holds_per_min"] = None
    if tr is not None and tr.valid() and r.value.get("dominant_frac"):
        hs = FR.talk_holds(pic, tr)
        dom = float(r.value["dominant_frac"])
        lo_r, hi_r = cfg["framing:push_coverage"]["push_ratio"]
        meds = [float(np.median([s["hh_frac"] for s in h])) for h in hs]
        same = [(h, md) for h, md in zip(hs, meds) if lo_r <= md / dom <= hi_r]
        pushed = [(round(h[0]["t"], 2), round(h[-1]["t"], 2), round(md / dom, 3))
                  for h, md in same if abs(md / dom - 1.0) >= 0.06]
        m["pushed_holds_per_min"] = len(pushed) / (dur / 60.0)
        x["pushed_holds"] = pushed
        x["talk_hold_levels"] = [(round(h[0]["t"], 2), round(md, 4)) for h, md in same]
    say(f"  push spread x{m['push_spread']} off {m['push_off_frac']} pushed holds {m['pushed_holds_per_min']}/min"
        f"   ({r.detail[:90]})")
    x["seconds"] = round(time.time() - t0, 1)
    x["probe"] = dict(size=pr["size"], fps=pr["fps_str"], duration=pr["vdur"])
    return m, x


def band(vals):
    v = [float(a) for a in vals if a is not None]
    if not v:
        return None, None
    lo_, hi_ = min(v), max(v)
    margin = max(0.5 * (hi_ - lo_), 0.10 * (sum(v) / len(v)))
    return max(0.0, lo_ - margin), hi_ + margin


def compare(ref, m, fmt=None):
    """(key, value, lo, hi, status) for every reference number a measurement carries.
    status: PASS | DEFECT (outside on the defect side) | OVERSHOOT (outside on the warning side)."""
    out = []
    for k, spec in ref["numbers"].items():
        v = m.get(k)
        lo_, hi_ = spec["lo"], spec["hi"]
        if v is None:
            out.append((k, None, lo_, hi_, "NOT MEASURED"))
            continue
        v = float(v)
        side = spec["defect_side"]
        if lo_ <= v <= hi_:
            st = "PASS"
        elif v < lo_:
            st = "DEFECT" if side in ("low", "both") else "OVERSHOOT"
        else:
            st = "DEFECT" if side in ("high", "both") else "OVERSHOOT"
        out.append((k, v, lo_, hi_, st))
    return out


def fmt_val(v):
    return "n/a" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v))


def report(rows, title):
    print(f"\n{title}")
    for k, v, lo_, hi_, st in rows:
        print(f"  {st:12s} {k:26s} {fmt_val(v):>9s}   [{lo_:.3f} .. {hi_:.3f}]")
    n = dict(PASS=0, DEFECT=0, OVERSHOOT=0)
    n["NOT MEASURED"] = 0
    for r in rows:
        n[r[4]] += 1
    print(f"  {n['PASS']} in range, {n['DEFECT']} DEFECT, {n['OVERSHOOT']} overshoot warning(s), "
          f"{n['NOT MEASURED']} not measured")
    return n


# ---------------------------------------------------------------------------- commands
def build(args):
    today = datetime.date.today().isoformat()
    sources, meas, extras, hands, hand_rows = {}, {}, {}, {}, {}
    for key, spec in MASTERS.items():
        p = spec["path"]
        if not os.path.exists(p):
            raise SystemExit(f"master not on disk: {p}")
        print(f"\n[{key}] {os.path.basename(p)}")
        pr = C.probe(p)
        sources[key] = dict(path=os.path.relpath(p, REPO), sha256=C.sha256(p), bytes=os.path.getsize(p),
                            size=pr["size"], fps=pr["fps_str"], duration=pr["vdur"])
        meas[key], extras[key] = measure(p, FORMAT_OF_MASTERS)
        mod = load_beats(spec["beats"], spec["beats_cwd"])
        hands[key], hand_rows[key] = hand_count(mod, pr["vdur"])
        hand_rows[key]["source"] = spec["beats"]
        hand_rows[key]["note"] = spec["beats_note"]
        print(f"  hand count: {hands[key]['graphics_per_min']:.2f} graphics/min, "
              f"{hands[key]['inserts_per_min']:.2f} inserts/min, coverage {hands[key]['insert_coverage_hand']:.2f}, "
              f"{hands[key]['pushes_hand_per_min']:.2f} pushes/min, longest talk {hands[key]['longest_talk_hand_s']:.1f}s")
    numbers = {}
    for k, spec in NUMBERS.items():
        vals = {key: (hands[key][k] if spec.get("hand") else meas[key][k]) for key in MASTERS}
        lo_, hi_ = band(vals.values())
        numbers[k] = dict(
            **{key: (round(v, 4) if isinstance(v, float) else v) for key, v in vals.items()},
            lo=round(lo_, 4) if lo_ is not None else None, hi=round(hi_, 4) if hi_ is not None else None,
            unit=spec["unit"], defect_side=spec["side"], instrument=spec["instrument"],
            measured_on=dict(files=[sources[key]["path"] for key in MASTERS], date=today,
                             format=FORMAT_OF_MASTERS if not spec.get("hand") else "beat sheet"))
    ref = dict(
        name="picture reference -- Muhammad's finished 16:9 edits (Ad 1 + Ad 2)",
        version=VERSION, built=today, gate_version=__import__("_shared.deliver.gate", fromlist=["GATE_VERSION"]).GATE_VERSION,
        window="the whole runtime of each master",
        rule="lo/hi = [min - margin, max + margin] over the two edits, margin = max(0.5*(max-min), 0.10*mean), "
             "floored at 0. defect_side names the side a departure is a defect on; the other side is the "
             "overshoot warning (memory audio-never-over-strip: past the target is not a win).",
        sources=sources, numbers=numbers,
        ramp={key: extras[key]["ramp"] for key in MASTERS},
        shot_lengths={key: extras[key]["shot_lengths"] for key in MASTERS},
        luma={key: extras[key]["luma"] for key in MASTERS},
        push_coverage={key: dict(extras[key]["push_coverage"], pushed_holds=extras[key].get("pushed_holds"),
                                 talk_hold_levels=extras[key].get("talk_hold_levels")) for key in MASTERS},
        naked_splices={key: extras[key]["naked_splices"] for key in MASTERS},
        hand_count=hand_rows,
        measure_seconds={key: extras[key]["seconds"] for key in MASTERS},
    )
    json.dump(ref, open(OUT, "w"), indent=1)
    print(f"\n-> {OUT}")
    for k, n in numbers.items():
        print(f"  {k:26s} ad1 {fmt_val(n['ad1']):>9s}  ad2 {fmt_val(n['ad2']):>9s}   lo {n['lo']:.3f}  hi {n['hi']:.3f}  ({n['defect_side']})")
    return 0


def load_ref():
    if not os.path.exists(OUT):
        raise SystemExit(f"{OUT} does not exist: run `picture_ref.py build` first")
    ref = json.load(open(OUT))
    for key, s in ref["sources"].items():
        p = os.path.join(REPO, s["path"])
        if os.path.exists(p) and C.sha256(p) != s["sha256"]:
            raise SystemExit(f"{key}: {p} is not the pinned master (sha256 differs) -- rebuild or restore it")
    return ref


def check(args):
    ref = load_ref()
    m, x = measure(args.video, args.fmt)
    if args.beats:
        mod = load_beats(args.beats, args.beats_cwd or os.path.dirname(os.path.abspath(args.beats)))
        h, _ = hand_count(mod, x["probe"]["duration"])
        m.update(h)
    rows = compare(ref, m)
    n = report(rows, f"picture reference v{ref['version']} -- {os.path.basename(args.video)} as {args.fmt}")
    if args.json:
        json.dump(dict(video=os.path.abspath(args.video), sha256=C.sha256(args.video), format=args.fmt,
                       numbers=m, rows=[dict(key=k, value=v, lo=lo_, hi=hi_, status=st) for k, v, lo_, hi_, st in rows],
                       extras=x), open(args.json, "w"), indent=1)
    return 1 if n["DEFECT"] else 0


def prove(args):
    """The proof the handoff asks for: both his edits pass every bound derived from them (re-measured,
    not read back), and the rejected ad1-vertical-attempt1 fails at least push_spread and
    naked_splices."""
    ref = load_ref()
    result = dict(reference_version=ref["version"], when=datetime.datetime.now().isoformat(timespec="seconds"), files={})
    ok = True
    for key, spec in MASTERS.items():
        p = spec["path"]
        print(f"\n[{key}] re-measuring {os.path.basename(p)}")
        m, x = measure(p, FORMAT_OF_MASTERS)
        mod = load_beats(spec["beats"], spec["beats_cwd"])
        h, _ = hand_count(mod, x["probe"]["duration"])
        m.update(h)
        rows = compare(ref, m)
        n = report(rows, f"{key}: Muhammad's master must PASS every number")
        bad = [r for r in rows if r[4] in ("DEFECT", "OVERSHOOT", "NOT MEASURED")]
        result["files"][key] = dict(path=p, sha256=C.sha256(p), verdict="PASS" if not bad else "FAIL",
                                    rows=[dict(key=k, value=v, status=st) for k, v, _, _, st in rows])
        if bad:
            ok = False
            print(f"  ✗ {key}: {[r[0] for r in bad]}")
    p = ATTEMPT1["path"]
    print(f"\n[attempt1] {os.path.basename(p)}  (corpus {ATTEMPT1['corpus_id']}: Dan -- {ATTEMPT1['dan']!r})")
    m, x = measure(p, ATTEMPT1["fmt"])
    rows = compare(ref, m)
    report(rows, "ad1-vertical-attempt1: the rejected cut must FAIL push_spread and naked_splices")
    st = {k: s for k, _, _, _, s in rows}
    must = {"push_spread": "DEFECT", "naked_splices_per_min": "DEFECT"}
    fails = {k: st.get(k) for k in must}
    got = all(st.get(k) == v for k, v in must.items())
    result["files"]["attempt1"] = dict(path=p, sha256=C.sha256(p), format=ATTEMPT1["fmt"],
                                       required_failures=must, observed=fails,
                                       verdict="FAIL as required" if got else "DID NOT FAIL AS REQUIRED",
                                       rows=[dict(key=k, value=v, status=s) for k, v, _, _, s in rows])
    if not got:
        ok = False
        print(f"  ✗ attempt1 did not fail where it must: {fails}")
    else:
        others = [k for k, s in st.items() if s == "DEFECT" and k not in must]
        print(f"  ✓ attempt1 fails push_spread and naked_splices; also outside on: {others}")
    result["verdict"] = "PROVEN" if ok else "NOT PROVEN"
    json.dump(result, open(PROOF, "w"), indent=1)
    print(f"\nPICTURE REFERENCE {result['verdict']}   -> {PROOF}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    c = sub.add_parser("check")
    c.add_argument("video")
    c.add_argument("--format", dest="fmt", required=True, choices=sorted(FMT.FORMATS))
    c.add_argument("--beats", help="a beats.py to add the hand-count rows")
    c.add_argument("--beats-cwd")
    c.add_argument("--json")
    sub.add_parser("prove")
    a = ap.parse_args()
    return dict(build=build, check=check, prove=prove)[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
