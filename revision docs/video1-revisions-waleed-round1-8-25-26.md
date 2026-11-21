# Video 1 ("This Picture Got Me Abs") — Revision Notes for Waleed, Round 1

Google Doc (share this with Waleed after Dan approves):
https://docs.google.com/document/d/1wu1spi5KaQTK7gbPZ_HdWE8z87_osb8dnCt3_ruTDTQ/edit

Reviewed video: https://drive.google.com/file/d/1ZWv5t3rNitubDUDaSKcrn5SqVJCEX2ip/view (4:27, 1080p30, delivered 2026-08-24)
Editor: Waleed — one of the tryout editors cutting this same script. **First set of notes he has received.**

Note on tone: these are first-round notes for a tryout cut. They are written as goals, not as steps in
any particular program — Waleed is working with AI editing tools, so it is up to him how he hits each one.

---

## Nice work — three things are already right, keep them

1. **The pacing is excellent.** Total dead air across the whole 4:27 is 0.3 seconds. Most first cuts of this script come back loose; this one doesn't. Keep it exactly this tight.
2. **The punch-ins work.** Cutting between a wide and a tighter framing on the talking head is what we want, and the timing on the phrase boundaries is good.
3. **You used the real app screen recording at 1:18 instead of a mockup.** That is the single most important thing to get right in this ad, and most editors get it wrong. One fix is needed inside it (see 1:28 below), but the instinct was correct.

The notes below are everything that needs to change before this can run as an ad.

---

## THROUGHOUT VIDEO

**THE AUDIO NEEDS TO BE REBUILT FROM THE SOURCE — THIS IS THE #1 ITEM**

This one isn't your fault, but it has to be fixed and it can only be fixed at the source, so please read it carefully.

- **Our camera does not record a normal stereo pair.** It records **two completely different microphones**, one in each channel. The **right channel** is the lav mic clipped to Dan's chest. The **left channel** is a room mic about 9 feet away.
- Because the room mic is 9 feet further from Dan, its copy of his voice arrives **7.8 milliseconds late**, and on these files it is also **polarity-flipped** relative to the lav.
- Every phone, laptop and TV speaker mixes left and right together to play in mono. When these two channels get mixed, they partly cancel each other out. Measured on this export: **the voice loses 4.0 to 4.6 dB** and takes on a hollow, comb-filtered sound the instant it plays in mono.
- **What we need: the finished audio must come from the RIGHT channel of the camera files only, as mono.** Discard the left channel entirely for every talking-head clip. Whatever tool you use, the goal is the same — one mono voice track, sourced only from the right channel.
- **Do not try to repair the current mix** with EQ, de-reverb, denoise, or any AI audio-cleanup pass. Once the two mics are mixed, the cancellation is baked in and no processing can undo it. The voice has to be rebuilt from the source.

**THE MASTER IS TOO LOUD AND IS CLIPPING**

- This export measures **−8.0 LUFS with a true peak of +2.5 dB**. Our target is **−14 LUFS with a true peak of −1.5 dB or lower.** It is about 6 dB too hot.
- Because of that overload, **166,000 samples in the left channel and 29,000 in the right are clipped.** That is audible crackle and distortion on the loudest words, and it is currently baked into the file.
- Bring the level down and master to −14 LUFS with a ceiling of −1.5 dB. Do this **after** the mono-from-right fix, not before.

**ADD A MUSIC BED AND SOUND EFFECTS**

- There is no music under this video at all. We checked — the level between words is just room noise, with no musical content anywhere in the 4:27.
- Add a music bed running under the entire video, roughly **20 dB below the voice**. Use a royalty-free / commercial-use track; no attribution required.
- Add a short whoosh or pop on every text graphic and every insert as it enters and exits. Right now the graphics appear in silence, which is the main reason they feel flat.

**PUT EVERY GRAPHIC IN OUR BRAND COLORS**

None of the graphics currently use our colors. The yellow bullet text, the glossy blue "TAP BUTTON BELOW" button and the red-and-yellow comic "FREE" starburst all read as default stock templates. Rebuild all of them in this scheme:

- Background / panel: black, or our dark brand green **#162118**
- Header text: large, ALL CAPS, brand olive green **#8C9858** (this reads properly on black)
- Body text: off-white **#E9EEDE**
- Red **#E22222** only as an attention accent, never as a background
- Font: Manrope, Bold for headers
- **Title Capitalization on every graphic.** Don't copy the capitalization used in this document.
- For the look we're after, see the Abs By AI YouTube Shorts cover images.

**EVERY AI-GENERATED VISUAL NEEDS AN AI LABEL**

- There is currently no AI label anywhere in the video. We require one on **every** AI-generated image or clip, on screen for its **full duration**, reading "\*AI Generated".
- In this cut that means at minimum the phone lock-screen clip (**0:07.8–0:09.4**) and the heavier-Dan-on-the-couch clip (**0:09.4–0:12.6**), plus anything new that gets added.
- **Full-screen AI clips:** label in the **upper-left**, about 50% larger than a normal caption. **Small panel inserts:** small centered tag at the bottom of the panel.
- The photos of Dan at 0:13.4–0:15.1 are real photographs from his shoot, so those correctly need no label. When in doubt, ask — don't guess.

**COMPLIANCE — FOUR HARD RULES**

These come from Google Ads policy. A violation gets the whole ad account suspended, so nothing ships until all four are clean:

- **Never a side-by-side before/after**, AI or real. Before, then footage, then after, shown separately and disclosed, is fine. (Currently violated at 1:28 — see below.)
- **Never a morph or transformation inside one continuous shot** — no body visibly changing on screen.
- **Never negatively portray a fat or out-of-shape person, and no belly-fat close-ups.** (Currently violated at 0:22 — see below.)
- **Never show an email-capture form on screen.** Currently clean.

**VERTICAL CLIPS CAN'T SIT IN PLAIN BLACK BARS**

- The heavier-Dan couch clip at **0:09.4–0:12.6** is a vertical clip sitting in the middle of the frame with plain black bars either side.
- Fill the sides with either a brand-colored card behind the clip, or a blurred, enlarged copy of the clip itself. Never plain black.

**THE LAST 47 SECONDS HAVE NOTHING ON SCREEN**

- From **3:38 to 4:25** there is not a single insert, graphic or product screen — just the talking head for 47 straight seconds. That is the section where the product is actually explained, and it's the weakest stretch in the video.
- Across the whole cut, inserts and graphics cover only about **30% of the runtime.** We want roughly double that. The timestamped fixes below close most of the gap.

---

## TIMESTAMPED REVISIONS

- **0:00 – 0:04.4 (the hook) — WRONG PICTURE. This is the most important fix in the document.**
  The script says *"This picture got me abs and it's not even real."* The image on screen is the **joke Photoshop picture** — a stranger's bald head crudely pasted onto a bodybuilder's body. That image is a gag, and it appears in the asset folder only so it can be used on one specific line later (see 1:04). Opening with it tells the viewer in the first three seconds that the whole premise is a joke.
  Replace it with the real AI goal image: **01_HOOK+ENDCARD_ai-goal-image_dan-by-pool.png** — https://drive.google.com/file/d/1-8QAfoeAIt52fswKhFvg6ep1i4iqLGGu/view
  Present it as a brand-styled card rather than a plain floating rounded rectangle, with an animated highlight box drawing around it on the word "picture", and the AI label on it. Worth knowing: the physical printed photo taped to the door on the left of frame is the same picture — putting the highlight box on that instead would work just as well, and is a stronger moment.

- **0:03.8 – 0:06.4 ("I was 200 pounds")** — add a title graphic reading "200 Pounds". Use the real before picture full screen with a slow push in: **02_BEFORE-PICTURE_dan-200lb.png** — https://drive.google.com/file/d/11Qb559-mqga9FznIpC8tgxLLfz1BUKQX/view

- **0:07.8 – 0:09.4 (phone lock screen)** — same wrong-image problem: the lock screen on the phone is the joke Photoshop picture. Rebuild this mockup with the real AI goal image (01_HOOK, linked above) as the wallpaper. Add the AI label, upper-left, large.

- **0:09.4 – 0:12.6 (Dan on the couch)** — fix the black bars per the note above, and add the AI label. Clip: **03_CLIP_heavier-dan-looks-at-phone.mp4** — https://drive.google.com/file/d/1oWU1nx1K3EN-yIlaT0Sb7MSiteAzCGEj/view

- **0:13.4 – 0:15.1 ("this is where I'm at today")** — good, keep. Two of the four shoot photos are here. Add the other two so it plays as a sequence of four at roughly 0.4s each, each with a slow move: **06_SHOT3_photoshoot-towel-smile.jpg** — https://drive.google.com/file/d/1DlngN_zRBigpnCpqCjaEgWNXbq-g5FhP/view and **07_SHOT4_photoshoot-standing.jpg** — https://drive.google.com/file/d/14MaZWbcfU84uFPGFPf0ew2JPKfS0OTiY/view

- **0:15.4 – 0:31.3 ("In today's episode…")** — remove the fruit-bowl stock photo at 0:20.3 and build a bullet graphic instead. Header: "In Today's Episode". Bullets appearing one at a time, on the line that mentions each, evenly spaced:
  - How I Got Limitless Motivation To Work Out And Eat Healthy
  - What I Needed To Do To Lose My Belly Fat And Get Six-Pack Abs
  - How You Can Generate A Goal Picture Of Yourself With Abs For Free

- **0:22.4 – 0:25.8 — REMOVE. BANNED.** A three-second full-screen close-up of a stranger grabbing a roll of belly fat on a yellow background. This is exactly the belly-fat close-up and negative portrayal our ad policy prohibits, and it's off-brand on top of that. Cover the line with the bullet build above instead.

- **0:30.4 – 0:31.6 — REMOVE the comic "FREE" starburst.** A red and yellow cartoon burst with rainbow stars — it reads as a free template and it is nothing like our brand. Replace with a simple brand card: "Free" in olive green ALL CAPS on black, or drop the graphic entirely.

- **0:41 – 0:50** — add a lower-third chip: "The Problem" (white on dark green) over "No Time, No Motivation." (white on black). The office stock clip at 0:47.4–0:50.3 can stay.

- **0:50 – 0:58** — add a title card: "Visualizing Your Goal" over "One Of The Most Powerful Ways To Motivate Yourself".

- **1:04.3 – 1:15.4 (the Photoshop gag)** — **this is the one place the joke image belongs, and you've placed it correctly.** Two changes: it runs 11 seconds, which is far too long — cut it to about 4 seconds around "it looked ridiculous" — and put it in a brand-styled frame rather than a plain floating card. Clip version if you prefer it: **08_CLIP_crude-photoshop-gag.mp4** — https://drive.google.com/file/d/1IhiEN4f-jggd2MgHxHckoO5kr8lf12vP/view

- **1:18 – 1:35.5 (the app screen recording)** — using the real product here was the right call. Four fixes:
  - **1:28.5 – 1:30 — REMOVE. BANNED.** The "Meet the new you." screen shows **BEFORE and AFTER side by side**, along with "Estimated body fat 20–24% → 9%". A side-by-side before/after is the hardest rule we have. **End the recording before this screen appears**, on the after picture ALONE.
  - The panel is small and pushed to the right edge, so the text is unreadable at phone size. Make it noticeably larger.
  - The recording currently starts on the tail of the photo-crop screen — "Remove photo" is visible at 1:18. Start a little later, at the generation screen.
  - Source: **09_CLIP_app-generate-future-self.mp4** — https://drive.google.com/file/d/14yOV7t-9tlrg7J5ZROBlpDq25KFyXXMR/view — the usable window is 0:03–0:25, accelerated to fit the slot.

- **1:36 – 1:42** — add a statement bar: "If You Saw Yourself With Abs, You'd Be MOTIVATED To Make Your Dream Body A Reality."

- **1:43 – 1:52.7 (first CTA) — the "TAP BUTTON BELOW" button needs replacing.** It's a glossy grey-blue 3D pill that looks like an old Windows button, it's in ALL CAPS, and it sits on top of the printed pool photo on the door, which is the strongest thing in that corner of the frame. Replace it with a **full-screen CTA card**, white on dark green: "Get A FREE AI Image Of Yourself With Abs" over "Tap The Button Below".

- **1:53 – 2:09.4 (the benefits) — replace the text list with our AI clips.** The current graphic is a yellow-and-white bullet list in the top-left corner with no panel behind it, in sentence case, overlapping Dan's face and the door photo. Cut it. Use these instead, each full screen with the large AI label upper-left:
  - "You're more attractive to women" (~1:59) → https://drive.google.com/file/d/15g3Lf3oIcaGZpLM8QFvL4Qso-F81HgBt/view
  - "Men respect you more" (~2:01) → https://drive.google.com/file/d/1KAXCrU36IWBWpvMK3yIwnWocT4yfQa1z/view
  - "You feel better / more energy / health improves" (~2:03–2:09) → https://drive.google.com/file/d/1wXw7uSqKa_vFwnxr7oVbXDToqOZ0NREM/view

- **2:09 – 2:20** — add a lower third: "You Don't Need More Knowledge" over "You Need Motivation To Execute What You Already Know."

- **2:24 – 2:35 ("a 38 year old dad living a busy, stressful life")** — nothing is on screen here for 11 seconds. Use the busy-dad AI clip: **AI clip - busy dad no motivation (kitchen).mp4** — https://drive.google.com/file/d/1-VdGbUOkcTxj_gKfQFNEqK66JmLvDhfY/view — with the large AI label. Accelerate it to fit if it runs short.

- **2:37.4 – 2:42.2 — WRONG PICTURE AGAIN.** The script says *"Nothing worked to motivate me until I generated this picture and made it my phone lock screen."* The joke Photoshop image is on screen again. Replace it with the real AI goal image (01_HOOK, linked above) and label it.

- **2:53.5 – 2:55.6 (meal prep)** — the stock clip shows a bald, heavily-built man, and the chalkboard behind him reads "3200 CALS/DAY", which contradicts a fat-loss message. Replace with a clip of a lean man aged 30–50 doing meal prep, or drop it.

- **2:55.6 – 2:57 — REMOVE.** This is a generic third-party calorie-tracking app ("DAILY CALORIES 1320 cal") from a stock library. We never show another company's product as if it were ours. Replace it with our real macro tracker screen: **12_APP_meal-plan.png** — https://drive.google.com/file/d/1GhWuPso3bywsyYEmxk-I1y9WjkP5qkEh/view

- **3:16 – 3:21.7 (ChatGPT)** — the logo floats unframed over the fridge with a small blue "AI" chip next to it. Put the logo inside a small brand-styled card, and drop the blue chip.

- **3:35 – 3:38.3 — REMOVE. This is an invented product and it's full of typos.** A full-screen tablet showing a made-up dashboard headed "AI OPTIMIZED PLAN - WEEK 4 (LEAN GAINS)". It is not our app, and the AI-generated text is visibly broken: "ADAPTED BASSED ON MACROS & NACROS LOGGED", "Eas1 Defiotion (106 6g)", "Quinoas Food", the "SMART NUTRITION ADJUSTMENTS" header printed twice, "MACROS LOGGED" printed twice, and a garbled calendar. It also says "LEAN GAINS" in a fat-loss ad. Anyone who pauses sees a product that doesn't exist.

- **3:38 – 4:25 — fill this section with the real app screens.** This is the 47 seconds of unbroken talking head. Use these full screen with a slow push in, cut to the lines that describe them:
  - "Our AI scans your current picture to assess your body fat percentage and your training status" (~3:38–3:47) → **10_APP_trainer-assessment.png** — https://drive.google.com/file/d/1wFsyT9eKeUVzDcF0L7bbAPn5DSAVdRIs/view
  - "Your workout plan works around your injuries… uses the specific equipment you actually have" (~3:55–4:04) → **11_APP_monday-workout.png** — https://drive.google.com/file/d/11AS0LYjs-LfUPuhhVqGdAtiN1sjkJ02j/view
  - "Your nutrition plan is calibrated exactly for your goal…" (~4:04–4:13) → **12_APP_meal-plan.png** — https://drive.google.com/file/d/1GhWuPso3bywsyYEmxk-I1y9WjkP5qkEh/view
  - For the body-fat scan line at 3:43, build a simple scan animation over the after image in brand colors: a scan line sweeping down, then stat lines appearing (Current Weight → Goal Weight, Body Fat %, Muscle Gain), ending on "Recommended Workout Plan". Label it, and don't reveal a finished plan.

- **4:25.4 – END — there is no end card.** The video simply stops on the talking head with the same glossy blue button. Add an end sequence: the after picture full screen and labeled, then a full-screen CTA card, white on dark green: "See Yourself With Abs — Free" over "Tap The Button Below". After picture: **01_HOOK+ENDCARD_ai-goal-image_dan-by-pool.png** — https://drive.google.com/file/d/1-8QAfoeAIt52fswKhFvg6ep1i4iqLGGu/view — shown ALONE, never beside the before.

---

## STANDING RULES FOR EVERY VIDEO YOU CUT FOR US

- **Our camera audio is always taken from the RIGHT channel only, as mono.** The left channel is a distant room mic and must never reach the master.
- **Deliver at −14 LUFS with a true peak of −1.5 dB or lower, every time.** Anything above −12 LUFS, or peaking over 0 dB, comes back.
- **Every AI-generated visual carries the "\*AI Generated" label for its full duration** — upper-left and larger on full-screen clips, small and centered on panel inserts.
- **Never invent a product screen.** If we don't have a real screenshot of something, we don't show it — cover the line with the talking head or a text graphic instead. No AI-generated dashboards, no mockups of apps we don't make, and never another company's app.
- **Match the picture to the line being spoken.** Several of the fixes above are the right asset used on the wrong sentence. When the script says "this picture", it means the real AI goal image — never the joke Photoshop one, which has exactly one home, on the line about fitness models photoshopping their faces.
- **When you're unsure whether an asset is allowed, ask before you cut it in.** The compliance rules above are account-level risk, not style preferences.
