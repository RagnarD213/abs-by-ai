"""Writes review/page_extra.json (locks, decisions, AI pairs, what I decided, checks, reply) from the measured results. RO-14 round 1."""
import json, os
W = "/Volumes/Extreme/_edit_work/RO-14/round1"; OUT = f"{W}/review"
S = json.load(open(f"{W}/shots.json")); FPS = 30000 / 1001; film = S[-1]["out_f1"] / FPS
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def J(p, d=None): return json.load(open(p)) if os.path.exists(p) else d
fm_gate = J(f"{OUT}/first-minute/DRAFT - RO-14 round 1 - first minute.mp4.audio_gate.json", {})
fid = J(f"{OUT}/first-minute/fidelity.json", {})
hair = J(f"{OUT}/first-minute/hair.json", {})
pre = J(f"{W}/framing/hair_pre.json", {}).get("margins", {})
cy = J(f"{W}/framing/crop_y.json", {})
fm_end = J(f"{OUT}/first-minute/end.json", {}).get("end", 0)
R = {it["id"]: it for it in json.load(open(f"{W}/plan_resolved.json"))}
WO = json.load(open(f"{W}/words_out.json"))
FIVE = [w["t0"] for w in WO if w["w"].strip(".,").lower() in ("five", "5") and w["t0"] < 30]
NLT = sum(1 for it in R.values() if it["kind"] == "lt")
IC = J(f"{OUT}/INDEPENDENT-CHECK.json", {})
lifts = sorted(((162 - v["W2"]) if "W2" in v else 0, k) for k, v in cy.items())
maxlift = max([l for l, _ in lifts] + [0])

AI = [
 dict(id="A1", name="The broken scale", action="Morning, a bright bathroom. A man in gym clothes, towel on his shoulder, steps on the scale and looks down, hopeful. Then he steps off, picks the scale up and shakes it, peering at it like it must be broken. 'You are eating healthy. You are working out. But the scale will not move', acted out before you say a word of it.",
      fallback="Pexels: bare feet stepping onto a glass bathroom scale (it also plays at 1:45, so I would use a different scale clip there), or you on camera.",
      cost="6 s take, about $0.90. Recommended as the opener (decision 1)."),
 dict(id="A3", name="Smashing the piggy bank", action="Friday night at the kitchen table, a man in a loud party shirt grins and brings a hammer down on his piggy bank; it shatters, coins everywhere, and he throws a triumphant fist in the air, laughing, the pizza and the beers waiting beside it. Saving all week, blowing it all at the weekend.",
      fallback="You on camera (the week card just before it already shows the numbers).", cost="6 s take, about $0.90."),
 dict(id="A7", name="The giant drink", action="Lunch at the kitchen counter: a man sits proudly in front of a tiny side salad, then ignores it and sips, eyes closed in bliss, from a bucket-sized whipped-cream iced coffee. 'They're just drinking a thousand calories per day.'",
      fallback="You on camera.", cost="8 s take, about $1.20."),
 dict(id="A2", name="The trash-can nuggets", action="Evening in a family kitchen: a dad holds his kid's plate over the open trash can, three leftover chicken nuggets on it. Instead of scraping them in, he eats them, cheeks full, glancing at the door to check nobody saw. Covers 'the bites of your kids food, the three chicken nuggets you eat standing over the trash can'.",
      fallback="You on camera.", cost="8 s take, about $1.20."),
 dict(id="A4", name="Dessert for two", action="A candle-lit restaurant. He has a small salad; his heavier girlfriend smiles sweetly and slides a huge slice of chocolate cake across to him, then takes the fork from the plate and holds a bite out to him. He looks at it, tempted and resigned. Under 'She orders the dessert. She wants the pizza. She is the one who says you look fine.'",
      fallback="Pexels: a couple eating pizza on the couch, or you on camera.", cost="8 s take, about $1.20."),
 dict(id="A5", name="The salad guy", action="A sports bar table crowded with wings, nachos, burgers and pitchers of beer, five heavy-set guys laughing. The waiter sets a plain salad in front of the one fit guy, and the whole table goes silent and stares at it; one friend freezes with a wing halfway to his mouth. Under 'The guy ordering a salad at the table ruins the night for everyone.'",
      fallback="You on camera.", cost="6 s take, about $0.90."),
 dict(id="A6", name="Negotiating with the donut", action="The office break room. An exhausted man, bags under his eyes, coffee in hand, stands over an open box of donuts, his hand hovering, arguing with himself; then he gives in and takes a huge bite, eyes closed in defeat. Under 'On 5 hours you stand there and negotiate with yourself and eventually you lose.'",
      fallback="Library A0170 (the office donut, then asleep on the keyboard, from RO-08), or you on camera.", cost="6 s take, about $0.90."),
]

decisions = [
 "<b>Opener (0:00 to 0:05), under \"You are eating healthy. You are working out, but the scale will not move.\"</b> (a) <b>The broken scale</b> (A1, new, recommended): he steps on, stares, then picks the scale up and shakes it. (b) Pexels: bare feet stepping onto a glass scale. (c) You on camera.",
 "<b>AI clip frames: which of the 7 ideas get motion?</b> Name the ones to drop. All 7 are below with their frames and the line each plays under. Motion is about $0.15 a second (Veo 3.1 Fast): all 7 first takes about $7.20, about $10 to $13 with the retakes I expect, inside the $15 long-form cap. You said about five per video, so drop roughly two. My ranking: The trash-can nuggets, The broken scale, The salad guy, The giant drink, Negotiating with the donut, Smashing the piggy bank, Dessert for two.",
 f"<b>\"Five hidden reasons\" ({' and '.join(mmss(t) for t in FIVE)}).</b> In the intro you say \"five hidden reasons\" and \"some of those five\", and the video gives four (every take says five). Cutting the word out sounded choppy (a blind listen scored it 2 out of 10), so this round plays it as filmed. (a) <b>Re-record the line at Thursday's shoot</b> (recommended; I put it on the pickups list and in Teleprompter 0: \"...then four hidden reasons... some of those four...\"; it plays under the full-screen 'In this video' card, so it drops in with no picture join). (b) Leave it as filmed and take the line off the list.",
]

locked = ("the 9/23 studio colour (look C) and the wide/tight framing (W2/T2) from the website video and RO-10 to RO-17; the approved studio voice "
          "(audio B) plus the standard bass lift you set on RO-19; Soft Blue Light and the HyperFrames templates (lower third, fact card, side list); "
          "the section card with a picture on the right (RO-11 layout B); the standard before picture; your 'talk to your doctor' clip (A0166); "
          "the app tour in the phone at the end (RO-06); no music, no AbsByAI.com end mark.")

decided = [
 "<b>Takes: the last clean take of every line.</b> The opening is your third run (the first two stopped for prompter scrolls: \"Roll it back to the top\", \"Back to the top one more time\"). Second copies kept where you re-said a line at once: \"I was 200 pounds at 5'7\" (the first said \"I would told you\"), \"There are four leaks\", \"With AI, you take a photo\", \"Leak number two\", \"This is why Monday to Friday dieters\", \"the three chicken nuggets\" (the first stopped at \"over the trash because\"), \"Reason number one\", \"If your partner is not dedicated to fitness herself\", \"You will be less attracted to her\" (the first ad-libbed \"and your own\" and \"sooner than you think\"; the second is the script), \"And since she's the single biggest influence\", \"If you have plateaued for months\", \"It's not going to melt your belly\" (third copy), \"Pick a bedtime\", \"Your problem is that nothing in your day is measured\" (the first said \"this day\"), one doubled \"If\", and the closing call to action (third copy: the first dropped \"part\", the second stumbled on \"gives you\").",
 "<b>One exception to last-take: \"30 days of honest tracking will destroy that bullshit story...\"</b> The FIRST copy is used: the re-said one came out \"then you will be actually able to fix it\".",
 "<b>Cut out:</b> the slate, seven remarks to the crew (\"Roll it back\", \"A little more\", \"That's good there\", \"There we go\"), a 15 s water break, a burp between call-to-action takes and 22 restarts. 20 kept pieces, every edge in room tone with about 80 ms before the first word. Pauses over 0.7 s inside a line are tightened to about 0.4 s.",
 f"<b>Length:</b> {mmss(film)}.",
 f"<b>Look (studio standard, no options, per your 10-14 rule):</b> C1708 under the locked look C measures 0.294 median brightness against 0.296 on RO-17's C1713, same set and light. I measured your hair every half second of every shot and lifted the crop on {len(cy)} shots where it came within 4 % of the top (largest lift {maxlift} px).",
 "<b>Voice:</b> the approved studio voice (audio B: the chain's own fit on this roll + 0.9 dB at 150 Hz, no echo removal) plus your standard bass lift (+3 dB at 120 Hz), as on RO-17. The audio gate's tone row fails on any fixed bass lift (the known mismatch since RO-19). A/B link under the first minute.",
 "<b>No music, no sound effects</b>, as on RO-10 to RO-17.",
 "<b>Numbers on screen are the ones you say</b>, plus two I chose: the study card (New England Journal of Medicine, 1992, Lichtman: people who said they could not lose weight on under 1,200 calories reported eating 1,028 a day and actually ate 2,081, under-reported by 47 %; it backs your \"sometimes by 40 % or more\") and the week card's split of the weekend (Friday night +1,500, Saturday +1,000, which is my illustration of your \"erases all of it\" against the 5 x 500 = 2,500 you say). Others: 120 calories a tablespoon of olive oil, 400 a day = 40 pounds a year, the last 10 lb in 1 to 2 months, 4 hours of sleep.",
 "<b>The reasons on screen use your own words:</b> Reason #1 \"A Fat Girlfriend Or Wife\", Reason #2 \"Fat Friends\", and \"Your Body, Or An Overweight Girlfriend?\" under \"So you have to decide\".",
 "<b>Capitals:</b> title case everywhere; FULL CAPS on two punch words in the whole film (ZERO, GUESSING).",
 "<b>Real pictures:</b> the standard before picture (deck chair, heavier) on \"I was 200 pounds at 5'7\"\"; studio-blue-240 (smiling, glasses, shorts) on \"Zepbound has helped me get abs\". Both carry the real-picture chip.",
 "<b>Clip library first:</b> A0050 (a man weighs his plate and types it into his phone) on \"weighing food on a scale and typing into an app\", A0166 (your talk-to-your-doctor clip), A0169 (the fasting workday) on \"fast until 2 PM\", B0486 (black coffee), and two real app screen recordings in the phone beside you: B0035 (a photo of a plate, 363 calories itemized) on \"With AI, you take a photo of your plate\" and the approved RO-06 app tour (B0544) on the call to action. Everything else is Pexels (free licence), one clip per source, no repeats; each one shows the thing you name (the oil going into the pan, the dressing, the sauce, the juice, the shake, the beer). Five dark clips are lifted so they sit with the film (oil in the pan, dressing, sauce, black coffee, the night-time sleep clip).",
 f"<b>Graphics:</b> {NLT} lower thirds (Motivation format), a fact card (olive oil), a side list (your two choices), a study card, a week card (the deficit bars going down Monday to Friday, then the weekend erasing them, each bar on its word), the daily weigh-in vs 7-day average chart (RO-16's), two numbered lists that land item by item ('In this video', '5 things'), and four section cards with a picture on the right (Part 4's phone shows the app's real photo-to-calories result). Two lower thirds were dropped because they would have blinked back to back with the next one.",
 "<b>AI frames: every pair went through the new frame gate and a fresh independent reviewer before you see it (the standing check from today), and four needed fixing.</b> The donut box lost half of the donut in front of the taken one (repaired: that donut put back from the START frame); the salad changed into a different salad on its way to the table (repaired the same way); the scale shrank to tablet size and his feet stood where it lay (redrawn); the pizza slice came from a pizza with no gap, then from two odd gaps, then the hammer changed shape (redrawn three times; now he throws a fist up instead of grabbing pizza, pizza untouched); the cake slid onto his salad's spot, shrank, and a fork appeared from nowhere next to two spoons sharing one handle (whole pair redrawn: one fork on the plate, the same fork carries the bite). All seven now pass both. 21 images on the Codex subscription ($0).",
 "<b>Spend so far:</b> about $0.65 of Gemini listening (the verbatim restart listen and the 'five' splice test). No video generation yet.",
]
decided.append("<b>Independent check before you saw any of it</b> (a fresh reviewer, every still, every context clip and every join in the first minute frame by frame; its report is review/INDEPENDENT-CHECK.md). It found seven things and all are fixed: the black-coffee clip was much darker than you (lifted); the second half of the 'Too Many Calories' lower third came in a second early (now on \"without realizing\", and the study card starts a moment later so it reads); a scale clip at 5:10 cut before the foot landed and was the fourth scale in the film (removed, you stay on camera); a half-second tight shot at the very end of the app demo (the phone now runs to the cut); the reason lower thirds had softened your words (now your words); four errors in this page's own text; and a stray space in \"47%\". From its notes I also fixed: the beer clip that read as juice (now an amber pint), the dressing poured into an empty bowl (now dressing on a salad), the olive-oil card's photo that repeated the pour right before the pour clip (now a small cup of oil), Part 3's picture that reused an AI frame (now friends sharing a pizza), Part 4's phone with a blank screen (now the app's result), the AI chip over the woman's hair, and a key point that left too quickly. Kept as notes: the 24 and 25 frame stock judders very slightly in a 30 frame film; the first 32 s have 14 s of full-screen cards (the 'In this video' card is where the pickup goes).")

reply = "1. Opener: (a) broken scale / (b) stock scale / (c) camera\n2. AI clips to drop: \n3. Five hidden reasons: (a) re-record Thursday / (b) leave as filmed\n\nOther notes (item ID + what to change):\n"
checks = []
if fm_gate:
    rows = fm_gate.get("rows", []); bad = [r.get("key", r.get("name", "?")) for r in rows if not r.get("ok", r.get("pass", True))]
    checks.append(f"First minute audio gate: {len(rows) - len(bad)} of {len(rows)} rows pass" + (f"; failing: {', '.join(map(str, bad))} (the tone row is the known bass-lift mismatch)." if bad else "."))
if fid and fid.get("untouched_frames"):
    u = fid["untouched_frames"]; checks.append(f"Picture outside the graphics matches its graded base: {u['mean']} dB on {u['frames']} frames, so the compositing changes nothing it should not.")
if hair: checks.append(f"Hair in the first minute, every 0.25 s: closest {hair.get('min_px')} px from the top, median {hair.get('median_px')} px.")
checks.append("Graphics checks on every context clip: 29 of 30 pass as measured; the side list (G24) flagged a 47-pixel speck the person mask found at the bottom edge under the card, not you; your real edge stays 162 px or more clear of the card (checked by hand, review/checks/G24/DISPOSITION.txt).")
checks.append("Every graphic's copy fits its template (from_plan fit check); every part lands on the word that names it (beat sheets under each graphic).")
checks.append("The full film, its delivery gate, watch pass and the independent review of the film come in the next round, once you have picked.")

fm_links = "<a href='first-minute/RO-14 round 1 - audio A-B vs reference.mp4'>audio A/B vs the reference voice</a>"
json.dump(dict(film_len=mmss(film), locked=locked, decisions=decisions, ai=AI, decided=decided, checks=checks, reply=reply,
               ai_intro="Each idea: its START and END frame, the line it plays under, and what plays if you say no. Motion is generated only for the ones you approve, from exactly these frames. Every AI clip carries the AI-GENERATED chip for its whole length, and every take gets the sense check (cause and effect, readable with the sound off, shows the line) before you see it moving.",
               first_minute=dict(end=fm_end, links=fm_links,
                                 note="The AI opener shows its START and END frames as labelled placeholders, in place, so you can judge the timing; the real motion goes in after you approve the frames.")),
          open(f"{OUT}/page_extra.json", "w"), indent=1)
print("page_extra ok", mmss(film))
