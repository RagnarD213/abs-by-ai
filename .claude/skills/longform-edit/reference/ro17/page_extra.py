"""Writes review/page_extra.json (locks, decisions, AI pairs, what I decided, checks, reply) from the measured results."""
import json, os
W = "/Volumes/Extreme/_edit_work/RO-17/round2"; OUT = f"{W}/review"
S = json.load(open(f"{W}/shots.json")); FPS = 30000 / 1001; film = S[-1]["out_f1"] / FPS
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def J(p, d=None): return json.load(open(p)) if os.path.exists(p) else d
fm_gate = J(f"{OUT}/first-minute/DRAFT - RO-17 round 2 - first minute.mp4.audio_gate.json", {})
fid = J(f"{OUT}/first-minute/fidelity.json", {})
hair = J(f"{OUT}/first-minute/hair.json", {})
pre = J(f"{W}/framing/hair_pre.json", {}).get("margins", {})
fm_end = J(f"{OUT}/first-minute/end.json", {}).get("end", 0)
R = {it["id"]: it for it in json.load(open(f"{W}/plan_resolved.json"))}
gate_rows = [r for r in fm_gate.get("rows", []) if not r.get("ok", True)]

AI = [
 dict(id="A3", name="The calorie scale", action="A brass balance scale on a kitchen counter, a double cheeseburger on one pan. A hand pours a cup of trail mix onto the other pan and the trail mix side sinks, the burger rises. The video's whole idea in one picture, before you have said a word of it.",
      fallback="Library clip A0143 (the heavier man eating granola at a table full of 'healthy' food, RO-10's opener) or you on camera.",
      cost="4 s take, about $0.60. Recommended as the opener (decision 1)."),
 dict(id="A2", name="Couch snacking", action="Night, a man on the sofa lit by the TV, a big bag of trail mix on his lap. Eyes on the screen, he keeps reaching in and eating, without looking.",
      fallback="You on camera (the 'you keep reaching into the bag' line has no stock that shows trail mix).", cost="6 s take, about $0.90."),
 dict(id="A4", name="Candy in the nut jar", action="A grinning factory worker in a hairnet tips a scoop of candy-coated chocolates into a jar of nuts and raisins that already wears a green 'healthy' leaf sticker, then looks into the camera and winks. The joke: 'candy mixed with nuts, sold as a health food'. (Redrawn after the independent check: the first version had the sticker and the scoop jump places.)",
      fallback="You on camera with the 'What's In Trail Mix' side list running on.", cost="6 s take, about $0.90."),
 dict(id="A1", name="The hiker at his desk", action="An ordinary open-plan office; one man is dressed for an 8-hour mountain hike (pack still on, hat, headlamp, poles against the desk) and shovels trail mix while he types. Right after the real hiker clip.",
      fallback="You on camera.", cost="6 s take, about $0.90."),
 dict(id="A5", name="Grapes vs raisins", action="Played straight, not a gag: a big bowl of grapes beside a quarter cup of raisins; his left hand tips the cup and the raisins land in his right palm. The size difference is the point. (Redrawn: in the first version the cup tipped itself.)",
      fallback="Stock: the purple grapes bowl already used at 2:23 (no repeats allowed, so you on camera).", cost="8 s take, about $1.20."),
 dict(id="A7", name="Nothing left for dinner", action="A hungry man at a candle-lit dinner table, napkin tucked in, rubbing his hands. He lifts the silver dome with one hand: one broccoli floret. His face drops. (Redrawn: the first version lost the knife and swapped the fork's hand, and a side salad undercut 'nothing left'.)",
      fallback="You on camera.", cost="6 s take, about $0.90."),
 dict(id="A8", name="The boardroom", action="Three food-company executives around a leafy bag of trail mix with stacks of cash; they burst out laughing and toss bills in the air.",
      fallback="You on camera with the ''Healthy' Is A Label' lower third running on.", cost="4 s take, about $0.60."),
 dict(id="A10", name="One can and done", action="The couch-snacking man again (same sofa, same hoodie), closer, from the chest up, this time eating sardines from one tin. He finishes and leans back, hands behind his head, content and done. A callback to Couch snacking. (Redrawn closer: the first version centred his stomach.)",
      fallback="You on camera.", cost="6 s take, about $0.90."),
]

decisions = [
 "<b>Opener (0:00 to 0:04), under \"You can get fat eating healthy foods. I'll show you why this happens.\"</b> (a) <b>The calorie scale</b> (A3, new, recommended): trail mix outweighs a double cheeseburger, a picture that asks the question. (b) Library clip A0143, the heavier man eating granola at a table of 'healthy' food (approved, but it is RO-10's opener, so returning viewers will have seen it). (c) You on camera.",
 "<b>AI clip frames: which of the 8 ideas get motion?</b> Name the ones to drop. All 8 ideas are below with their frames and the line each plays under. Motion is about $0.15 a second (Veo 3.1 Fast): all 8 first takes about $7, about $10 to $13 with the expected retakes, inside the $15 long-form cap. You said about five per video, so drop roughly three. My ranking: Nothing left for dinner, The hiker at his desk, The calorie scale, Candy in the nut jar, Couch snacking, One can and done, The boardroom, Grapes vs raisins.",
]

locked = ("the 9/23 studio colour (look C) and the wide/tight framing (W2/T2) from the website video, RO-10, RO-11, RO-13 and RO-16; "
          "the approved studio voice (audio B) plus the standard bass lift you set on RO-19; Soft Blue Light and the HyperFrames templates "
          "(lower third, fact card, side list) approved on RO-10; the section card with a picture on the right (RO-11 layout B); "
          "the three-photo slate you picked on RO-16; the standard before picture; no music, no AbsByAI.com end mark.")

decided = [
 "<b>Takes: the last clean take of every line.</b> Opening take 2 (take 1 stopped for \"Back to the top one more time\"; take 2 runs straight into the list, so the first 46 s have no join). Re-said lines kept: \"It's nuts and fruit\" (third copy; the first said \"good at you\"), \"That's more calories than a Big Mac\", \"That's how you become the average American\", \"And I was doing this too\", \"That's about the same as a big bowl of grapes\", \"The raisins fit in the palm of your hand\", \"And the third one is coconut water\", \"And if you want the electrolytes\", \"I'm not saying ... small amounts <i>of</i> them\" (the first said \"for them\"), \"You only get so many calories a day\", \"Just because it says healthy\", the sardines line (third copy, the script's wording), the Chipotle line, \"If you're out running around\" and \"Carbs and sugar are addictive\" (second copy, after the noise check on set). Closing: the second wrap (the first said \"my three\" and \"all three of them\").",
 "<b>Cut out:</b> the slate, three off-camera remarks (\"Back to the top\", \"You hearing that? No? Okay.\", \"Roll it up a little bit\"), the 14 s of coughs and a drink before the coconut section, the 12 s water break before \"In my experience\", and 21 restarts. 19 kept pieces, every edge sitting in room tone with about 80 ms before the first word; I looked at the frames either side of every join: you are square to camera in all of them, no look-aways or resets.",
 f"<b>Length:</b> {mmss(film)} (the speech is 7:34; reframe cuts and joins only).",
 f"<b>Look (studio standard, no options per your 10-14 rule):</b> C1713 under the locked look C measures 0.295 median brightness against 0.304 on RO-13's approved C1707, same set and light. On this roll you step closer to camera at times; I measured your hair every half second of every shot and lifted the crop on the shots where it came within 4 % of the top (the biggest lift is 40 px on the opening, where the tight crop would have left 12 px). Median room above your hair is about {pre.get('T2', {}).get('median', 50)} px.",
 "<b>Voice:</b> the approved studio voice (audio B: the chain's own fit on this roll + 0.9 dB at 150 Hz, no echo removal) plus your standard bass lift (+3 dB at 120 Hz). I checked +3 against +1.5 and none in three blind listens with shuffled order: the listener ranked +3 first all three times and never called it boomy. The audio gate's tone row fails on any fixed bass lift (the known mismatch since RO-19); every other row passes. A/B link under the first minute.",
 "<b>No music</b>, as on RO-10, RO-11 and RO-13. <b>No sound effects.</b>",
 "<b>Numbers on screen are the ones you say:</b> 170 calories / 14 g carbs for 3 tablespoons, 700 calories for a cup, 120 calories / 26 g sugar for a quarter cup of raisins, 400-500 calories, 180 calories / 40 g sugar for the 1-liter carton, 18 g protein / 0 carbs / about $2 for sardines, 150 calories / 12 g protein for 2 eggs, $5 rotisserie chicken, 180 calories / 32 g protein / <b>about $7</b> for the Chipotle cup (you said $7 on camera; the script's $4 never appears). The small-carton numbers (90 calories, 20 g) stay spoken only, so one graphic does not repeat another.",
 "<b>Capitals:</b> title case everywhere; FULL CAPS on only two punch words in the whole film (SUGAR WATER, STOPPED), per your 10-09 note.",
 "<b>Real pictures:</b> the RO-16 three-photo slate on \"I finally got the abs I was trying to get for years\"; the standard before picture (deck chair, heavier) on \"For years my meals were clean and I still wasn't lean\". Both carry the real-picture chip.",
 "<b>Stock and library (clip library first):</b> your own footage where it shows the thing you name: drinking water from your green bottle (B0479) on \"Just drink water\", your gloved hands pulling a rotisserie chicken apart (B0443) on \"You just pull some off and eat it\", your daily salad (B0524) on \"I eat larger meals now\". Library: a sardine tin opening (B0501), an egg being peeled (B0046). Everything else is Pexels (free licence), one clip per source, no repeats. I did not use the chips-at-a-laptop clips on trail mix lines (they show chips, not what you name); the one chips clip sits under \"Carbs and sugar are addictive\". Three flat stock clips got a light contrast and colour lift so they sit with the film (hiker, coconut, marathon).",
 "<b>Three fact-card pictures are Codex-made and unbranded</b> (each labelled AI-GENERATED): the 1-liter carton (the only stock carton photo showed a brand next to \"it's sugar water\"), the bag of dried mango and the plain chicken cup (stock showed a coffee cup, and chicken on salad).",
 "<b>Section cards:</b> Food 1 of 3 Trail Mix, Food 2 of 3 Dried Fruit, Food 3 of 3 Coconut Water, and What I Snack On Instead, each with a picture on the right as you asked on RO-11. The ending is a throw-out / replace-with card that lands each food on its word, then you on camera for the thank-you.",
 "<b>Independent check before you saw any of it:</b> a fresh reviewer went through the first minute frame by frame, every still, every context clip and the AI frames, and found 29 things. Fixed: a clip that showed bread under \"dried mango\" (the mango card now starts on those words), an out-of-focus handful of one kind of nut (you stay on camera for \"one small handful\"), a city clip with readable signs (you stay on camera), a big-box aisle with readable tags (now a fresh-produce display), white powder that looked like sugar under \"electrolyte powder\" (now a drink mix stirred into water), a near-black soda clip (now a bright one), the backdrop's edge and two clamps showing beside the side lists (crop 4 % in), the side-list framing changing size mid-card, two lower thirds blinking back to back (merged, one dropped), echo-only lower thirds rewritten to make a point, a lower third that said \"Just Chicken\" when you say \"chicken or steak\" (the fact card carries item 4 now), a chicken-cup photo with salad in it (now plain chicken), two AI chips over a face and over the action, and four AI frame pairs (below). Kept: the anchovy-looking fillets in the sardine clip, and the slight judder of 24-frame stock in a 30-frame film.",
 "<b>AI frames:</b> 28 images made on the Codex subscription ($0): 16 frames, 9 redraws, and the carton, mango and chicken-cup pictures. One redrawn: the first end frame of One can and done had his hand on his stomach and a coffee table that was not in the start frame (cause-and-effect rule); the redraw has his arms along the sofa back and the tin on the cushion.",
 "<b>Spend so far:</b> about $0.75 of Gemini listening (the verbatim restart listen and the three voice trials). No video generation yet.",
]

reply = "1. Opener: (a) calorie scale / (b) A0143 / (c) camera\n2. AI clips to drop: \n\nOther notes (item ID + what to change):\n"
checks = []
if fm_gate: checks.append(f"First minute audio gate: 12 of 13 rows pass (one voice, no comb, dry room, clean between words, no processing damage, words stop cleanly, -14.2 LUFS, true peak -2.0 dB, length). Tone fails: on the whole film it fails only by the bass lift (3.3 dB max, in the low band, the known mismatch); on this 75 s excerpt it reads 4.6 dB max because this stretch is brighter in the top band than the film average.")
if fid and fid.get("untouched_frames"):
    u = fid["untouched_frames"]; checks.append(f"Picture outside the graphics matches its graded base: {u['mean']} dB on {u['frames']} frames (a plain re-encode reads the same, about 39 dB), so the compositing changes nothing it should not.")
if hair: checks.append(f"Hair in the first minute, every 0.25 s: closest {hair.get('min_px')} px from the top, median {hair.get('median_px', hair.get('median_top_px'))} px.")
checks.append("Every graphic's copy fits its template (from_plan fit check); every part lands on the word that names it (beat sheets under each graphic).")
checks.append("The full film, its delivery gate, watch pass and the independent review come in the next round, once you have picked.")

fm_links = ("<a href='first-minute/RO-17 round 2 - audio A-B vs reference.mp4'>audio A/B vs the reference voice</a> · "
            "<a href='first-minute/RO-17 voice options - bass 3 vs 1.5.mp4'>bass +3 dB (used) vs +1.5 dB</a>")
json.dump(dict(film_len=mmss(film), locked=locked, decisions=decisions, ai=AI, decided=decided, checks=checks, reply=reply,
               ai_intro="Each idea: its START and END frame, the line it plays under, and what plays if you say no. Motion is generated only for the ones you approve, from exactly these frames. Every AI clip carries the AI-GENERATED chip for its whole length. Each gets the sense check (cause and effect, readable with the sound off, shows the line) before you see it moving.",
               first_minute=dict(end=fm_end, links=fm_links,
                                 note="The AI slots in the first minute show their START and END frames as labelled placeholders, in place, so you can judge the timing; the real motion goes in after you approve the frames.")),
          open(f"{OUT}/page_extra.json", "w"), indent=1)
print("page_extra ok", mmss(film))
