# Veo motion: subscription first (Dan, 2026-10-17)

Every AI video clip (Veo motion from approved START/END frames) is generated in **Google Flow on Dan's Google AI Ultra
credits** (upgraded from Pro to Ultra 5x, $99.99/mo, on 2026-10-20: 10,000 credits a month plus 50 a day), by a background sub-agent driving his Chrome, while the main agent keeps editing. The paid Replicate API is
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

## Which model and how many takes (Dan, 2026-10-21)

Credits are not the limit on Ultra (about 1,000 Veo Fast clips a month), so when in doubt, generate more, not less. Dan:
*"If you're in doubt as to which one is better, I prefer you generate with both, given that we have the subscription now
and there aren't per-clip generation costs."*

- **Default:** Veo 3.1 Fast (`--model fast`), one take. Won or tied every pair of the 2026-10-21 blind bake-off.
- **Important clips** (a hook, an ad opener, the first few seconds of any video): **two Veo takes** (`--takes 2`); show
  Dan the better one, or both if they are close.
- **Generate with BOTH Veo and Omni** (queue the Omni twin as `<ID>o`, e.g. `A3` fast + `A3o` omni, same frames and
  prompt) when the clip needs any of:
  1. one continuous shot longer than 8 s (Omni goes to 10 s; Veo Frames mode is fixed at 8 s);
  2. a short 4 or 6 s clip where the action must fill the length;
  3. a fix to one detail of an existing clip Dan otherwise likes (Omni can edit a clip from an instruction; still
     generate a fresh Veo take of the same shot alongside it);
  4. a shot built from several reference images (a specific product plus a specific setting).
- **In doubt whether a clip falls in one of these, or which model suits it: generate both.**
- **Exception:** any shot showing Dan's body shirtless or in swimwear is Veo only. Omni refused one twice
  ("reputational risk"); do not spend a run on it.
- Every take of either model goes through the same motion gate and reviewer before Dan sees it. On the review page,
  label which model made each take only after Dan picks, unless he asks.

## Subscription upgraded (Dan, 2026-10-20)

Dan: *"We've upgraded our Google Video Generation subscription. Try it again, and do it on subscription."* The Flow balance read
9,830 credits right after the upgrade (it had been 10 that afternoon, when four editing sessions drained the Pro allowance). At
20 credits a Fast clip that is about 490 clips, so plan retakes on the subscription; the paid API stays for "rush" only. The
Pro figures in the table below are history; read the live balance (`veo.py credits`) before a big batch.

## What the subscription gives (measured 2026-10-17 on Pro, the 5-clip test)

**Ultra since 2026-10-20:** 10,000 credits a month + 50 a day. Live Flow rates on Ultra (read 2026-10-20): **Veo 3.1 Fast 10, Lite 5, Omni 1.1 Flash 12** per 8 s clip, so about 1,000 Fast clips a month. Omni bake-off (`/Volumes/Extreme/_edit_work/omni-bakeoff-20261020/`, blind page on :9071, key in `blind-key.json`): Omni refused the Top 5 Zepbound Tips shirtless 9:16 pair twice ("reputational risk"), Veo made it. **Result (Dan, 2026-10-21, blind):** 2 ties, Veo preferred on the other 3, Omni preferred on none ("very close for all of them"). Decision: **Veo 3.1 Fast stays the default**; Omni only alongside Veo in the cases under "Which model and how many takes".

| | Flow on Google AI Pro | Replicate API (paid) |
|---|---|---|
| Cost | $0 extra; 20 credits a clip (Veo 3.1 Fast); 1,000 credits a month + 50 a day | $0.10/s, $0.80 for 8 s |
| Allowance | about 50 Fast clips a month, plus 2 or 3 a day from the daily 50 | no cap |
| Length | 8 s only in frames mode (trim in the edit) | 4, 6 or 8 s |
| Resolution | 720p generated, 1080p upscaled download (1920x1080, 24 fps) | 1080p |
| Watermark | none visible with "Visible watermarking" off (avatar menu); SynthID always | none visible |
| Speed | 5 clips in about 10 min wall (all submitted in 2 min; about 70 s to generate each; the one-at-a-time 1080p download is the bottleneck) | about 80 to 130 s a take, run in parallel |
| Negative prompt | not supported (prompt must say what must not happen) | supported |

Other models in Flow, if a job asks: Veo 3.1 Lite 10 credits, Veo 3.1 Quality 100, Omni 1.1 Flash 12 (`--model`).

## Files

- `veo.py`: route, add, status, mark, collect (with the opens-on-START check), credits, api. Job state: `JOBDIR/veo/job.json`.
  Account-wide credit and spend log: `~/.absbyai-veo-ledger.jsonl` (Claude and Codex share it on this Mac).
- `FLOW-RUNBOOK.md`: the click-by-click Flow procedure. Flow changes its interface often; whoever finds a step that no
  longer matches fixes the runbook in the same session.
- `TEST-20261017.md`: the timed 5-clip test and the watermark check.

The background agent itself is not free: the 5-clip test used about 205,000 Sonnet tokens of Claude allowance (about
40,000 a clip, mostly screenshots). Batch clips into one agent run per job rather than one agent per clip.

## Traps (RO-14 round 2, 2026-10-20)

- **Never run two `veo.py api` calls on one job at once.** Each rewrites `job.json` whole, so parallel runs overwrote each other
  (a finished take's record and a just-added clip both vanished). Run paid takes one after another, or in separate job folders.
- **Replicate refuses some frames with E005 ("input or output was flagged as sensitive"), at $0.** Flow accepted the same frames.
  RO-14: a restaurant frame with a low-cut dress failed even START-only, so it went back to Flow; a sports-bar pair passed only
  START-only (the END frame tripped it). Try START-only once, then Flow.
- **Chrome can stop saving Flow downloads mid-job (2026-10-20, about 19:00).** Flow said "downloaded" but nothing reached
  ~/Downloads after a dozen downloads in a row (likely Chrome's "automatic downloads" block for flow.google.com). The agent
  cannot fix it: the media URL is signed, the browser tools hide signed URLs, and a local POST waits on Chrome's local-network
  prompt. Dan has to allow automatic downloads for flow.google.com (address-bar icon), then a fresh agent collects the tiles.
  Download right after each clip finishes rather than batching ten at the end.
- **Veo still fails hand-and-object continuity often.** RO-14 (2026-10-20): about 20 takes (Fast, paid, Quality) for five
  food/prop gags; no full take passed (nuggets merge, a knife becomes a fork, a donut box refills, a straw slides, a lifted
  scale doubles its display). START/END frames whose prop geometry cannot connect (a display on the near corner on the floor,
  on top when held) make it worse. Plan clean 2 to 3 s windows from the start, or frames that need no object to change.
