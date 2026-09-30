# RO-12 "Top 5 Zepbound Tips": round 2, approve two clips one by one, then remake the full video

Written 2026-09-30 by Claude (Opus 5.5) from Dan's notes on the delivered round-1 cut. Supersedes the open actions in
`handoff-20260930-ro12-round1-dan-review.md` (keep that file for the recipe and locks). Recommended model: **Claude Opus 5.5,
medium** (two bounded inserts on a working recipe).

## Dan's words (verbatim record: `/Volumes/Extreme/_edit_work/ro12/round2-plan/decisions.json`)
> "I don't like this clip at 1:43. This doesn't clearly show the idea of nausea and fatigue. Give me start and end frames for an
> AI-generated clip of a slightly overweight 40-year-old man with a plate of food. He eats a few bites, and then he holds his
> stomach with nausea." ... "at 256, I want you to find a video clip on YouTube or somewhere else of someone demonstrating a
> Zepbound injection. Don't show the syringe in the clip or the injection itself. Just show someone pinching the appropriate part
> of the thigh (like I'm referring to) to prepare themselves for the injection. Show me that clip for approval in the next round."
> "Make me a handoff document to approve those revisions individually in the next task, and then we'll remake the full video."

Reviewed master: `claude edited long form content/09 - Top 5 Zepbound Tips/Top 5 Zepbound Tips | claude | 16x9 | RO-12.mp4`,
sha256 `a4230be29b770b1b...` (full value in decisions.json). Work dir `/Volumes/Extreme/_edit_work/ro12/`, frames in `rev1/`.
Dan was shown `claude edited long form content/09 - Top 5 Zepbound Tips/round2-frames/RO12-round2-frames.jpg` in chat on 09-30.

## The two items (present each one separately; Dan approves, changes or rejects each)

**R1: 1:44-1:47, "The nausea, the fatigue, the days where you feel like garbage"** (plan item `I03`, stock `px10515019`, source
232.26-235.48 s, slot about 3.2 s). Replace with a new AI clip.
- Recommended frames: `rev1/N1-start.png` (slightly overweight man, navy t-shirt, kitchen table, grilled chicken, rice and
  vegetables, fork raised) and `rev1/N1-end-b.png` (same man, fork down, hand over mouth, other hand on his stomach, eyes shut,
  turning away). Checked at full size: natural hands, same identity, no steam, no text.
- Alternatives to show beside it: `N1-end.png` (subtler nausea), `N2-start/end` (pasta, reads average build, weaker), and the
  existing library clip A0060 (fit man in a grey shirt, one bite, stomach pain; $0, motion exists).
- Intended motion (4 s): he takes a bite, chews, sets the fork down, then presses his stomach and covers his mouth. The script says
  "a few bites"; 4 s holds one bite plus the reaction. Say so and offer 6 s with a trim if Dan wants two bites visible.

**R2: 2:56.26-3:02.80, "Inject into your thigh on the outer front part right around the middle. Not the inside of your leg, not
down by your knee"** (source 332.42-339.08, currently Dan on camera, then the G05 steps card at 3:03.25). Add a full-frame insert.
- The search Dan asked for came back empty: 11 Pexels clips, 1 Pixabay clip and 21 YouTube injection tutorials (Gemini watched each;
  `rev1/pinch/yt_scan1.json`, `yt_scan.json`). No clip shows a clean outer-front-thigh pinch without a syringe or pen in frame.
  Nearest misses, to show as links with timestamps (never download before Dan picks one):
  `https://www.youtube.com/watch?v=HcAsUbiFJyw&t=138` (2:18-2:21: bare thigh through bike shorts, syringe in her other hand, vertical
  video inside a collage, identifiable creator) and `https://www.youtube.com/watch?v=T4NWm7mqbHI&t=363` (6:03-6:06: low res, a
  diagram covers a third of the frame, pinch through a dress). Also note a YouTube excerpt is someone else's footage and can draw a
  Content ID claim on the upload.
- Recommended instead: AI frames `rev1/P3b-start.png` (man in a grey t-shirt and plain navy shorts seated on a bed, hand resting on
  the thigh) and `rev1/P3b-end.png` (same frame, thumb and two fingers pinching a fold on the outer thigh). No syringe, pen or needle.
  Checked: anatomically correct hands; the shorts' logo was painted out by hand on the start frame (a local clone patch, no
  regeneration). Rejected attempts, do not show as options: P1 (pinch reads as a grip), P2 (malformed hand).
- Intended motion (6 s): his hand moves from resting to pinching the fold and holds it; nothing else moves. If Dan wants the pinch
  on the front of the thigh rather than the side, regenerate the end frame only (about $0.15).

## Order of work
1. Re-hash the files above against decisions.json. Build one review page per memory `review-page-what-i-decided` (a "What I
   decided" block, then R1 and R2 each with its frames, the words before/under/after, and Approve / Changes / Remove). Stop and
   send Dan the page. Do not generate motion before he approves each pair of frames (VIDEO-RULES frame-approval rule).
2. On approval, generate motion with Replicate `google/veo-3.1-fast` (`image` + `last_frame`, 1080p, 16:9, no audio): R1 4 s
   (about $0.60), R2 6 s (about $0.90). Check every frame for AI giveaways (hands, fork, food morphing, fingers merging into skin).
   Show each clip in context (5 s either side, `<ID>-context.mp4`) for approval. One retry each fits the budget.
3. After both clips are approved, edit `recipe/plan.py`: replace `I03` with the R1 clip (`ai=True`, AI-GENERATED chip placed clear
   of his face, bottom corner) and add an insert for R2 over 332.42-338.9 source (`ai=True`), ending before G05. Check the
   insert-length rule (slot must not exceed the clip) and the sliver rule. `build.py timeline`, `stills I03 <R2 id>`, then
   `zsh recipe/rebuild_r2.sh` (about 60 minutes; two-build cap first). Negative-events rescan, gate, a fresh independent reviewer
   (brief: copy `REVIEW-BRIEF-R3.md`, scope it to the two new inserts plus the full-film checks), deliver with `recipe/deliver.sh`,
   send Dan the new REVIEW 540p, set the queue to `delivered`.
4. Register both approved clips in the clip library (`clip_library.py add ... --status used-final --used-in "RO-12"`).

## Still open from round 1 (unchanged, Dan's calls)
Burger stock at 5:56 (negative-events row needs a human); the vial ad-lib at about 2:40; whether organic videos keep the ad rule
banning "Zepbound" in speech and subtitles (two gate rows). Gate state on the round-1 master: 34 pass, 4 fail (the known rule
mismatches), 1 needs review.

## Cost ledger (this video, $5 AI cap)
Frames so far: 13 nano-banana-pro 2K images, about $1.95 (includes the rejected P1/P2). Gemini: about $1.10 (round-1 listening),
about $0.90 (YouTube search), reviewers under $2.30, all under the Gemini quality-review authorization. Motion: $0 so far; planned
$1.50 plus at most one retry each keeps the video under $5.

## Starter prompt
> Read `Handoffs/handoff-20260930-ro12-round2-two-clips-then-full-remake.md`. Build the round-2 review page for RO-12 and show me
> R1 (nausea clip frames) and R2 (thigh-pinch frames and the two YouTube near-misses) so I can approve each one separately. After I
> approve, generate the motion, show me each clip in context, then remake the full video, gate it, independent review, and send me
> the new review copy.
