# RO-17 "3 Healthy Foods That Made Me Fat": round 3, apply Dan's round 2 picks, AI motion, then the full film

**LFC (long-form content, 16:9).** Sidebar name: `3 Healthy Foods LFC R3`.
Written 2026-10-14 by Claude (Opus 5.5) at the end of round 2. Recommended: **Claude Opus 5.5, high effort.**

Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (top sections: AI clip sense QC,
budget, thumbnails do not apply here), `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, `.claude/skills/longform-edit/SKILL.md`,
`.claude/skills/longform-edit/reference/ro17/README.md` (this film's recipe and traps), then Dan's reply to the round 2 page.

## Where things are

- Work dir: `/Volumes/Extreme/_edit_work/RO-17/round2/` (recipe in `recipe/`, copy also in the repo at
  `.claude/skills/longform-edit/reference/ro17/`). Build round 3 in a new `round3/` folder beside it; never overwrite `round2/review/`.
- Round 2 review page: http://127.0.0.1:8877/ (`python3 .claude/skills/_shared/review_server.py 8877 /Volumes/Extreme/_edit_work/RO-17/round2/review`).
  First minute copy for VLC: `Videos to Review/3 Healthy Foods LFC R2 - first minute.mp4`.
- Roll: 9/23 C1713. Take map `recipe/edl.py` (19 pieces, last clean take of every line, reasons per piece), `shots.json` (42 shots),
  `words_out.json` (roll medium.en words mapped to the film), `plan.py` / `plan_resolved.json` (60 items), `hf/` (28 HyperFrames graphics).
- Film length 7:32.2.

## Locked by the editor in round 2 (Dan sees them as "What I decided"; reopen only if he names them)

Look C + W2/T2 (C1713 measured the same as C1707; per-shot crop lifts in `framing/crop_y.json` where hair came within 4 %);
voice = audio B (chain fit on this roll + 0.9 dB at 150 Hz) + the standard +3 dB at 120 Hz (`fit/eq_B_bass3.txt`; ranked first in 3 of 3
blind listens; tone row fails as the known mismatch); no music; all graphics Soft Blue HyperFrames; B-roll grades on C05, C10, C12;
side-card framing W4S = 2690x1513 @ 110,183 (4 % in so the backdrop's edge and clamps never show); no reframe cut under a side card.
Before Dan saw it, two independent checks ran on the page (`review/INDEPENDENT-CHECK.md`, the first in `review/_superseded_r2a/`);
the frames of A4, A5, A7 and A10 were redrawn after the first (rejected versions in `aiframes/rejected_r2a/`).

## Dan's decisions on the round 2 page (2026-10-14, recorded with frame hashes in `/Volumes/Extreme/_edit_work/RO-17/round3-plan/decisions.json`)

- **Opener: A3 "The calorie scale"**, with one change. Dan: *"I like this idea for the opener, but I want to change the trail mix.
  Keep everything else the same, but the trail mix, those M&M's, I want to change them to white little orbs that look like M&M's,
  like white M&M's, like yogurt-covered raisins type of thing. Something that isn't obviously unhealthy. Just change that. Keep
  everything else in the opening frames the same."*
- **A2 Couch snacking:** the same change. *"Make it like white yogurt-covered raisins instead of M&M's in the trail mix. Keep
  everything else the same."*
- **As is, motion authorized:** A4 Candy in the nut jar (*"Keep candy in the nut jar the same. Generate as is."*), A1 The hiker at his
  desk (*"Generate hiker at his desk as is."*), A5 Grapes vs raisins, A7 Nothing left for dinner, A8 The boardroom (*"looks good"*).
- **A10 One can and done: new character.** *"I like the idea for 'One can and, you're done,' but I want to make this a guy who's
  ripped and in shape, wearing a tank top."*
- **Clip C13 cut** (library B0479, now marked rejected in the clip library): *"This is literally relevant, but it's a weird clip where
  I'm looking down and off-center here. Eliminate that clip and just use the camera scene."*
- **Everything else approved:** *"Everything else looks good."* (all graphics, section cards, stock clips, real photos, the first minute,
  look and voice.)

## Then, in order

1. **Frames.** Codex subscription (`.claude/skills/_shared/codex-image.sh`, two jobs at a time: eight at once hit 429).
   - A3 and A2: edit BOTH frames of each pair and change only the candy in the trail mix: the colourful candy-coated chocolates
     become small white yogurt-covered-raisin orbs (round, white, the same size); nuts, raisins, every other pixel unchanged. Edit
     START first, then END with the new START as a second reference so the orbs match. For A3 that includes the trail mix in the cup
     and on the pan; for A2 the mix in the bag and in his hand.
   - A10: a new pair. A ripped, lean, in-shape man (not bulky) in a tank top on the same sofa at night, framed from the chest up.
     START: the last sardine on his fork near his mouth, an empty open tin in his other hand. END: the empty tin with the full-size fork
     in it set on the sofa back beside his shoulder, hands clasped behind his head, content. Keep the fork the same size in both
     frames and the tin empty (the two faults the round 2 reviewer caught).
   - Every new or edited pair: spec (copy `aiframes/specs/<ID>.spec.json`, keep its people boxes), `lockstill.py` with the spec's
     boxes (build the `--box` arguments in Python, not zsh), `framecheck/gate.py`, then a fresh `frame-reviewer` agent, then
     `gate.py --verify`. Redraw until PASS.
   - **Show Dan the new A10 pair before its motion** (a new character is a materially different frame: VIDEO-RULES), on a one-section
     page, together with the A2 and A3 revised frames for a look (those two need no answer: he specified the change). Send it early and
     keep working; only A10's motion waits on his reply.
2. **Motion** for A1, A4, A5, A7, A8 now, A2 and A3 once their edited frames pass the gate and reviewer, A10 after Dan's yes.
   Stamps: `aiframes/<ID>-end.png.framecheck.json`, specs `aiframes/specs/<ID>.spec.json`, reviews `aiframes/framecheck/`. Call
   `require_pass(START, END)` before generating, and re-gate plus re-review if a frame changes. Reviewers' notes to watch in the
   takes: A1 the hand must dip into the bag before the mouth; A3 the beam's left half and the burger's cheese may shimmer; A4 the
   scoop must not grow; A5 the raisins must not change shape as they land; A10 he must eat the sardine (not vanish it) and the tin
   must not slide. Generate with `.claude/skills/ai-clip-ideas/reference/gen-veo-keyframes.js` (RO-13
   used it: no audio, Veo 3.1 Fast, about $0.15 a second). Durations: A3 4 s, A2 6 s, A4 6 s, A1 6 s, A5 8 s, A7 6 s, A8 4 s, A10 6 s.
   Guard any generation script with `if __name__ == "__main__":` (RO-12 trap 12).
3. **Before Dan sees any motion**, every take gets the measured self-change map (`longform-edit/reference/ro08/a5_cut.py`) and the three
   questions (cause and effect; readable with the sound off; shows the line, joke lands). Regenerate or trim a take that fails; at the
   $15 cap with problems left, ask for budget first (alone, with the number). Crop the 4 black rows Veo leaves top and bottom (RO-13).
   Known risks: A3 the scale must tip only after the trail mix lands; A4 the sticker's leaf and the candy must not morph; A7 the floret
   must be there under the dome, not appear; A10 the tin must be set down, not vanish; A8 bills must leave the hands.
4. Plan: delete C13 from `plan.py` (Dan on camera for "Just drink water"; confirm with `build.jumps()` that the source join at about
   4:21 is a W2/T2 size change and no presenter sliver appears). Each approved `ai` item becomes `kind="clip"`, `label="AI-GENERATED"`, chip measured clear of faces. `resolve.py`, then
   `from_plan.py --render` (only changed graphics re-render; compare against round 2 renders with psnr), `dupscan.py`.
5. Full film: `build.render_range(0, 452.15, round3/RO17_MASTER.mp4)`, then the finish chain from RO-13 (`finish.py`, `finish_chain.sh`:
   audio gate, transcript, SRT from the delivered audio, chapters, watch pass, `haircheck.py`, hyperframes `checks.py`), own
   negative-events scan, one `ra-reviewer` independent review (all images incl. the pair_* strips; the three AI questions per clip in
   its brief), `watch.py --judge`, edit sheet + `validate.py`, delivery gate (`--format longform`), deliver to
   `claude edited long form content/<NN> - 3 Healthy Foods That Made Me Fat/` with the REVIEW 540p copy, A/B, stamps, notes, recipe.
6. Copy the full film to `Videos to Review/3 Healthy Foods LFC R3 - full film.mp4`, open the folder, send Dan the page + file names.
   `queue.py set RO-17 delivered`, mirror to the Edit Queue page, board entry, commit.

## Cost ledger

Known: Gemini listening about $0.75 (round 2). Codex images: 34, on the subscription ($0). Veo: $0 so far. Cap: $15 for this
long-form (Dan 2026-10-13). Unknown: none.

## Starter prompt

> CONTENT (LFC). Name this task `3 Healthy Foods LFC R3`. Read and execute
> `Handoffs/handoff-20261014-ro17-round3-ai-motion-and-full-film.md`. My round 2 answers are recorded in it. Swap the trail mix candy
> for white yogurt-covered raisins on the opener and the couch clip, make One can and done with a ripped guy in a tank top and show me
> that pair, cut C13, make the other AI clips as they are, check every clip before I see it, then build the full film, every gate,
> independent review, and send me the review copy.
