# Codex: adopt the RO-16 review-page format for every approval packet

**Written:** 2026-09-30 by Claude (Opus 5.5) at Dan's request. **For:** Codex. **Model:** GPT-6 Sol, medium (a bounded
template and tooling change with routine verification; no creative choices).

## Why
Dan reviewed Claude's RO-16 round 1 page and said, in his words: *"I think you made some significant improvements to our
process too, beyond what Codex did. I like the 'What I Decided' section. I like the format of this page, where the first
minute is right on top, the AI opener frames are below that, and all graphics and clips are in order. That makes it
significantly faster for me to review than looking at all this in the browser panel one at a time."* He asked for Codex to
adopt it.

## The standard (already written into the shared docs)
Read `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, section **"The review page: one layout, and a 'What I decided' list on
every packet"**, and the matching entry at the top of `.claude/skills/_shared/VIDEO-RULES.md`. Order on the page:
1. Header: the video, what is locked, then "Your decisions (N)", numbered, 2-3 options each, recommendation first.
2. The first minute (or current finished section) in one lazy player at the top.
3. AI opener / new AI clip START and END frames side by side, with action, duration and cost.
4. **"What I decided (overrule anything)"**: one plain-language line per call made without asking.
5. Every graphic and clip in timeline order, **three per row**: still on its real graded frame, ID, time range, copy,
   source, collapsible speech before / during / after.
6. One reply box, pre-filled, with a Copy button.

Reference page (open it in Chrome): serve `cd /Volumes/Extreme/_edit_work/ro16/round1 && python3 -m http.server 8794 --bind 127.0.0.1`,
then http://127.0.0.1:8794/index.html. Generator to copy: `.claude/skills/longform-edit/reference/ro16/page.py`
(reads `stills.json`: id, kind, t0, t1, copy, src, note, before/during/after speech).

## What to change
1. Codex skills: `~/.codex/skills/long-form-content-edit/`, `vsl-edit/`, `abs-edit-ad/` and their copies under
   `Media/codex-video-trial/skills/`: wherever a packet or review page is described or generated, adopt this order and the
   "What I decided" list. Keep each skill's existing approval rules (the VSL keeps its deeper approval cadence; only the page
   layout changes).
2. Any page builder Codex uses for packets (for example the WV-01 / RO-01 `recipe/page*.py` pattern) becomes one shared
   builder that takes the same `stills.json` shape, so every video gets the identical page.
3. `scripts/edit-queue/review_page.py` (Dan's queue review page, port 8830): check whether its asset-packet view should
   follow the same order; if it is only for delivered cuts, leave it and say so in your report.
4. Verify: build one real page from an existing packet (RO-01 or WV-01 records), confirm every `src`/`href` returns 200 over a
   local server, the three-per-row grid collapses to one column on a phone width, and there are no em dashes in the page copy.

## Not in scope
No re-rendering of any video, no new approvals, no changes to thresholds or gates.

## Deliver
Commit the skill and script changes (never media; the repo is public), report to Dan in plain language with the page URL of
your verification build.

## Starter prompt (Codex)
> Read `Handoffs/handoff-20260930-codex-adopt-review-page-format.md` and execute it: adopt the RO-16 review-page layout
> (first minute, AI frames, What I decided, all graphics and clips three per row) in every Codex video skill and page
> builder, verify one real page in Chrome, commit, and report back.
