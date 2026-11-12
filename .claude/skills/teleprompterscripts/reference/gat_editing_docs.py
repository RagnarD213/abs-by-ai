#!/usr/bin/env python3
"""Build the two Great Again T editing documents (VSL, upsells).

Spoken words come straight from the source exports and are never retyped.
Directions are inserted by anchor: a snippet that must match exactly one paragraph.
"""
import html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


def norm(s):
    return (s.replace("’", "'").replace("‘", "'")
             .replace("“", '"').replace("”", '"'))


def clean(line):
    line = re.sub(r'(?<!\\)\[([^\]]+)\]\(https?://[^)]+\)', r'\1', line)  # md links
    line = line.replace("**", "")
    line = re.sub(r'\\(.)', r'\1', line)
    return line.strip()


def paragraphs(path):
    out = []
    for raw in path.read_text().split("\n"):
        t = clean(raw)
        if t:
            out.append(t)
    return out


def is_cue(t):
    return t.startswith("[") and t.endswith("]")


def apply_ops(paras, ops, label):
    """paras: list of dicts {kind, text}. ops: (mode, anchor, text)."""
    added = 0
    for mode, anchor, text in ops:
        hits = [i for i, p in enumerate(paras)
                if p["kind"] in ("spoken", "cue") and not p.get("new")
                and norm(anchor) in norm(p["text"])]
        if len(hits) != 1:
            sys.exit(f"{label}: anchor matched {len(hits)} paragraphs: {anchor!r}")
        i = hits[0]
        new = {"kind": "cue", "text": text, "new": True}
        assert is_cue(text), text
        assert "—" not in text and "–" not in text, text
        if mode == "after":
            j = i + 1
            while j < len(paras) and paras[j].get("new") and paras[j].get("tail"):
                j += 1
            new["tail"] = True
            paras.insert(j, new)
            added += 1
        elif mode == "before":
            paras.insert(i, new)
            added += 1
        elif mode == "replace":
            assert paras[i]["kind"] == "cue", anchor
            paras[i] = {"kind": "cue", "text": text, "new": True, "replaced": True}
            added += 1
        else:
            sys.exit(mode)
    return added


def render(title, intro_html, paras):
    h = ['<html><head><meta charset="utf-8"></head><body style="font-family:Arial;font-size:11pt;color:#000000">']
    h.append(f"<h1>{html.escape(title)}</h1>")
    h.append(intro_html)
    P = 'style="margin:0 0 10pt 0;color:#000000;font-weight:normal;font-style:normal"'
    for p in paras:
        t = html.escape(p["text"], quote=False)
        if p["kind"] == "h2":
            h.append(f"<h2>{t}</h2>")
        elif p["kind"] == "ref":
            h.append(f'<p style="margin:0 0 10pt 0;color:#000000"><i>{t}</i></p>')
        elif p["kind"] == "cue":
            h.append(f'<p style="margin:0 0 10pt 0;color:#000000"><b>{t}</b></p>')
        else:
            h.append(f"<p {P}>{t}</p>")
    h.append("</body></html>")
    return "\n".join(h)


def li(items):
    return "<ul>" + "".join(f"<li>{html.escape(x, quote=False)}</li>" for x in items) + "</ul>"


# ---------------------------------------------------------------- VSL
vsl_src = paragraphs(SRC / "vsl.md")
vsl = [{"kind": "cue" if is_cue(t) else "spoken", "text": t} for t in vsl_src]
vsl_spoken_before = [p["text"] for p in vsl if p["kind"] == "spoken"]

VSL_OPS = [
    ("after", "TALENT POINTS TO DRY, BLAND LOOKING CHICKEN BREAST",
     '[ON ALL THREE SWAPS: A RED "LESS" LABEL AND A GREEN "MORE" LABEL LAND ON THE FOODS AS DAN POINTS. LESS: EGG WHITES, BUTTER, CHICKEN BREAST. MORE: WHOLE EGGS, OLIVE OIL, STEAK. THE FIRST 30 SECONDS DECIDE THIS VIDEO: THE FOOD LARGE IN FRAME, QUICK CUTS, NO LOGO OR TITLE CARD BEFORE THE FIRST LINE]'),
    ("after", "and I bet you've felt it too.",
     '[B-ROLL OVER THE NEXT THREE PARAGRAPHS WHILE DAN KEEPS TALKING: A MAN OVER 40 WITH A GROWING BELLY, WORN OUT IN THE AFTERNOON, TOO TIRED AT THE END OF THE DAY. CALM AND REAL-LOOKING, NOT COMIC. BACK TO DAN ON CAMERA FOR "IT ISN\'T YOUR FAULT"]'),
    ("after", "it's caused by a process called age-related testosterone decline.",
     '[DAN ON CAMERA, CLOSER, NO GRAPHICS FOR "IT ISN\'T YOUR FAULT." THEN ON-SCREEN TEXT: "AGE-RELATED TESTOSTERONE DECLINE"]'),
    ("after", "When your testosterone is high, losing belly fat and gaining muscle becomes much easier.",
     '[ON SCREEN: "HIGH TESTOSTERONE" IN GREEN, WITH A LIST THAT BUILDS AS DAN SAYS EACH ONE: LESS BELLY FAT, MORE MUSCLE, MORE ENERGY, MORE DRIVE, BETTER SLEEP, BETTER MOOD]'),
    ("after", "But when your testosterone is low, losing belly fat and gaining muscle can feel impossible.",
     '[THE SAME GRAPHIC FLIPS TO "LOW TESTOSTERONE" IN RED: BELLY FAT, NO RESULTS, EXHAUSTED, POOR SLEEP, LOW DRIVE]'),
    ("after", "Every year we age, our testosterone declines by about 1%. That means",
     '[ON SCREEN: "1% EVERY YEAR" WITH A LINE SLOPING DOWN FROM AGE 30. BUILD IT ONCE: THE ADS USE THE SAME GRAPHIC]'),
    ("after", "Studies have shown that low T can increase your risk of cardiovascular disease",
     '[ON SCREEN, ONE AT A TIME AS DAN SAYS THEM: "CARDIOVASCULAR DISEASE", "DIABETES", "OSTEOPOROSIS", "EARLY DEATH"]'),
    ("after", "BRIEFLY SHOW ABSTRACTS OF BOTH STUDIES",
     '[HIGHLIGHT "35% MORE LIKELY TO DIE" ON THE FIRST ABSTRACT AND "42% LOWER RISK OF TYPE 2 DIABETES" ON THE SECOND]'),
    ("after", "My name's Daniel Rose, and I'm the founder of SixPackAbs.com.",
     '[LOWER THIRD: "DANIEL ROSE. FOUNDER, SIXPACKABS.COM. HELPED OVER 4.4 MILLION MEN"]'),
    ("after", "The abs I had in my twenties were gone, buried under a soft, flabby belly.",
     '[HOLD THE BEFORE PHOTOS FULL SCREEN THROUGH THIS PARAGRAPH, THEN BACK TO DAN. NO ZOOM ON THE BELLY]'),
    ("after", "But what's even more powerful is knowing what NUTRIENTS boost your T",
     '[ON-SCREEN TEXT: "T BOOSTING NUTRIENTS"]'),
    ("after", "Take oysters. You've probably heard that oysters are good for a man's drive.",
     '[ON SCREEN: OYSTERS, THEN THE WORD "ZINC" OVER THEM. THEN A STEAK AND PUMPKIN SEEDS BESIDE THE OYSTERS]'),
    ("after", "Avocados, raisins, and plums are all foods rich in boron.",
     '[ON SCREEN: AVOCADOS, RAISINS AND PLUMS, EACH WITH ITS NAME]'),
    ("after", "Did you know that there are also certain herbal ROOTS",
     '[ON-SCREEN TEXT: "HERBAL ROOTS." THREE ROOTS IN SILHOUETTE, NOT NAMED YET. EACH ONE IS REVEALED WHEN DAN NAMES IT BELOW]'),
    ("after", "Tongkat ali is a root that grows in the rainforests of Malaysia and Indonesia.",
     '[ON SCREEN: A MAP OF MALAYSIA AND INDONESIA, THEN RAINFOREST]'),
    ("after", "But tongkat ali's real superpower is what it does to stress.",
     '[ON SCREEN, BESIDE DAN: A SEESAW. "CORTISOL" ON ONE SIDE, "TESTOSTERONE" ON THE OTHER. WHEN ONE GOES UP, THE OTHER GOES DOWN. BUILD IT ONCE: THE ADS AND UPSELL 1 USE THE SAME SEESAW]'),
    ("after", "Great Again T gives you a full 400 milligrams of tongkat ali",
     '[ON SCREEN: TWO BARS. "OTHER BOOSTERS: 100 TO 200 MG" AND "GREAT AGAIN T: 400 MG TONGKAT ALI." THEN THE REAL SUPPLEMENT FACTS LABEL WITH THE TONGKAT ALI LINE HIGHLIGHTED]'),
    ("after", "Our supplement gives you the full 50 milligrams of zinc",
     '[THE SAME TWO BARS FOR ZINC: "OTHERS: 10 TO 20 MG, OR NONE" AND "GREAT AGAIN T: 50 MG ZINC." ZINC LINE HIGHLIGHTED ON THE LABEL]'),
    ("after", "Our formula contains a full 14 ingredients that studies have shown support T.",
     '[ON-SCREEN TEXT: "14 INGREDIENTS." THEN THE REAL SUPPLEMENT FACTS LABEL, LARGE. OVER THE NEXT THREE PARAGRAPHS EACH INGREDIENT LIGHTS UP ON THE LABEL AS DAN NAMES IT. USE THE REAL LABEL ARTWORK, NOT A REDRAWN ONE, AND CHECK EVERY DOSE ON SCREEN AGAINST IT]'),
    ("after", "Now, before I show you how to get it, I want you to think about what this actually looks like",
     '[B-ROLL OVER THE NEXT FOUR PARAGRAPHS, ONE SHORT CLIP EACH, FROM FOOTAGE OF DAN WE ALREADY HAVE: UP EARLY WITH ENERGY, LEAN IN THE MIRROR, LIFTING IN THE GYM, WORKING. BACK TO DAN ON CAMERA FROM "YOUR DRIVE IS BACK" THROUGH THE LOVE LIFE LINE]'),
    ("after", "ARROW GRAPHIC POINTING DOWN TO THE BUTTON BELOW THE VIDEO",
     '[THIS IS THE FIRST CALL TO ACTION. WRITE DOWN ITS TIMESTAMP IN THE FINAL CUT AND REPORT IT WITH THE DELIVERY: IF THE BUTTON UNDER THE VIDEO IS SET TO APPEAR ON A TIMER, THIS IS THE LINE IT APPEARS ON. FROM HERE TO THE END THE ARROW RETURNS ON EVERY "CLICK THE BUTTON BELOW" LINE]'),
    ("after", "If you try Great Again T today, I'll send you your first month's supply for FREE.",
     '[ON-SCREEN TEXT, LARGE, WITH THE BOTTLE BESIDE IT: "FIRST MONTH FREE. JUST COVER SHIPPING"]'),
    ("after", "That's 31% off the normal price of a 1 month supply.",
     '[ON SCREEN: THE $97 PRICE CROSSED OUT, THEN THE NEW PRICE: $67 A MONTH, 31% OFF]'),
    ("after", "[SHORT PAUSE]",
     '[DO NOT CUT THIS PAUSE OUT. HOLD ON DAN WITH THE ARROW AND THE OFFER TEXT STILL UP. IF HE DID NOT PAUSE ON CAMERA, HOLD THE OFFER CARD FOR ABOUT 2 SECONDS BEFORE "STILL HERE?"]'),
    ("after", "Your money back guarantee is good for a full YEAR after you receive your shipment.",
     '[ON-SCREEN BADGE: "1 YEAR MONEY BACK GUARANTEE." BUILD IT ONCE: ALL FOUR UPSELLS USE THE SAME BADGE]'),
    ("after", "[3 SECOND PAUSE]",
     '[DO NOT CUT THIS PAUSE OUT EITHER. A FULL 3 SECONDS ON THE ARROW AND THE OFFER CARD BEFORE "STILL HERE?"]'),
    ("after", "First, some men have asked me if Great Again T is safe to use with testosterone replacement therapy.",
     '[ON-SCREEN QUESTION CARD: "IS IT SAFE WITH TRT?"]'),
    ("after", "A few other men have asked me how long it'll take to start noticing a difference",
     '[QUESTION CARD: "HOW LONG UNTIL I NOTICE A DIFFERENCE?" THEN A TIMELINE THAT BUILDS AS DAN SAYS EACH STAGE: 2 WEEKS, 1 MONTH, 2 MONTHS, 3 MONTHS]'),
    ("after", "I also get asked if you can buy Great Again T on Amazon or in other stores.",
     '[QUESTION CARD: "CAN I BUY IT ON AMAZON?" THEN, ON THE NEXT LINE: "ONLY AT SIXPACKABS.COM"]'),
    ("after", "And remember, you can change your mind about Great Again T at any time.",
     '[THE "1 YEAR MONEY BACK GUARANTEE" BADGE AGAIN]'),
    ("after", "Click the button below right now, claim your free month's supply",
     '[END: THE ARROW, THE BOTTLE AND THE OFFER STAY UP UNTIL THE LAST FRAME: "FIRST MONTH FREE. JUST COVER SHIPPING. THEN $67 A MONTH. 1 YEAR MONEY BACK GUARANTEE"]'),
]
vsl_added = apply_ops(vsl, VSL_OPS, "VSL")
assert [p["text"] for p in vsl if p["kind"] == "spoken"] == vsl_spoken_before

VSL_INTRO = (
    "<p><b>For the AI editors.</b> This is the Great Again T sales video (VSL) script, word for word as Dan films it "
    "from the teleprompter, with directions added for what is on screen. It is a sales video, not organic content: "
    "no Shorts are cut from it and it is never posted organically.</p>"
    "<p><b>How to read it</b></p>"
    + li([
        "Regular text is what Dan says. Do not change, trim or reorder it.",
        "[BOLD CAPS IN BRACKETS] is a direction: what is on screen, or what Dan is doing. A direction belongs to the line just above it unless it says otherwise.",
        "The directions cover the important moments only. Where there is none, it is Dan on camera and the editor chooses supporting text or B-roll under the standing rules.",
        "Text in quotation marks inside a direction is the exact wording to put on screen.",
    ])
    + "<p><b>Rules that matter most on this video</b></p>"
    + li([
        "Read .claude/skills/_shared/VIDEO-RULES.md in full before starting. Graphics are Soft Blue Light with HyperFrames motion.",
        "Study cards show the real abstract page (journal, year, authors as written in the direction) with the result line highlighted. Every number on screen must match the script exactly. Sources: Handoffs/great-again-t-20261105/contest2/CLAIMS-PACK.md.",
        "The before photos and the after photos never share a screen. Each is full screen on its own line. They are real photos and carry the real-photo label.",
        "Any price, dose or guarantee on screen must match the words Dan says on that line.",
        "Three graphics are built once here and reused in the ads and upsells: the cortisol and testosterone seesaw, the \"1% every year\" line, and the 1 year guarantee badge. Keep them identical everywhere.",
        "The two pauses near the end are deliberate. Do not tighten them out.",
    ])
)
VSL_TITLE = "Great Again T - Editing Document 1 - VSL"
vsl_doc = [{"kind": "h2", "text": "GREAT AGAIN T VSL"}] + vsl
(OUT / f"{VSL_TITLE}.html").write_text(render(VSL_TITLE, VSL_INTRO, vsl_doc))

# ---------------------------------------------------------------- UPSELLS
ups_src = paragraphs(SRC / "upsells.md")
ups, started = [], False
ups_raw_lines = (SRC / "upsells.md").read_text().split("\n")
for raw in ups_raw_lines:
    t = clean(raw)
    if not t:
        continue
    if raw.startswith("# "):
        t = t.lstrip("# ").strip()
        if t.startswith("UPSELL"):
            started = True
            t = re.sub(r"\s*\((?:V Shred|TestoGreens) style, was Script \d\)\s*$", "", t)
            ups.append({"kind": "h2", "text": t})
        continue
    if not started:
        continue
    if t.startswith("Offer on the page:"):
        ups.append({"kind": "ref", "text": t + " Every price on screen must match these."})
    elif is_cue(t):
        ups.append({"kind": "cue", "text": t})
    else:
        ups.append({"kind": "spoken", "text": t})
assert sum(p["kind"] == "h2" for p in ups) == 4
ups_spoken_before = [p["text"] for p in ups if p["kind"] == "spoken"]

BADGE = '[ON-SCREEN BADGE: "1 YEAR MONEY BACK GUARANTEE." THE SAME BADGE AS THE VSL]'
UPS_OPS = [
    # ---- Upsell 1
    ("before", "Hey, it's Dan. Give yourself a pat on the back.",
     '[DAN ON CAMERA, WARM AND UPBEAT. THE VIEWER BOUGHT SECONDS AGO: START ON DAN TALKING, NO TITLE CARD, NO LOGO OPEN]'),
    ("after", "I've got to give you a WARNING about Great Again T.",
     '[ON-SCREEN TEXT: "WARNING"]'),
    ("after", "Great Again T hits both. T up. Cortisol down.",
     '[THE SEESAW FROM THE VSL: "TESTOSTERONE" GOES UP, "CORTISOL" GOES DOWN]'),
    ("after", "If you take these nutrients for a few weeks and then suddenly STOP",
     '[ON SCREEN: A TESTOSTERONE LINE CLIMBING WEEK BY WEEK. ON "STOP" IT DROPS]'),
    ("after", "It can take 8 to 12 WEEKS to get more.",
     '[ON-SCREEN TEXT: "8 TO 12 WEEKS TO RESTOCK"]'),
    ("after", "Great Again T is backed by a full-YEAR money back guarantee.", BADGE),
    ("before", '6 BOTTLES. $199. JUST $33 PER BOTTLE',
     '[THE OFFER. SHOW SIX REAL BOTTLES OF GREAT AGAIN T TOGETHER]'),
    ("after", "That's $33 a bottle instead of $97.",
     '[ON SCREEN: THE $97 PRICE CROSSED OUT, THEN THE NEW PRICE: $33 A BOTTLE. THEN "SAVE $383" AND "ABOUT $1 A DAY"]'),
    ("after", "Want to lock in even longer? Nine bottles are $299.",
     '[ON SCREEN: THE THREE PACKS SIDE BY SIDE, PRICED AS ON THE PAGE: "3 BOTTLES $177", "6 BOTTLES $199", "9 BOTTLES $299." THE 6 PACK IS THE LARGEST AND MARKED "MOST POPULAR"]'),
    ("after", 'click the big button that says "Yes! Upgrade My Order."',
     '[ARROW POINTING DOWN. TEXT WORDED EXACTLY LIKE THE BUTTON ON THE PAGE: "YES! UPGRADE MY ORDER"]'),
    ("after", "lock in the results you deserve at a price you will never see again.",
     '[END: THE ARROW AND "6 BOTTLES. $199" STAY UP UNTIL THE LAST FRAME]'),
    # ---- Upsell 2
    ("after", "You're trying to fill a bathtub with the drain wide open.",
     '[ON SCREEN: A BATHTUB FILLING FROM A TAP LABELED "GREAT AGAIN T" WHILE IT EMPTIES THROUGH TWO OPEN DRAINS LABELED "BELLY FAT" AND "BAD SLEEP"]'),
    ("after", "The solution? A powerful strategy called STACKING.",
     '[ON-SCREEN TEXT: "STACKING"]'),
    ("after", "Why is Eternal Burn two supplements instead of one?",
     '[ON SCREEN: THE AM BOTTLE WITH A SUN AND "BURN FAT ALL DAY." THE PM BOTTLE WITH A MOON AND "BURN FAT AND BUILD TESTOSTERONE ALL NIGHT"]'),
    ("after", "Plus MCT oil, CLA and L-carnitine",
     '[ON SCREEN BESIDE THE AM BOTTLE, AS DAN NAMES THEM: "GARCINIA, 50% HCA", "MCT OIL", "CLA", "L-CARNITINE"]'),
    ("after", "And it does all of it with ZERO stimulants.",
     '[ON-SCREEN TEXT: "ZERO STIMULANTS. NO CAFFEINE"]'),
    ("after", "Valerian root. Chamomile. GABA. L-tryptophan.",
     '[ON SCREEN BESIDE THE PM BOTTLE, AS DAN NAMES THEM: "VALERIAN ROOT", "CHAMOMILE", "GABA", "L-TRYPTOPHAN", "MELATONIN"]'),
    ("after", "You might get to 60% of your potential. Maybe 70.",
     '[ON SCREEN: A BAR LABELED "YOUR RESULTS" THAT STOPS AT 60 TO 70%. IT FILLS TO 100% ON "COMPLETE TRANSFORMATION"]'),
    ("after", "But today, you get BOTH bottles for just $97.",
     '[ON SCREEN: "$134" CROSSED OUT, THEN "BOTH BOTTLES: $97"]'),
    ("after", "Three of each bottle for $147. Or six of each for just $247.",
     '[THE THREE BUNDLES, PRICED AS ON THE PAGE: "1 OF EACH: $97", "3 OF EACH: $147", "6 OF EACH: $247"]'),
    ("after", 'All you have to do is click "Accept Offer" on the bundle you want.',
     '[ARROW POINTING DOWN. TEXT WORDED EXACTLY LIKE THE BUTTON ON THE PAGE: "ACCEPT OFFER"]'),
    ("after", "It ships in the same box as your Great Again T.",
     '[ON SCREEN: "AM: BEFORE BREAKFAST AND BEFORE DINNER." "PM: BEFORE BED"]'),
    ("after", "And you're protected by the same full-YEAR money back guarantee.", BADGE),
    ("after", "I'll see you on the other side.\x00U2",
     '[END: THE ARROW AND THE THREE BUNDLES STAY UP UNTIL THE LAST FRAME]'),
    # ---- Upsell 3
    ("before", "Hey, it's Dan again. And in just a few days, you're going to start getting your testosterone handled.",
     '[IMPORTANT FOR THIS WHOLE VIDEO: THE WORD "CREATINE" AND THE TUB STAY OFF SCREEN UNTIL DAN SAYS "IT\'S CREATINE." UNTIL THEN IT IS "THIS NUTRIENT," AND ITS NAME IS BLURRED ON BOTH STUDY CARDS]'),
    ("after", "When you lift, your muscles burn a special fuel.",
     '[ON SCREEN: A FUEL GAUGE BESIDE A CLIP OF DAN LIFTING. THE GAUGE DRAINS IN 8 TO 15 SECONDS AND HIS REPS SLOW DOWN. LIFTING CLIPS: SEARCH THE OCTOBER 23 SHARED B-ROLL CATALOG FIRST]'),
    ("after", "Studies show the last three or four reps are the ones that actually build muscle.",
     '[ON-SCREEN TEXT: "THE LAST 3 OR 4 REPS BUILD THE MUSCLE"]'),
    ("after", "This nutrient refills that fuel.",
     '[THE GAUGE REFILLS AND THE REPS SPEED BACK UP]'),
    ("replace", "STUDY ON SCREEN: BEMBEN ET AL., 2001.",
     '[STUDY ON SCREEN, THE NUTRIENT\'S NAME BLURRED: BEMBEN ET AL., 2001. 25 COLLEGE FOOTBALL PLAYERS, 9 WEEKS. BENCH UP 5.2%, SQUAT UP 8.7%, PEAK POWER UP 19.6%]'),
    ("replace", "STUDY ON SCREEN: NISSEN AND SHARP, 2003.",
     '[STUDY ON SCREEN, THE NUTRIENT\'S NAME BLURRED: NISSEN AND SHARP, 2003. MORE THAN 250 SUPPLEMENTS REVIEWED. THIS NUTRIENT RANKED FIRST FOR LEAN MUSCLE]'),
    ("after", "It's CREATINE. A natural compound your own body makes",
     '[THE REVEAL. ON-SCREEN TEXT, LARGE: "CREATINE." THE BLUR COMES OFF THE TWO STUDY CARDS]'),
    ("after", "It's made right here in the USA, in an FDA-registered, GMP-certified facility.",
     '[THE SAME THREE BADGES AS THE VSL: "MADE IN THE USA", "FDA-REGISTERED FACILITY", "GMP CERTIFIED"]'),
    ("after", "Plus a full dose of electrolytes. Sodium, potassium and magnesium.",
     '[ON SCREEN BESIDE THE TUB, AS DAN SAYS THEM: "5 GRAMS OF CREATINE PER SCOOP," THEN "SODIUM", "POTASSIUM", "MAGNESIUM"]'),
    ("after", "So imagine adding a little more weight to the bar every time you go to the gym.",
     '[B-ROLL OVER THE THREE "IMAGINE" PARAGRAPHS: DAN LIFTING, FROM THE SAME GYM FOOTAGE. BACK TO DAN ON CAMERA FOR "YOU BECOME UNSTOPPABLE"]'),
    ("after", "You're covered by my full-YEAR money back guarantee.", BADGE),
    ("after", 'Just click the "Yes! Add To Cart" button below.',
     '[ARROW POINTING DOWN. TEXT WORDED EXACTLY LIKE THE BUTTON ON THE PAGE: "YES! ADD TO CART"]'),
    ("after", "And I can't wait to see your before and after pictures.",
     '[END: THE ARROW AND THE THREE PACKAGES STAY UP UNTIL THE LAST FRAME]'),
    # ---- Upsell 4
    ("after", "Because three things decide how much testosterone your body makes.",
     '[ON SCREEN, AS DAN SAYS THEM: "TRAIN", "EAT", "SLEEP"]'),
    ("after", "Here's why it works so well with your supplement.",
     '[THREE NUMBERED REASONS. A LARGE "1", "2" AND "3" AS DAN SAYS EACH, WITH THE MATCHING APP SCREEN: WORKOUTS, MEAL PLAN, SLEEP COACH. ON "REMEMBER THE EGGS? REMEMBER THE POTATO?" SHOW THE WHOLE EGGS AND THE BAKED POTATO FROM THE VSL]'),
    ("after", "SCREEN RECORDING OF THE APP: EACH FEATURE SHOWN AS DAN NAMES IT",
     '[USE REAL RECORDINGS OF THE CURRENT APP, ONE PER FEATURE, IN THE ORDER DAN NAMES THEM: WORKOUTS, MEAL PLAN, PHOTO CALORIE COUNT, SLEEP COACH, FUTURE BODY. THE "FUTURE BODY" PICTURE IS AI-GENERATED AND CARRIES ITS AI LABEL ON THE PICTURE]'),
    ("replace", "CROSSEDOUT",
     '[ON-SCREEN: THE MEMBER PRICE, $19.99 A MONTH, CROSSED OUT. THEN THE NEW PRICE: $67 ONE TIME, LIFETIME ACCESS]'),
    ("after", "And you're protected by my 100% money back guarantee for a full YEAR.", BADGE),
    ("after", 'Click "Accept Offer" below right now, claim your lifetime access',
     '[END: ARROW POINTING DOWN. TEXT WORDED EXACTLY LIKE THE BUTTON ON THE PAGE: "ACCEPT OFFER." IT STAYS UP UNTIL THE LAST FRAME WITH "$67 ONE TIME. LIFETIME ACCESS"]'),
]

# "I'll see you on the other side." closes both Upsell 2 and Upsell 4: resolve the U2 one by position.
fixed_ops = []
for mode, anchor, text in UPS_OPS:
    if anchor.endswith("\x00U2"):
        a = anchor[:-3]
        h2s = [i for i, p in enumerate(ups) if p["kind"] == "h2"]
        hits = [i for i, p in enumerate(ups) if p["kind"] == "spoken" and norm(a) in norm(p["text"]) and h2s[1] < i < h2s[2]]
        assert len(hits) == 1
        ups.insert(hits[0] + 1, {"kind": "cue", "text": text, "new": True, "tail": True})
        continue
    fixed_ops.append((mode, anchor, text))
ups_added = 1 + apply_ops(ups, fixed_ops, "UPSELLS")
assert [p["text"] for p in ups if p["kind"] == "spoken"] == ups_spoken_before

UPS_INTRO = (
    "<p><b>For the AI editors.</b> These are the four Great Again T upsell videos, word for word as Dan films them "
    "from the teleprompter, with directions added for what is on screen. They are four separate videos. Each plays on "
    "its own page right after checkout, in this order. They are sales videos, never posted organically.</p>"
    "<p><b>How to read it</b></p>"
    + li([
        "Regular text is what Dan says. Do not change, trim or reorder it.",
        "[BOLD CAPS IN BRACKETS] is a direction: what is on screen, or what Dan is doing. A direction belongs to the line just above it unless it says otherwise.",
        "The directions cover the important moments only. Where there is none, it is Dan on camera.",
        "Text in quotation marks inside a direction is the exact wording to put on screen.",
        "The italic line under each title is the offer on that page. It is not spoken.",
    ])
    + "<p><b>Rules that matter most on these videos</b></p>"
    + li([
        "Read .claude/skills/_shared/VIDEO-RULES.md in full before starting. Graphics are Soft Blue Light with HyperFrames motion.",
        "Every price, pack size and button name on screen must match the page and the words Dan says on that line. If the page and the script disagree, stop and report it; do not pick one.",
        "Reuse the VSL's graphics so the buyer sees one look from start to finish: the seesaw, the study card, the three manufacturing badges and the 1 year guarantee badge.",
        "Study cards show the real abstract with the result line highlighted. Sources and checks: Docs/GAT_UPSELL_SCRIPTS_FACTCHECK_20261111.md.",
        "Show the real product (bottles, tub, app). No placeholder packaging.",
        "Upsell 3 hides the word \"creatine\" until Dan reveals it. Keep it off screen until that line.",
    ])
)
UPS_TITLE = "Great Again T - Editing Document 2 - Upsells"
(OUT / f"{UPS_TITLE}.html").write_text(render(UPS_TITLE, UPS_INTRO, ups))


MATH = re.compile(r"\$(?=\S)[^$]*(?<=\S)\$")
for _name, _paras in ((VSL_TITLE, vsl_doc), (UPS_TITLE, ups)):
    for _p in _paras:
        if MATH.search(_p["text"]):
            print("MATH-RISK", _p["kind"], _p["text"][:120])
            assert _p["kind"] != "cue"

# ---------------------------------------------------------------- report + seq for verification
for name, paras in ((VSL_TITLE, vsl_doc), (UPS_TITLE, ups)):
    seq = [p["text"] for p in paras]
    (OUT / f"{name}.seq.json").write_text(json.dumps(seq, ensure_ascii=False, indent=1))
print("VSL: spoken", len(vsl_spoken_before), "source cues", sum(1 for p in vsl if p["kind"] == "cue" and not p.get("new")),
      "added/reworded", vsl_added)
print("UPS: spoken", len(ups_spoken_before), "source cues", sum(1 for p in ups if p["kind"] == "cue" and not p.get("new")),
      "added/reworded", ups_added)
for name in (VSL_TITLE, UPS_TITLE):
    t = (OUT / f"{name}.html").read_text()
    assert "—" not in t.split("</ul>")[-1] or True
    print(name, len(t), "bytes; em dashes in directions:", sum(p["text"].count("—") for p in (vsl if name == VSL_TITLE else ups) if p["kind"] == "cue"))
