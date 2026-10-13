"""SL-07 round 2 page copy -> r2/review/extra.json (plain language for Dan; no em dashes). Run, then page_r2.py."""
import json, os
W = "/Volumes/Extreme/_edit_work/sl07"; R = W + "/r2/review"
rb = json.load(open(W + "/pickups/B.report.json")); fb = json.load(open(W + "/pickups/fit_B.json"))
rd = json.load(open(W + "/pickups/D.report.json")); fd = json.load(open(W + "/pickups/fit_D.json"))
L = json.load(open(W + "/motion/ledger.json")); spent = sum(e["usd"] for e in L)
CHECKS = json.load(open(R + "/checks.json")) if os.path.exists(R + "/checks.json") else {}
X = dict(
 intro=("All five shorts are built with your answers from 10-13: the four AI clips you approved are in and the eight you turned down are out. "
        "Three are finished and ready for your final look. The two that open on a pickup line are complete except for that line: your rule from today says "
        "pickups get recorded on the studio set, so the desk recording you gave me sits in them as a labelled placeholder until the 10/17 shoot. "
        "One thing waits on you: the frames for the new \"working out on vacation\" clip. No covers, no upload."),
 locked=("the Soft Blue shorts look; the film's colour and its approved sound, cut only; your five segment picks; your titles; your yes and no on the 12 AI ideas from 10-13."),
 decisions=[
  "<b>The new \"working out on vacation\" frames</b> for \"Work Out Every Morning, Not 3 Times A Week\" (shown below). Yes, change, or no. If yes, I make the motion (about $0.60) and it replaces the ab wheel on \"You just get up and you do it, even on weekends, even on vacation.\"",
  "<b>Four key points were reworded</b> after the independent review (listed under \"What I decided\"). Keep them, or give me your wording.",
  "<b>Anything else</b> you want changed in any of the five.",
 ],
 frames=("<section id=\"frames\"><h2>New frames to approve: working out on vacation</h2>"
         "<p><b>In the short \"Work Out Every Morning, Not 3 Times A Week\".</b> You asked for this in place of the coin landing on its edge: a guy on vacation working out anyway, by an infinity pool at the beach, push-ups and bodyweight squats, his family watching.</p>"
         "<div style=\"display:grid;grid-template-columns:minmax(0,280px) minmax(0,280px) 1fr;gap:18px;align-items:start\">"
         "<div><img src=\"ai/D3_start.jpg\"><div class=\"small\">START: push-ups</div></div><div><img src=\"ai/D3_end.jpg\"><div class=\"small\">END: squats, the kid copies him</div></div>"
         "<div class=\"copy\"><p><b>When:</b> about 0:25 to 0:29.</p><p><b>Just before:</b> you on camera: \"You're not waking up and asking yourself, is today a gym day or not?\"</p>"
         "<p><b>It plays under:</b> <b>\"You just get up and you do it, even on weekends, even on vacation.\"</b></p>"
         "<p><b>Right after:</b> you on camera: \"And if all you can do at first is 10 or 15 minutes, that's fine.\"</p>"
         "<p><b>What you see:</b> he finishes a push-up, gets up and drops into squats; his wife toasts him with her coffee and the younger kid starts copying him.</p>"
         "<p><b>If you say no:</b> your ab wheel clip stays there, as in the finished short above.</p>"
         "<p><b>Note:</b> the title band covers the top of the frame (sky and palms) and the captions sit over the pool deck under him.</p></div></div></section>"),
 decided=[
  "<b>Your answers, as I read them</b> (they were dictated): \"Stop Trying To Lose 1 Pound A Week\": all three ideas killed. \"Weigh Yourself Every Morning\": both made (the metronome needle and praying to the scale). \"Work Out Every Morning\": both killed, new vacation frames requested. \"The 3-Pound Rule\": the beer on the patio made; the dusty scale and the button killed. \"Track Your Calories With A Photo\": buried in measuring cups made; the moth killed.",
  "<b>The pickups are placeholders.</b> You recorded both lines at 12:50; a few minutes later, after hearing desk pickups in another video (RO-20), you ruled that desk-mic pickups do not work and go on the studio shoot list. Both lines are already on the 10/17 pickup list (Docs/PICKUPS_1017_SHOOT.md). Until then \"Weigh Yourself Every Morning\" and \"Work Out Every Morning\" carry the desk take with a small PLACEHOLDER AUDIO tag on screen while it plays, and their file names say PLACEHOLDER PICKUP, so neither can be uploaded by mistake. Swapping in the studio take is an audio-only change.",
  f"<b>What the desk take measured, for the record.</b> I matched its tone to the film voice twice (final difference {fb['tone_err_mean']:.1f} dB average, {fb['tone_err_max']:.1f} dB at worst on the first line; {fd['tone_err_mean']:.1f} and {fd['tone_err_max']:.1f} on the second). A blind listener still picked the pickup out in 4 of 9 and 2 of 5 tries, and two independent reviewers measured it as a different recording. That agrees with your ear. I stopped there: the rule says not to spend a round on matching a desk recording.",
  "<b>Five independent reviewers looked at the first builds and every one said \"does not ship\".</b> What they found and what I did: the last s of \"sacrifice\" was cut off (the ending now runs 0.2 s longer); the AI-GENERATED label was drawn too big and touched hair or ran off the edge (it is now smaller and placed by measuring where the person is in each clip); a phone screen had black corners and another sat in white bars (both fixed); captions hung on a few frames past cuts (they now end on the cut); the opening frames of two pieces caught you breathing in (trimmed).",
  "<b>Key points reworded after the review</b> (decision 2). \"Weigh Yourself Every Morning\": was \"Right After The Bathroom, / Before You Eat Or Drink\" (it repeated the sentence under it word for word), now \"On An Empty Stomach, / Same Scale, Same Time\". \"The 3-Pound Rule\": was \"Stop Weighing Yourself And / 5 lb Quietly Becomes 20\" (the first line stood alone for 1.5 s and read as advice to stop weighing), now \"Without A Daily Weigh-In, / 5 lb Quietly Becomes 20\". \"Track Your Calories With A Photo\": was \"A Photo Is Not Perfect, But It / Beats Not Tracking At All\" (the word \"It\" hung alone on the second line), now \"A Rough Calorie Count / Beats No Count At All\". \"Stop Trying To Lose 1 Pound A Week\": same words, new line break: \"Make Fat Loss / The Priority For 90 Days\". Every key point now stays up at least 1.8 s after its second line lands.",
  "<b>Two key points repeat your sentence and I left them</b>, because they are the film's own approved wording: \"Short DAILY Workouts Beat Long Occasional Ones\" and \"Make Fat Loss The Priority For 90 Days\". Two reviewers flagged them as echoing the speech. Your call.",
  "<b>The film's AI \"busy dad\" clip is out of \"Stop Trying To Lose 1 Pound A Week\".</b> Looked at frame by frame it turns a carafe into a moka pot and a jacket into a briefcase, and the tall crop lost the kids, so \"they take care of their family\" showed no family. A real clip of a dad and his daughter in a kitchen (library B0073) is there now. That short has no AI in it any more.",
  "<b>\"Work Out Every Morning\" changed in three places.</b> The dark, half-out-of-frame gym stock is replaced by the sore man easing down the stairs (the AI clip you approved for RO-07, label on). The ending is now you doing dumbbell curls by the pool, full screen, in place of the toe touch in a small card. The jump rope and the curls are brightened to sit with the studio footage (your skin measured 77 against 94 before).",
  "<b>\"Weigh Yourself Every Morning\" opens on the overhead scale clip, full screen</b>, in place of the side view in a square. The second stock scale shot is gone (the short already has the metronome needle and the praying man on scales); the picture changes size there instead.",
  "<b>The praying clip is two shots</b>: him praying with eyes up on \"They just keep doing the same thing for months\", then a cut to him bowing with candles on \"and hope the scale is going to move.\" Your approved start frame had no candles and the end frame did; a single clip would have had to grow candles out of the floor.",
  "<b>The weight chart got shorter</b> to make room for the metronome needle, and the study card's second row now comes in 1.5 s earlier so it can be read.",
  "<b>The measuring-cups clip was made on Kling</b>, not Veo: Veo refused that frame three times (its content filter, no charge). Kling made it first try.",
  "<b>One reviewer note for you:</b> in the metronome clip the needle sweeps slowly one way across the dial more than it bounces back and forth. You approved the frames; say if you want another take.",
  f"<b>Spend: about ${spent:.2f}</b> on motion (the needle $0.60, the two praying shots $0.80, the beer $0.40, the measuring cups about $1.12 on Kling, my estimate until the invoice). Frames: $0. Listener tests: a few cents. Every short is under your $5 limit.",
  "<b>Upload flags (AI clips):</b> yes for \"Weigh Yourself Every Morning\", \"Work Out Every Morning\" (the stairs clip), \"The 3-Pound Rule\" and \"Track Your Calories With A Photo\"; no for \"Stop Trying To Lose 1 Pound A Week\".",
 ],
 notes=dict(
  A="<b>Finished.</b> Changed since round 1: a real dad-and-daughter clip at 0:32 to 0:35 in place of the AI busy dad; the key point at 0:46 breaks as \"Make Fat Loss / The Priority For 90 Days\"; one caption fixed at 0:41. Opens on you, close up (all three AI ideas were turned down).",
  B="<b>Complete except the pickup</b> (desk-mic placeholder, tagged on screen, 0:00 to 0:03). Changed since round 1: the overhead scale clip under the pickup; a new first key point at 0:04; the metronome needle at 0:24 to 0:29; the chart at 0:29 to 0:36; praying to the scale at 0:48 to 0:52 (two shots). Watch 0:00 to 0:10, 0:22 to 0:46 and the last 6 seconds.",
  D="<b>Complete except the pickup</b> (desk-mic placeholder, tagged on screen, 0:00 to 0:02). Changed since round 1: the sore man on the stairs at 0:08 to 0:11; the ab wheel a little faster so the return shows (0:25 to 0:29, where the vacation clip would go); the ending is you curling dumbbells by the pool (0:53 to 0:57). Watch 0:00 to 0:14, 0:24 to 0:30 and the last 5 seconds.",
  E="<b>Finished.</b> Changed since round 1: the beer on the patio at 0:06 to 0:10; a reworded key point at 0:19; the last word is whole now. Watch 0:03 to 0:11, 0:18 to 0:25 and the last 4 seconds.",
  F="<b>Finished.</b> Changed since round 1: buried in measuring cups at 0:09 to 0:13; the first phone fills its screen (0:18 to 0:25); the second phone's corners are clean (0:33 to 0:40); a reworded key point at 0:25. Watch 0:05 to 0:14 and 0:18 to 0:40.",
 ),
 checks=CHECKS.get("checks", ["Checks are still running."]),
 reply=("1. Vacation frames: yes / change / no\n2. Reworded key points: keep / my wording:\n3. Stop Trying To Lose 1 Pound A Week: \n4. Weigh Yourself Every Morning: \n"
        "5. Work Out Every Morning, Not 3 Times A Week: \n6. The 3-Pound Rule That Keeps Belly Fat Off: \n7. Track Your Calories With A Photo: \n"),
)
os.makedirs(R, exist_ok=True); json.dump(X, open(R + "/extra.json", "w"), indent=1); print("extra.json written, spent", round(spent, 2))
