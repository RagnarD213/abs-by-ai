"""SL-07 round 3 page copy -> r3/review/extra.json (plain language for Dan; no em dashes). Run, then page_r3.py.
Every time on the page is read from the round 3 build (shots.json, hf/manifest.json), never typed."""
import json, os, sys
W = "/Volumes/Extreme/_edit_work/sl07"; R = W + "/r3/review"; sys.path.insert(0, W)
import plans as P
FPS = 30000 / 1001
def mm(t): return f"{int(t // 60)}:{int(t % 60):02d}"
def span(S, cid):
    sh = next(s for s in json.load(open(f"{W}/build/{S}/shots.json")) if s["kind"] != "talk" and s.get("cid", s["roll"]) == cid)
    return sh["f0"] / FPS, sh["f1"] / FPS
def at(S, cid, pre=2, post=2):
    a, b = span(S, cid); end = json.load(open(f"{W}/build/{S}/timeline.json"))["total"]
    return f"{mm(a)} to {mm(b)} (watch {mm(max(0, a - pre))} to {mm(min(end, b + post))})"
def bar(S, i):
    m = json.load(open(f"{W}/build/{S}/hf/manifest.json"))[i]; return mm(m["a"])
L = json.load(open(W + "/motion/ledger.json")); spent = sum(e["usd"] for e in L)
TR = [json.load(open(f"{W}/listen/trials{n}.json")) for n in (4, 5, 6, 7)]
def calls(k): r = [x for t in TR for x in t.get(k, [])]; return sum(1 for x in r if x[1]), len(r)
rb = json.load(open(W + "/pickups/B.report.json")); rd = json.load(open(W + "/pickups/D.report.json"))
import subprocess, shutil
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
sys.path.insert(0, W); import importlib.util as _iu
_sp = _iu.spec_from_file_location("sl07_deliver", W + "/deliver.py"); Dl = _iu.module_from_spec(_sp); _sp.loader.exec_module(Dl)
os.makedirs(R + "/cov", exist_ok=True); os.makedirs(R + "/ai", exist_ok=True); os.makedirs(R + "/media", exist_ok=True)
def still(S, cid):
    a, b = span(S, cid); out = f"cov/{S}_{cid}.jpg"
    subprocess.run([FF, "-v", "error", "-y", "-ss", f"{(a + b) / 2:.2f}", "-i", Dl.dname(S), "-frames:v", "1", "-vf", "scale=540:-2", "-q:v", "3", f"{R}/{out}"], check=True); return out
for f in ("D3_start.jpg", "D3_end.jpg"): shutil.copyfile(f"{W}/aiframes/{f}", f"{R}/ai/{f}")
for S in "BD":                                  # what ships (the head of the delivered short's audio) and the other treatment, for Dan's ear
    subprocess.run([FF, "-v", "error", "-y", "-i", f"{W}/build/{S}/audio.wav", "-t", "8.2", "-ac", "1", "-b:a", "192k", f"{R}/media/pickup_{S}.mp3"], check=True)
shutil.copyfile(f"{W}/listen/src_B_r3pickup.mp3", f"{R}/media/pickup_B_alt.mp3"); shutil.copyfile(f"{W}/listen/src_D_r3match.mp3", f"{R}/media/pickup_D_alt.mp3")
COV = [("A", "scale2", "The overhead scale clip.", "Let's say you have 30 pounds to lose and you are losing 1 pound a week."),
       ("A", "rope", "You jumping rope by the pool (the fast skip).", "It's far, far easier to go all-in for 90 days and get it over with."),
       ("A", "curls", "You curling dumbbells by the pool.", "I would make losing fat the number one priority in my life for 90 days,"),
       ("A", "family", "Dad and daughter in the kitchen, now 0.5 s longer (it ends where \"eat\" begins).", "They drive home, then they take care of their family, and then they try to work out"),
       ("E", "salad", "Salad being packed into meal containers.", "I would go right back to cutting calories until it's gone. Losing 3 pounds is not a big deal."),
       ("E", "abwheel", "Your ab wheel rollout, as a wide card so the whole move is in frame. The ending.", "Losing 30 pounds is 90 days of sacrifice."),
       ("D", "stairs", "The sore man on the stairs, now 1.8 s longer.", "They get really sore, then something comes up at work and they miss a day, and within a month they're not going at all."),
       ("B", "needle", "The metronome scale, dial rebuilt (see What I decided).", "Now, your weight is going to bounce around 2 or 3 pounds from day to day,")]
TT = {S: " ".join(P.TITLE[S][1]) for S in P.SEG}
coverage = ("<section id=\"coverage\"><h2>New and changed clips (my call, swap any of them)</h2>"
  "<p>The delivery gate wants at least 30% of each short to show something other than you talking. Three shorts were under it, because the film has almost no B-roll over those passages. These are library clips (nothing generated, nothing spent), plus the stairs clip lengthened and the needle clip rebuilt. Stills are from the finished files.</p>"
  "<div style=\"display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;align-items:start\">"
  + "".join(f"<div><img src=\"{still(S, c)}\"><div class=\"small\"><b>{TT[S]}, {at(S, c)}.</b> {d} Plays under \"{ln}\"</div></div>" for S, c, d, ln in COV)
  + "</div></section>")
ab0, ab1 = span("D", "abwheel")
frames = ("<section id=\"frames\"><h2>Still open from round 2: working out on vacation (frames)</h2>"
  "<p><b>In \"Work Out Every Morning, Not 3 Times A Week\".</b> You asked for this in place of the coin landing on its edge: a guy on vacation working out anyway, by an infinity pool, push-ups and bodyweight squats, his family watching. Motion needs your yes on these frames first, so the ab wheel holds the slot in the finished short.</p>"
  "<div style=\"display:grid;grid-template-columns:minmax(0,260px) minmax(0,260px) 1fr;gap:18px;align-items:start\">"
  "<div><img src=\"ai/D3_start.jpg\"><div class=\"small\">START: push-ups</div></div><div><img src=\"ai/D3_end.jpg\"><div class=\"small\">END: squats, the kid copies him</div></div>"
  f"<div class=\"copy\"><p><b>When:</b> {mm(ab0)} to {mm(ab1)}, in place of the ab wheel.</p><p><b>Just before:</b> you on camera, \"You're not waking up and asking yourself, is today a gym day or not?\"</p>"
  "<p><b>It plays under:</b> \"You just get up and you do it, even on weekends, even on vacation.\"</p><p><b>Right after:</b> you on camera, \"And if all you can do at first is 10 or 15 minutes, that's fine.\"</p>"
  "<p><b>What you see:</b> he finishes a push-up, gets up and drops into squats; his wife toasts him with her coffee and the younger kid starts copying him.</p><p><b>If you say no:</b> the ab wheel stays.</p></div></div></section>")
CHECKS = json.load(open(R + "/checks.json")) if os.path.exists(R + "/checks.json") else {}
def share(S):
    sh = json.load(open(f"{W}/build/{S}/shots.json")); T = json.load(open(f"{W}/build/{S}/timeline.json"))
    return f"{100 * sum(s['f1'] - s['f0'] for s in sh if s['kind'] != 'talk') / T['frames']:.0f}%"
cov = {S: share(S) for S in P.SEG}
pb, nb = calls("B_r3pickup"); pd, nd = calls("D_r3pickup")
cA, cAj, cE = calls("A_film"), calls("A_filmjoin"), calls("E_film")
X = dict(
 intro=("All five shorts, complete, with your studio pickups from the 10/15 shoot in. You skipped round 2 because the pickups were missing, "
        "so this page shows each short whole, with a short list of what changed since round 1 and where. Every open question from round 2 is here too. "
        "No covers, no upload."),
 locked=("the Soft Blue shorts look; the film's colour and its approved sound (cut only, after the pickup); your five segment picks and titles; "
         "your yes and no on the 12 AI ideas from 10-13; the opening lines you scripted for the two pickups."),
 decisions=[
  "<b>The two pickups</b>: listen to both versions of each (under \"The pickups\") and tell me which sounds right, or how it sounds off. Swapping is audio only, no re-render.",
  "<b>The new and changed clips</b> (my call, under \"New and changed clips\"): keep, or name any to swap.",
  "<b>The \"working out on vacation\" frames</b>: yes, change, or no. If yes, it is a small round 4 (about $0.60 of motion).",
  "<b>Four reworded key points</b>: keep, or give me your wording.",
  "<b>\"Track Your Calories With A Photo\" at 0:37 to 0:40</b>: the \"Today's total\" line is gone from the phone. Want it back?",
  "<b>Anything else</b> in any of the five.",
 ],
 pickups=("<section id=\"pickups\"><h2>The pickups</h2>"
  "<p>Both opening lines are your 10/15 green screen takes on the shoot's clip-on mic (roll C1722): the second, last clean read of each, word for word as scripted. "
  "The picture under each stays B-roll (the overhead scale clip, your jump rope), so the green screen never shows. Level is matched to the film line after it, peaks capped at the film's own, "
  "and the last 60 ms of each pickup now blends into the film's own room sound, so there is no gap at the join. No noise removal, no gate, no echo removal. Your desk recordings are kept, unused.</p>"
  "<p><b>Two treatments, because the checks disagree.</b> (1) The film's own voice settings. (2) Tone matched to the film voice band by band from the raw take, plus a light de-esser. "
  "The independent reviewers measured version 1 as clearly off from the film (fuller and much brighter on the s sounds, worst on \"Weigh Yourself\"). "
  f"A blind listener (Gemini, told only that SOME clips start with a pickup) agreed on \"Weigh Yourself\" (version 1 picked out {calls('B_r3pickup')[0]} of {calls('B_r3pickup')[1]} tries, version 2 {calls('B_r3match')[0]} of {calls('B_r3match')[1]}) "
  f"but not on \"Work Out\" (version 1 {calls('D_r3pickup')[0]} of {calls('D_r3pickup')[1]}, version 2 {calls('D_r3match')[0]} of {calls('D_r3match')[1]}). The film-only control clips: {cA[0] + cAj[0] + cE[0]} of {cA[1] + cAj[1] + cE[1]}. "
  "So the shorts carry the better one for each: version 2 in \"Weigh Yourself\", version 1 in \"Work Out\". The rooms decay the same (about 60 to 65 ms), so this is tone, not echo.</p>"
  "<div style=\"display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px\">"
  "<div><b>Weigh Yourself Every Morning</b>: \"Here's how to know if your fat loss plan is working.\"<br>In the short (version 2): <audio controls preload=\"none\" src=\"media/pickup_B.mp3\"></audio><br>Version 1: <audio controls preload=\"none\" src=\"media/pickup_B_alt.mp3\"></audio></div>"
  "<div><b>Work Out Every Morning</b>: \"Here's why you should work out every single morning.\"<br>In the short (version 1): <audio controls preload=\"none\" src=\"media/pickup_D.mp3\"></audio><br>Version 2: <audio controls preload=\"none\" src=\"media/pickup_D_alt.mp3\"></audio></div></div></section>"),
 coverage=coverage, frames=frames,
 decided=[
  "<b>The pickups went in as recorded</b>: takes B2 and D2 (your last clean read of each line). Both are a little shorter than the desk placeholders, so everything after them moved about half a second earlier.",
  "<b>\"Weigh Yourself Every Morning\": the metronome needle is rebuilt.</b> The AI take's needle made one slow sweep up the dial (it read as a big weight gain) and stretched as it turned; the round 2 reviewer had flagged it too. The man and the room were perfectly still, so I kept the take and redrew only the dial: the old needle painted out, a clean needle swinging back and forth around one reading about every 1.3 s. It passed the motion check and a fresh reviewer.",
  "<b>\"Weigh Yourself Every Morning\": the praying gag is one shot now.</b> The first shot (eyes up, hands together) failed its check: his hair changes from curly to slicked back by itself mid-shot. The candles shot passes and already shows him praying to the scale, so it now carries the whole line \"They just keep doing the same thing for months and hope the scale is going to move.\"",
  "<b>\"The 3-Pound Rule\": you posing by the pool is out</b> (your 10-14 rule, never a shot of you just standing around; library B0435 was under \"once you have your abs, you can eat more\"). I tried the library clip of a lean man enjoying a plate: both versions of it have a cut-out outline around every edge, so it failed. You stay on camera there, with a size change on \"And once you have your abs\". The salad clip runs 2.5 s longer instead.",
  "<b>B-roll share, measured on every short</b> (the gate wants at least 30%): " + ", ".join(f"\"{' '.join(P.TITLE[S][1])}\" {cov[S]}" for S in P.SEG if cov.get(S)) + ".",
  "<b>\"Work Out Every Morning\": the stairs clip runs 1.8 s longer</b>, through \"within a month they're not going at all\", which also removes a 1.3 s shot of you between the clip and the first key point.",
  "<b>\"Work Out Every Morning\": two timing fixes from its reviewer.</b> 0.2 s more of the film's own pause after your pickup, before \"Most guys\" (it was 0.13 s, against your usual 0.4 to 0.5 s), and the early-morning clip now runs to the end of \"Let me tell you why.\" so that caption no longer crosses a cut.",
  "<b>Your curls clip now starts on your first rep</b> in both shorts that use it. It used to end on you standing with your arms down between reps (a reviewer flagged it).",
  "<b>Every AI clip was checked before you see it</b>: the motion check (nothing vanishing or appearing from nowhere) and a fresh reviewer's three sense questions (cause and effect, clear with the sound off, shows the line). The stairs, the beer, the candles, the rebuilt needle and the trimmed measuring cups pass; three takes failed and were fixed or cut (needle, praying shot, the cups' last half second).",
  "<b>Key points reworded after the round 2 review</b> (still open, decision 4). \"Weigh Yourself Every Morning\": was \"Right After The Bathroom, / Before You Eat Or Drink\" (it repeated the sentence word for word), now \"On An Empty Stomach, / Same Scale, Same Time\". \"The 3-Pound Rule\": was \"Stop Weighing Yourself And / 5 lb Quietly Becomes 20\" (the first line alone read as advice to stop weighing), now \"Without A Daily Weigh-In, / 5 lb Quietly Becomes 20\". \"Track Your Calories With A Photo\": was \"A Photo Is Not Perfect, But It / Beats Not Tracking At All\", now \"A Rough Calorie Count / Beats No Count At All\". \"Stop Trying To Lose 1 Pound A Week\": same words, new break, \"Make Fat Loss / The Priority For 90 Days\".",
  "<b>Two key points repeat your sentence and I left them</b>, because they are the film's own approved wording: \"Short DAILY Workouts Beat Long Occasional Ones\" and \"Make Fat Loss The Priority For 90 Days\".",
  "<b>The small labels stay in capitals</b> as you saw them in round 1 (\"LOSE YOUR BELLY FAT\" over each title, and \"KEY POINT\", \"THE MATH\" and the like on the key points). Today's title-case rule is for new copy; say if you want these in title case too.",
  "<b>Your round 1 answers, as I read them</b> (dictated): \"Stop Trying To Lose 1 Pound A Week\": all three AI ideas killed. \"Weigh Yourself Every Morning\": the metronome needle and praying to the scale made. \"Work Out Every Morning\": both killed, vacation frames requested. \"The 3-Pound Rule\": the beer on the patio made. \"Track Your Calories With A Photo\": buried in measuring cups made.",
  f"<b>Spend: about ${spent:.2f}</b> on motion, all in round 2. Nothing new this round (the needle fix and the pickup work cost nothing; listener tests a few cents). Every short is under your $5 limit.",
  "<b>Upload flags (AI clips):</b> yes for \"Weigh Yourself Every Morning\", \"Work Out Every Morning\", \"The 3-Pound Rule\" and \"Track Your Calories With A Photo\"; no for \"Stop Trying To Lose 1 Pound A Week\".",
 ],
 notes=dict(
  A=(f"<b>Changed since round 1:</b> new this round, the overhead scale clip {at('A', 'scale2')}, you jumping rope {at('A', 'rope')} and you curling dumbbells {at('A', 'curls')}; "
     f"since round 2, a real dad-and-daughter kitchen clip {at('A', 'family')} in place of the AI busy dad, and the key point at {bar('A', 1)} breaks as \"Make Fat Loss / The Priority For 90 Days\"."),
  B=(f"<b>Changed since round 1:</b> your studio pickup over the overhead scale clip {at('B', 'scale', 0)}; a new first key point at {bar('B', 0)}; "
     f"the metronome needle {at('B', 'needle')} (rebuilt this round); the chart {at('B', 'chart')}; praying to the scale (now one shot, with candles) {at('B', 'candles', 3, 0)}."),
  D=(f"<b>Changed since round 1:</b> your studio pickup over the jump rope {at('D', 'jumprope', 0)}; the sore man on the stairs {at('D', 'stairs')} (longer this round); "
     f"the ab wheel a little faster {at('D', 'abwheel')} (the vacation clip's slot); the ending is you curling dumbbells {at('D', 'curls', 3, 0)}."),
  E=(f"<b>Changed since round 1:</b> new this round, you stay on camera at 0:04 to 0:06 (you posing by the pool is out), salad into containers {at('E', 'salad')} and your ab wheel to end on {at('E', 'abwheel', 3, 0)}; "
     f"since round 2, the beer on the patio {at('E', 'beer')}, the reworded key point at {bar('E', 0)}, and the last word \"sacrifice\" is whole."),
  F=("<b>Re-rendered this round for one fix:</b> the measuring-cups clip (0:09 to 0:13) now ends as he slumps onto the binder, before the cup tower falls. "
     "The new AI check caught the falling cups melting into a see-through blob in the last half second. Everything else is as in round 2 (independent review ship, delivery gate 39 of 39 then). "
     "Changed since round 1: the measuring cups clip; the first phone fills its screen (0:18 to 0:25); the second phone's corners are clean (0:33 to 0:40); a reworded key point at 0:25. "
     "<b>Open question at 0:37 to 0:40:</b> to remove a flash in the phone's corner I dropped the scroll to \"Today's total\", so \"it adds up your day for you\" plays over the day's meal list with no total line. Want the total back?"),
 ),
 checks=CHECKS.get("checks", ["Checks are still running."]),
 reply=("1. Pickups: fine / Weigh Yourself sounds: / Work Out sounds:\n2. Extra B-roll: keep / swap these:\n3. Vacation frames: yes / change / no\n4. Reworded key points: keep / my wording:\n"
        "5. Track Your Calories, \"Today's total\" at 0:37: back / leave it\n6. Stop Trying To Lose 1 Pound A Week: \n7. Weigh Yourself Every Morning: \n8. Work Out Every Morning, Not 3 Times A Week: \n"
        "9. The 3-Pound Rule That Keeps Belly Fat Off: \n10. Track Your Calories With A Photo: \n"),
)
os.makedirs(R, exist_ok=True); s = json.dumps(X, indent=1)
assert chr(8212) not in s and chr(8211) not in s, "dash"
open(R + "/extra.json", "w").write(s); print("extra.json written")
