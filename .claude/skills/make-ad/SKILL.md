---
name: make-ad
description: >
  End-to-end production of an AI-generated video ad for Abs By AI, MadMuscles-style
  (9:16 vertical, 60–110s, AI characters + voiceover, stitched from 5–10s clips).
  Use this skill whenever Dan asks to make an ad, video ad, ad creative, ad variant,
  "MadMuscles-style" content, or to continue ad production at ANY stage (script,
  character sheet, voiceover, clips, assembly, variants) — even if he doesn't say
  "/make-ad". Also use when reviewing or revising a previously produced ad.
---

# Make-Ad: AI Video Ad Production for Abs By AI

**STATUS: v2 — updated 2026-07-30 after the completed "The Upload" pilot** (two
finished ads: narrator cut + first-person cut, total spend ~$40, both in
`ad-factory/the-upload/final/`). Every ⚠️ assumption was tested; the answers live in
the Lessons section at the bottom — READ IT BEFORE GENERATING ANYTHING. Keep updating
Lessons after every ad — this skill is supposed to get smarter each time.

## The one-paragraph mental model

Nobody generates a 90-second ad in one shot. An ad is ~10 short clips (5–10s each)
stitched in an editor with ONE continuous voiceover carrying the story across cuts —
the unbroken voice is what makes separate clips feel like one film. Characters stay
consistent because every clip is generated from the same written "character bible"
plus the same 3–4 reference photos. Dan approves at fixed gates; everything between
gates is Claude's to execute autonomously.

## Ground rules

- **Dan is non-technical.** Explain each step's result in plain language.
- **Every generation batch costs real money.** Before any batch (images, VO, clips),
  state the estimated cost and get Dan's OK if it exceeds ~$20. Check the Replicate
  balance is comfortably above $20 first — below that, Replicate throttles to
  6 requests/min (bit us during the FLUX work).
- **All models run on Replicate** via `REPLICATE_API_TOKEN` (in Railway env; read it
  the way the bake-off harnesses did). One account, one bill.
- **Work files live in `ad-factory/<ad-slug>/`** in the project root, which must be
  git-ignored (the repo is public; also keeps video files out of git). Layout:
  `script.md`, `character/`, `vo/`, `clips/`, `assembly/`, `final/`.
- **Approval gates are hard stops.** Never proceed past a gate on an old approval —
  a script change after clips exist means regenerating clips.

## Model routing (verified in production during the pilot, 2026-07-30)

| Job | Model (slug) | Notes | Verified cost |
|---|---|---|---|
| Character stills + B-roll start frames | `google/nano-banana-pro` | Face consistency = pass the close-up still as `image_input` on every call | ~$0.13/image |
| Dialogue clips (character speaks on camera) | `google/veo-3.1` | The ONLY way to do talking scenes (lip-sync repaint is banned — see Lessons). Output geometry unpredictable: ALWAYS cropdetect | $0.40/s with audio ($3.20 per 8s take) |
| B-roll clips | `kwaivgi/kling-v3-video`, mode `standard` (720p) | **NO reference-image input — consistency comes ENTIRELY from `start_image`** (a nano-banana frame). Flexible integer durations incl. 3s | ~$0.17/s no-audio (49s of pilot B-roll ≈ $8.35) |
| Voiceover | `minimax/speech-02-hd` (slug confirmed) | `<#seconds#>` pause markers work; `subtitle_enable` returned nothing — get timing from Whisper instead | cents |
| Voice clone (narrator == on-camera voice) | `minimax/voice-cloning` | Sample as **data URI** (Replicate file URLs fail "invalid file ext"); needs 10s–5min of audio; set `model: speech-02-hd` | ~$3 per clone |
| Caption timing | `vaibhavs10/incredibly-fast-whisper` with `timestamp: word` | Community model → use generic `/v1/predictions` with a version id, not the models endpoint | ~1¢ |

Pull each model's live OpenAPI schema from Replicate before first use instead of
guessing input fields — this caught real issues again in the pilot (Kling's missing
reference input, Veo's duration enum, the voice-clone file-ext check).

## The 11-step workflow

Steps marked **[GATE]** stop and wait for Dan.

1. **Brainstorm.** Source concepts from memory `ai-ad-creation-research` (10 pitched
   concepts + MadMuscles theme data). Proven themes: military/respect, tai chi
   master, calisthenics elder, podcast story. Our unique angle: the product's own
   before/after output IS the ad's proof — no competitor can copy that.
2. **Script.** Deliverable is `script.md` containing: (a) the hook (first 5s — this
   is what variants will swap); (b) ~12 numbered narration lines; (c) a shot list of
   8–12 shots, each with: duration, dialogue-or-B-roll, which model, and the full
   generation prompt including the character bible verbatim; (d) end card copy
   ("absbyai.com — see your future self free").
3. **[GATE] Dan edits the script.** Lock narration TIMING here too — narration length
   dictates every shot duration.
4. **Character sheet.** Write the character bible: one paragraph, exact face/age/
   build/outfit/setting. THE OUTFIT NEVER CHANGES between shots — costume drift is
   where AI characters fall apart. Generate 3–4 stills (front, profile, close-up)
   with the image models. For "The Upload"-style ads where the character's fit
   version appears: generate the after-body through the LIVE product pipeline
   (per memory `proof-banner-image-gen-process` — Dan's results beat ad-hoc
   prompting).
5. **[GATE] Dan approves the character sheet.**
6. **Voiceover.** One continuous MP3 of all narration lines. Note the duration — it
   is the ad's skeleton.
7. **[GATE] Dan approves the voiceover** (send the MP3 with SendUserFile).
8. **Clips.** **Draft in the Gemini app first (free), then generate approved shots
   through the API** — see "Free drafting on Dan's Gemini subscription" below.
   Generate per the shot list: Veo for dialogue shots (pass the character
   stills as reference images + the bible in the prompt), Kling/Seedance for B-roll.
   QC each clip by extracting 3–4 frames (ffmpeg) and inspecting them: anatomy,
   outfit match, setting match, no text artifacts. Auto-retry duds — pilot measured 10/10
   first-try passes when every clip animates from a face-locked start frame. Only surviving clips go to Dan.
9. **Assembly (ffmpeg, NOT CapCut).** Build `assembly/build.sh` per ad: concat clips
   in shot order, trim cuts to narration beats, lay the VO, duck a royalty-free
   music bed under it, burn bold captions (ASS subtitles, MadMuscles style: large,
   centered-low, word-emphasis), append end card. The script IS the timeline —
   any tweak is a one-line change + re-render, which is what makes variants cheap.
   Caption spec + word-timestamp method: see Lessons (canonical). If a cut feels flat,
   the clips + VO folder can go to a human editor (Romeysa) for polish instead.
10. **[GATE] Dan approves the assembled ad** (send the MP4). He judges motion, lip
    sync, and pacing — frame QC can't catch those.
11. **Variants.** Swap ONLY the hook (new 5s opening clip and/or first narration
    line), re-render via the assembly script. Name `<slug>_v1..vN` like MadMuscles.
    **[GATE] Dan approves variants.** Deliver finals from `final/`.

## Free drafting on Dan's Gemini subscription (measured 2026-08-10)

Video is the single biggest line item in ad production — the pilot spent $16 on five
Veo takes and ~$33 on Kling in one month, and **most of those takes were iteration,
not the finished shot.** Dan pays for **Google AI Pro** ($19.99/mo), which includes
Veo generation in the Gemini app at zero marginal cost. Use it for the deciding pass.

**How:** drive `gemini.google.com/app` with the claude-in-chrome tools (Dan is already
signed in; no OAuth grant is needed, unlike `labs.google` Flow which prompts for one).
`+` → **Create video** → type the shot prompt → Enter. Poll with screenshots; the tab
title flips to "…Ready" when done. Download with the download button, which needs Dan's
one-time OK because it writes to his Downloads folder.

**What you get, measured on a real generation:**

| | Gemini app (subscription) | API (Replicate/Google) |
|---|---|---|
| Cost | **$0** | ~$3.20 per Veo take |
| Wall time | ~7 min | ~2 min |
| Output | 1280×720 landscape, 24fps, h264 + real AAC audio | full-res, native vertical |
| Watermark | **yes** — persistent Gemini sparkle | none |

**The watermark is real but does not block drafting.** It is a translucent
four-point sparkle roughly 45×45 px in a 1280×720 frame, inset about 10% from the
right edge and 80% down, present on **every** frame. It landed on the subject's
shoulder in the test, not in a safe corner. Two consequences:
- A **9:16 centre crop excludes it entirely** (the crop spans x 437–842; the mark
  sits at x≈1105–1155), so a vertical draft comes out clean with no retouching.
- **It is still not usable for finals — but resolution is the real reason, not the
  watermark.** A 9:16 crop of 720p is only 405 px wide, a 2.7× upscale to reach
  1080×1920. Visibly soft, and the whole pitch of these ads is that they look real.

**So: draft in the app, finish through the API.** Use it to answer "does this shot
idea work, is the motion right, does the composition read" — then spend the $3.20
only on shots that survived. On the pilot's numbers that is roughly 30 of 40 takes.

**The binding constraint is a daily cap, not the monthly credit pool.** Pro is ~1,000
Flow credits/month but is reported to allow only ~3 quality videos/day. **Not yet
measured** — find out on the first real batch and record the number here. If it
bites, that caps drafting throughput regardless of budget.

## MadMuscles reference patterns (why these choices)

Their $488M/yr machine (VidTao, July 2026): all ads 9:16, 60–110s, AI character +
AI VO, themes rotated by performance (tai chi → military), 5–10 hook variants per
script, losers killed at ~$5k spend, winners scaled to $200k+/30d. Reference winners
to study: youtu.be/lfa71t4RAyw ($224.8k/30d military street-interview),
youtu.be/HZLYJPGi8gI, youtu.be/3-dC0_qRXd0 (male tai chi). Full data in memory
`ai-ad-creation-research`.

## Lessons learned (append after every ad)

### From "The Upload" pilot (2026-07-29/30 — two finished ads, ~$40 all-in incl. every retake; a clean rerun of both would be ~$20-25)

**The five rules that were paid for in retakes — do not relearn these:**

1. **NEVER use lip-sync repaint models (`kwaivgi/kling-lip-sync`, latentsync, etc.) for talking scenes.** Dan rejected the result on sight ("obviously AI... not really getting it"). Mouth-repainting decouples lips from jaw/cheeks/head and the eye catches it instantly. Talking scenes = **Veo 3.1 native dialogue only** — it generates voice + face together with real speech physics. That's what "looks like a guy talking."
2. **Narrator voice == character voice via voice cloning, not the other way around.** Flow: generate the Veo talking takes first → extract their audio → clone it (`minimax/voice-cloning`, data-URI sample, ~$3) → synthesize ALL narration with the clone (`voice_id` saved in `vo/clone-voice-id.txt`). First-person ads (character narrates own story) are Dan's preferred format over third-person narrator.
3. **Captions are ALWAYS generated from Whisper word-level timestamps of the FINAL mixed audio** (`assembly/captions-from-words.js`) — never from estimated line windows. Estimates drift the moment the voice changes; Dan caught it immediately. The transcript's sentence map is also the cut sheet: realign scene boundaries so lines land on matching visuals ("lock screen" line over the phone shot, etc.).
4. **The after-photo is the product being sold — be pickiest there, and the target is the KINO BODY**: lean, sharp abs, deliberately NOT bulky ("a 40-year-old on the Kinobody plan"). Winning recipe through the LIVE pipeline: dream-physique description "lean and athletic, sharp defined abs, slim waist, not bulky — not a bodybuilder" + the app's real "Fix my result" pass ("not enough change" chip + "sharpen abs, add ZERO muscle size"). The plain male Ripped tier reads too muscular for ad use.
5. **Veo's output geometry is a lottery — cropdetect every take.** `aspect_ratio: 9:16` is IGNORED in reference-images mode (true 16:9 out). Image-to-video mode returns 9:16 content PILLARBOXED inside 1920x1080 with varying bars (602 or 608 wide, once ~square 1036) — crop with the measured values, never assumed ones.
6. **Export the finished ad at 1.2x speed, not the raw assembled pace.** Both v1 and v2 of the pilot were produced at normal (1.0x) pacing; Dan asked for both to be sped up afterward and confirmed he prefers the 1.2x cut — that faster pacing is now the target, not a post-hoc tweak. Build the ad normally start to finish, THEN apply a final speed pass: `setpts=PTS/1.2` on video + `atempo=1.2` on audio in the same ffmpeg call (pitch-corrected, no chipmunk voice, stays lip-synced). Use the bundled `ffmpeg-static` binary at `ad-factory/the-upload/node_modules/ffmpeg-static/ffmpeg` (no Homebrew needed). This is the very last step, after captions are burned in — captions are timed off the final mixed audio (rule 3) and setpts/atempo scale them proportionally, so speeding up post-caption-burn keeps everything in sync; do not try to build at 1.2x from the start.

**Costs & reliability actually measured:**
- Kling B-roll first-try success: **10/10** (the skill predicted 1-in-3 retries). The consistency workflow is what does it: every clip animates from a nano-banana start frame built from the character stills; Kling prompts describe MOTION only. Kling ≈ 133s/clip wall time; Veo ≈ 80-130s.
- Character sheet: still 1 from text, stills 2-4 with still 1 as `image_input` — zero drift, zero retries. Same trick for every start frame (face-locked close-up as first ref).
- MiniMax voices: the three "storyteller" voices didn't match a solid 40s everyman; deeper set fit. **ManWithDeepVoice** chosen for the pilot's character. PatientMan reads ~30% slower (80s vs 58s for the same script) — voice choice changes ad length; re-transcribe + re-time after ANY voice change.
- Full pilot spend ≈ $40: nano images ×~22 ≈ $2.90, Kling 49s+16s regen ≈ $11, Veo ×5 takes $16, MiniMax TTS ~$0.40, clone $3, product generations ~$0.35, lip-sync experiments $0.25 (dead end), Whisper ~2¢.

**Caption spec (defined from MadMuscles' $224.8k ad, now canonical):** Arial Bold 86px at 1080x1920, white, black outline 7, shadow 3, bottom-center with MarginV 690 (~62% height), 2-4 word chunks broken at punctuation and >0.6s audio gaps, uppercase for punch words (ABS, YOU, FREE, WEIGHTS/WALKS/PROTEIN). Persistent micro-disclaimer, 26px translucent at ~82%: "AI-generated actor. Story for illustration purposes only. / Results are not guaranteed." (they burn one into every ad; so do we). ASS gotcha: the Events Format line MUST include the `Effect` field or every caption gains a leading comma. Fonts: copy Arial Bold/Black from /System/Library/Fonts/Supplemental into assembly/fonts and pass `fontsdir` (no Homebrew on this Mac — ffmpeg comes from `npm i ffmpeg-static`, has libass).
- No captions over the end card (the card text collides) and keep the AI-GENERATED label clear of the caption band (y≈1345 works).

**Audio gate on the final mux (2026-09-02):** run `python3 .claude/skills/_shared/audio/audio_gate.py FINAL.mp4 --synthetic` on the delivered file (and on the 1.2x export) — an AI voice has no camera room to match, so `--synthetic` keeps the loudness (−14 ±1 LUFS), true peak (≤ −1.0 dBTP), centred-image, no-silent-second and audio-length rows. It writes the stamp beside the file; a FAIL is not deliverable.

**Assembly architecture that made 6+ re-renders cheap:** per-segment intermediate MP4s (uniform 1080x1920@30 h264+aac) → concat → burn ASS → single audio bed. Mute ALL segment audio except Veo talking scenes; lay the VO MP3s at exact offsets. Every revision (new voice, new scene timing, caption fix) = edit `build*.js` + 2-min re-render, zero regeneration. Timelines in `timeline*.json`; silencedetect (`-35dB:d=0.3`) maps VO pauses; Whisper maps words/sentences.

**Product-capture recipe (S5 app-demo segment):** run the REAL flow in the iOS Simulator — `xcrun simctl addmedia` the character's photo, drive the actual photo picker, real generation, `simctl io screenshot` at retina (1206x2622), Ken-Burns the stills with zoompan. 100% genuine UI. **MANDATORY cleanup: the generation saves into the logged-in demo account (danroseconsulting+applereview@gmail.com — the Apple-review account!) and STEALS ITS HOME-SCREEN HERO. Delete the stray transformation from My Transformations and verify the curated beach-man hero is restored** (bit us twice; the app was Waiting for Review both times).

**Misc that will bite again if forgotten:** Replicate community models need `POST /v1/predictions` + `version` (models endpoint 404s). The Replicate files API loses filename extensions — pass media as data URIs. Balance has no API — check replicate.com/account/billing via Dan's Chrome (was $22.97 pre-pilot, card on file). The AI-reveal effect (scan flash + AI-GENERATED drawtext) is pure ffmpeg on the hook — free, reusable. MadMuscles reference pacing: long 5-10s conversational shots, 2 settings intercut, direct-to-camera close. Wispr voice-dictation: "abs" transcribes as "ads", "Kino body" as "keno body".
