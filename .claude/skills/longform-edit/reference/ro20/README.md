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
- **`stills.py` showed only the first source of a multi-source clip and drew lower thirds over the presenter even when a clip
  covered him.** Use `stills20.py`.
- **A dying session loses the last tool call.** The chain script had not been written when the session dropped; nothing was
  running overnight. Write the unattended chain to disk and start it before the long wait, then check `chain.log`.

## Round 1 state (2026-10-11)

Sent to Dan: look D, voice 4, opener O1 (O2 alternative), AI frames A1 to A4, the first minute (70 s), 190 lower thirds and 177
cutaways as stills, nine decisions. No motion generated, no full render. Next: `Handoffs/handoff-20261011-ro20-round2-after-dan-review.md`.
