---
name: astra-vs-fable-verdict
description: "Sep 8 + Sep 9 2026 verdicts on offloading Abs By AI work to GPT-6 Astra — keep everything in Fable; Astra's only edge is GUI computer use, and the cheaper way to get an NLE timeline is an FCPXML bridge, not a GUI agent"
metadata:
  node_type: memory
  type: project
---

**Sep 8 2026 — which of seven task areas to offload to GPT-6 Astra (OpenAI, released Sep 3 2026):**
offload nothing. Astra's only clear superiority is driving GUI apps by computer use (Final Cut Pro,
Affinity Photo). Everything else depends on the calibrated skills, memory and measured gates in Claude
Code. Astra on ChatGPT Plus is not in chat mode (Work/Codex only, 5–45 msgs/5 h, cut ~4x after launch);
usable Astra needs Pro at $100–200/mo. API is $10 in / $50 out per M tokens.

**Sep 9 2026 — Dan asked about replacing the ffmpeg/Python pipeline with Astra driving Premiere or
Final Cut. Verdict: no, and the framing is wrong.** Three facts settled it:

1. **Our rejections are perceptual, not tooling.** Every one Dan has issued (audio twice, spray-tan
   patch, framing, coverage) is a "does it sound/look right" failure. A GUI editor does not fix those —
   a reference file and a gate row does. See [[audio-never-over-strip]], [[framing-standard-hair-anchored]].
2. **A GUI agent cannot give frame-exact repeatability.** Our warm-cache revision is 6.7 min and
   byte-reproducible; a clicking agent re-derives the edit each time. OSWorld 2.0: Astra 72.6 %,
   i.e. ~1 in 4 runs does not complete.
3. **The viral "Astra edited a whole video" demo was NOT Final Cut** — it drove HyperFrames, a web
   timeline tool, ~50 min and ~$60 of API for one video. The real FCP test was narrow (import,
   grade, sync).

**The better third path, and the actual recommendation: an FCPXML export from our EDL.** Final Cut has
no scripting API but reads/writes FCPXML, and FCPXML MCP servers already exist. Claude writes the
timeline; Dan (or an editor) opens it in FCP for eyes-on polish. No new subscription, no GUI agent, and
it keeps the caches and gates. If a GUI agent is ever used anyway, **Premiere beats Final Cut for it** —
UXP scripting (standard in Premiere 2026, ExtendScript EOL Sep 2026) lets an agent script instead of click.

**Hardware verdict:** do not buy a machine for the current pipeline. Measured bound is x264 across all
10 cores (81 % of a 19.1-min cold build); a second Mac buys one more concurrent build, not a faster one.
Free the existing Mac mini M2 Pro instead (honour the two-build cap). Buy only if he commits to a GUI
agent, which owns the screen for hours ([[computer-takeover-frustration]]) — then a second box is
mandatory, and an M4 Max Mac Studio (est. ~2x x264 throughput), not another mini.

Related: [[fable-included-in-max]], [[muhammad-trial-edit-analysis]], [[photo-retouch-recipe]].
