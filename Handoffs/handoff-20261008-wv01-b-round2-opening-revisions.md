# AD: Fired Them All AD R2

2026-10-08. Recommended model: GPT-6 Astra, high effort. Use `$vsl-edit`. This is the next revision of the WV-01 Version B website sales opening. Dan requested this handoff; the revisions and new images have not been made yet.

## First action and scope

Rename the task **Fired Them All AD R2**. Read `.claude/skills/_shared/VIDEO-RULES.md` in full, the VSL editing skill, shared image-generation and pre-render approval rules, and this handoff. Work in `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round2/`; preserve round1.

First deliver start/end frames for the firing scene and three alternative AI-training concepts, plus focused previews of the straightforward picture revisions below. Get Dan's frame/concept choice before generating new AI motion. Use the Codex subscription to generate the images. No image generation or paid motion was performed while preparing this handoff.

Scope is the B opening and its join into A. Do not build complete B, add the six C1700 callbacks, change approved A, upload, install or publish. Three AI-training concepts are alternatives for one placement, not three clips to install consecutively.

## Current cut and approvals

R1 is a completed first-cut preview, not a finalized video. Opening duration 254.921333 seconds; opening plus A context 265.031433 seconds. Review URL: http://127.0.0.1:8870/ . Current full-quality file:

`/Volumes/Extreme/_edit_work/wv01-edit/version-b/round1/previews/DRAFT - Fired Them All B opening and join 1080p.mp4`

SHA256: `6e60be3d333a603b45bf3a2214d5cc6d341bf44b3a9c59ef170157da376e7bba`.

Dan explicitly approved **color correction and audio** on October 8: "color Correction, audio is looking good". Preserve those exact treatments. This does not approve all graphics, framing, the join or the whole film. R1 uses A's grade C, source-fitted shared voice processing and no music. Keep narration timing and accepted audio unchanged for these picture revisions; stream-copy accepted audio where practical. Do not remix short excerpts just to clear a window-dependent audio score.

Read `Handoffs/results-20261007-wv01-b-opening-r1.md` and round1 `review/decisions.json`, `take-map.json`, `picture-repairs.json`, `QA.md`, `watch_pass.json`, `edit-sheet-validation.json`, `words_out.json`, `shots.json`, `assets.json`, `custom_graphics.json`, `join-map.json` and `plan_resolved.json`. Recipes are in round1 `recipe/prepare.py`, `build.py`, `finish.py`, `page.py` and `sheet.py`.

The new decision record and three supplied screenshots are saved under:
`/Volumes/Extreme/_edit_work/wv01-edit/version-b/round2/brief/`

Files: `dan-decisions-20261008.json`, `tight-crop.png`, `portrait-at-15s.png`, `promise-at-40s.png`. These are durable copies, not temporary clipboard references.

## 1. Opening: fire the three humans

Replace the current opening role cards with an AI-generated scene, three equal vertical panels filling a 16:9 frame:

- Left: male personal trainer in recognizable trainer clothes, slightly overweight and unimpressive. Dan called the desired look "kind of like a loser".
- Middle: female nutritionist, similarly slightly overweight and unimpressive, in a clearly readable nutrition-consultation setting.
- Right: female meal-prep worker cooking with many prepared meal containers in front of her, similarly slightly overweight and unimpressive.

Use average American physiques. No extreme obesity, grotesque caricature or exaggerated bodies. Make each occupation recognizable immediately.

Start frame: all three visible in their environments before any stamps. End frame: the same people and framing, with all three marked **Fired**. Generate clean underlying frames, then composite the exact large word separately so typography and timing are reliable. Supply a labeled storyboard showing the intermediate one-stamp and two-stamp states as well. In motion, each stamp lands separately with the corresponding person in the narration; mild disappointed reactions are enough.

R1 word anchors: "fired" 0.437s; "personal trainer" 1.117-1.877s; "nutritionist" 2.357-3.037s; "meal prep service" 3.617-4.437s. "Replaced" begins 4.897s. Use the actual spoken rhythm to land the three stamps, then transition into the AI-training shot. Do not alter Dan's voice to fit the imagery.

## 2. Next shot: AI training shirtless, ripped Dan

Dan explicitly requests an AI-generated depiction of himself working out, shirtless and ripped. Use his existing approved identity references and recognizable face, hair, glasses when appropriate, and physique. This permission is specific to this generated scene. The real photos in section 4 must stay real. Follow the established AI scene disclosure style.

Make **three start/end frame pairs**, one for each concept. Recommend the phone concept first. All three must communicate an active coach helping Dan exercise, not just Dan posing next to technology. Use a simple exercise with a plausible start/end movement, consistent camera, props and anatomy. Do not make incompatible poses or camera positions between the two endpoints.

### A. Phone projects an AI coach (recommended)

Start: shirtless Dan prepares a dumbbell curl beside a phone on a stand; blue light begins rising from the phone. End: Dan completes the curl as a life-size translucent coach projected from the phone indicates his elbow position, with a clean rep indicator. Keep the phone and the beam connection clearly visible. This adapts the established blue phone-projection language to actual training.

Located and visually inspected prior reference: **A0045**, three cyborg coaches emerging from a glowing phone, marked used-final in WV-01 opening. It does not itself show Dan exercising, so use it as the visual reference rather than pretending it fulfills the new shot.

`/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/04 AI-Generated Clips/concepts-and-gags/A0045_three-cyborg-coaches-over-phone_16x9_5s.mp4`

Contact sheet: project `Media/clip-library/contact/A0045.jpg`.

### B. Robot personal trainer

Start: Dan is ready to perform a dumbbell curl, with a sleek humanoid robot beside him watching his arm. End: Dan reaches the top of the rep while the robot demonstrates the correct elbow position and gives a clear positive cue. A restrained blue display can count the completed rep. Make the robot visibly useful as a coach and keep the shot grounded in a real gym.

### C. AI digital twin

Start: shirtless Dan and a translucent blue digital double stand side by side at the bottom of the same dumbbell movement. End: both complete the rep in sync, with one simple highlighted movement path and a confirmation cue. This shows AI demonstrating the correct movement and Dan following it. Keep the effect immediately understandable and avoid a busy screen of tiny data.

These are proposed concepts, not Dan-approved designs. Show all six endpoint frames for this second placement, alongside the first clip's pair, before motion generation. The user said "starting inference" in dictation; interpret in context as start/end frame concepts. No need to ask the same brief again.

## 3. Presenter framing

Dan wants less empty space above his head and a slightly wider tight shot so more of his body is visible. Match the main VSL already published at https://absbyai.com/start . Keep static framing, intact hair and natural proportions. Do not solve headroom by zooming in tighter.

Live page source checked October 8: desktop video is `https://absbyai.com/video/wv01-a-1080.mp4`; mobile is `/video/wv01-a-720.mp4`. Saved live HTML: round2 `brief/live-start-20261008.html`. The next task must compare representative live/reference presenter frames visually before locking the new crop. The media bytes were not compared to the local A master during handoff preparation.

Useful baseline: round1 B WIDE is `3552:1998:144:100`; TIGHT is `2608:1466:616:80` (width:height:x:y). Prior A presenter recipe in `/Volumes/Extreme/_edit_work/wv01-edit/round13/recipe/previews.py` uses WIDE `3552:1998:144:162`, TIGHT `2608:1466:616:184`. These are reference values, not an instruction to copy coordinates blindly across different source rolls. Show a representative revised tight shot beside the reference; check hair/headroom throughout affected shots, not just one still. Preserve the R1 fixes that removed three brief unintended camera shots.

## 4. Around 0:15: three real portraits

Replace P02-now (currently 14.887-17.237s), the single-photo "THIS IS ME NOW / AT 40" card, with a full-screen graphic containing three vertical real photos of Dan. Reuse prior VSL work. Do not repeat the later graphic at about 3:57, and do not regenerate or redraw Dan's real photos.

Good existing alternative, visually inspected: `/Volumes/Extreme/_edit_work/wv01-edit/round9/graphics/portrait-results-1.mp4`, with still `portraits-1.jpg` in the same folder. It uses **studio-blue-11, studio-blue-127, studio-blue-247**, three distinct poses. This was a previous proposed option, not the ultimately selected A trio; present its reuse as the R2 proposed replacement rather than claiming Dan already approved this choice. Its existing real-photo panel treatment is suitable. The next task may lift that trio into the requested full-screen layout; keep any text appropriate to this early narration rather than inventing new claims.

Later P04-results is at 235.552-240.332s and reuses `/Volumes/Extreme/_edit_work/wv01-edit/round10/graphics/portrait-results-final.mp4` with 0.6s source offset. That later trio is **studio-white-23, studio-blue-173, studio-blue-240**. Preserve it. The proposed early trio has zero overlapping photos.

Sources: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/photos/finalized social media photos/_cutouts/<name>_CUTOUT.png`. Existing render recipes: round9 `recipe/components9.py`, round10 `recipe/components10.py`. Maintain the real-photo disclosure and do not distort bodies.

## 5. Around 0:40: exact title replacement

G03-promise runs 36.117-44.557s. Replace its two text lines exactly:

- Blue: **What you'll learn today**
- Larger white: **5 ways AI beats human fitness experts.**

Keep the established style and readable placement. The supplied screenshot is `brief/promise-at-40s.png`. Check line breaks at the actual delivery resolution. Do not paraphrase, capitalize everything by default, or retain the old "THE PROMISE / 5 Things AI Did Better" copy.

## 6. Around 3:07: reuse the failed and successful planning clips

"307" means approximately 3:07, not 307 seconds; the current opening is only 254.9 seconds. Both requested existing clips were found in the library and their contact sheets were visually inspected.

**Failed plan: A0055, 6 seconds, used-final in WV-01 opening.** AI-Dan at a home laptop reads a generic ChatGPT plan and raises his hand to his forehead in frustration.

`/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/04 AI-Generated Clips/ai-dan/A0055_ai-dan-frustrated-laptop-generic-chatgpt_16x9_6s.mp4`

Existing A presentation with approved fixed crop and disclosure: `/Volumes/Extreme/_edit_work/wv01-edit/round10/graphics/laptop-insert.mp4`. Prefer this approved presentation if its duration fits; original library clip is available if needed. Preserve natural speed and gesture.

**Successful plan: A0043, 6.1 seconds, used-final in WV-01.** AI-Dan at a three-monitor desk compares five AI conversations, then refines the center monitor.

`/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/04 AI-Generated Clips/ai-dan/A0043_ai-dan-typing-three-monitor-desk_16x9_6s.mp4`

Contact sheets: project `Media/clip-library/contact/A0055.jpg` and `A0043.jpg`. Reuse these clips rather than regenerating them. Preserve existing scene labeling and apply the established disclosure if absent in the raw library copy.

R1 narration map from `review/words_out.json`:

- 185.092-190s: "So I tried it. I went to ChatGPT and Claude and asked them to get me in shape."
- About 190-201s: first results terrible, generic workouts, chicken and broccoli, one-size-fits-all template. Place the failed laptop clip on the most relevant complete phrase.
- About 201-209s: "But I didn't give up. I spent months prompting, reprompting, and testing five different frontier AI models against each other." Place the three-monitor clip here so the visual directly supports the five-model line.
- About 209-226s: different AIs do different jobs, right AI/right job, better results. Preserve existing G10-specialists at 210.91-222.33 unless a precise transition adjustment is necessary to prevent overlap.

Choose final in/out frames against speech. Do not stretch a six-second clip across the whole passage, freeze its last frame, or alter approved narration. Show the full failed-to-successful sequence in context.

## Delivery and verification

Make the still-frame approval sheet first. Complete the crop, exact text, real-photo reuse and existing planning-clip insertions without waiting on new motion choices. Then show short changed sections with narration and enough surrounding context to judge entries/exits. Once Dan picks the AI frames, animate only the selected designs, check anatomy/continuity and integrate them in a new round. Follow shared QA and actual budget rules. Do not reopen approved color/audio or pretend unchanged approvals cover new material.

Preserve approved A master `/Volumes/Extreme/_edit_work/wv01-edit/round17/final/WV-01 FINAL Website VSL A 1080p.mp4`, SHA256 `acddfb5b3bad7bb6d85f937b74054fafb4be33505f49ae91cd765a8ecac88836`. Existing join uses original A frames 5111:5414, exclusive end. A has creative approval but an inherited website delivery gate FAIL; do not relabel that PASS. R1 exact-file checks remain historical evidence, not R2 checks.

For every review video 45 seconds or longer, place a full-quality actual copy in `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Videos to Review/`, with a clear `Fired Them All AD R2` filename. Dan opens long clips in VLC. Verify copied bytes. Remove only this video's review copies after Dan has both reviewed and finalized it. R1 is not finalized; do not delete its review copies now. Preserve masters and sources.

The review server was repaired in commits c30c3c6 and 8087a17. It now runs under macOS launchd, restarts automatically and serves a local snapshot of linked assets so delayed reviews do not depend on a temporary shell session or background external-drive access. After updating the page and media, refresh its published snapshot by running from the project:

```sh
python3 .claude/skills/_shared/review_server.py 8870 '/Volumes/Extreme/_edit_work/wv01-edit/version-b/round2'
```

Do this only once a valid round2 page exists. Preserve working links and verify seeking, byte ranges, local cached assets and VLC copies. Prior browser-tool access to port8870 was blocked by its security policy; do not claim a visual browser recheck without a successful permitted check. Server health and local-file verification remain available. No reboot was tested, although worker restart recovery was tested successfully.

## Ready-to-paste starter prompt

AD: Start Fired Them All AD R2 using $vsl-edit. Read Handoffs/handoff-20261008-wv01-b-round2-opening-revisions.md and execute those revisions. Use the Codex subscription to generate the images. First show start/end frames for the three-panel firing clip and all three AI-training concepts before generating motion. Preserve my approved color and audio, match the published VSL framing, replace the 0:15 photo graphic and 0:40 text, and reuse the located laptop and three-monitor clips. Put review videos 45 seconds or longer in Videos to Review. Keep this scoped to the B opening and join; do not build complete B or publish.
