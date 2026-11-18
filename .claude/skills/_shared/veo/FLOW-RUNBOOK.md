# Flow runbook: generating Veo clips on the Google AI Pro subscription in Chrome

For the `flow-veo` background agent (`.claude/agents/flow-veo.md`) and for Codex driving its own browser. Mapped on
2026-10-17 against flow.google.com (frontend build `boq_labs-ai-sandbox-frontend_20261016`). Flow changes its interface
often: if a step below no longer matches the screen, find the control by its label, finish the job, then fix this file.

You get a job folder. Everything you need is in `JOBDIR/veo/job.json`: per clip the `upload_start` / `upload_end` JPEGs,
the `prompt`, `aspect` and `model`. Only clips with `"status": "queued"` and `"route": "flow"` are yours.

## 0. Before you start

- Use supported browser tools in the current client, in this job’s own new tab. Native Mac file-picker controls are allowed when the supported uploader is unavailable. Never touch another job’s tabs.
- The account is Dan's (signed in, PRO badge top right). Never sign out, never change account settings, never click
  Upgrade or Manage subscription, never buy credits.
- One-time agreements (privacy notice, "Rights to use this image") were accepted by Dan on 2026-10-17. If any NEW
  agreement, terms, payment or consent screen appears, stop and report it; do not click it.

## 1. Credits check (every job, before the first submit)

Open `https://flow.google.com/`, click the round avatar (top right). The menu shows **"N Google Flow credits"** and the
**Visible watermarking** switch. Record the balance: `python3 veo.py credits --set N`. Check the switch is OFF
(`aria-checked="false"` on the button labelled "Visible watermarking"); if it is ON, turn it off (it is Dan's display
preference for this purpose, set 2026-10-17). Press Escape. Inside the project, the gear icon (top right) holds **Return silent videos**: it must be ON (Dan, 2026-10-20; without it a clip whose audio fails comes back as a "No audio generated" error tile instead of a usable silent video). If it is off, turn it on.

Cost per generation (shown live as "Generating will use N credits" in the settings popover, trust that over this table):
Pro: Veo 3.1 Lite 10, **Veo 3.1 Fast 20 (default)**, Veo 3.1 Quality 100, Omni 1.1 Flash 12 (Pro gets 1,000 a month plus 50 a day). Measured on Ultra 2026-10-20 (badge ULTRA, balance about 10,000): Lite 5, **Fast 10**, Omni 1.1 Flash 12 (Omni offers 360p/720p and 4/6/8/10 s; pick 720p, 8 s). The Download menu on Ultra shows 4K for 50 credits: never click it. **If the balance is below what the remaining queued clips need, submit only what fits, then stop and report
`CREDITS_OUT` with the clip ids left.** Never switch to the paid API yourself; the main agent asks Dan.

## 2. Open a project for the job

On the home page click **New project** (a changelog popup may appear: "Get started" closes it). Rename the project to the
job name: click the date title top left, select all, type the job name, Enter. Keep the project URL
(`https://flow.google.com/project/<uuid>`) and write it in your report.

## 3. Set the composer once

At the bottom is the prompt box. If an **Agent** pill is white (on), click it so it goes grey: we generate directly, never
through Flow's agent. Click the settings chip at the right of the prompt box (it reads like "Video · 720p · 8s · x1"):

- **Video** (not Image), then **Frames** (not Ingredients).
- Orientation from the clip's `aspect`: 16:9 or 9:16.
- Model dropdown: **Veo 3.1 - Fast** unless the clip says `lite`, `quality` or `omni` (`quality` only on a clip whose job entry records `dan_asked`; otherwise use Fast and report it) (`omni` means the currently available Flash version, recorded explicitly in the job). Since 2026-10-21 a job often mixes models (a Veo clip `A3` and its Omni twin `A3o`, see README "Which model and how many takes"): **re-check the dropdown before EVERY submit** and switch it to that clip's model; it is not a set-once setting in a mixed job. Select the clip’s requested duration from the current menu and verify the actual exported frame count; availability differs by model/version.
- Count **x1**.
- Read the "Generating will use N credits" line. Press Escape.

Observed November 17, 2026 on Ultra: **Veo 3.1 Fast Frames offered 4, 6 and 8 seconds with both START and END assigned**. Fast showed 10 credits at both 4 and 8 seconds. The tested 4-second native export contained 94 frames at 24 fps (3.916667 seconds); preserve those actual frames without padding. **Omni 1.2 Flash** was available and showed 12 credits for 4 seconds and 24 for 8 seconds; tested native exports contained 96 and 192 frames respectively at 24 fps. These observations supersede the older fixed-eight-second note. Recheck model, duration and live price before every submission, rather than assuming these options persist. Flow has no negative-prompt field: the `negative` text is not sent (the prompts already say what must not happen).

## 4. Upload the job's frames (once per job)

Flow builds its file chooser only when **Upload media** is clicked. Use the current client's documented file-chooser/upload API, arming its filechooser event before clicking. Do not inject upload hooks, mutate the DOM with evaluation, use CDP/private APIs, or bypass current tool restrictions.

If the supported uploader fails because Chrome's extension file-URL access is off, retain the error and use the native Mac picker. Do not repeatedly retry the blocked uploader or silently change that permission. On Codex, follow the installed computer-use skill and `@oai/sky` through node_repl. Get fresh full native accessibility state before using element indices when diff indices are unreliable. In the native Open dialog, **Go to Folder** reaches the exact staged upload directory; verify the full path and selected filenames. Use native **Edit > Select All** if the shortcut fails. All28 small JPEGs (10.7MB total) uploaded successfully in one native batch on November17; transport limits may differ for supported API uploads.

Wait until every upload has finished before assigning frames: the picker list re-sorts while uploads complete. Search each exact unique staged filename and verify that its preview matches the correct START or END. Never select from a shifting unfiltered list. Any NEW rights agreement, consent, terms or payment screen follows the current action-time confirmation policy; do not treat an old acceptance note as permission to accept a new agreement.

## 5. Submit each clip

For each queued clip, in job order:

1. **Fill END first, then START (measured 2026-10-20: with START filled first, the End picker's Add landed the START image in both slots).** Clicking a filled slot empties it. In each picker type the file name, wait for the preview to show the right frame, then click **Add to prompt** (never the result row). Slot thumbnails are square center crops, so hands at the edges vanish: compare faces/poses, not edges. Old order, for reference: Click **Start** → type the clip's exact start file name (`A1-start`) in "Search assets" so only that file is listed
   (it is highlighted already) → click **Add to prompt** directly. Do not click the result row: on the test that sometimes
   closed the picker and added the frame on its own. The End picker is wider, so its Add to prompt button sits further right.
2. After END is assigned, click **Start** → search the exact START filename → verify its preview name → **Add to prompt**. Zoom on
   the two thumbnails in the prompt box and compare them with the job's frames: START left, END right (⇄ swaps them).
   **This step is the one that went wrong on the first test (2026-10-17): the END frame landed in both slots.**
   `veo.py collect` now refuses a take that does not open on START, but a wrong pick still wastes 20 credits.
3. Click the prompt text area and type the clip's `prompt` exactly.
4. Click the round arrow button (bottom right of the prompt box). The clip appears as a new tile at the top left of the
   grid with a percentage; the prompt box clears and the Start/End slots empty.
5. Record it: `python3 veo.py mark JOBDIR A1 submitted` (this also logs the credits spent).

Submit the next clip right away; Flow runs several at once. Do not wait for one to finish before submitting the next.
Measured 2026-10-17: one Veo 3.1 Fast frames-to-video clip took about 70 s from submit to finished.

## 6. Wait, then collect each finished clip

Poll every 30 to 60 s with a small screenshot (scale 0.4) or `get_page_text`. A finished tile shows the first frame and a
play icon instead of a percentage. A failed tile (narrow, with Retry / Reuse prompt / Delete buttons) shows an error or a "violates policy" note: record it with
`veo.py mark JOBDIR A1 failed --note "<the message>"` and move on (do not resubmit more than once; a policy refusal on
the same frames is reported, not retried with a changed prompt).

Flow titles each finished tile itself ("Businessman smirking at desk"). Tie it to the clip first: hover the tile → **⋮
More options** → **Rename**, **wait about a second** for the box, select all (cmd+a), type the clip id (`A1`), Enter.
Typing too early appends to the old title. Tiles start newest first, but the grid re-sorts after renames and reloads:
find tiles by name, or click **Videos** in the left sidebar to hide the uploaded frames.

Always collect the **full native original** first. In the November 17 Flow UI, the tile’s direct Download button saved native 720p immediately. Right-clicking the completed asset group opened Rename and a Download submenu with **720p Original size** and **1080p Upscaled**. Reinspect the current UI rather than assuming this layout persists. Do not click paid 4K or Upgrade options without applicable authorization. Rename first, wait for the edit box, select all and confirm the exact saved title.

Use the actual browser host’s Downloads folder. A supported browser download-event wait timed out on November 17 even though Chrome had saved the complete file. Check the exact title/token, file stability, media metadata and SHA before retrying a download. A generated title alone does not prove completion: failed tiles can have titles too. Read provider error/Retry controls before collection.

Request a provider 1080p export only within the job’s budget and preserve it as a separate output. Inspect **both frame count and actual endpoint chronology** against the native file. In CLIPLIB-V2, five exports contained 188 frames versus 190 native, while one preserved all 192. These are actual job results, not proof that future exports will truncate. If an export drops clean source frames, make the required 1080p review copy from the complete native original without retiming, interpolation or added holds, and gate/review that exact derivative. Never shorten the archived original to match an export. Record the upscale method honestly.

Historical upscaling took 50 seconds to six minutes. Collect one export before starting another, checking the filesystem rather than a lingering toast. Download names and UI positions vary; use the actual observed file, never a guessed filename. Then:

```bash
python3 .claude/skills/_shared/veo/veo.py collect JOBDIR A1 --from ~/Downloads/<the new file>.mp4
```

It copies the take to `JOBDIR/veo/A1-flow-tN.mp4` (never overwriting), measures it, checks that it opens on the START
frame, and marks the clip done. If it says the take does not open on START, the wrong frame was picked: resubmit that
clip once with the right frames.

Measured 2026-10-17: the 1080p download is 1920x1080, 24 fps, 8.0 s, H.264 with an AAC soundtrack (Veo adds sound; the
edit mutes or replaces it), **no visible watermark** with the switch off (checked every second of the frame, corners
included). The invisible SynthID mark is always there and is not our concern.

## 6a. Preserve every collected take (Dan, 2026-11-16)

Every collected output must be accounted for in the library source archive, including rejected, unused and unreviewed takes. Follow `../cliplib/README.md` and the all-output filing rule in VIDEO-RULES.md. Preserve the full original, its SHA-256 and job/model provenance, merge the M2 source register and verify the Drive copy. The parent owns quality decisions and promotion of cleared clean parts into permanent usable library IDs; the runner never calls a raw take usable. Report any uncollected or unarchived output by exact ID, never silently skip it.

## 7. Report back (your final message)

- Per clip: id, status, file, resolution and length, seconds from submit to finished.
- Output reconciliation: successful generations, collected files, source-archive references and Drive verification, plus any exact pending IDs. Parent must supply usable keeper IDs and sheet/job-doc verification before closing the overall job.
- Batch wall time: first submit to last file collected.
- Credits before and after (open the avatar menu again, `veo.py credits --set N`).
- Anything that went wrong or a screen that did not match this runbook.
- Do NOT judge or approve the motion: the main agent runs the motion gate (`_shared/framecheck/clipcheck.py`) and the
  frame-reviewer before anything reaches Dan.
