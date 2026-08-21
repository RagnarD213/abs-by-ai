# Handoff: Install the 13 AI-Dan exercise demo videos in the app + capture the App Store trainer screenshot

**Date:** 2026-08-21
**Project:** Abs By AI (web app + iOS wrapper)
**Business goal this serves:** App adoption first (iOS is still the only fully-blocked distribution channel, and this directly strengthens the Guideline 1.1 "we are a fitness app, not a body editor" argument), technical excellence second.

## Objective

Ship the 13 finished, Dan-approved AI-Dan exercise demo videos into the live Abs By AI trainer, replacing the stick-figure drawing in the **exercise detail sheet only** for the exercises that have a video, with the stick figure remaining as the fallback for the other 84 exercises. Compress the videos for web delivery, wire them into `public/index.html`, commit/push/deploy to Railway, verify on `https://absbyai.com`, then capture a new iOS App Store screenshot of the trainer showing AI-Dan mid-rep — the screenshot is arguably worth more than the feature, because it is the fastest way to make a reviewer perceive the app as fitness coaching rather than photo morphing.

## Current State

**The videos exist and are finished.** 13 Dan-approved finals live at
`Media/exercise-demos/<exercise-id>/<exercise-id>-AIDAN-narrated-FINAL.mp4`:

| exercise id | duration | source size | resolution |
|---|---|---|---|
| `bird-dog` | 27.0s | 17 MB | 1920x1080 |
| `cable-tricep-pushdown` | 25.9s | 14 MB | 1920x1080 |
| `db-bench-press` | 24.3s | 7 MB | 1920x1080 |
| `db-goblet-squat` | 25.0s | 9 MB | 1920x1080 |
| `db-rdl` | 25.7s | 10 MB | 1920x1080 |
| `db-row` | 27.7s | 22 MB | 1920x1080 |
| `dead-bug` | 28.4s | 17 MB | 1920x1080 |
| `face-pull` | 27.7s | 20 MB | 1920x1080 |
| `incline-pushup` | 25.9s | 11 MB | 1920x1080 |
| `leg-press` | 22.5s | 13 MB | 1920x1080 |
| `plank` | 20.2s | 3 MB | **1284x716 (odd — see gotchas)** |
| `pushup` | 19.2s | 15 MB | 1920x1080 |
| `reverse-lunge` | 17.0s | 13 MB | 1920x1080 |

**Total 177 MB.** Every folder name is already an exact match for an id in `public/exercises.js` — no mapping table needs to be invented.

- These are **landscape 16:9, ~17–28s, WITH Dan's cloned-voice narration** reading the form cues. They are not silent 8s loops. That drives the player decisions below.
- `Media/` is **gitignored** (`.gitignore:71`) because the repo is public and that tree holds shirtless/personal footage. The web-delivery copies must therefore be written to `public/exercise-demos/`, which is tracked and served.
- **Current stick figures:** `public/exercise-anims.js` — 342 lines, 60 SMIL pose sets, `getExerciseAnim(id, size)` on `window`. Rendered in exactly 3 places in `public/index.html`:
  - line ~8010 — workout card, 68px
  - line ~8059 — "next up" icon, 52px
  - line ~8137 — **exercise detail sheet (`openExerciseSheet`), 120px ← this is the only one that changes**
- **`openExerciseSheet(exId, cue, mistake)`** is at `public/index.html:8128`. It already ends with a conditional `lib.video` CTA button — `▶ Watch form video` — which links out to a hand-curated **YouTube** URL. All 98 exercises have one populated (`public/exercises.js:11` documents the field).
- `public/` is currently only **2.3 MB** total. The service worker (`public/sw.js`, cache `absbyai-v3`) precaches only `/offline.html` and `/img/logo.png` and never caches app or API requests — so it will **not** try to swallow the videos. No sw change required, but do not add them to the precache list.
- `ffmpeg`/`ffprobe` are **not on PATH**. Use the repo-local binaries: `./Media/video_edit/bin/ffmpeg` and `./Media/video_edit/bin/ffprobe`.
- App Store screenshot sets already exist at `app-store-assets/6.9-inch/` (1320x2868), `app-store-assets/6.5-inch/`, `app-store-assets/13-inch-ipad/`. The trainer slot is `06-ai-trainer-workout.png` (6.9-inch) and `04-ai-trainer-workout.png` (6.5-inch) — those are the files this task replaces.
- iOS is mid-rejection cycle. Read `Handoffs/handoff-20260821-ios-third-rejection-fix.md` before touching any App Store Connect asset — the 1.1 body-morphing fight is live and this screenshot is part of that argument, not an isolated cosmetic swap.

## Key Decisions Already Made

- **Only the detail sheet gets video. The 52px and 68px icons keep stick figures.** At icon size a photoreal video reads as mush, and a grid with 13 photoreal thumbnails sprinkled among 84 stick figures is what looks broken. In a detail sheet, a mixed library just reads as "some exercises have demos yet" — normal for a fitness app.
- **Ship the partial set now; do not wait for all 97.** 13/97 coverage is fine under the decision above, and the App Store screenshot value is available immediately.
- **Compress before committing. Never commit the 177 MB masters.** The repo is public and Railway deploys the repo; a 177 MB image is a slow, bad deploy and 13 MB per demo is unacceptable on cellular.
- **Do not autoplay with sound and do not autoplay-muted-loop.** The narration is the value of these clips; browsers block sound-on autoplay anyway. Poster image + tap-to-play with `playsinline` and `preload="none"` is the shipped behavior.
- **The AI-Dan video supersedes the YouTube `▶ Watch form video` button for the 13.** Two form videos in one sheet is confusing, and the point is that ours is better. Keep the YouTube button for the other 84.
- **Stick figures stay in the codebase.** `exercise-anims.js` is the fallback for 84 exercises and must not be deleted.

## Detailed Plan

1. **Confirm the shipping set with Dan before encoding.**
   The coordination file records that Dan approved `dead-bug` and `bird-dog` only reluctantly and **plans to drop both**. **OPEN:** ship 13 or ship 11? Default if Dan does not answer: **ship all 13** — they are approved, and pulling them later is a one-line map edit. Note the standing rule that alternating-limb moves rendered single-side or with visible seams are unacceptable in future batches.

2. **Create the web-delivery encodes** into `public/exercise-demos/`.
   Target ~960x540, H.264 High, CRF 28, `faststart` (so playback begins before the file finishes downloading), AAC 96k mono. Expect **~1.2–1.8 MB each, ~18–22 MB total**. Write a small script rather than 13 hand-typed commands:

   ```bash
   FF=./Media/video_edit/bin/ffmpeg
   mkdir -p public/exercise-demos
   for f in Media/exercise-demos/*/*-AIDAN-narrated-FINAL.mp4; do
     id=$(basename "$(dirname "$f")")
     "$FF" -y -i "$f" \
       -vf "scale=960:-2" -c:v libx264 -profile:v high -crf 28 -preset slow \
       -pix_fmt yuv420p -movflags +faststart \
       -c:a aac -b:a 96k -ac 1 \
       "public/exercise-demos/$id.mp4"
     "$FF" -y -ss 1 -i "$f" -frames:v 1 -vf "scale=960:-2" -q:v 4 \
       "public/exercise-demos/$id.jpg"
   done
   du -ch public/exercise-demos/* | tail -1
   ```
   Then **watch at least 3 encodes back** and confirm no banding/mush on the tank top and that the narration is intact. If the total lands above ~30 MB, drop to `scale=854:-2` before lowering quality further.

3. **Handle the `plank` outlier.** It is 1284x716, not 1920x1080 — a different aspect ratio (1.79 vs 1.78, close but the odd pixel dimensions will produce a non-even scale). `scale=960:-2` will still yield an even height; just verify the output visually. Do not pad or crop it — CSS `aspect-ratio` on the player handles the small difference invisibly.

4. **Wire it into the detail sheet.** In `public/index.html`, inside `openExerciseSheet` (~line 8128):
   - Add a module-level constant listing the ids that have a demo (or, cleaner, add `demo: true` to those 13 entries in `public/exercises.js` — pick one, do not do both).
   - Replace the 120px stick-figure line (~8137) with: if the exercise has a demo, render
     ```html
     <video class="ex-demo" src="/exercise-demos/<id>.mp4" poster="/exercise-demos/<id>.jpg"
            controls playsinline preload="none" style="width:100%;border-radius:12px;display:block"></video>
     ```
     otherwise render the existing `getExerciseAnim(lib.id, 120)` block unchanged.
   - Suppress the `lib.video` YouTube CTA when a demo exists (per the decision above).
   - Fire a PostHog event on play (`exercise_demo_played`, props `{ exercise_id }`) — the codebase already uses `window.posthog` guarded (see `posthog.capture('workout_completed', …)` near line 8120) so match that pattern.
   - Add a small `.ex-demo` CSS rule near the other `ex-sheet-*` rules; keep `aspect-ratio: 16/9` and a dark background so the poster load is not a white flash.

5. **Local verify before deploying.** Start the dev server via the Browser pane (`preview_start`, `.claude/launch.json`) — **never** run a dev server through Bash. Open the trainer, open a detail sheet for `pushup` (has demo) and for `bb-row` (no demo), confirm: video plays with narration, poster shows before play, the stick figure still renders for the non-demo exercise, no console errors, and no layout shift when the sheet opens.

6. **Commit, push, deploy, verify live.** One commit containing only this task's files (`public/exercise-demos/*`, `public/index.html`, and `public/exercises.js` if the `demo` flag route was chosen). Push to `main`, confirm the Railway auto-deploy finishes, then verify on `https://absbyai.com` — load a demo exercise sheet on a real page load and confirm the MP4 returns 200 and plays. Also check the deploy did not slow meaningfully with ~20 MB added.

7. **Capture the App Store screenshot.** This is the highest-value step; do not skip it because step 6 felt like the finish line.
   - Open the iOS Simulator panel **first** (`mcp__Claude_Code_iOS_Simulator__control` with `action: "attach"`) so Dan can watch, then build/launch the wrapper in `ios-app/`.
   - Navigate to the AI Trainer, open a demo exercise sheet, and **pause the video on a frame where AI-Dan is mid-rep with visible form and the gym clearly readable** — not the first frame, not a blurred transition. The frame is the whole point: it must read "fitness app."
   - Capture at 6.9-inch dimensions (**1320x2868**) and produce the matching 6.5-inch and 13-inch-iPad variants. Overwrite `app-store-assets/6.9-inch/06-ai-trainer-workout.png` and `app-store-assets/6.5-inch/04-ai-trainer-workout.png`; add the iPad equivalent (`app-store-assets/13-inch-ipad/03-ai-trainer.png`).
   - Reuse the existing caption/panel styling from `app-store-assets/tools/composite_panel.py` so the new shot matches the rest of the set. **Note:** that directory is littered with ` 2.py`, ` 3.py` numbered duplicates — the canonical file is the un-numbered one.
   - **Do NOT upload to App Store Connect in this session.** Show Dan the frames first; storefront assets are his call, and the 1.1 appeal strategy in the third-rejection handoff governs what gets submitted when.

8. **Flag the native retest explicitly.** This changes what the iOS and Android wrappers display in the trainer. Tell Dan in plain language that the iOS and Android apps need a quick retest of the trainer screen before the next store submission — silence is read as "no retest needed."

9. **Close out.** Update `AI_COORDINATION.md`, and check the dashboard task off at `absbyai.com/dashboard` in the same session using the `/dashboard-tasks` skill (gated endpoints + `X-Dash-Key`; do not work those endpoints from memory).

## Things to Avoid / Lessons Learned

- **`ffmpeg` is not on PATH on this machine.** Use `./Media/video_edit/bin/ffmpeg` and `./Media/video_edit/bin/ffprobe`. A bare `ffmpeg` call will fail with "command not found."
- **Never commit anything under `Media/`** — it is gitignored on purpose (public repo, shirtless/personal footage). Only the compressed `public/exercise-demos/` copies get committed.
- **Do not add the videos to the service worker precache.** `public/sw.js` deliberately caches almost nothing; adding 20 MB there would make every first load download the whole set.
- **Do not swap video into the 52px/68px icons.** Already tried in reasoning and rejected — that is precisely where the "mismatched" look Dan noticed comes from.
- **Do not delete `public/exercise-anims.js`.** 84 exercises still depend on it.
- **Do not autoplay.** Sound-on autoplay is blocked by browsers, and muted autoplay throws away the narration that these clips were built around.
- **Numbered duplicate files (` 2.py`, ` 3.mp4`) are everywhere in this repo** and are gitignored by the `* [0-9].py` style rules. Always operate on the un-numbered canonical file.
- **The `Media/exercise-demos/` folder also contains directories for exercises with no final** (e.g. `crunch`, `pullup`, `db-curl`). Glob on `*-AIDAN-narrated-FINAL.mp4`, not on directory names, or empty/partial folders will be picked up.
- **App Store screenshots are governed by the live 1.1 rejection strategy.** Do not upload or alter store metadata without reading `Handoffs/handoff-20260821-ios-third-rejection-fix.md` and getting Dan's sign-off.

## Relevant Files & Locations

- Masters (gitignored): `Media/exercise-demos/<id>/<id>-AIDAN-narrated-FINAL.mp4`
- Web encodes (to create, tracked): `public/exercise-demos/<id>.mp4` + `<id>.jpg`
- Detail sheet: `public/index.html` → `openExerciseSheet()` at line ~8128, stick-figure line ~8137
- Other stick-figure call sites (leave alone): `public/index.html` ~8010, ~8059
- Stick figures: `public/exercise-anims.js`
- Exercise library (97 exercises): `public/exercises.js`
- Service worker: `public/sw.js` (cache `absbyai-v3`)
- ffmpeg/ffprobe: `Media/video_edit/bin/`
- Screenshot sets: `app-store-assets/6.9-inch/` (1320x2868), `6.5-inch/`, `13-inch-ipad/`
- Screenshot tooling: `app-store-assets/tools/composite_panel.py`
- iOS wrapper: `ios-app/`
- Live site: `https://absbyai.com` · Dashboard: `https://absbyai.com/dashboard`
- Related handoffs: `Handoffs/handoff-20260821-ios-third-rejection-fix.md`, `Handoffs/handoff-20260819-exercise-demo-videos.md`
- Skills: `/exercisegeneration` (if more demos are generated), `/dashboard-tasks` (close-out)
- Baseline commit: `1f70d1d`

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Sonnet 5, standard thinking.** The whole job in one session. It is well-specified single-file UI work plus a scripted ffmpeg batch — no architecture, no brand voice, no Anthropic API code. Opus is not needed. |
| **If Claude usage is high / approaching a limit** | **Split it.** Codex (current flagship, medium effort) for steps 1–6 (encode, wire up, deploy, verify) — it is exactly the kind of well-specified implementation work Codex handles cheaply. Then a short **Claude Code session (Sonnet 5, low effort)** for steps 7–9. |

**Task-type override that applies regardless of usage:** step 7 (the App Store screenshot) **must** run in Claude Code, not Codex — it needs the iOS Simulator MCP to boot, drive, and capture the wrapper, which Codex cannot do. Everything before it is portable.

If it turns out harder than expected (video playback misbehaving inside the iOS WKWebView wrapper is the most likely surprise), escalate that specific problem to Opus with extended thinking rather than re-running the whole task at a higher tier.

## Starter Prompt for the Next Task

> Install the 13 finished AI-Dan exercise demo videos into the Abs By AI app, then capture the new App Store trainer screenshot. Full plan is in `Handoffs/handoff-20260821-exercise-demos-in-app.md` — read it first, it has the exact ffmpeg settings, the file paths, and the gotchas (ffmpeg is NOT on PATH — use `./Media/video_edit/bin/ffmpeg`; `Media/` is gitignored so the compressed copies go in `public/exercise-demos/`).
>
> Decisions are already settled: video goes in the **exercise detail sheet only** (the 52px/68px card icons keep their stick figures), stick figures stay as the fallback for the other 84 exercises, no autoplay (poster + tap to play, the clips have Dan's narration), and the AI-Dan video replaces the YouTube "Watch form video" button for those 13 exercises only.
>
> First concrete action: ask me whether to ship all 13 or drop `dead-bug` and `bird-dog` (I said I might drop those), then run the encode batch in step 2 and report the total output size before wiring anything into `index.html`.
>
> Finish the whole thing: commit, push, confirm the Railway deploy, verify on absbyai.com, capture the screenshot in the iOS Simulator, tell me if a native retest is needed, and check the task off on the dashboard. Do not upload anything to App Store Connect — show me the screenshot frames first.
