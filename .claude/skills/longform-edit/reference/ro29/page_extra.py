"""Writes review/page_extra.json (locks, decisions, AI pairs, look and sound options, what I decided, checks, reply) for RO-29 round 1."""
import json, os
W = "/Volumes/Expansion/_edit_work/RO-29/round1"; OUT = f"{W}/review"
S = json.load(open(f"{W}/shots.json")); FPS = 30000 / 1001; film = S[-1]["out_f1"] / FPS
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def J(p, d=None): return json.load(open(p)) if os.path.exists(p) else d
FM = f"{OUT}/first-minute/DRAFT - RO-29 round 1 - first minute.mp4"
fm_gate = J(FM + ".audio_gate.json", {})
fid = J(f"{OUT}/first-minute/fidelity.json", {})
hair = J(f"{OUT}/first-minute/hair.json", {})
hair540 = J(f"{OUT}/first-minute/hair540.json", {})
fm_end = J(f"{OUT}/first-minute/end.json", {}).get("end", 0)
R = {it["id"]: it for it in json.load(open(f"{W}/plan_resolved.json"))}
NLT = sum(1 for it in R.values() if it["kind"] == "lt"); NFACT = sum(1 for it in R.values() if it.get("scene") == "fact")
NL3 = sum(1 for it in R.values() if it["kind"] == "l3"); NCLIP = sum(1 for it in R.values() if it["kind"] == "clip")
voice = J(f"{W}/options/voice/listen_summary.json", {})

AI = [
 dict(id="A1", name="The cocktail bartender", action="A heavyset man in a fluffy white bathrobe shakes a cocktail shaker by his shoulder like a flashy bartender, sets it down, then lifts his salted orange \"cortisol cocktail\" in a smug little toast to the camera. The island hides his waist (no belly in the first 30 seconds).",
      fallback="You on camera, or the real cortisol cocktail TikTok moved to the front (decision 3).", cost="One Veo take on your Flow subscription (no charge)."),
 dict(id="A2", name="Zen and mellow, still gaining", action="A heavyset man meditates cross-legged on a yoga mat, eyes closed, blissful, surrounded by open pizza boxes, donuts and chips. Still in the pose, eyes still closed, he calmly reaches out, takes a slice and lifts it.",
      fallback="You on camera.", cost="One Veo take on the subscription."),
 dict(id="A3", name="Straight to the candy jar", action="A frazzled office worker in a loosened tie stands by a reception counter while his colleagues argue behind the glass wall. He stares at a huge jar of wrapped candy, then gives in: he reaches in and lifts out a fistful, eyes closed in relief.",
      fallback="Library A0173: a man in pyjamas sneaks a pizza box of ice cream and cake out of the fridge at night.", cost="One Veo take on the subscription."),
 dict(id="A4", name="The supplement receipt", action="At a health-food shop checkout with a dozen supplement bottles on the counter, the receipt keeps printing out of the register until it lies in loops around his shoes. He picks up a stretch of it and stares, jaw dropped.",
      fallback="You on camera.", cost="One Veo take on the subscription."),
 dict(id="A5", name="Quitting the stressful job", action="In a corner office, a calm employee lifts his ID badge off his chest and sets it on his frowning boss's desk, picks up his box with a plant and a mug from the chair and walks out smiling. The boss leans back, stunned.",
      fallback="You on camera.", cost="One Veo take on the subscription."),
 dict(id="A6", name="The husband who can't", action="You do the whiny voice on this line. A man on the couch leans toward the camera, palms up, protesting; beside him his wife glares at him with her arms crossed. His lips are synced to YOUR recorded line, from \"Oh Dan, that's crazy\" to \"stresses me out\", the way you liked it on RO-06 and RO-20.",
      fallback="You on camera doing the voice.", cost="One Veo take on the subscription plus about $0.50 of paid lip sync, only with your OK. If the sync fails its check once, it goes in with his mouth shut and your voice over it (your 10-12 rule)."),
 dict(id="A7", name="Weighing the chicken after a fight", action="In an evening kitchen his girlfriend shouts and points at him from across the room; he stays calm and sets a raw chicken breast on his kitchen scale beside his rice and broccoli. By the end she storms off and he is still weighing his food.",
      fallback="Library A0050: a man logging his plated meal on his phone at the kitchen counter.", cost="One Veo take on the subscription."),
]

decisions = [
 "<b>Colour</b> (the three options are side by side under the first minute). (a) <b>Rich Balanced, warmer skin</b>, recommended: your pick on the Zepbound film shot on this same set. (b) Rich Balanced (the I'm 41 grade). (c) Richer Colour (your pick on Boring Abs At 40, a little darker).",
 "<b>Voice</b> (same 30 seconds, level matched, under the first minute). (a) <b>Untreated</b>, recommended: only the low rumble removed, finished to the same loudness. It averaged 7.6 of 10 over 10 blind listens and was picked to ship in 6 of them, and our rule is that a treatment ranking below the untreated voice never ships. (b) Warm bass, no gate (5.4). (c) Warm bass plus the extra bass lift (5.3). (d) Warm bass, your pick on It's Boring, But It Got Me Abs At 40 (3.6; the listener heard chopped word endings on the chained versions). (e) The chain's automatic tone match (3.6).",
 "<b>Opener (0:00 to 0:07), under \"Cortisol belly is real, but the TikTok fixes for it, like the cortisol cocktail, won't take an inch off your waist.\"</b> (a) <b>The cocktail bartender</b> (A1, recommended: it shows the cocktail the whole video is about, and it is funny). (b) The real viral cortisol cocktail TikTok, moved to the front in the phone beside you. (c) You on camera.",
 "<b>AI clips: which of the 7 get motion?</b> Name any to drop. All 7 are below with their frames and the line each plays under. Motion runs on your Google Flow subscription (no charge, about 140 credits for 7 clips, more with retakes); the only paid item is about $0.50 of lip sync on the husband, which I run only with your OK (write \"lip sync OK\" in decision 4). My ranking: The cocktail bartender, The husband who can't, Zen and mellow still gaining, The supplement receipt, Straight to the candy jar, Quitting the stressful job, Weighing the chicken after a fight.",
 "<b>The two TikToks</b> (the viral \"adrenal cocktail\" video from your script, and the backup \"cortisol cocktail\" one) play MUTED in the phone beside you. (a) <b>Keep them muted</b> under your lines (recommended: your lines already say what she says). (b) Let the first one play 3 to 4 seconds with her own sound (\"the only thing that helped her chronic fatigue was adrenal cocktails\") before you say \"But then TikTok tells you the fix is a drink.\"",
]

locked = ("the 10/15 studio set's framing (the Zepbound film's sizes and hair measurements; you sit in the same place on both rolls); Soft Blue Light with HyperFrames motion "
          "(the Motivation lower third, the fact card, the 3A side list); your approved pool B-roll grades from the Zepbound film; no music, no AbsByAI.com end mark.")

vtxt = ""
if voice:
    vtxt = "; ".join(f"{k} {v['mean']:.1f}" for k, v in sorted(voice.items(), key=lambda kv: -kv[1]["mean"]))
decided = [
 "<b>Takes: the last clean take of every line.</b> The hook is your second start (the first stopped at \"like the cortisol...\"). Second reads kept where you re-said a line at once: the first Yale study, \"On a calm day, they ate the same, and they went for more sweets\" (matches the script), \"Stress does not directly lead to belly fat\", \"When I started working out first thing in the morning\", \"And here's the sixth thing\". The recap and the close come from the retake roll C1773, and the close is the one after your \"Roll that back a little\". The half-said \"now I know a lot\" before \"Now I know a lot of you guys are saying\" is cut (caught on the check transcript of the assembled cut).",
 "<b>Cut out:</b> the slate (\"This video is...\"), and 7 restarts: \"Training is one of the best ways to...\", \"I also did a lot less late night eating than wh-\", \"You'll find you have zero\" and \"You'll find that y-\", \"You should have a routine where eating nearly...\", \"Even if you do reduce...\". Each was found by a listener and confirmed on the waveform before cutting. 14 kept pieces; pauses over 0.7 s tightened.",
 "<b>The sleep study card says \"Short Sleep, Same Diet\", no hours.</b> You say the hours yourself (\"five and a half hours\" against \"eight and a half\"), so the card keeps to the result: 55% less fat lost.",
 "<b>Fix 4 on screen reads \"Appetite Medication (Talk To Your Doctor)\"</b>, the wording in your script; you say Zepbound, the graphic keeps the brand name off (organic rule).",
 f"<b>Length:</b> {mmss(film)}.",
 "<b>Framing:</b> wide and tight at the Zepbound film's sizes; I measured the top of your hair every half second of every shot and set each crop so your hair keeps room; checks under the first minute.",
 "<b>Voice:</b> the same 30 seconds were ranked blind 10 times (fresh letters and order each time) against a clip of the approved I'm 41 film. Untreated averaged 7.6 and was shipped 6 times of 10; warm bass, your pick on It's Boring, But It Got Me Abs At 40, averaged 3.6 here. I added a warm bass version without the chain gate between words (5.4, 5 listens) to test whether the gate was the problem; it helped but still ranked below untreated. So the first minute uses the untreated voice, and you can audition all five.",
 "<b>No music, no sound effects</b>, as on the other studio films.",
 f"<b>Graphics ({NLT + NFACT + NL3}):</b> {NFACT} moving fact cards for the studies (Yale 2000, Yale 2001, the sleep study), {NL3} side lists (the real rule, the cocktail's ingredients, the 6 fixes in the recap, split 1 to 3 and 4 to 6 so each card keeps your numbering) and {NLT} lower thirds (the two parts, every fix as you name it, action steps (\"Skip The Cocktail And The Supplements\" sits on your skip line, over the receipt clip), a new \"Is It Worth Killing Yourself For This?\" card so the 30 seconds after the divorce line are not talking head only, subscribe). Numbers on screen are the ones you say.",
 f"<b>Clips ({NCLIP} plus 2 TikToks):</b> your own pool footage first for the training section (curls, handle push-ups, goblet squats, kettlebell deadlifts), then the library (a stressed office worker, a heavy man snacking on the sofa at night, the bar-stool beer gag, meal prep) and Pexels (a stressed worker, orange juice, a restless sleeper, a thermostat turned down from 73 to 68, a sound sleeper, a man drinking alone, vials and a syringe). Your 63-degree thermostat and heavy gym sets were not filmed, so stock covers the thermostat (a finger scrolling it down from 73 to 68 degrees Fahrenheit) and your pool sets cover training.",
 "<b>AI frames: 7 ideas, all 7 passed</b> the frame check and a fresh independent reviewer. Fixed on the way: the opener's shaker changed shape between frames (twice; now the same closed shaker), the receipt paper appeared from nowhere (now it keeps printing), the quitter had to walk to the chair and back in 5 seconds (now he ends at the chair), and a see-through arm from my own repair on the candy jar (regenerated, not patched). The chicken scene was redrawn after the independent check (with the sound off it read as a calm couple, not a fight; now she shouts and points, then storms off). All frames on the Codex subscription ($0).",
 "<b>Independent check before you saw this:</b> a fresh reviewer went through every item and found 15 things, all fixed: a shirtless belly clip in the first minute (swapped for a clothed man snacking), the skip-the-cocktail card landing on the wrong line, lower thirds leaving before you could read them (each now stays at least 1.5 s after its last word lands), the recap numbering fixes 3 to 5 as 1 to 3, a sleep photo that repeated the next clip, a readable thermostat logo, a dark orange bed clip, a ghosted dissolve on the meal-prep clip, the lip-sync window starting late, the chicken scene, the part 2 strip rising over the phone, two key points that only repeated your words, and two wrong lines on this page.",
 "<b>Spend so far:</b> under $1 of Gemini listening (5 blind voice rankings and the restart listens). No video generation yet.",
]

reply = ("1. Colour: (a) warmer skin / (b) Rich Balanced / (c) Richer\n2. Voice: (a) untreated / (b) warm bass no gate / (c) warm bass + extra bass / (d) warm bass / (e) auto\n"
         "3. Opener: (a) cocktail bartender / (b) TikTok / (c) camera\n4. AI clips to drop:    / lip sync OK (about $0.50): yes / no\n5. TikToks: (a) muted / (b) play the first with her sound\n\nOther notes (item ID + what to change):\n")
checks = []
if fm_gate:
    rows = fm_gate.get("rows", []); bad = [r.get("key", r.get("name", "?")) for r in rows if not r.get("ok", r.get("pass", True))]
    checks.append(f"First minute audio gate: {len(rows) - len(bad)} of {len(rows)} rows pass" + (f"; failing: {', '.join(map(str, bad))}." if bad else "."))
    if "tone" in bad: checks.append("Why the tone row fails: it measures how far the voice sits from the I'm 41 reference's tone balance (3.8 dB average gap). The untreated voice is not tone matched on purpose; it won the blind listens anyway, and every damage row (chopped words, swirl, comb, room) passes. If you pick a warm bass option instead, the tone row is measured again on that version.")
if fid and fid.get("untouched_frames"):
    u = fid["untouched_frames"]; checks.append(f"Picture outside the graphics matches its graded base: {u['mean']} dB on {u['frames']} frames.")
if hair: checks.append(f"Hair clearance in the first minute (1080p), every 0.25 s of you on camera: closest {hair.get('min_px')} px from the top edge (needs 20), median {hair.get('median_px')} px, {hair.get('samples')} samples.")
if hair540: checks.append(f"Same check on the 540p review copy: closest {hair540.get('min_px')} px (1080 scale).")
ck = J(f"{OUT}/checks/all.json", {})
if ck:
    nf = [k for k, v in ck.items() if v.get("failures")]
    checks.append(f"Graphics checks (face clear of lower thirds, arms clear of side cards, card fill): {len(ck) - len(nf)} of {len(ck)} pass" + (f"; flagged: {', '.join(nf)}." if nf else "."))
checks.append("Every graphic's copy fits its template (fit check) and every part lands on the word that names it; the beat sheet under each graphic shows the word.")
checks.append("The full film, its delivery gate, the watch pass and the independent review come in the next round, once you have picked.")
fm_links = "<a href='first-minute/RO-29 round 1 - audio A-B vs reference.mp4'>audio A/B vs the reference voice</a>"
json.dump(dict(film_len=mmss(film), locked=locked, decisions=decisions, ai=AI, decided=decided, checks=checks, reply=reply,
               ai_intro="Each idea: its START and END frame, the line it plays under, and what plays if you say no. Motion is generated only for the ones you approve, from exactly these frames. Every AI clip carries the AI-GENERATED chip, and every take gets the sense check and the motion gate before you see it moving. In the first minute below, the AI slots still show you on camera.",
               first_minute=dict(end=fm_end, links=fm_links,
                                 note="Built with the recommended colour (a) and voice (a). The AI slots (the opener at 0:00 and the zen man still gaining weight at 0:48) still show you on camera: AI motion comes after you approve the frames.")),
          open(f"{OUT}/page_extra.json", "w"), indent=1)
print("page_extra ok", mmss(film))
