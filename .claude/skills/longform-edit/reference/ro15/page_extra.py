"""Writes review/page_extra.json (locks, decisions, AI ideas, look and sound options, what I decided, checks, reply) for RO-15 round 1."""
import json, os
W = "/Volumes/Extreme/_edit_work/RO-15/round1"; OUT = f"{W}/review"
S = json.load(open(f"{W}/shots.json")); FPS = 30000 / 1001; film = S[-1]["out_f1"] / FPS
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def J(p, d=None): return json.load(open(p)) if os.path.exists(p) else d
FM = f"{OUT}/first-minute/DRAFT - RO-15 round 1 - first minute.mp4"
fm_gate = J(FM + ".audio_gate.json", {})
fid = J(f"{OUT}/first-minute/fidelity.json", {})
hair = J(f"{OUT}/first-minute/hair.json", {})
fm_end = J(f"{OUT}/first-minute/end.json", {}).get("end", 0)
R = {it["id"]: it for it in json.load(open(f"{W}/plan_resolved.json"))}
NLT = sum(1 for it in R.values() if it["kind"] == "lt"); NL3 = sum(1 for it in R.values() if it["kind"] == "l3")
NCLIP = sum(1 for it in R.values() if it["kind"] in ("clip", "phone"))
voice = J(f"{W}/options/voice/listen_summary.json", {})
cy = J(f"{W}/framing/crop_y.json", {})
FR = open(f"{W}/aiframes/start-frames-review.md").read() if os.path.exists(f"{W}/aiframes/start-frames-review.md") else ""

COST = "Motion on your Google Flow subscription (no paid generation): one take, then the motion check and a fresh reviewer; a retake if it fails."
AI = [
 dict(id="A1", name="The Supplement Graveyard", action="Opener. 3 AM: a worn-out man sits up in bed wide awake beside a nightstand crowded with about fifteen sleep supplement bottles. He slowly turns his head to the bottles and sighs.", fallback="You on camera, which is what the first minute shows now.", cost=COST),
 dict(id="A2", name="The Night Sweats", action="A man has just woken up overheated: sweat on his forehead, collar soaked, pushing the duvet off his chest.", fallback="You on camera.", cost=COST),
 dict(id="A3", name="The Thermal Camera", action="A thermal-camera view of a man asleep on his bed. His hands and feet glow brightest while his body cools from red toward blue: the 'heat leaves through your hands and feet' idea in one picture.", fallback="You on camera, then the 'How Glycine Cools You' list.", cost=COST),
 dict(id="A4", name="Kicking The Covers Off", action="Funny: a restless sleeper on a warm night kicks his heavy duvet clean off the bed onto the floor and sighs with relief.", fallback="You on camera with the 'Good For You If' lower third.", cost=COST),
 dict(id="A5", name="Three Blankets And A Beanie", action="Funny: the cold sleeper this isn't for, buried under three blankets in a knit beanie, shivering and clutching the covers.", fallback="You on camera.", cost=COST),
 dict(id="A6", name="The Thermostat War", action="Funny: he reaches to turn the hallway thermostat down; his girlfriend, wrapped in a fleece blanket, stares him down until he backs off with his hands up.", fallback="You on camera.", cost=COST),
 dict(id="A7", name="A Handful Of Capsules", action="Funny: a man at his bathroom sink stares at a heaping palmful of about thirty capsules, a glass of water in his other hand, and shakes his head.", fallback="You on camera; the 'Powder, Not Capsules' lower third stays.", cost=COST),
 dict(id="A8", name="Out Like A Light", action="A man in bed switches off his bedside lamp, settles into the pillow and is asleep with a calm face, on 'a new tool in your toolbox for deeper sleep'.", fallback="You on camera.", cost=COST),
]
locked = ("the 9/23 studio framing (wide W2 and tight T2, as on RO-10 to RO-18); Soft Blue Light graphics from the HyperFrames templates "
          "(Motivation lower third, the side card, the photo fact card); the AI Supplement Audit screen recordings from the app; no burned captions, no music, no AbsByAI.com end mark.")
decisions = [
 "<b>Colour</b>: (a) look C, the locked 9/23 studio colour you approved on the website video and used on RO-10 to RO-18 (recommended), (b) look C with a little more colour, (c) look C a touch brighter.",
 "<b>Voice</b>: (a) your studio voice with the standard bass lift and no gate between words (recommended: it won the blind listens, as on Man Boobs), (b) the same with the gate (what RO-14 to RO-18 used). Three more are in the options section.",
 "<b>Opener</b> (0:00, 'This amino acid helped me sleep more than any other supplement I've ever taken'): (a) The Supplement Graveyard AI clip (recommended), (b) stay on camera.",
 "<b>AI clips</b>: eight ideas, expect to keep about five. Name any to drop. Four ideas show two start frames (X1, X2): name the one you like. The end frame is made from your pick and shown to you before any motion.",
 "<b>Your real Oura data</b> (the script cues 'Oura Ring sleep and body temperature screenshots' at 2:41 to 3:44): (a) send me screenshots of your Oura temperature trend and sleep scores from when you started glycine, and I put them on screen (recommended: real beats stock), (b) keep what this round shows (a stock sleeper and lower thirds with the numbers you say).",
 "<b>Your ad-lib</b> 'or if you just have a thick build like I do... than a lean guy or a thin guy does' (2:03.7) is not in the script. (a) keep (recommended, it sounds like you), (b) cut.",
]
vtxt = "; ".join(f"{k.split('-',1)[1].replace('-',' ')} {v['mean']:.1f}" for k, v in sorted(voice.items(), key=lambda kv: -kv[1]["mean"])) if voice else ""
lifts = [(162 - v["W2"]) for v in cy.values() if "W2" in v]
decided = [
 "<b>Takes: the last clean take of every line.</b> The intro is your fourth run (the first three ended in 'Back to the top' twice and 'Back to the top one more time'). The close is your third run of 'When you become a member...' (the second re-said 'And it designs you').",
 "<b>Restarts cut:</b> 'So wh-' (then 'So what that does'), 'Now I want you to keep this' (re-said 'Now I want to keep this'), 'If you rarely' (then a throat clear and a drink of water), 'My average sleep score... and now I'm usually in the se-', 'I've found that factors' (twice, the second ending in 'Roll that back a little bit'), 'Once you have the major thing-', 'But if your numbers go up, you've-', and the slate.",
 "<b>Small stumbles checked:</b> every word over half a second and every pause over 0.4 s inside a kept line was looked at on the waveform; all were natural sentence pauses, so none was cut.",
 "<b>Please listen at 5:04:</b> one transcript prints a half-started 'If' before 'If you want a full supplement plan'. The waveform and the full-roll listen show it said once; your ear decides.",
 "<b>Kept though not word for word in the script:</b> 'It's just a little white powder', 'or any supplement for that matter', 'Now that I'm taking glycine every night', and the ad-lib in decision 6.",
 f"<b>Length:</b> {mmss(film)}, from 9 kept pieces of the roll.",
 f"<b>Framing:</b> the locked 9/23 wide and tight crops, alternating at every cut so no cut is a jump cut. I measured your hair every half second of every shot and raised the crop on {len(lifts)} shots where it came within 4 % of the top" + (f" (largest raise {max(lifts)} px of the 4K frame)." if lifts else "."),
 f"<b>Voice:</b> five versions of the same 30 seconds (your first lines), level matched, ranked blind 6 times by a listening model: {vtxt} (out of 10). Scores swung a lot between runs; the ungated one won most often, as on Man Boobs. Room tone fills every join from this roll's own quiet room.",
 "<b>Colour:</b> three versions of the same wide and tight moments, next to the approved 3 Healthy Foods film (same set).",
 "<b>Numbers on screen are the ones you say:</b> 3 grams; Yamadera 2007 and Bannai 2012 (the script's cue); 67 and 63 degrees; 10 cents a night; sleep score 70 to 75 before, 75 to 80 now; supplements about 5% of your results.",
 "<b>Capitals:</b> title case on every lower third and card; the small label above each is in capitals; no shouted words this film.",
 f"<b>Graphics:</b> {NLT} lower thirds, {NL3} side lists (What Glycine Is, How Glycine Cools You, What They Found, What Matters More, How To Take It) and one study card for the two Japanese studies. Every part lands on the word that names it.",
 f"<b>Clips ({NCLIP}):</b> the app's real AI Supplement Audit (start screen, then the keep or drop list) in the phone beside you on 'When you become a member'. The rest is Pexels (free licence), one source and one scene per clip, each showing what you name: capsules tipped into a palm, the white powder going into water, a man tossing in a hot bed, fish oil softgels, a man lying awake beside his clock, a sleeper beside his phone and watch, sweat on a face, a peaceful sleeper, an AI chat on a phone. Colour matched to the studio by measurement (true blacks kept). Your own supplement-stack clip (B0002) was dropped: it shows brand labels and cuts your head off.",
 "<b>Left on camera on purpose:</b> 'I sleep best around 63' (the thermostat stock showed the wrong numbers), 'And the powder is a lot cheaper', and the thank you.",
 "<b>Not shown on purpose:</b> nobody's belly, no pinching, and nothing branded on screen except the app and the AI chat on 'Claude or ChatGPT'.",
 "<b>AI frames:</b> eight ideas, made on your Codex and Google subscriptions and shown unlabeled. Every frame went through a fresh independent frame reviewer before this page (21 frames reviewed across three passes). Redrawn after it failed them: the opener (a headboard narrower than the bed, then a squiggly fabric texture), a man hugging the duvet instead of pushing it off, feet cut off in the thermal view, a logo on a pair of shorts, a head cut by the frame edge. Four ideas have two passing frames to choose from (Night Sweats, Thermal Camera, Beanie, Out Like A Light). The other four have one: the second version failed review twice or was refused, so it was dropped.",
 "<b>Independent check before you saw this:</b> a fresh reviewer found 17 things, all fixed: a sentence that ran into the next one at 4:17 (pause widened), the supplement-stack clip (brands, your head cut off), one bedroom scene used twice and a washed-out grade, seven lower thirds that left before you could read them (three cut, the rest held longer or simplified), a study card that sat empty, and this page's wrong time for the ad-lib. Its join check at 4:47 was a false alarm: your voice ends a third of a second before that cut.",
 "<b>Spend so far:</b> about $1 of Gemini listening (the restart listen and the voice rankings). Frames on your subscriptions. No video generation yet.",
]
reply = ("1. Colour: (a) look C / (b) more colour / (c) brighter\n2. Voice: (a) bass lift, no gate / (b) with the gate / other:\n3. Opener: (a) Supplement Graveyard / (b) camera\n"
         "4. AI clips to drop:     Start frame picks (X1 or X2): Night Sweats    Thermal Camera    Beanie    Out Like A Light\n"
         "5. Oura screenshots: (a) I'll send them / (b) keep as is\n6. Ad-lib 'thick build': (a) keep / (b) cut\n7. Notes on anything else:\n")
checks = []
if fm_gate:
    rows = fm_gate.get("rows", []); bad = [r.get("key", r.get("name", "?")) for r in rows if not r.get("ok", r.get("pass", True))]
    checks.append(f"First-minute audio gate: {len(rows) - len(bad)} of {len(rows)} rows pass" + (f"; failing: {', '.join(map(str, bad))}." if bad else "."))
    if any("tone" in str(b) for b in bad): checks.append("The tone row compares your voice with Muhammad's reference mix; any fixed tone shape like the bass lift fails it by design (the known mismatch in the rules), as on RO-14 to RO-18.")
if fid and fid.get("untouched_frames"):
    u = fid["untouched_frames"]; checks.append(f"Picture outside the graphics matches its graded base: {u['mean']} dB on {u['frames']} frames.")
if hair: checks.append(f"Hair clearance in the first minute (1080p), every 0.25 s of you on camera: closest {hair.get('min_px')} px from the top edge (needs 20), median {hair.get('median_px')} px, {hair.get('samples')} samples.")
ck = J(f"{OUT}/checks/all.json", {})
if ck:
    nf = [k for k, v in ck.items() if v.get("failures")]
    checks.append(f"Graphics checks (face clear of lower thirds, arms clear of side cards, card fill): {len(ck) - len(nf)} of {len(ck)} pass" + (f"; flagged: {', '.join(nf)}." if nf else "."))
checks.append("L02 (How Glycine Cools You) is a false alarm: the check only measures sideways; your hand passes about 300 px below the card at 1:11.4 and never touches it (I looked at the frame).")
checks.append("Audio was measured, not heard by me: nobody has listened to it but the listening model and you.")
checks.append("The full film, its delivery gate, the watch pass and the independent full-film review come in the next round, once you have picked.")
fm_links = "<a href='first-minute/RO-15 round 1 - audio A-B vs reference.mp4'>audio A/B vs the reference voice</a>"
json.dump(dict(film_len=mmss(film), locked=locked, decisions=decisions, ai=AI, decided=decided, checks=checks, reply=reply, frame_review=FR,
               ai_intro="Each idea: its start frame, the line it plays under, and what plays if you say no. X1 and X2 are two versions of the same idea; pick one. The end frame is made from the start frame you pick, and motion only after you've seen it.",
               first_minute=dict(end=fm_end, links=fm_links, note="Built with colour (a) and voice (a). The AI slots show you on camera until their motion is approved.")),
          open(f"{OUT}/page_extra.json", "w"), indent=1)
print("page_extra ok", mmss(film))
