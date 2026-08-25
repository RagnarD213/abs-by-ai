# Video 1 ("This Picture Got Me Abs") — Revisions, Round 2

Google Doc (share this with the editor after Dan approves):
https://docs.google.com/document/d/1BkuKa6Elu_7Ye47ZFvYy0XxXxIJhBKeYr53jScs5uKQ/edit

Reviewed video: https://drive.google.com/file/d/1ZWv5t3rNitubDUDaSKcrn5SqVJCEX2ip/view (4:27, 1080p30, Premiere export 2026-08-24, editor: teamcrackhow4@gmail.com)
Round 1 doc: https://docs.google.com/document/d/13uu4k9y2ttOWD9sp3KU-OLAeCNO74-3pWeIrBjcgVhk/edit

Reviewed cut: 4:27, 1080p30, delivered 2026-08-24.
Previous notes: "Video 1 revisions - round 1" — please re-read it, most of it has not been applied yet.

**Good news first — three things did get fixed and they should stay:**

1. **Pacing is now excellent.** Total dead air in the whole video is 0.3 seconds. That was the biggest structural problem in round 1 and it is solved.
2. **Punch-ins are in.** The talking head now cuts between wide and tighter framings instead of sitting on one shot.
3. **The real app screen recording replaced the fake app UI at 1:18.** That was the most important round-1 item and it is done (one fix still needed inside it — see 1:28 below).

**The rest of round 1 has not been done.** The audio fix, the music bed, the sound effects, the brand color scheme, the AI disclosure labels, the vertical-video framing, the real app screens at the end, and the end card are all still outstanding. Two banned items are still in the cut, and two new ones have appeared. Details below.

---

## THROUGHOUT VIDEO

**THE AUDIO IS THE #1 PROBLEM AND IT GOT WORSE, NOT BETTER**

- Round 1 asked for the two camera microphones to be separated. That has not happened. This export now carries **both microphones, one in each speaker**: the right speaker is the lav mic on Dan's chest, and the left speaker is a room mic about 9 feet away. The left one arrives 7.8 milliseconds later **and with its polarity flipped**.
- Why this matters: every phone, laptop and TV speaker mixes left and right together. When these two get mixed, they partly cancel each other out. Measured on this file: the voice loses **4 dB** and gets a hollow, comb-filtered sound the moment it plays in mono. Nothing can be done about that after the fact — it has to be fixed at the source.
- **The fix: re-import every talking-head camera file and use the RIGHT channel only, as mono.** In Premiere: right-click the clip → Modify → Audio Channels → set it to Mono, taking the Right channel only. Do this for every camera file in the timeline.
- Do NOT try to fix this with EQ, de-reverb, or a noise reducer. The voice has to be rebuilt from the right channel of the source files.

**THE MASTER IS FAR TOO LOUD AND IS CLIPPING**

- This export measures **−8.0 LUFS with a true peak of +2.5 dB**. The target is **−14 LUFS, true peak −1.5 dB or lower**. It is about 6 dB too loud.
- Because of that overload, **166,000 samples in the left channel and 29,000 in the right are clipped** — that is audible crackle and distortion on the loudest words, and it is baked into the file.
- Back the level off, then master to −14 LUFS with a limiter ceiling of −1.5 dB. Do this after the mono-from-right fix, not before.

**STILL NO MUSIC BED AND NO SOUND EFFECTS**

- There is no music under this video at all. Measured: the level between words is just room noise, with no musical content anywhere in the 4:27.
- Add a music bed under the entire video, roughly 20 dB below the voice.
- Add a short whoosh or pop sound effect on every text graphic and every insert entrance and exit. Right now the graphics appear silently, which is why they feel flat.

**EVERY GRAPHIC IS IN THE WRONG COLORS — USE THE BRAND SCHEME**

None of the graphics in this cut use our colors. The yellow bullet text, the glossy blue "TAP BUTTON BELOW" button and the red-and-yellow comic "FREE" starburst all look like default stock templates. Rebuild all of them in this scheme:

- Background / panel: black, or our dark brand green **#162118**
- Header text: large, ALL CAPS, brand olive green **#8C9858** (this reads properly on black)
- Body text: off-white **#E9EEDE**
- Red **#E22222** only as an attention accent, never as a background
- Font: Manrope, Bold for headers
- **Title Capitalization on every graphic.** Don't copy the capitalization I use in this document.
- Reference look: the Abs By AI YouTube Shorts cover images.

**THE AI DISCLOSURE LABELS ARE GONE ENTIRELY**

- Round 1 asked for the "AI GENERATE D" typo to be fixed. Instead the labels have been removed from the whole video. **There is not a single AI label anywhere in this cut.**
- Every AI-generated image or clip needs "*AI Generated" on screen for its full duration. In this cut that means at minimum the phone lock-screen clip (0:07.8–0:09.4) and the heavier-Dan-on-the-couch clip (0:09.4–0:12.6), plus anything new that gets added.
- Full-screen AI clips: label in the **upper-left**, about 50% larger than a normal caption. Small panel inserts: small centered tag at the bottom of the panel.
- The photos of Dan at 0:13.4–0:15.1 are real photographs from his shoot, so those correctly need no label.

**COMPLIANCE — THESE ARE HARD RULES, NOT PREFERENCES**

These are Google Ads policy. A violation gets the ad account suspended, so nothing ships until all four are clean:

- **Never a side-by-side before/after**, AI or real. Before, then footage, then after, shown separately and disclosed, is fine. (Violated at 1:28 — see below.)
- **No morph or transformation in one continuous shot.** This one WAS fixed — the old 3:38 morph is gone. Keep it gone.
- **Never negatively portray a fat or out-of-shape person. No belly-fat close-ups.** (Violated at 0:22 — see below.)
- **Never show an email-capture form.** Currently clean.

**VERTICAL CLIPS STILL HAVE RAW BLACK BARS**

- The heavier-Dan couch clip at **0:09.4–0:12.6** is still a vertical clip sitting in the middle of the frame with plain black bars either side. Round 1 flagged this and it hasn't changed.
- Fill the sides with either a brand-colored card behind the clip, or a blurred, enlarged copy of the clip itself. Never plain black.

**THE LAST 47 SECONDS HAVE NOTHING ON SCREEN**

- From **3:38 to 4:25** there is not a single insert, graphic or product screen — just the talking head for 47 straight seconds. That is the section where the product is actually explained, and it is the weakest stretch in the video.
- Measured across the whole cut, inserts and graphics cover only about **30% of the runtime**. The reference edit runs roughly twice that. The fixes below fill most of the gap.

---

## TIMESTAMPED REVISIONS

- **0:00 – 0:04.4 (the hook) — WRONG PICTURE. This is the most important fix in the document.**
  The script says *"This picture got me abs and it's not even real."* The image on screen is the **joke Photoshop picture** — a stranger's bald head pasted onto a bodybuilder's body. That is the gag image, and using it here tells the viewer the whole premise is a joke in the first three seconds.
  Replace it with the real AI goal image: **01_HOOK+ENDCARD_ai-goal-image_dan-by-pool.png** — https://drive.google.com/file/d/1-8QAfoeAIt52fswKhFvg6ep1i4iqLGGu/view
  Present it as a brand-styled card (not a floating rounded rectangle), with an animated highlight box drawing around it on the word "picture", and "*AI Generated" on it. Note the physical printed photo taped to the door on the left of frame is the same picture — a highlight box on that instead would work just as well and is a stronger moment.

- **0:03.8 – 0:06.4 ("I was 200 pounds")** — add a title graphic reading "200 Pounds". Use the real before picture full screen with a slow push in: **02_BEFORE-PICTURE_dan-200lb.png** — https://drive.google.com/file/d/11Qb559-mqga9FznIpC8tgxLLfz1BUKQX/view

- **0:07.8 – 0:09.4 (phone lock screen)** — same wrong-image problem. The lock screen on the phone is the joke Photoshop picture. Rebuild this mockup with the real AI goal image (01_HOOK, linked above) as the wallpaper. Add "*AI Generated", upper-left, large.

- **0:09.4 – 0:12.6 (Dan on the couch)** — remove the black bars per the THROUGHOUT note, and add the "*AI Generated" label. Clip: **03_CLIP_heavier-dan-looks-at-phone.mp4** — https://drive.google.com/file/d/1oWU1nx1K3EN-yIlaT0Sb7MSiteAzCGEj/view

- **0:13.4 – 0:15.1 ("this is where I'm at today")** — good, keep. Two of the four shoot photos are here. Add the other two so it lands as a sequence of four at roughly 0.4s each, each with a slow move: **06_SHOT3_photoshoot-towel-smile.jpg** — https://drive.google.com/file/d/1DlngN_zRBigpnCpqCjaEgWNXbq-g5FhP/view and **07_SHOT4_photoshoot-standing.jpg** — https://drive.google.com/file/d/14MaZWbcfU84uFPGFPf0ew2JPKfS0OTiY/view

- **0:15.4 – 0:31.3 ("In today's episode…")** — remove the fruit-bowl stock photo at 0:20.3 and build the bullet graphic round 1 asked for. Header: "In Today's Episode". Bullets, appearing one at a time on the line that mentions them, evenly spaced:
  - How I Got Limitless Motivation To Work Out And Eat Healthy
  - What I Needed To Do To Lose My Belly Fat And Get Six-Pack Abs
  - How You Can Generate A Goal Picture Of Yourself With Abs For Free

- **0:22.4 – 0:25.8 — REMOVE. BANNED.** A three-second full-screen close-up of a stranger grabbing a roll of belly fat on a yellow background. This is exactly the belly-fat close-up and negative portrayal our ad policy prohibits, and it is off-brand on top of that. Cover the line with the bullet build above instead.

- **0:30.4 – 0:31.6 — REMOVE the comic "FREE" starburst.** Red and yellow cartoon burst with rainbow stars — it looks like a free template and it is nothing like our brand. Replace with a simple brand card: "Free" in olive green ALL CAPS on black, or drop the graphic entirely.

- **0:41 – 0:50** — add a lower-third chip: "The Problem" (white on dark green) over "No Time, No Motivation." (white on black). The office stock clip at 0:47.4–0:50.3 can stay.

- **0:50 – 0:58** — add a title card: "Visualizing Your Goal" over "One Of The Most Powerful Ways To Motivate Yourself".

- **1:04.3 – 1:15.4 (the Photoshop gag)** — **this is the one place the joke image belongs** and it is correctly used here. Two changes: it runs 11 seconds, which is far too long — cut it to about 4 seconds around "it looked ridiculous" — and put it in a brand-styled frame rather than a plain floating card. Clip version if wanted: **08_CLIP_crude-photoshop-gag.mp4** — https://drive.google.com/file/d/1IhiEN4f-jggd2MgHxHckoO5kr8lf12vP/view

- **1:18 – 1:35.5 (the app screen recording)** — the right product is now on screen, which is the big win of this round. Three fixes:
  - **1:28.5 – 1:30 — REMOVE. BANNED.** The "Meet the new you." screen shows **BEFORE and AFTER side by side**, plus "Estimated body fat 20–24% → 9%". A side-by-side before/after is the single hardest rule we have. **Cut the recording before this screen appears** and end on the after picture ALONE.
  - The panel is small and pushed to the right edge; the text is unreadable at phone size. Make it noticeably larger.
  - Round 1 asked for the recording to start at the generation screen. It currently starts on the tail of the photo-crop screen ("Remove photo" is visible at 1:18). Start a little later.
  - Source: **09_CLIP_app-generate-future-self.mp4** — https://drive.google.com/file/d/14yOV7t-9tlrg7J5ZROBlpDq25KFyXXMR/view — usable window is 0:03–0:25, accelerated to fit.

- **1:36 – 1:42** — add a statement bar: "If You Saw Yourself With Abs, You'd Be MOTIVATED To Make Your Dream Body A Reality."

- **1:43 – 1:52.7 (first CTA) — the "TAP BUTTON BELOW" button is wrong.** It is a glossy grey-blue 3D pill that looks like an old Windows button, it is in ALL CAPS, and it sits on top of the printed pool photo on the door, which is the best thing in that corner of the frame. Replace with a **full-screen CTA card**, white on dark green: "Get A FREE AI Image Of Yourself With Abs" over "Tap The Button Below".

- **1:53 – 2:09.4 (the benefits) — replace the text list with our AI clips.** The current graphic is a yellow-and-white bullet list in the top-left corner with no panel behind it, in sentence case, overlapping Dan's face and the door photo. Cut it. Use these instead, each full screen with the large "*AI Generated" label upper-left:
  - "You're more attractive to women" (~1:59) → https://drive.google.com/file/d/15g3Lf3oIcaGZpLM8QFvL4Qso-F81HgBt/view
  - "Men respect you more" (~2:01) → https://drive.google.com/file/d/1KAXCrU36IWBWpvMK3yIwnWocT4yfQa1z/view
  - "You feel better / more energy / health improves" (~2:03–2:09) → https://drive.google.com/file/d/1wXw7uSqKa_vFwnxr7oVbXDToqOZ0NREM/view

- **2:09 – 2:20** — add a lower third: "You Don't Need More Knowledge" over "You Need Motivation To Execute What You Already Know."

- **2:24 – 2:35 ("a 38 year old dad living a busy, stressful life")** — nothing on screen here for 11 seconds. Use the busy-dad AI clip: **AI clip - busy dad no motivation (kitchen).mp4** — https://drive.google.com/file/d/1-VdGbUOkcTxj_gKfQFNEqK66JmLvDhfY/view — with the large AI label. Accelerate to fit if it runs short.

- **2:37.4 – 2:42.2 — WRONG PICTURE AGAIN.** The script says *"Nothing worked to motivate me until I generated this picture and made it my phone lock screen."* The joke Photoshop image is on screen again. Replace with the real AI goal image (01_HOOK, linked above) and label it.

- **2:53.5 – 2:55.6 (meal prep)** — the stock clip shows a bald, heavily-built man and the chalkboard behind him reads "3200 CALS/DAY", which contradicts a fat-loss message. Replace with a clip of a lean man 30–50 doing meal prep, or drop it.

- **2:55.6 – 2:57 — REMOVE.** This is a generic third-party calorie-tracking app ("DAILY CALORIES 1320 cal") from a stock library. We never show another company's product as if it were ours. Replace with our real macro tracker screen: **12_APP_meal-plan.png** — https://drive.google.com/file/d/1GhWuPso3bywsyYEmxk-I1y9WjkP5qkEh/view

- **3:16 – 3:21.7 (ChatGPT)** — the logo floats unframed over the fridge with a small blue "AI" chip next to it. Put the logo inside a small brand-styled card as round 1 asked, and drop the blue chip.

- **3:35 – 3:38.3 — REMOVE. This is a fake product and it is full of typos.** A full-screen tablet showing an invented dashboard headed "AI OPTIMIZED PLAN - WEEK 4 (LEAN GAINS)". It is not our app, it is AI-generated slop, and the text is visibly broken: "ADAPTED **BASSED** ON MACROS & **NACROS** LOGGED", "Eas1 Defiotion (106 6g)", "Quinoas Food", the "SMART NUTRITION ADJUSTMENTS" header printed twice, "MACROS LOGGED" printed twice, and a garbled calendar. It also says "LEAN GAINS" in a fat-loss ad. Anyone who pauses sees a product that doesn't exist.

- **3:38 – 4:25 — fill this section with the real app screens.** 47 seconds of unbroken talking head. Use these full screen with a slow push in, cut to the lines that describe them:
  - "Our AI scans your current picture to assess your body fat percentage and your training status" (~3:38–3:47) → **10_APP_trainer-assessment.png** — https://drive.google.com/file/d/1wFsyT9eKeUVzDcF0L7bbAPn5DSAVdRIs/view
  - "Your workout plan works around your injuries… uses the specific equipment you actually have" (~3:55–4:04) → **11_APP_monday-workout.png** — https://drive.google.com/file/d/11AS0LYjs-LfUPuhhVqGdAtiN1sjkJ02j/view
  - "Your nutrition plan is calibrated exactly for your goal…" (~4:04–4:13) → **12_APP_meal-plan.png** — https://drive.google.com/file/d/1GhWuPso3bywsyYEmxk-I1y9WjkP5qkEh/view
  - For the body-fat scan line at 3:43, build a simple scan animation over the after image in brand colors: a scan line sweeping down, then stat lines appearing (Current Weight → Goal Weight, Body Fat %, Muscle Gain), ending on "Recommended Workout Plan". Label it, and do not show a finished plan.

- **4:25.4 – END — there is no end card.** The video simply stops on the talking head with the same glossy blue button. Add an end sequence: the after picture full screen and labeled, then a full-screen CTA card, white on dark green: "See Yourself With Abs — Free" over "Tap The Button Below". After picture: **01_HOOK+ENDCARD_ai-goal-image_dan-by-pool.png** — https://drive.google.com/file/d/1-8QAfoeAIt52fswKhFvg6ep1i4iqLGGu/view — shown ALONE, never beside the before.

---

## FOR ALL FUTURE VIDEOS

- **The joke Photoshop picture is only ever used on the line about fitness models photoshopping their faces.** It is never the hero image, never the lock screen, never the hook. Anywhere the script says "this picture", it means the real AI goal image.
- **Every AI-generated visual carries an AI Generated tag for its full duration** — the "\*AI Generated" label, upper-left and larger on full-screen clips. If a label ever has to be removed for a re-render, put it back before delivery.
- **Never invent a product screen.** If we don't have a real screenshot of something, we don't show it — we cover the line with the talking head or a text graphic instead. No AI-generated dashboards, no mockups of apps we don't make, no other companies' apps.
- **Deliver at −14 LUFS, true peak −1.5 dB or lower, every time.** Anything above −12 LUFS or peaking over 0 dB comes back.
- **Camera audio is always Mono from the Right channel.** The left channel on this camera is a distant room mic and must never reach the master.
