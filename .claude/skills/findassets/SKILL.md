---
name: findassets
description: Find an asset Dan called for in a revision note — a B-roll shot, a clip from one of our own finished videos, a stock or AI clip, a photo — then CUT the exact portion out, upload just that portion to Google Drive, and drop the link into the revision doc at the right place. Use whenever Dan writes a revision that names footage instead of linking it ("replace this with footage of me doing X", "use the clip from the Y video", "find that B-roll"), or leaves a "[CLAUDE - FIND THIS CLIP...]" placeholder in a doc — even if he doesn't say "/findassets". Writing the revision review itself is /revisions; re-rendering our own cuts is /ad-edit and /longform-edit.
---

# /findassets — locate the asset, cut it, upload it, link it

Dan writes revision notes for human editors by hand. When he calls for footage we
already own he does not want to go hunting for the file, scrubbing for the moment, and
trimming it himself. **This skill does that end to end.**

**The deliverable is never "here is the source video, look around 6:20."** It is a
trimmed clip, already the right length and the right look, sitting in Drive, linked from
the revision doc at the exact bullet Dan wrote. The editor should be able to drag it onto
the timeline without a decision.

---

## Step 0 — read the revision doc and pull out every asset call

Read the doc with the Drive MCP (`read_file_content` on the doc id). Look for:

- explicit placeholders — `[CLAUDE - FIND THIS CLIP AND GIVE DIRECT GOOGLE DRIVE LINK…]`
- descriptions with no link — "replace this with footage of me doing toe touches"
- references to another one of our videos by title — "from the *Ultimate 1 Minute Ab
  Workout* video"
- references to a folder that already exists — those need no work, just verify the link

A doc can carry revisions for **more than one video** (this one had ab-wheel notes and ad
notes in the same file). Only act on the section Dan pointed you at.

## Step 1 — ask the questions that change the deliverable, then stop asking

Ask in ONE round, up front. The four that actually matter:

1. **Which occurrence** — Dan's videos usually show an exercise twice (a teaching demo
   while he talks, and the silent workout run-through). They look completely different on
   a timeline. Ask which; don't guess.
2. **Length** — the useful answer is usually "the same length as the clip that's there
   now," which means you have to go measure the existing clip in the editor's cut. Ask,
   because "8 seconds with handles" and "match the existing clip exactly" are different jobs.
3. **Audio** — keep or mute. If KEEP, the clip's audio goes through the shared standard (below), never `-c:a copy`.
4. **Where on Drive** — which folder, and who needs access.

Everything after that is your call. Do not come back with more questions.

### If the clip keeps its audio — the shared standard applies (2026-09-02)

A clip cut from a raw roll for a third-party editor used to be cut with **no channel rule at all**, so
the editor received both mics (a comb filter on any phone) or, on an 8/28 roll, the far mic. Now:

1. `python3 .claude/skills/_shared/audio/pick_lav.py ROLL.MP4` — measures which stream/channel is the
   lav on THIS roll (2-channel rolls and the 8/28 four-mono-track rolls) and writes `ROLL.MP4.audio_source.json`.
2. Cut the clip with that JSON's `-map` + filter, then `pan=stereo|c0=c0|c1=c0` (lav mono → centred
   stereo). Never `-c:a copy` from a roll.
3. `python3 .claude/skills/_shared/audio/audio_gate.py CLIP.mp4 --synthetic` before upload (L/R image,
   loudness, true peak, silence, length — the reference-tone rows do not apply to a raw excerpt).
4. Put the `pick_lav` verdict line (`LAV = stream a:N channel K`) in `DELIVERED_CLIPS.md` for that clip,
   so the editor and the next session know which mic the clip carries.

## Step 2 — find the source, and find the CLEAN source

Search both places, in parallel:

- **Local / Seagate.** `find ~ /Volumes/Extreme -iname "*keyword*"`. Long-form masters
  live in `YouTube Long Form Video Content/` and `claude edited long form content/`; raw
  and cutdown footage lives on `/Volumes/Extreme/Abs By AI Photo Shoots/` and the
  per-shoot folders.
- **Drive** — `search_files` with `title contains '...'`.
- **The asset library** —
  `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/`, mirrored on
  Drive at folder `1Hby8O4mB4HZS341qvrVKHSHyCGBgP8mi`. Read
  `00 START HERE - asset index.txt` first; the answer may already be a file in there.

> ⚠ **The published master is usually the WRONG source.** Our uploaded YouTube videos
> carry burned-in lower thirds from the old teal/pink branding ("Toe Touches / 10 Reps").
> Handing the editor a clip with a dead brand's graphic baked in is worse than handing him
> nothing. Look for a `- DESCRIPT RAW CUTDOWN` file or the original shoot footage — same
> take, no graphics. Then fix the grade yourself (Step 5).

Use the transcript to find the section fast when there is one: `v4-words.json` /
`*-transcript.txt` next to the video, grep for the words Dan says right before the moment
("I'm going to run you through this workout one time through the series").

## Step 3 — measure the clip you are replacing

Download the editor's cut (`curl -sL "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`
works for anything shared with Dan) and find the exact in/out of the shot at the timestamp:

```
ffmpeg -v info -ss <T-6> -t <14> -i cut.mp4 -vf "select='gt(scene,0.12)',metadata=print:file=-" -an -f null - 2>/dev/null | grep pts_time
```

Add the `-ss` offset back to every `pts_time`. Confirm visually with a labelled frame grid
before you trust it. **Duration of that shot is the spec.** (In the first run it was
34.87 → 39.34 = **4.47 s**.)

Also check the runtime against Dan's timestamps to make sure you downloaded the right cut
— two editors may each have sent a version of the same video.

## Step 4 — pick the best moment, and look at it

Dan's briefs say things like "find the incident where my abs look best." That is a
judgement call you have to actually make, with your eyes:

```
ffmpeg -v error -ss <start> -i src.mp4 -t <dur> -vf "fps=2,crop=<w>:<h>:<x>:<y>,scale=360:-1,tile=6x10" -frames:v 1 grid.jpg
```

Read the grid. Then read a tighter one at 1 fps cropped to the torso. Pick a window that:

- sits **later in the set** — abs are pumped, definition reads better, and the camera has
  usually pushed in by then (less upscaling when you match the punch-in)
- contains at least one full peak contraction
- starts and ends on a clean beat, not mid-blur

## Step 5 — match the look of the cut it is going into

If you had to fall back to raw/ungraded footage, fit the grade to the graded master.
Both files contain the same footage, so:

1. Find the time offset and the punch-in by brute-force correlation — grayscale, downscale
   to 480×270, search scale ∈ [1.0, 1.7] and crop offset, take the best normalized
   correlation. Refine at 640×360. (First run: raw = master + 0.583 s, crop
   `1684:947:110:50`, corr 0.81.)
2. Fit the grade by **percentile matching per channel** over 3 paired frames — robust to
   the residual spatial misalignment that a pixel-wise fit is not. Emit an ffmpeg
   `curves=r=…:g=…:b=…` string.
3. Verify: means and p10/p90 per channel within ~3 levels of the master, and eyeball an
   A/B hstack.

`reference/curves_1min-ab-workout_rawcutdown-to-V4.txt` is the fitted curve for the
1-Minute Ab Workout raw cutdown → published V4 look. Reuse it for that roll; refit for any
other roll.

Render at the source frame rate, `-crf 20`, `yuv420p`, lanczos.

## Step 6 — get it onto Drive (this part has a trap)

There is **no Drive write path except the browser.** The Drive MCP's `create_file` sends
content as base64 through the model, so anything over a few hundred KB is impossible. The
`GOOGLE_REFRESH_TOKEN` in `~/.absbyai-secrets.env` is **calendar.readonly only** — no
Drive scope. There is no rclone, no Drive desktop sync.

**The working route — synthetic drop into the Drive web UI:**

1. Keep the file **under 10 MB** (`file_upload`'s hard cap). `-crf 20` on a ~5 s 1080p
   clip lands around 8–9 MB.
2. Open the destination folder in Chrome (`mcp__claude-in-chrome__navigate`).
3. Drive's page has **no `input[type=file]`** — create one:
   ```js
   const i=document.createElement('input');i.type='file';i.id='claude-upload-input';
   i.setAttribute('aria-label','claude upload input');
   i.style.cssText='position:fixed;top:10px;left:10px;z-index:99999;width:300px;height:40px;background:#fff';
   document.body.appendChild(i);
   ```
4. `find` it to get a `ref_N`, then `file_upload` the local path into it. The File object
   is now in the page.
5. Build a `DataTransfer` from `input.files[0]` and dispatch `dragenter` → `dragover` →
   `drop` on the element chain under the file list. Drive's drop overlay appears on
   dragenter; the drop only lands once the overlay is up.
6. **It will upload once per ancestor you dispatch on.** The first run produced **17
   duplicates.** Dispatch on ONE element (retry a level up only if nothing uploads), then
   immediately list the folder (`search_files` with `parentId = '<folder>'`) and
   `trash_file` every copy but the earliest. Search indexing lags — list the folder by
   parent, not by title, and list it twice.
7. Remove the injected input when done.

**Permissions:** a file dropped into a folder that is already "anyone with the link:
reader" inherits that. Check with `get_file_permissions` — if it inherited, do not call
`share_file` at all.

## Step 7 — write the link into the doc, in place

Open the doc in Chrome in edit mode. **Triple-click** the placeholder bullet to select the
whole paragraph, then type the replacement over it. Type the prose first, then the URL
followed by a **trailing space** — Docs auto-links it.

Write it as an instruction to the editor, not as a note to Dan. Say what the clip is,
that it is already trimmed to length, that it needs no further work:

> USE THIS CLIP - Dan doing toe touches, from the workout run-through in "The Ultimate 1
> Minute Ab Workout." Already trimmed to 4.47 seconds, the exact length of the V-Sit
> Twists clip currently at 0:36, and color-matched to the same graded look with no
> on-screen graphics. Drop it straight in: <link>

Do **not** restructure or reword anything else in Dan's doc.

## Step 8 — file the clip for reuse

Copy the delivered clip into
`/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/`
with a descriptive name, and append a row to `DELIVERED_CLIPS.md` in this skill folder so
the next session finds it in one grep instead of re-cutting it.

---

## Standing rules that apply to anything you cut

Inherited from the asset library and the ad rules — they bind here too:

1. Never deliver a **side-by-side before/after** for an ad. Sequential is fine.
2. Any AI-generated body image or clip needs the burned-in **AI-GENERATED** tag.
3. No **body-shaming** framing — no zoom-ins on belly fat.
4. Old-branding graphics (teal/pink chips) must not survive into a new cut.
5. Never show the **email-capture screen** in an ad.

## Lessons

1. **The published video is not the clean source.** Burned-in lower thirds from the old
   branding are on every workout master. Look for the DESCRIPT raw cutdown.
2. **Ask which occurrence.** Demo reps and workout reps are different shots, different
   weight, different audio.
3. **"Same length as the existing clip" means go measure it** in the editor's cut — scene
   detection plus a labelled frame grid, not an eyeball.
4. **Two editors may have sent the same video.** Match the file's runtime against the
   timestamps in the revision doc before you measure anything.
5. **Match the grade, don't ship flat footage.** Percentile-match per channel across three
   paired frames; a pixel-wise fit fails on the residual misalignment.
6. **Later reps look better than early reps** — pumped abs, and the camera has pushed in.
7. **Drive upload has exactly one route** (synthetic drop, §6) and it **duplicates**.
   Always clean up by listing the folder by `parentId`, twice.
8. **10 MB is the `file_upload` ceiling.** Encode to fit before you start.
9. **Check inherited permissions before sharing.** Files dropped into an already-public
   folder are already public.
10. **"Keep original audio" can mean silence.** The raw cutdown's workout section measured
    −70 dB; the music only exists on the graded master. Say so in the note rather than
    quietly delivering a silent track as if it were the take audio.
12. **A clip cut with audio carries the lav only, per `pick_lav`, and is gated `--synthetic` before upload**
    (2026-09-02). See the audio block under Step 1.
11. **YouTube is not a source you can count on from this Mac (2026-09-01).** yt-dlp is pinned at
    2025.10.14 because the only Python is 3.9 (newer builds need 3.10+ and a JS runtime for SABR);
    `android_vr`/`ios`/`mweb` clients and `--cookies-from-browser chrome` all 403 or return no
    formats, and Node `@distube/ytdl-core` fails the same way. Do not burn time on it — check
    `08 SixPackAbs Archive - CHECK BEFORE USING/` and Drive folder `1ZO4wukehoHAwnRRyDyFKm4hFtXMYF2Ex`
    for Dan's own screen recordings of the old-channel videos first, and say plainly when the
    recording shows a different moment than the one asked for.
12. **The synthetic drop must land on the file-list grid, not the page container.** Dispatching on
    `div[role="main"]` did nothing; dispatching dragenter→dragover→drop on
    `document.querySelector('[role="grid"] [role="row"]')` uploaded exactly once (no duplicates).
    The javascript_tool result is sometimes "[BLOCKED]" — confirm with a screenshot ("1 upload
    complete" toast) and a `parentId` listing, not the return value.
13. **Typing a new bullet right after a hyperlink line inherits blue-underline styling** that is NOT a
    real link (the context menu offers "Insert link", not "Remove link"). Select the new lines and
    cmd+\ (Clear formatting); the list structure survives.

