#!/usr/bin/env python3
"""RO-12 graphics and inserts, every one anchored to the words Dan says (source seconds on C1706; words.at()).
Soft Blue Light only (softblue.py): section titles (RO-05 title_scene), Motivation lower thirds, 3A left-third cards,
full-screen scenes for the before/now photos, the dose ramp, the weekly curve and the recap.
No drug or device brand names on screen (00-RULES: GLP-1 material). No em dashes anywhere."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from words import at
ST = "/Volumes/Extreme/_edit_work/ro12/stock"
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
PH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/photos"
BEFORE = f"{PH}/dan transformation photos/Facetune_03-04-2026-18-52-49.jpeg"   # real, March 2026 by the pool (script: the one the AI after was made from)
NOW = f"{PH}/dan transformation photos/photo-180_FINAL_PRIMARY copy.png"         # real, 7/31 pool shoot
DISC = "Not medical advice. Talk to your doctor."
s = lambda p, n: at(p, n)[0]
e = lambda p, n: at(p, n)[1]

ITEMS = [
    # ---------------------------------------------------------------- intro
    dict(id="G01", kind="lt", t0=s("so you lose fat", 104), t1=e("keeping your muscle", 107) + 2.4,
         topic="5 TIPS", point="Lose Fat FAST On A GLP-1 And KEEP YOUR MUSCLE"),
    dict(id="S01", kind="photo", photo=BEFORE, eyebrow="BEFORE", t0=s("here's what i looked like before", 112.5) - 0.05,
         t1=s("here's what i look like now", 119.3) - 0.05),
    dict(id="S01b", kind="photo", photo=NOW, eyebrow="NOW", t0=s("here's what i look like now", 119.3) - 0.05, t1=s("i look better", 123) - 0.05),
    # ---------------------------------------------------------------- tip 1
    dict(id="T01", kind="title", t0=s("number one use needles", 167.6) - 0.08, t1=e("not quick pens", 169.5) + 0.3,
         eyebrow="TIP 1 OF 5", headline="Use Needles And Vials,\nNot Pens"),
    dict(id="G02", kind="l3", t0=s("there are two ways", 171), t1=s("almost everyone", 179.3) - 0.06,
         heading="2 Ways To Inject", items=["A Syringe Filled From A Vial", "A Pen Or Auto-Injector"],
         item_t=[s("there are two ways", 171), s("or with a quick pen", 175)]),
    dict(id="I01", kind="insert", src=f"{ST}/px7579972.mp4", off=3.2, t0=s("almost everyone", 179.3) - 0.06, t1=e("handed to you", 184.5)),
    dict(id="G03", kind="lt", t0=s("and for most of you watching", 190.7), t1=e("minimum dose", 196.8) + 1.0,
         topic="KEY POINT", point="Most Of You Should Start BELOW The 2.5 mg Pen Dose"),
    dict(id="I02", kind="insert", src=f"{ST}/px8413544.mp4", off=0.2, t0=s("i have found that a dose", 211.3), t1=s("one milligram", 217.4)),
    dict(id="I02b", kind="insert", src=f"{LIB}/03 B-Roll - Real Footage/stock/other/B0352_finger-pushes-syringe-plunger-dark_16x9_19s.mp4", off=2.0, t0=s("one milligram", 217.4), t1=e("the pen would give you", 220.5)),
    dict(id="S02", kind="ramp", t0=s("for most of you watching this channel you should start", 221.3), t1=e("stepping up your dose", 231.5) + 0.2,
         steps=[("1 mg", s("start at 1 milligram", 223)), ("2 mg", s("step up to 2", 225)), ("2.5 mg", s("to 2 and a half", 226))]),
    dict(id="I03", kind="insert", src=f"{ST}/px10515019.mp4", off=2.0, t0=s("the nausea", 232.3), t1=e("feel like garbage", 235.2)),
    dict(id="G04", kind="lt", t0=259.55, t1=e("maintenance dose for me", 264.3) + 0.4,
         topic="MY DOSE", point="Maintenance: 1.5 mg A Week, Down From 2.5 mg"),
    dict(id="I04", kind="insert", src=f"{ST}/px6824226.mp4", off=1.0, t0=s("once you get good with a needle", 267.5), t1=e("you control the needle", 274.6)),
    dict(id="I05", kind="insert", src=f"{ST}/px6290576.mp4", off=4.0, t0=s("you get a vial", 292.8), t1=e("side of the barrel", 299.3)),
    dict(id="I06", kind="insert", src=f"{ST}/px7582844.mp4", off=14.0, t0=s("most of the time with", 314.7), t1=e("marks on the syringe", 322.2)),
    # ---------------------------------------------------------------- tip 2
    dict(id="T02", kind="title", t0=s("number two how to actually inject", 327.1) - 0.08, t1=e("how to actually inject", 328.5) + 0.3,
         eyebrow="TIP 2 OF 5", headline="How To Actually Inject"),
    dict(id="G05", kind="l3", t0=s("pinch the fat", 339.6), t1=e("that's the whole thing", 364.9) + 0.3,
         heading="The 10-Second Injection", items=["Outer Front Thigh, Midway Down", "Pinch A Fold Of Fat", "Needle In, Not Too Deep",
                                                   "Push The Plunger SLOWLY", "Wait 1 Second, Then Withdraw"],
         item_t=[s("pinch the fat", 339.6), s("pinch the fat", 339.6) + 0.25, s("stick the needle in", 348.6), s("inject the zip bound slowly", 356.0),
                 s("wait one second", 361.1)]),
    dict(id="G06", kind="lt", t0=s("a good stick is nearly painless", 368.2), t1=377.55,
         topic="KEY POINT", point="Blood Or Pain Means Your TECHNIQUE Was Off"),
    dict(id="I08", kind="insert", src=f"{ST}/px8413524.mp4", off=2.0, t0=391.6, t1=397.2),
    dict(id="G07", kind="lt", t0=s("rotate your sights", 400.5), t1=e("stopped working", 413.4),
         topic="KEY POINT", point="Same Spot Every Week Leads To HARD LUMPS And Weaker Doses"),
    dict(id="I09", kind="insert", src=f"{ST}/px4718397.mp4", off=2.5, t0=s("hold an ice cube", 416.5), t1=e("it numbs it", 419.5)),
    # ---------------------------------------------------------------- tip 3
    dict(id="T03", kind="title", t0=s("number three inject thursday", 426.0) - 0.08, t1=e("inject thursday evening", 428.0) + 0.3,
         eyebrow="TIP 3 OF 5", headline="Inject On Thursday Evening"),
    dict(id="S03", kind="week", t0=s("the medication is strongest", 431.8), t1=e("need the most help", 440.3) + 0.2),
    dict(id="I10", kind="insert", src=f"{ST}/px8922355.mp4", off=3.0, t0=s("that is the dinner out", 453.5), t1=s("the pizza with", 456.0)),
    dict(id="I12", kind="insert", src=f"{ST}/px8045155.mp4", off=1.0, t0=s("the pizza with", 456.0), t1=s("the nothing to do", 457.2)),
    dict(id="I13", kind="insert", src=f"{ST}/px7855731.mp4", off=4.0, t0=s("the nothing to do", 457.2), t1=e("out of boredom", 459.4)),
    dict(id="G08", kind="lt", t0=s("if you inject thursday evening", 460.0), t1=e("working worst", 469.2),
         topic="KEY POINT", point="Inject THURSDAY So It Peaks On The WEEKEND"),
    dict(id="I14", kind="insert", src=f"{ST}/px9057559.mp4", off=0.5, t0=s("whatever day you pick", 481.1), t1=e("supposed to stay steady", 486.4)),
    dict(id="G09", kind="lt", t0=s("if you're switching", 494.0), t1=e("a few extra days one time", 502.1) + 0.2,
         topic="KEY POINT", point="Switching Days? Never STACK Two Shots Close Together"),
    # ---------------------------------------------------------------- tip 4
    dict(id="T04", kind="title", t0=511.55, t1=515.9, eyebrow="TIP 4 OF 5", headline="Ramp On Slowly,\nTaper Off Even Slower"),
    dict(id="I15", kind="insert", src=f"{ST}/px4731063.mp4", off=1.0, t0=s("go off it again", 541.5), t1=e("they got the body", 547.5)),
    dict(id="G10", kind="l3", t0=562.0, t1=e("go back up 1 .5 mg", 586.0) + 0.4,
         heading="How To Taper Off", items=["Drop From 2.5 mg To 2 mg", "No Weight Gain? Go To 1.5 mg", "Keep Dropping 0.5 mg A Week At Or Below Goal",
                                            "Over Goal At All? HOLD Your Dose", "3+ lb Over Goal? Go Back Up 0.5 mg"],
         item_t=[562.0, s("if you do not gain any weight", 566.7), s("keep lowering", 570.1), s("if you go above your goal", 575.8), s("and if you gain more", 583.4)],
         disc=DISC),
    dict(id="I16", kind="insert", src=f"{ST}/px9154824.mp4", off=2.0, t0=s("walk down the stairs", 609.2), t1=e("off the roof", 611.6)),
    # ---------------------------------------------------------------- tip 5
    dict(id="T05", kind="title", t0=s("number 5", 612.2) - 0.08, t1=e("focus on protein", 614.6) + 0.3, eyebrow="TIP 5 OF 5", headline="Focus On Protein"),
    dict(id="I17", kind="insert", src=f"{LIB}/04 AI-Generated Clips/concepts-and-gags/A0058_split-screen-same-man-lean-vs-weak-gym_16x9_5s.mp4",
         off=0.0, t0=s("but studies have shown", 619.4), t1=e("on this medication", 624.2), ai=True, ai_split=True, ai_pos="bottom"),
    dict(id="I18", kind="insert", src=f"{ST}/px4745812.mp4", off=1.0, t0=s("by weight training regularly", 628.5) - 0.9, t1=631.5),
    dict(id="I19", kind="insert", src=f"{LIB}/03 B-Roll - Real Footage/dan-filmed/B0030_dan-ab-wheel-rollout-rep-poolside_16x9_8s.mp4",
         off=0.5, t0=635.6, t1=e("because of this", 639.2)),
    dict(id="G11", kind="lt", t0=s("what you're aiming for", 659.1), t1=e("lean body mass", 663.5) + 1.0,
         topic="YOUR PROTEIN TARGET", point="At Least 0.8 g Per Pound Of LEAN BODY MASS, Every Day"),
    dict(id="I20", kind="insert", src=f"{ST}/px6107302.mp4", off=3.0, t0=s("with lunch and dinner", 666.0), t1=s("rotisserie chicken", 671.9)),
    dict(id="I21", kind="insert", src=f"{LIB}/03 B-Roll - Real Footage/stock/food-nutrition/B0047_rotisserie-chicken-display-street-food_16x9_7s.mp4",
         off=1.0, t0=s("rotisserie chicken", 671.9), t1=s("sardines", 673.0)),
    dict(id="I22", kind="insert", src=f"{ST}/px6398611.mp4", off=4.5, t0=s("sardines", 673.0), t1=s("eggs", 674.8)),
    dict(id="I23", kind="insert", src=f"{LIB}/03 B-Roll - Real Footage/stock/food-nutrition/B0046_peeling-hard-boiled-egg-close-up_4096x2160_44s.mp4",
         off=30.0, t0=s("eggs", 674.8), t1=e("snacks should be protein", 677.0)),
    dict(id="I24", kind="insert", src=f"{LIB}/04 AI-Generated Clips/lifestyle/A0064_lean-man-bathroom-mirror-satisfied_16x9_8s.mp4",
         off=1.0, t0=s("the scale will go down", 701.0), t1=e("feel like it's working", 703.7), ai=True, ai_split=False),
    dict(id="G12", kind="lt", t0=s("that is the actual risk", 734.6), t1=e("nobody warned you", 743.8) + 0.3,
         topic="KEY POINT", point="The Real Risk Isn't Side Effects. It's LOSING YOUR MUSCLE"),
    dict(id="G13", kind="lt", t0=s("protecting your muscle", 744.4), t1=e("that one next", 753.8) + 0.2,
         topic="WATCH NEXT", point="How To Keep Your Muscle While You Lose Fat"),
    # ---------------------------------------------------------------- wrap
    dict(id="S04", kind="recap", t0=s("so those are your 5 tips", 754.3), t1=e("guard your protein", 769.9) + 0.3,
         items=[("Needles And Vials, Not Pens", s("needles instead of pens", 757.3)), ("Inject The Outer Thigh", s("inject correctly", 759.4)),
                ("Inject Thursday Evening", 764.17), ("Ramp On Slow, Taper Off Slower", s("ramp on slow", 766.3)),
                ("Guard Your Protein", s("guard your protein", 768.6))]),
    dict(id="G14", kind="lt", t0=822.45, t1=826.9, topic="SUBSCRIBE", point="Get My Newest Videos As Soon As They're Out"),
]

# ---------------------------------------------------------------- added for coverage (2026-09-30)
ITEMS += [
    dict(id="G16", kind="lt", t0=s("the pen exists because", 275.1), t1=e("properly with a needle", 280.9) + 0.2,
         topic="KEY POINT", point="With A Needle, YOU Control The Dose And The Speed"),
    dict(id="I27", kind="insert", src=f"{ST}/px8657614.mp4", off=2.0, t0=s("your doctor or your pharmacy", 300.0), t1=e("concentration you have", 306.1)),
    dict(id="I28", kind="insert", src=f"{ST}/px7039913.mp4", off=0.5, t0=s("friday night", 448.8), t1=e("where diets go to die", 452.9)),
    dict(id="I29", kind="insert", src=f"{ST}/px6719385.mp4", off=0.3, t0=s("you are just walking", 589.4), t1=e("when to stop", 592.9)),
    dict(id="P01", kind="phone", src=f"{LIB}/03 B-Roll - Real Footage/screen-recordings/B0035_app-meal-photo-macro-analysis-chicken-broccoli_660x1434_9s.mp4",
         off=2.6, t0=s("so track your macros", 650.6), t1=655.0),
]
ITEMS.sort(key=lambda i: i["t0"])
FLASH_AT = ["T01", "T02", "T03", "T04", "T05", "S04"]
