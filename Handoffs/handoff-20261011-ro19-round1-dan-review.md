LFC (long-form content). Task name for the next session: `My First Spray Tan LFC R2`.

# RO-19 "My First Spray Tan": round 1 is with Dan, round 2 starts from his reply

**Written 2026-10-11 by Claude (Opus 5.5).** Job doc: `Handoffs/video-editing/RO-19-my-first-spray-tan.md`. Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`. Recipe and traps: `.claude/skills/longform-edit/reference/ro19/README.md`.

## Where it stands

- Re-edited from scratch from roll C1512 (8/3 kitchen doorway, 30:42 raw). Nothing from the old edit was used except the list of which of Dan's photos are the pale "before" set.
- The cut is locked at 18:41 (38 pieces, 134 shots). No full film has been rendered. Round 1 shows Dan the look, the sound, the first minute, four AI frame pairs and every graphic and clip.
- Review page: http://127.0.0.1:8863/ (managed service, folder `/Volumes/Extreme/_edit_work/ro19/round1/`). First minute for VLC: `Videos to Review/My First Spray Tan LFC R1 - first minute.mp4`.
- Work dir: `/Volumes/Extreme/_edit_work/ro19/`. Hashes of everything shown: `round1/round1-hashes.sha256`.

## What Dan is deciding (4)

1. Colour: D bright and natural (as built) / F one step richer / E more contrast.
2. Voice: 1 the microphone as recorded (as built) / 3 warm / 4 warm with less room echo.
3. AI clip frames A4 (the appointment), A3 (destroy your sheets), A2 (too much tan), A1 (vampires): approve, change or drop each.
4. The close: build the approved app tour beside him on the trainer and nutritionist lines (recommended) / keep the two feature lower thirds shown.
Plus his notes on the first minute and on any graphic or clip by ID.

## Locked before this round (do not reopen)

- Take picks, Dan 2026-09-24: opening take 5 of 5, closing take 4 of 4, the stumble cut ("If you have someone who can help you apply the tan").
- Soft Blue Light graphics, the Motivation lower third, hard cuts, no camera movement, no burned captions, no AbsByAI.com end mark, the approved self-generation demo file (`/Volumes/Extreme/_edit_work/ro06/round5/phone/P01-softblue.mp4`).

## Nothing is approved yet from round 1

Record Dan's reply in `/Volumes/Extreme/_edit_work/ro19/round2-plan/decisions.json` (per item: id, path, sha256 from the hash file, verdict, his exact words, scope, next action, plus `motion_authorized` and `new_frames_before_motion`). Only then act.

## Round 2, in order

1. Re-hash every file in `round1/round1-hashes.sha256` and record expected against actual.
2. Apply his colour and voice picks (`look_option.txt`; `build.VOICE4` holds the voice flags, currently voice 1: rumble filter only, no expander, no dereverb). If he picks voice 4, copy the flags from the RO-07 recipe.
3. Apply his graphic and clip notes in `recipe/plan_parts/` (lead items are in `p90_lead.py`), then `resolve.py`, `dupscan20.py`, `pairs.py` for any changed photo scene, `from_plan.py --render`.
4. AI motion only for the frame pairs he approves: `gen_motion.py` (Veo 3.1 Fast on Replicate, $0.10 a second; write prompts from the page's action lines; A4 one 6 s take, A3, A2, A1 one 8 s take each, about $3.00 in all, cap $5.00 for the video including retries). Judge each take at playback speed, then frame by frame.
5. If he picks the app tour for the close: `recipe/phone_side.py` with library clip B0544 (reference scene B0543), Dan moved right, the phone on the left, on "We have an AI personal trainer" through "get you to your goal".
6. Pin the framing solve before the full render (`build._PIN`), music bed (`bed.py`, level set on the gate's floor row), the full 16:9 render, SRT and chapters, the finish chain (audio gate, transcript check, watch pass), one `ra-reviewer` pass, the edit sheet, the delivery gate. Later-round delivery lists every change with timestamps in the new film.
7. Do not upload or queue. `/video-setup` is a separate task.

## Cuts already applied (do not apply twice)

All in `recipe/edl.py` (each piece has its reason). Restarts removed: "My AI went through all the reviews", "These type of things are more appropriate if you're", "Now, after this" (first), "In my normal life" (first take), two "Sun exposure is one of the most common" attempts, "So sun damage, even though", "In my opinion" (first), "Now, even if you are", the first "who should be spray tanning" run, "So that way the clothes", "then I would invest in a...", "And then finally, before your shoot, just spend five to", the first "from what my tanning specialist told me ... the longevity of it", four earlier closes. Five wordless slivers dropped in `shots.py`. Pauses of 0.70 s or more are tightened to about 0.42 s once, in `shots.py`.

## Gate status, stated honestly

- First minute audio gate: 10 of 12 rows pass. FAIL: dry room (85 ms against 80) and tone match. Both follow from leaving the microphone untreated, which nine blind trials preferred on this roll.
- No delivery gate, watch pass, edit sheet or independent review has run: there is no film yet.
- Hair: the camera frames his hair at the top edge for the whole roll and clips it slightly in the opening take. Both sizes keep the top row. Expect the hair rows of the delivery gate to fail on the full film; that is the camera, and it goes to Dan as a note.
- An outside review of the first minute (Gemini) claimed jump cuts and a repeated phrase; both were checked against the segment list and a re-transcription and are not there. It also called the room echo and bright skin: those are decisions 1 and 2.

## Cost ledger

- AI motion: $0.00 of the $5.00 cap. Estimated for all four clips: $3.00.
- Images: 8 frame images on the Codex subscription (two extra attempts: one failed, one refused for briefs).
- Gemini: 9 blind listening trials and 1 first-minute review, a few cents.

## Open risks

- The plan has two poolside posing clips of Dan (Cd07's second shot and Cd20) that may be the same take: check the source rolls before the full render and swap one if they share frames.
- Three swimming shots and five photographer shots across the film are different sources; if Dan finds them samey, cut to him instead.
- The machine was shared with the RO-20 build; renders here ran one worker at low priority.

## Model and effort for round 2

Opus 5.5, high (editorial judgment on his notes, AI motion review, the full assembly).

## Starter prompt

```
My First Spray Tan LFC R2. Read Handoffs/handoff-20261011-ro19-round1-dan-review.md and continue RO-19 from Dan's round 1 reply below: record his decisions with hashes, apply his colour, voice, graphic and clip notes, generate motion only for the AI frames he approved, then build the full film and take it through the gates and one independent review. Do not upload or queue. His reply:
<paste the reply from the review page here>
```
