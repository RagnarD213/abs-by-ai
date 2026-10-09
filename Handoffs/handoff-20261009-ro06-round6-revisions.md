# RO-06 "How To Work Out At Home On A Budget": round 6, Dan's four revisions to the full film

**LFC (long-form content, 16:9).** Sidebar name: `Work Out At Home LFC R6`.
Written 2026-10-09 by Claude (Opus 5.5) after Dan reviewed the round 5 full film. This is the only RO-06 handoff: it replaces
`handoff-20261008-ro06-round6-dan-review.md`.
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/longform-edit/SKILL.md`,
`.claude/skills/longform-edit/reference/ro06/README.md` (round 5 section: the tools and every trap),
`/Volumes/Extreme/_edit_work/ro06/round6-plan/decisions.json` (Dan's words, the reviewed hash, my reading),
`/Volumes/Extreme/_edit_work/ro06/round5/round5-record.json` (hashes, checks, costs).

## Scope of this round
Apply four revisions, render the film once, run the checks, show Dan the film again with only what changed. Build in
`/Volumes/Extreme/_edit_work/ro06/round6/`. Never overwrite `round1/` to `round5/`. The recipe lives in `ro06/recipe/`
(copy `render5.py`, `finish5.py`, `finish_chain5.sh`, `page5.py` to round 6 names and point them at `round6/`).

## The four revisions (Dan, 2026-10-09)
1. **3:51, the jump rope clip (C06, 229.61 to 233.37 s).** It is the both-feet clip `B0430`. Dan: "change this to the clip of
   me doing jump rope correctly, the clip where I'm quickly skipping over the rope with correct form." Use the fast skip.
   The opening already uses `B0448` from 4.0 to 6.4 s (roll C1674, 99.0 to 101.4 s), so take a DIFFERENT 3.8 s of the same
   fast stretch of roll C1674 (it runs steady for about 12 s; measure it as round 3 did: head height against the median
   plate). No frame of the film may appear twice. If no clean non-overlapping 3.8 s exists, shorten the slot, never slow it.
   **Standing rule now on record** (`_shared/VIDEO-RULES.md`, top section; memory `jump-rope-clip-rule`): `B0430` is a mistake
   demo only, `B0447` is the beginner demo only, correct jump rope is always the fast boxer skip.
2. **9:24, hair out of frame (shots mb2.0r0 at 9:23.2 to 9:30.7 and mb2.0r1 at 9:30.7 to 9:34.1, roll C1574).** Dan: "crop a
   little wider and higher so that my hair, when I raise my arms a few seconds after that, doesn't go out of frame."
   Facts he does not have: the crop's top row is already the camera's top row once the operator has tilted down (the tilt is
   about 145 source px over the first 4 s, `round5/stab.json`), and at 9:32.3 his hair leaves the CAMERA frame. There is no
   recorded picture above his head after the tilt. What exists: for the first second of the take the camera was aimed about
   145 px higher, so the background above his head (trees, the pavilion roof, sky) was recorded there.
   Build it this way: make a still plate of that upper background from the take's own first frames, stabilised to the settled
   position (`stab.py` gives the offsets), and lay it above the camera frame so the canvas is taller; then crop wider and
   higher with real headroom (aim for 40 px or more above the hair in the 1080 frame, on every frame of both shots). Check the
   three moments his hands go up (9:27 to 9:33): a hand that crosses the camera's old top edge would be cut by an invisible
   line under the plate. Where that happens, either keep the crop top just above the hair and below the hands' cut, or cover
   those frames by starting the toe-touch cutaway C12 (9:34.1) earlier, if `B0467` is long enough (never hold or slow it).
   If the plate cannot be made to hold (moving leaves, parallax), make the upper band with Codex on the subscription
   (`_shared/codex-image.sh`, background only, his real picture untouched) and say so. Show Dan a before and after still and
   the moving shot on the page. Run the dense hair check on the result and report the smallest headroom.
3. **11:23, the mic is blown out (11:22 to 11:26, shot db3.0r7, roll C1576 about 65.3 to 69.6 s).** He turns his head down
   toward the lav for the overhead triceps demo. Measured on the untreated voice: 10 dB hotter than the seconds around it
   (rms -11 dBFS against -21) with peaks pinned at the recorder's ceiling (-0.4 dBFS). Dan: "try to fix that audio so that it
   sounds as normal as possible." Order of attempts: (a) run `pick_lav.py`'s probe on C1576 and see whether the second
   microphone is clean for those 4 s; if it is, patch those words from it, matched in level and tone to the lav on either
   side, with short crossfades inside the words' own pauses; (b) otherwise repair the lav: `adeclip` on the stretch, then ride
   the level down to the neighbours' loudness, then the normal chain. Keep the change inside the stretch: prove the untreated
   voice is sample-identical everywhere else, and that the first minute's md5 proof still holds
   (`fbf7798364cf1f0592144e03827a3b8a` over 0 to 62.9963 s). Never over-strip (memory `audio-never-over-strip`). Put a
   before and after clip of those six seconds on the page. If it still sounds damaged, say so plainly and offer the cutaway
   option (cover does not fix sound) or losing the sentence.
4. **15:49, the phone clip (C29, `B0437`).** Dan: "I don't like that. It's just me looking at my phone. I want to replace this
   with the camera scene with a graphic of the Abs By AI home screen next to me, and then click into it, seeing the calorie
   tracking functionality, seeing some of the AI-generated workout videos, and basically showing off a few of the best
   features at that part in a left-third graphic within a phone frame next to me."
   - **What to build:** Dan on camera, shifted right, with an upright phone on the left third (the approved shell:
     `phone_demo.shell()`), in the approved workout-app format (VIDEO-RULES, "Approved workout-app format": upright phone,
     side presenter, visible tap, natural-speed exercise video). Screens in order: the app's home screen, a visible tap,
     the calorie tracking (meal photo to calories and macros), a visible tap, an AI workout demo video playing in its
     exercise sheet. A few of the best features, no more than fits.
   - **Where:** my reading is the whole sentence the clip sat in, 15:44.0 to 15:53.7 ("On AbsByAI.com, we're not just gonna
     generate an image ... a custom workout plan just for you"), about 9.7 s: home 2 s, calories 3.5 s, workout video 4 s.
     P01 follows at 15:55.5 and stays as built.
   - **The hard part:** this roll (C1581) is shot close. His body spans x 295 to 1507 of 1920, so a phone does not fit
     beside him as shot (round 5 found this for P02). He must move about 350 px right in a FIXED composition with both arms
     intact for the whole span (GRAPHICS-STANDARDS, "Lists and phones alongside Dan"; never animate the presenter). The
     left 645 px then needs background: stretch the wall only if it holds up; otherwise build a clean background plate
     (the camera is locked off in this take; Codex on the subscription for the still plate if needed). Measure the moving
     source over the whole span before choosing, and watch the right edge when he gestures.
   - **Screen sources:** library `B0034` (workout list and exercise sheets; its player is paused, so lay the app's own demo
     file in as `phone_demo.p02_frame` does), `B0035` and `B0038` (meal photo and the itemised calorie result). There is no
     recording of the home screen: capture it from the live app at phone size (built-in browser, mobile preset; test
     account values come from the project's seed files, never Dan's password). Do not reuse P02's goblet squat sheet as the
     workout beat: pick another exercise, ideally a home one (toe touches or push-ups).
   - **Rules that bite here:** no side-by-side before and after screen, no "Meet the new you" screen, no email screen, no
     stick-figure demos, AI-GENERATED on any AI demo video inside the phone, before and after are the same person. The phone
     never covers his face; captions are not burned.
   - It is a new graphic: show a still on its real frame and "play it in place" on the page.

## What Dan liked (keep, do not reopen)
"I like your use of the AI leg press, leg curl, and then the deadlift clip that we generated. That was a good reuse of
existing assets." C19, C20, C21 stay exactly as placed.

## What he did not speak to (stays as built; list each in one line on the page so he can overrule)
Voice tone stays A, the chain he approved (the audio gate's tone row still fails; option B is a 4 dB treble shelf). The bed
stays at `--bed-db -15`. Hair in the closing rolls stays as shot. P01 and P02 stay. Cutaways C16 to C18, C23 to C27 and C30
stay. None of these is recorded as approved.

## Order of work
1. Re-hash the round 5 master (`round5-record.json`) and the locked round 4 first minute.
2. Plan edits (`recipe/plan.py`): C06 source; C29 out, the new phone item in; then `resolve.py`.
3. The audio repair (item 3) and the 9:24 picture (item 2) are their own small builds: prove each on a 10 s excerpt first.
4. Before the render: compare the solve with `round5/RO-06 round 5 - full film.mp4.build.json` (point `_R2` in `build.py` at it:
   every shot keeps its size and crop except the ones this round names), pre-flight every clip against its slot, rerun
   `leanscan.py`, scan the lower-third timing rules from `hf/beats.json`.
5. Render once, `finish_chain` (audio gate, SRT, chapters, plan, watch pass, hair check, HyperFrames checks), the edit sheet.
6. Watch pass: prove which strips are unchanged against `round5/` (PSNR of every frame against the round 5 540p copy) and
   carry their verdicts with `merge_findings.py`; send only the changed strips and the sheets to a fresh `ra-reviewer`.
   Do not delete a `watch/` folder while a judge is working in it.
7. One fresh independent review (`ra-reviewer`) on the final file, then the delivery gate. A check that did not run is a
   failure: say so. Never raise a bound.
8. Deliver: review page on a free port with `review_server.py` (the full film on top, What changed, What I decided, the four
   revisions with before and after, the lines he did not speak to, one reply box); VLC copy
   `Videos to Review/Work Out At Home LFC R6 - full film.mp4`; delete the R5 copy there; delivery folder
   `claude edited long form content/13 - How To Work Out At Home On A Budget/`; edit queue `delivered`. Then stop.

## If the lower-third template fix has landed by then
A separate task fixes the narrow word gap between the parts of a two-part lower third (shared template). If it is merged
when this round starts, `from_plan.py --render` re-renders every lower third: restore the four single-part lower thirds
(G04, G15, G22, G25) to their two-part form from `recipe.round4/plan.py`, and tell Dan the first minute's two lower thirds
changed by a word space. If it has not landed, leave everything as is.

## Open items a reviewer will raise again (all told to Dan on the round 5 page)
Audio gate tone row (5.5 kHz +6.1 in the 20 to 140 s window, with the chain he approved; not the bed). Watch pass: hands out
of the top at 8:59 and 11:23 (the camera's edge), a lower third over his stomach at 1:19 and 13:34, the word gap. Delivery gate
FAIL: 24 rows pass, 10 fail (`round5/logs/gate.log`); cutaway cover reads 34 % against 40 %.

## Budget
$5 per video for AI clips, retries included. **Spent: $2.43.** Nothing here needs a new AI clip. Still images made with Codex
on the subscription cost nothing. Past $5: stop and tell Dan the number and the reason first.

## After Dan finalizes the film (not this round unless he says so)
Queue to `finalized`; `roll_sidecar.py mark-used` for every piece in `edl.json`; register the four AI clips and the stock clips
in the clip library (`--status used-final --used-in "RO-06"`); add the approval to the QC corpus with his words; delete this
video's copies in `Videos to Review/`; stop the page services (`review_server.py PORT --remove` for 8846 to 8850 and the round 6
port); delete the board entry; write the `/video-setup` handoff (thumbnails with Codex on the subscription, AI flag TRUE at
upload, the next free Sunday slot).

## Next action
Re-hash, then the four revisions in the order above. Recommended: **Claude Opus 5.5, high.**

## Starter prompt
> Read `Handoffs/handoff-20261009-ro06-round6-revisions.md` and execute it with /longform-edit. This is RO-06 "How To Work Out
> At Home On A Budget", long-form content (LFC); name this task `Work Out At Home LFC R6`. Apply my four revisions: the fast
> jump rope skip at 3:51, the wider and higher crop at 9:24, the blown-out mic at 11:23, and at 15:49 me on camera with the
> app in a phone frame beside me (home screen, calorie tracking, AI workout videos). Everything I did not mention stays as
> built (change any line before sending): voice tone as I approved it, music bed as is, hair as shot, both app demos as
> built. Use the Codex subscription for any still image. Run every check and one independent review, show me the full film,
> then stop.
