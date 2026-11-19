AD (Great Again T upsell video). Task name: `GAT Upsell 2 AD R2`.

# Great Again T Upsell 2: Eternal Burn AM/PM (WV-05): round 2 handoff (2026-11-19)

Written by the "GAT Upsell 2 AD R1" chat after Dan's round 1 review. **Model: Claude Opus 5.5, high effort.** **Mac: the M6**
(the job lives at `~/Projects/_edit_work/WV-05`, internal SSD). One native 9:16 upsell (1080x1920, 29.97), Dan on green screen over
Wood Kitchen 1, roll C1904 13:45-30:31.

## 0. Read first
- `~/Projects/_edit_work/WV-05/round1/ROUND-1-NOTES.md` (what is built, recipes, open items) and `round1/ROUND-1-REVIEW.md`.
- `film/recipe/` (edl_build.py, plates.py, graphics.py, captions.py, render_film.py, check_film.py, chain_*.sh), `key/` (chain_piece.sh,
  run_all.sh, pieces.json), `round1/review/` (make_inputs.py, build_page.py: reuse both).
- `.claude/skills/_shared/VIDEO-RULES.md` top sections, including **"funnel CTA = text with down arrows"** (Dan, 2026-11-19, on Upsell 4),
  `Handoffs/video-editing/WV-04-round-2-revisions.md` sections 1-2 (upsell style), `/ad-edit`, `PRE-RENDER-APPROVAL.md`,
  `CUT-CONTINUITY-QC.md`, `.claude/skills/_shared/cliplib/README.md` (every AI take is filed).
- **All 68 key pieces are keyed** (`key/logs/run_all.log` ends ALL_PIECES_DONE, 00:46 Nov 19). Never re-key a done piece.
- The round 1 page is still served on http://127.0.0.1:9877/. The blind key is `round1/frames/blind_key.json`; never put it on a page.

## 1. Dan's round 1 words (verbatim, 2026-11-19)
> Okay, first minute looks good. I do feel like, while we don't want to make this as busy as the main VSL, we don't want any frenetic fast cuts. I do think there are some things that we could add in, like an AI-generated clip of their bottles being packed. Clip to illustrate the complete head-to-toe transformation of the wife asking, "What the heck's gotten into you?" Basically, I want to see some options. Even if you aren't completely sure, I'll accept them. I think there's some room to add in a little bit more clips and graphics here, and I can always reject what doesn't make sense. Let's go with match color. Match or the house-based voice all graphics are looking good, but I'd like to see a few more options for clips and full-screen graphics without making the video excessively busy. Keep it trustworthy, but give me some more options so that it's not just so much straight camera scene. Proceed to the next round of edits.

Save them as `round2-plan/notes_r1.txt` and your reading as `round2-plan/decisions.json`.

## 2. Locked by Dan
- First minute (as cut), colour **Matched**, voice **House bass** ("Match or the house-based voice" = House bass, Wispr Flow), green-screen key.
- All 15 round 1 graphics approved ("all graphics are looking good"), EXCEPT the CTA below, which a newer standing rule replaces.

## 3. What to change
1. **CTA (standing rule, 2026-11-19):** replace the C01 "Accept Offer" button and the C02 pill with plain text plus pulsing down arrows,
   no button or pill shape. Dan says "click Accept Offer on the bundle you want", so use text like "Click Accept Offer Below" or
   "Click The Button Below To Try Eternal Burn" (title case; say which and why on the page). Keep it under the captions to the end.
2. **More options, not busier.** Dan wants less straight-camera time, still trustworthy, no fast cuts. Propose roughly 8-12 NEW options
   spread through the whole film (each lands on a key line, holds long enough to read, one at a time): AI clips as START/END pairs and
   new full-screen graphics (more study/fact cards, the AM and PM routine, ingredient cards for real Eternal Burn ingredients, a
   simple "how it works" card). He will reject freely. Never add a graphic over a cut that would make it feel hectic.
   - **Bottles being packed (he asked for it):** 0:07.9-0:15.0, "Your Great Again T is being packed for shipment as we speak ... before
     we seal up your box and send it out". A calm close shot of hands packing real Great Again T bottles into a shipping box. The label
     must match the real approved label (use the approved bottle renders as references; inspect every frame; regenerate any warped
     text). Consider a second pack shot at 8:46 ("It ships in the same box as your Great Again T") with Eternal Burn AM and PM added.
   - **Wives clip E02 (he asked for it):** 0:26-0:32. Its two picture pairs (X1/X2, both passed the gate and review) are on the round 1
     page; he did not pick one. Make motion for BOTH pairs on the subscription so he picks between moving takes. People clip: AI label on the picture.
   - **Drain clip E01** (2:12, frame pairs only): still open; offer it again with the new options.
   - New AI ideas go to Dan as START/END pairs first (two blind pairs each, gate + fresh frame-reviewer each), per the frame gates.
     Codex images: pace big batches (memory `codex-image-batches-exhaust-subscription`). Google Flow first for motion.
3. **Pauses (decision 3, not answered):** apply my recommendation as the default and say so on the page: restore the breath at the two
   paragraph breaks (0:13.1, 0:37.9) and the inhale cut short at 0:57.0, keep the rest tight. Also end the film's last words cleanly (reviewer D6).
4. **Garcinia photo (decision 6, not answered):** keep A (in the film) and offer B again.

## 4. Deliver
- Edit slot: `editcap.py acquire WV-05` first (M6). ETA: `eta.py plan WV-05 ...` then `eta.py step` per step.
- Render the **full film** (draft) with everything locked plus every new full-screen graphic option in place, AI slots on camera until
  picked (or a picked moving take where Dan's choice exists). Full checks (`check_film.py`), audio gate, seamscan of every join.
- Run an independent review (`ra-reviewer`, fresh agent) before Dan sees it; fix what it finds.
- Review page (reuse round 1's builder): film in the side player loaded at start; decisions on top; each new option in context with a
  Keep/Reject note; E02 moving takes side by side; new AI pairs; "What I decided". Test at 800 and 1150 px in silent check mode, hand off.
- File every generated AI take (clip library rule) before pausing for review. Then `editcap.py release WV-05 --review`,
  `queue.py set WV-05 delivered` plus the artifact db mirror, board line, `safe-push.sh`, wrap-up boxes.
- Delivery gate (`deliver/gate.py --format ad9x16`) needs a gate plan before the FINAL export; not required on this draft.
