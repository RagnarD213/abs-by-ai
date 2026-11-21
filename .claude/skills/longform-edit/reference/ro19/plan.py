"""RO-19 "My First Spray Tan" visual plan (8/3 kitchen doorway roll C1512, 18:47). Every item is
anchored to the words Dan says (phrase -> output time via words_out.json). HyperFrames templates (from_plan.py): lt
(Motivation lower third). clip = full-frame cutaway, hard cuts. Order of preference: Dan's own B-roll, existing library
clips (A#### AI, B#### stock/B-roll), Pexels stock (ro20/stock/), then new AI (frames first, $5 for the whole film).
No side-list cards: the roll is a centred waist-up medium at 1080p with no free wall (RO-06 / RO-07 trap), so lists land as
lower thirds whose parts come up on the words. Title case; FULL CAPS only on the rare word that carries the punch.
The plan is written in parts (plan_parts/pNN_*.py, each defines PART = [...]), in film order."""
import glob, os
HERE = os.path.dirname(os.path.abspath(__file__))
W = "/Volumes/Extreme/_edit_work/ro19"
SHOOT = "/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera"
AI = f"{W}/aiframes"; ST = f"{W}/stock"
def br(roll, t): return f"{SHOOT}/{roll}.MP4@{t}"
def stock(name, t=0.0): return f"{ST}/{name}@{t}"
DAN = dict(people="dan", physique=False)          # real MOVING footage of Dan: no photo label applies
OTHER = dict(people="other", physique=False)
NONE = dict(people="none", physique=False)
AIL = dict(label="AI-GENERATED")
def _period(it):
    """part e wrote sentence points without the full stop the other parts use; section labels (BUY n OF 7) stay bare"""
    if it["kind"] == "lt" and len(it["point"].split()) >= 5 and it["point"][-1] not in ".?!" and " OF " not in it["topic"]:
        it["point"] += "."; it["parts"][-1][0] += "."
    return it
PLAN = []
ONLY = [x for x in os.environ.get("RO19_PARTS", "").split(",") if x]      # e.g. RO19_PARTS=p00 while later parts are still being written
for f in sorted(glob.glob(f"{HERE}/plan_parts/p[0-9][0-9]_*.py")):
    if ONLY and os.path.basename(f)[:3] not in ONLY: continue
    g = dict(br=br, stock=stock, DAN=DAN, OTHER=OTHER, NONE=NONE, AIL=AIL, AI=AI, ST=ST, W=W)
    exec(compile(open(f).read(), f, "exec"), g); PLAN += g["PART"]
ids = [p["id"] for p in PLAN]; assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
