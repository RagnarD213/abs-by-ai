# RA-07 "Fire Your Trainer!": round 2 (after Dan's answers on the round 1 page)

**AD (short-form, filmed).** Sidebar name for the next task: `Fire Your Trainer AD R2`.
Written 2026-10-13 at the end of round 1 (Claude Opus 5.5). Job doc: `Handoffs/video-editing/RA-07-fire-your-trainer.md`.
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, the `/ad-edit` skill,
`_shared/PRE-RENDER-APPROVAL.md`, `_shared/IMAGE-GENERATION.md`, `_shared/CUT-CONTINUITY-QC.md`.

**Do not fire this until Dan has replied to the round 1 page** (http://127.0.0.1:8807/, folder
`/Volumes/Extreme/_edit_work/ra07/round1/`). Nothing in round 1 is approved yet. His reply goes, word for word, into
`/Volumes/Extreme/_edit_work/ra07/round2-plan/decisions.json` before anything is built.

## What round 1 put in front of Dan

1. **Three questions:** (a) the claim lines as spoken (they print in the captions, they are in no graphic): "Why are
   thousands of guys across America firing their personal trainer", "AI can do three things no human trainer can",
   "you'll get far better results than the generic program that a human trainer will give you"; (b) the opening:
   A (recommended) the library clip A0147 from frame 0 under the whole hook line, B Dan on camera first (what the
   sample shows); (c) yes or no to each of five AI clip ideas.
2. **Five AI clip ideas, START and END frames only** (`round1/frames/I1..I5-start|end.png`, made on the Codex
   subscription, $0): I1 The sad paper (18.85 to 22.99 s), I2 Same sheet for everyone (31.63 to 34.30), I3 Tweaked
   shoulder (36.47 to 38.54), I4 Out of order (40.44 to 42.11), I5 Back next week (43.94 to 47.01). One ordinary man in
   all five. Where he says no, the ad stays on Dan (levels for that are in `s60_plan.py` `HOLDS`).
3. **Every graphic and clip as a still:** H1 (A0147 hook clip), L1/L2/L3 (signposts "1 OF 3 / See Your Goal Physique",
   "2 OF 3 / A Program Built For Your Goal", "3 OF 3 / A Plan That Adjusts To Your Life"), P1 (approved
   self-generation demo, then its result), K1 (the goal picture as a lock screen, built in code, clock above his head),
   W1 and T1 (real AI Trainer screens, library B0034: the exercise sheet; the day's list with Swap links), M1 (library
   A0039, home workout), C1 (button "Tap The Button Below / Get Started").
4. **A 12.6 s opening sample** for the cut, captions and sound. ⚠ Its colour and framing are the OLD RA-01 ones.

## ⚠ Colour and framing come from RA-14, not from round 1

Dan reviewed RA-14 (The Cheat Code, same pool set, same day) on 2026-10-13: *"I want both the tight and the wide shot a
little bit wider. Both are a little bit too tight."* and *"I want to see some color correction options here. I feel like
we can do better with the color corrections."* RA-07's round 1 page tells him his RA-14 picks will be applied here and
that he is not asked twice. So:

- Read RA-14's latest decisions (`/Volumes/Extreme/_edit_work/ra14/round*-plan/decisions.json`, handoff
  `Handoffs/handoff-20261013-ra14-cheat-code-round2-after-dan-review.md` and whatever followed it).
- **Framing:** convert his picked pair to this roll by body landmark, not by pixel count. On C1664 Dan is RA-01's size
  (head 370 px, face 228 px wide, hair top about 1116 in the 2160x3840 frame); on RA-14's roll C1667 he is smaller
  (head 290, face 178). Round 1 here used RA-01's 594x1056 close and 702x1248 wide (2.85 and 3.37 head heights), which
  is TIGHTER than the RA-14 crops he called too tight (3.09 head heights close). Keep the exact 9:16 lattice
  (w = 18m, h = 32m), y0 = the hold's minimum hair top minus 4 % of the crop height, wide at least 1.10x the close.
- **Colour:** apply the grade he picks on RA-14, then check it on this roll's frames beside the RA-14 frames he approved
  (skin luma and saturation, then by eye). `grade.json` here is still RA-01's (LUT e1.15, saturation 1.25).
- **Voice:** RA-14 asks whether to add the +3 dB at 120 Hz bass lift on this set. Apply his answer. `mix.wav` here is
  the RA-01 chain (fitted tone, no dereverb, Realizer bed at -32), audio gate PASS 12 of 12, -14.1 LUFS.
- If RA-14 is still unanswered when this fires, do not guess: build the framing pair and colour candidates on RA-07's
  own frames and ask once, on this ad's round 2 page.

## Round 2 deliverable: one review page, then stop

Build in `/Volumes/Extreme/_edit_work/ra07/round2/`; serve on a free port (8807 is round 1, keep it).

1. Record his reply in `round2-plan/decisions.json` (per item: id, path, sha256, verdict, his exact words, scope, next
   action; `motion_authorized` for the AI ideas he said yes to).
2. Re-plan `s60_plan.py` for his opening choice and for every AI idea he turned down (`CARDS` status and the fallback
   holds), with the new crop sizes in `ra01lib.py` `Aspect.levels`.
3. **AI motion for the approved ideas only**, from their approved frames (ad budget $10 for the whole ad across all
   rounds, retries included; spent so far $0). Check every take with the three sense questions in VIDEO-RULES (cause and
   effect, readable with the sound off, shows the line) and frame strips of the first and last second. I3: the dumbbell
   must be lowered into his lap, never vanish. I4 and I5 carry generated signs: the lettering must stay readable and
   unchanged through the take. AI-GENERATED chip on every one, clear of faces.
4. Sharpen the two small library clips for full screen (A0147 is 720x1280, A0039 is 848x480): Real-ESRGAN locally, or
   the upscaled A0147 from the Ad 13 vertical build. Look at them at 1080x1920 before using them.
5. Run the cut QC that round 1 did not have a build slot for: `_shared/cut/junk.py` on C1664 with `cut.json`
   (stretched words flagged: "firing" 0.72 s, "now." 0.72 s), then `s25_hard.py` on the re-rendered opening and
   `_shared/cut/piccuts.py`. Three pause splices sit inside camera holds (13.01, 23.42, 35.07 s): each needs a size
   change or an insert. Holds that wander more than 6.6 % of the crop width (5.77 to 9.58, 9.58 to 12.58, 12.58 to
   14.95, 34.30 to 36.47 s) need the land-then-hold track (`_shared/cut/landing.py`).
6. Moving previews of every graphic and clip in context ("Play it moving, in context"), then **the finished first
   30 seconds** with his framing and colour. Listen and look before sending (a passed gate is not a listen).
7. Page, handoff for round 3 (full 9:16, then the 16:9 from the same cut, edit sheet, both gates, watch pass,
   independent review, delivery folder `Claude Ad Videos/fire your trainer - RA-07/`), then stop.

## Round 1 files (work dir `/Volumes/Extreme/_edit_work/ra07/`, sha256 first 16; re-hash before touching)

| file | what | hash |
|---|---|---|
| `edl_spec.json` | take map by phrase, with the reasons | 0b411437c8335156 |
| `tx/c1664.whisper.json` | word list, 372 to 460 s, two passes joined, three times corrected from the envelope | ae704fdd66930086 |
| `cut.json` | the cut: 51.89 s of talk, 16 pause cuts, one take seam at 47.01 s | d548aa837fe38410 |
| `mix.wav` | voice chain + bed, 52.685 s | a0c8e558e1e523ef |
| `words_aligned.json` | 183 words, CTC aligned to `mix.wav` | 0f3b808eed7bbedb |
| `framing.json` | head and hair track, 257 samples | ebe37beb873262e3 |
| `beats.json` | round 1 beat sheet (changes in round 2) | 1727ccf8492ee000 |

Scripts: `recipe/` in the work dir (copies of the RA-14 build's adapted RA-01 scripts, re-pointed at C1664, plus
`s63_cards07.py`, `tx/replicate_words.js`). Chains: `r1_chain_a.sh`, `r1_chain_b.sh`. Stage 1 of `s62_sample.py`
decodes the roll from 0 to 6:45 and took 11 minutes on a busy machine; `SKIP1=1` rebuilds only the cards and the join.

## What I decided in the cut (told to Dan on the page; he may overrule)

- Roll C1664, portrait, dual-mono lav (`pick_lav.py` measured on 394 to 439 s, inside these takes), room decay 24 ms.
- Hook: the second read. Head edge 389.95 s: 389.70 to 389.90 is an inhale, the word starts at 390.00.
- Body: one unbroken take, hook to "until next week" (389.95 to 441.61 s). Nothing cut from the script.
- CTA: the LAST take (450.14 to 455.62 s), "Tap the button below to take the first step". The first CTA take has a
  3.4 s stall inside "building".
- **End hold 0.80 s, not RA-01's 1.65 s** (`ra01lib.END_HOLD`): Dan holds his smile to about 456.5 s, then drops his
  hands and says "All right, let's break" at 457.1 s. Check the last frames by eye in the full film.
- Total 52.69 s (6.3 s under 0:59). Captions: the paper line is punctuated from the script (says "Goal: lose 20
  pounds"); "way. When" restored from the script.
- No analysis card in this ad (the line is about the workout program; real program screens instead). No AbsByAI.com
  mark or URL on the button (Dan's 10-01 rule; the job doc's September line asked for it and is overridden).
- When the EDL is final, run `roll_sidecar.py mark-used` for C1664's kept ranges.

## Cost ledger

AI generation: $0 (ten frames on the Codex subscription). Replicate transcript: two calls, under 1 cent each.
Cap for the ad: $10.

## Starter prompt (Opus 5.5, high)

> Read `Handoffs/handoff-20261013-ra07-fire-your-trainer-round2-after-dan-review.md` and run RA-07 "Fire Your Trainer!" round 2 with /ad-edit. Name this task `Fire Your Trainer AD R2`. My answers to the round 1 page are below; record them word for word first. Apply the framing and colour I picked on the Cheat Code ad (RA-14), generate motion only for the AI clips I said yes to, build the moving previews and the finished first 30 seconds, send me the review page, write the round 3 handoff and stop. Use the Codex subscription to generate any images.
>
> [paste your reply from the round 1 page here]
