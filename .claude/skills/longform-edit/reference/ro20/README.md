# RO-20 "Why You Should Invest More In Your Health" (8/3 kitchen doorway roll C1511, 68:51 raw, 53:04 cut): round 1 recipe (Claude Opus 5.5, 2026-10-10/11)

One roll, filmed off an outline, re-edited from scratch (the old edit was scrapped). Starts from `../ro07/` (copy RO-07's
WORKING recipe folder on the SSD, `/Volumes/Extreme/_edit_work/ro07/recipe/`, then this folder: the repo copies of ro06 to
ro16 carry each job's own `W =` path and half of them are not the last working version). Work dir and media:
`/Volumes/Extreme/_edit_work/ro20/`. Review page: port 8862.

Order: `pick_lav.py --ss 600 --t 60` -> lav wav -> `asr_rolls.py` (medium.en, 37 min for 69 min under load) -> take map
(`takesel/`, `edl.py`, `mkglobal.py`, `shots.py`, `words_src_out.py`) -> `premask.py` -> `framing.py` -> `grade20.py masks|stats`
-> `lookstills20.py` -> `audio_options20.py` -> `listen_trials.py` -> `plan_parts/` (+ `resolve_part.py`) -> `resolve.py` ->
`build.py segs` -> `chain.sh` (lower thirds part by part, `stills20.py`, `page20.py`, context clips).

## What is new here

- **A long film is planned in parts, in parallel.** `plan.py` loads `plan_parts/pNN_*.py` (each defines `PART`), in film order.
  One plan writer per 8 to 10 minutes of film, each a separate agent given `PLAN_BRIEF.md`, its transcript stretch and an ID
  letter (`Gb01`, `Cb01`). `resolve_part.py` checks ONE part alone (phrases, clip lengths against their slots, overlaps, cover,
  gaps, capitals) so writers never touch the film's `plan_resolved.json`; `RO20_PARTS=p00` limits the loader while later parts
  are still being written. `dupscan20.py` then finds any source two parts both took (four here, all fixed by the last writer).
  364 items for 53 minutes took six writers about 20 minutes each.
- **The take map was delegated the same way** (one agent, `takesel/`): it found two hidden false starts the scrapped edit had
  kept, and patched 25 mistimed first words (`word_patches.json`, applied by `mkglobal.py`).
- **Pexels without a key, for many beats at once.** In the Browser pane on pexels.com, one `javascript_tool` call can
  `fetch('/search/videos/<term>/?orientation=landscape')` for dozens of terms and collect `<id> <slug>` pairs (split the list:
  one call times out at 45 s, the page keeps going). Getting 50 KB out without reading it into the conversation: put it in
  `window.name`, navigate the tab to a one-file local receiver (`px_recv.py` pattern: GET serves a page, POST writes the body),
  and POST `window.name` same-origin. The pexels.com page's own CSP blocks a direct POST to localhost. Downloads are plain
  `curl https://www.pexels.com/download/video/<id>/`.
- **Lower thirds render in parallel with `from_plan.py --only id,id`** into one `--out`; a last run without `--render` merges
  the manifest. Two workers is the cap (three plus another session's render put the load average at 120). About one minute
  per lower third per worker.
- **`stills20.py`**: a lower third that sits over a cutaway is drawn over THAT cutaway (the old still showed the presenter the
  clip hides), a cutaway of two or three shots shows them side by side, and rows merge into `stills.json` so the page fills
  in part by part. `qcsheets.py` makes 5 x 4 labelled sheets for the editor's own look before Dan sees anything.
- **`page20.py` reads its words from `round1/page_copy.json`**, so decisions and notes change without touching the generator.

## Traps this build paid for

- **This roll's blacks sit at 0.084 and the black tank top at 0.10.** `grade.py`'s fixed shadow control at x = 0.10 landed 0.016
  from the black point and the spline rang: posterised skin, green and purple fringes. `grade20.curve20` puts the shadow
  control halfway between the black point and the skin median. Look at the first stills before measuring anything.
- **A steep per-channel curve alone pushed skin to hue 31 and saturation 0.58** (yellow-orange arms). Saturation 0.92 and
  `hue=h=-6` bring it back to the camera's own hue 25 and RO-07 look D's saturation. Positive `hue=h` turns skin yellower.
- **One Gemini blind listen decides nothing on close voice options.** The same clip scored 2 and 9 in two runs. `listen_trials.py`
  repeats the ranking with fresh letters and send order and averages: seven trials said only that the chain default never
  wins and the fixed warm EQ does. The room measurement (87 ms raw, 52 ms with the light pass) and Dan's own RO-07 pick
  settled the rest. Say that on the page; do not present one ranking as a verdict.
- **Gemini answers "no audio was attached" and then quotes the audio.** It still caught a real stumble ("pri- priority").
- **The camera cut the top of his hair for most of the roll** (the person mask reaches row 0 in 73 % of sampled frames, median
  68 px of hair crossing the edge). Both sizes keep the camera's top row; reported to Dan as unfixable in the edit.
- **Six plan writers downloading and sheeting stock at once is itself a load.** Start the first-minute render before them.
- **A context clip costs 75 to 90 s for 13 s of picture.** For 190 lower thirds that is hours: run it last, two workers, lower
  thirds only (a cutaway under a lower third is seen in that clip), and let the page fill in.
- **Veo 3.1 Fast takes are 4, 6 or 8 s.** A 6.4 s slot needs the 8 s take; trimming two gag slots to under 6 s (start on the
  second sentence) kept five clips at $4.05 with room for one retry.
- **`resolve.py` snaps clip edges to shot joins AFTER `resolve_part.py` checked the part**, so a slot can grow past its source:
  three clips came up 0.06 to 0.4 s short and each killed a batch of context clips. Run `preflight20.py` after every
  `resolve.py`; it prints the largest start offset that fits.
- **`stills.py` showed only the first source of a multi-source clip and drew lower thirds over the presenter even when a clip
  covered him.** Use `stills20.py`.
- **A dying session loses the last tool call.** The chain script had not been written when the session dropped; nothing was
  running overnight. Write the unattended chain to disk and start it before the long wait, then check `chain.log`.

## Round 1 state and Dan's verdict (2026-10-11)

Sent to Dan: look D, voice 4, opener O1 (O2 alternative), AI frames A1 to A4, the first minute (70 s), 190 lower thirds and 177
cutaways as stills with a context clip per lower third, nine decisions. No motion generated, no full render.

His reply (word for word in `round1-decisions.json`): look D and voice 4 locked; both AI gag openers rejected ("Just use a
camera scene for the intro"); the excuse-voice clips A1 to A3 approved, the lawyer clip cut; two cutaways of someone looking
at a phone thrown out (one is now a standing never-use, B0437); three of his own pool clips called "excessively dark", which
became the standing rule that all B-roll is colour corrected; and the 53 minute film split into THREE videos tied together
with audio pickups he records. What that taught: check every one of his own B-roll stills beside a presenter still before
the page goes out, and for a film this long raise the split question with the take map, not after 367 stills.
Next: `Handoffs/handoff-20261011-ro20-round2-after-dan-review.md`.

## Round 2 (2026-10-11): three videos from one roll, audio pickups, his round 1 revisions

Dan split the 53 minute cut into three videos (RO-20, RO-20B, RO-20C) joined by audio pickups he records. Scripts added beside this
file: `cards20.py` (full-screen cards as pre-rendered plan clips), `brollgrade20.py`, `context2.py`, `page2_20.py`, `gen_motion20.py`,
`lipsync20.py`. Handoff for the next round: `Handoffs/handoff-20261011-ro20-round3-pickups-and-first-minutes.md`.

- **Split a film without touching its cut:** keep ONE timeline and ONE framing solve, and make each video a set of ranges of it
  (`build.py range a b`) plus its pickup segments. Before changing the plan, dump the solve Dan reviewed (`all_segments()` on the
  locked `plan_resolved.json`) to `round2-plan/segs.round1.json` and point `_PIN` at it: after removing the opener and three other
  items, 499 of 499 shots kept their size and crop.
- **Grep the transcript for promises that cross the new boundaries** ("in a minute", "later", "like I said"). Two sentences in video 1
  pointed at material that is now another video; both sit at the end of a piece and come out with no new join.
- **Pickup scripts:** content plan per pickup, then `dan-voice-writer` with the real sentences either side as his-words, two drafts
  each (formats `script` and `video`), pick by which carries the plan, do not polish. State the lead-in constraint in the plan
  ("the last sentence must lead into ..."): three first drafts ended on the wrong beat and were redrafted by seed.
- **An audio pickup has no camera picture, so plan its pictures with the script.** One reusable three-part card with a picture
  window (rows light up as he names each part) carries all four pickups; clips from the OTHER videos are fair game in the window
  because the no-repeat rule is per video. Check whether he already said the hook on camera somewhere in the roll: here the exact
  line sits in the summary, so video 2 can open on camera and the pickup only bridges.
- **`curves` works in RGB. Fed YUV it converts with the BT.601 default** and tints the picture (pink concrete, green skin on the first
  B-roll stills). Decode to RGB with `in_color_matrix=bt709` first (`format=gbrp`), then grade, in the measurement AND in the build.
- **Grading his outdoor B-roll from the skin MEDIAN alone flattens it:** in hard sun the median is his shaded side, so the gain is far
  too high and the lit skin loses its shape. `brollgrade20.py` takes the geometric mean of the median and 90th-percentile gains
  against the presenter, never darkens, caps at 2x and leaves highlights where they are. The hue-based skin meter also reads sunlit
  concrete and grass as skin (clips "measuring" 0.70): those are skips, decided by eye. Three passes before the stills were right.
- **A lower third removed from the plan is still in `hf/manifest.json`** and keeps drawing (two retired lower thirds came up over the
  new full-screen cards in the first context clip). After any plan edit, diff the manifest ids and times against `plan_resolved.json`.
- **A phone-screen mock that is already drawn inside a flat phone** (library A0089): crop its screen under its own status bar, put
  the page at the top of a canvas with the shell's aspect, its page colour under it and its tab bar at the very bottom, then use the
  approved shell. Trim each static screen to its words, never past the screen's own source length.
- **`zsh` does not split `set -- $v`**, so a download loop over "id slug" pairs silently made no files. Name the files outright.
