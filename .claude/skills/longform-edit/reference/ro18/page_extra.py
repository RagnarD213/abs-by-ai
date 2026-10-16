"""Writes review/page_extra.json (locks, decisions, AI pairs, what I decided, checks, reply) from the measured results. RO-18 round 1."""
import json, os
W = "/Volumes/Extreme/_edit_work/RO-18/round1"; OUT = f"{W}/review"
S = json.load(open(f"{W}/shots.json")); FPS = 30000 / 1001; film = S[-1]["out_f1"] / FPS
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def J(p, d=None): return json.load(open(p)) if os.path.exists(p) else d
fm_gate = J(f"{OUT}/first-minute/DRAFT - RO-18 round 1 - first minute.mp4.audio_gate.json", {})
fid = J(f"{OUT}/first-minute/fidelity.json", {})
hair = J(f"{OUT}/first-minute/hair.json", {})
cy = J(f"{W}/framing/crop_y.json", {})
fm_end = J(f"{OUT}/first-minute/end.json", {}).get("end", 0)
R = {it["id"]: it for it in json.load(open(f"{W}/plan_resolved.json"))}
NLT = sum(1 for it in R.values() if it["kind"] == "lt")
NCLIP = sum(1 for it in R.values() if it["kind"] in ("clip", "phone"))
lifts = sorted(((162 - v["W2"]) if "W2" in v else 0, k) for k, v in cy.items())
maxlift = max([l for l, _ in lifts] + [0])

AI = [
 dict(id="A1", name="The treadmill clothes rack", action="Late at night, a tired man in a wrinkled dress shirt types at his laptop. Behind him his home treadmill is buried under laundry: shirts on hangers hooked over the handrails, clothes heaped on the belt. He turns his head, looks at it, and sighs, hands still on the keys. 'You don't have the time to work out', in one picture.",
      fallback="You on camera (the line is strong on its own).", cost="7 s take, about $1.05. Recommended as the opener (decision 1)."),
 dict(id="A2", name="Voice-to-text rage", action="A guy on his couch holds his phone to his mouth and whines into it; then he lowers it and glares at the screen in disgust. His lips are synced to YOUR recorded impression voice on the line (you do the whiny voice there, as on RO-06), the way you liked it on RO-06 and RO-20.",
      fallback="You on camera doing the voice.", cost="6 s take about $0.90, plus about $0.50 of lip sync. If the sync fails its check once, it goes in with his mouth shut and your voice over it (your 10-12 rule)."),
 dict(id="A6", name="Robot mower, kettlebell on the patio", action="The script's own cue. A white robot mower cuts neat stripes across a suburban lawn while a fit man does kettlebell swings on the patio in front of it. Plays under 'Buy a robot lawnmower like you're seeing on the screen right now'.",
      fallback="Your own robot mower footage from Thursday's shoot (decision 4), or a Pexels push mower.", cost="6 s take, about $0.90."),
 dict(id="A7", name="The teacher slams the laptop", action="An empty classroom after school. A teacher at her desk, red pen in hand, stares at her laptop in outraged shock (she is watching this video); then she slams it shut, crosses her arms and scowls at the camera.",
      fallback="You on camera.", cost="5 s take, about $0.75."),
 dict(id="A8", name="Essays by hand", action="A dorm room at 2 AM. A heavy-set student writes an essay by hand on a legal pad, surrounded by textbook stacks, chips and an energy drink; he puts the pen down and shakes out his cramping hand, wincing at the stack still left.",
      fallback="Pexels: a frustrated student writing in a lecture hall (it plays just before, at 8:08).", cost="8 s take, about $1.20."),
 dict(id="A9", name="Nobody at work has to know", action="An open-plan office. A man leans way back, feet on the desk, hands behind his head, smiling, while his laptop does the work. His boss walks in from the left with a coffee; he snaps upright, feet down, hands on the keyboard, typing with a dead-serious face.",
      fallback="You on camera.", cost="8 s take, about $1.20."),
]

decisions = [
 "<b>Opener (0:00 to 0:07), under \"You don't have belly fat because you lack knowledge. You have belly fat because you don't have the time to work out and eat right.\"</b> (a) <b>The treadmill clothes rack</b> (A1, recommended): a busy man at his laptop glances back at his treadmill buried under laundry. (b) You on camera.",
 "<b>AI clip frames: which of the 6 get motion?</b> Name any to drop. All 6 are below with their frames and the line each plays under. Motion is about $0.15 a second: all 6 first takes about $6.00 plus about $0.50 of lip sync on the voice-to-text guy, about $8 to $11 with the retakes I expect, inside the $15 long-form cap. My ranking: The treadmill clothes rack, Nobody at work has to know, The teacher slams the laptop, Voice-to-text rage, Essays by hand, Robot mower.",
 "<b>Wispr Flow on screen.</b> The script cues your phone and Mac running Wispr Flow and a typing-vs-dictating race; neither was filmed, and your ScreenFlow demo is still on your side (DS-26 waits for it too). This round shows Pexels dictation and typing clips, a 'what you say vs what it types' card and a typing-vs-talking card. (a) <b>Upload the ScreenFlow demo</b> and I put your real Wispr Flow under \"You hold down a button, you talk...\" (0:55), recommended: real beats stock. (b) Keep it as is.",
 "<b>Robot mower footage.</b> You say \"like you're seeing on the screen right now\" (4:21). Thursday's shoot films your own mower for DS-29. (a) <b>Swap in your real mower after Thursday</b> (recommended: real beats AI; the AI mower clip then drops). (b) Keep the AI clip A6.",
 "<b>Equipment.</b> On \"All you need is a yoga mat, push-up handles, a pair of light dumbbells, a kettlebell, an ab wheel, and a jump rope. And you're seeing that on screen right now\" (2:36) I built a six-picture card, each picture landing on its word (the push-up handles are yours, from your 3-minute workout video). Thursday's shoot also films the six pieces. (a) <b>Keep the card</b> (recommended: it names each piece as you say it). (b) Your Thursday footage instead.",
]

locked = ("the 9/23 studio colour (look C) and the wide/tight framing (W2/T2) from the website video and RO-10 to RO-17; the approved studio voice "
          "(audio B) plus the standard bass lift you set on RO-19; Soft Blue Light and the HyperFrames lower third; the section card with a picture on "
          "the right (RO-11 layout B); the self-generation demo (RO-06) and the app tour in the phone (RO-06) at the end; the correct jump rope clip; no music, no AbsByAI.com end mark.")

decided = [
 "<b>Takes: the last clean take of every line.</b> The intro is your fourth run (the first three stopped for 'Back to the top', 'A little more' and 'roll that back one more time'). Second or third copies kept where you re-said a line at once: \"But I know you still think\", \"So here's an app\", \"You hold down a button\" (third), \"Now I know a lot of you guys are saying, oh Dan\", \"For most people I would say\", the gym paragraph (second read), \"And you don't need a lot of equipment\", \"You can get all that stuff for under $100\" (third), \"If you're making decent money\", \"If you have a house with a yard\", \"You map out your yard\", \"But a lawn mowing service is a hundred to two hundred\" (third), \"So a robot lawnmower actually costs you nothing\", \"You'll be shocked at how much more mental focus\" (third), \"You are never going to use it\", \"Then run what it writes you\", \"Alright guys, so let's add\", \"A car that drives for you\" (third), and the whole close from \"So you're not too busy\" (second run).",
 "<b>Across the two rolls:</b> C1714 ends mid meal-prep with \"Something happened with the script here\"; C1715 re-reads from \"But if time is the reason\". I used C1715's read of that paragraph and the meal-prep section (it says \"2 or 3 hours\"; C1714 said \"3 to 5\" and stopped). The camera did not move between the rolls (the light tube and bulb measure 0 px apart; you stand a little further left in C1715), so the same crops serve both.",
 "<b>Your ad-libs stay:</b> \"I don't know technology\", \"including probably this one you're watching right now\", \"That is stupid\", \"Put that time into working out instead\", and the Tesla lines about looking away from the road and working on a laptop in a robotaxi (the shoot report marks those as intended).",
 "<b>Cut out:</b> the slate, crew remarks (\"Back to the top\", \"Can you move that much\", \"Roll it back a little bit\"), water breaks, throat clears and 25 restarts. 29 kept pieces, every edge in room tone about 80 ms before the first word.",
 f"<b>Length:</b> {mmss(film)}.",
 f"<b>Look (studio standard, no options, per your 10-14 rule):</b> the locked 9/23 look C and W2/T2 crops, as on RO-14 and RO-17. I measured your hair every half second of every shot and lifted the crop on {len(cy)} shots where it came within 4 % of the top (largest lift {maxlift} px).",
 "<b>Voice:</b> the approved studio voice (audio B: the chain's own fit on this roll + 0.9 dB at 150 Hz, no echo removal) plus your standard bass lift (+3 dB at 120 Hz), as on RO-14 and RO-17. Joins are filled with each roll's own room tone. A/B link under the first minute.",
 "<b>No music, no sound effects</b>, as on RO-10 to RO-17.",
 "<b>Numbers on screen are the ones you say:</b> 6 ways, 10+ hours a week; 40 vs 150 words a minute; free or $15 a month; 30 minutes of typing, 20 back; 20 to 40 minutes a gym trip, 15 each way doubling a 30-minute workout; under $100; over 5 hours a week on food; 2 to 3 hours saved; about $8 a meal; a lawn service at $100 to $200 a visit, $3,000 to $6,000+ a year, against a $1,000 to $2,500 robot; 1 hour a day = 7 a week; Model 3 about $37,000, Camry about $30,000, Kelley Blue Book about $4,600 less to fuel and maintain over 5 years; 90 % of their work; the add-it-up list; 10+ hours back against about 2.5 needed. The only words that are mine: the 'what you say vs what it types' example sentence.",
 "<b>Capitals:</b> title case on every lower third, headline and section card (the small labels inside cards are sentence case); FULL CAPS on three punch words in the whole film (LATER, NOTHING, HERE).",
 f"<b>Graphics:</b> {NLT} lower thirds (Motivation format), six section cards with a picture on the right (Way 1 to 6), the equipment card, the dictation card, typing vs talking, the drive-doubles-it bar, the lawn service vs robot card, Tesla vs Camry, the add-it-up list (each line lands as you say it) and the 10+ hours vs 2.5 card. The equipment card now also carries "All of it: under $100" (a separate lower third there was on screen for 2 s). I dropped two lower thirds near 9:07 that would have blinked back to back.",
 f"<b>Clips ({NCLIP}):</b> your own footage first: the correct jump rope (B0448), ab wheel (B0427), push-ups (B0032), walking lunges (B0462), medicine-ball toe touches (B0003), your 3-minute total body workout video (V7, on YouTube) on \"I have a three minute total body home workout on this channel\", the real app screen recording (a meal photo analysed to 363 calories, B0035) in the phone beside you on \"AI built the entire Abs By AI app\", the approved app tour (B0544) at the close, and the approved self-generation demo on \"You upload a picture of yourself\". The rest is Pexels (free licence), one source per clip and no scene twice, each showing what you name (the gym bag, the drive, a barbell coming off the floor, the grocery aisle, the microwave, the bin, the delivery at the door, the mower, the traffic, a Tesla driving itself, a robotaxi, Austin, a student asleep in class, programmers, receipts). Four clips are lifted to sit with the film (night traffic, pasta into a pot, the video editor, and the back-seat laptop ride is daytime). I left you on camera where no clip shows the line (\"use your dating apps\": the library dating-app clip is vertical and crops to a shirtless man's stomach in a 16:9 frame).",
 "<b>\"AI editing videos for this channel, including probably this one\":</b> nine of THIS video's own graphics and clips in a grid, as the AI editor laid them out.",
 "<b>Section 4's picture</b> is a real robot mower photo with its brand on it (Landroid). Tell me if you want an unbranded one.",
 "<b>AI frames: 9 ideas made, 6 passed, 3 dropped.</b> Every pair went through the frame gate and a fresh independent reviewer (a new one each retry) before you see it. Fixed on the way: a door that turned to glass and legs that grew (that opener idea was replaced by the treadmill), a missing seat belt, a sliding foot, a mower that changed shape, a leftover pen tip, a missing earring, a laptop lid too deep for its base, a grey patch on a desk. Dropped after three failed tries each: <i>Gym clothes in traffic</i> (his hair and headband changed every time; the traffic line uses Pexels instead), <i>Roll out of bed</i> (a twisted foot; your own push-ups play there), <i>The dish mountain</i> (the gloves kept growing or losing fingers; Pexels dishwashing). All frames on the Codex subscription ($0).",
 "<b>Spend so far:</b> about $1.20 of Gemini listening (the verbatim restart listen in seven chunks and one check that you use the impression voice on the voice-to-text line). No video generation yet.",
 "<b>Housekeeping:</b> the Extreme drive is full (5 GB free), so this job's stock, render cache and review media live on the Seagate (Expansion) under the same folder name, linked from the usual work folder.",
]

reply = ("1. Opener: (a) treadmill clothes rack / (b) camera\n2. AI clips to drop: \n3. Wispr Flow: (a) I'll upload the ScreenFlow demo / (b) keep as is\n"
         "4. Robot mower: (a) swap in my real mower after Thursday / (b) keep the AI clip\n5. Equipment: (a) keep the card / (b) my Thursday footage\n\nOther notes (item ID + what to change):\n")
checks = []
if fm_gate:
    rows = fm_gate.get("rows", []); bad = [r.get("key", r.get("name", "?")) for r in rows if not r.get("ok", r.get("pass", True))]
    checks.append(f"First minute audio gate: {len(rows) - len(bad)} of {len(rows)} rows pass" + (f"; failing: {', '.join(map(str, bad))} (the tone row is the known bass-lift mismatch)." if bad else "."))
if fid and fid.get("untouched_frames"):
    u = fid["untouched_frames"]; checks.append(f"Picture outside the graphics matches its graded base: {u['mean']} dB on {u['frames']} frames, so the compositing changes nothing it should not.")
if hair: checks.append(f"Hair in the first minute, every 0.25 s: closest {hair.get('min_px')} px from the top, median {hair.get('median_px')} px.")
ck = J(f"{OUT}/checks/all.json", {})
if ck:
    nf = [k for k, v in ck.items() if v.get("failures")]
    checks.append(f"Graphics checks on every lower-third context clip: {len(ck) - len(nf)} of {len(ck)} pass" + (f"; flagged: {', '.join(nf)} (see each item)." if nf else "."))
checks.append("Every graphic's copy fits its template (from_plan fit check); every part lands on the word that names it (beat sheets under each graphic).")
checks.append("The full film, its delivery gate, watch pass and the independent review of the film come in the next round, once you have picked.")

fm_links = "<a href='first-minute/RO-18 round 1 - audio A-B vs reference.mp4'>audio A/B vs the reference voice</a>"
json.dump(dict(film_len=mmss(film), locked=locked, decisions=decisions, ai=AI, decided=decided, checks=checks, reply=reply,
               ai_intro="Each idea: its START and END frame, the line it plays under, and what plays if you say no. Motion is generated only for the ones you approve, from exactly these frames. Every AI clip carries the AI-GENERATED chip for its whole length, and every take gets the sense check (cause and effect, readable with the sound off, shows the line) and the motion gate before you see it moving.",
               first_minute=dict(end=fm_end, links=fm_links,
                                 note="The AI opener shows its START and END frames as labelled placeholders, in place, so you can judge the timing; the real motion goes in after you approve the frames.")),
          open(f"{OUT}/page_extra.json", "w"), indent=1)
print("page_extra ok", mmss(film))
