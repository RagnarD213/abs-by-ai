"""Writes review/page_extra.json (locks, decisions, AI pairs, look and sound options, what I decided, checks, reply) for RO-28 round 1."""
import json, os
W = "/Volumes/Expansion/_edit_work/ro28/round1"; OUT = f"{W}/review"
S = json.load(open(f"{W}/shots.json")); FPS = 30000 / 1001; film = S[-1]["out_f1"] / FPS
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def J(p, d=None): return json.load(open(p)) if os.path.exists(p) else d
FM = f"{OUT}/first-minute/DRAFT - RO-28 round 1 - first minute.mp4"
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
 dict(id="A1", name="The pharmacist's double take", action="A lean, ripped man about 40 in a black tank top stands at a bright pharmacy counter. The pharmacist, holding his small white prescription bag, looks up from her screen at him and does a double take, mouth open in disbelief; he grins. The opener: a ripped guy picking up a weight-loss drug.",
      fallback="You on camera (the hook line is strong on its own).", cost="One Veo take on your Flow subscription (no charge). Recommended as the opener (decision 3)."),
 dict(id="A2", name="The doctor says no", action="A doctor reads a ripped patient's chart on his clipboard, looks up at him and shakes his head no, one hand raised palm out. The patient on the exam table looks hopeful, then let down.",
      fallback="The older doctor at his desk (library B0390), which plays just before.", cost="One Veo take on the subscription."),
 dict(id="A3", name="Better than average at the barbecue", action="Four men at a backyard barbecue, drinks in hand around the grill; three are clearly heavier. The slimmest one, only a bit soft himself, glances at his buddies and puffs his chest out, smug. The grill hides everyone's waist (no belly shot).",
      fallback="You on camera.", cost="One Veo take on the subscription."),
 dict(id="A5", name="The skeptic on the couch", action="You do the whiny 'excuse' voice on this line. A skeptical guy in a hoodie on his couch, laptop on his lap, looks up with a smirk and waves the claim off; his lips are synced to YOUR recorded voice on the line, the way you liked it on RO-06 and RO-20.",
      fallback="You on camera doing the voice.", cost="One Veo take on the subscription plus about $0.50 of lip sync. If the sync fails its check once, it goes in with his mouth shut and your voice over it (your 10-12 rule)."),
 dict(id="A6", name="Waiting for the study", action="A ripped man in a tank top sits in a clinic waiting room, arms crossed, glancing up at the wall clock; then he slides down in the chair, head back against the wall, bored out of his mind.",
      fallback="Your ab wheel rollouts by the pool (roll C1749).", cost="One Veo take on the subscription."),
 dict(id="A7", name="The referee at breakfast", action="A man in his 60s at his kitchen table holds up his blood-pressure pill; a referee in stripes beside him has his whistle up, pointing at it. The man takes the pill with a drink of water and the referee lowers the whistle, shrugs and gives a thumbs up. 'Nobody calls it cheating.'",
      fallback="Pexels: an older man taking his medication at his kitchen table (6285971).", cost="One Veo take on the subscription. The motion prompt makes the pill visibly go into his mouth."),
 dict(id="A8", name="The steroid bodybuilder", action="A comically oversized bodybuilder (tiny head, huge veiny arms, deep fake tan) flexes both biceps at the camera in a gym, then drops the pose and grabs his lower back, wincing.",
      fallback="Library B0148: a real bodybuilder posing (plain, no gag).", cost="One Veo take on the subscription."),
]

decisions = [
 "<b>Colour</b> (the three options are side by side under the first minute). (a) <b>Rich Balanced</b>, recommended: the grade of the approved I'm 41 film on this same set; brighter skin. (b) Richer Colour: your pick on Boring Abs At 40, a little darker. (c) Rich Balanced with warmer skin.",
 "<b>Voice</b> (same 30 seconds, level matched, under the first minute). (a) <b>Warm bass</b>, recommended: your pick on Boring Abs At 40 (same set, same mic); it also came first in 11 blind listens. (b) Warm bass plus the extra bass lift. (c) The chain's automatic tone match. (d) Untreated.",
 "<b>Opener (0:00 to 0:04), under \"I think every man should take Zepbound, even if you're already ripped.\"</b> (a) <b>The pharmacist's double take</b> (A1, recommended). (b) You on camera.",
 "<b>AI clips: which of the 7 get motion?</b> Name any to drop. All 7 are below with their frames and the line each plays under. Motion runs on your Google Flow subscription (no charge, about 140 of your credits for 7 clips, more with retakes); the only paid item is about $0.50 of lip sync on the skeptic. My ranking: The pharmacist's double take, The skeptic on the couch, Better than average at the barbecue, The steroid bodybuilder, The referee at breakfast, Waiting for the study, The doctor says no.",
 "<b>Your vial and needle.</b> The script cues \"my vial and needle on the counter\" (0:27) and \"me drawing up my dose from the vial\" (5:32). Neither was filmed, so this round uses stock vials and a stock syringe being filled. (a) <b>Keep the stock</b> so this video can release now (recommended: the script says \"this year\"). (b) Film 10 to 15 seconds on your phone of your own vial and of drawing a dose, and I swap them in.",
]

locked = ("the 10/15 studio set's framing sizes from the approved I'm 41 film (wide and tight, 1.31x apart); Soft Blue Light with HyperFrames motion "
          "(the Motivation lower third, the fact card, the 3A side list); the 'talk to your doctor' clip A0166; the correct jump rope footage; no music, no AbsByAI.com end mark.")

vtxt = ""
if voice:
    vtxt = "; ".join(f"{k} {v['mean']:.1f}" for k, v in sorted(voice.items(), key=lambda kv: -kv[1]["mean"]))
decided = [
 "<b>Takes: the last clean take of every line.</b> The intro is your third run (the first two stopped for 'Roll it back' and 'Roll it back to the top'); inside it, your re-said \"It's obviously proven to help you lose fat\" replaces \"It's already proven\". Second or third copies kept where you re-said a line at once: \"people with prediabetes who lost about 6%\" (without the ad-libbed \"by losing weight\"), \"A lot of guys think they're at a normal weight\" (third start), \"and many men who aren't technically overweight\", \"Nearly 99%\", \"then there's heart failure\" and \"tirzepatide cut the risk ... by 38%\", \"Now I know a lot of you guys are saying, oh Dan\" (third start), \"Most of the research on weight loss medication\", the semaglutide heart study line, \"And even if you don't, I would still talk to your doctor\" (your second version, ending \"just 1 to 1.5 milligrams if you don't need to lose weight\"), \"Now for the benefits I showed you\", and the last outro (\"Thank you for watching guys\", the one after 'Roll it back a little bit').",
 "<b>Your ad-libs stay</b> (\"Regardless of what they say, I encourage you to go against the medical consensus...\", \"Not a huge dose, but just 1 to 1.5 milligrams\", \"That makes it a little bit easier for me to adjust my dosage\"). <b>One ad-lib cut:</b> \"That is (the) standard starting dose, usually the lowest dose that people will get / do\": both reads were rough and \"instead of the standard 2.5\" a few seconds later says it. Also cut: your aside \"That is seven out of 10 people. And even if you're not technically overweight or obese, a lot of people who aren't technically overweight could still benefit\" (you went back and re-read from there).",
 "<b>Cut out:</b> the slate (\"Alright, this video is why Zepbound...\"), crew remarks, and 12 restarts. 17 kept pieces; pauses over 0.7 s tightened. A listener pass on the whole cut found no stumble left inside a kept line.",
 f"<b>Length:</b> {mmss(film)}.",
 "<b>Framing:</b> wide and tight at the approved I'm 41 sizes. I measured the top of your hair every half second of the whole roll (highest point 84 px from the top of the 4K frame) and set each shot's crop so your hair keeps visible room in both sizes; checks under the first minute.",
 f"<b>Voice:</b> the 30 seconds were ranked blind by a listener 11 times against a clip of the approved I'm 41 film{(' (average scores out of 10: ' + vtxt + ')') if vtxt else ''}. Warm bass came first overall; one listen is noise, so I lean on your own pick on this set. The first minute uses it.",
 "<b>No music, no sound effects</b>, as on the other studio films.",
 f"<b>Graphics ({NLT + NFACT + NL3}):</b> {NFACT} moving fact cards for the studies (a photo on the left, the number counting up on the word you say it), {NL3} side lists (\"Abs Lower Your Risk Of\", \"My Dose\", \"What It Helps Prevent\") and {NLT} lower thirds (sections, action steps, the two FDA approvals, subscribe). The numbers on screen are the ones you say. Organic rule: you say Zepbound; the graphics keep brand names out (\"the drug\", study names, tirzepatide is not on screen either).",
 f"<b>Clips ({NCLIP}):</b> your own pool footage first (curls, handle push-ups, the fast jump rope, goblet squats, kettlebell deadlifts), cropped in so you fill the frame, never cutting your hair; then the library (vials and syringes, two doctors, a lab, the 'talk to your doctor' clip, hundred-dollar bills) and Pexels (the snoring husband, a pill and a glass of water, a syringe and vials, drawing a dose). Each B-roll was checked beside your studio picture for colour. Dropped: a statin clip whose 'water' reads as red wine, a lab rack with a brand name on it.",
 "<b>AI frames: 8 ideas, 7 passed.</b> The snoring husband idea was dropped because a real stock clip shows it. Every pair went through the frame check and a fresh independent reviewer before you see it. Fixed on the way: a second whistle, jagged referee stripes, a mismatched mirror reflection (the bodybuilder now faces the camera). All frames on the Codex subscription ($0).",
 "<b>Spend so far:</b> about $1.50 of Gemini listening (11 blind voice rankings and one whole-cut listen). No video generation yet.",
]

reply = ("1. Colour: (a) Rich Balanced / (b) Richer / (c) warmer\n2. Voice: (a) warm bass / (b) warm bass + extra bass / (c) auto / (d) untreated\n"
         "3. Opener: (a) pharmacist double take / (b) camera\n4. AI clips to drop: \n5. Vial: (a) keep stock / (b) I'll film my vial\n\nOther notes (item ID + what to change):\n")
checks = []
if fm_gate:
    rows = fm_gate.get("rows", []); bad = [r.get("key", r.get("name", "?")) for r in rows if not r.get("ok", r.get("pass", True))]
    checks.append(f"First minute audio gate: {len(rows) - len(bad)} of {len(rows)} rows pass" + (f"; failing: {', '.join(map(str, bad))}." if bad else "."))
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
fm_links = "<a href='first-minute/RO-28 round 1 - audio A-B vs reference.mp4'>audio A/B vs the reference voice</a>"
json.dump(dict(film_len=mmss(film), locked=locked, decisions=decisions, ai=AI, decided=decided, checks=checks, reply=reply,
               ai_intro="Each idea: its START and END frame, the line it plays under, and what plays if you say no. Motion is generated only for the ones you approve, from exactly these frames. Every AI clip carries the AI-GENERATED chip, and every take gets the sense check and the motion gate before you see it moving. In the first minute below, the AI slots still show you on camera.",
               first_minute=dict(end=fm_end, links=fm_links,
                                 note="Built with the recommended colour (a) and voice (a). The opener slot (0:00 to 0:04) and the doctor slot (0:39) still show you on camera: AI motion comes after you approve the frames.")),
          open(f"{OUT}/page_extra.json", "w"), indent=1)
print("page_extra ok", mmss(film))
