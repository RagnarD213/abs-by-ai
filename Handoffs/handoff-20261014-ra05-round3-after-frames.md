AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `How AI Real Abs AD R3`.

# RA-05 "How AI Can Get You REAL Six Pack Abs": round 3 (Dan has answered round 2)

**Written 2026-10-14 by the round 2 session (Claude, Opus 5.5).** Dan answered the round 2 page (http://127.0.0.1:8808/) the same day.
His words, per item, with hashes: `/Volumes/Extreme/_edit_work/ra05/round3-plan/decisions.json` (repo copy
`.claude/skills/ad-edit/reference/ra05/round3-plan-decisions.json`). Fire this now.

Read: this file; `.claude/skills/ad-edit/reference/ra05/round2/README.md` (stage order, seven lessons); `/ad-edit`;
`.claude/skills/_shared/VIDEO-RULES.md` (first sections: whole short in one round, AI clip sense checks, squares and verticals fill the
frame); `_shared/PRE-RENDER-APPROVAL.md`; `_shared/GRAPHICS-STANDARDS.md` + `SOFTBLUE.md` for the new callouts. Round 1 record (take map,
traps): `handoff-20261013-ra05-round2-after-dan-review.md`. Work dir: `/Volumes/Extreme/_edit_work/ra05/round2/` holds every round 2 input
and script; build round 3 in a new `/Volumes/Extreme/_edit_work/ra05/round3/` (copy, as round 2 did from round 1). Never overwrite
`round2/review/` (Dan's page).

## What Dan decided (2026-10-14, on the round 2 page)

1. **Couch clip frames APPROVED, motion authorized** (*"Start and end frames for the couch clip are approved."*). START
   `round2/frames/couch_START.png` sha256 4d4773381a6c431490ca09208c2ba4ee790a06a8f6dec6fdd2a048f3e079451f, END
   `round2/frames/couch_END.png` sha256 54315a6a0af8a97d844cadf6dc0b1f980b989d518de6afac01eb0a47d129989d.
2. **Opening APPROVED as built** (*"Everything in the new opening looks good."*): `round2/cards_9x16/open.mp4` and `s06_open.py`. Locked.
3. **Body scan: keep it, rebuild it VERTICAL** (*"For the start frame VSL clip, I would like you to essentially reproduce this in a vertical
   format so that his body occupies the full vertical frame. You can put the notes maybe on the top or the bottom. I like that body scan
   there, but I want it in a vertical format."*; "start frame VSL" read as the /start VSL, a Wispr slip).
4. **Speed 1.06x APPROVED** (*"Yes, we can keep the 1.06x speedup."*): 58.36 s, 1,749 frames, `round2/mix.wav` (frame-locked, gate PASS).

Everything else on the page got no note (A1 Soft Blue analysis card, LT1, LT2, K1 lock screen, T1 app tour; and after 30 s the B2 poses,
the CTA button, the end hold). Treat them as kept, not as approved in words.

## Round 3 deliverable: the WHOLE 9:16 on one page, then stop

Nothing unseen remains once the couch motion passes its checks and the vertical scan is built, so this round shows the whole ad
(VIDEO-RULES 2026-10-14), with the couch clip and the new scan also as items moving in context.

1. **Re-hash** the round 2 files (table below), expected against actual, before touching anything.
2. **Couch motion:** two separate takes joined by a CUT, never a morph. Shot A from START (used 3.47 to 5.77 s film, 2.3 s: he holds the
   phone toward the camera, a small turn of the screen, settles into a half smile); shot B from END (5.77 to 7.91 s, 2.1 s: he grins,
   holds the phone beside his abs, a small proud nod). Replicate `google/veo-3.1-fast`, image only (no `last_frame`: two shots), 9:16,
   4 s, no audio, about $0.40 each. Template `.claude/skills/longform-edit/reference/ro06/gen_motion.py`: assert both frame sha256s above,
   ledger every call. Prompts: plain actions, ad-edit Step 4.5 vocabulary, "camera stays still", nothing appears or vanishes, the phone
   screen keeps the same picture, no lettering. Use the best-flowing part of each take; never slow or hold one.
3. **Check every take before Dan sees it moving:** the self-change map (`longform-edit/reference/ro08/a5_cut.py`) and the three sense
   questions (cause and effect; sound off, would a stranger get it; does it show "guys are using AI to get them six-pack abs in real
   life"), by you and then by a fresh independent reviewer with the questions in its brief. Also: hands (five fingers), the phone picture
   stays the same, the face stays the same man across the cut. A failing take is retaken or trimmed, never described on the page.
   Budget **$10 for this ad, $0 spent**; retakes of approved frames need no question inside the cap; ask first, alone, before passing it.
4. **The vertical body scan** (replaces round 2's boxed card, same slot 25.99 to 29.96 s, under "It will see exactly where you need to
   gain muscle, and tailor your workout program"). Source A0044 = `/Volumes/Extreme/_edit_work/wv01-edit/round4/motion/SCAN-readable.mp4`
   (1920x1080, 5.0 s, all four callouts up by 1.0 s). Measured at 2.0 s (person mask): he spans **x 694 to 1220, y 44 to 1079** (the frame
   cuts him at mid thigh). Recommended build, $0, in code:
   - **Picture:** a full-height 9:16 window **608 x 1080 at x about 653** (centred on him, about 40 px spare each side; land-then-hold, no
     pan), scaled to 1080 x 1920 full screen. That is a 1.78x enlargement: Real-ESRGAN is NOT installed here, so use Lanczos plus a light
     unsharp (RA-07 round 2 precedent, `ra07/round2/s75_clips.py`) and compare his face sharpness against the presenter's close shot at
     native size. If it reads soft, say so on the page and offer the fallback below; do not ship it silently.
   - **The leftovers:** the window keeps the ends of the original leader lines and their glowing dots on his body (shoulder, abs, side of
     the waist, head). Either attach the new callouts to those dots (preferred: the lines then point at what the clip already marks) or
     paint the stubs out. Check frame by frame that nothing dangles.
   - **The notes, Dan's words "on the top or the bottom":** redraw the four callouts as Soft Blue graphics, two at the top (over the
     background above his shoulders, clear of his face and hair) and two at the bottom (over his legs or shorts, ending above the caption
     line at y 1376), each with a thin line to its body point, landing one by one in the first second (or on the words "exactly", "where
     you need", "gain muscle", "tailor"). Same four texts, set in code, large enough to read on a phone (captions are 64 px; aim for 34 px
     or more). Title capitalization per VIDEO-RULES 2026-10-09, no full caps, no numbers. AI-GENERATED chip clear of his face and the notes.
     Show it first as a still on its real frame (the page's grid), then moving in context.
   - **Fallback, only if the enlargement is too soft:** a Codex 9:16 frame of the same scan scene (the 2.0 s frame as the reference, his
     body filling the frame, no text) plus one Veo take, about $0.40, frames shown to Dan first. Say this on the page as an option, do
     not make it unasked.
5. **Rebuild and render** (round 2 README stages 5 to 9, couch branch swapped from placeholder to the motion, scan branch swapped to the
   vertical card; `s10_render05.py` with `SKIP1=1` if no hold changed; re-lock the mix to the picture and re-run the audio gate).
6. **Before the page**, on the whole film: print his mouth frame by frame after the last word and end on the held pose (RA-14 round 4
   lesson 1); `s04b_holdstart.py` + the land-then-hold check; `piccuts.py decide`; `junk.py` on the final cut; two frames either side of
   every join after 30 s (round 2 did the first 30); captions after 30 s proofread against the audio; negative-imagery scan of the
   first 30 s. Copy the full-quality review file to `Videos to Review/` as `How AI Real Abs AD R3 - whole 9x16.mp4` (it is over 45 s).
7. **The page** (round 2's `page_r2.py` is the template; new folder `round3/review/`, a new port): the whole 9:16 on top, then the couch clip
   and the vertical scan as items moving in context, "What I decided", a short decisions list (approve the whole ad; approve the couch
   motion; approve the vertical scan), one reply box. Listen to and watch it once more before sending.
8. Write the round 4 handoff and stop. After Dan approves the whole 9:16, round 4 is delivery: the list in the round 1 handoff, "Next
   action" item 5 (edit sheet, delivery gate, watch pass, independent review, the 16:9 from the same edit, delivery folder
   `Claude Ad Videos/how ai can get you real six pack abs - RA-05/`, queue status, clip library `add --used-in "RA-05"` for the couch clip
   and the vertical scan).

## Risks, stated plainly

- The vertical scan is a 1.78x enlargement of an AI clip; it may read softer than the presenter. The fallback costs a frame round.
- Dan's face first appears at 7.9 s (opening, then couch). He did not comment; leave it.
- The speed-up is detectable beside the normal-speed version (blind listener); approved by Dan regardless.

## Files (work dir `/Volumes/Extreme/_edit_work/ra05/round2/`, sha256 first 16)

| file | sha256 |
|---|---|
| `review/DRAFT - RA-05 round 2 - first 30 seconds.mp4` (what Dan reviewed) | 5d059813336a5d8d |
| `draft_9x16.mp4` (internal full draft) | 21266d833150148b |
| `picture_9x16.mp4` | af10305ff5102cc8 |
| `mix.wav` (frame-locked, gate PASS, Dan's 1.06x) | 3857ef27e0e39167 |
| `cut.json` (film time, speed 1.06) | 3e7410a0fb7d2a2e |
| `cut_tight.json` (normal speed) | fceffe9c53ce99f5 |
| `beats.json` | abcd7f8ea2b57809 |
| `words_aligned.json` | 158afa843fe886ee |
| `framing.json` | 39e2d193414d84d1 |
| `hf9/manifest.json` | 279afccecef1ce88 |
| `hf9/plates.json` | 09a23bd5fac8b078 |
| `cards_9x16/open.mp4` (approved) | ad11958532e154b4 |
| `cards_9x16/scan.mp4` (replaced this round) | 0e3c98baa93a31e2 |
| `cap_9x16/captions.mov` | c29ac42adebd3d17 |
| `review/index.html` | 439dc30af1c3964f |

Cost ledger: $0 of $10. Codex subscription: 3 images so far. Gemini checks about $0.10 (standing authorization).

## Starter prompt (paste into a fresh Claude Code session)

> AD. Rename this task `How AI Real Abs AD R3`. Read `Handoffs/handoff-20261014-ra05-round3-after-frames.md` and run round 3 of RA-05
> "How AI Can Get You REAL Six Pack Abs" with /ad-edit. My answers are already recorded in
> `/Volumes/Extreme/_edit_work/ra05/round3-plan/decisions.json`. Make the two couch shots from my approved frames and check every take
> for sense before I see it, rebuild the body scan vertical with his body filling the frame and the notes on the top and bottom, keep
> 1.06x, then build the WHOLE 9:16 and show it to me on one page with the couch clip and the new scan moving in context. Write the round 4
> handoff and stop.

**Recommended model and effort: Opus 5.5, high.** Two short AI takes with checks, one new code-built card, then a recipe-backed full render.
