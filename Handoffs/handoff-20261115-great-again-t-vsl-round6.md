SUPERSEDED 2026-11-15: round 6 was run the same evening in the round 5 chat. Use `handoff-20261115-great-again-t-vsl-round7.md`.

AD (Great Again T sales video). Task name: `Great Again T VSL AD R6`.

# Great Again T VSL (WV-03): round 6 handoff

Written 2026-11-15 by the round 5 editor (Claude Fable 5.2 coordinating Opus and Sonnet workers). **Model: Claude Opus 5.5,
high effort** (a video stays on the AI it started on). Do not fire before the usage limits below allow it, and not before
Dan has replied on the round 5 page.

One native 9:16 sales video (1080x1920, 29.97), Dan on green screen, roll C1903. The job lives on the M6's internal
drive: `~/_edit_work/wv-03/`. On resume: `python3 .claude/skills/_shared/editroute/resume.py check WV-03`, then
`editcap.py acquire WV-03 --title "Great Again T VSL" --type AD`.

## 1. Where round 5 ended

Review page: http://127.0.0.1:9764/ (generator `round5/review/build_page.py`; inputs `round5/review/inputs/films.json` and
`pairs.json`; real build `python3 build_page.py`). Tested in the side pane at 800 and 1150 px with the real data.

**Part A, delivered:** the first 2:52.67 of the film (to the end of L038), one cut in two backgrounds:
`round5/DRAFT - Great Again T VSL R5 - First 3 Minutes - Wood Kitchen.mp4` (sha256 b58187c3...3874f) and
`... - Teal Studio.mp4` (874f82c4...aa1d4). Everything about the build is in `round5/film/REPORT.json`,
`round5/film/BUILD_LOG.md` and the recipe `round5/film/recipe/` (chain: `chain_film.sh`). Key pieces H5 (round 2), S1
(RIM=3 redo) and P1 to P6 under `round5/key/`, each with a keyonce stamp: never re-key them.

**Part B, partly delivered:** 26 of the 44 AI clip ideas have at least one START/END pair that passed the frame gate and a
fresh reviewer (8 ideas have two pairs, 18 have one): 34 pairs on the page. 18 ideas have none yet and are listed on the page
as still to come: AI-01, 03, 05, 07, 10, 19, 22, 23, 24, 25, 26, 30, 34, 35, 38, 40, 41, 42.

## 2. Usage limits that stopped round 5 (check before starting)

- **ChatGPT / Codex subscription: out of usage until 2026-11-18 11:57 AM.** About 150 Codex image generations in one day
  did it (memory `codex-image-batches-exhaust-subscription`). Until then frames are Google only.
- **Claude weekly limit (Opus and Sonnet): reset 2026-11-19 10:00 AM Central.** Every background worker died on it at about
  2 PM on 11-15, including the film editor (after its final render and checks), the gating agents and the second-attempt
  agents. Fable still ran.
- Google AI (Flow, Nano Banana Pro): about 180 images at 0 credits each. The balance read 20,312 in the morning and 19,822
  at 1:55 PM; another task used Flow that day. Confirm before blaming this job.

## 3. What round 6 does (in this order; Dan's reply on the page decides the details)

1. **Record Dan's reply** in `round6-plan/decisions.json` in his words (film notes by time, anything to carry from the teal
   version, the pairs he selected as `AI-xx X1` lines). Log his pair picks with `blind-image/blind.py pick` on each
   `round5/frames/<ID>/blindset` that has one (two-model ideas only; never reveal sources; single-pair ideas are keyed in
   `.manual-key.json` and are not comparison offers).
2. **Second attempt for the 18 ideas with no pair** (he asked for pictures for all 44). The plan is written and not started:
   `round5/frames/BRIEF_WAVE2.md` (a designer rewrites each idea so the END is one small, visibly caused change; a Google
   runner draws them into `<ID>/wave2/`; same gate and fresh `frame-reviewer` per pair; one END remake, then dropped).
   Replace `round5/frames/wave2_ids.txt` with the 18 ids above first. `assemble_pairs.py` already picks up verified
   `wave2/` pairs; rebuild the page and tell Dan which ideas are new. An idea that still fails is listed as dropped with
   the reason in plain words.
3. **Motion only for the pairs Dan selected** (expect about five clips for the film; he selects more than he will use):
   Flow through the `flow-veo` agent, one continuous take per clip, `clipcheck.py` and a fresh frame reviewer on the frames
   the edit uses, the three sense questions. Paid fallback cap: $5 for this video, $0 spent so far.
4. **Film revisions from his notes** on the first 2:53 (re-render with `chain_film.sh`; unchanged pieces reuse their plates).
5. **Still required before any full render (round 2 decision, binding):** a full graphics review of everything after 2:53:
   every card as a still on its real frame, then moving. Not started.

## 4. Open items from round 5, stated plainly

- Captions after the first 30 s: "I bet you've felt it too" and "as I got older" are uncertain (a second transcription heard
  "you felt" and "get"). Listen and fix if wrong; two words.
- Audio gate on both draft files FAILS three rows: tone (the fixed bass lift, known mismatch), floor between words (-3.5
  against -3.0) and do-no-harm (not measured: no untreated-audio stamp for a draft). Loudness -14.2 LUFS, peak -1.3 dBTP
  pass. Nothing was tuned. Nobody has listened through speakers.
- Arm separation on the kitchen: median 32.7, minimum 27.8; 32 half-second samples under 30, mostly in the hook and first
  minute (the look Dan approved in round 4 measured the same way).
- Caption to graphic clearance: closest 11 px (no touch). The ad-edit lesson asks for 20 px over lower thirds: raise the
  lift if Dan sees crowding.
- The lower third "Age-Related Testosterone Decline" sits across his chest in the FAR shot at 1:58 (on the page under "What
  I decided").
- The independent film review (`round5/film/ROUND-5-REVIEW.md`) was started on Fable after the Opus reviewers died; read it
  first and fix anything it marks "must fix" that round 5 did not get to.
- Git: the main folder could not push (other sessions' live edits). Round 5's commits are local.

## 5. Traps learned in round 5

- A frame gate FAIL that is only static drift (unchanged areas redrawn a few pixels over, a room that brightens) is repaired
  with `framecheck/lockstill.py` and re-gated before it counts as a failed END (`round5/frames/NOTE_LOCKSTILL.md`). Half the
  early drops were this.
- Image models fail the same things every time: sit-down or stand-up (shins grow 12 to 33%), walking toward the camera
  (he never gets closer), an object pushed by another object, tools whose mechanics must be right (hole punch, pressure
  gauge), anything counted (a fourth tub vanishes, a 14-egg carton), printed banknotes, product labels in a shopping cart.
  Design the pair around one small caused change instead.
- Reviewers must never see a source name: give each pair a neutral link folder (`round5/frames/_rev/`).
- With one heavy render-queue slot held on a 6-core budget, frame gates run one a minute and can stall for 40 minutes. Use
  `/away` hours or run the gates before the key.
- A page generator that checks for source file names will trip on its own neutral media names if the input pictures are
  named the same way (`assemble_pairs.py` now writes `in_<ID>_<label>_s.jpg`).
- The film check must decode by frame number; an `-ss` seek showed joins one frame early that were right in the file.

## Starter prompt (Claude: Opus 5.5, high effort)

> AD (Great Again T sales video). Name this chat "Great Again T VSL AD R6". Read `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` and `Handoffs/handoff-20261115-great-again-t-vsl-round6.md`, then run round 6 of the Great Again T VSL (WV-03) as that handoff lists: record my round 5 reply (below), make the second-attempt pictures for the AI clip ideas that have none, generate motion only for the pairs I selected, apply my notes to the first 3 minutes, and send me the round 6 review page tested in the side pane. Use /ad-edit. My round 5 reply: [paste the reply text from the round 5 page]
