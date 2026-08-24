#!/usr/bin/env python3
"""rev5 beat sheet -- the single source of truth for graphics, inserts, SFX and QC.

Every beat is anchored to a PHRASE, not to a hardcoded second. The tight cut's timeline
moves whenever a pause-removal parameter changes, and hardcoded anchors silently drift
off the words they were meant to land on. `at("some words")` finds the phrase in the
tight word list and returns the start of its first word.

Beat list = Muhammad's 2.5-min cut, beat for beat, WITH Dan's revision doc applied
(2026-08-23), then continued to the end of the ad, which his cut never reached.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
TC = json.load(open(f"{HERE}/tight_cuts_full.json"))
WORDS = TC["words"]
DUR = TC["dur"]

# strip() matters: Whisper tokens carry a LEADING SPACE, and " this" never
# equals "this" no matter how the punctuation is cleaned.
_norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
_SEQ = [_norm(w["w"]) for w in WORDS]

def _find(phrase, after=0.0):
    """Index of `phrase`, searching only at/after tight time `after`.

    `after` is not optional decoration: this script repeats whole phrases ("tap the
    button below", "phone lock screen", "stressful life"), and matching the first
    occurrence silently produced beats with NEGATIVE duration.
    """
    toks = _norm(phrase).split()
    start = next((i for i, w in enumerate(WORDS) if w["t"] >= after), 0)
    for i in range(start, len(_SEQ) - len(toks) + 1):
        if _SEQ[i:i + len(toks)] == toks:
            return i
    raise KeyError(f"phrase not found after {after}s: {phrase!r}")

def at(phrase, pad=-0.06, after=0.0):
    """Start time of the first word of `phrase`, nudged early so the cut leads the word."""
    return round(WORDS[_find(phrase, after)]["t"] + pad, 3)

def end_of(phrase, pad=0.10, after=0.0):
    """End time of the LAST word of `phrase`."""
    i = _find(phrase, after) + len(_norm(phrase).split()) - 1
    return round(WORDS[i]["e"] + pad, 3)

# ------------------------------------------------------------------ the beats
CALLOUT = (0.00,              end_of("not even real"))
GEN     = (at("I generated"), end_of("200 pounds"))
PHONE   = (at("I made it my phone"), end_of("more than a year"))
TODAY   = (at("And this is where"), end_of("at today"))
BULLETS = (at("In today's episode"), end_of("with abs for free"))
LOWER3  = (at("The problem is that finding"), at("when you're living a busy") - 0.05)
DADCLIP = (at("when you're living a busy"), end_of("stressful life"))
TITLE   = (at("Visualizing your goal"), end_of("motivate yourself"))
BBUILD  = (at("Fitness models and bodybuilders"), end_of("for decades"))
SHOP    = (at("Some of them would literally"), end_of("every day"))
APPDEMO = (at("With AI, you can create"), end_of("always wanted"))
AMAZING = (at("You realize how amazing"), end_of("stomach fat"))
LOWER3B = (at("And you'd be filled"), end_of("a reality"))
FREECARD= (at("And right now, you can generate"), end_of("completely free"))
_c1 = at("Just tap the button below")
CTA1    = (_c1, end_of("see yourself with abs", after=_c1))
BEN1    = (at("You're more attractive"), end_of("to women"))
BEN2    = (at("Men respect you more"), end_of("respect you more"))
BEN3    = (at("You feel better"), end_of("health improves"))
BEN4    = (at("And you'll probably live longer"), end_of("live longer too"))
LOWER3C = (at("If you're not working out"), end_of("what you already know"))
BEFORE1 = (at("I wanted to get my abs back"), at("as a 38 year old dad"))
_fd = at("as a 38 year old dad")
FATDAD  = (_fd, end_of("stressful life", pad=0.05, after=_fd))
_ap = at("until I generated this picture")
AFTERPIC= (_ap, end_of("phone lock screen", after=_ap))
# The other two shoot photos from Dan's 0:11 list. Four photos will not read in the
# 1.8 s "where I'm at today" beat (0.44 s each is a flicker), so two land there and two
# land on the line that is literally about how he looks now.
LOOKNOW = (at("this is how I'm supposed to look"), end_of("how I need to look"))
# ---- the remainder Muhammad's cut never reached ----
MEALPREP= (at("To meal prep every week"), end_of("track my calories"))
APPINTRO= (at("that I created an app"), end_of("goal for free"))
SUPERIOR= (at("So it's far superior"), end_of("general purpose AI"))
_c2 = at("To generate an image of yourself")
CTA2    = (_c2, end_of("tap the button below", after=_c2))
STEP1   = (at("The picture is just step one"), end_of("just step one"))
SEQ     = (at("Once you generate an image"), end_of("to make it real"))
ASSESS  = (at("Our AI scans your current"), end_of("training status"))
GOALSCAN= (at("Then it scans your goal picture"), end_of("want to be"))
WORKOUT = (at("Then it builds your customized"), end_of("and your goal"))
PLANBUL = (at("Your workout plan works around"), end_of("actually have"))
NUTRI   = (at("Your nutrition plan is calibrated"), end_of("stick to it"))
ENDCARD = (at("To start losing your belly fat"), round(DUR, 3))

BEATS = {k: v for k, v in sorted(globals().items())
         if k.isupper() and isinstance(v, tuple) and len(v) == 2 and k not in ("BEATS",)}
for _k, (_a, _b) in BEATS.items():
    assert _b > _a, f"{_k} has non-positive duration {_a}->{_b}"

if __name__ == "__main__":
    print(f"tight duration {DUR:.2f}s\n")
    for k, (a, b) in sorted(BEATS.items(), key=lambda kv: kv[1][0]):
        print(f"  {int(a//60)}:{a%60:05.2f} -> {int(b//60)}:{b%60:05.2f}  ({b-a:5.2f}s)  {k}")
