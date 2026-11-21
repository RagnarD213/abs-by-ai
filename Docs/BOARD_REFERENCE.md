# Reference facts moved off the coordination board (2026-09-15)

`AI_COORDINATION.md` is a status board with a 2,500-word budget. These facts were sitting in its entries with no other
durable home, so they live here now. The verbatim pre-diet board is in `AI_COORDINATION_ARCHIVE.md` under
"Board snapshot before the 2026-09-14 diet (verbatim)".

## Meta API access — WORKING

- `META_ADS_TOKEN` (system user `abs-automation`, never expires: ads_management, ads_read, business_management,
  pages_show_list, pages_read_engagement, pages_manage_posts, instagram_basic) + `META_APP_SECRET` in
  `~/.absbyai-secrets.env`. `ads_read` verified 2026-09-02 (`scripts/ads/ads-digest.js` fills the Meta section).
- ⚠ The Business Settings token UI silently fails for ads scopes even for an app Administrator — **mint via
  `POST /{system_user_id}/access_tokens` with `appsecret_proof`** (recipe: `Handoffs/handoff-20260902-ig-engagement-ad-identity.md`).
- App `1598463548528030` is LIVE since 2026-09-02 (dev mode blocked all API ad creatives, subcode 1885183). App-settings
  writes are disabled via API and Claude is platform-blocked from the settings form — Dan fills Basic, Claude can click Publish.
- ⚠ Duplicate Page's real id is **`1348044195050800`** (`61593951123927` is its business-asset id). Keeper
  `1380236418500031`. Not deleted. **Do not use the API to tell them apart** — `instagram_business_account` reads empty
  for ALL pages, a false negative.
- ⚠ IG `explore` placement is deprecated in v21.0; campaigns now require `is_adset_budget_sharing_enabled`.

## Video-quality engine notes (Phases 1–2, VQC-A)

- Phase 1 (`eff3896`): `_shared/deliver/gate.py`, 30 rows × 7 formats; `gate.py --audit` proves no holes. The 17 old QC
  forks are BANNERED, not deleted — delete at the end of Phase 3.
- Banned-screen scan was blind before Phase 1 (matched the recording, not the screen; spray-tan longform has carried
  the BEFORE/AFTER screen at 18:04). Phase 2 registered `compliance:banned_screen` using "the band between the chrome
  strips is a photograph" (0.00–0.30 white vs 0.94–0.97 on look-alikes); the pairing test does not separate.
- rev 6 (Dan's approved website final) passes the per-hold headroom ceiling with ZERO margin (70 px) — recorded in
  `formats.py`, not tuned.
- `public/exercise-demos/plank.mp4` ships at 960x536 where the other 32 are 960x540.
- VQC-A baseline `Docs/VQC_baseline_20260909.md`: 166 masters re-gated, 159 would not ship. The substantive finding is
  62 of our own Shorts/longforms, incl. **21 of 23 V2/V3/V6 cutdowns missing −14 LUFS while already published — owned by
  nobody.** `selftest.sh` is zsh; `bash selftest.sh` gives a fake "unbound variable".

## `gate.py` run on the Ad 5 vertical (2026-09-11)

Master 26/2, cutdown 27/1. `reference/plan_build.py` builds the plan from a build's own files.
1. `compliance:labels` takes ONE chip position per kind; Muhammad-style cards put the AI chip at each card's own
   corner, so it cannot be measured on his builds (0 wrong labels; passes on the cutdown).
2. `cut:min_segment` flags two framing stubs of 5 and 3 frames (68.60 s, 133.17 s) — pre-existing in the approved crop;
   merge each into the hold before it in a future round.
3. `captions:graphic_clearance` needs per-graphic MOVs a PIL compositor never produces; `captions:sync` NOT MEASURED on
   a cut with one post-silence cue (`qc.py` check 20 covers it).
⚠ Feeding `crop.json` holds straight into `punch` reads contiguous same-level splits as fake jump cuts — merge first.
⚠ `reference/caption_sync_check.py` must keep per-process temp files and least-washed-frame sampling. The `ad3-vert/`
and `ad4-vert/` build copies still write fixed `/tmp` paths — re-copy the skill's version before reusing them.

## Zeeshan organic batch brief (2026-09-09)

Doc `1Tdng5SrBthSaFDxaPnY2bWVhxp5e14YKbe3EVGhfjPE` — five videos: ab wheel workout-only (C1630–33), arms & shoulders
(C1582–87), STOP Deadlifting (C1487–88), Oura review (C1610–13), abs at 40 vs 25 (C1609). Lav is the right channel on
every roll. Video 3 has an asset hole (rows, pulldowns, rear-delt flye, powerlifter physique never shot).
Remaining unedited pool (10): Belly Fat Emergency, Real Reason You Don't Have Abs, Keep Your Muscle On Zepbound, Daily
Salad, The Vacuum (+ workout-only), Arms & Shoulders workout-only, Why You MUST Workout Every Day, Intermittent Fasting,
How To Work Out At Home On A Budget.

## Incidents already fixed

- 2026-09-14: another session replaced `Muhammad Ad Videos/this picture got me abs - ad 1/… muhammad | 16x9 | ad 1.mp4`
  (the audio selftest's pinned reference) with a 24 s audio-only file. Restored from
  `_edit_work/ad1-8-14/reference/muhammad_final.mp4` (sha matches corpus); bad file in `_edit_work/_clobbered_20260914/`.
- 2026-09-09 spray-tan shorts: the pipeline kept a forked `work/dereverb.py` and `finishaudio.py` fitted 7 octave bands
  while the gate grades 10 — both moved to the shared module (`9f42e12`). Rollback: `spray-tan-first/out/_PRE_AUDIO_20260909/`.
- 04 invest-health: the delivered mix has no dereverb (any spectral subtraction fails the artifacts row on this
  programme); EDT reads 80.00 ms against an 80.0 bound. Dereverbed alternative = re-mux of `audio/final_mix_v5.wav`
  (cannot carry a PASS stamp). Detail: `REBUILD_NOTES.md` in the delivery folder.
