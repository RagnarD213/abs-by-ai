CONTENT (LFC). Task name: `First Time At The Gym LFC R2`. Model: Claude Opus 5.5, high effort (the video started on Claude).

# RO-37 "I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time": round 2 (cutout rebuild)

## Dan's round 1 verdict (exact words; full record `/Volumes/Expansion/_edit_work/RO-37/round2-plan/decisions.json`, sha256 c5468b14...)
- On the R1 page: "I feel like the crop looks awkward... This looks weird with the boxed-in thing. Maybe some kind of graphics next to me the whole time."
- On the 20 s cutout test (http://127.0.0.1:9538/, `cutout_test/test-bim.mp4`): "Yes, this cutout works. I think we should edit the video this way.
  I like what you did with the ending scene and with the 'how this looks' full-screen graphic. I think we should only rarely use that super
  close-in shot, though, or only if we can generate some footage on the sides. I think it's just a little bit too close to be used, maybe rarely
  for that. Go ahead and edit the video in this way. Focus more on the green screen shots and full-screen graphics with me and the scene behind me.
  Try some scenes like that, and just use that super close-in shot sparingly."
- "The ending scene" = test 0:13-0:20: his gym clip full screen, Dan cut out small in the lower right. "The how this looks full-screen graphic" =
  test 0:00-0:08: Dan cut out on the right on the moving Soft Blue field, a list card on the left.

## Read first
`Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (green-screen sections, round-1 rules, hair clearance, silent review),
`.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, `.claude/skills/_shared/greenscreen-bg/README.md` (THE layout system now: types soft, corner,
side, wall, cards, bigtype, panel, set; planner rules), `.claude/skills/longform-edit/reference/ro37/README.md` (portrait traps + the approved
cutout method), and RO-24's round 3 recipe it points to (`longform-edit/reference/ro24/round3/`).

## What carries over unchanged (round 1, `/Volumes/Expansion/_edit_work/RO-37/round1/`)
- EDL (35 pieces, 7:55.5, every join re-transcribed clean), `words_out.json`, colour F grade, voice A chain, 13 tuned gym B-roll clips
  (`broll/grade.json`), 24 HyperFrames graphics (`hf/`), lav wavs, hair_roll.json. Hashes in decisions.json `locked_hashes`.
- Six AI frame pairs passing gate + fresh reviewer (`ai/frames_report_page.json`): A1 Frozen at the gym door, A2 Done at hour two, A3 Too sore
  for the stairs, A4 The gym bag under the desk, A6 Two weeks of cobwebs, A7 Nobody is watching you. NOT yet approved by Dan; no motion authorized.

## What changes in round 2
1. Every presenter shot is the cutout (method in ro37 README / `cutout_test.py`: BiRefNet per frame, 3-frame median alpha, ~$0.002 a frame) placed
   with the greenscreen-bg template: background changes on cuts with what he says (soft = his gym clip or the pool picture blurred/navy, corner
   over a gym clip, side, cards, bigtype for his numbers like "15 minutes", the Soft Blue field with a list beside him). Keep W/T style size
   changes at every cut by the template's own wide/tight placements, not the full-frame close-up.
2. The full-frame pool close-up: rarely (a few moments at most). Dan's alternative "generate footage on the sides" is optional; do not spend on it
   without showing him a sample.
3. Lower thirds and side lists sit beside or below the cut-out Dan, never across his face or abs (measure with the person mask).
4. Matting cost estimate: cut-out frames only (B-roll and full-screen cards excluded), about 9,000-12,000 frames = $18-24 on Replicate: inside the
   $25 session cap but state the estimate before the batch; first minute alone is about $3. Apple Vision (free, softer) is the fallback.

## Round 2 deliverable (round-1 style page, since the look changed)
The first minute rebuilt this way, plus every graphic/clip in context with the new layouts, and still open from R1: colour (F recommended), voice
(A recommended; blind listener preferred C), opener (A1 recommended), which AI pairs to animate, weeks 2-4 layout. Keep "What I decided" and
the reply box; hair/face clearance check on the cutout; Videos to Review copy; silent checks then owner handoff. No full film until the
choices and AI motion are locked.

## Next action
1. `python3 .claude/skills/_shared/editcap/editcap.py acquire RO-37 --title "I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time" --type LFC --release 2027-01-01`
   (exit 3 = wait with `editcap.py wait RO-37` in the background).
2. Re-hash the locked files against decisions.json. Build in `/Volumes/Expansion/_edit_work/RO-37/round2/` (copy round1/recipe; never overwrite round1).
3. Plan the backgrounds with the greenscreen-bg planner on the round-1 EDL and plan; matte the first minute; render; page; stop for Dan.
Release Fri Jan 1, 2027; finished and set up by Dec 18. Spend so far: about $0.90 (cutout test).

## Starter prompt
> Read Handoffs/handoff-20261029-ro37-first-time-at-the-gym-r2.md and run round 2 of "I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time" (First Time At The Gym LFC R2): rebuild it with Dan cut out of the pool footage in the green-screen background style he approved, the close-up used rarely, then deliver the round-2 page. Name the chat "First Time At The Gym LFC R2".
