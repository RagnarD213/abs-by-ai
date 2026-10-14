AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `How AI Real Abs AD R3`.

# RA-05 "How AI Can Get You REAL Six Pack Abs": round 3 (after Dan answers the round 2 page)

**Written 2026-10-14 by the round 2 session (Claude, Opus 5.5).** Do not fire before Dan has replied to the round 2 page
**http://127.0.0.1:8808/** (managed review service, folder `/Volumes/Extreme/_edit_work/ra05/round2/review/`). His reply goes,
word for word, into `/Volumes/Extreme/_edit_work/ra05/round3-plan/decisions.json` first (shape: `../round2-plan/decisions.json`).

Read: this file; `.claude/skills/ad-edit/reference/ra05/round2/README.md` (stage order, seven lessons); `/ad-edit`;
`.claude/skills/_shared/VIDEO-RULES.md` (first sections: whole short in one round, AI clip sense checks); `_shared/PRE-RENDER-APPROVAL.md`.
Round 1 record (take map, traps): `handoff-20261013-ra05-round2-after-dan-review.md`. Work dir: `/Volumes/Extreme/_edit_work/ra05/round2/`
(build round 3 in a new `round3/` beside it; never overwrite `round2/review/`).

## What round 2 built (all on the page)

- **Every line kept, the whole ad at 1.06x** (Rubber Band, pitch and formants kept): 61.0 s of talk to 57.51 s, plus the 0.85 s end
  hold at normal speed = **58.36 s (1,749 frames)**. Audio gate PASS on the frame-locked mix (-14.2 LUFS, -2.4 dBTP, tone max 2.24).
- **Opening (0 to 3.47 s):** B0049 as a fast cut: photo added (3.05-3.45 s, real time), Peak tapped and Generate pressed (7.25-7.98,
  1.4x), loading in two jumps (9.65-12.40 and 13.20-24.40), then the result alone from 28.0 s for 1.53 s. AI-GENERATED only on the
  result. Every frame checked: no crop screen, no "Meet the new you", no email form.
- **Couch clip "Steps out of the phone" (3.47 to 7.91 s), FRAMES ONLY.** START `frames/couch_START.png`
  (sha256 4d4773381a6c431490ca09208c2ba4ee790a06a8f6dec6fdd2a048f3e079451f), END `frames/couch_END.png`
  (sha256 54315a6a0af8a97d844cadf6dc0b1f980b989d518de6afac01eb0a47d129989d, derived from START, second take). Cut at 5.77 s
  ("six-pack abs in real life"), moved from the handoff's "in real life" so the END shot runs 2.1 s. Prompts:
  `reference/ra05/round2/frame_prompts/`. The page plays it as a labelled START/END placeholder.
- **A1** Soft Blue HyperFrames analysis card 14.08-18.52 s (rows on "exactly", "right now", "where you want"; band 18.00).
- **SCAN** A0044 body scan 25.99-29.96 s, x 150-1770 full height, hole [36, 510, 1044, 1182], from clip 1.0 s, natural speed,
  AI-GENERATED under it. Callout words about 16 px tall on 1080x1920 (said on the page).
- Unchanged from round 1, retimed only: LT1, K1 (A0074), T1 (B0544), LT2, B2 poses (46.95-50.52), CTA button (51.45 to end).
- Look locked from RA-14: framing 648x1152 / 810x1440, colour C2 brighter gold re-baked for C1664, voice + `equalizer=f=120:t=q:w=0.8:g=+3.0`.

## Dan's four decisions on the page

1. Couch START/END frames: approve for motion, or changes (new frames, show again, no motion).
2. The new opening: approve or changes.
3. The body scan card: approve or changes.
4. Speed: keep 1.06x (58.36 s, recommended) or 1.05x (58.9 s). For 1.05x: `SPEED = 1.05` in `ra01lib.py`, then stages 2 to 9 of
   the round 2 README (every time in the plan moves; nothing is reused).

## Round 3 work, in order (only what his answers allow)

1. Re-hash the round 2 files below; record expected against actual.
2. **Couch motion, only if he approved the frames:** two separate takes joined by a CUT, never a morph: shot A from START (about
   2.3 s used: he holds the phone up, a small turn of the screen toward the camera, settles into a half smile), shot B from END
   (about 2.1 s used: he grins, holds the phone beside his abs, a small proud nod). Replicate `google/veo-3.1-fast`, image only
   (no `last_frame`: they are separate shots), 9:16, 4 s, no audio, about $0.40 each. Template:
   `.claude/skills/longform-edit/reference/ro06/gen_motion.py` (assert both frame sha256s above; ledger every call). Prompts: plain
   actions, Step 4.5 vocabulary, "camera stays still", no lettering, nothing appears or vanishes. Budget: **$10 for this ad, $0 spent**.
   Retakes of approved frames need no question inside the cap.
3. **Check every take before Dan sees it moving** (VIDEO-RULES 2026-10-13/14): the measured self-change map
   (`longform-edit/reference/ro08/a5_cut.py`) and the three sense questions, by you and by a fresh independent reviewer with the
   questions in its brief. Fix a failure by retake or trim, never by describing it.
4. Swap the placeholder for the motion (`s06_inserts05.py` couch branch reads frames; add a clip branch: fill the frame, chip top left
   clear of his face), re-render (`s10_render05.py`, `SKIP1=1` if no hold changed), re-lock the mix.
5. **Then the WHOLE 9:16 on the page**, not 30 s (VIDEO-RULES 2026-10-14: nothing new remains after the couch clip). Before it:
   print his mouth frame by frame after the last word (RA-14 round 4 lesson 1) and end on the held pose; `s04b_holdstart.py` +
   the land-then-hold check; `piccuts.py decide`; `junk.py` on the final cut; watch the joins after 30 s (two frames either side, as
   round 2 did for the first 30). Copy the full review file to `Videos to Review/` (it is over 45 s).
6. After Dan approves the whole 9:16: the delivery list in the round 1 handoff, "Next action" item 5 (edit sheet, gates, watch pass,
   independent review, 16:9 from the same edit, delivery folder, queue status, clip library `add --used-in "RA-05"`).

## Risks, stated plainly

- Dan's face first appears at 7.9 s. If he finds it slow, the page's fix: start the couch clip at "in real life" and put him on camera
  for "but now guys are using AI". Not changed unasked.
- The speed-up is detectable when played beside the normal-speed version (blind listener, 5 of 5); on a single listen it was judged not
  noticeable. Gemini also claimed "smeared consonants" for every stretch method alike, which the measurements do not support.
- Lip sync measured inside one frame (source-frame matching); a Gemini watch claimed a 0.1 s lead, which that test does not support.
- The opening's first 0.4 s shows the man's real heavy before photo (his choice, same recording as the approved RA-01 and Ad 1).

## Files (work dir `/Volumes/Extreme/_edit_work/ra05/round2/`, sha256 first 16)

| file | sha256 |
|---|---|
| `review/DRAFT - RA-05 round 2 - first 30 seconds.mp4` (31.70 s) | 5d059813336a5d8d |
| `draft_9x16.mp4` (internal full draft, not shown) | 21266d833150148b |
| `picture_9x16.mp4` | af10305ff5102cc8 |
| `mix.wav` (frame-locked, gate PASS) | 3857ef27e0e39167 |
| `cut.json` (film time, speed 1.06) | 3e7410a0fb7d2a2e |
| `cut_tight.json` (normal speed) | fceffe9c53ce99f5 |
| `beats.json` | abcd7f8ea2b57809 |
| `words_aligned.json` | 158afa843fe886ee |
| `framing.json` | 39e2d193414d84d1 |
| `hf9/manifest.json` | 279afccecef1ce88 |
| `hf9/plates.json` | 09a23bd5fac8b078 |
| `cards_9x16/open.mp4` | ad11958532e154b4 |
| `cards_9x16/scan.mp4` | 0e3c98baa93a31e2 |
| `cap_9x16/captions.mov` | c29ac42adebd3d17 |
| `review/index.html` | 439dc30af1c3964f |

Cost ledger: $0 of $10. Codex subscription: 3 images (START, END take 1 rejected for the sweatpants texture, END take 2). Gemini
listening checks about $0.10 (standing authorization).

## Starter prompt (paste into a fresh Claude Code session)

> AD. Rename this task `How AI Real Abs AD R3`. Read `Handoffs/handoff-20261014-ra05-round3-after-frames.md` and continue RA-05
> "How AI Can Get You REAL Six Pack Abs" with /ad-edit. My answers to the round 2 page are: [paste the reply box]. Record them word
> for word first. If I approved the couch frames, make the two couch shots (check every take for sense before I see it), then build the
> WHOLE 9:16 and show it to me on one page with the couch clip moving in context. Write the round 4 handoff and stop.

**Recommended model and effort: Opus 5.5, high.** Two short AI takes with checks, then a recipe-backed full render.
