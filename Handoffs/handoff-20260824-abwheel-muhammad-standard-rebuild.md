# Handoff: Rebuild the ab-wheel longform to Muhammad's standard (Plan A), then rebuild /longform-edit so it can't regress (Plan B)

**Date:** 2026-08-24
**Project:** Abs By AI — longform content pipeline
**Business goal this serves:** Clear the editing backlog in-house at $0/video, and settle the "decide the video-editing stack" question with evidence instead of opinion.

## Objective

Two phases, in order, then a set of questions for Dan.

**Phase A** — rebuild `FINAL_ab-wheel-beats-every-crunch.mp4` to the standard of Muhammad A's cut of the same footage. Dan on our version (2026-08-24): *"substantially better than what we made. It looks better, it sounds better, and the graphics are better. Everything about his video is better than ours."*

**Phase B** — change `/longform-edit` so the next video starts at that standard instead of arriving at it after a rejection. **The core problem is not missing technique — it is that the skill's quality bar is prose and its quality gate is code, so the style steps are skippable and got skipped.**

**Phase C** — only after B is done, ask Dan the open questions (listed at the end). **Do not ask them earlier; Dan explicitly wants the work done first.** Nothing in A or B is blocked on them.

The full measured analysis is published at
**https://claude.ai/code/artifact/061cbf89-e97c-47b4-b008-fa4183284c61** ("The Muhammad Standard").

---

## ⚠️ READ THIS FIRST — the working drive changed

**The Seagate 4TB is gone. Everything now lives on `/Volumes/Extreme/`** (a SanDisk Extreme, exFAT). The migration is complete and nothing was lost — segment cache, transcripts, recipes and the delivered files are all present.

**Every script in `_edit_work/` and in the skill's `reference/` has `/Volumes/Seagate 4TB/` hardcoded.** Fixing those paths is step A0 and it is not optional — the builders will fail immediately otherwise.

exFAT notes: `._`-prefixed AppleDouble files appear next to everything (harmless, ignore them), and `mv` prints a benign `set flags … Invalid argument` warning.

---

## Current State

### What exists and is good
- **The cut is editorially correct and Dan has not asked for content changes.** 18 beats from four rolls, take choices documented, one real audio defect already found and fixed (a clipped fricative on "crunches"). Keep the beat structure; Phase A changes presentation, not which takes are used.
- **The colour grade is BETTER than his — do not touch it.** Ours: mean luma 141, black point 3. His: 129, black point 19. Per-roll crush curves are in `ranges.py` (`GRADES`) and were validated closed-loop.
- **Loudness is better than his** (−14.6 LUFS vs −16.0). Keep the corrective measured-value loudnorm pass.
- **The segment cache works** — the one re-cut last session reused 17 of 18 beats. Re-cutting is cheap.

### What is wrong
| | ours | his | note |
|---|---|---|---|
| runtime, same content | 8:58 | **6:58** | he has 1,315 words to our 1,365 |
| pace | 152 wpm | **189 wpm** | |
| dead air ≥0.25 s | 192 s (36%) | 96 s (23%) | |
| visual cuts (scene detect) | **1** | **54** | ours is one locked wide shot for 9 min |
| median shot | 269 s | 3.3 s | |
| insert coverage | 21% | ~90% | spray tan shipped 51% |
| longest bare stretch | **64 s** ×2 | — | Dan's own written rule is 30 s max |
| voice centring (L/R corr) | **−0.005** | +0.993 | |
| music bed | none | yes | |

### The audio defect — fix this even if nothing else gets done
**The delivered file plays Dan's voice out of the right speaker only and hiss out of the left, for all nine minutes.** On rolls C1630/C1631/C1633 the LEFT channel is dead: SNR 0.4–1.0 dB (no speech at all), right channel 31–43 dB, zero-lag correlation ~0.000. The edit shipped the camera's raw two-channel recording as stereo.

This is **not** the two-mic comb filter documented in Step 5.6 for the 8/3 rolls — it is worse and simpler: one channel is empty. The fix is the same (right channel only).

---

## Key Decisions Already Made

- **Keep the beat structure, the take choices and the grade.** Phase A is presentation.
- **Music is already settled and is NOT a blocker.** `/ad-edit` rev-5 uses a **Pixabay** track — the Pixabay Content Licence permits commercial use with **no attribution**, deliberately chosen over CC-BY so nothing has to be credited in perpetuity. Use the same source, and pick the specific track **by measurement** with `reference/rev5/pick_bed.py` (scores spectral shape + flatness against Muhammad's own bed). Whether to upgrade to a paid subscription library is a Phase C question, not a Phase A decision.
- **Skip the vintage infomercial clip for now.** Muhammad used real archival footage of the original ab-roller infomercial when Dan says the wheel was sold on one. It works, but it is third-party copyrighted material on a monetised channel. Build the video without it; ask in Phase C.
- **Burned captions ON for this video.** The skill's "SRT, not burned in" rule was decided for the meal-prep split-screen tutorial, where captions fought the app UI in the left 570 px. It should be scoped to that case, not global. Ship burned captions **and** the `.srt`.
- **Do not re-litigate the split-screen/PiP or SRT-upload decisions** for tutorials that actually have a screen recording — those still stand.
- **No AI spend.** Everything here is local Whisper, ffmpeg, PIL, Pexels and Pixabay. If a step seems to need a paid API, it is a wrong turn.

---

## Detailed Plan — PHASE A: rebuild the video

Work in `/Volumes/Extreme/_edit_work/abwheel/`. Deliver over the existing folder (keep the old master alongside as `*_PRE_MUHAMMAD.mp4`).

0. **Repath everything.** Rewrite `/Volumes/Seagate 4TB/` → `/Volumes/Extreme/` across `_edit_work/abwheel/*.py` and the skill's `reference/*.py`. Confirm `ffmpeg` runs from `/Volumes/Extreme/_edit_work/bin/`. **Export `PATH` in every background command** — Whisper shells out to ffmpeg and fails with `FileNotFoundError: 'ffmpeg'` otherwise.

1. **Fix the audio (do this first, it stands alone).**
   Recipe already proven on the spray-tan and the four 8/23 longforms:
   `reference/chan_analyse.py` → `build_audio_singlemic.py` (right channel only, frame-locked to the existing picture) → `fitvoice_longform.py` (**fit the EQ to THESE rolls — do not copy another roll's curve**) → `finish_audio.py` → `-c:v copy` remux.
   Assert: L/R correlation ≥ +0.99, side ≥ 20 dB under mid, no drift against the rendered picture.

2. **Tighten to ~190 wpm.** Remove ~95 s more dead air. Use `reference/rev5/tight_full.py` as the model: **silence measured from a 5 ms RMS envelope of the real audio, never from Whisper's word times.** Cuts go *inside* beats, not only between them. Target 7:00–7:15. Do not cut into the three live workout sets' rep cadence — trim the gaps around them.

3. **Punch-ins.** Port the zoom-cut system from `/ad-edit` Step 3. Every join becomes a reframe, and any take longer than ~12 s gets a mid-beat reframe. Source is 1920×1080, so keep crops ≥ ~72% of frame width or it softens visibly. **Target ≥ 40 detected scene changes** (measure with `select='gt(scene,0.25)'`, the same way the gap was measured).

4. **B-roll — this is the biggest single lift.** Follow `Step 5.5` exactly; it is already written and was skipped last time.
   - `reference/plan_map.py` prints the output timeline, existing graphic windows, and every gap with the transcript text inside it — **map the existing graphics first, then fill gaps**, so each clip is chosen for the line it illustrates.
   - Pexels, no key: search pages 403 to curl, but a page open in the in-app browser can `fetch('/search/videos/<term>/')` same-origin. Download via `https://www.pexels.com/download/video/<ID>/`.
   - Pre-render each insert to an exact-duration 1920×1080 MP4 (`build_inserts.py`); vertical stock gets a blurred fill, never a centre-crop.
   - Terms that map to this script: ab wheel rollout, core training, gym abs, plank, dumbbell rack, home workout mat, crunches, gym interior.
   - **Target 25–35 clips and ≥ 50% coverage, longest bare stretch < 30 s.** `reference/verify_cover.py` asserts it.

5. **Rebuild graphics as animation.** Convert all 18 static chips to `motionlib.py` components (in `.claude/skills/ad-edit/reference/`, palette `motionlib.GREEN` — written for exactly this and never wired into longform). Add, matching his frames: full-screen title cards that build line-by-line on the dark-green field with corner brackets; the muscle-name stack (Rectus Abdominis / Transverse Abdominis / Internal Obliques) appearing as he names them; a large **$17** callout; numbered section labels ("02 — It Has A Built In Progression"); framed rounded insets for the rollout footage. Contact sheets of his design are at `ref_muhammad/sheet_0.jpg`–`sheet_2.jpg`.

6. **Burn captions** in the olive chip style, word-timed **from the final mixed audio** (`reference/rev5/captions5.py` is the model). Suppress captions over full-screen cards; shift them clear of any panel. Rebuild the `.srt` against the new cut too.

7. **Music + SFX.** Pixabay bed chosen by `pick_bed.py`, ducked under the voice; whooshes/pops from `sfxlib.py` on every graphic entrance; light-leak flares on cuts. Re-run the corrective loudnorm afterwards and re-measure — **do not chase −1 dBTP with `alimiter`**, it costs a dB of loudness per dB of peak (already measured).

8. **Replace the end card** with a real app screen — the phone mockup running the absbyai.com generation flow, as the ad pipeline already builds. Muhammad ends on this; we ended on a text box.

9. **QC against the NEW gates** (see Phase B step 1 — write the gates first if that is easier), re-run `tailcheck.py` and `srt_validate.py`, then deliver: master + srt + chapters + a ≤28 MB review copy, updated `notes.md`, and send the review copy to Dan.

---

## Detailed Plan — PHASE B: rebuild the skill

1. **Move every style rule into the automated gate.** This is the point of the whole exercise. Add hard failures to `reference/qc_generic.py`:
   - longest bare stretch > 30 s → FAIL (Dan's rule, currently prose only)
   - insert coverage < 40% → FAIL
   - detected scene changes < 4/min → FAIL
   - any audio channel with SNR < 10 dB, or L/R correlation < +0.9 → FAIL (catches both the dead channel and the comb filter)
   - dead air ≥ 0.25 s exceeding ~25% of runtime, or pace < 170 wpm → FAIL
   - no music bed detected (noise floor never drops below ~−50 dBFS is the signature) → FAIL
   - captions absent on a talking-head video → FAIL
   Each failure message must name the fix and the step number.

2. **Merge the modern toolkit into longform.** `motionlib.py`, `sfxlib.py`, the zoom-cut system and the music/duck chain currently live only under `/ad-edit`. Move them to a shared location both skills import (e.g. `.claude/skills/_shared/`) so a fix in one reaches the other, and update both SKILL.md files to point at it.

3. **Write the house-style spec from his frames.** One reference doc with measured values for the title cards, caption chips, section labels and framed insets, so every future video is the same product rather than a fresh interpretation. Measure off `ref_muhammad/` rather than from memory.

4. **Re-order the skill.** Coverage, punch-ins and captions currently sit late (Steps 5.5–8), which is where a session runs out of room — and is why they were skipped. Move them up next to the cut, and mark them REQUIRED with their gate values inline.

5. **Scope the subtitle rule.** Rewrite Step 8: burned captions for talking-head content; `.srt` only for split-screen tutorials where a screen recording occupies the frame. Both get an uploaded `.srt`.

6. **Record the meta-lesson** in SKILL.md, plainly: *a quality bar that only exists in prose will be skipped under time pressure; if it matters, it fails the build.* This is the third time a metric or a rule has been the problem rather than the media.

7. Commit and push (media stays out of git — run `git check-ignore -v` before staging), update `AI_COORDINATION.md`, check the dashboard task off via `/dashboard-tasks`.

---

## PHASE C: questions for Dan — ONLY after Phase B is complete

Ask these together, in chat, with a recommendation on each:

1. **Stock footage library.** We use Pexels (free, no key, no attribution). Muhammad's gym clips look like premium stock. Does Dan want a paid footage subscription (Artgrid / Storyblocks, roughly $25–50/mo) for better and more specific coverage, or is Pexels good enough? *Recommend: stay on Pexels until a video is actually blocked by it.*
2. **Music library.** The Pixabay bed is licensed, commercial-safe and free. Upgrade to Epidemic Sound / Artlist (~$15–25/mo) for range, or keep Pixabay? *Recommend: keep Pixabay for now; revisit if the channel starts sounding repetitive.*
3. **The archival infomercial clip.** Use Muhammad's, source a licensed equivalent, or skip it? It is third-party footage on a monetised channel. *Recommend: skip unless he wants it; the joke lands without it.*
4. **Are we still building in-house?** This is the second time an outside editor has beaten the pipeline on the same criteria. Once Phase A ships, Dan has a like-for-like comparison on the same footage. This feeds the dashboard task `business::Decide the video-editing stack`.
5. **Does the new standard get applied retroactively** to the five delivered longforms (spray tan, Zepbound, supplements, invest-health, meal prep), or only forward?

---

## Things to Avoid / Lessons Learned

- **Do not skip Steps 5.5 and 5.6 again.** They are correct, they are written, and skipping them is exactly what produced this rebuild.
- **Do not touch the colour grade.** It already beats his. Anchor crush points stay per roll.
- **Do not re-fit a voice EQ by copying another roll's curve** — the spray-tan roll needed the *opposite* low-end correction to the ad roll.
- **Never validate a joint with a Whisper window that ends at the join.** It drops the final word (7 false "missing word" reports last session) and can invent a doubled phrase. Windows must extend ~1.5 s past the join.
- **A −30 dB `silencedetect` cannot see a trailing fricative.** If the stretched-last-word rule fires on a word ending in s/sh/f/th/ch, check at −45 dB. Do **not** promote −45 dB to a general assertion — outdoors it flags almost every edge.
- **The QC split metric must be guarded on `source`** for multi-roll videos, or a roll change reads as a −72 s "artificial split".
- **zsh eats `$VAR:a` and `$VAR:l`** as path/case modifiers inside ffmpeg filter strings — always brace: `${VAR}:attack=5`.
- **ffmpeg eats stdin in loops** — pass `-nostdin` and `</dev/null`.
- **The camera audio clips in-camera at +2.94 dBTP.** The edit cannot undo that. It is a note for Jeff, along with the standing 4K request (this shoot was 1080p again).
- **Work on the external drive**, not the boot disk — the finished files run 0.2–1.8 GB each.

---

## Relevant Files & Locations

**Reference (Muhammad's cut, already downloaded and analysed):**
`/Volumes/Extreme/_edit_work/abwheel/ref_muhammad/` — `muhammad_organic.mp4` (6:58), `m.whisper.json` (word timings), `scenes.txt` (his 54 cuts), `shots/` (55 per-shot frames), `sheet_0.jpg`–`sheet_2.jpg` (design contact sheets), `m_st.wav`.
Original: Drive `1RPcsJbq81A6ablUZYVrfIM8vi2i1zrg0`.

**Our working dir:** `/Volumes/Extreme/_edit_work/abwheel/`
`ranges.py` `chips.py` `pip.py` `edl.json` `build_edl.py` `build_gfx.py` `composite.py` `make_srt.py` `qc.py` `tailcheck.py` `sil45.py`, `clips_graded/` (**the segment cache — never delete**), `C163*.whisper.json`, `sil_*.json`.

**Delivery folder:** `/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose/EDITED LONGFORM 8-20-26/abwheel-17-dollar-ab-wheel/`

**Raw rolls:** `C1630` (intro) `C1631` (why + how) `C1632` (progression) `C1633` (live sets + CTA), in the shoot folder above.

**Skills:**
- `.claude/skills/longform-edit/SKILL.md` + `reference/` — Step 5.5 (cutaways), 5.6 (channels), the multi-source builders, `verify_cover.py`, `plan_map.py`, `build_inserts.py`, `chan_analyse.py`, `build_audio_singlemic.py`, `fitvoice_longform.py`, `finish_audio.py`
- `.claude/skills/ad-edit/reference/` — `motionlib.py`, `sfxlib.py`, and `rev5/` (`tight_full.py`, `captions5.py`, `audio5.py`, `pick_bed.py`, `gfx5.py`) — **the closest working precedent for every Phase A step**

**Outline:** Google Doc `1uDAWvxoAjXUaawZctgdSDj_9JPa5mfk5MMM2Sh8L7yE` (video 2).

---

## Exact next action

Start at **Phase A step 0** (repath), then **step 1** (audio) — the audio fix is worth shipping on its own even if the session runs out of room for the rest.

### Starter prompt

> Execute `Handoffs/handoff-20260824-abwheel-muhammad-standard-rebuild.md`. Phase A first (rebuild the ab-wheel longform to Muhammad's standard), then Phase B (rebuild /longform-edit so the style rules are enforced by the QC gate, not just written in prose). Do NOT ask me the Phase C questions until Phase B is finished. The working drive is now `/Volumes/Extreme/`, not the Seagate — repath the scripts first.
