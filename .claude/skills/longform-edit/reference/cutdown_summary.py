#!/usr/bin/env python3
"""Per-section duration table for both variants against v3 and the handoff's
beat-map targets — the sheet Dan reads next to the two files."""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SRC = Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/"
           "Media/longform-raw/absbyai-0803-shoot/invest-health")
SEC = [
 (1,"Intro + halo setup",2.8,104,40,25),(2,"Job / partnership",111,156,40,25),
 (3,"Relationship / divorce",178,268,60,35),(4,"Dating",274,378,65,40),
 (5,"Productivity + meal service",387,495,70,45),(6,"Doctor time-cost",500,549,30,20),
 (7,"Long-term thinking",555,614,45,25),(8,"Mental health spiral",624,730,70,40),
 (9,"Bad health is expensive",738,805,45,30),(10,"Diabetes friend story",811,916,90,60),
 (11,"Money-dead + inheritance",921,1002,50,35),(12,"Not-dead-but-sick",1007,1149,85,45),
 (13,"Brokie pivot",1174,1222,40,35),(14,"Never-cut list",1227,1293,50,35),
 (15,"Bars & clubs",1306,1458,80,50),(16,"Restaurants (+ AbsByAI plug)",1464,1565,70,45),
 (17,"Junk food",1570,1606,32,28),(18,"Vacations",1612,1690,55,35),
 (19,"Therapy & psych meds",1694,1754,50,0),(20,"Sacrifice recap",1767,1817,30,25),
 (21,"Brokie tier",1844,2077,150,100),(22,"Premium protein + 401k",2089,2257,120,80),
 (23,"Mattress + Purple + fluids",2269,2490,145,70),(24,"Gym membership",2498,2629,90,60),
 (25,"Sleep tracker",2664,2779,80,55),(26,"GLP-1",2784,2962,130,90),
 (27,"TRT",2967,3047,55,35),(28,"Supplements big-3",3056,3219,110,70),
 (29,"Home gym + both worlds",3234,3405,115,70),(30,"Meal prep / chef",3415,3537,85,55),
 (31,"Outsource chores",3546,3587,35,25),(32,"Trainer & nutritionist",3595,3682,65,40),
 (33,"Mega-baller + Bryan Johnson",3695,3834,90,60),(34,"Summary",3839,3963,70,40),
 (35,"Outro CTA",4062,4127,64,50),
]
def load(p): return json.load(open(p))["ranges"]
R = {"v3": load(SRC/"edit"/"edl.json"), "cons": load(HERE/"cons"/"edl.json"),
     "sub30": load(HERE/"sub30"/"edl.json")}
def dur(rs, a, b): return sum(min(r["end"],b)-max(r["start"],a) for r in rs if r["end"]>a and r["start"]<b)
rows = []
print(f"{'#':>2} {'section':30s} {'v3':>7} {'cons':>7} {'(tgt)':>6} {'sub30':>7} {'(tgt)':>6}")
for n, name, a, b, ct, st in SEC:
    v, c, s = dur(R["v3"],a,b), dur(R["cons"],a,b), dur(R["sub30"],a,b)
    print(f"{n:2d} {name:30s} {v:7.1f} {c:7.1f} {'('+str(ct)+')':>6} {s:7.1f} {'('+str(st)+')':>6}")
    rows.append((n,name,v,c,ct,s,st))
for k in ("v3","cons","sub30"):
    t = sum(r["end"]-r["start"] for r in R[k])
    print(f"{k:>6}: {t:8.1f}s = {int(t//60)}:{int(t%60):02d}   ({len(R[k])} ranges)")
