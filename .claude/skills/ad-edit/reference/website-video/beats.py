#!/usr/bin/env python3
"""Website video beat sheet -- the single source of truth for graphics, inserts and QC.

Every beat is anchored to a PHRASE on the tight timeline (ad-edit lesson 38), searched
AFTER a time wherever a phrase repeats. This video plays on absbyai.com right after the
visitor generates their goal image, so the design brief is TRUST: real app screens,
Dan's real photos, calm holds, no flashes, no whooshes, nothing that reads as hype.
"""
import json, os, re
HERE=os.path.dirname(os.path.abspath(__file__))
TC=json.load(open(f"{HERE}/tight_cuts.json"))
WORDS=TC["words"]; DUR=TC["dur"]
_norm=lambda s: re.sub(r"[^a-z0-9 ]","",s.lower()).strip()
_SEQ=[_norm(w["w"]) for w in WORDS]
def _find(phrase, after=0.0):
    toks=_norm(phrase).split()
    start=next((i for i,w in enumerate(WORDS) if w["t"]>=after),0)
    for i in range(start,len(_SEQ)-len(toks)+1):
        if _SEQ[i:i+len(toks)]==toks: return i
    raise KeyError(f"phrase not found after {after}s: {phrase!r}")
def at(phrase, pad=-0.06, after=0.0):
    return round(WORDS[_find(phrase,after)]["t"]+pad,3)
def end_of(phrase, pad=0.10, after=0.0):
    i=_find(phrase,after)+len(_norm(phrase).split())-1
    return round(WORDS[i]["e"]+pad,3)

# ------------------------------------------------------------------ the beats
# REV 2 (2026-09-02): 21 beats -> 13. Dan: "graphics sparingly -- much more sparingly."
# REV 4 (2026-09-08): + 7 AI clip inserts and the members-home scroll (Dan's placements, see below) -> 21 beats.
# Removed: POOL, ASSESS, TELLAI, WORKOUT, MEALPLAN, MEALBUL, SLEEP, TRYLIST.
NAME     = (at("This isn't just an AI picture"), end_of("that you've always wanted"))
# the before picture goes ON "I've been out of shape" and nowhere near a line about being lean;
# it ends before "and now at 40" (Dan: "opposite of what we're trying to convey")
# ...and it is fully gone 0.5 s before the after-photos start, so the two never share a frame
# (before -> Dan on camera -> after; a crossfade between them would superimpose the two)
# REV 3: the repeated first attempt is cut (tight.py MANUAL_CUTS), so the line is now
# "Now, I've been out of shape, and now at 40, I have the most defined abs of my life" -- 1.3 s of
# speech for the before card instead of rev 2's 2.6 s. So the card fades in on the pause after
# "finally lost.", holds through "I've been out of shape," and is out by "and" (Dan, rev 1: never let
# the before picture run into "and now at 40"). Dan is on camera for "and now at 40," (~1.1 s), and
# the four after photos start on "I have the most defined abs" -- the claim they prove.
_bef0    = end_of("finally lost", pad=0.0)
BEFORE   = (_bef0, at("and now at 40", after=_bef0))
# "how I look today" = Muhammad's four shoot photos, in sequence, over the whole lean passage
# (~8 s = ~2 s per photo; four photos in the 2.7 s line alone would be a flicker, lesson 41)
TODAY    = (at("I have the most", after=_bef0), end_of("get six pack abs"))
assert TODAY[0]-BEFORE[1]>=0.50, f"before -> Dan -> after needs >= 0.5 s of Dan between the cards (got {TODAY[0]-BEFORE[1]:.2f})"
_hw      = at("Here's why")
NUM1     = (at("First human fitness experts"),   end_of("but they can't do it for you"))      # lower third
MACRO    = (at("Abs by AI can actually track"), end_of("changed the game"))  # REAL recording (salmon plate -> 775 cal logged), PiP beside Dan.
# REV 4: the beat runs 4.4 s longer, to "before AI changed the game", so the logged-meal payoff is on screen long enough to read (judgment call, flagged in the notes)
FLYBLIND = (at("That means you don't have to fly"), end_of("far more easily"))               # lower third
NUM2     = (at("Second Abs by AI will create"),  end_of("than you think"))                    # lower third
NUM3     = (at("Third abs by AI will create"),   end_of("bases your program off that"))       # lower third
TRIAL    = (at("For a limited time"),            end_of("completely free for 7 days"))        # title card
CANCEL   = (at("If it's not for you"),           end_of("charged a dime"))                    # lower third
PRICE    = (at("and you'll be charged this"),    end_of("would charge you"))                  # title card
# REV 5 (Dan): the goal-image card at 3:36 is REMOVED -- "I want to keep the emphasis on the prospect and not on me at
# this point." Dan is on camera for the line with captions on; nothing replaces it.

# ---- REV 4 (Dan's rev-3 review, 2026-09-08): AI clip inserts to break up the talking head, and the members-home scroll.
# Full-frame inserts, tagged AI-GENERATED (upper-left, 1.5x -- lesson 17), captions stay on. Anchored to PHRASES.
AI_A  = (at("Imagine yourself taking off"),   end_of("seeing right now"))                 # the pool reveal
AI_B  = (AI_A[1],                             end_of("stubborn belly fat"))               # beach jog, a straight cut from the pool clip; Dan is back on camera for "finally lost." BEFORE the before card
AI_C1 = (at("Once our AI has all this"),      at("And when you're following"))            # training with the plan on his phone
AI_C2 = (at("And when you're following"),     at("Third abs by AI will create")-0.45)     # the quiet nod; out 0.45 s before the NUM3 lower third
# REV 5 (Dan's rev-4 review): D1's source leans in toward the pans from 4.4 s and Veo rendered his breath as SMOKE at
# 5.0-5.4 s, which was the insert's last second. The run starts a WORD LATER so the beat is 3.68 s and the clip is cut
# at source 4.08 -- 0.3 s before the lean. Dan is on camera for "Your AI will also" (1.5 s); the clips fade in on
# "customize". (ad-edit lesson 115: never prompt breath/smell/steam near the face.)
AI_D1 = (at("customize your eating plan"),    at("and to avoid the foods"))               # grilling, ends on him stirring
# D2's clip carries two Veo-baked dissolves (0.5-0.9 s and 3.9-4.6 s) AND, from ~7.0-7.1 s, the row of containers in the
# wide shot drifts and vanishes (Dan's rev-4 note). REV 5 cuts the wide shot at source 7.05 -- usable 2.85 + 2.35 =
# 5.20 s -- and hands the 0.97 s back to D3, which has spare clip (0.2-8.0 = 7.80 s usable, tail measured clean).
AI_D2 = (at("and to avoid the foods"),        at("that you have", after=156.0)-0.25)      # portioning into containers
AI_D3 = (AI_D2[1],                            end_of("you have available"))               # eating, loving it
HUB   = (at("We also have an AI sleep coach"), end_of("much more"))                       # members-home scroll, phone PiP beside Dan

_cta     = at("Try abs by AI for free", after=at("that they always wanted")-1.0)
CTA      = (_cta, round(DUR,3))                                                              # end card, holds

BEATS={k:v for k,v in sorted(globals().items())
       if k.isupper() and isinstance(v,tuple) and len(v)==2 and k!="BEATS"}
for _k,(_a,_b) in BEATS.items():
    assert _b>_a, f"{_k} has non-positive duration {_a}->{_b}"
_o=sorted(BEATS.items(), key=lambda kv: kv[1][0])
for (n1,(a1,b1)),(n2,(a2,b2)) in zip(_o,_o[1:]):
    ov=b1-a2
    assert ov<=0.25, f"{n1} {a1}-{b1} overlaps {n2} {a2}-{b2} by {ov:.2f}s"
    if ov>0:
        BEATS[n1]=(a1,round(a2-0.01,3)); globals()[n1]=BEATS[n1]
_o=sorted(BEATS.items(), key=lambda kv: kv[1][0])
for i,((n1,(a1,b1)),(n2,(a2,b2))) in enumerate(zip(_o,_o[1:])):
    if 0 < a2-b1 < 0.35:
        BEATS[n1]=(a1,round(a2,3)); globals()[n1]=BEATS[n1]
_o=sorted(BEATS.items(), key=lambda kv: kv[1][0])

# OVERLAY beats keep Dan full-frame (a lower third sits over the footage).
# PANEL beats keep Dan in the right column with a panel on the left.
# Everything else is a full-frame card that replaces him.
OVERLAY={"NAME","NUM1","FLYBLIND","NUM2","NUM3","CANCEL"}   # lower thirds over Dan
PANEL  ={"MACRO","HUB"}    # the phone PiPs: Dan stays on camera, pushed right, in the PIP level (FAR geometry)
AI     ={"AI_A","AI_B","AI_C1","AI_C2","AI_D1","AI_D2","AI_D3"}   # full-frame AI clips (tagged); captions stay on
for _n in AI: assert _n in BEATS, _n
assert BEFORE[0]-AI_B[1]>=0.5, f"Dan must be on camera between the beach clip and the before card (got {BEFORE[0]-AI_B[1]:.2f} s)"
assert NUM3[0]-AI_C2[1]>=0.36, f"the C2 clip must be fully out before the NUM3 lower third (got {NUM3[0]-AI_C2[1]:.2f} s)"
assert AI_D1[0]-NUM3[1]>=0.3, f"D1 must start after NUM3 ends (got {AI_D1[0]-NUM3[1]:.2f} s)"

if __name__=="__main__":
    print(f"tight duration {DUR:.2f}s   {len(BEATS)} beats\n")
    cov=0.0; prev=0.0
    for k,(a,b) in _o:
        if a-prev>0.05: print(f"  {int(prev//60)}:{prev%60:05.2f} -> {int(a//60)}:{a%60:05.2f}  ({a-prev:5.2f}s)  -- bare (Dan on camera)")
        print(f"  {int(a//60)}:{a%60:05.2f} -> {int(b//60)}:{b%60:05.2f}  ({b-a:5.2f}s)  {k}")
        cov+=b-a; prev=b
    if DUR-prev>0.05: print(f"  {int(prev//60)}:{prev%60:05.2f} -> {int(DUR//60)}:{DUR%60:05.2f}  ({DUR-prev:5.2f}s)  -- bare")
    full=sum(b-a for k,(a,b) in BEATS.items() if k not in OVERLAY)
    hard=sum(b-a for k,(a,b) in BEATS.items() if k not in OVERLAY and k not in PANEL)
    print(f"\nany graphic on screen      {cov/DUR*100:.0f}%")
    print(f"insert/graphic coverage    {full/DUR*100:.0f}%")
    print(f"Dan fully replaced         {hard/DUR*100:.0f}%")
    bare=[]; prev=0.0
    for k,(a,b) in _o:
        if a-prev>0.05: bare.append((prev,a))
        prev=b
    if DUR-prev>0.05: bare.append((prev,DUR))
    print(f"longest bare stretch       {max((b-a for a,b in bare),default=0):.1f}s")
