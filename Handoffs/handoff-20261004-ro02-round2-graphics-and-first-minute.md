# Handoff: RO-02 round 2. Apply Dan's round 1 answers, then every graphic and clip as a still, the opener frames, the finished first minute (2026-10-04)

**CONTENT, long-form (LFC).** It gets Shorts cut from it later and nothing else: no vertical, no square, no 1-minute version.

**Goal.** Finish RO-02 "The Vacuum: The Best Ab Exercise For Belly Fat" (8/14 poolside rolls C1614 to C1629; job doc
`Handoffs/video-editing/RO-02-the-vacuum-explainer.md`). Round 1 (cut + look) is answered. Round 2 applies the answers
and puts one page in front of Dan: the opener's AI frames and graphic, every other graphic and clip as a still on its
real frame, and the finished first minute. No AI motion and no full film this round. Session name: `The Vacuum LFC R2`.
This replaces `handoff-20261003-ro02-round1-dan-review.md` (keep it for the state it records).

**Read first.** `_shared/VIDEO-RULES.md`, `_shared/PRE-RENDER-APPROVAL.md`, `_shared/GRAPHICS-STANDARDS.md`,
`_shared/hyperframes/README.md`, `_shared/IMAGE-GENERATION.md`, `.claude/skills/longform-edit/reference/ro02/README.md`,
then `../ro13/README.md`, `../ro11/README.md`, `../ro10/README.md`. Work dir: `/Volumes/Extreme/_edit_work/ro02/`
(the recipe that ran is in `recipe/`; the skill copy is `reference/ro02/`).

## Dan's round 1 answers (2026-10-04; his exact words are in `round2-plan/decisions.json`)

1. **Colour: A, approved.** "Okay, let's use color A throughout the video." Locked. Do not show colour again.
2. **Framing: approved with one change.** "Eliminate about half of that unnecessary space above my head. The framing on
   the bottom looks good for both, but cut down on that space above my head by about 50% in both the near and far."
   In `frames.py`: `PAD` F 50 to 25 and N 40 to 20 (source px above the shot's highest hair). **Keep each shot's bottom
   edge where it is now**, so the window gets shorter and the scale rises: F 744 to about 720 rows (x1.50), N 600 to
   about 580 (x1.86). Compute the new top from the new pad, hold the old bottom, derive the 16:9 width, re-centre on
   his head. The size ratio stays about 1.24, so every join is still a clear size change. Re-run the dense hair check on
   everything rendered: round 1 measured 70 px minimum and 106 median in the first minute, so expect about 35 and 55.
   Hair must still clear the top on every sample (VIDEO-RULES "Hair never leaves the frame"); if a shot drops under
   about 20 px, give that shot more pad and say so.
3. **Sound: not answered.** Do not treat silence as approval. Build with the same chain (`FIT.json` EQ via `--eq`) and
   carry the question to the round 2 page.
4. **The opening: a motion graphic holding two small AI clips** (spec below). This replaces all three round 1 options.
5. **Length: not answered.** Keep the cut as it is (11:50, nothing removed) and carry the question to the round 2 page
   with the same three options (the aside is C1617 18.24 to 24.94; the three types trim ends that piece at C1620 19.32).

## The opener (Dan's spec, his words in decisions.json)

A full-screen Soft Blue Light motion graphic under his own voice, from 0:00.
- **Title, top left:** "Stop doing ab exercises if you have belly fat" (set it in the family's title case).
- **Two small AI clips inside it:** on the left an overweight man doing crunches; beside him an overweight man doing
  sit-ups. Two different men. Each does a rep or two.
- **On his words:** "If you have belly fat, stop doing ab exercises." (0:00 to about 0:03.4) both clips play.
  "Stop doing crunches," (0:03.90) a red X crosses out the crunches clip. "stop doing sit ups," (0:05.30) a red X
  crosses out the sit-ups clip. Anchor both X's on the heard words through `resolve.py`, never on whole seconds.
- **Where it ends is your call:** on "sit ups," (about 0:06.4) or after "stop doing all those ab exercises" (about
  0:08.3), then a hard cut to Dan on camera. Pick one, say why in "What I decided".
- **AI clip rules that bind it.** Search the clip library first (`clip_library.py find`), though round 1 found no
  crunches or sit-ups clip. START and END frames are made by Codex on the subscription
  (`.claude/skills/_shared/codex-image.sh`), never a paid image API. Frame each man to fit his panel, subject centred,
  one simple body action between START and END (crunch up, sit up) so the motion model only moves the torso. Each clip
  carries the AI-GENERATED chip for its whole time, clear of the title and the X. **No motion is generated until Dan
  approves the frames.** Motion budget: $5 for the whole video including retries.
- **The X and the two-panel layout are new graphic pieces.** Show the graphic as stills at three moments (both
  playing, first X on, both X's on) with the START frames in the panels and a clear PLACEHOLDER line.
- The first minute on the round 2 page carries the opener as labelled START/END placeholder frames (ro11/ro13
  `ai_placeholder` pattern).
- This drops the round 1 plan to use his own crunches footage at 0:03.

## State at handoff

- Cut: 29 pieces from 13 rolls, 66 shots, 11:49.9 (`edl.json`, `shots.json`; every take choice in `recipe/edl.py`).
  Splice re-listens: `logs/verify_asr.txt`.
- **`words_out.json` is stale.** It predates the last two cut changes (the ending's restart at C1629 54.75 to 56.72
  removed; "So," restored at C1622 84.88). Run `asr_assembled.py` then `words_out.py` before any plan work, and read
  the assembled transcript end to end again.
- Look: `grade.py` cubes (colour A = C1630 calibration, strength 1.0), per-shot exposure trim from `skin.json`, crops
  from `measure.json`. Audio: gate PASS 13 of 13 on the round 1 first minute, -14.2 LUFS, EQ in `FIT.json`.
- Round 1 page: http://127.0.0.1:8822/ (launchctl `com.absbyai.ro02-round1-review`). Build round 2 in `round2/`, never
  over `round1/`. Re-hash the files listed in `decisions.json` before touching anything.
- The segment cache (`cache/`) holds the first 84 s at the OLD crops; the new pads change the cache key, so they re-render.
- Spend: $0.

## Round 2 work, in order

1. Framing change (answer 2). Regenerate two or three FAR / NEAR stills and look at them before going further.
2. Re-run ASR and `words_out.py`.
3. Copy `plan.py`, `resolve.py`, `gfx.py`, `stills.py`, `review_media.py`, `page.py`, `page_extra.py` and the plan loop
   of `build.py` from `../ro13/` into the ro02 recipe. Keep ro02's `edl.py`, `shots.py`, `frames.py`, `grade.py` and
   the multi-roll `render_seg`.
4. Write the plan, phrase-anchored. Carried over from the round 1 page (times are the current cut's):
   - his real vacuum (clip library B0419, or the 16:9 8/28 roll C1677) at 0:25, "the vacuum, the only ab exercise that
     can actually shrink your waist";
   - six section titles: Why Ab Exercises Do Not Burn Belly Fat; The Muscle That Shrinks Your Waist; Why The Standing
     Vacuum; How To Do It; A Live Set; Your Routine;
   - anatomy card, 1:25 to 1:58: six pack muscle in front, the deep muscle wrapped around the waist behind it. Drawn,
     simple, labelled, not an AI body. A new kind: needs its own still approval;
   - fact card: SPOT REDUCTION / Is A Myth / You burn fat evenly, all over (about 1:10);
   - KEY POINT lower thirds: Ab Exercises Build Muscle UNDER The Fat (0:13); Bodybuilders Have Used It Since THE 1960s
     (2:05); The Mirror Is HALF The Exercise (3:38); Do It On An EMPTY STOMACH (7:00); Keep Breathing: SHORT BREATHS
     Through Your Nose (8:20);
   - side lists: 3 Types Of Vacuums (Kneeling, Hands And Knees, Standing) 4:25; Why Standing (Anywhere, No Equipment,
     A Few Minutes) 5:24; Before You Start (In A Mirror, Shirtless, Empty Stomach) 6:30; The Steps (Slump, Suck It In,
     Hold 20 Seconds, Keep Breathing) 7:26; The Routine (1 Set, Then 2, Then 3, One Minute Rest) 9:20;
   - the approved self-generation demo (`Media/codex-video-trial/assets/ad/simulated-dan-sunglasses-to-pool/`, exact
     approved sequence and AI-GENERATED label) at "a real life AI transformation picture" (5:50) and in the ending (11:05);
   - a 20-second countdown over the live set (8:52 to 9:14), a new kind;
   - recap card in the takeaway (10:12); AbsByAI.com chip in the ending. No end mark.
5. `from_plan.py` without `--render` first (copy fit), then render, stills, `checks.py`.
6. The finished first minute (opener placeholders in), audio gate, hair check, every join in it frame by frame.
7. The page (RO-10 layout: decisions, first minute, AI frames, What I decided, all items three per row with the
   context player, reply box), served with `_shared/review_server.py` on a free port, every link checked, one seek
   tested. Decision budget: this video has used 5; keep round 2 to about 6 (opener frames A, opener frames B, the
   opener graphic, the anatomy card, sound, length), everything else listed as decided.
8. Handoff for round 3 with a starter prompt, board entry, queue. Stop.

## Traps specific to this film

- **Side lists over a standing, gesturing presenter on a 1080p source.** There is no W4S slide here (the studio trick
  needed a 4K frame). Check every list against every piece it spans with the person mask before proposing it; where he
  will not clear, use one lower third per item as he names it.
- With the tighter headroom, a lower third sits closer to nothing new, but a section title or a chip near the top must
  be re-checked against his hair.
- He says "supine" for the hands-and-knees vacuum: keep the speech, the graphic says Hands And Knees. "Zepbound" stays
  in speech and SRT, never in a graphic. "you want to pull your shirt out" is what he says.
- The hook (full sun) reads warmer than the cloudy sections after the trim. Dan saw it and approved A; leave it.
- The opener's two men are not Dan, so the before/after same-person rule is not in play; AI-clip defects are (hands,
  morphing limbs: check frame by frame once motion exists).
- The Extreme drive had about 50 GB free on 10-03. Machine cap: two builds across all sessions.

## Not done (do not claim)

No graphics, no clips, no AI frames, no finished first minute, no full film, no SRT or chapters, no delivery gate, no
watch pass, no independent review. Only the first minute's four joins have been looked at; the other 61 are unseen.
`roll_sidecar.py mark-used` not run (the EDL is not final until length is answered). Nothing in the clip library yet.

## Git state

Round 1's commit `73c7464` is local only: `safe-push.sh` stopped (exit 2) on other sessions' uncommitted edits to
`.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/framing-motion.md`,
`.claude/skills/shortad-from-longform/reference/render.py` and `Docs/WEB_CART.md`, still uncommitted on 10-04. This
handoff, the README row, the board line and the queue files are uncommitted for the same reason. Try
`scripts/git/safe-push.sh` once at the end of round 2 with all of RO-02's files; if it stops again, report it.

## Starter prompt (Claude Opus 5.5, effort high)

Read `Handoffs/handoff-20261004-ro02-round2-graphics-and-first-minute.md`. Name this session "The Vacuum LFC R2". This
is a CONTENT long-form. Build RO-02 round 2: apply my round 1 answers (colour A, half the headroom, the AI opener
graphic), make the opener's START and END frames with the Codex subscription, build every graphic and clip as a still
on its real frame and the finished first minute, and put it all on one review page. No AI motion and no full film
until I approve. Stop for my review.
