# Ad 13 "The Cost Of Getting Abs", round 2: Dan's revisions, a new AI opener, and a new horizontal

Rewritten 2026-10-02 after Dan answered the round 1 page. Recommended: **Claude Opus 5.5, High**.
Sidebar name: `The Cost Of Getting Abs AD R2`. Parent: `handoff-20261001-ad13-other-formats.md` (AV-11 + AS-10).

**Round 2 is another approval round, not the full build.** Dan asked for a new AI clip and six replaced items, so the
round method applies again: show him the opener's START and END frames and every changed item, plus the first minute
of the new horizontal, then stop. The full files come in round 3, after he locks this page.

## What Dan said (verbatim, with scope: `/Volumes/Extreme/_edit_work/kit9x16/av11-ad13/review/decisions.json`)

Approved in the first minute: **audio and colour** ("the audio sounds good and the color correction looks good").
He gave no notes on the graphics he did not name; do not reopen them and do not claim he approved each one.

| # | Item | What he wants | Applies to |
|---|---|---|---|
| 1 | New AI opener | A new AI clip for the first few seconds, like the campaign image where a robot spots a man on the bench press while the fired personal trainer walks past carrying a box of his things. | vertical, square, new 16:9 |
| 2 | Centering | "A little bit less aggressive": less camera motion, more tolerance for him sitting slightly off centre. Not as loose as the old builds where he left the frame. | vertical, square |
| 3 | P03 (0:24, old channel clip) | Replace with the Crazy 3 Minute Home Abs Workout video (toe touches, V sits, triangles) as a phone-orientation screenshot video of the YouTube page. Use the start of that video, before he begins, where he looks most ripped, the camera is on him, he is centred and Mike Chang is off to the side. | vertical, new 16:9 |
| 4 | P06 (0:42, flag photo) | Replace with a vertical studio-shoot photo of him, smiling and ripped, shown full screen like P05. | vertical |
| 5 | P09 to P11 (1:18, three food clips) | One single clip of a chicken, broccoli and rice meal that looks bland and terrible. He believes we already generated one. | vertical |
| 6 | P20 (2:38, workout phone) | Show the AI-generated exercise videos, never the stick figures. | vertical, new 16:9 |
| 7 | P22 (3:26, meal tracker phone) | Replace with the three-meal recipe screen (Honey Soy Chicken, the Mexican dish, Greek Yogurt Berry Bowl): the user taps Honey Soy Chicken, sees it, taps the Mexican dish, sees it. | vertical |
| 8 | New horizontal | Re-edit the existing 16:9: the new AI opener at the start, item 3, item 6, and every graphic redrawn in Soft Blue Light. "Everything else will stay the same." | new 16:9 |

Not answered: question 2 (the Thai shorts photo P05). He used P05 as the model for P06, so it stays.

## Where things are (verified 2026-10-02)

- Build dir `/Volumes/Extreme/_edit_work/kit9x16/av11-ad13/`. Round 1 page `http://127.0.0.1:8813/` (served from
  `review/`; restart: `cd` there, `python3 -m http.server 8813`). Build round 2 in `review2/` on a new port; never
  overwrite the reviewed page.
- Editorial copy and picture swaps live in `sbl_copy.json` (format: `kit9x16/master_to_sbl.py` docstring). Path and
  lessons: `kit9x16/README.md`, section "An editor's master in Soft Blue Light". Memory `kit-master-path-soft-blue`.
- Done: recover, measure, content, restyle, setup, audio (his mix untouched), kit, base, track, graphics (HyperFrames),
  labels, words, captions. Caption spellings are fixed in `ref.whisper.json`; do not regenerate it.
- Master: Muhammad's round 4 HD in the Ad 13 folder (7,339 frames, 4:04.878). Raw roll: 8/14 shoot `C1602.MP4`.
- Queue: AV-11 `draft_review`, AS-10 `in_progress`. Spend so far: under one cent.

## Assets already found

- **Opener reference image:** `output/campaign-images-mockups-20261001/ai_fire_your_trainer.jpg` and the approved K3
  set `output/campaign-images-20261001/K3-b.png` (Dan's pick), text-free scene in `plates/`. Prompt wording: K3/K4
  scene in `Handoffs/handoff-20261001-campaign-images-build.md`.
- **3 minute abs video:** the sales letter's screenshot is `public/img/letter/sixpackabs-3min-abs.jpg` ("YouTube page
  of the SixPackAbs.com Crazy 3 Min Home Abs Workout video"). Find the full finished video the way WV-01 sourced M100
  (`/Volumes/Extreme/_edit_work/wv01-edit/round7/assets/`); if it is not on disk, download it with `yt-dlp`.
- **Bland meal:** search first: `clip_library.py find "chicken broccoli rice"` (B0042 is a barbecue bowl, too
  appetizing; check the AI food clips by eye). If nothing reads as bland, it becomes a second new AI clip.
- **AI exercise demos:** `public/exercise-demos/*.mp4` and the library's `exercise-demos/` (A0134 toe touches). The
  approved workout-app format is WV-01 round 8 (`VIDEO-RULES.md`, "Approved workout-app format"):
  `/Volumes/Extreme/_edit_work/wv01-edit/round8/graphics/early-app-flow.mp4`.
- **Three-meal recipe demo:** WV-01's P07 recipes (`/Volumes/Extreme/_edit_work/wv01-edit/round4/previews/P07-recipes.mp4`,
  later rounds in `round12/` and `round13/recipe/`). Reuse the approved phone shell and screens; the taps Dan wants are
  Honey Soy Chicken, then the Tex Mex dish.
- **Studio photo for P06:** `photos/finalized social media photos/` (studio-blue / white / gray `_FINAL_PRIMARY.jpg`),
  never from `Frowning Photos/`. Pick on the rendered 9:16 crop with the label placed by `kit_labels.py`.

## Work, in order

1. Read: `.claude/skills/_shared/VIDEO-RULES.md`, `PRE-RENDER-APPROVAL.md`, `IMAGE-GENERATION.md`,
   `kit9x16/README.md`, memories `ai-clip-artifact-giveaways`, `never-show-stick-figures`, `untagged-video-bt601-trap`.
2. **Opener frames first (do this before anything slow).** Use the Codex subscription to generate the images
   (`.claude/skills/_shared/codex-image.sh`): a START and an END frame at 9:16 and at 16:9, same scene as K3-b, no text.
   Action: the robot spots the man through a bench press rep while the fired trainer walks across the background with
   his box. A few seconds long. Put the frame pairs, the action, the length and the cost on the round 2 page. Do NOT
   generate motion until Dan approves the frames (standing rule). Motion budget: $5 per video including retries.
   The opener replaces picture only: Muhammad's audio stays untouched, so decide which opening words it covers and
   keep the hook lower third readable.
3. **Centering.** The kit round 2a added an off-centre tolerance to `kit_track.py` ("calmer camera"). Use it and tune
   toward less motion; measure before and after on the delivered first minute (pan speed and how far he sits off
   centre) and show both numbers on the page. The framing gate rows must still pass; never move a bound.
4. **Swaps in `sbl_copy.json`** (`pictures` + `media`), then rerun `kit_run.py --master ... --sbl ... --from restyle
   --until words`, `kit_deliver.py captions`, and `sbl_page.py --media` into `review2/`. Items 3 to 7 above. Check every
   AI clip frame by frame. A phone demo is the whole phone in a card; a labelled picture of Dan gets its measured chip.
5. **New horizontal, first minute only this round.** Start from Muhammad's round 4 master and his audio (untouched).
   His graphics are burned into his picture, so the Soft Blue Light version has to be rebuilt from the raw roll with
   the recovered edit and grade, the same way the vertical was, at 1920x1080 with the approved 16:9 templates
   (`_shared/hyperframes/`: lower third, side list beside Dan, before card; price cards need a 16:9 title card).
   Reuse the vertical's copy file wording. Prove the grade against his master side by side before showing it.
   This is a new build path: say plainly on the page what is proven and what is not.
6. **Round 2 page** (standard layout): the new first minute at 9:16 and at 16:9, the opener frames, "What I decided",
   then only the changed items, each with "Play it moving, in context". Keep Dan's decisions to a handful.
7. Record everything in `review2/decisions.json` when he answers, write the round 3 handoff (full vertical + 59 s,
   square look page and square files, full horizontal, gates, three fresh judges, independent `ra-reviewer`), and stop.

## Traps

- Nothing is uploaded. This is an ad (ends "Tap the button below"): Unlisted via `/ad-setup` only, after approval.
- The horizontal Dan is replacing is live in Google Ads (YouTube `-SuKGXGcbIg` / `hrQf1240kQA`). Never delete or
  replace the live video in this task; the new file is a new deliverable for `/ad-setup`.
- 52 % of the words sit under graphics that pause captions. If the gate's caption rows object in round 3, shorten
  graphic times in the copy file, never the bound.
- Not yet proven on a Soft Blue Light master build: `kit_plan.py`, the gate pre-check, `kit_cutdown.py`, and 1:1
  template layouts (`vertical.py` is 9:16 only).
- At most two builds at once on this machine. Run `gate.py` detached. No em dashes in anything written.
- The shared board is over its word limit from other sessions' entries; edit only the Ad 13 line.

## Starter prompt

> Read `Handoffs/handoff-20261001-ad13-round2-full-build-after-lock.md` and the files it lists. Name this session
> "The Cost Of Getting Abs AD R2". This is round 2 of Ad 13: apply my round 1 revisions (they are in the handoff and
> in decisions.json), make the START and END frames for the new robot-spotter opener and stop for my approval before
> generating motion (use the Codex subscription to generate the images), make the six item swaps, calm the centering,
> and build the first minute of the new Soft Blue Light horizontal. Show me one round 2 page with only what changed.
> Do not build the full videos yet and do not upload anything.

Model and effort: Claude Opus 5.5, High.
