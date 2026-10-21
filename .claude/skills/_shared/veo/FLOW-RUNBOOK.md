# Flow runbook: generating Veo clips on the Google AI Pro subscription in Chrome

For the `flow-veo` background agent (`.claude/agents/flow-veo.md`) and for Codex driving its own browser. Mapped on
2026-10-17 against flow.google.com (frontend build `boq_labs-ai-sandbox-frontend_20261016`). Flow changes its interface
often: if a step below no longer matches the screen, find the control by its label, finish the job, then fix this file.

You get a job folder. Everything you need is in `JOBDIR/veo/job.json`: per clip the `upload_start` / `upload_end` JPEGs,
the `prompt`, `aspect` and `model`. Only clips with `"status": "queued"` and `"route": "flow"` are yours.

## 0. Before you start

- Chrome tools only (`mcp__claude-in-chrome__*`), in your own new tab (`tabs_create_mcp`). Never touch other tabs.
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
- Model dropdown: **Veo 3.1 - Fast** unless the clip says `lite`, `quality` or `omni` (`omni` = **Omni 1.1 Flash**). Since 2026-10-21 a job often mixes models (a Veo clip `A3` and its Omni twin `A3o`, see README "Which model and how many takes"): **re-check the dropdown before EVERY submit** and switch it to that clip's model; it is not a set-once setting in a mixed job. Omni's length: use the clip's `seconds` (4, 6, 8 or 10); Veo Frames mode stays 8 s.
- Count **x1**.
- Read the "Generating will use N credits" line. Press Escape.

Frames mode on Veo 3.1 Fast always makes an 8-second 720p clip; there is no 4 or 6 s choice. The edit trims to the
clip's `seconds`. Flow has no negative-prompt field: the `negative` text is not sent (the prompts already say what must
not happen).

## 4. Upload the job's frames (once per job)

Flow builds its file box only when "Upload media" is clicked, which would open a Mac file picker you cannot operate.
Hook it first, in the project tab:

```js
if(!window.__veoHook){window.__veoHook=true;const o=HTMLInputElement.prototype.click;
HTMLInputElement.prototype.click=function(){if(this.type==='file'){this.id='veo-file-input';
this.style.cssText='position:fixed;left:0;top:0;width:40px;height:40px;opacity:0.01;z-index:99999';
if(!this.isConnected)document.body.appendChild(this);return;}return o.call(this);};}
```

Then click **Start** in the prompt box (opens "Select a frame image"), click **Upload media** at its bottom left, and
`find` "file input" to get its ref. `file_upload` with up to 10 MB per call: every `upload_start` / `upload_end` path of
the queued clips (each JPEG is about 0.4 MB, so all of a job's frames go in one or two calls). The first upload of the
day may show "Rights to use this image": Dan agreed to it on 2026-10-17 for our own AI frames, so click **I agree**.
**Wait until every upload has finished** (no percentage left on any tile in the grid behind the picker) before you assign
any frame: the picker list re-sorts while uploads complete, and a click lands on a different file. Close the picker with
its X. After a page reload the hook is gone: run it again before the next upload.

## 5. Submit each clip

For each queued clip, in job order:

1. **Fill END first, then START (measured 2026-10-20: with START filled first, the End picker's Add landed the START image in both slots).** Clicking a filled slot empties it. In each picker type the file name, wait for the preview to show the right frame, then click **Add to prompt** (never the result row). Slot thumbnails are square center crops, so hands at the edges vanish: compare faces/poses, not edges. Old order, for reference: Click **Start** → type the clip's exact start file name (`A1-start`) in "Search assets" so only that file is listed
   (it is highlighted already) → click **Add to prompt** directly. Do not click the result row: on the test that sometimes
   closed the picker and added the frame on its own. The End picker is wider, so its Add to prompt button sits further right.
2. If the clip has an end frame: click **End** → search `A1-end` → click it → confirm the name → **Add to prompt**. Zoom on
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

To get the file: ⋮ **More options** → **Download** → **1080p Upscaled** (720p "Original size" only if 1080p is missing;
4K needs Ultra, never click its Upgrade). Upscaling took 50 s on 2026-10-17 but 1.5 to 6 minutes on 2026-10-20 (other Flow tabs queue behind each other); Flow asks you not to run several at once. Rename the tile first (it names the file `P1_1080p_<timestamp>.mp4`), then poll `~/Downloads/<id>_*.mp4`: start
one, wait until the file is in `~/Downloads` (usually `<tile title>_1080p_<YYYYMMDDHHMMSS>.mp4`; once it came without
"1080p" in the name and was still 1920x1080), then the next. Watch `~/Downloads`, not the "Upscaling" toast, which lingers
for minutes. The submenu is translucent for a moment after it opens: 1080p Upscaled is its third entry. Then:

```bash
python3 .claude/skills/_shared/veo/veo.py collect JOBDIR A1 --from ~/Downloads/<the new file>.mp4
```

It copies the take to `JOBDIR/veo/A1-flow-tN.mp4` (never overwriting), measures it, checks that it opens on the START
frame, and marks the clip done. If it says the take does not open on START, the wrong frame was picked: resubmit that
clip once with the right frames.

Measured 2026-10-17: the 1080p download is 1920x1080, 24 fps, 8.0 s, H.264 with an AAC soundtrack (Veo adds sound; the
edit mutes or replaces it), **no visible watermark** with the switch off (checked every second of the frame, corners
included). The invisible SynthID mark is always there and is not our concern.

## 7. Report back (your final message)

- Per clip: id, status, file, resolution and length, seconds from submit to finished.
- Batch wall time: first submit to last file collected.
- Credits before and after (open the avatar menu again, `veo.py credits --set N`).
- Anything that went wrong or a screen that did not match this runbook.
- Do NOT judge or approve the motion: the main agent runs the motion gate (`_shared/framecheck/clipcheck.py`) and the
  frame-reviewer before anything reaches Dan.
