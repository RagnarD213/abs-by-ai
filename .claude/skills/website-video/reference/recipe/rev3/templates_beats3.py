#!/usr/bin/env python3
"""Ad 3 beat sheet -- the single source of truth for graphics, inserts, SFX and QC.

Every beat is anchored to a PHRASE, never to a hardcoded second (lesson 38): the tight
cut's timeline moves whenever a pause parameter changes. `at()` searches the tight word
list; `after=` is mandatory wherever a phrase repeats ("tap the button below",
"personal trainers", "your goal picture"), or the first occurrence silently wins and the
beat comes out with negative duration.

Beat list = the Ad 3 cue doc's bracketed cues, in order, plus the graphics the rev-5
style system applies to enumerations and statements.
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

# ---------------------------------------------------------------- the beats
# HOOK line 1 stays clean on Dan -- the cue says [SKIP STOPPER - DAN TO CAMERA],
# and the tight pass is forbidden from splicing inside it.
LOWER3A  = (at("AI has made human personal"), at("And in the next few minutes"))
ROBOTCUT = (at("And in the next few minutes"), end_of("free AI tools"))
SPACLIP  = (at("In fact my first channel"),    end_of("history of YouTube"))
_wt      = at("So let's talk about why AI")
WHYCARD  = (_wt, end_of("including me", after=_wt))
NUM1     = (at("Number one human trainers"),   end_of("bucks an hour"))
COSTCARD = (at("AI is free or very cheap"),    end_of("home gym setup"))
ROBOTSTORY=(at("Number two human trainers"),   end_of("generic plan every time"))
NUM3     = (at("Number three AI gives you"),   end_of("the actual science"))
BROCARD  = (at("They're passing along"),       end_of("10 years ago"))
NUM4     = (at("And number four this is"),     end_of("once a week or maybe even less"))
ADAPTMID = (at("If you tweak your shoulder"),  end_of("for that instantly"))
TOOLATE  = (at("By the time you talk"),        end_of("too late to matter"))
BEFORE   = (at("This is what I looked like"),  end_of("unhealthy dad bod"))
GOALIMG  = (at("But then I used AI to generate"), end_of("goal image of myself"))
TODAY    = (at("Then I had AI generate a training"), end_of("what I look like today"))
_c1      = at("Tap the button below to generate")
CTA1     = (_c1, end_of("stubborn stomach fat", after=_c1))
HOWCARD  = (at("So let me show you exactly"),  end_of("how this works"))
APPGEN   = (at("First you upload a picture"),  end_of("actually stick"))
ASSESS   = (at("Then the AI scans both pictures"), end_of("hit that goal"))
TAILOR   = (at("It also identifies your strong"), end_of("like your goal picture"))
PLANBUL  = (at("And it designs the whole plan"), end_of("you can really train"))
WORKOUT  = (at("then once you get your plan"), end_of("is with you at every workout"))
DEMOS    = (at("with videos showing you"),     end_of("every single exercise"))
GYMQ     = (at("And you can get any exercise"), end_of("right there in the gym"))
ADAPTS   = (at("And your plan adapts on the fly"), end_of("for that too"))
NOTPRICE = (at("That is not something a human"), end_of("not at any price"))
_c2      = at("So generate your future self image")
CTA2     = (_c2, round(DUR,3))

BEATS={k:v for k,v in sorted(globals().items())
       if k.isupper() and isinstance(v,tuple) and len(v)==2 and k!="BEATS"}
for _k,(_a,_b) in BEATS.items():
    assert _b>_a, f"{_k} has non-positive duration {_a}->{_b}"
# Beats must not overlap. at() pads -0.06 and end_of() pads +0.10, so back-to-back
# beats routinely touch by up to 0.16 s; trim the earlier one rather than fail. A real
# overlap (a mis-anchored phrase) is bigger than that and still asserts.
_o=sorted(BEATS.items(), key=lambda kv: kv[1][0])
for (n1,(a1,b1)),(n2,(a2,b2)) in zip(_o,_o[1:]):
    ov=b1-a2
    assert ov<=0.25, f"{n1} {a1}-{b1} overlaps {n2} {a2}-{b2} by {ov:.2f}s"
    if ov>0:
        BEATS[n1]=(a1,round(a2-0.01,3)); globals()[n1]=BEATS[n1]
# Close sub-0.35 s gaps between consecutive beats: two frames of bare footage between
# two full-screen cards reads as a flash, not as an edit.
_o=sorted(BEATS.items(), key=lambda kv: kv[1][0])
for i,((n1,(a1,b1)),(n2,(a2,b2))) in enumerate(zip(_o,_o[1:])):
    if 0 < a2-b1 < 0.35:
        BEATS[n1]=(a1,round(a2,3)); globals()[n1]=BEATS[n1]
_o=sorted(BEATS.items(), key=lambda kv: kv[1][0])

# OVERLAY beats keep Dan on screen (a lower-third bar sits over the footage); only
# FULL-screen cards and video/panel inserts actually replace him. Coverage is measured
# on the latter, which is what the 58% reference figure counts.
OVERLAY={"LOWER3A","NUM1","NUM3","NUM4","TOOLATE","GYMQ","NOTPRICE"}
PANEL  ={"COSTCARD","TAILOR","PLANBUL","ADAPTS","ADAPTMID"}   # left panel, Dan still right

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
    print(f"insert/graphic coverage    {full/DUR*100:.0f}%  (reference editor 58%)")
    print(f"Dan fully replaced         {hard/DUR*100:.0f}%")
    bare=[]; prev=0.0
    for k,(a,b) in _o:
        if a-prev>0.05: bare.append((prev,a))
        prev=b
    if DUR-prev>0.05: bare.append((prev,DUR))
    print(f"longest bare stretch       {max((b-a for a,b in bare),default=0):.1f}s  (rule: nothing unchanged >25s)")
