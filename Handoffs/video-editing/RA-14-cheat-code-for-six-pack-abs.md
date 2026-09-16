# RA-14 — "The Cheat Code For Six Pack Abs": short-form ad, first cut from raw footage

**List 1 · ad (raw only) · READY.** Read `00-RULES.md` first. One of 16 short-form ad scripts Dan filmed on 8/28, all in the
same room on the same teleprompter set. Build them to one shared look.

## Source
* **Roll:** `/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/` **C1667 ≈5:28–6:59**. Times are approximate, taken from a Whisper pass. Full transcript: `/Volumes/Extreme/_edit_work/_transcripts-828-full/` (one `.txt` per roll).
  The range holds every take of this script: slate (*"the video I'm about to film is…"*), retakes and crew chatter.
* **Script:** Shoot 5 scripts doc, Drive `1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k` (local plain-text copy: `Media/codex-video-trial/05-recipes/candidates/shoot5-notes.txt`), lines **404–411** (section 3, short-form ad scripts, *"Paid ads, not organic content. Every one ends on a 'tap the button below' call to action."*).
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
* Three numbered steps. Use real app screens for each; J2 step cards.

## Deliver
New folder `Claude Ad Videos/the cheat code for six pack abs - RA-14/` (or `Codex Ad Videos/…`):
`… | claude | 9x16 | RA-14.mp4`, `… | claude | 16x9 | RA-14.mp4` + review copies + stamps. Send Dan the 9:16 review copy. Update `00-MASTER.md`.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/RA-14-cheat-code-for-six-pack-abs.md`: cut the "The Cheat Code For Six Pack Abs" short-form ad from its 8/28 raw takes with /ad-edit. Best take of every line, 9:16 master ≤0:59 plus the 16:9 from the same edit, lav picked per file, the 8/28 S-Log3 conversion, same-person before/after, claim lines flagged to me. Every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/RA-14-cheat-code-for-six-pack-abs.md` with `$abs-edit-ad`: 9:16 master ≤0:59 plus 16:9 from the same edit. Deliver, send Dan the review copy, update `00-MASTER.md`.
