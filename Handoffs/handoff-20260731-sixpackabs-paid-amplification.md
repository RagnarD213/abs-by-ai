# Handoff: Paid amplification playbook — boost only proven creative, aimed at absbyai.com

**Date:** 2026-07-31
**Project:** Abs By AI / sixpackabs.com
**Business goal this serves:** Profitability (spend only where a payback path is measurable)

## Objective

Define and then execute the rules for the very limited ad budget: **no paid traffic to the blog** (it can't pay you back), **no spend on unproven creative**. Money only amplifies a video that has already won organically — or the already-approved AI ad — and it always lands on absbyai.com, where 3 free generations and the paywall can actually convert it. This handoff is part playbook (write the rules down, set up measurement) and part execution (run the first small test when a trigger fires).

## Current State

- **Budget:** very limited, per Dan (2026-07-31). No campaigns exist anywhere.
- **Ready creative exists today:** `ad-factory/the-upload/final/the-upload_v1_9x16.mp4` (70s narrator cut) and `_v2_firstperson_9x16.mp4` (76s) — Dan-approved, captioned, 9:16. Hook variants were deliberately deferred "until ad traffic starts" — that decision point is THIS task.
- **Compliance prerequisite is DONE:** the 8 Google Ads compliance pages (terms, refunds, contact, disclaimer, etc.) shipped and live-verified 2026-07-30 (commit `ae92324`), plus the AI-GENERATED labeling on the proof strip and the support@absbyai.com forwarder (closed 2026-07-31). absbyai.com is ready to receive paid traffic without policy landmines.
- **Measurement:** PostHog project 458833 tracks the full absbyai.com funnel (generation, paywall, checkout events). No ad-platform pixels are installed.
- **Organic signal sources** (what defines a "winner"): the YouTube channel from `handoff-20260731-sixpackabs-video-centerpiece.md` doesn't exist yet — so until it does, the only actionable spend is a small controlled test of "The Upload."

## Key Decisions Already Made

- **Never buy blog traffic.** The blog has no monetization; paid clicks go to absbyai.com only.
- **Boost winners, don't gamble on unknowns.** A video earns budget by outperforming organically first. Exception: "The Upload" is pre-approved creative and may get one small controlled test without an organic signal.
- **Boost on the platform where the content won** (a Short that pops → YouTube/Google Ads video campaign; a Reel → Meta boost; TikTok → Spark Ads on the original post, which keeps its organic engagement).
- **Every paid click carries UTMs** (`utm_source=<platform>&utm_medium=paid&utm_campaign=<creative-slug>`), so PostHog attributes generations/emails/trials to the creative without needing platform pixels on day one.

## Detailed Plan

1. **Write the trigger rule down where it'll be seen** (this doc is the source of truth):
   - A video qualifies for boosting when it does ≥3× the channel's median views in its first week, OR shows retention/CTR clearly above the channel's norm (YouTube Studio), OR a vertical clip organically breaks out on any platform.
   - Until the channel has ≥5 uploads, "median" is unstable — during that period only "The Upload" test (step 3) is authorized spend.
2. **Set budget guardrails:** $5–10/day per test, hard cap **$50–100 per creative test**, one test running at a time. Kill early if spend hits half the cap with zero generations attributed.
3. **First test — "The Upload":** run v1 vs v2 (first-person) as a 2-variant test on ONE platform. Recommendation: TikTok or Meta Reels first (cheapest CPMs for cold 9:16 creative; Google/YouTube can come second) — OPEN: Dan picks the platform and confirms the card/account to use. Destination `https://absbyai.com/?utm_source=<platform>&utm_medium=paid&utm_campaign=the-upload-v1` (v2 respectively). Dan does the ad-account setup and payment steps himself; Claude preps targeting notes, copy, and the exact UTM URLs, and handles all measurement.
4. **Measure in PostHog per creative:** sessions → uploads → generations → email captures → paywall hits → purchases/trials, each divided into cost. The three numbers that matter: **cost per generation** (leading indicator), **cost per email**, **cost per trial/purchase** (the verdict). Build a saved PostHog insight or dashboard for `utm_medium=paid` before the first dollar is spent.
5. **Decision rules after a test:** if cost-per-trial beats ~1 month of membership revenue ($19.99), scale gently (raise daily budget ~50%, add the second platform). If cost-per-generation is good but nothing converts downstream, the problem is the app funnel, not the ad — stop spend and fix the funnel first. If nothing generates, kill and produce the deferred hook variants (`.claude/skills/make-ad/SKILL.md` step 7) before spending again.
6. **When the YouTube channel is live and has history,** apply the step-1 trigger to shoot content and repeat steps 2–5 for each qualifying winner.
7. **Close out each test** with a short results note appended to this doc's section in AI_COORDINATION.md (spend, the three costs, verdict) so the next test doesn't re-derive anything. Dashboard check-off per Rule 9 when the playbook's first test completes.

## Things to Avoid / Lessons Learned

- **No spend before the PostHog paid-traffic dashboard exists.** Unmeasured spend on a tiny budget is pure waste.
- **Don't run Google Ads first** — its policy machinery is the most sensitive to health/body-image claims. The compliance pages protect us, but cut teeth on TikTok/Meta CPMs first.
- **Don't spend on hook variants speculatively** — that work was explicitly deferred until a live test shows the current hooks failing.
- Claude cannot and must not enter payment details or create ad accounts — Dan does those steps; everything else (copy, URLs, measurement, verdicts) is Claude's.
- Body-transformation ad policies on Meta/TikTok restrict "idealized body" framing and before/after imagery in some placements — check each platform's current rules when building the test, and keep the AI-GENERATED labeling in the creative (it's already in "The Upload").

## Relevant Files & Locations

- Creative: `ad-factory/the-upload/final/the-upload_v1_9x16.mp4`, `the-upload_v2_firstperson_9x16.mp4`
- Ad production skill + lessons: `.claude/skills/make-ad/SKILL.md`
- PostHog: us.posthog.com, project 458833 (funnel events: `generation_verifier`, paywall/locked events, checkout)
- Compliance pages (live): absbyai.com/terms, /refunds, /contact, /disclaimer
- Competitor benchmarks: memory `youtube-ad-competitor-research` (MadMuscles spend patterns)
- Upstream: `handoff-20260731-sixpackabs-video-centerpiece.md` (source of future winners)

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking |
| **If Claude usage is high / approaching a limit** | Claude Sonnet 5 anyway — this task is small (a PostHog dashboard, ad copy, URLs, a walkthrough with Dan); there's no heavy build to offload to Codex. |

Task-type override: ad copy + spend-strategy judgment → Always-Claude. Cheapest competent model (Sonnet 5) is right; no Opus.

## Starter Prompt for the Next Task

> Execute `handoff-20260731-sixpackabs-paid-amplification.md` in the Abs By AI project root. Goal: set up the paid-amplification playbook — build the PostHog paid-traffic dashboard (sessions → generations → emails → trials for utm_medium=paid), then prep the first controlled test of "The Upload" v1 vs v2 ($5–10/day, $50–100 cap) with exact UTM URLs and platform-compliant ad copy. First action: build the PostHog dashboard (no spend is authorized before it exists), then ask Dan the one OPEN question: which platform for test #1 (recommendation: TikTok or Meta Reels, not Google, for the first test).
