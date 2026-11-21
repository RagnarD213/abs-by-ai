"""Writes review/page_extra.json (locks, decisions, AI pairs, look and sound options, what I decided, checks, reply) for RO-31 round 1."""
import json, os
W = "/Volumes/Expansion/_edit_work/RO-31/round1"; OUT = f"{W}/review"
S = json.load(open(f"{W}/shots.json")); FPS = 30000 / 1001; film = S[-1]["out_f1"] / FPS
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def J(p, d=None): return json.load(open(p)) if os.path.exists(p) else d
FM = f"{OUT}/first-minute/DRAFT - RO-31 round 1 - first minute.mp4"
fm_gate = J(FM + ".audio_gate.json", {})
fid = J(f"{OUT}/first-minute/fidelity.json", {})
hair = J(f"{OUT}/first-minute/hair.json", {})
hair540 = J(f"{OUT}/first-minute/hair540.json", {})
fm_end = J(f"{OUT}/first-minute/end.json", {}).get("end", 0)
R = {it["id"]: it for it in json.load(open(f"{W}/plan_resolved.json"))}
NLT = sum(1 for it in R.values() if it["kind"] == "lt"); NFACT = sum(1 for it in R.values() if it.get("scene") == "fact")
NL3 = sum(1 for it in R.values() if it["kind"] == "l3"); NCLIP = sum(1 for it in R.values() if it["kind"] == "clip")
voice = J(f"{W}/options/voice/listen_summary.json", {})

COST = "One Veo take on your Flow subscription, then the motion check and a fresh reviewer. No paid generation."
AI = [
 dict(id="A1", name="The Mirror Check", action="A man frowns at himself in the mirror, holding up a big black T-shirt, then pulls it on to hide in it. Framed from the chest up, stomach out of shot.", fallback="You on camera, which is what the first minute shows now.", cost=COST),
 dict(id="A2", name="The Pool Shirt", action="Pool party, everyone shirtless, one man roasting in a tent-sized black T-shirt with his arms folded. A friend waves him into the pool, he shakes his head and tugs the shirt down.", fallback="You on camera.", cost=COST),
 dict(id="A6", name="The One-Minute Diagnosis", action="A doctor holds up a stopwatch. He clicks it and gives the nervous patient a calm thumbs-up.", fallback="You on camera.", cost=COST),
 dict(id="A3", name="The Jiggle Belt", action="Funny: a man stands strapped into a 1950s vibrating belt machine round his chest, calmly eating chips while it shakes him.", fallback="You on camera.", cost=COST),
 dict(id="A4", name="Four Straws", action="Funny: a man drinks a soda, a juice, a sweet coffee and a beer at once through four long straws. The levels drop and he sighs, happy.", fallback="You on camera.", cost=COST),
 dict(id="A5", name="T-Shirt Double Take", action="A lean man tries on a fitted white T-shirt, raises his eyebrows at the mirror and smiles. His girlfriend looks up from her phone and does a double take.", fallback="You on camera.", cost=COST),
 dict(id="A7", name="The Locker Room Flex", action="A huge bodybuilder admires his bicep in the locker room mirror, glances down, his smile fades, and he quietly pulls a loose T-shirt out of his bag. The source line for the study sits over it.", fallback="You on camera with the same lower third.", cost=COST),
 dict(id="A8", name="Push The Diets Aside", action="A fed-up man pushes his stack of diet books aside and picks up his phone to call the doctor.", fallback="You on camera with the same lower third.", cost=COST),
]
locked = "the studio set and its crop default; the Soft Blue Light graphics and Motivation lower third; library clips you approved on other films (A0166, the doctor clip); the 3A side card; no burned captions."
decisions = [
 "<b>Colour</b>: (a) Rich Balanced, warmer skin (recommended, your pick on the Zepbound film and on Cortisol Belly), (b) Rich Balanced, (c) Richer Colour.",
 "<b>Voice</b>: (a) warm bass plus (recommended, your pick on Cortisol Belly, same set and mic), (b) untreated. The blind listener preferred untreated here too, as it did on Cortisol Belly, and you chose warm bass plus there. Three more options are in the section below if you want them.",
 "<b>Opener</b> (0:00, 'You think that you have man boobs, but you don't'): (a) The Mirror Check AI clip (recommended), (b) stay on camera. Then a real before and after on 'it comes off the same way'.",
 "<b>AI clips</b>: eight ideas, expect to keep about five. Name the ones to drop. Where two start frames are shown (X1, X2), name the one you like. The end frame is made from your pick, then shown to you before any motion.",
 "<b>Your two ad-libbed lines</b> after 'not a doctor' ('I encourage you to take Zepbound even if you're not technically overweight...' and 'It's changed my life...') are not in the script. (a) keep (recommended, they sound like you), (b) cut.",
 "<b>The chest diagram</b> (D01, D02): I drew it by hand as a moving graphic. (a) keep (recommended), (b) change it, tell me how.",
]
vtxt = "; ".join(f"{k} {v['mean']:.1f}" for k, v in sorted(voice.items(), key=lambda kv: -kv[1]["mean"])) if voice else ""
decided = [
 "<b>Takes: the last clean take of every line.</b> The hook is your second read (the first ended with 'Roll it back a little bit'); the opening slate is gone.",
 "<b>Restarts cut:</b> 'The second kind is true gynecomastia' (third start), 'The fastest way I know', 'On Zepbound I went from 192' (second read; it says 'to about 175'), 'Then track your calories' (third read, the one that says 'AI app'), 'Try mine at AbsByAI.com' (third start), 'Now let's talk about the fix' (second read), 'True gynecomastia has a cause' (second read), 'But again', 'So don't assume', 'Either way' (second read). Your 'Okay' after 'another diet' is out.",
 "<b>Three hidden restarts the first transcript missed</b>, confirmed by a separate listen and cut: 'If you want a diag-', 'The second step is...' and 'Push-up...'.",
 "<b>Kept though not in the script:</b> 'If you do truly have gynecomastia, you will feel a firm gland and you will definitely know that it's there' (it helps the check), and the two ad-libs in decision 5. 'Try mine' replaces the script's 'Try ours'.",
 "<b>Chest flies:</b> the job note said this B-roll wasn't filmed, but the 10/23 gym shoot has it, so C03 uses your real chest fly machine footage, from the low angle because the other angles show the gym's logo on the wall.",
 "<b>Please listen at 3:24:</b> two separate transcripts print 'Zetbound' for Zepbound on your recap line. It's the only read of that line, so if it sounds wrong, it needs a pickup.",
 "<b>Stayed on camera for the thank you:</b> a cutaway there didn't show what you were saying.",
 "<b>Script's full-screen lists:</b> 'Lose The Fat' and the recap are side cards so you stay on screen. The study line (up to 1 in 4 cases from drugs, American Family Physician) is a lower third.",
 "<b>Graphics say Appetite Meds,</b> never the drug name, because this film isn't entirely about the drug. You still say Zepbound.",
 "<b>Not shown on purpose:</b> no hands on a chest or belly, nobody pinching fat, and the opener frames stop at the chest, so the first 30 seconds stay safe for engagement ads.",
 f"<b>Voice:</b> 8 blind rankings of five versions on the same 30 seconds: {vtxt}. Scores swung widely between runs. The listener heard room echo least on untreated. I recommend warm bass plus because that's what you chose on this same set.",
 "<b>Colour:</b> three grades compared on the same wide and tight moments next to the approved I'm 41 film.",
 "<b>Independent check before you saw this:</b> a fresh reviewer found 19 things, all fixed: the diagram, a jump cut beside the phone, graphics that left too fast, a gym logo, an orange skin tone, a shirt vanishing in a library clip, and three AI ideas whose action could not work.",
 "<b>AI frames:</b> 15 start frames went through a fresh independent reviewer. One was redrawn (a straw stopped in the beer foam). The opener was redrawn before review because the first version centred on his stomach. Where an idea shows one frame, the alternative failed review twice or was refused.",
 "<b>Stock checked moving:</b> doctor (Pexels 7579840) and surgery (Pexels 7584434, nothing graphic).",
 "<b>Spend so far:</b> under $1 of Gemini listening. Frames were on your subscriptions. No video generation yet.",
]
reply = ("1. Colour: (a) warmer skin / (b) Rich Balanced / (c) Richer\n2. Voice: (a) warm bass plus / (b) untreated / other:\n3. Opener: (a) Mirror Check / (b) camera\n"
         "4. AI clips to drop:     Start frame picks (X1 or X2): Mirror Check    Four Straws    One-Minute Diagnosis    Push The Diets Aside\n5. Ad-libs: (a) keep / (b) cut\n6. Diagram: (a) keep / (b) change:\n7. Notes on anything else:\n")
checks = []
if fm_gate:
    rows = fm_gate.get("rows", []); bad = [r.get("key", r.get("name", "?")) for r in rows if not r.get("ok", r.get("pass", True))]
    checks.append(f"First minute audio gate: {len(rows) - len(bad)} of {len(rows)} rows pass" + (f"; failing: {', '.join(map(str, bad))}." if bad else "."))
    if "tone" in bad: checks.append("Why the tone row fails: it measures how far the voice sits from Muhammad's reference voice's tone balance, and warm bass plus is a fixed tone shape, so this row fails by design. The separate damage row also fails narrowly on this draft: the gate between your words adds a little more wobble than the raw recording had. If you keep warm bass plus, I will finish the full film without that gate so the row passes.")
if fid and fid.get("untouched_frames"):
    u = fid["untouched_frames"]; checks.append(f"Picture outside the graphics matches its graded base: {u['mean']} dB on {u['frames']} frames.")
if hair: checks.append(f"Hair clearance in the first minute (1080p), every 0.25 s of you on camera: closest {hair.get('min_px')} px from the top edge (needs 20), median {hair.get('median_px')} px, {hair.get('samples')} samples.")
if hair540: checks.append(f"Same check on the 540p review copy: closest {hair540.get('min_px')} px (1080 scale).")
ck = J(f"{OUT}/checks/all.json", {})
if ck:
    nf = [k for k, v in ck.items() if v.get("failures")]
    checks.append(f"Graphics checks (face clear of lower thirds, arms clear of side cards, card fill): {len(ck) - len(nf)} of {len(ck)} pass" + (f"; flagged: {', '.join(nf)}." if nf else "."))
checks.append("L04 is a false alarm: the check only measures sideways. Your fist passes about 220 px below the card and never touches it (looked at by the independent reviewer at 3:27).")
checks.append("Speech checks: every restart cut was confirmed against a separate listen, and the leftover-footage scan found none left. Audio was measured, not heard; nobody has listened to it but you.")
checks.append("Hair and the delivery gate on the whole film come with the full render. The hair numbers above cover the first minute only.")
checks.append("Every graphic's copy fits its template (fit check) and every part lands on the word that names it; the beat sheet under each graphic shows the word.")
checks.append("The full film, its delivery gate, the watch pass and the independent review come in the next round, once you have picked.")
fm_links = "<a href='first-minute/RO-31 round 1 - audio A-B vs reference.mp4'>audio A/B vs the reference voice</a>"
json.dump(dict(film_len=mmss(film), locked=locked, decisions=decisions, ai=AI, decided=decided, checks=checks, reply=reply,
               ai_intro="Each idea: its start frame, the line it plays under, and what plays if you say no. X1 and X2 are two versions of the same idea. The end frame comes next, from the start frame you pick, and motion only after you've seen it.",
               first_minute=dict(end=fm_end, links=fm_links, note="Built with colour (a) and voice (a). The AI slots show you on camera until their motion is approved.")),
          open(f"{OUT}/page_extra.json", "w"), indent=1)
print("page_extra ok", mmss(film))
