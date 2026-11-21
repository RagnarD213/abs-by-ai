**CONTENT / LFC. Next task: Top 1 Percent LFC R3.**

# RO-26 round 3: apply Dan's selected revisions

Prepared at Dan's explicit request on 2026-10-16 after he said, "That's it for revisions."
Recommended executor: **GPT-6 Sol, High**, using `$long-form-content-edit`.
This is the next editing round, not permission to upload or publish.

## Goal and source of truth

Build the revised first-minute draft and changed narrated contexts, repair the high-school incline frame pair, and generate/check the already-approved Nutrition B motion. Show the remaining workout frames for approval before generating workout motion. Preserve the selected colour, voice, real footage and recap design. Do not restart creative selection or ask Dan to repeat his picks.

Project root R: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.
Existing work W: `/Volumes/Extreme/_edit_work/ro26/round2`.
Revisions V: `W/revisions-20261016`.
Create new outputs under `/Volumes/Extreme/_edit_work/ro26/round3`; reuse immutable R2 sources and components.

Read current `R/AGENTS.md`, `R/.claude/skills/_shared/VIDEO-RULES.md`, PRE-RENDER-APPROVAL.md, CUT-CONTINUITY-QC.md, framecheck/README.md and the named skill:
`R/Media/codex-video-trial/skills/long-form-content-edit/SKILL.md`.

The authoritative collected decisions are `V/revisions.json`; exact selected frames are in `W/ai/final_pairs.json`. Also read `W/packet.json`, `cut_map.json`, `words_out.json`, `plan_resolved.json`, `edit_sheet_graphics.json`, `review/checks/asset-manifest.json` and `qa-summary.json`. This handoff and the latest user decisions supersede the older R1/R2 briefs where they differ.

The current Mac-local review is http://127.0.0.1:8982/. It still plays the earlier draft and contexts, with notices describing queued changes. R2 first-minute draft is 61.43 seconds. Existing project copy: `R/Videos to Review/Top 1 Percent LFC R2 - first minute.mp4`. There is no finished full film.

Source is 10/15 roll C1768, S-Cinetone/Rec.709, left-channel lav. Exact source path/map is in `W/cut_map.json` and `W/audio/audio_source.json`. Current speech cut is 305.672 seconds.

## Locked choices

- **Colour B: Clear Studio Look.** Exact filter and audition hashes are in `V/revisions.json -> colour_selection`. Already used by the current draft and queued contexts. Preserve it.
- **Voice C: Warm Bass.** Dan said "warm base"; this clearly selects the displayed Warm Bass option C. Exact EQ and audition hash are in `voice_selection` and `W/audio/opts/options.json -> C-warm-bass`. Keep the audition's shared chain, with no additional dereverb or compressor.
- **Nutrition B: Patio Salad Bite.** START `W/ai/N-B-start-final.png`, END `W/ai/N-B-end.png`. Both automatic and independent frame checks pass. Dan explicitly selected B; frame selection authorizes motion for this pair. START hash `3d8c16284bde28b01de4bbc339adc82a0101a883beef041de19441edce74a71c`; END hash `d7a961d4fd8747d617cfd9bec620527e68d0ca00d5ce686eb0c63d96a6eb8a5b`. Do not redraw or reopen the choice. Nutrition A was not selected.
- **G05 recap design remains approved.** Exact source `W/review/assets/G05-approved.png`, SHA-256 `5e6d0ea53d1c5d39033ff22a212898bd96c6ff4a7535edb6793a0e05559e4aeb`. Preserve the design and word-timed reveals.
- **All three Six Pack Shortcuts source choices look good.** Dan requested shorter cuts, followed by the real Flight Club speech for his advertising agency.
- Four section lower thirds remain Working Out, Nutrition, Starting a Business and Martial Arts, using shared Soft Blue Light/Motivation/HyperFrames 0.8.97.

No blanket final-film approval was given. Unmentioned candidates retain their recorded status. Do not infer approval for old workout B or generate its motion.

## Exact revisions

### 1. Opening: stronger previously retouched portraits

Replace the raw-photo trio at about 0:02 with the previously made stronger graphic treatment and touched-up images. This explicitly supersedes R2's raw-camera-only choice.

Verified earlier composition: `/Volumes/Extreme/_edit_work/wv01-edit/round10/graphics/portraits-final.jpg`.
Recipe: sibling `round10/recipe/components10.py`.
Reference copy: `V/refs/previous-three-photo-graphic.jpg`.
Staged sources: `V/retouched-opening-sources/`, comprising `studio-white-23_CUTOUT.png`, `studio-blue-173_CUTOUT.png`, `studio-blue-240_CUTOUT.png`.

Reuse the stronger portraits/treatment with copy suitable for this film and current Soft Blue Light standards. Preserve hair and abs. Do not retain the older graphic's "not AI-generated" claim: these are retouched photos. The rejected pool image remains excluded.

Planned trio range: 0.9009 to 2.5025. Rebuild it; it is not yet inserted.

### 2. Multimillionaire opening: exact Flight Club speech found

Use the actual speech matching Dan's attached reference: gray rolled-sleeve button shirt, glasses, lav, clicker and FLIGHT CLUB MASTERMIND backdrop, speaking to an audience. No fallback or further broad search is needed.

Drive: [Copy of 1-Dan Rose.mp4](https://drive.google.com/file/d/1YtxOSTAVA28l8wErSDYtMVOVBnkJukvg/view).
Local full source: `V/refs/Flight-Club-Dan-Rose.mp4`, 2,130,548,947 bytes, 1920x1080, 23.976 fps, 3744.366 seconds.
SHA-256: `9dc67cbb54bb52e22631e99030f9e018a290a9e8150169d528a0f7395a452eef`.
Reference: `V/refs/flight-club-reference.png`; verified stills/contact sheets are beside it.

Opening source selection: 317.0 onward, planned output 2.5025 to 3.9039 over "I'm a multimillionaire." Keep narration; mute speech-source audio. A short verified source preview already exists at `V/refs/Flight-Club-selected-stage-317-318.75.mp4`; its stream-copy preroll makes it unsuitable as the frame-accurate final trim.

### 3. Black-belt opening and supplemental image

Opening promotion insert is planned at 3.9039 to 5.9059 under the black-belt claim. Select the visible belt/hands moment at normal speed.
Real source: `W/refs/black-belt-instagram.mp4`, supplied Instagram post https://www.instagram.com/p/CuiCQVAJw7q/.
Group image: `V/refs/black-belt-group.png`, copied from Dan's supplied photo. Use it as supplemental in the later section, preserving the actual promotion clip.

### 4. Hinge: Dan's ripped photo and many matches at about 0:07

Reuse the previous populated-Matches animation with Dan replacing its fictional male profile. This has already been adapted and rendered as native UI, not AI video motion:
`V/hinge/hinge-Dan-many-matches.mp4`, 58 frames at 29.97 fps, 1.935 seconds.
SHA-256 `cd26a164805ff6be29747aa2b58944c6d656b7cd1271821e95f89ed5777670d5`.
Recipe/receipt: `V/hinge/render.py`, `prepare.py`, `screens.py`, `receipt.json`.

It uses retouched `R/photos/finalized social media photos/studio-blue-11_FINAL_PRIMARY.jpg`, Dan's name/avatar and the existing 24-match badge/seven conversations. The first 0.6 seconds show his profile; then populated Matches. Keep its illustrative-reconstruction disclosure for the fictional matches.

Planned output: 5.9059 to 7.8409, under "I'm enjoying an abundant dating life." Keep original narration. Inspect the actual clip and insertion boundaries; it is not yet in the draft.

### 5. Workout: high-school incline bench, not curls

Dan rejected the first workout concept. Replace it with younger Dan in a tank top doing incline bench press in a high-school gym, with other high-school students training around him. The narration explicitly says 16 immediately before this line, so age 16 is grounded in the script.

Use the high-school football-team line at 42.3219 to 44.5419; planned insert 42.3089 to 44.5779. Do not put high-school footage under the later "Then in my 20s" sentence. Keep presenter there until suitable selected coverage exists.

**No approval-ready replacement pair exists.** Attempts are in `V/high-school-incline/`. `START-wide.png / END-v3.png` failed independent anatomy review; `END-v4.png` failed the automatic gate. `START-side.png` is exploratory only and has no matching END. Reviews, measurements, specs and prompts remain there. They are not approved or displayed as passing on the page.

Repair/rebuild one coherent START/END pair, using a clearer angle if necessary. Preserve Dan's identity, tank top, school setting, other students, plausible incline mechanics, closed grips, rigid bar and anchored body. Do not repeat the same failed perspective blindly, loosen gates or substitute the old curls/lateral raises. The existing wide-scene body detector can confuse Dan with other students; use valid isolated measurements plus fresh independent review.

Generate stills with the Codex subscription. Write the spec before END, run the shared frame gate and a fresh independent frame reviewer using the long-form skill's GPT-6 Sol model rule. Show only a passing pair. **Workout motion must wait for Dan's approval of the corrected pair.**

### 6. Nutrition B motion

Generate/check motion only for the exact approved Patio B frames. Intended action: finish the forkful and withdraw the empty fork, retaining fork, bowl, hands, identity and scene. Planned slot 117.8314 to 122.8114 (about five seconds); planning estimate was a six-second take. Run clipcheck plus fresh independent review on the used portion, then show it with actual narration and surrounding presenter footage. Do not treat frame approval as approval of a defective motion take.

No AI motion has been generated or charged yet. Prior long-form motion cap is $15; verify current provider pricing before spending and record costs.

### 7. Business: quicker three-shot sequence, then Flight Club agency footage

Use shorter cuts at normal speed, not sped-up people. Proposed conformed timings already stored in `business_revision.shots`:

| Output | Picture | Length |
|---|---|---|
| 160.5604 to 162.5624 | Dan deadlifting with Mike at right | 2.002 s |
| 162.5624 to 164.3642 | Dan talking with Mike | 1.802 s |
| 164.3642 to 166.5330 | Dan as Story Of SixPackAbs.com CEO | 2.169 s |
| 166.5330 to 169.5360 | Real Flight Club speech | 3.003 s |

Reuse prepared `W/review/assets/BIZ1-deadlift.mp4`, `BIZ2-with-Mike.mp4`, `BIZ3-story-CEO.mp4`. Preserve authentic page framing and Dan/Mike identification. The first three now total 5.973 seconds rather than 10.5 seconds.

Agency narration is the full clean sentence "Then I followed it up by starting my advertising agency," at 166.5416 to 169.4616. The queued Flight Club trim starts at source 300.0 seconds; the source identity at 300 seconds is verified, but inspect the entire 300 to 303-second trim for camera/slide cuts before accepting it. Keep narration, mute source audio.

### 8. Martial Arts: promotion full screen from the section introduction, lower third over it

Dan said "The first thing I did right" while referring to the black-belt section. The actual recorded line is "The fourth thing that I did right"; align to that existing section, preserving narration.

Move the existing complete 7.5-second promotion selection (source 27.0 to 34.5) to output 211.2777 to 218.7852, beginning with the section introduction around 3:31. Put existing **G04 Martial Arts** lower third over the full-screen clip at its word-timed range 211.2685 to 215.0885.

Reuse `W/review/assets/MA-enhanced.mp4` and the exact shared G04 overlay/mask in `W/hf/renders/`. `plan_resolved.json` and the graphics edit sheet now record this background/layer order. Recheck the actual moving composite: faces, belt and promotion hands must remain readable. Do not repeat the previous layout where the heading ends before the clip starts.

The source is a 540x304 horizontal band inside a vertical montage, cropped at y328 and conservatively upscaled. It already crops part of the instructor's head. Preserve the ceremony and aspect ratio; do not invent faces or stretch it.

## Queued work and important implementation state

At handoff preparation, these two existing workers were alive, waiting on the shared build cap:
- PID 7316: `V/business_revision_render.py`, log `business-render.log`.
- PID 9499: `V/martial_revision_render.py`, log `martial-render.log`.

PIDs are a snapshot: check them and the outputs before restarting. Do not launch duplicates or kill unrelated builds. Both workers are configured to write revised contexts and contact sheets, **not publish unreviewed output**. Expected receipts: `V/business-render-receipt.json`, `V/martial-render-receipt.json`. Neither receipt or revised context existed when checked for this handoff.

Expected context names:
- `W/review/context/BUSINESS-r2-quick-flight.mp4`, surrounding timeline 156.5564 to 175.0749.
- `W/review/context/MARTIAL-r2-footage-heading.mp4`, surrounding timeline 207.2737 to 226.0925.
Each also gets a 540p review copy and contact sheets under V.

**Both workers imported the previous Voice D before Dan selected C. Their soundtracks need replacement with C before revised delivery.** Do not re-encode their pictures just to replace audio. `W/build_review.py` now selects C from packet.json and uses a separate `audio/cut-warm-bass.wav` cache; that WAV does not exist yet. Do not accidentally reuse `cut-light-bass.wav`.

The picture builder has been patched for quicker business cuts and the moved black-belt background, but **opening portraits, opening Flight Club/promotion and Hinge insertion still need integration**. Its older hardcoded raw-portrait opening/disclosure is superseded. Adapt in R3 rather than running the old whole script unchanged. Do not run another job's recipes.

Preserve existing speech repairs: complete "Today" intro, removal of failed agency takes with the single intact source241.6414 to244.7445 take, and restored complete martial-arts sentence. Do not undo the cut/word map or re-cut words from ASR guesses.

Old diagnostic delivery/audio gates are not final-film passes. The earlier Voice D failed strict reference-tone matching; C has not been checked as a complete edited soundtrack. Keep actual failures explicit without altering Dan's approved EQ to chase a reference score. No full-film SRT, final delivery stamps or independent full-film review exists.

## Exact next actions and round boundary

1. Claim R3; inspect existing workers/receipts, preserve R2 and reuse completed components.
2. Apply Voice C and the selected opening/Hinge edits; inspect revised business and black-belt contexts, including source-camera changes, belt/hand clearance, shared graphic checks, complete words and every changed join.
3. Rebuild and quality-check the high-school START/END pair. Independently complete the already-approved Nutrition B motion and its motion checks.
4. Present one R3 page: revised playable first minute at top, new workout frame pair, approved-choice nutrition motion, and changed business/black-belt/opening contexts with narration and 3 to 5 seconds either side. Use the shared floating scrubbable player, show exact new timestamps/watch ranges and identify any pending footage. Keep colour/voice picks recorded instead of asking again.
5. Test actual browser playback, seeking and audible narration; use the managed range-capable review server and copy videos of at least45 seconds to `R/Videos to Review/`. HTTP/ffprobe alone is not playback QA.
6. Stop for the corrected workout frames and remaining revised asset/motion approvals. **No workout AI motion before its frame approval; no full placeholder film, full final render, upload or release at this boundary.** Once required choices are locked, the later full-film stage still needs SRT, exact-file picture/audio gates and independent full-candidate review.

Update only RO-26 queue/master/own coordination and this handoff's index entry. No dashboard work, new scheduled routine or unrelated job changes. Costs recorded so far: $0 paid still API, $0 AI motion; listening costs estimated below$2, exact billing and editor/reviewer token usage unavailable.

## Ready-to-paste starter

Name this task "Top 1 Percent LFC R3". Execute `Handoffs/handoff-20261016-ro26-round3-selected-revisions.md` with `$long-form-content-edit` using GPT-6 Sol, High. Apply all collected revisions, preserving approved Clear Studio Look B, Warm Bass C, Nutrition B frames and the recap design. Reuse the found Flight Club source and prepared retouched portraits/Hinge footage. Inspect existing queued workers before launching anything. Build the revised first minute and changed narrated contexts, repair and show the high-school incline START/END pair, and generate/check only the already-approved Nutrition B motion. Do not generate workout motion until I approve its corrected frames. Do not render the full film or upload/publish in this round.
