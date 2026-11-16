AD (Great Again T sales video). Task name: `Great Again T VSL AD R8`.

# Great Again T VSL (WV-03): round 8 handoff (2026-11-16)

Written by the round 7 editor after Dan's full round 7 review. **Model: Claude Opus 5.5, high effort.** **Dan fires this himself.**
**Run the chat ON THE M2** (the SSH connection `m2`), not on the M6: the job lives on the M2's Extreme and round 7 lost its
network share for an hour when it ran from the M6 (VIDEO-RULES "Two Macs": never run job work through the SMB share).

One native 9:16 sales video (1080x1920, 29.97), Dan on green screen over Wood Kitchen 1, roll C1903. ~25 minutes.

## 0. Where things are
- Job folder (M2): `/Volumes/Extreme/_edit_work/WV-03` (also `~/_edit_work/wv-03` on the M2, a symlink). The M6's
  `~/_edit_work/wv-03` is the frozen round 6 copy: never use it. Recipe paths on the M2 were rewritten to the Extreme.
- Dan's round 7 words, verbatim: `round8-plan/notes_r7.txt` (sha256 29bfa896...). Editor's reading: `round8-plan/decisions.json`.
  His words outrank both this file and the reading.
- Round 7 film (no notes, stands): `round7/DRAFT - Great Again T VSL R7 - First 3 Minutes - Wood Kitchen.mp4`, sha256
  `4526966636e2d62368d24730e8844c9c2fc2a5700eb84d08b13f21fc0652ed83`. Recipe `round5/film/recipe/` (`chain_film_r7.sh`,
  `render_film.py` writes round7/), build log `round5/film/BUILD_LOG.md`, independent review `round7/ROUND-7-REVIEW.md` (its
  minor notes are open: tight pacing, two shots under 1 s, mid-frame lower third at 1:57.80, "Go" caption 0.17 s).
- Frames: `round5/frames/AI-xx/` (codex/, google/, codex_r7c/), briefs `BRIEF_R7_FRAMES.md` + older briefs, characters in
  `round5/frames/characters/` (everyman, everyman_after, everyman_far, wife, fitman, dan_before_ref_*).
- Motion: `round7/motion/` (MANIFEST.json, final/, rv/ neutral review folders, prompts/, veo/job.json, PAID_REQUEST.md).
  22 verified finals. Not verified: AI-47, AI-18, AI-26, AI-54, AI-51 (both), AI-07 first pair, AI-57, AI-58.
- Graphics: `round7/graphics/` (MANIFEST.json, 67 graphics + 7 stock items + A0042): ALL APPROVED by Dan.
- Story laydown: `round7/story_laydown.json`. Review page generator: `round7/review/build_page_r7.py` (PAGE_NOTES.md).
- Spend: $3.17 of the $5 paid cap (two paid Veo takes for children Flow refuses). Flow credits 18,635. Codex images used today: 58.
- Tools: `round7/tools/m2` wrapper (for M6-driven work only). After any change to `review_server.py`/`review_player.js` run
  `python3 .claude/skills/_shared/review_refresh.py` on the M6. Review pages' Full screen now opens VLC (shared fix, 11-16).

## 1. Dan's round 7 decisions (summary; see decisions.json)
- **Graphics after 2:52: all approved.** Maca root X2, Tongkat root X1. Stock picks blank: use each item's first candidate and
  say so; S10 tablets: generate a man's palm in Flow (editor default).
- **Moving clips approved** (22 verified), except **AI-02 Two PM Crash: out** (he dislikes it); AI-68 X1 takes 1:22.
- **Motion to make from his picks:** AI-63 X1, AI-62 X1, AI-64 X2, AI-67 X1, AI-68 X1, AI-76 X1 (powder), AI-73 X1, and BOTH
  AI-70 pairs (love life, he wants to compare).
- **New START/END pairs (one character, blind pairs from both models, frame gate + fresh reviewer each):**
  1. AI-47 at 0:54 (AI Dan, number candles): a more accurate Dan, WITH GLASSES and his CURRENT haircut, slightly younger and
     a little heavier. Use recent real photos of him with glasses as identity references (find them in the project photo
     folders / `plan/asset_inventory.md`), plus the old before photos for build. Its motion failed on flames: design the END
     with the candles already out (smoke wisp) and nothing that needs fire physics, or the camera scene.
  2. 1:07 strength/stamina: on the trail with his wife and two kids; they are fine, he alone is struggling.
  3. AI-14 Stair Landing: he climbs a few steps first, then stops, tired.
  4. 1:11 stay in shape: jogging, sweaty, exhausted, then stops, defeated and frustrated.
  5. 1:14 work all day: an electrician doing complex wiring; the wall clock behind him spins (normal-speed take; the edit
     speeds it up and drives the hands in code, as planned for AI-48/AI-54).
  6. AI-15 Shoulder Ride: the Everyman in his 50s, not a young dad (child: Flow refuses; paid fallback ~$0.80 fits the cap).
  7. 1:24 active vacation, TWO new ideas: wife, a boy and a girl want to go kayaking; he does not; they push off in the
     kayaks while he sits on the dock; he lets them down. (Children: plan the paid fallback or keep kids small/from behind.)
  8. 1:35-1:39 love life, a third design beside AI-70: husband and wife in bed under the covers, after he could not perform;
     he defeated and ashamed, she angry and disappointed. Tasteful, clothed or covered.
  9. AI-77 Backyard Wiffle Ball: keep the idea; the father much closer (an underhand pitch distance); the boy's swing ends
     facing forward and to the side (follow-through), never facing backwards.
- 0:58 AI-71 had no pick: keep Dan on camera there unless he picks it.

## 2. Order of work (and what Dan sees at the end of round 8)
1. Acquire: `editroute.py pick WV-03 --kind VSL --round 8` (expect m2), `editcap.py acquire WV-03 --title "Great Again T VSL" --type AD`.
2. Tell Dan the Codex image count first (about 25-35 for these 10 ideas, both models). Make the new pairs as in round 7
   (Role A design + Google gating, Role B Flow runner, Role C Codex + gating; all on the M2 or over ssh, never the share).
3. Motion: his picks above (two takes for anything in the first minute), plus one more designed retry of the not-verified
   approved clips (AI-18, AI-26, AI-54, AI-51 x2, AI-07 first pair, AI-57, AI-58): lockstill, shorter clean ranges, calmer
   prompts. Ask Dan before exceeding the $5 paid cap ($1.83 left); never ship a faulty clip.
4. In parallel, start the FULL film (graphics are approved): key the rest of C1903 with the house key (keyonce stamps; never
   re-key a stamped piece), the approved closer framing for the whole film, build every approved graphic at its real film
   time, place every verified approved clip, and leave story slots awaiting new pairs on Dan (the camera scene). Full gates,
   watch pass, audio gate, caption proof, and a fresh independent `ra-reviewer` on the full file before Dan sees it.
5. Round 8 review page (side pane, 800 and 1370 px, silent checks then owner handoff): what changed with timestamps, the
   full film, the new pairs to pick, the new clips. Then `editcap.py release WV-03 --review` and STOP: do not start round 9
   while Dan is still reviewing or a decision is open.

## 3. Traps learned in round 7
- The M6's SMB share of the M2 drives hung (M2 smbd at 700% CPU); it now self-repairs, but never put job I/O on it.
- Gate checks time out when the M2 queue is busy: re-run with no time limit before calling a pair failed.
- Flow refuses frames with children; Replicate Veo worked ($0.80 a take) but trimmed ranges (AI-15 0-139, AI-06 108-185).
- Clips with a held object (basket), fabric, a printed label or fire failed the motion gate repeatedly: design those out.
- Google END frames edited in Flow carry the START's portrait chips; check identity on every END.
- The first "Full screen" fix test launched VLC on a wrong path when a `find` returned nothing: always test that a file exists.

## Starter prompt (Claude: Opus 5.5, high effort; start the chat on the SSH connection `m2`)

> AD (Great Again T sales video). Name this chat "Great Again T VSL AD R8". Run it on the M2. Read `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` and `Handoffs/handoff-20261116-great-again-t-vsl-round8.md`, then run round 8 of the Great Again T VSL (WV-03) as that handoff lists: my round 7 notes are saved word for word in `round8-plan/notes_r7.txt`. Make the new start and end pictures I asked for, make moving clips for my picks, retry the clips that failed, build the full film with all the approved graphics, and send me the round 8 review page tested in the side pane. Use /ad-edit.
