AD. Latest instructions: [R2 handoff, approved cut and voice](../handoff-20261014-ra16-round2-approved-cut-and-voice.md), 2026-10-14. Dan kept the full opening, allowed only two line deletions, authorized acceleration and selected warm voice with added bass. This supersedes the pending decisions and 50.4-second proposal below.

# RA-16 — "AI Took My Job": short-form ad, first cut from raw footage

**List 1 · ad (raw only) · NEEDS DAN (see "This ad's specifics" / "This short's specifics").** Read `00-RULES.md` first. One of 16 short-form ad scripts Dan filmed on 8/28, all in the
same room on the same teleprompter set. Build them to one shared look.

## Source
* **Roll:** `/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/` **C1668 ≈2:12–4:37**. Times are approximate, taken from a Whisper pass. Full transcript: `/Volumes/Extreme/_edit_work/_transcripts-828-full/` (one `.txt` per roll).
  The range holds every take of this script: slate (*"the video I'm about to film is…"*), retakes and crew chatter.
* **Script:** Shoot 5 scripts doc, Drive `1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k` (local plain-text copy: `Media/codex-video-trial/05-recipes/candidates/shoot5-notes.txt`), lines **419–429** (section 3, short-form ad scripts, *"Paid ads, not organic content. Every one ends on a 'tap the button below' call to action."*).
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
* ⚠ **Dan's call before firing:** the script opens *"I'm a personal trainer. And AI just took my job."* Dan isn't a working personal trainer, so on a paid ad this persona line is a deceptive-claim risk (memory `ad-copy-no-unbelievable-claims`, Google ad policy). Options: open on the second line, or run it only if Dan confirms it's true enough. The master list marks it NEEDS DAN.
* Also *"everyone is using AI to get in shape now"* and *"far better than any human fitness plan"*: keep them off-screen and flag them.

## Deliver
New folder `Claude Ad Videos/ai took my job - RA-16/` (or `Codex Ad Videos/…`):
`… | claude | 9x16 | RA-16.mp4`, `… | claude | 16x9 | RA-16.mp4` + review copies + stamps. Send Dan the 9:16 review copy. Update `00-MASTER.md`.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/RA-16-ai-took-my-job.md`: cut the "AI Took My Job" short-form ad from its 8/28 raw takes with /ad-edit. Best take of every line, 9:16 master ≤0:59 plus the 16:9 from the same edit, lav picked per file, the 8/28 S-Log3 conversion, same-person before/after, claim lines flagged to me. Every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/RA-16-ai-took-my-job.md` with `$abs-edit-ad`: 9:16 master ≤0:59 plus 16:9 from the same edit. Deliver, send Dan the review copy, update `00-MASTER.md`.


## Codex preparation, 2026-10-13

AD. R1 preparation is saved, not delivered or finalized.

- Review of the proposed cut, color/framing stills and voice auditions: http://127.0.0.1:8976/ (managed local review service).
- Work folder: `/Volumes/Extreme/_edit_work/ra16/`. Read `WORK_PACKET.json`, `proposed-cut.json`, `cost-ledger.json` and `recipe/` before continuing.
- The actual C1668 source is native portrait footage by the pool, stored 3840x2160 with rotation -90. It has one two-channel dual-mono microphone stream. The indoor, horizontal and four-track description above is incorrect for this roll. The existing sidecar and direct ffprobe agree; the picture was inspected.
- Selected full-script ranges total about 73.4 seconds before further pause trimming. A proposed 50.4-second version keeps the complete hook, introduction, three product steps and final CTA. Source boundaries remain provisional until heard-word checks. Removing the persona line would shorten it further.
- Dan has been asked to choose the opening and approve the line cuts. No answer or waiver has been recorded. Keep both decisions pending.
- Proposed removals: both free-app passages and the early CTA; the obsolete/everyone passage; the second human-plan comparison; the human-trainers-leave-you-confused tail. Exact kept words and ranges are in `proposed-cut.json` and on the review page.
- Three color variants were inspected at two moments. B is preferred: e1.45 daylight LUT, saturation 1.12, gamma 1.03. This is a proposal, not Dan approval. The framing uses the shared land-and-hold module for vertical and fixed crops for horizontal.
- Audio self-test PASS. Four voice auditions and five randomized blind listens are saved. Default won 3/5, with varying scores. Internal 9.943-second motion excerpts fail the audio gate on tone and spread; an exact-excerpt refit still misses tone. They are withheld as review videos. Do not claim delivery PASS or change thresholds.
- A model's claim that the excerpt used unrelated voice/picture was contradicted by zero-lag source waveform comparison and matching source/candidate mouth and hand frames. Evidence is in `source/sync-proof/` and `round1/audio-checks.json`. No complete-candidate audit has happened.
- Existing opener candidates A0147/A0148 provide the robot-replaces-trainer scene in both formats. The approved Dan self-generation demo is available. B0037 was rejected because it contains stick figures. Graphics, exact clip placements and the opening are not locked.
- No image or motion generation charges. Six Gemini quality-review calls returned token usage, retained in the ledger; actual billed dollars were not exposed. Estimated review cost was under $1. Subscription token usage is unavailable.
- Next: resolve Dan's two editorial choices; verify the final speech edges; prepare the 30-second opening and complete graphics/clip review; finish the chosen timeline's sound; then render both masters, run exact-file checks and one independent complete-candidate review, and deliver the review copies. Do not set delivered or finalized yet.
