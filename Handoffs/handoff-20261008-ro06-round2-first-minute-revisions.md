# RO-06 "How To Work Out At Home On A Budget": round 2, revise the first minute to Dan's notes

**LFC (long-form content, 16:9).** Sidebar name: `Work Out At Home LFC R2`.
Written 2026-10-08 by Claude (Opus 5.5) after Dan reviewed the round 1 first minute. This replaces
`handoff-20261008-ro06-round1-dan-review.md` as the next action (that doc still describes the full-film steps for later).
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/longform-edit/SKILL.md`,
`.claude/skills/longform-edit/reference/ro06/README.md`, `/Volumes/Extreme/_edit_work/ro06/round2-plan/decisions.json`.

## Scope of this round
Rebuild ONLY the first minute with the framing and B-roll changes below, in `/Volumes/Extreme/_edit_work/ro06/round2/`
(never overwrite `round1/`), refresh the stills that change, show Dan a short round 2 page, then stop. No full film yet.

## Locked by Dan (do not reopen)
- **Audio:** "The audio is sounding good." The voice chain as used in round 1 (lav only, EQ in `FIT.voice_chain.json`,
  no echo removal). Voice only; the music question is still open.
- **Colour:** "Color correction is looking good." Grade option B (`grades.json`, `look_option.txt` absent = B).
- Reviewed file: `round1/first-minute/DRAFT - RO-06 round 1 - first minute.mp4`, sha256 starts `cbd671f92fc97493`
  (full hash in `decisions.json`). Re-hash before building.

## Dan's notes, word for word
1. "For the start of the video, I want this to start on the tight shot of me, cropped slightly above my hairline to a
   little bit below my shorts line. Start in on the tight shot in the first few seconds."
2. "I like the first B-roll clip that you did with the ab wheel. I would like three B-roll clips here: a different one,
   not two ab wheel clips, but ab wheel and me doing two other exercises with this setup, to illustrate the point that
   there are a few different things and that this isn't only about the ab wheel."
3. "I do think it'd be good to start on the tight shot, then go to the wide shot, like you have it. Throughout the
   video, I'd like to see a little bit more of the tight shot. Once we've established that stuff on the ground in front
   of me, then I think we can alternate between that tight shot that we used at the start and the wide shot. We don't
   have to go super wide like this all the time. Just establish it, and then use it occasionally throughout the video
   for that super wide shot showing all the stuff on the floor in front of me."

## What to change
- **Tight shot = hair to just below the shorts.** Already measured per shot: `shot_framing.json` now carries `T2`
  (crop w, h, x, y), `zt2` (1.8x to 2.44x on the wide rolls, about 2.05x on the hook) and `active` (13 shots where he
  raises his arms, bends or steps sideways: these cannot take the tight crop). `recipe/framing.py` writes them.
- **Still to code** (nothing below is done yet): in `recipe/frames.py` `crop_of()` add a third framing; in
  `recipe/build.py` `all_segments()` solve with three sizes on the wide rolls: tight `T2` (default, cost 0), medium
  (the current `T`, 1.5x, only where a real join needs a size change), wide `W` (the establishing shot, the $58 list,
  `active` shots, and a few times through the film). Keep: a real join inside one roll never has two sizes within 1.2x;
  joins inside one continuous take need no cut at all; flip a middle shot to medium when one size would hold over about
  22 s. Medium rolls (C1563, C1574, C1577 to C1579): their 1.3x crop is already hair to shorts, prefer it. Close rolls
  (C1580, C1581): the camera frame is already tighter than his tight shot, prefer the camera frame.
- **Opening order:** `hook.0r0` tight (0 to 3.7 s), then the B-roll, then `hook.0r1` wide (the establishing shot, "like
  you have it"), then tight again. Set these two in `OVERRIDE`.
- **C01 becomes three clips** over "This is a setup I personally use ... make gains during that time" (3.7 to about
  10.9 s, about 2.4 s each): ab wheel `B0436@2.0` first (the one he liked), then two other exercises that cannot be
  mistaken for it, for example jump rope `B0447` and kettlebell swings `B0439`. No source may repeat later in the film
  (`B0430`, `B0431`, `B0427` are already used later). In `plan.py` set `end="during that time"`.
- The tight shot is a 2x enlargement of a 1080p frame, so it is softer than the wide. Raise the sharpening for it
  (`unsharp` in `build.render_seg`), compare at full size against the medium, and tell Dan plainly what he is trading.
- Then: `resolve.py`, `from_plan.py` (unchanged scenes are skipped), render the first minute to
  `round2/first-minute/`, audio gate, contact sheet, a frame strip of every cut, dense hair check on the tight shots
  (hair must stay at least 20 px from the top; on rolls C1567 to C1574 the source has only 5 to 15 px, report it).
- Regenerate the stills whose framing changed and a short round 2 page (`recipe/page.py` is the generator): the first
  minute on top, "What changed", the still-open decisions, one reply box. Serve it with `_shared/review_server.py`.

## Still open from round 1 (Dan has not answered; do not infer from silence)
3 hair at the top edge on 9 rolls · 4 length (trim repeats or keep 17:39) · 5 AI product pictures in the price cards ·
6 jump rope "$10" vs "$9" · 7 music bed · 8 app demo treatment · 9 an AI opener (his notes keep the on-camera open).
Ask again on the round 2 page, in one list.

## State and costs
Round 1 page still at `round1/index.html` (server on port 8846 may have stopped). Cut, shots, plan and all 41 graphics
are built and unchanged. Spend: $0 metered, six Codex stills on the subscription. Queue: `draft_review`.
Not run yet: delivery gate, watch pass, independent review (they need the complete film).

## Starter prompt (Claude, Opus 5.5, high)
> Read `Handoffs/handoff-20261008-ro06-round2-first-minute-revisions.md` and execute it with /longform-edit. This is
> RO-06 "How To Work Out At Home On A Budget", long-form content (LFC); name this task `Work Out At Home LFC R2`.
> Rebuild only the first minute: open on the tight shot (hair to just below my shorts), then the wide, tight shot as
> the default through the film, and three different B-roll clips at the start (ab wheel plus two other exercises).
> Audio and colour are approved, do not change them. Show me the new first minute and the open decisions, then stop.
