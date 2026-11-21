# RA-01 "The AI Trick That Got Me Abs" — ROUND 1 REVIEW

Reviewer: independent (Fable 5.1), 2026-09-17. Read only: `AGENTS.md`, `00-RULES.md`, `RA-01-plan.md`, the two masters,
their four stamps, `gate_plan_9x16.json` / `gate_plan_16x9.json`, script lines 259–274, the named source assets, the
source roll C1663 (for crop and word checks) and the approved Ad 1 vertical. Did not read the editor's round file, notes,
watch-pass folders, `flux_diagnosis.json` or the delivery folder. All evidence is in
`/Volumes/Extreme/_edit_work/ra01/review-r1/` (paths below are relative to it).

Files reviewed:
- `master_9x16.mp4` sha256 `3e5e32bb…7132` — 1080×1920, 30000/1001, h264 High yuv420p bt709/tv, AAC 48 kHz 2 ch, 57.591 s, 1726 frames
- `master_16x9.mp4` sha256 `57cde3cf…3806` — 1920×1080, same, 57.591 s, 1726 frames

```
VERDICT: DOES NOT SHIP

DEFECTS (most serious first):

  D1  both files, whole file — stamps
      Plan §1/§6/§7 and AGENTS.md require a PASS audio_gate stamp and a PASS deliver_gate stamp on each delivered file.
      →  All four stamps are FAIL. audio_gate (both): row `artifacts` FAIL — "flux 0.090 (his 0.072) … both <= his x1.1"
         (limit 0.079). deliver_gate 2.1.0 (both): verdict FAIL, row `audio:stamp` FAIL ("AUDIO GATE FAILED … fix the
         audio, do not deliver"). sha256 and GATE_VERSION (2.1.0) are current, so these are valid FAIL stamps, not stale
         ones. Note for whoever decides: the stamp's own do_no_harm row shows the UNTREATED lav already reads flux 0.094,
         i.e. the chain improved it (x0.95) and the source itself is over the bound — that is an exception only Dan can
         grant (DS-17 precedent); it is not a pass.                                                  severity: blocker

  D2  both files 00:00.00–00:12.24 (and 00:25.14–00:32.09, 00:36.18–00:40.07) — captions / hook
      Plan §7: burned word-timed captions, "first 30 s proofed word for word"; approved Ad 1 vertical captions from
      frame 0 ("This picture got me" at 0:00, caption under every card).
      →  NO caption exists until 00:12.24 (first cue "it inspired me to"). L1–L4 — the entire hook, "This picture got me
         abs. And it's not even real!" — is never on screen. Captions are switched off under every card, so only ~12.6 s
         of the first 30 s is captioned, and cues restart mid-sentence with words dropped: 00:32.24 "it gave me a"
         ("Then" missing), 00:40.24 "me to work out." ("AI inspired" missing; Dan is on camera uncaptioned
         00:40.07–00:40.24). Muted, the first 12.6 s is a still picture with an AI-GENERATED chip and nothing else: the
         hook does not land. With sound, the first word starts at 00:00.25 (0.84 s of near-silence, −55 to −60 dBFS)
         where the approved reference speaks from 0.0 s.
         Evidence: sheets/s9_01.jpg, sheets/ref_01.jpg, caps/c_01.jpg, caps/d_01.jpg, caps/e_01.jpg, f9x16/n00000.png
                                                                                                      severity: major

  D3  both files, every talking-head hold — framing levels
      Plan §5 / locked standard: two levels only, NEAR = hair → belly button, FAR = hair → shorts line with the
      waistband in frame.
      →  Both levels are one notch too tight. Delivered "NEAR" ends below the pecs (belly button never in frame);
         delivered "FAR" ends at the belly button and the waistband is out of frame or on the last rows. Measured against
         the native roll: FAR crop ≈ 630×1120 px (hair y≈1140, navel ≈2080, waistband ≈2220 → crop bottom ≈2180);
         NEAR ≈ 850 px tall. Consequences: (a) in the 9:16 NEAR holds Dan's sway cannot be contained — face box reaches
         96.4 % of frame width at 00:16.05 and 98.2 % (ear on the right edge) at 00:45.18–00:45.24, face centre swings
         36 %→71 % inside one hold; (b) extra upscale on already soft footage — face Laplacian variance, RA-01 vs the
         approved Ad 1 vertical talking-head frames: native 12 vs ~20, phone-sized (360 px wide) 67 vs ~170, face
         normalised to 256 px 14 vs ~41. It reads visibly soft next to Ad 1.
         Evidence: pairs/levels_near_far.jpg, pairs/lean_4570.jpg, pairs/lean_1615.jpg, face_x_9x16.json,
                   src_view.jpg, pairs/sharp_ra01near_far_vs_ref.jpg, pairs/grid16_levels_pills.jpg   severity: major

  D4  both files 00:40.04–00:40.07 (frames 1203–1205) — macro-tracker beat tail
      Plan §4 L10: the itemized-results moment (food list + calorie total).
      →  The slice runs past it: at ≈00:39.25 the list recalculates (458 cal → 342 cal), "Log Meal" is pressed at
         00:40.03, and for the last 3 frames a DIFFERENT screen ("Today's total … Add a meal photo … ✓ logged") flashes
         before the cut to Dan. A 3-frame flash frame. Trim the slice to end before 00:39.2 of the delivered timeline.
         Evidence: pairs/macro_end_strip.jpg, pairs/p9_40.240.jpg                                     severity: major

  D5  master_16x9.mp4 00:19.14–00:21.03 and 00:54.16–00:55.29 — CTA pill
      Plan §4: a CTA pill, "Tap the button below" + AbsByAI.com.
      →  In 16:9 the pill is a ≈1800-px-wide solid black band across the whole frame with small centred text; at CTA 2
         it lies across Dan's neck and shoulders directly under his chin and hides the top of the physique. It reads as
         a letterbox error, not a pill. (9:16 pill is acceptable: 960 px, on the chest, clear of the face; its
         AbsByAI.com line is small, ≈20 px.)
         Evidence: pairs/grid16_levels_pills.jpg                                                      severity: major

  D6  both files, talking head throughout — skin colour
      Task check: skin natural; plan §0 asks exposure be chosen against an approved frame.
      →  Dan's cheek measures Lab a*/b* ≈ +10/+12 (chroma ≈16) against ≈ +17/+22 (chroma ≈28) on the approved Ad 1
         vertical at similar luma (L≈93 vs 91): about 40 % less colour. He looks grey-brown and flat beside the saturated
         AI image and the studio photos he is intercut with. Consistent shot to shot in hue; cheek luma ranges L 77–103
         across holds. No BT.601 shift (files tagged bt709; cards match their sources within ΔLab ≤ 5; app white 252/252/252).
         The plan forbids grade changes beyond exposure, so this is for the planner/Dan to rule on, but Dan will see it.
         Evidence: pairs/sharp_ra01near_far_vs_ref.jpg, sheets/s9_02.jpg                              severity: major

  D7  both files 00:07.03–00:07.16 — 13-frame flash of Dan
      Plan §4: before → other → after.
      →  Satisfied only technically: the BEFORE picture holds 0.83 s (00:06.08–00:07.03; Ad 1 held it ≈2.3 s), then Dan
         on camera for 0.43 s in a silent gap between "pounds" and "and", then the after pictures. It reads as a glitch,
         and the before picture is too brief to register.
         Evidence: pairs/EV_flash_dan_7.1s.jpg, pairs/p9_06.273.jpg, pairs/p9_07.541.jpg              severity: minor

  D8  master_9x16.mp4, every card — chip position / card field
      Plan §4: chips "inside the safe area"; cards "on the J2 field".
      →  Every chip sits at y = 60–122 px (top 3–6 % of 1920), the band platform UI occupies; the approved Ad 1 keeps
         its label on the picture. Cards sit on a blurred copy of the photo, not the J2 field. In 16:9 the chips
         straddle the card's top edge and the hook chip is offset left of the card while the end-card chip is centred.
         All chips are clear of face, hair and abs (checked at full resolution).
         Evidence: f9x16/n00000.png, pairs/chips9_scan.jpg, pairs/chips16_fullres.jpg                 severity: minor

  D9  both files 00:12.24 and 00:32.24 — caption casing
      →  Sentence-initial "it" is lowercase ("it inspired me to", "it gave me a"); every other sentence start is capitalised.
         Evidence: caps/c_01.jpg, caps/d_01.jpg                                                       severity: minor

  D10 both files 00:55.28–00:56.02 — tail audio
      →  After "below." the bed drops to −57 dBFS for ≈0.1 s and steps back to −41 dBFS within 5 ms at the 56.056 join
         (click ratio 1.78× the local ceiling; every other join ≤ 0.47×). Low level, but it is the one join that measures
         as a discontinuity. The music bed overall sits ≈ −46 dBFS (side −57): legal (≤ −30) but effectively inaudible.
                                                                                                      severity: minor

  D11 stamps — not_applicable reasons that do not fit this cut, and the watch pass
      →  9:16 `framing:no_wide_level` n/a "Dan sits in a full-width WINDOW above the text": not this cut (he is
         full-frame); harmless here (head ≥ 33 % of frame). 16:9 `framing:centering` n/a "editor's layout puts bullets
         left and Dan right": not this cut, and plan §5 names this row as one to satisfy — it was never measured by the
         gate. My measurement: 16:9 holds sit −0.1…+3.9 % off centre (all FAR holds lean +3.3…+3.9 % right), inside 6 %.
         `srt:*` n/a fits. 9:16 `watch:pass` was judged by "round-1 editor session" re-verifying a judge — not an
         independent pass (the 16:9 one names an independent judge).                                  severity: minor

CHECKED AND CLEAN:
  §1 container: both 57.591 s ≤ 59.00, sizes/fps/codecs/pix_fmt as specified, bt709 tagged, last frame is the held end
     card (luma 85 / 59, not black), first frame is the AI card. 16:9 audio stream md5 identical to 9:16 (1f6ac654…).
  §2 take map: my own Whisper pass of the delivered audio vs my pass of C1663 25–97 s: L1–L14 all present, in order,
     194/194 words match, L5 t2 used, false start and L5 t1 gone, L11 kept. Spoken drift only where Dan said it
     ("200 pounds", "the exact same way that I did", "It gave me"). No drug names.
  §3 length: nothing cut, no speed ramp evident, both CTA lines intact.
  §4 cue map: AI image on L1/L2/L4 with AI-GENERATED; BEFORE on "200 pounds" (= 01_LIGHT_plus8lb, no chip per plan);
     three distinct after photos = studio-blue-10, studio-gray-41, studio-white-90 (feature-matched to the files, none
     in Frowning Photos/), one at a time, each with the "Real picture of me — not AI-generated" chip above his head;
     no real-picture chip on moving footage; stats scan on Dan's own AI image with AI-GENERATED, bars only, no numbers;
     macro tracker shows the itemized list and total; end card = AI image + "Tap the button below" + AbsByAI.com + chip,
     1.6 s. Never two physique pictures at once; no side-by-side, no "Meet the new you", no email screen, no printed
     claim. (The app's own "Powered by Claude + Gemini" footer is legible at 00:39–00:40 — Dan's call.)
  §5 hair never clipped in either aspect (every talking frame inspected, pairs/hair_top_9x16.jpg); levels alternate at
     every visible join; longest hold 6.5 s; crops are fixed per hold (background drift 0.00 % in all 12 holds, both
     aspects); no naked jump cut at any of the 20 picture cuts (pairs/p9_*.jpg).
  §6 audio: −14.1 LUFS, LRA 3.2, true peak −2.1 dBTP, L/R corr 0.9998, no silent seconds; 20 of 21 joins show no click
     and word onsets ramp up naturally (no clipped words); captions that exist are word-accurate, "abs" lowercase, "AI"
     uppercase, no "apps", clear of pill and chips, y≈1445 as in Ad 1.
  Stamps: all four sha256 values match the delivered files; deliver GATE_VERSION 2.1.0 = current; audio STAMP_VERSION 1 = current.

COULD NOT VERIFY:
  - Listening by ear: I measured every join and the loudness but cannot hear the mix; the artifacts FAIL needs a human ear.
  - The delivery folder (names, 540p copies, A/B clip, notes, recipe, measurements JSON) — I was barred from it.
  - Exact platform safe-area numbers for the chip band (D8) — not in my reading list.
  - Lip-sync inside the 0.43 s flash at 00:07 beyond the gate's audio-vs-source row.
  - Whether `pick_lav`/`voice_chain` were the tools used (recipe scripts not in my reading list).
```
