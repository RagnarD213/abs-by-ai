"""SL-09 round 1 page copy (Oura Ring Review SFL R2). Plain language for Dan; no em dashes."""
import json, os
import plans as P
W9 = "/Volumes/Extreme/_edit_work/sl09/round2"
ORDER = ["A", "I", "H", "K", "J"]
NUM = P.ORDER
NAMES = {"A": "Train Harder After A Bad Night's Sleep", "I": "Your Sleep Score Shows Who's Toxic In Your Life", "H": "Cut The Adrenaline Before Bed",
         "K": "You're Not Sleeping As Well As You Think", "J": "Oura Ring Or WHOOP? Which One To Buy"}
TASK = "Oura Ring Review SFL R2"
def _share(S):
    sh = json.load(open(f"{W9}/build/{S}/shots.json")); T = json.load(open(f"{W9}/build/{S}/timeline.json"))
    return sum(s["f1"] - s["f0"] for s in sh if s["kind"] != "talk") / T["frames"], T["frames"] / (30000 / 1001)
LEN = {S: "{1:.0f} seconds; {0:.0%} of it is clips or graphics, the rest is you on camera".format(*_share(S)) for S in ORDER}
REVIEW = {S: f"shorts/{P.NAME[S]} - REVIEW 540p.mp4" for S in ORDER}
AB = {S: f"shorts/AB_film-vs-short_{P.NAME[S]}.mp4" for S in ORDER}
VLC = {S: f"{TASK} - short {NUM[S]} - {NAMES[S].replace('?', '')}.mp4" for S in ORDER}
INTRO = ("Five shorts from Zeeshan's \"My Honest Oura Ring Review After 1.5 Years\" (Video 4), your picks A, H, I, J and K, built whole "
         "in the Soft Blue shorts look. Every graphic, clip and phone screen is further down on its real frame, with a button that plays it "
         "moving with the speech around it. No covers, no upload, nothing queued.")
LOCKED = ("the Soft Blue shorts look you approved on the salad shorts (title band for the whole short, two steady crops, the two-line key-point "
          "bar, captions under it, clips filling the picture); Zeeshan's colour and sound exactly as you finalized the film, cut only, so the "
          "first-round colour and voice options do not apply here; your five picks from today.")
DECISIONS = [
 "<b>Oura Ring Or WHOOP? opener:</b> use the AI smart-ring close-up (frames below) in place of the Oura app screens for the first 4 seconds? "
 "Recommended: yes, it shows the product he is asking about. If yes, the motion is made on your Google subscription ($0) and checked before you see it.",
 "<b>You're Not Sleeping As Well As You Think opener:</b> use the AI \"thumbs-up, then nods off into his coffee\" gag (frames below) in place of "
 "the stock clip of a man rubbing his eyes? Recommended: yes, it acts out \"you are in denial\" in one look.",
 "<b>Anything to change</b> on the five shorts (a clip, a key point, a cut). Write it in the reply box with the short and the time.",
]
SHORTS_INTRO = ("In release order (training and food rules first; you can reorder at setup). Only short 1 has a slot on the shorts "
                "calendar so far (Fri Nov 13, 9 AM Chicago, two days after the long-form goes public on Wed Nov 11); the setup task puts the "
                "other four in the next free slots. The players here and the VLC copies are the same files.")
CHECK = {
 "A": "Check: the opener (a man jolted awake by his alarm while you say \"when you get a bad night of sleep\"), the key point at 0:09, the deadlift and power clean on \"high risk moves\", and your own curls and lateral raises on \"low risk\".",
 "I": "Check: the arguing couple opener, the sleep-score scene with your real Oura chart at 0:19, the key point at 0:39, and the step to the closer crop at 0:46 where the cut middle part was.",
 "H": "Check: the opener (your own last line moved to the front, over night driving and a man throwing his pillow at 4:28 AM), the empty highway and the light-streak drive that replace Zeeshan's AI Tesla, the key point at 0:36, and his real Tesla self-driving footage from \"press a button\".",
 "K": "Check: the yawning opener, the scale on \"weighing yourself every day\", your real Oura sleep screen at 0:20 with its one flagged row (Restfulness: Fair) lit up on \"the problem\", the drink / late snack / stress clips under the key point, and the ending on you.",
 "J": "Check: the opener on your real Oura app screens, the Apple Watch on \"not recommended\", the moving Oura vs WHOOP comparison from 0:21 (each row lands on your words), and the ending.",
}
ABOUT = {
 "A": "57 seconds. The Oura Ring says to take it easy after bad sleep; you say go harder, just pick low-risk exercises over deadlifts and power cleans.",
 "I": "55 seconds. The most unexpected thing the ring showed you: your sleep score crashed during a toxic relationship, so anyone who wrecks your sleep has to change or go.",
 "H": "56 seconds. Something you do near bedtime may be spiking your adrenaline: for you it was fast late-night driving, and cutting it fixed your sleep.",
 "K": "43 seconds. Most people think they sleep fine; a tracker shows the problem and what causes it (alcohol, late eating, stress), so buy one even if it is not the Oura.",
 "J": "46 seconds. Yes to the Oura for most people; Apple Watch and Fitbit not recommended; the Oura's and WHOOP's advantages side by side.",
}
ABOUT_AI = {
 "J": "The opener is now your real Oura app on screen. This idea would replace it with the product itself on a hand.",
 "K": "The opener is now a stock clip of a man yawning. This idea makes the \"denial\" line funny.",
}
AI_INTRO = ("Made on the ChatGPT subscription ($0). Both pairs passed the frame check and a separate reviewer before this page. Motion is only "
            "made for the ones you approve, on the Google subscription ($0), then checked again before you see it moving. Each short works "
            "without its AI clip: \"If you say no\" is what plays there now.")
# id, short, name, when, before, under, after, what you see, if no, note
AI_ITEMS = [
 ("J1", "J", "Smart ring close-up", "The very first picture, 0:00 to 0:04.", "Nothing. This opens the short.",
  "Should you buy the Oura Ring? In my opinion, yes for most people.",
  "Cut to you on camera: \"Now, should you buy a sleep tracker? Absolutely, everybody needs a sleep tracker.\"",
  "A man's hand resting on white sheets in morning light with a matte black smart ring on the index finger; the hand lifts a little and turns so the ring catches the light. No logo on the ring.",
  "Your real Oura app screen in a phone frame (what the short has now).", "AI-GENERATED chip on it. The model drew a left hand; nobody can tell in a close-up, and the ring is worn on either hand."),
 ("K1", "K", "Thumbs-up, then nods off", "The very first picture, 0:00 to 0:05.", "Nothing. This opens the short.",
  "You watching this video right now are probably where I was at a few years ago, which is to say you are in denial.",
  "Cut to you on camera: \"You think you're sleeping okay. You think you're getting enough sleep...\"",
  "An obviously underslept man at his kitchen table smiles and gives a confident thumbs-up, then dozes off mid thumbs-up, head drooping toward his coffee, thumb still up.",
  "The stock clip of a man yawning (what the short has now).", "AI-GENERATED chip on it. The kitchen behind him is copied from the start frame so it cannot drift while he moves."),
]
DECIDED = []          # filled by page build (decided.py) with the gate and review results
ITEM = {}
REPLY = ("Oura Ring Review SFL R2, my notes:\n\n1. Smart-ring opener (Oura Ring Or WHOOP?): \n2. Thumbs-up nods-off opener (You're Not Sleeping): \n"
         "3. Changes:\n   Short 1 Train Harder: \n   Short 2 Sleep Score: \n   Short 3 Adrenaline: \n   Short 4 Not Sleeping: \n   Short 5 Oura Or WHOOP: \n")
if os.path.exists(f"{W9}/decided.json"):
    _d = json.load(open(f"{W9}/decided.json")); DECIDED = _d["decided"]; ITEM = _d.get("item", {})
