# AI inserts for the website video — get the perfect clip, regenerate rather than trim

Dan's instruction (2026-09-09): invest MORE in AI clips here than in content or ad videos — money and attempts —
because a clip that reads as AI, or as staged, or as a different exercise than the one named, costs trust on the page
where trust is the product. Budget inside the $25/session cap; a still is ~$0.13 (nano-banana draft tier), a Veo 3.1
Fast 8-second 1080p clip is ~$1.20. Ten clip attempts and a dozen stills is a normal video, not an overspend. State the
estimate before a batch, keep the running total, filtered attempts are free.

## The character

One man across every clip: `reference/recipe/ai/prompts/MAN.txt` (an ordinary white man ~42, deliberately NOT a model,
open pores, a crooked smile, lean and visibly ripped). His reference image is the approved pool still
(`ai/stills/A.jpg`); every new still passes `--image` of that reference. Continuity is the whole point — if the man
changes, the seven clips read as seven ads.

**Change one thing = edit the approved still in place.** "Steak instead of chicken" was three in-place edits of the
rev-5 stills ("Edit this photograph. Change only the food… keep absolutely everything else identical: the same man, his
exact pose…") and every other pixel stayed. New scene = new still from the man's reference.

## Prompting (Step 4.5 of /ad-edit, verbatim rules)

Never in a prompt: camera or lens brands, anamorphic, bokeh, shallow focus, lens flare, dolly, crane, gimbal,
steadicam, push in, whip pan, colour grade, LUT, film grain, slow motion, cinematic, dramatic lighting, epic,
stunning, moody, anything implying a crew. Lean on: handheld, flat daylight, slight camera shake, one small reframe
mid-shot, amateur photograph realism. State the texture (pores, uneven tone, hair out of place), the clothing down to
its wear, a settled expression. Rule out lettering, logos, makeup, sunglasses, hair across the face. Frame it slightly
wrong. Hold ambience density constant across all clips.

Things the model renders badly, so never ask for them (each one shipped once):
- breath, smell, steam, blowing near the face → smoke out of his mouth
- a beat that ends on static objects → they drift and vanish
- "glances up at the camera" → a theatrical grin to camera
- hands to the floor / a rest position inside a rep exercise → a different exercise
- a tall pose (legs raised) without saying "WIDE shot, he occupies the lower two-thirds, empty wall above his toes"
  → the feet are cropped at the top edge (took three stills)
- a home exercise with any equipment in shot (Dan: "at home without weight")

Always ask for: still working / still mid-rep at the end of the shot; hands never touch the floor (for floor abs
work); legs never come down; the exact food Dan named (steak).

## Acceptance checklist — per clip, on frame strips, before it goes in

Build three strips with `strip.py`: whole clip at 0.5 s, first second at 0.1 s, last second at 0.1 s (and the last
second of the span you will actually USE, which is usually not the clip's end). Look at them at full size. A clip
passes only if every line is a yes:

1. The still: whole figure inside the frame (no cropped feet, no cut head), six fingers / scrambled signage / wrong
   props absent, the man is the same man, the room matches the story (home = living room floor, not a garage gym).
2. The movement is unmistakably the named exercise or action for the whole used span; no rest position, no second
   exercise, no sit-up when a toe-touch was asked for.
3. Nothing from the mouth or face (smoke, steam, a mid-word freeze); no grin to camera inside the used span.
4. No baked dissolve or double image anywhere in the used span (Veo bakes a cross-dissolve roughly one clip in three
   — 0.5–0.9 s and 3.9–4.6 s on D2 rev 4, 2.5–2.9 s on D2 rev 6). If the clean shots on either side are each usable,
   cutting them together with a straight cut is allowed (`build_inserts.EDIT`) — a cut reads as b-roll editing.
5. No static hold at the end of the used span; no object drift in its last second.
6. The used span, after in-point (skip Veo's static opening ~0.2–0.3 s), covers the beat + 0.10 s at 0.85–1.0× speed.
   Never slow a clip below 0.85× to fill a beat — shorten the beat or hand time to a neighbour.
7. Watch-pass sanity after the mix: flagged jumps inside the clip should be a handful, not twenty (the rejected curl
   clip carried 23 of the video's 30).

A clip that fails 2, 3, 4 (with no clean shots) or 5 is **regenerated** — new prompt line addressing the failure, same
still — up to three attempts, then a different action for that beat, then tell Dan. Trimming is for a clean clip that
is too long, never for hiding a flaw: the two rev-4 tails Dan caught were trimmed around, and he saw them anyway.

## Placement

Full-frame inserts, tagged AI-GENERATED upper-left at 1.5× (`gfx/tag15.png` at 40,40), captions stay on, 0.5 s alpha
fades only at the OUTER edges of a run (A→B, C1→C2, D1→D2→D3 are straight cuts). A run must end at least 0.36 s
before the next lower third and ≥ 0.5 s before a before-photo card (asserted in `beats.py`). The punch plan treats a
segment hidden under an insert as not advancing the NEAR/FAR alternation, so the framing changes across every insert.
Every insert's MOV is checked against its beat length before the mix (`|mov − beat| < 0.1 s`).

## Where the seven beats sit (first video, for orientation — a new script gets its own)

pool reveal → beach jog (hook, ~0:19–0:30); toe-touches at home → water/towel nod (~2:04–2:15); grilling steak →
portioning → eating (~2:28–2:44). Dan chose these placements on the rev-3 review to break up the talking head; the
principle is one or two runs per minute of pitch, each illustrating the sentence literally.
