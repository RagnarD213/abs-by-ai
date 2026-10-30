"""RO-37 round 2 page text (review/page_extra2.json), with the live numbers: scene counts from bg_plan.json, spend from the
matte ledger, check results from review/checks.json."""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2
W = r2.W2
plan = json.load(open(f"{W}/bg_plan.json"))["segments"]
led = json.load(open(f"{W}/matte/ledger.json")); spend = sum(x["usd"] for x in led)
ck = json.load(open(f"{W}/review/checks.json"))
lay = json.load(open(f"{W}/hf/lt/layout.json"))
need = r2.needed_frames(0, r2.END_F); left = sum(1 for roll, ks in need.items() for k in ks if not os.path.exists(r2.mpath(roll, k)))
cnt = collections.Counter(s["type"] for s in plan)
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
big = [f"“{' '.join(s['lines']).title()}” at {mmss(s['t0'])}" for s in plan if s["type"] == "bigtype"]
two = [g for g, v in lay.items() if v["lines"] == 2]
lt_worst = max((v["px"] for v in ck["lt"].values()), default=0)
lt_hand = [f"{g} at {mmss(v['t'])}" for g, v in ck["lt"].items() if v["px"] > 0]
X = dict(
    intro=("Round 2 rebuilds the video the way you approved on the cutout test: you are cut out of the upright pool footage in every shot "
           "and stand in front of a scene that changes on the cuts with what you are saying, mostly your own October 23 gym clips. "
           "This page has the rebuilt first minute, every scene behind you across the whole film as a still, and every graphic, gym clip "
           "and AI clip spot playing in the new layout. Colour, voice, the opener, the AI clips and weeks 2 to 4 are still open from round 1. "
           "No full film until you pick. Release: Fri Jan 1, 2027 (finished and set up by Dec 18)."),
    locked=("your cutout test look (you cut out with a soft shadow, beside a card on the moving blue, small in the corner over your gym clip); "
            "the long-form green-screen background template; round 1's cut, every word of the graphics, the gym clip picks and their "
            "colour lift; Soft Blue Light graphics; the October 23 exercise names and Color C."),
    decisions=[
        "<b>Colour</b>: <b>F Deep And Vivid</b> (recommended, your pick on Hamstring Curls and Pull-Ups, same pool, same day), E Vivid Softer, or B Richer Contrast. Stills below are in the new layout.",
        "<b>Voice</b>: <b>A Natural Warmth</b> (recommended, your pick on three Shorts from this pool) or C Original Mic (the blind listener's favourite, but its scores swung 3 to 9 on the same clip). B and D are there too.",
        "<b>Opening</b>: open on the AI clip <b>“Frozen at the gym door”</b> (A1) under “If I walked into a gym for the first time today...” (recommended), or keep you on camera there, now standing in front of the gym (the first 6 seconds of the first minute).",
        "<b>AI clips</b>: which of the six to animate (frames below; motion is free on your Flow subscription). Their spots now play in the new layout.",
        "<b>Weeks 2 to 4</b>: keep your three Workout B machine clips then the “Alternate” side list (now on the moving blue with you beside it, at 4:10 to 4:22), or build a full-screen A/B card?",
    ],
    first_minute=dict(end=61.0944, note=("Built with the recommended choices: colour F, voice A. The AI slots (the opener, “Done at hour two”, "
                                         "“Too sore for the stairs”) show you on camera, in the new layout, until their motion is approved.")),
    ai_intro=("The same six ideas as round 1, START and END frames checked by the frame gate and an independent reviewer. Approve the ones "
              "to animate; the rest leave you on camera. “Play the spot in context” now shows the spot in the round 2 layout."),
    scenes_intro=(f"{len(plan)} scenes across the whole film, one still each, in order. The scene changes only on a cut, about every 8 to 20 "
                  f"seconds, and follows what you say: your gym footage softened behind you ({cnt['soft']}), sharp behind you with you to the "
                  f"right ({cnt['side']}), still rolling with you in the corner right after a gym clip ({cnt['corner']}), stills from your gym "
                  f"footage as drifting cards ({cnt['cards']}) or a scrolling wall ({cnt['wall']}), your number huge and faint beside you "
                  f"({cnt['bigtype']}), the moving blue beside a side list ({cnt['list']}), and the pool close-up ({cnt['closeup']}). "
                  "Graphics are off in these stills; they play in context further down."),
    look_intro="The same two moments in each grade, in the new layout: wide beside the “Each Machine” list, and close in front of your softened gym footage.",
    decided=[
        "Every shot of you is cut out with the method you approved (each frame cut out separately, then smoothed over three frames), with the test's soft shadow. New since the test: a green-spill clean-up on the hair edge (the pool hedge showed through the back of your hair) and a slightly tighter edge (a faint light line on your cheek).",
        "Sizes: wide shows you hair to waistband, close is 1.35 times bigger, and every cut still changes the size or your place, so no cut is a jump. Six joins between takes under a lower third get a small push-in instead.",
        "The full-frame pool close-up appears twice in the whole film: 6:11 “I'm just keeping it real with you guys” and 7:44 “Don't worry about going hard. Just worry about showing up.” None in the first minute. No generated side footage (you said that was optional; it would need a sample first).",
        f"Lower thirds: the same words. Under one you move to the right and the strip ends left of your body, measured on every lower third; {len(two)} long ones wrap to two lines ({', '.join(two)}).",
        "Side lists (Each Machine, Alternate, How-To Videos, The Whole Plan) sit on the moving blue with you to the right, your approved test look, instead of the template's softened footage.",
        "Behind you: only your own October 23 gym clips (machines, cables, the bike, the stair climber, the sled), colour-lifted like the cutaways. The scene uses the machine you name where it can (the bike under “five minutes on the bike”), otherwise it rotates so nothing repeats close together.",
        "After the opening montage: stills of your gym clips as drifting cards, then the scrolling wall, as the template does after an intro.",
        f"Big faint numbers where you say one and no lower third shows it: {'; '.join(big)}. Your 80% line stays spoken only (round 1's call).",
        "Not used from the template: the before/after panel (nobody's transformation in this film) and the studio set (it needs a new AI set picture; the gym scenes give enough variety).",
        f"Spend this round: ${spend:.2f} for the cutouts (Replicate). The rest of the film needs about ${left * 0.002:.2f} more ({left} frames) once you lock the choices. Total for the video so far: ${spend + 0.90:.2f}.",
    ],
    checks=[
        f"Hair clearance on every cut-out frame rendered this round ({ck['hair']['frames']} frames, first minute and all context clips): closest {ck['hair']['min']} px (needs 20), {'PASS' if (ck['hair']['min'] or 0) >= 20 else 'FAIL'}. The {ck['hair'].get('missing', 0)} frames with no top-of-frame reading are all the small corner shots, where your hair sits 470 px or more below the top.",
        f"Lower thirds against your body, every third frame of each: {'no pixel of you under any strip' if lt_worst == 0 else 'a hand passes under the strip end at ' + ', '.join(lt_hand) + '; your face and abs stay clear'}.",
        f"Cuts: {len(ck['cuts']['jump'])} joins between takes with no change of size or place (jump cuts), {len(ck['cuts']['still_bg_swap'])} scene changes with you standing still.",
        "Background footage: clips chosen from tripod shots (no handheld moves behind you); the soft and side clips are graded with round 1's colour lift.",
        "Not run yet (they run on the full film after you lock the choices): the delivery gate, the audio gate stamp, the full jump-cut and junk pass, the independent reviewer.",
    ],
    reply=("Colour: F\nVoice: A\nOpening: A1 Frozen at the gym door\nAI clips to animate: A1, A2, A3, A4, A6, A7\n"
           "Weeks 2 to 4: keep the clips and side list\nFirst minute notes:\nScenes notes:\nGraphics and clips notes:\n"),
)
json.dump(X, open(f"{W}/review/page_extra2.json", "w"), indent=1)
print("extra ok")
