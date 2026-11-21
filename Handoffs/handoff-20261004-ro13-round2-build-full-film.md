# Handoff: RO-13 round 2, build the full film (2026-10-04)

**CONTENT, long-form (LFC).** "Can You Drink Alcohol And Still Have Abs?", 9/23 roll C1707. Session name:
`Alcohol And Abs LFC R2`. Shorts are the only thing ever derived from this film, in their own task, after it is final.

**Goal.** Dan approved round 1. Generate the two AI clips, record the app capture, build the full film from the locked
parts, gate it, run one independent review, deliver the review copy to Dan.

**Dan's reply (2026-10-04), verbatim:** "Okay, everything looks good on the review page. Create a handoff document for
Claude to finish this edit in a new task."
He named no option on the three choice questions, so the recommended option stands on each. Recorded with hashes in
`/Volumes/Extreme/_edit_work/ro13/round2-plan/decisions.json` (all nine locked files re-hashed 10-04: no drift).

| # | decision | result |
|---|---|---|
| 1 | first minute (0:00 to 1:10.8) | approved |
| 2 | AI clips | both: A the opener, B the mirror (recommended, not named) |
| 3 | deficit line | "an entire day's deficit", as built (recommended, not named) |
| 4 | "take a photo of your drink" beat | real app capture in the phone layout (recommended, not named) |
| 5 | the 25 HyperFrames graphics | approved |

If Dan's starter prompt says otherwise on 2, 3 or 4, his words win. Do not re-ask any of the five.

**Read first.** `_shared/VIDEO-RULES.md` (it changed since round 1), `_shared/PRE-RENDER-APPROVAL.md`,
`_shared/hyperframes/README.md`, `.claude/skills/longform-edit/reference/ro13/README.md`, then `../ro11/README.md`,
`../ro10/README.md`, and RO-10's round 2 for the full-film pattern (`../ro10/finish.py`,
`Handoffs/handoff-20261001-ro10-round2-build-full-film.md`).

**Locked, do not reopen.** Cut (`edl.json`, 21 pieces, 37 shots, 7:10), `plan_resolved.json`, `hf/manifest.json` and its
25 renders, the first minute, colour C, W2/T2 framing (W4S under side cards), audio B chain with the EQ fitted on this
roll (`FIT.mp4.voice_chain.json`) plus 0.9 dB at 150 Hz, the RULE n OF 6 titles, recap G26, three-photo slate P01, the
17 stock placements. Work dir: `/Volumes/Extreme/_edit_work/ro13/`. Build in `round2/`; never overwrite `round1/`.
Round 1 page (record only): http://127.0.0.1:8803/ (LaunchAgent `com.absbyai.ro13-round1-review`).

**What this round builds.**
1. **AI motion, A01 and A02.** Authorized from the approved frames only: `aiframes/A-start.png` to `A-end.png` (he
   raises the beer, then sips; 3.1 s) and `aiframes/B-start.png` to `B-end.png` (shirt held up at the mirror, he lets it
   drop, both hands on the sink, head down; 7.6 s). Veo first/last frame. Both are big body actions (RO-12 trap 11).
   Check every frame: hands, the bottle, the mirror reflection matching the man, no fog on the mirror, no morphing
   bottles. Swap A01/A02 from kind `ai` to kind `clip` with `label="AI-GENERATED"`. A clip never holds or stretches to
   fill its slot: if a take is short, regenerate or trim the slot to a cut. Any NEW still image goes through
   `.claude/skills/_shared/codex-image.sh`, never a paid image API (rule of 10-01); the four approved frames stay as they are.
2. **App capture for C08's slot** (2:58.9 to 3:04.0, "This is the part where the app does the work for you. Take a photo
   of your drink and you're done."). One real session of the AbsByAI macro tracker logging a photo of a drink on the
   live app (memory `local-funnel-test-recipe`; no physique is shown, so the same-person rule is not in play). Place it
   as kind `phone` (`gfx.iphone`, the approved RO-05 shell) beside Dan. Put shot boundaries on the card's first and last
   frame and re-run the framing solver (`build.jumps()` must stay empty). No stick figures, no "Meet the new you", no
   email screen. If a real capture cannot be made cleanly, keep stock clip C08 and say so; do not fake a screen.
3. **Full film.** `resolve.py`, `from_plan.py --render` (only changed scenes re-render), then
   `build.render_range(0, <end>, <out>)`. SRT from the delivered audio's own transcript and chapters (`finish.py`
   pattern), label chips, gate plan.
4. **Checks on the exact file.** `_shared/deliver/gate.py --format longform`, audio gate with the A/B clip, hair check
   over the whole film, `checks.py` on the film, junk and jump-cut pass on every join (`CUT-CONTINUITY-QC.md`), scan
   every clip's first and last used frames for fades and internal cuts, read the SRT cue at every join, a watch pass.
   Then one `ra-reviewer`. Fix what it finds and re-check; expect "does not ship" the first time.
5. **Deliver.** `claude edited long form content/NN - Can You Drink Alcohol And Still Have Abs/` (next free number):
   master, SRT, chapters, stamps, `REVIEW 540p`, audio A/B, `notes-RO13.md`, `recipe-ro13/`. Queue `delivered`
   (`queue.py set RO-13 delivered`, mirror to the artifact db, `mark-synced`). Register the two AI clips and the used
   stock in the clip library; `roll_sidecar.py build` then `mark-used` for the EDL ranges.

**Known and accepted.** "far more moderately than I do in the past" (5:55) stays; both takes say "do" and Dan saw it
listed. Zepbound is spoken and subtitled, never in a graphic. No Oura screenshot exists; the stock clip covers that line.
The delivery gate's `captions:burned` / `captions:card_collision` rows read Soft Blue lower thirds as captions (RO-12
trap 10): report, never tune.

**Spend.** About $1.70 of the $5 for this video so far. Two Veo clips at about $0.60 to $1.20 each fit; stop and tell
Dan before passing $5 in total.

**Git.** Round 1's commit `3180cf7` (recipe in `reference/ro13/`, round 1 handoff) was rejected on push on 10-01 and may still be local only; check with `scripts/git/drift-check.sh`. Push with
`scripts/git/safe-push.sh -m "..." -- <your files>` only; if it stops, report the files it lists.

**Not part of this task.** Thumbnails, upload and setup. After Dan finalizes the film, write ONE Claude handoff for
thumbnails plus setup, and its starter prompt must say "Use the Codex subscription to generate the images."

**Starter prompt (Claude Opus 5.5, effort high):**

Name this session "Alcohol And Abs LFC R2". CONTENT, long-form. Read
`Handoffs/handoff-20261004-ro13-round2-build-full-film.md` and execute it: generate the two approved AI clips, record
the app capture, build the full RO-13 film, gate it, run the independent review, deliver it and send me the review copy.
