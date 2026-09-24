#!/usr/bin/env python3
"""TAKE SELECTION. Today we remove flubs; this picks the BEST take, by the four rules that were
written down across the skills and implemented nowhere (handoff-20260911-junk-footage-pass.md):

  1. later-take-wins ONLY when the later take is fluent          (ad-edit/SKILL.md take lessons)
     -- "a later take with internal silences loses to a clean earlier take"
  2. a roll's noise floor identifies the bad take                (ad-edit lesson 57)
     -- Dan's own "did that plane pick up?" measured −41.6 dBFS / 20-200 Hz −13.3 dB on the bad
        take against −45.3 / −20.2 on the retake and ≈ −48 everywhere else
  3. cut the whole restated SENTENCE, not the aborted take inside it
     -- v2 cut only the flub and Dan flagged it again, because the sentence restated "all kinds
        of problems" from 6 s earlier
  4. his rhetorical repeats (anaphora) are deliberate; re-INTRODUCTIONS of the same item are junk

  takes.py <roll.MP4> [--words words.json] [--model small] [--out takes_report.json] [--md list.md]

The roll's own sidecar is used when it exists (`<stem>.roll/words.json`, `<stem>.roll.json` for the
lav channel); otherwise the roll is transcribed with the chunked runner. The output is a LIST FOR
DAN: every retake group, which take was chosen and why, the keep range in source timecode, and
what was dropped. ⚠ Its choices are shown to Dan before a cut is built on them -- this file
recommends, it does not cut.

A "take" here is a run of speech with no gap ≥ 1.0 s (the roll sidecar's definition), and a
"group" is a take plus the takes that re-say it: whole-text similarity ≥ 0.72 (the sidecar's
retake rule) OR the same first twelve words at ≥ 0.75 (an abandoned attempt followed by the full
take -- short against long, their whole-text ratio is low but they start the same).
"""
import argparse
import difflib
import json
import os
import re
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

from _shared.cut import speech as S                          # noqa: E402
from _shared.cut import junk as J                            # noqa: E402

TAKE_GAP = 1.0            # roll_sidecar.take_list: a new take begins after ≥ 1.0 s of no words
RETAKE_WHOLE = 0.72       # roll_sidecar: whole-text similarity that marks a retake
RETAKE_HEAD = 0.75        # the first twelve words agree: an aborted attempt + its full take
RETAKE_WINDOW = 180.0     # a retake follows within three minutes; beyond that it is a new beat
FLUENT_GAP = 0.90         # an internal gap this long inside a take is a hesitation (0.55-0.65 is breath)
FLUENT_SWALLOW = 0.45     # a swallowed pause this long is a hesitation, not timing slop
NOISY_FLOOR_DB = 4.0      # a take whose floor sits this far above the roll's TYPICAL take floor is the plane
COMPLETE_FRAC = 0.60      # a take shorter than 60 % of its group's longest is an abandoned attempt
NOISY_LOW_DB = 5.0        # ...or whose 20-200 Hz floor does
LEAD_S, TAIL_S = 0.20, 0.30   # the pads a keep range gets into the measured silence


def _sim(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio() if a and b else 0.0


def toks(words):
    return [S.norm(w["w"]) for w in words if S.norm(w["w"])]


# ---------------------------------------------------------------------------- takes and groups
def split_takes(words, gap=TAKE_GAP):
    groups, cur = [], [words[0]] if words else []
    for w in words[1:]:
        if w["t"] - cur[-1]["e"] >= gap:
            groups.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        groups.append(cur)
    out = []
    for i, g in enumerate(groups, 1):
        out.append(dict(take=i, start=g[0]["t"], end=g[-1]["e"], words=g,
                        text=" ".join(w["w"].strip() for w in g), tokens=toks(g)))
    return out


def group_retakes(takes):
    """Assign each take a group: the earliest take it re-says, chained."""
    for t in takes:
        t["group"] = t["take"]
        t["retake_of"] = None
        for prev in reversed(takes[:t["take"] - 1]):
            if t["start"] - prev["end"] > RETAKE_WINDOW:
                break
            a, b = t["tokens"], prev["tokens"]
            if len(a) < 3 or len(b) < 3:
                continue
            whole = _sim(a, b)
            head = _sim(a[:12], b[:12])
            if whole >= RETAKE_WHOLE or head >= RETAKE_HEAD:
                t["group"] = prev["group"]
                t["retake_of"] = prev["take"]
                t["retake_similarity"] = dict(whole=round(whole, 2), head=round(head, 2))
                break
    groups = {}
    for t in takes:
        groups.setdefault(t["group"], []).append(t)
    return [groups[k] for k in sorted(groups)]


# ---------------------------------------------------------------------------- measures per take
def lowband_envelope(a):
    """20 ms RMS dB of the 20-200 Hz band -- lesson 57's second number."""
    from scipy.signal import butter, sosfiltfilt
    sos = butter(4, [20, 200], btype="band", fs=S.SR, output="sos")
    return S.envelope(sosfiltfilt(sos, a))


def measure_take(t, db, low_db, gaps):
    i0, i1 = int(t["start"] / S.HOP_S), max(int(t["end"] / S.HOP_S), int(t["start"] / S.HOP_S) + 5)
    seg, lseg = db[i0:i1], low_db[i0:i1]
    floor = float(np.percentile(seg, 5)) if len(seg) else float("nan")
    low = float(np.percentile(lseg, 5)) if len(lseg) else float("nan")
    inner = [(g0, g1) for g0, g1 in gaps if g0 >= t["start"] and g1 <= t["end"]]
    long_gaps = [(round(g0, 2), round(g1 - g0, 2)) for g0, g1 in inner if g1 - g0 >= FLUENT_GAP]
    sw, fixed = J.detect_swallowed(t["words"], inner)
    swallowed = [c for c in sw if c["measure"]["seconds"] >= FLUENT_SWALLOW]
    stretched = [(round(w["t"], 2), w["w"].strip(), round(w["e"] - w["t"], 2))
                 for w in t["words"] if w["e"] - w["t"] > J.STRETCH_MIN]
    reps = J.detect_repeats(fixed, inner)
    restarts = [c for c in reps if c["measure"]["kind"] == "RESTART"]
    reintro = [c for c in reps if c["measure"]["kind"] == "REINTRO"]
    anaphora = [c for c in reps if c["measure"]["kind"] == "ANAPHORA"]
    last = t["words"][-1]["w"].strip() if t["words"] else ""
    defects = len(long_gaps) + len(swallowed) + len(restarts)
    t["measure"] = dict(
        seconds=round(t["end"] - t["start"], 2), words=len(t["words"]),
        floor_db=round(floor, 1), low_floor_db=round(low, 1),
        long_gaps=long_gaps,
        swallowed=[(c["t"], c["measure"]["seconds"], c["measure"]["word"]) for c in swallowed],
        stretched=stretched,
        restarts=[dict(t=c["t"], second=c["measure"]["second"], kind=c["measure"]["kind"],
                       gram=c["measure"]["gram"]) for c in restarts],
        anaphora=[c["measure"]["gram"] for c in anaphora],
        reintro=[dict(t=c["t"], second=c["measure"]["second"], gram=c["measure"]["gram"]) for c in reintro],
        ends_sentence=bool(re.search(r"[.?!]$", last)), defects=defects,
        fluent=bool(defects == 0),
    )
    t["_words"] = t.pop("words")
    return t


def mark_noise(takes):
    """Rule 2. The roll's TYPICAL take floor is the median over takes ≥ 3 s (lesson 57's "≈ −48 dB
    everywhere else on the roll"); a take sitting NOISY_FLOOR_DB above it, or NOISY_LOW_DB above
    it in the 20-200 Hz band, is the one the plane is on. ⚠ Not the roll's 5th percentile: that
    reads the pre-roll's digital silence and calls every take noisy."""
    long_ = [t for t in takes if t["measure"]["seconds"] >= 3.0] or takes
    roll_floor = float(np.median([t["measure"]["floor_db"] for t in long_]))
    roll_low = float(np.median([t["measure"]["low_floor_db"] for t in long_]))
    for t in takes:
        m = t["measure"]
        m["floor_over_roll_db"] = round(m["floor_db"] - roll_floor, 1)
        m["low_over_roll_db"] = round(m["low_floor_db"] - roll_low, 1)
        m["noisy"] = bool(m["floor_over_roll_db"] > NOISY_FLOOR_DB or m["low_over_roll_db"] > NOISY_LOW_DB)
    return roll_floor, roll_low


# ---------------------------------------------------------------------------- selection
def choose(group):
    """Rules 1, 2 and 4 on one retake group. Returns (chosen take, reason, flags)."""
    if len(group) == 1:
        t = group[0]
        flags = []
        if t["measure"]["restarts"]:
            flags.append(f"{len(t['measure']['restarts'])} restart(s) inside the take: rule 3, cut each "
                         f"restated sentence whole (see the junk report for the timecodes)")
        if t["measure"]["reintro"]:
            flags.append(f"{len(t['measure']['reintro'])} phrase(s) said twice fluently at "
                         f"{', '.join(J.mmss(r['t']) for r in t['measure']['reintro'])}: listen -- a re-introduction is junk, a parallel list is deliberate")
        if t["measure"]["noisy"]:
            flags.append(f"floor {t['measure']['floor_over_roll_db']:+.1f} dB / low band "
                         f"{t['measure']['low_over_roll_db']:+.1f} dB over the roll's takes: listen for the plane")
        return t, "only take", flags
    longest = max(t["measure"]["words"] for t in group)
    for t in group:
        t["measure"]["complete"] = t["measure"]["words"] >= COMPLETE_FRAC * longest
    usable = [t for t in group if not t["measure"]["noisy"]] or group
    noisy_note = [] if len(usable) == len(group) else \
        [f"take {t['take']} dropped on noise floor ({t['measure']['floor_over_roll_db']:+.1f} dB over the roll's takes)"
         for t in group if t not in usable]
    whole = [t for t in usable if t["measure"]["complete"]] or usable
    fluent = [t for t in whole if t["measure"]["fluent"]]
    if fluent:
        pick = fluent[-1]                                    # rule 1: the LATER fluent take
        later = [t for t in usable if t["take"] > pick["take"]]
        why = "later fluent take" if not later else \
            (f"latest FLUENT take -- take {later[-1]['take']} is later but "
             f"{'not fluent (' + _why_not(later[-1]) + ')' if later[-1]['measure']['complete'] else 'an abandoned attempt'}")
        return pick, why, noisy_note
    # nobody is fluent: the fewest defects among the complete takes, later on a tie, and say so
    best = sorted(whole, key=lambda t: (t["measure"]["defects"], -t["take"]))[0]
    return best, f"no fluent take in the group; fewest defects ({best['measure']['defects']})", \
        noisy_note + ["needs a listen: every complete take in this group hesitates or restarts"]


def _why_not(t):
    m = t["measure"]
    bits = []
    if m["long_gaps"]:
        bits.append(f"{len(m['long_gaps'])} internal gap(s) ≥ {FLUENT_GAP} s")
    if m["swallowed"]:
        bits.append(f"{len(m['swallowed'])} swallowed pause(s)")
    if m["restarts"]:
        bits.append(f"{len(m['restarts'])} restart(s)")
    if not m.get("complete", True):
        bits.append("an abandoned attempt (under 60 % of the group's longest take)")
    return ", ".join(bits) or "?"


def keep_range(t, gaps, restart_cut=True):
    """The recommended keep range for a chosen take, in SOURCE time, padded into measured silence.
    Rule 3: if the take itself contains a restart, the keep begins at the SECOND copy's sentence
    (the whole restated sentence goes, not the flub inside it)."""
    a, b = t["start"], t["end"]
    note = None
    if restart_cut and t["measure"]["restarts"]:
        r = t["measure"]["restarts"][0]
        note = (f"rule 3: restart at {J.mmss(r['t'])} -> {J.mmss(r['second'])} ({r['gram']!r}); cut the "
                f"whole restated sentence from the first copy through the hesitation, keep from the second copy "
                f"-- confirm by ear")
    lead = LEAD_S
    g = S.gap_at(gaps, a - 0.01) or next(((g0, g1) for g0, g1 in reversed(gaps) if g1 <= a), None)
    if g:
        lead = min(LEAD_S, max(0.0, a - g[0]))
    tail = TAIL_S
    g = S.gap_at(gaps, b + 0.01) or next(((g0, g1) for g0, g1 in gaps if g0 >= b), None)
    if g:
        tail = min(TAIL_S, max(0.0, g[1] - b))
    return [round(a - lead, 3), round(b + tail, 3)], note


def restated_tail(prev, nxt):
    """Rule 3 across takes: the chosen take B opens by re-saying the tail of the chosen take A
    before it. Returns the index into A's words where the restated SENTENCE begins (walked back to
    the previous sentence end), or None."""
    if not prev or not nxt or len(nxt["tokens"]) < 4:
        return None
    head = nxt["tokens"][:4]
    pw = [w for w in prev["_words"] if S.norm(w["w"])]
    tail_n = min(25, len(pw))
    for i in range(len(pw) - tail_n, len(pw) - 3):
        if _sim([S.norm(w["w"]) for w in pw[i:i + 4]], head) >= 0.75:
            j = i
            while j > 0 and not re.search(r"[.?!]$", pw[j - 1]["w"].strip()):
                j -= 1
            return prev["_words"].index(pw[j])
    return None


# ---------------------------------------------------------------------------- the report
def build(media, words, words_source, a, quiet=False):
    db = S.envelope(a)
    low_db = lowband_envelope(a)
    gaps = S.gaps_from_envelope(db)
    takes = split_takes(words)
    groups = group_retakes(takes)
    for t in takes:
        measure_take(t, db, low_db, gaps)
    roll_floor, roll_low = mark_noise(takes)
    chosen_prev = None
    out_groups = []
    for g in groups:
        pick, why, flags = choose(g)
        kr, note = keep_range(pick, gaps)
        if note:
            flags.append(note)
        cut_prev = restated_tail(chosen_prev, pick)
        if cut_prev is not None and out_groups and cut_prev > 0:
            new_out = chosen_prev["_words"][cut_prev]["t"]
            if new_out > chosen_prev["start"] + 0.5:
                out_groups[-1]["keep"][1] = round(new_out - 0.05, 3)
                out_groups[-1]["flags"].append(
                    f"rule 3: take {pick['take']} re-says this take's last sentence "
                    f"({' '.join(pick['tokens'][:4])!r}); keep now ends at {J.mmss(new_out)}, "
                    f"before that sentence -- the whole restated sentence goes")
        out_groups.append(dict(
            group=g[0]["group"], takes=[t["take"] for t in g], chosen=pick["take"], why=why,
            keep=kr, flags=flags,
            dropped=[dict(take=t["take"], span=[round(t["start"], 3), round(t["end"], 3)],
                          why=("noise floor" if t["measure"]["noisy"] else
                               _why_not(t) if (not t["measure"]["fluent"] or not t["measure"].get("complete", True))
                               else "earlier take (the later fluent take wins)"))
                     for t in g if t is not pick],
            text=pick["text"],
        ))
        chosen_prev = pick
    return dict(
        takes_report_version="1.0.0", when=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        media=os.path.abspath(media), sha256=S.sha256(media), words_source=words_source,
        duration=round(len(db) * S.HOP_S, 2), roll_floor_db=round(roll_floor, 1),
        roll_low_floor_db=round(roll_low, 1), gap_threshold_db=round(S.gap_threshold(db), 1),
        takes=[{k: v for k, v in t.items() if k not in ("_words", "tokens")} for t in takes],
        groups=out_groups,
        summary=dict(takes=len(takes), groups=len(groups),
                     groups_with_retakes=sum(1 for g in groups if len(g) > 1),
                     later_take_lost=sum(1 for g in out_groups if "latest FLUENT" in g["why"]),
                     noisy_takes=sum(1 for t in takes if t["measure"]["noisy"]),
                     needs_listen=sum(1 for g in out_groups if any("listen" in f for f in g["flags"]))),
    )


def markdown(r):
    L = [f"# Take selection: {os.path.basename(r['media'])}", "",
         f"{r['summary']['takes']} takes in {r['summary']['groups']} groups; "
         f"{r['summary']['groups_with_retakes']} groups have retakes; in {r['summary']['later_take_lost']} "
         f"the later take LOST to an earlier fluent one; {r['summary']['noisy_takes']} take(s) sit above the "
         f"roll's noise floor ({r['roll_floor_db']} dBFS, 20-200 Hz {r['roll_low_floor_db']} dB); "
         f"{r['summary']['needs_listen']} group(s) need a listen.", "",
         "Rules: later take wins only when fluent; a floor above the roll's marks the bad take; a restated "
         "sentence is cut whole; rhetorical repeats stay, re-introductions go.", "",
         "| group | takes | chosen | keep (source) | why | flags |", "|---|---|---|---|---|---|"]
    for g in r["groups"]:
        if len(g["takes"]) == 1 and not g["flags"]:
            continue                                         # a clean single take needs no row
        L.append(f"| {g['group']} | {', '.join(map(str, g['takes']))} | **{g['chosen']}** | "
                 f"{J.mmss(g['keep'][0])} - {J.mmss(g['keep'][1])} | {g['why']} | {'; '.join(g['flags'])} |")
    L += ["", "## Every retake group, with the text", ""]
    for g in r["groups"]:
        if len(g["takes"]) == 1:
            continue
        L.append(f"**Group {g['group']}** (takes {', '.join(map(str, g['takes']))}) -> take {g['chosen']}, "
                 f"{J.mmss(g['keep'][0])} - {J.mmss(g['keep'][1])}: {g['why']}")
        L.append(f"> {g['text'][:400]}{'…' if len(g['text']) > 400 else ''}")
        for d in g["dropped"]:
            L.append(f"- dropped take {d['take']} ({J.mmss(d['span'][0])} - {J.mmss(d['span'][1])}): {d['why']}")
        for f in g["flags"]:
            L.append(f"- ⚠ {f}")
        L.append("")
    return "\n".join(L)


def lav_for(media):
    """The roll sidecar's lav pick, if the rolls tool has built one (a two-mic roll needs it)."""
    side = os.path.splitext(media)[0] + ".roll.json"
    if os.path.exists(side):
        try:
            lav = json.load(open(side)).get("audio", {}).get("lav", {})
            return lav.get("map"), lav.get("filter")
        except Exception:                                    # noqa: BLE001
            pass
    return None, None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("roll")
    ap.add_argument("--words")
    ap.add_argument("--model", default="small")
    ap.add_argument("--map")
    ap.add_argument("--af")
    ap.add_argument("--out")
    ap.add_argument("--md")
    ap.add_argument("--quiet", action="store_true")
    A = ap.parse_args()
    if not os.path.exists(A.roll):
        raise SystemExit(f"not on disk: {A.roll}")
    amap, af = (A.map, A.af) if (A.map or A.af) else lav_for(A.roll)
    if A.words:
        words, src = S.load_words(A.words), f"file:{A.words}"
    else:
        side = os.path.join(os.path.splitext(A.roll)[0] + ".roll", "words.json")
        if os.path.exists(side):
            words, src = S.load_words(side), f"sidecar:{side}"
        else:
            words, src = S.transcribe(A.roll, A.model, amap, af, quiet=A.quiet)
    a = S.pcm(A.roll, amap, af)
    r = build(A.roll, words, src, a, A.quiet)
    out = A.out or (os.path.splitext(A.roll)[0] + ".takes_report.json")
    json.dump(r, open(out, "w"), indent=1)
    md = markdown(r)
    if A.md:
        open(A.md, "w").write(md)
    print(md if not A.quiet else md.splitlines()[2])
    print(f"\n-> {out}" + (f"\n-> {A.md}" if A.md else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
