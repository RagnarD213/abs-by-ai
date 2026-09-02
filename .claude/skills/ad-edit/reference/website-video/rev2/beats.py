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
# Removed: POOL, ASSESS, TELLAI, WORKOUT, MEALPLAN, MEALBUL, SLEEP, TRYLIST.
NAME     = (at("This isn't just an AI picture"), end_of("that you've always wanted"))
# the before picture goes ON "I've been out of shape" and nowhere near a line about being lean;
# it ends before "and now at 40" (Dan: "opposite of what we're trying to convey")
# ...and it is fully gone 0.5 s before the after-photos start, so the two never share a frame
# (before -> Dan on camera -> after; a crossfade between them would superimpose the two)
BEFORE   = (at("Now I've been out of shape"),    at("now at 40", after=at("out of shape"))-0.50)
# "how I look today" = Muhammad's four shoot photos, in sequence, over the whole lean passage
# (33.9-42.0 s = ~2 s per photo; four photos in the 2.7 s line alone would be a flicker, lesson 41)
TODAY    = (at("now at 40", after=at("out of shape")), end_of("get six pack abs"))
_hw      = at("Here's why")
NUM1     = (at("First human fitness experts"),   end_of("but they can't do it for you"))      # lower third
MACRO    = (at("Abs by AI can actually track"), end_of("all the macros in what you're eating"))  # REAL recording, PiP beside Dan
FLYBLIND = (at("That means you don't have to fly"), end_of("far more easily"))               # lower third
NUM2     = (at("Second Abs by AI will create"),  end_of("than you think"))                    # lower third
NUM3     = (at("Third abs by AI will create"),   end_of("bases your program off that"))       # lower third
TRIAL    = (at("For a limited time"),            end_of("completely free for 7 days"))        # title card
CANCEL   = (at("If it's not for you"),           end_of("charged a dime"))                    # lower third
PRICE    = (at("and you'll be charged this"),    end_of("would charge you"))                  # title card
SOLVED   = (at("But now AI has solved"),         end_of("a plan to get you there"))           # goal image, tagged
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
OVERLAY={"NAME","NUM1","FLYBLIND","NUM2","NUM3","CANCEL"}
PANEL  ={"MACRO"}          # the phone PiP: Dan stays on camera, pushed right, in the WIDE level

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
