# Handoff — Ad 5 vertical (Muhammad V3) — Dan's round-2 revisions

**Written 2026-09-12 by the session that executed round 1. Dan watched the round-1 re-delivery and asked for two changes.
He asked for a handoff rather than execution, so nothing here is built yet.** Delete this doc's entries (here,
`Handoffs/README.md`) when the re-delivery is in the folder.

## What exists

| | |
|---|---|
| build dir | `/Volumes/Extreme/_edit_work/ad5-vert/` — the Python compositor (`beats.py` → `render5.py` → `zmux.py`), every gate, three audits, the recipe |
| delivered | `Muhammad Ad Videos/every diet you've tried failed for the same reason - ad 5/… \| claude \| 9x16 \| ad 5.mp4` (7,036 frames = his) and `… \| 9x16 59s \| ad 5.mp4` (54.92 s), review copies, A/B audio, stamps, `notes-vertical.md`, `recipe-vertical/` |
| round 1 | every real after picture full-bleed portrait + the "Real picture of me — not AI-generated" chip; the two landscape stills replaced; the photo panel replaced by two studio shots. `qc.py` 20/20 both, corpus 19/19, audits 4/5/6 |
| skill | `/shortad-from-longform` — read **[A9]** first (round 1's twelve lessons), then [A7] and [A8]. `reference/zpick.py` picks after pictures on the RENDERED crop; `reference/plan_build.py` builds the delivery gate's plan |
| audio | **Muhammad's, untouched** — the master carries his AAC stream bit for bit (`zmux.py` asserts the md5 = `ed5c8da0…`), the cutdown his mix cut only. **Nothing in these revisions touches audio.** |

## Dan's two revisions (his words, 2026-09-12)

> "At the very end of the ad, it starts the generation with another Asian guy, the AI-generated guy, but then ends on me.
> In this part of the ad, I wanted to end on the correct before-and-after picture for that Asian guy that we have. Use his
> before-and-after picture, not mine. **Generally, going forward, don't mix before-and-after pictures. It should be the same
> person in the before and after.** That doesn't really make sense if you change the person."

> "For the pictures of me, I want to apply the 'real picture of me' label to all of these pictures. Right now, you have it
> not on one set of the pictures, the studio pictures later in the video. Where you do have it, **it's blocking my abs**. I
> want to put it **above my head**, make this label **a little bit larger**, and **more noticeable**. Put the label above my
> head or somewhere it doesn't block my face or my abs. Make it larger and more noticeable, and put it on **all** the
> pictures, not just the first set. All the pictures that are real, not the AI-generated goal picture, but all the real pictures."

**The standing rule from the first quote is already written** (2026-09-12, by the session that wrote this doc): "A before
and after picture are the SAME PERSON" is in `AGENTS.md` and in `/shortad-from-longform`, `/ad-edit`, `/longform-edit`,
`/shorts`, `/website-video`, `/make-ad`, `/revisions`, `/imagesandclips`. Nothing to do here except follow it.

---

## Item 1 — the app demo must end on the SAME man it started with (6716–6954)

**What it does now.** The beat plays the real app recording `09_CLIP_app-generate-future-self.mp4` (frames 6716–6905),
which uploads **a heavier Asian man who is not Dan**, and then at `result_n = 6905` cuts to a rebuilt result screen showing
**Dan's** AI goal image (`01 Before and After Images/dan by pool - AI GOAL IMAGE.png`) under "YOUR GOAL IMAGE". So the
before is one person and the after is another — exactly what Dan is calling out.

**⚠ His after picture does not exist yet.** The library's only before/after pairs are `male-before/after.webp` and
`male2-before/after.webp`, and **both are white men** — neither is the man in the recording (checked 2026-09-12). So this
cannot be solved by swapping in an existing asset.

**The method, and it is a standing rule of this skill (A5.23):** *an app screen with a different person is a REAL
GENERATION, never a composite.* Dan rejected a pasted-in before photo within minutes once. So:

1. Pull **his before photo at full resolution** out of the recording — the upload/adjust screen is on screen around
   3:44–3:47 (master frames ~6716–6800). Extract **by index** (`select='eq(n,N)'`, `-fps_mode passthrough`), take the photo
   inside the phone's own crop box, and keep it at the largest clean size the recording gives.
2. **Run a real generation with that photo** through the live site, exactly as `reference/record_gen_male2.py` does:
   Playwright, iPhone emulation, `set_input_files`, handle the "Which future you?" chooser by clicking the first
   "Keep this one", then capture the result screen **AFTER-ONLY** by hiding the before column and the body-fat row in the
   live DOM (`grid-template-columns:1fr`, `display:none`). One generation costs ~$0.10 and a fresh Playwright context has
   free generations — inside the standing spend authorization. **Never pass a `deviceId`.**
3. Rebuild the result screen from **the app's own rendering** of that man's result, in the same layout the current
   `assets/app_result.png` uses (page header + the image at the screen width, 40.5 % down, email form out of frame —
   the A8.11 recipe), and keep the **AI-GENERATED** chip on it: it is an AI image, just of him rather than of Dan.
4. **Do not use the before/after pair screen and do not show the chooser** — both are banned layouts (standing content
   rules). After-only, as now.

**If the generation cannot be made to work on his photo**, the fallback is the one Dan set for the rest of this batch on
09-10: re-record the demo with **Dan's own** before picture (`00 ASSETS USED IN THE REFERENCE AD/02_BEFORE-PICTURE_dan-200lb.png`,
his Ad 14 form of words) so the demo is Dan → Dan and still one person. **Ask Dan before taking the fallback** — he said
"use his before-and-after picture, not mine", so it is a change of his instruction, not a judgement call.

⚠ This same recording is the app demo in **Ads 6, 8, 9, 10, 13, 14, 15** of Muhammad's batch and in the Ad 3 / Ad 4
verticals. Fixing it here does not fix those; say so in the delivery note so Dan can decide whether the batch gets the
same treatment.

---

## Item 2 — the real-picture label: on every real picture, larger, off his face and abs

### 2a. It goes on six more beats, and one beat is labelled wrongly today

The chip is currently on the seven `bleed` beats only. Every real photograph of Dan in the cut:

| frames | seconds | what | label now | label wanted |
|---|---|---|---|---|
| 138–211 | 4.60–7.04 | deckchair BEFORE (card, blur-in) | none | **real** |
| 280–392 | 9.34–13.08 | fat-dad standing (card) | none | **real** |
| 392–439 | 13.08–14.65 | fat-dad on the ride (card) | none | **real** |
| 439–449 | 14.65–14.98 | SHOT4 pool (bleed) | real | real, moved + bigger |
| 449–459 | 14.98–15.32 | SHOT3 towel (bleed) | real | real, moved + bigger |
| 459–469 | 15.32–15.65 | photo-221 (bleed) | real | real, moved + bigger |
| 469–500 | 15.65–16.68 | photo-247 (bleed) | real | real, moved + bigger |
| 1035–1194 | 34.53–39.84 | deckchair BEFORE inside the WHY DIETS HAVE FAILED YOU card | none | **real** |
| 2133–2209 | 71.17–73.71 | fat-dad on the ride again (card, blur-in) | none | **real** |
| 2605–2763 | 86.92–92.19 | his own clip, heavier, looking at the phone | **AI-GENERATED** | **see below** |
| 3549–3582 | 118.42–119.52 | studio grey (bleed) | real | real, moved + bigger |
| 3582–3616 | 119.52–120.65 | studio white (bleed) | real | real, moved + bigger |
| 6360–6425 | 212.21–214.38 | SHOT4 pool (bleed) | real | real, moved + bigger |

**Note for Dan, do not guess:** the label IS on the studio pictures in the delivered file — verified at frames 3560 and
3600 of the delivered master on 2026-09-12. If he still sees it missing there, he is looking at an older copy; check with
him rather than "fixing" something that is already right.

**⚠ 2605–2763 is a judgement call for Dan.** That beat is REAL footage of Dan, heavier, holding a phone; it carries the
AI-GENERATED chip because his own oblique caption under it reads "AI PICTURE OF MYSELF WITH THE BODY I WANTED" — the AI
thing is the picture **on the phone**, not the man. Under Dan's rule ("every picture of Dan's physique carries exactly one
of them") the footage of *him* should read **real**, but then a frame showing an AI image would carry a "not AI-generated"
label. **Recommendation: carry the real chip on it and leave the AI wording to the existing caption**, and flag it in the
delivery note. Do not silently pick either way.

**Cards vs full-bleed.** Six of the newly-labelled beats are `card` / `why` / `fatdan` — the media sits in Muhammad's olive
card, not full frame. The chip must sit **inside the card's media hole** (the same place the AI chip sits on a card), not
floating on the field, or it reads as a caption rather than a label on the picture.

### 2b. Placement — "above my head" is not available on these crops, and here is why

The pool and studio sources are 2747×4096 and 3368×5056 (both ≈ 0.67), cover-cropped to 9:16, so **only width is cropped —
the full source height is already on screen** and no headroom can be added. Measured on the delivered master: Dan's hair
top sits ≈ **135 px** from the frame top on the studio shots and ≈ **170 px** on SHOT4. The Shorts/Reels top safe area is
y ≈ 150. So a chip genuinely above his head would have to live in the 0–135 px strip, **inside the platform's own UI band**.

**What to build instead, and it meets his stated test ("doesn't block my face or my abs"):** put the chip in a band just
under the top safe line, **top edge y ≈ 160**, centred. On these pictures that lands over his hair and the background
above his shoulders — never his face, never his abs. Verify per picture with `rc/personmask` + `rc/anchor.py`: the chip's
bottom edge must sit **above the top of the face band** on every frame of the beat. Where a picture's head sits too high
for that (measure, do not assume), fall back to the largest person-free region in the upper third — beside his head over
the background — and say which pictures took the fallback.

### 2c. Size — and the constraint that decides the design

Measured with the build's own Manrope SemiBold against a usable width of 1080 − 2×44 = **992 px**:

| one line | chip width | | two lines ("Real picture of me" / "not AI-generated") | chip width |
|---|---|---|---|---|
| 44 px (today) | 833 | fits | 56 px | 520 |
| 48 px | 907 | fits | 64 px | 590 |
| 52 px | 976 | fits (2 px of slack) | 72 px | 659 |
| 56 px | 1044 | **too wide** | 80 px | 730 |

So "larger" on **one line** tops out at **52 px** — a 18 % increase, which is not much more noticeable. **Recommendation:
set it on TWO lines at 64–72 px**, which is a 45–64 % increase in cap height, is far more legible on a phone, and leaves
300+ px of horizontal margin. Render one candidate of each (52 one-line, 64 two-line, 72 two-line) as stills on three
different pictures and look before committing.

"More noticeable" beyond size: options in Muhammad's own language are a higher chip opacity (it is 215/255 today), an
**olive tab** down the leading edge like his lower thirds, or olive type on the black chip. **Pick one, do not stack all
three**, and keep it visually distinct from the AI-GENERATED chip so the two never read as the same badge.

⚠ `g5.real_chip` is **shared with the Ad 4 vertical** (`reference/a8_ad4/g8.py` imports g5). Changing size and placement
there changes Ad 4's delivered look too. Either make the new placement the default for both (and say so, so Ad 4 gets
re-delivered when Dan next asks) or add the new geometry as parameters with the Ad 5 build passing them. **Recommend the
former** — Dan's instruction is about the device, not about this one ad.

---

## Then

1. `python3 render5.py --out picture.mp4` → `python3 zmux.py picture.mp4 ad5_vertical_9x16.mp4` (asserts his audio md5).
2. Every gate on the exact files: `audio_gate.py … --reference-mix his_mix.wav --verbatim --ab …`, `watch.py` +
   `zwatch_sheets.py`, `caption_sync_check.py`, `zhairgate2.py`, `landing_check.py`, then `reference/qc.py … --build-dir .`
   (20/20). **⚠ The chip moving to y ≈ 160 puts it inside the hair band `zhairgate2.py` measures — check that the gate is
   reading hair and not the chip, and if it is confused, that is a finding to fix properly, not a bound to loosen.**
3. The cutdown: `python3 zcutdown.py && python3 zcut_build.py`, `render5.py --cutplan cut_plan.json --out cut/picture.mp4`,
   mux with `cut/his_mix.wav`, the same gates from **inside** `cut/`.
4. `_shared/deliver/gate.py` on both, with `plan_build.py` regenerating `plan.json` (run it from inside the dir it is for).
   Round 1 left it at master 26/2, cutdown 27/1 — **the two `cut:min_segment` failures (5- and 3-frame framing segments at
   68.60 s and 133.17 s) are pre-existing in the approved crop; this is the round to fix them if Dan wants** (merge each
   stub into the hold before it in `crop.json`; do NOT re-run `zcrop`).
5. **Two independent Fable audits (Step 7b), and expect the first to say "does not ship"** — on round 1 the first two
   audits each found a real defect after 20/20 gates, and the third found a one-frame defect the second round's fix had
   introduced. Give them the changed spans and ask specifically: the label on every real picture and no AI picture, never
   over a face or abs, legible at 1:1; the app demo's before and after are the same man; nothing else in the film changed.
6. `python3 deliver5.py`, update `notes-vertical.md` with a "Round 2 (2026-09-12)" section, send Dan the 540p review
   copies, update the coordination entry, and delete this handoff from `Handoffs/README.md` and the HANDOFFS section.

## Traps specific to this build (read [A9] for the rest)

* **Re-render the whole master, never splice the changed spans** — the gray-trace diff against the previous render is what
  proves the change set, and on all four round-1 renders it came back as exactly the intended spans.
* **`-ss` time seeks land on the wrong frame on these masters** — extract by index.
* **Odd-width raw frames shear** — keep every media size even.
* **A caption plate is drawn only on `bleed` frames** (`render5.PLATE_FRAMES`). If a newly-labelled `card` beat also carries
  captions over bright media, it may need the same plate — check, do not assume.
* **The label chip and the caption plate must not collide**; the plate is caption-sized around y 1385–1523.
* `zcrop.py`'s measurements are build-specific — do not re-run it, the EDL is unchanged.
* The watch scan's one "unexplained jump" at 225.19 s is the app recording's own screen change — expected.

## Starter prompt (Opus, high)

> Execute `Handoffs/handoff-20260912-ad5-vertical-revisions-round2.md`: Dan's round-2 revisions on the Ad 5 vertical
> (`/Volumes/Extreme/_edit_work/ad5-vert/`) — (1) the app demo at the end must show the SAME man in the before and the
> after (his after has to be generated through the live app, it is not in the library), and (2) the "Real picture of me —
> not AI-generated" label goes on EVERY real picture of Dan (six more beats), moved off his face and abs to just under the
> top safe line, and made larger (two lines at 64–72 px is the recommendation). Muhammad's audio untouched. Load
> `/shortad-from-longform` first and read [A9]. Render, every gate on the exact files including `_shared/deliver/gate.py`,
> two independent audits, then `deliver5.py`, notes, board. Model: Opus, effort high.
