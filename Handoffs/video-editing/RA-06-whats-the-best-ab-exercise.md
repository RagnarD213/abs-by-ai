# RA-06 — "What's The Best Ab Exercise?": short-form ad, first cut from raw footage

**List 1 · ad (raw only) · READY.** Read `00-RULES.md` first. One of 16 short-form ad scripts Dan filmed on 8/28, all in the
same room on the same teleprompter set. Build them to one shared look.

## Source
* **Roll:** `/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/` **C1664 ≈5:00–6:12**. Times are approximate, taken from a Whisper pass. Full transcript: `/Volumes/Extreme/_edit_work/_transcripts-828-full/` (one `.txt` per roll).
  The range holds every take of this script: slate (*"the video I'm about to film is…"*), retakes and crew chatter.
* **Script:** Shoot 5 scripts doc, Drive `1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k` (local plain-text copy: `Media/codex-video-trial/05-recipes/candidates/shoot5-notes.txt`), lines **322–333** (section 3, short-form ad scripts, *"Paid ads, not organic content. Every one ends on a 'tap the button below' call to action."*).
* 4K 29.97 S-Log3, **four mono audio tracks**: pick the lav per file with `pick_lav.py`. Filmed horizontal and centre-safe for vertical crops (memory `shoot-828-slog3-format`).

## Deliverables (first cut)
1. **9:16 master, ≤ 0:59 hard** (YouTube Shorts ad inventory; memory `shorts-ads-research`: 0:45–0:59 is ideal, hook in the first 2 s).
2. **16:9 version of the same edit** (same takes, same audio, re-laid graphics).
3. REVIEW copies, audio A/B, stamps, `notes.md` (take map + every choice), `recipe/`.
The 1:1 square and any hook variants become List 3 jobs after Dan approves this cut.

If the best takes run over 0:59 after airtight trimming, **don't speed-ramp and don't cut the CTA.** Propose line cuts to Dan in the report and deliver the tightest honest version.

## Build
* **Standard:** Muhammad's approved ads (Ads 1–7, 10) for pacing, zoom cuts on word onsets, caption style, CTA pill, music bed and SFX. Our ad skill's measured targets: airtight, ~58% insert coverage, −14 LUFS / −1 dBTP for our own mix.
* **Colour:** S-Log3 → the approved 8/28 conversion (numpy LUT, memory `shoot-828-slog3-format`). The website conversion video (C1650/C1651, same shoot) is the closest graded reference. Decode as BT.709.
* **Claims:** on-screen text never states a number, a user count or a comparison Dan can't back (memory `ad-copy-no-unbelievable-claims`). Spoken words stay as filmed; flag risky ones in the report.
* End on the CTA with AbsByAI.com on screen. The landing page is decided at `/ad-setup`, not here.

## This ad's specifics
* Cue: **a split screen of Dan doing three exercises: toe touch, vacuum, spiderman plank.** The footage exists: 8/28 b-roll C1682 (toe touches), C1677 (vacuum), C1683 (V-sit/spiderman), plus the published `short2_toe-touches`, `short4_spiderman-planks`.
* ⚠ Claim line: *"thousands of guys have FIRED their trainer"*. The product has far fewer users (the board notes 75 people have ever generated). **Don't put it in on-screen text**, and flag the spoken line to Dan in the delivery report as his call.

## Deliver
New folder `Claude Ad Videos/whats the best ab exercise - RA-06/` (or `Codex Ad Videos/…`):
`… | claude | 9x16 | RA-06.mp4`, `… | claude | 16x9 | RA-06.mp4` + review copies + stamps. Send Dan the 9:16 review copy. Update `00-MASTER.md`.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/RA-06-whats-the-best-ab-exercise.md`: cut the "What's The Best Ab Exercise?" short-form ad from its 8/28 raw takes with /ad-edit. Best take of every line, 9:16 master ≤0:59 plus the 16:9 from the same edit, lav picked per file, the 8/28 S-Log3 conversion, same-person before/after, claim lines flagged to me. Every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/RA-06-whats-the-best-ab-exercise.md` with `$abs-edit-ad`: 9:16 master ≤0:59 plus 16:9 from the same edit. Deliver, send Dan the review copy, update `00-MASTER.md`.
