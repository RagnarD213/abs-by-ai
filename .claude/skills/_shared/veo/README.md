# Veo motion: subscription first (Dan, 2026-10-17)

Every AI video clip (Veo motion from approved START/END frames) is generated in **Google Flow on Dan's Google AI Pro
credits**, by a background sub-agent driving his Chrome, while the main agent keeps editing. The paid Replicate API is
used only when Dan says **rush**, **accelerate** or **as fast as possible**, or when the credits have run out AND Dan
has approved paying. Claude and Codex both.

Dan: *"Default to the subscription; switch to the paid API only when I say rush, accelerate, or as fast as possible. If
the subscription credits run out, ask me before paying."*

## The routine inside an editing task

1. Frames approved and gated as always (`_shared/framecheck/README.md`). Nothing here relaxes frame approval.
2. Route: `python3 .claude/skills/_shared/veo/veo.py route --said "<Dan's latest instruction>"` prints `flow` or `api`.
3. Queue each clip: `veo.py add JOBDIR A1 --start A1-start.png --end A1-end.png --prompt-file A1.txt [--aspect 9:16]`.
   It refuses frames that have not passed the frame gate and reviewer, and stages small JPEG copies for upload.
4. **Claude:** spawn the `flow-veo` agent (`.claude/agents/flow-veo.md`, Sonnet 5 medium) with `run_in_background: true`
   and the JOBDIR, then go back to editing. In a session started before that agent file existed, spawn a general-purpose
   Sonnet agent told to read it first. **Codex:** follow `FLOW-RUNBOOK.md` in your own browser session (Chrome or
   computer use), as a parallel task if you have one.
5. When the agent reports, run `veo.py status JOBDIR`, then the motion gate (`_shared/framecheck/clipcheck.py`) and the
   frame-reviewer on every take, exactly as for API takes. Only gated takes go on a review page.
6. **Credits out:** the agent stops with `CREDITS_OUT`. Ask Dan once, with the clip count and the dollar estimate
   (Veo 3.1 Fast on Replicate: $0.10 per second, $0.80 per 8 s take). Only on his yes:
   `veo.py api JOBDIR A1 --paid-ok "<his words>"`. Rush: `veo.py api JOBDIR A1 --rush "<his words>"`.
   Paid takes still count against the per-video generation budget (VIDEO-RULES, "Video clip generation budget").

## What the subscription gives (measured 2026-10-17, the 5-clip test)

| | Flow on Google AI Pro | Replicate API (paid) |
|---|---|---|
| Cost | 20 credits a clip (Veo 3.1 Fast); 1,000 credits a month + 50 a day | $0.10/s, $0.80 for 8 s |
| Allowance | about 50 Fast clips a month, plus 2 or 3 a day from the daily 50 | no cap |
| Length | 8 s only in frames mode (trim in the edit) | 4, 6 or 8 s |
| Resolution | 720p generated, 1080p upscaled download (1920x1080, 24 fps) | 1080p |
| Watermark | none visible with "Visible watermarking" off (avatar menu); SynthID always | none visible |
| Speed | see `TEST-20261017.md` | about 80 to 130 s a take |
| Negative prompt | not supported (prompt must say what must not happen) | supported |

Other models in Flow, if a job asks: Veo 3.1 Lite 10 credits, Veo 3.1 Quality 100, Omni 1.1 Flash 12 (`--model`).

## Files

- `veo.py`: route, add, status, mark, collect (with the opens-on-START check), credits, api. Job state: `JOBDIR/veo/job.json`.
  Account-wide credit and spend log: `~/.absbyai-veo-ledger.jsonl` (Claude and Codex share it on this Mac).
- `FLOW-RUNBOOK.md`: the click-by-click Flow procedure. Flow changes its interface often; whoever finds a step that no
  longer matches fixes the runbook in the same session.
- `TEST-20261017.md`: the timed 5-clip test and the watermark check.
