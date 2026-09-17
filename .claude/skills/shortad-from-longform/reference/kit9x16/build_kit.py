#!/usr/bin/env python3
"""BUILD THE 9:16 AD FROM THE KIT: template.json (his grammar) + content.json (WHAT goes where) + the
audio EDL (the cut) -> beats.json, edl_picture.json, piccuts.json, kit_report.json, and a `beats.py`
shim in the build dir that render.py / captions.py / mux.py / the plan builder import unchanged.

  python3 build_kit.py --from-master --build DIR --edl edl_final.json --content content.json --words WORDS
                       --reference his.mp4 --raw ROLL --grade grade.py [--rolls rolls.json] [--piccuts existing.json]
  python3 build_kit.py --from-raw    --build DIR --edl edl.json       --content content.json --words WORDS
                       --raw ROLL --grade grade.py [--rolls rolls.json] [--piccuts existing.json]
  python3 build_kit.py ... --plan-only        (no frame extraction: pushes/flashes/overlays from the content only)

WHAT THE KIT DECIDES (the design) and WHAT IT IS TOLD (the content):
  content.json says which insert, plate, lower third and CTA go with which words. The kit decides every
  time and every device around them the way his edits do: the picture cut at every talk splice
  (cut_rules.md), the push schedule (ramps that cover what the cut cannot match and keep the talking
  head from being one fixed crop), the light-leak on every insert -> talk return, lower-third and CTA
  timing against the words, caption suppression, chip placement by measurement. Every number comes
  from template.json, which cites _shared/reference/picture.json, and the generated design is scored
  against picture.json's lo/hi BEFORE anything renders (kit_report.json). A design outside his range
  is reported, never silently shipped -- and never fixed by moving the range.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
PICREF = os.path.join(REPO, ".claude/skills/_shared/reference/picture.json")
FPS = 30000 / 1001
TEXT_KINDS = ("window", "title", "stmt")
INSERT_KINDS = ("card", "bleed", "bleed2", "winmedia")
BASE_KINDS = ("talk", "window", "card", "title", "stmt", "bleed", "bleed2", "winmedia")

_n = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


# ---------------------------------------------------------------------------- inputs
def load_words(path):
    """-> [{w, t, e}] from m.whisper.json (segments/words), words_ctc.json ([{word,start,end}]) or [{w,t,e}]."""
    d = json.load(open(path))
    out = []
    if isinstance(d, dict) and "segments" in d:
        for s in d["segments"]:
            for w in s.get("words", []):
                if w["word"].strip():
                    out.append(dict(w=w["word"].strip(), t=float(w["start"]), e=float(w["end"])))
    else:
        for w in d:
            if "w" in w:
                out.append(dict(w=w["w"], t=float(w["t"]), e=float(w["e"])))
            elif "word" in w:
                out.append(dict(w=w["word"].strip(), t=float(w["start"]), e=float(w["end"])))
    return out


class Anchors:
    def __init__(self, words):
        self.W = [(_n(w["w"]), w["t"], w["e"]) for w in words if _n(w["w"])]

    _ALIAS = {"gonna": "goingto", "wanna": "wantto", "youd": "youwould", "200": "twohundred", "38": "thirtyeight"}

    def _seq(self, phrase, after=0.0):
        """The words that say `phrase`, at or after `after`. Exact first; then FUZZY: two transcripts of two
        takes of one script disagree in small ways ("I'm going to" / "I'm gonna"), so the earliest window whose
        tokens agree on >= 2/3 of the phrase (order kept) is taken. A phrase nothing resembles is an error."""
        toks = [_n(t) for t in phrase.split() if _n(t)]
        n = len(toks)
        for i in range(len(self.W)):
            if self.W[i][1] < after:
                continue
            if [w[0] for w in self.W[i:i + n]] == toks:
                return i, n
        import difflib
        want = "".join(self._ALIAS.get(t, t) for t in toks)
        best = (0.0, None, n)
        for i in range(len(self.W)):
            if self.W[i][1] < after:
                continue
            for m in (n, n - 1, n + 1):
                if m < 1 or i + m > len(self.W):
                    continue
                got = "".join(self._ALIAS.get(w[0], w[0]) for w in self.W[i:i + m])
                r = difflib.SequenceMatcher(None, want, got).ratio()
                if r >= 0.80:
                    return i, m                                   # the EARLIEST good window wins
                if r > best[0]:
                    best = (r, i, m)
        if best[1] is not None and best[0] >= 0.66:
            return best[1], best[2]
        raise SystemExit(f"content phrase not found after {after:.2f}s: {phrase!r} (best similarity {best[0]:.2f})")

    def at(self, phrase, after=0.0):
        i, _ = self._seq(phrase, after)
        return self.W[i][1]

    def end(self, phrase, after=0.0):
        i, n = self._seq(phrase, after)
        return self.W[i + n - 1][2]


def load_edl(path):
    E = json.load(open(path))
    out = []
    for i, s in enumerate(E):
        if "cut_in" in s:
            out.append(dict(i=i, cut_in=float(s["cut_in"]), cut_out=float(s["cut_out"]), src_in=float(s["src_in"]),
                            src_out=float(s.get("src_out", s["src_in"] + s["cut_out"] - s["cut_in"])), roll=s.get("roll")))
        else:
            a, b = s["out_seconds"]
            out.append(dict(i=i, cut_in=float(a), cut_out=float(b), src_in=float(s["src_in"]), src_out=float(s["src_out"]), roll=s.get("roll")))
    return out


def ref_number(ref, key):
    n = ref["numbers"].get(key)
    return (n["lo"], n["hi"], n.get("defect_side", "both")) if n else (None, None, None)


# ---------------------------------------------------------------------------- resolving content
def resolve_times(item, A, last_t):
    """t0/t1 from `t0`/`t1`, or from `at`/`until` phrases (+ pads), disambiguated after the previous item."""
    if "t0" in item and "t1" in item:
        return float(item["t0"]), float(item["t1"])
    after = float(item.get("after", max(0.0, last_t - 2.0)))
    t0 = A.at(item["at"], after) - float(item.get("pad_pre", 0.0))
    t1 = A.end(item.get("until", item["at"]), after) + float(item.get("pad_post", 0.0))
    if "dur" in item:
        t1 = t0 + float(item["dur"])
    return round(max(0.0, t0), 3), round(t1, 3)


def make_timeline(beats, dur):
    base = sorted([dict(b) for b in beats if b["kind"] in BASE_KINDS], key=lambda b: b["t0"])
    fixed, t = [], 0.0
    for b in base:
        b["t0"] = max(b["t0"], t)
        if b["t1"] - b["t0"] < 0.20:
            continue
        gap = b["t0"] - t
        if gap > 0.40:
            fixed.append(dict(kind="talk", t0=round(t, 3), t1=round(b["t0"], 3)))
        elif gap > 0:
            b["t0"] = t
        fixed.append(b)
        t = b["t1"]
    if dur - t > 0.10:
        fixed.append(dict(kind="talk", t0=round(t, 3), t1=dur))
    return fixed


# ---------------------------------------------------------------------------- the grammar
def flashes_for(tl, T):
    """A light-leak on every insert -> talk return (his rule), the content cut on the peak."""
    pre, dur, gap = T["flash"]["pre_s"], T["flash"]["dur_s"], T["flash"]["min_spacing_s"]
    out = []
    frm = tuple(T["flash"].get("on_return_from", ["card", "window", "title", "stmt", "winmedia"]))
    for i in range(1, len(tl)):
        if tl[i]["kind"] == "talk" and (tl[i - 1]["kind"] in frm or tl[i - 1].get("flash_after")) and tl[i]["t1"] - tl[i]["t0"] >= 0.6:
            c = tl[i]["t0"]
            if out and c - (out[-1][0] + pre) < gap:
                continue
            out.append((round(c - pre, 3), round(c - pre + dur, 3)))
    return out


def pushes_for(tl, splices, cover, words, T, flashes):
    """His push schedule, generated: a push covers every splice the cut rule could not match (ramp
    leading the cut by `lead_before_cut_s`), then every talk run is filled so no stretch of talk goes
    longer than `max_gap_s` without a push; pushes start on a sentence boundary when one is within
    1.5 s, hold 1.5-3.5 s cycling, ramp in 0.5 s, ramp out 0.5-0.8 s; never inside `min_gap_to_flash_s`
    of a flash; the first talk beat opens already punched when the template says so."""
    P = T["push"]
    holds = list(P["hold_s"]) if isinstance(P["hold_s"], list) else [P["hold_s"]]
    outs = list(P["ramp_out_s"]) if isinstance(P["ramp_out_s"], list) else [P["ramp_out_s"]]
    rin, lead, gap = P["ramp_in_s"], P["lead_before_cut_s"], P["max_gap_s"]
    fl_guard = P.get("min_gap_to_flash_s", 0.3)
    sents = sorted(w["e"] for w in words if w["w"].rstrip().endswith((".", "?", "!", ",")))
    flash_pts = [a + T["flash"]["pre_s"] for a, b in flashes]

    def near_flash(t):
        return any(abs(t - f) < fl_guard for f in flash_pts)

    def snap_sentence(t, lo, hi):
        c = [s for s in sents if lo <= s <= hi and abs(s - t) <= 1.5]
        return min(c, key=lambda s: abs(s - t)) if c else t

    pushes, n = [], 0
    talk = [b for b in tl if b["kind"] == "talk"]
    splices_all = list(splices)
    steps = []
    if T["cut"].get("step_every_bare_cut"):
        # THE ZOOM-CUT SYSTEM (ad-edit Step 3; measured on the kit's first Ad 1 render, 2026-09-16): a ramped
        # push spanning a cut does NOT hide a residual pose jump at the phone's 1.78x -- the judge read eight
        # of them as jump cuts, at similarities 0.46-0.67. So every bare talk-to-talk cut gets a framing
        # LEVEL CHANGE ON THE CUT FRAME: punch in (instant) if the head is at the base level, pull out
        # (instant) if it is inside a punch. Consecutive cuts alternate. Ramped pushes then fill only the
        # stretches with no cut. Reported separately as level steps; they are not his ramped pushes.
        hold_i = 0
        for c in sorted(splices):
            if near_flash(c) or any(abs(c - b["t0"]) < 0.3 or abs(c - b["t1"]) < 0.3 for b in tl):
                continue                                          # a beat boundary or a flash already covers it
            fr = round((round(c * FPS) - 0.5) / FPS, 4)          # half a frame before the cut frame
            live = steps[-1] if steps and steps[-1][0] < fr < steps[-1][3] else None
            if live is not None:
                live[2] = fr; live[3] = fr                        # inside a punch: the cut pulls out, instantly
            else:
                hold = holds[hold_i % len(holds)]; hold_i += 1    # at the base level: the cut punches in, holds, ramps out
                steps.append([fr, fr, round(fr + hold, 4), round(fr + hold + outs[hold_i % len(outs)], 4)])
        # a punch that would run past its beat's end ends with the beat
        for st in steps:
            for b in talk:
                if b["t0"] <= st[0] < b["t1"] and st[3] > b["t1"]:
                    st[2] = min(st[2], round(b["t1"], 4)); st[3] = round(b["t1"], 4)
        pushes.extend(tuple(x) for x in steps)
        n = len(steps)
        splices = [c for c in splices if c in cover and not any(p[0] <= c <= p[3] for p in pushes)]
    if P.get("opens_punched", T["opening"].get("opens_punched")) and talk and talk[0]["t0"] < 0.5:
        b = talk[0]
        end = min(b["t1"], b["t0"] + holds[0] + 1.0)
        pushes.append((0.0, 0.0, round(end - outs[0], 3), round(end, 3)))
        n += 1
    # 1. cover the unmatched splices
    for s in sorted(splices):
        if s not in cover:
            continue
        a1 = round(s - lead, 3)
        if any(p[0] <= s <= p[3] for p in pushes):
            continue
        hold = holds[n % len(holds)]
        ro = outs[n % len(outs)]
        b1 = round(a1 + rin + hold, 3)
        pushes.append((a1, round(a1 + rin, 3), b1, round(b1 + ro, 3)))
        n += 1
    # 2. fill every talk run so no stretch goes longer than max_gap_s without a push
    for b in talk:
        t = b["t0"]
        while b["t1"] - t > gap:
            target = t + gap * 0.75
            if any(p[0] - 1.0 <= target <= p[3] + 1.0 for p in pushes):
                t = max(p[3] for p in pushes if p[0] - 1.0 <= target <= p[3] + 1.0)
                continue
            a1 = snap_sentence(target, b["t0"] + 0.5, b["t1"] - 2.5)
            if near_flash(a1):
                a1 += fl_guard
            hold = holds[n % len(holds)]
            ro = outs[n % len(outs)]
            a2 = round(a1 + rin, 3)
            b1 = round(a2 + hold, 3)
            b2 = round(min(b1 + ro, b["t1"]), 3)
            b1 = min(b1, b2)
            if b2 - a1 < rin + 1.0:
                break
            pushes.append((round(a1, 3), a2, b1, b2))
            n += 1
            t = b2
    pushes.sort()
    # no overlaps: a push that starts inside the previous one is dropped
    clean = []
    for p in pushes:
        if clean and p[0] < clean[-1][3] + 0.4:
            continue
        clean.append(p)
    # 3. top up to HIS count: the reference's pushes per minute (midpoint of lo/hi) times the runtime.
    #    Each extra push goes into the longest stretch of talk with no push, on a sentence boundary.
    dur = tl[-1]["t1"]
    target = int(round(P.get("target_per_min", 3.43) * dur / 60.0))
    guard = 0
    nlike = lambda: sum(1 for p in clean if p[3] > p[2])          # pushes that hold and ramp out (steps that pull out instantly are not pushes)
    while nlike() < target and guard < 40:
        guard += 1
        gaps = []
        for b in talk:
            edges = [b["t0"]] + sorted([q for p in clean for q in (p[0], p[3]) if b["t0"] < q < b["t1"]]) + [b["t1"]]
            for x, y in zip(edges[:-1], edges[1:]):
                if not any(p[0] <= x and y <= p[3] for p in clean):
                    gaps.append((y - x, x, y))
        gaps.sort(reverse=True)
        placed = False
        for ln, x, y in gaps:
            if ln < rin + holds[0] + 0.6:
                break
            a1 = snap_sentence(x + ln * 0.4, x + 0.4, y - (rin + holds[0] + 0.5))
            if near_flash(a1):
                a1 += fl_guard
            hold = holds[n % len(holds)]
            ro = outs[n % len(outs)]
            a2 = round(a1 + rin, 3)
            b1 = round(a2 + hold, 3)
            b2 = round(min(b1 + ro, y), 3)
            b1 = min(b1, b2)
            if b2 - a1 < rin + 1.0 or any(p[0] - 0.4 < b2 and a1 < p[3] + 0.4 for p in clean):
                continue
            clean.append((round(a1, 3), a2, b1, b2))
            n += 1
            placed = True
            break
        if not placed:
            break
    # no framing stub at a beat edge: a punch that would end (or start) within 0.6 s of its talk beat's edge
    # ends (starts) WITH the beat (round 2's gate: a 0.2 s FAR segment at the very end of the film)
    fixed = []
    for p in clean:
        p = list(p)
        for b in talk:
            if b["t0"] <= p[0] < b["t1"]:
                if 0 < b["t1"] - p[3] < 0.6:
                    p[2] = p[3] = round(b["t1"], 4)
                if 0 < p[0] - b["t0"] < 0.6 and p[1] > p[0]:
                    p[0] = p[1] = round(b["t0"], 4)
        fixed.append(tuple(p))
    clean = fixed
    clean.sort()
    # a RAMPED push may not overlap a level step nor contain a bare cut: inside it the zoom is already at the
    # punched level, so the step adds no size change and the cut reads naked (round 2 judge, 147.25 s)
    step_spans = [(p[0], p[3]) for p in clean if p[1] <= p[0]]
    cut_ts = sorted(splices_all)
    out = []
    for p in clean:
        if p[1] > p[0]:
            if any(a - 0.4 < p[3] and p[0] < b + 0.4 for a, b in step_spans) or any(p[0] - 0.2 <= c <= p[3] + 0.2 for c in cut_ts):
                continue
        out.append(p)
    return out


def push_at(t, pushes, z):
    best = 0.0
    for a1, a2, b1, b2 in pushes:
        k = 1.0 if a2 <= a1 else max(0.0, min(1.0, (t - a1) / (a2 - a1)))
        ko = (1.0 if t >= b1 else 0.0) if b2 <= b1 else max(0.0, min(1.0, (t - b1) / (b2 - b1)))
        r = min(k, 1 - ko)
        if t < a1:
            r = 0.0
        best = max(best, r * r * (3 - 2 * r))
    return 1.0 + (z - 1.0) * best


# ---------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--from-master", action="store_true")
    g.add_argument("--from-raw", action="store_true")
    ap.add_argument("--build", required=True)
    ap.add_argument("--template", default=os.path.join(HERE, "template.json"))
    ap.add_argument("--edl", required=True)
    ap.add_argument("--content", required=True)
    ap.add_argument("--words", required=True)
    ap.add_argument("--reference")
    ap.add_argument("--raw")
    ap.add_argument("--rolls")
    ap.add_argument("--grade")
    ap.add_argument("--piccuts", help="reuse an existing piccuts.json instead of extracting frames")
    ap.add_argument("--plan-only", action="store_true")
    a = ap.parse_args()

    T = json.load(open(a.template))
    ref = json.load(open(PICREF)) if os.path.exists(PICREF) else None
    if ref is None:
        raise SystemExit(f"{PICREF} does not exist -- build the picture reference first (step 0)")
    C = json.load(open(a.content))
    E = load_edl(a.edl)
    words = load_words(a.words)
    A = Anchors(words)
    dur = round(E[-1]["cut_out"], 6)
    os.makedirs(a.build, exist_ok=True)

    # ---- content -> base beats and overlays (times resolved against the words)
    beats, last = [], 0.0
    for it in C["beats"]:
        t0, t1 = resolve_times(it, A, last)
        b = {k: v for k, v in it.items() if k not in ("at", "until", "pad_pre", "pad_post", "dur", "after")}
        b.update(t0=t0, t1=min(t1, dur))
        # a CARD with a label kind gets the chip text the plate draws under its hole (plate_card `label`);
        # a full-bleed beat gets its chip PLACED BY MEASUREMENT later (kit_labels.py -> chip_png)
        if b.get("label_kind") and b["kind"] == "card":
            b["label"] = T["labels"]["real"] if b["label_kind"] == "real" else T["labels"]["ai"]
        beats.append(b)
        last = t1
    # carry a VALIDATED chip placement over from the previous beat sheet when the same picture sits on the
    # same beat (kit_labels.py is a segmenter pass per candidate; a re-plan that does not move the beat keeps it)
    prev_sheet = os.path.join(a.build, "beats.json")
    if os.path.exists(prev_sheet):
        old_beats = json.load(open(prev_sheet)).get("beats", [])
        for b in beats:
            for ob in old_beats:
                if ob.get("chip_png") and ob.get("media") == b.get("media") and abs(ob["t0"] - b["t0"]) < 0.02 \
                        and abs(ob["t1"] - b["t1"]) < 0.02 and os.path.exists(ob["chip_png"]):
                    b["chip_png"], b["chip_box"] = ob["chip_png"], ob["chip_box"]
                    if ob.get("chip_label"):
                        b["chip_label"] = ob["chip_label"]
    tl = make_timeline(beats, dur)
    lts, last = [], 0.0
    L = T["lower_third"]
    for it in C.get("lower_thirds", []):
        t0, t1 = resolve_times(it, A, last)
        if "t0" not in it:
            t0 = round(t0 - L["lead_s"], 3)
            t1 = round(min(max(t1, t0 + L["min_s"]), t0 + L["max_s"]), 3)
        # never over a text plate: clip to the talk/insert beat it sits on
        for b in tl:
            if b["kind"] in TEXT_KINDS and b["t0"] < t1 and b["t1"] > t0:
                t1 = min(t1, b["t0"]) if t0 < b["t0"] else t1
                t0 = max(t0, b["t1"]) if t0 >= b["t0"] else t0
        o = dict(kind="lt", t0=t0, t1=t1, lines=it["lines"])
        if "y_bottom" in it:
            o["y_bottom"] = it["y_bottom"]
        lts.append(o)
        last = t1
    ctas, last = [], 0.0
    Cc = T["cta"]
    items = C.get("ctas")
    if not items:
        # no CTA list in the content: a pill on EVERY occurrence of a template CTA phrase, in order
        items = []
        for ph in Cc["phrases"]:
            aft = 0.0
            while True:
                try:
                    i, n = A._seq(ph, aft)
                except SystemExit:
                    break
                items.append(dict(t0=round(A.W[i][1], 3), t1=round(A.W[i][1] + Cc["dur_s"], 3)))
                aft = A.W[i + n - 1][2] + 0.5
        items.sort(key=lambda x: x["t0"])
    for k, it in enumerate(items):
        if "t0" in it:
            t0 = float(it["t0"]); t1 = float(it.get("t1", t0 + Cc["dur_s"]))
        else:
            t0 = round(A.at(it["at"], float(it.get("after", last))), 3)
            t1 = round(t0 + Cc["dur_s"], 3)
        ctas.append(dict(kind="cta", t0=t0, t1=t1, top=it.get("top", C.get("cta_top", "Get A FREE AI Image Of Yourself")),
                         big=it.get("big", C.get("cta_big", "With Abs")), **({"big_size": it["big_size"]} if "big_size" in it else {})))
        last = t1 + 0.5
    if ctas and Cc.get("last_runs_to_end"):
        ctas[-1]["t1"] = dur
    flashes = flashes_for(tl, T)

    # ---- the talk splices and the picture cuts
    talk_spans = [[b["t0"], b["t1"]] for b in tl if b["kind"] == "talk"]
    json.dump(talk_spans, open(os.path.join(a.build, "talk_spans.json"), "w"))
    splices = [s["cut_in"] for s in E[1:]]
    in_talk = [s for s in splices if any(x + 0.05 <= s <= y - 0.05 for x, y in talk_spans)]
    pc_path = a.piccuts or os.path.join(a.build, "piccuts.json")
    if not a.plan_only and not (a.piccuts and os.path.exists(a.piccuts)):
        cmd = [sys.executable, os.path.join(HERE, "kit_cuts.py"), "decide", "--build", a.build,
               "--mode", "master" if a.from_master else "raw", "--raw", a.raw, "--edl", a.edl,
               "--talk", os.path.join(a.build, "talk_spans.json"), "--search", str(T["cut"]["search_frames"]),
               "--trusted", str(T["cut"]["trusted_conf"]), "--cover-below", str(T["cut"]["cover_below"])]
        if a.reference:
            cmd += ["--reference", a.reference]
        if a.grade:
            cmd += ["--grade", a.grade]
        if a.rolls:
            cmd += ["--rolls", a.rolls]
        if a.from_master and not a.reference:
            raise SystemExit("--from-master needs --reference (his render)")
        print("kit_cuts:", " ".join(cmd[2:6]), flush=True)
        subprocess.run(cmd, check=True)
    piccuts = json.load(open(pc_path)) if os.path.exists(pc_path) else []
    # ---- splices INSIDE a plated beat that shows Dan in a window (window / stmt / winmedia). The window is a
    #      fixed crop with no zoom to step, and round 2's judge read three of these as jump cuts (167.6, 171.7,
    #      224.0 s). They take the documented fallback: a 5-frame cross-dissolve in the BASE (shortad Step 7c),
    #      where there are no graphics, so nothing downstream moves.
    have = {r["i"] for r in piccuts}
    piccuts = [r for r in piccuts if r.get("method") != "window-dissolve"]
    for i in range(1, len(E)):
        t = E[i]["cut_in"]
        if i in have and not any(r["i"] == i and r.get("method") == "window-dissolve" for r in piccuts):
            pass
        def _kind(x):
            return next((b["kind"] for b in tl if b["t0"] <= x < b["t1"]), None)
        DANWIN = ("window", "stmt", "winmedia")
        # both sides show Dan in a plate window (a cut 3 frames before a window -> statement boundary is as
        # bare as one in the middle: round 2 judge, 171.7 s)
        if _kind(t - 0.05) in DANWIN and _kind(t + 0.05) in DANWIN and not any(r["i"] == i for r in piccuts):
            piccuts.append(dict(i=i, cut=round(t, 3), n0=round(t * FPS), k=0, pic_frame=round(t * FPS), conf=0.0,
                                method="window-dissolve", cover="dissolve", sim_at_k=None))
    piccuts.sort(key=lambda r: r["i"])
    # ---- clamp every moved cut so a take is never on screen for less than min_take_frames, then
    #      write edl_picture.json from the AUDIO EDL + the (clamped) k of every talk splice
    MINF = int(T["cut"].get("min_take_frames", 8))
    bounds = sorted({round(b["t0"] * FPS) for b in tl} | {round(b["t1"] * FPS) for b in tl})
    byi = {r["i"]: r for r in piccuts}
    n_audio = [round(s["cut_in"] * FPS) for s in E]
    talk_edges = sorted({round(b["t0"] * FPS) for b in tl if b["kind"] == "talk"} | {round(b["t1"] * FPS) for b in tl if b["kind"] == "talk"})
    for r in piccuts:
        if r.get("cover") == "dissolve":
            continue
        i, k = r["i"], int(r["k"])
        n0 = n_audio[i]
        # a cut within the search window of a talk-beat EDGE moves ONTO the edge: the insert boundary (and its
        # flash) then hides it. Round 2's gate: the join at 50.72 s, 8 frames after a card -> talk return, read
        # 86.3 against the file's own 66.5 ceiling.
        near = [e for e in talk_edges if 0 < abs(e - n0) <= int(T["cut"]["search_frames"]) and e not in (0, round(dur * FPS))]
        if near:
            e = min(near, key=lambda x: abs(x - n0))
            r["k_unsnapped"], r["k"], r["snapped_to_boundary"] = k, e - n0, True
            r["cover"] = None
            continue
        prev_n = n_audio[i - 1] + (int(byi[i - 1]["k"]) if (i - 1) in byi else 0)
        next_n = n_audio[i + 1] if i + 1 < len(E) else round(dur * FPS)
        lo_n = max([prev_n] + [b for b in bounds if b <= n0]) + MINF
        hi_n = min([next_n] + [b for b in bounds if b >= n0]) - MINF
        kk = max(lo_n - n0, min(hi_n - n0, k)) if lo_n <= hi_n else 0
        if kk != k:
            r["k_unclamped"], r["k"], r["clamped_k"] = k, kk, True
    P = [dict(s) for s in E]
    for i in range(1, len(P)):
        k = int(byi[i]["k"]) if i in byi else 0
        if k:
            dt = k / FPS
            P[i]["cut_in"] += dt; P[i]["src_in"] += dt
            P[i - 1]["cut_out"] += dt; P[i - 1]["src_out"] += dt
    prev = 0
    for i, sg in enumerate(P):
        cum = round(sg["cut_out"] * FPS)
        sg["n0"], sg["n1"] = prev, cum
        sg["audio_cut_in"] = E[i]["cut_in"]
        sg["rel"] = int(byi[i]["k"]) if i in byi else 0
        prev = cum
    json.dump(P, open(os.path.join(a.build, "edl_picture.json"), "w"), indent=1)
    json.dump(piccuts, open(os.path.join(a.build, "piccuts.json"), "w"), indent=1)
    cover = {round(r["cut"], 3) for r in piccuts if r.get("cover")}
    moved = {round(r["cut"], 3): r["k"] for r in piccuts if r.get("k")}
    # the PICTURE cut times (on the delivered timeline) of every bare talk splice: each gets a level STEP
    pic_cuts = sorted(round((n_audio[r["i"]] + int(r["k"])) / FPS, 4) for r in piccuts if r.get("cover") != "dissolve")

    # ---- the push schedule and the design's own numbers
    pushes = pushes_for(tl, pic_cuts if T["cut"].get("step_every_bare_cut") else [round(s, 3) for s in in_talk],
                        cover, words, T, flashes)
    steps = [p for p in pushes if p[1] <= p[0]]                  # instant-in on a cut = a level step
    ramped = [p for p in pushes if p[1] > p[0]]                   # a ramped emphasis push (the top-up)
    # his hand-counted pushes are punch-ins on the talking head that also hide his trims; a step-in that
    # holds and ramps out is one of those. A step whose pull-out is also instant is a pure framing change.
    pushes_like = ramped + [p for p in steps if p[3] > p[2]]
    z = T["push"]["z"]
    talk_s = sum(b["t1"] - b["t0"] for b in tl if b["kind"] == "talk")
    pushed = sum(1 for i in range(int(dur * 10)) if push_at(i / 10, pushes, z) > 1.0 + (z - 1) * 0.5
                 and any(b["t0"] <= i / 10 < b["t1"] for b in tl if b["kind"] == "talk")) / 10
    mins = dur / 60.0
    ins = [b for b in tl if b["kind"] in INSERT_KINDS]
    txt = [b for b in tl if b["kind"] in TEXT_KINDS]
    design = dict(
        pushes_hand_per_min=len(pushes_like) / mins,
        level_steps_per_min=len(steps) / mins,
        push_off_frac=pushed / max(talk_s, 1e-6),
        flashes_per_min=len(flashes) / mins,
        lower_thirds_per_min=len(lts) / mins,
        cta_count=len(ctas),
        graphics_per_min=(len(lts) + len(ctas) + len(txt)) / mins,
        inserts_per_min=len(ins) / mins,
        insert_coverage_hand=sum(b["t1"] - b["t0"] for b in tl if b["kind"] != "talk") / dur,
        longest_talk_hand_s=max((b["t1"] - b["t0"] for b in tl if b["kind"] == "talk"), default=0.0),
    )
    # opening_changes_15s, change_rate, static_run etc. are the gate's own instruments and are measured on the
    # DELIVERED file (picture_ref.py check), not estimated here
    rows = []
    for k, v in design.items():
        lo, hi, side = ref_number(ref, k)
        if lo is None:
            rows.append((k, v, None, None, "no reference (his cuts need none: his frame choice hides them)" if k == "level_steps_per_min" else "no reference"))
            continue
        st = "PASS" if lo <= v <= hi else ("DEFECT" if (v < lo and side in ("low", "both")) or (v > hi and side in ("high", "both")) else "OVERSHOOT")
        rows.append((k, v, lo, hi, st))

    # ---- write the beat sheet the pipeline consumes
    out = dict(
        kit="kit9x16", template_version=T["version"], mode="master" if a.from_master else "raw",
        dur=dur, fps="30000/1001", push_z=z,
        beats=beats, lower_thirds=lts, ctas=ctas, insets=C.get("insets", []),
        pushes=[list(p) for p in pushes], flashes=[list(f) for f in flashes],
        no_caps_kinds=C.get("no_caps_kinds", ["window", "title", "stmt", "cta"]),
        no_caps_bodies=C.get("no_caps_bodies", []),
        base_kinds=list(BASE_KINDS), seams=[],
        cta_top=C.get("cta_top", "Get A FREE AI Image Of Yourself"), cta_big=C.get("cta_big", "With Abs"),
        deviations=C.get("deviations", []),
        words=[dict(w=w["w"], t=round(w["t"], 3), e=round(w["e"], 3)) for w in words],
        picture_cuts=dict(talk_splices=len(in_talk), moved=len(moved), covered=len(cover), source="piccuts.json"),
    )
    json.dump(out, open(os.path.join(a.build, "beats.json"), "w"), indent=1)
    shutil.copy(os.path.join(HERE, "kit_beats.py"), os.path.join(a.build, "beats.py"))
    rep = dict(build=os.path.abspath(a.build), mode=out["mode"], template=os.path.abspath(a.template),
               reference=PICREF, reference_version=ref.get("version"),
               design=design, rows=[dict(key=k, value=v, lo=lo, hi=hi, status=st) for k, v, lo, hi, st in rows],
               timeline=[dict(kind=b["kind"], t0=b["t0"], t1=b["t1"], media=b.get("media")) for b in tl],
               pushes=[list(p) for p in ramped], level_steps=[list(p) for p in steps], flashes=out["flashes"], lower_thirds=[(o["t0"], o["t1"]) for o in lts],
               ctas=[(o["t0"], o["t1"]) for o in ctas], talk_splices=in_talk,
               covered_splices=sorted(cover), moved_splices=moved)
    json.dump(rep, open(os.path.join(a.build, "kit_report.json"), "w"), indent=1)
    print(f"\nkit9x16 {out['mode']}: {len(tl)} base beats, {len(ins)} inserts, {len(txt)} text plates, {len(lts)} lower thirds, "
          f"{len(ctas)} CTAs, {len(flashes)} flashes, {len(ramped)} ramped pushes + {len(steps)} level steps ({100 * design['push_off_frac']:.0f}% of talk); "
          f"{len(in_talk)} talk splices, {len(moved)} moved, {len(cover)} covered")
    print(f"design vs picture.json v{ref.get('version')}:")
    for k, v, lo, hi, st in rows:
        band = f"[{lo:.3f} .. {hi:.3f}]" if lo is not None else ""
        print(f"  {st:10s} {k:24s} {v:8.3f}  {band}")
    bad = [k for k, *_, st in rows if st == "DEFECT"]
    if bad:
        print(f"  ⚠ the generated design is outside his range on {bad} -- fix the content or the grammar, never the range")
    print(f"-> {a.build}/beats.json, beats.py, kit_report.json")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
