---
name: opus-5-5-release
description: "Opus 5.5 launched 2026-09-22; matches or beats Fable 5.1 on Anthropic's benchmarks at 60% lower per-token price; the model-routing recommendation given to Dan"
metadata:
  node_type: memory
  type: reference
  originSessionId: f669596c-8694-4448-bc93-159611a3b01e
  modified: 2026-09-22T18:01:31.274Z
---

Claude Opus 5.5 (`claude-opus-5-5`) launched 2026-09-22. API $4/$20 per M tokens (Opus 5 $5/$25, Fable 5.1 $10/$50, Sonnet 5 $2/$10). Anthropic claims ~40% cheaper per task than Opus 5 and 30% faster output. Its own table has it ahead of Fable 5.1 on every listed benchmark (Terminal-Bench 4.0 66.4 vs 55.8, GDPval 1846 vs 1735, OSWorld 2.0 81.8 vs 80.7, Chartography 89.0 vs 88.4, HLE 67.7 vs 65.6). Writing is less formulaic ("less Claudish"). Thinking is always on; API default effort is medium. Caveat: at max effort it uses ~119k output tokens per task vs Fable 78k, so avoid max. Subscription 5-hour limits rose 20%.

Recommendation given to Dan 2026-09-22 (not yet applied to agent files or the queue config): Opus 5.5 becomes the default for planning, editing, writing, revisions and photo judgment; keep Fable 5.1 as the blind reviewer (model diversity) and as the escalation when Opus 5.5 misses something twice; Sonnet 5 for routine runners. Anthropic's own guidance: Fable only for problems Opus fails at higher effort.

Related: [[fable-included-in-max]], [[three-role-video-pipeline]], [[video-editing-executor-routing]].

Added 2026-09-30: Anthropic's full launch table also has Opus 5.5 ahead on FrontierCode 54.4 vs 50.3, CursorBench 57.8 vs 51.8, AutomationBench 40.0 vs 31.4, Terminal-Bench-Science 58.7 vs 52.6, and says the real gap "is narrower than these scores suggest". Artificial Analysis: Intelligence Index 58 vs 53, 92 vs 69 tok/s, index run cost $8.7k vs $13.1k; no measured category where Fable beats Opus. Anthropic still positions Fable for long-running, low-oversight, multi-app work and vision document analysis, without numbers. No public evidence Fable is measurably better at anything Dan does.

Update 2026-10-02: Dan adopted the fuller recommendation, Opus for ship-critical copy, design locks and routine first cuts; Fable demoted to escalation only. See [[model-routing-plan]].
