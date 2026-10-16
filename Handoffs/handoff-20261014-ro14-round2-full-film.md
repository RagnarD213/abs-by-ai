# RO-14 "Why You're Not Losing Weight": round 2, apply Dan's round 1 picks, AI motion, the pickup, then the full film

> **2026-10-16: the studio pickups for this job are recorded** (Dan, 10/15 shoot, shoot lav, roll C1722, green screen set): `/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1722.MP4`. Lav on the LEFT channel only (`-map 0:a:0 -af pan=mono|c0=c0`); it flat-tops at -0.49 dBFS on loud words, so check each take. Takes to use (Whisper small times, set exactly on the lav envelope, confirm by ear): the opening line (pickup 12) 342.4 to 350.5 s, the last full take; fallback 319.0 to 327.3 s. Whisper hears "the four ways you were eating" in the last take (script: "you are eating"), so listen to both. He says "four hidden reasons why you're eating them", his wording. Full take map: `Docs/PICKUPS_1017_SHOOT.md`, section "Recorded 2026-10-15: where every take is (roll C1722)". Same mic as the film: run the pickup through the film's own voice chain settings and level-match it to the film line it joins, rather than the desk-mic matching; the desk takes in this job's `pickups/` folder are timing placeholders only and do not ship.


**LFC (long-form content, 16:9).** Sidebar name: `Not Losing Weight LFC R2`.
Written 2026-10-14 by Claude (Opus 5.5) at the end of round 1. Recommended: **Claude Opus 5.5, high effort.**

Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (top sections: AI clip sense QC, budget),
`.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, `.claude/skills/longform-edit/SKILL.md`, `.claude/skills/longform-edit/reference/ro14/README.md`
(this film's recipe and traps), then Dan's reply to the round 1 page.

## Where things are

- Work dir: `/Volumes/Extreme/_edit_work/RO-14/round1/` (recipe in `recipe/`, copy in the repo at `.claude/skills/longform-edit/reference/ro14/`).
  Build round 2 in a new `round2/` folder beside it (copy `recipe/` and the data files, repoint `W`); never overwrite `round1/review/`.
- Round 1 review page: http://127.0.0.1:8964/ (`python3 .claude/skills/_shared/review_server.py 8964 /Volumes/Extreme/_edit_work/RO-14/round1/review`).
  First minute for VLC: `Videos to Review/Not Losing Weight LFC R1 - first minute.mp4`.
- Roll: 9/23 C1708 (sidecar `C1708.roll.json` beside it). Take map `recipe/edl.py` (20 pieces, last clean take of every line, reason per piece;
  one exception: the FIRST "30 days of honest tracking" copy, the second swapped words). `shots.json` (41 shots), `words.json` (medium.en
  plus five patched restart starts, `recipe/patch_words.py`), `words_out.json`, `plan.py` / `plan_resolved.json` (about 66 items), `hf/` (30 HyperFrames graphics).
- Film length 8:27.4.

## Round 1 independent check (done before Dan saw the page)

`review/INDEPENDENT-CHECK.md` (fresh reviewer, all 75 items, every first-minute join frame by frame): 7 must-fix items, all fixed and
rebuilt (`run_fix_r1.sh`): coffee clip lifted, G03 part 2 on its word (G04 starts on "People underestimate"), scale clip C19 removed,
P04 ends on the cut, reason lower thirds in Dan's own words, page text, "47%". Notes fixed too: C10 amber pint (p4752641), C12
dressing on a salad (p6162044), G15 photo a cup of oil (px10420382), T3 friends with pizza (px36729762), T4 phone shows the app result,
A4 chip top centre, G36 longer. Kept as notes: 24/25 fps stock judder, 14 s of full-screen cards in the first 32 s (G02 is where the
pickup goes). Page now 74 items.

## Locked by the editor in round 1 (Dan saw them as "What I decided"; reopen only if he names them)

Look C + W2/T2 (C1708 measures 0.294 vs 0.296 on C1713; per-shot crop lifts in `framing/crop_y.json`); voice = audio B (chain fit on this
roll's assembled voice + 0.9 dB at 150 Hz) + the standard +3 dB at 120 Hz (`fit/eq_B_bass3.txt`; tone row fails as the known mismatch);
no music; no SFX; all graphics Soft Blue HyperFrames / softblue; W4S side-card framing; the study card (Lichtman, NEJM 1992); the week card.

## Dan's decisions on the round 1 page (record his words in `round2-plan/decisions.json`, then act)

1. **Opener** (0:00 to 0:05): A1 "The broken scale" (recommended) / stock scale (Pexels 7555158, which also plays at 1:45: swap that one
   for p7801722's sibling or camera) / camera.
2. **AI clips to drop** from A1 broken scale, A2 trash-can nuggets, A3 piggy bank, A4 dessert for two, A5 salad guy, A6 donut, A7 giant drink.
   A dropped idea becomes the fallback named on the page; delete its plan item.
3. **"Five hidden reasons"**: (a) re-record at the 10/17 shoot (pickup 12 is already on `Docs/PICKUPS_1017_SHOOT.md`, the shoot doc and
   Teleprompter 0, PromptSmart script 1491684) or (b) leave as filmed (then take pickup 12 off all four places).

## Then, in order

0. **All seven frame pairs passed `_shared/framecheck/gate.py` and a fresh `frame-reviewer` on 2026-10-14** (specs, reviews and stamps in
   `aiframes/`, `aiframes/framecheck/`; rejected versions in `aiframes/rejected_r1/`). Before generating motion run
   `gate.py START END --verify` on each approved pair; any frame edit clears both checks (re-gate, fresh reviewer).
   A3 now ENDS on a fist pump with the pizza untouched (the slice version failed review three times); A4's whole pair was remade
   (one fork on the plate in START, the same fork carries the bite in END); A5 and A6 ENDs were repaired in code
   (`*.repair.txt`). Reviewer notes worth putting in the motion prompts: A1 "he steps back off the scale, bends, lifts it" (the
   rug was redrawn slightly, watch for shimmer); A2 "he picks up each nugget and eats it, none vanish"; A3 "a big laugh" (END face
   is close to START); A7 "he shuffles along the seat toward the cup"; A4 the cake must not shrink.
1. Motion for each approved pair from exactly those frames: `.claude/skills/ai-clip-ideas/reference/gen-veo-keyframes.js` (RO-13, RO-17):
   no audio, Veo 3.1 Fast, about $0.15 a second. Durations: A1 6 s, A2 8 s, A3 6 s, A4 8 s, A5 6 s, A6 6 s, A7 8 s. Guard any generation
   script with `if __name__ == "__main__":`.
2. **Before Dan sees any motion**, every take gets the measured self-change map (`longform-edit/reference/ro08/a5_cut.py`) and the three
   questions (cause and effect; readable with the sound off; shows the line, joke lands). Regenerate or trim a take that fails; at the
   $15 cap with problems left, ask for budget first. Crop the 4 black rows Veo leaves top and bottom (RO-13). Known risks: A1 the scale must
   be lifted by his hands, not float; A2 all three nuggets must go into his mouth, none vanish; A3 coins must spill from the broken pig
   and the pizza must stay untouched;
   A4 the cake plate must slide by her hand; A5 the waiter must walk out, not vanish; A6 one donut leaves the box in his hand.
3. Plan: each approved `ai` item becomes `kind="clip"`, `label="AI-GENERATED"`, chip measured clear of faces. `resolve.py`, then
   `from_plan.py --render` (only changed graphics re-render), `dupscan.py`.
4. **If decision 3 is (a) and the 10/17 pickup is in:** find pickup 12 on the shoot roll (`pick_lav.py`, `roll_sidecar.py`), last clean take,
   lay it over film 16.1 to 29.4 under the G02 card (replace the source audio of that span; G02 already covers the picture), match level and
   tone by ear and on the gate rows, and remap words for G02's reveals. If the pickup is not filmed yet, build with the filmed line and say so.
5. Full film: `build.render_range(0, 507.41, round2/RO14_MASTER.mp4)`, then the finish chain from RO-17 (`finish.py`, `finish_chain.sh`:
   audio gate, transcript, SRT from the delivered audio, chapters, watch pass, `haircheck.py`, hyperframes `checks.py`), own
   negative-events scan, one `ra-reviewer` independent review (all images incl. the pair strips; the three AI questions per clip in
   its brief), `watch.py --judge`, edit sheet + `validate.py`, delivery gate (`--format longform`), deliver to
   `claude edited long form content/<NN> - Why You're Not Losing Weight/` with the REVIEW 540p copy, A/B, stamps, notes, recipe.
6. Copy the full film to `Videos to Review/Not Losing Weight LFC R2 - full film.mp4`, open the folder, send Dan the page + file names.
   `queue.py set RO-14 delivered`, mirror to the Edit Queue page, board entry, commit.

## Cost ledger

Known: Gemini about $0.65 (verbatim restart listen, the 'five' splice test); sidecar $0.001. Codex images: 21 (14 frames + 7 redraws), on the subscription ($0).
Veo: $0 so far. Cap: $15 for this long-form (Dan 2026-10-13). Unknown: none.

## Starter prompt

> CONTENT (LFC). Name this task `Not Losing Weight LFC R2`. Read and execute
> `Handoffs/handoff-20261014-ro14-round2-full-film.md`. My answers to the round 1 page: [paste the reply box].
> Make the AI clips I approved, check them before I see them, then build the full film, every gate, independent review, and send me
> the review copy.
