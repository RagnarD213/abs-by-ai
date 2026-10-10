AD: Fired Them All (WV-01 Version B) vs Version A, 50/50 split test on /start

# Handoff, 2026-10-10

Task name: **Fired Them All AD Setup**. Recommended: **Opus 5.5, high effort** (page code on a paid-traffic page plus a video delivery; a miss means a redo).

## Goal

Put WV-01 Version B ("Fired Them All") on `https://absbyai.com/start` as a 50/50 split test against the live Version A. Same page, same ads, same cart. The video is the only difference. Then build the PostHog scoreboard and record the test so later sessions can read it.

## Precondition: stop if not met

Dan must have approved Version B R5 in VLC. On 2026-10-10 the board still read "Fired Them All AD R5, Codex. Awaiting VLC approval." If the starter prompt does not say R5 is approved and the board entry is still there, ask Dan in one line and do nothing else.

## Decisions already made (do not reopen)

- **Split on the page, not at the ad level.** One URL, a sticky per-browser coin flip. No second landing URL, no Google Ads changes.
- **No new software.** The page's own code does the split. PostHog (already installed) keeps score. No PostHog feature flag: both stored keys lack flag scopes, and the flag is not needed.
- **Version B runs at 1.2x, the same as A.** The session makes the 1.2x copy itself. Dan does not send it for a re-edit and does not need to review the speed copy before it goes live (uniform speed change of an approved film; the split is reversible).
- **Layout is locked.** Tests on /start are between videos, never page designs (Dan, 2026-09-28). Do not touch copy, layout, buttons or the cart.
- **Winner is called on trial starts per visitor and cost per trial**, never on a mid-funnel number (Dan's standing rule). Sound-on rate is an early warning only.

## Baseline (PostHog, 2026-09-30 to 2026-10-10, Version A only)

| Step | People |
|---|---|
| `vsl_landing_seen` | 714 (about 70 a day; 528 mobile, 175 desktop) |
| `vsl_sound_on` | 87 (12%) |
| `vsl_video_progress` 25 / 50 / 75 / 100 | 15 / 10 / 6 / 2 |
| `vsl_trial_cta_clicked` | 39 |
| `cart_checkout_completed` | 5, of which 2 look like Dan's own tests (Georgetown), so 3 real, all `utm_source=google` |

## Inputs

- Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.
- **Version B master (normal speed):** `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round5/final/Fired Them All AD R5 - complete Version B 1080p.mp4`, SHA256 `903eca4cd69ba19203394ee2a1c51ebb7bc9fce5d9bd6a9d8710c05297bf16fa`, with `.srt` and `.vtt` beside it. About 14:21 at normal speed, so about 11:57 at 1.2x. Verify the hash and probe the real duration first. If Dan approved a later round than R5, use that file and record its hash.
- **How A's 1.2x copy was made:** `Handoffs/handoff-20260929-wv01-final-a-1p2x-speed-variation.md`; its output and checks are in `/Volumes/Extreme/_edit_work/wv01-edit/speed-1p2/` (`exact_verify.py`, `REVIEW.md`). Use the same method for B.
- **Live A files:** `public/video/wv01-a-720.mp4` (87.1 MB) and `public/video/wv01-a-1080.mp4.part1` / `.part2` (85.3 MB each). Poster: `public/img/letter/video-poster-wv01.jpg`.
- **Page generator:** `.claude/skills/design-sales-page/reference/round2-letter/build_live.py` (`VARIANT`, `CHECKOUT`, `POSTER`, `VIDEO_PHONE`, `VIDEO_DESK` at lines 33-37; the `<video>` tag near line 57; `window.VSL` near line 270; the event script from line 282). Check with `verify_live.py` in the same folder. **Never hand-edit `public/start.html`.**
- **Video route:** `server.js` near line 11643. It joins `<name>.part1`, `.part2`, ... from `public/video/` and serves `/video/:name` with a 7-day cache.
- **Cart side:** `public/index.html` line 5991 registers `landing: 'vsl', landing_variant: q.get('v')` when `from=vsl`.
- Operating doc: `Docs/VSL_LANDING.md`. Memory: `vsl-landing-page`, `local-funnel-test-recipe`, `cross-platform-retest-rule`, `paying-members-count`.
- Read `.claude/skills/_shared/VIDEO-RULES.md` in full before the 1.2x render.

## Steps

### 1. Make Version B at 1.2x

Work in a new folder, `/Volumes/Extreme/_edit_work/wv01-edit/version-b/speed-1p2/`. Uniform 1.2x on picture and sound, pitch preserved, no cuts, no creative changes. Retime the SRT and VTT by the same factor. Run the same exact-file checks A's copy got (full decode, duration, sync from start through the final CTA, last words intact). The approved R5 master stays untouched.

### 2. Web files for B

- Encode `wv01-b-720.mp4` (phones) and `wv01-b-1080.mp4` (desktop) with the same codec, bitrate and faststart settings as A's live files. Probe A's files and match them, so the test is not also a picture-quality test.
- **GitHub rejects files over 100 MB.** B is about 14% longer than A, so at A's bitrate the 720p file lands near 99.5 MB and the 1080p near 195 MB. Keep every committed file under 95 MB by splitting into numbered parts (720p in 2 parts, 1080p in 3). Do not lower the bitrate to make it fit. Confirm the join route handles three parts and a split 720p before relying on it.
- New file names only (the route caches 7 days). Leave A's files as they are.
- Make B's poster the same way A's was made (caption-free early frame of B, 1280x720): `public/img/letter/video-poster-wv01-b.jpg`.

### 3. The split, in `build_live.py`

- Pick the arm in the head script, before first paint, in this order: `?vid=a` or `?vid=b` (QA override, marked `forced: true`), then the stored value in `localStorage.absbyai_vsl_video`, then a 50/50 coin that is stored. If storage is blocked, flip per page load and mark `sticky: false`.
- One constant sets B's share (0.5 now). Setting it to 0 or 1 and rebuilding is the rollback and the rollout.
- The browser must request only the chosen arm's video and poster. No flash of the other arm, no double download. The poster preload in the head follows the arm.
- Keep `landing_variant: 'letter-v1'` exactly as it is (existing reports depend on it). Add **`video_variant: 'a' | 'b'`** to every `vsl_` event, and `posthog.register({ video_variant })` so later events carry it.
- Add `vid=<arm>` to the checkout link next to `v=letter-v1`, and extend `public/index.html` line 5991 to register `video_variant` from `vid`. This covers browsers that drop the registered value between pages.
- Fire `$feature_flag_called` with `$feature_flag: 'vsl-video-variant'` and the arm as the response once per page view, the same pattern the old /start-v1 page used, so a PostHog experiment can read it later if the flag is ever created.
- **Watch time in seconds.** The two films differ in length and in where the opening ends, so percent milestones do not compare. After sound on, also fire `vsl_video_watch { sec }` at 30, 60, 120, 240 and 480 seconds, and `vsl_opening_done` when the viewer passes the end of that arm's opening. Take the exact opening end for each arm from the edit records (B's opening is frames [0,7640) of the normal-speed film, about 4:15, so about 3:32 at 1.2x; find A's from `version-b/round4/review/assembly-edl.json`) and write both values into the generator with a comment. Keep the existing percent events.
- Inside the Android and iOS apps nothing changes except which video plays.

### 4. Check before deploy

- Update `verify_live.py` for the two arms and run it.
- Locally (see memory `local-funnel-test-recipe`): load `/start?vid=a` and `/start?vid=b` on phone and desktop widths. Confirm the right video and poster, one video request only, sound-on restart from 0:00 still works, the muted preview still pauses when scrolled away, and the coin sticks across reloads without `?vid=`.
- Click through to the cart (do not pay) and confirm `cart_viewed` carries `video_variant`.

### 5. Deploy and verify live

Push only your files with `scripts/git/safe-push.sh -m "..." -- <files>`. Confirm the Railway deploy, then repeat the step 4 checks on `https://absbyai.com/start` for both arms and confirm the events arrive in PostHog with `video_variant`. Flag the native retest in your report (web deploys reach the apps).

### 6. PostHog scoreboard

Build one dashboard, "/start video test: A vs B", broken down by `video_variant`, with forced visits excluded: visitors, sound-on rate, `vsl_opening_done`, the seconds milestones, button clicks, `cart_viewed`, and trial starts (`cart_checkout_completed`). Add an annotation at the minute the split went live. Standing analytics authorization covers this.

### 7. Record it

- `Docs/VSL_LANDING.md`: a short section on the split (arms, file names, the share constant, events, the dashboard link, the read rules below).
- Update memory `vsl-landing-page`, then `scripts/sync-memory-to-repo.sh` and push `Docs/memory`.
- Board: one ACTIVE entry "/start video test RUNNING" with the start date and the two read dates. Remove this handoff's line from the board and from `Handoffs/README.md`. Run `scripts/board-check.sh`.

## How the test is read (put these in the doc and the board entry)

- **Minimum run: 21 days.** No winner before that, even with an early lead.
- **Early warning at day 14, or 500 visitors per arm, whichever is later:** if B's sound-on rate trails A's by a third or more (for example 8% against 12%), set B's share to 0 and tell Dan. A lead for B at this point changes nothing; keep running.
- **Winner on trials:** needs about 20 real trial starts in total, with the leader holding about 15. Count real trials from live Stripe, excluding Dan and test accounts, and match each to its arm in PostHog. At today's traffic this is about two months. Do not call it sooner on a smaller count.
- **Freeze during the test:** no changes to /start, the cart, or the ads feeding it. `Handoffs/handoff-20261001-search-campaigns-to-vsl-page.md` changes the traffic mix: hold it until the test ends unless Dan fires it before the split goes live.

## Out of scope

No YouTube upload, no Google Ads edits, no budget change (Dan is deciding that separately), no organic posting of either film, no page copy or layout changes, no PostHog feature flag, no new creative on either video.

## Open risks

- Repo growth: about 295 MB of new video in git. Expected, same approach as A.
- If the three-part join fails on Railway's boot, desktop visitors in arm B get no video. Verify the 1080p B file plays on the live site from a desktop browser before calling the task done.
- Visitors who already saw A and return may be flipped to B on their first post-launch visit. Small at this volume; note it in the doc, do not engineer around it.

## Exact next action

Verify the precondition, hash the R5 master, then start step 1.

## Starter prompt

> Rename this task "Fired Them All AD Setup". Version B (Fired Them All R5) is approved. Run `Handoffs/handoff-20261010-start-vsl-split-test-a-vs-b.md`: make the 1.2x copy of Version B, encode its web files, add the 50/50 video split to /start through the page generator, deploy, verify both arms live on phone and desktop, build the PostHog A vs B dashboard, and record the test in the doc, memory and board. Do not change the page, the cart or any ads.
