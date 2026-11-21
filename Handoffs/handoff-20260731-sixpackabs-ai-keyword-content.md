# Handoff: SixPackABS.com AI-keyword content pivot + "When will my abs show?" calculator

**Date:** 2026-07-31
**Project:** sixpackabs.com → Abs By AI funnel
**Business goal this serves:** Marketing performance (traffic growth that converts) + profitability

## Objective

Shift SixPackABS.com's new content toward search queries where Abs By AI is literally the answer ("what would I look like with abs", "AI body transformation app", etc.) — low-competition queries big fitness sites can't chase because they have no AI product — and build one free interactive tool, a **"When will my abs show?" calculator**, as the site's link magnet and email-capture engine. Together these make traffic growth and conversion the same project instead of two separate ones.

## Current State

- sixpackabs.com: WordPress.com Atomic site (blog_id `253647467`), 113 posts of general ab/nutrition/fat-loss content, ~533 views/month, ~4 months old. Ranking for competitive generic fitness terms is unrealistic at this domain age; long-tail and novel-topic queries are the opening.
- Existing content is solid informational filler but none of it targets the AI-transformation angle, and none of it links to Abs By AI (the conversion layer is a separate handoff: `handoff-20260731-sixpackabs-conversion-layer.md` — ideally shipped first, but not a hard blocker).
- The `anthropic-skills:blog-posts` skill exists in Claude Code and can write + schedule WordPress posts in batch (it embeds YouTube videos — useful once Dan's channel exists; for now posts can embed relevant third-party videos or none).
- No calculator or interactive tool exists on the site. 44 pages exist (compliance/info pages).

## Key Decisions Already Made

- **Content strategy = AI-angle long-tail, not generic fitness.** "How to do a deadbug" cannot outrank Healthline from a 4-month-old domain; "what would I look like with a six pack" has almost no serious competition and every searcher is a perfect Abs By AI prospect.
- **The calculator is the link-building strategy.** Free tools earn backlinks passively; no paid links, no mass guest-posting.
- **Show the calculator result immediately, then offer the email follow-up** ("get your week-by-week plan emailed") — don't gate the result behind an email. Gated results kill the shareability that makes the tool a link magnet.
- Every post and the calculator end in the same place: Abs By AI CTA with UTMs (`utm_source=sixpackabs&utm_medium=blog&utm_campaign=calculator` / `=post_<slug>`).

## Detailed Plan

1. **Keyword set.** Target these query families (each becomes 1–3 posts):
   - "what would I look like with abs / with a six pack" (the money query)
   - "AI body transformation (app/generator/free)"
   - "see yourself fit/muscular app", "fitness goal visualization"
   - "abs filter" / "six pack photo editor" (vs. the real thing — comparison angle)
   - "body fat percentage to see abs" (men/women variants — feeds the calculator)
   - "how long to get visible abs" (feeds the calculator)
   - "realistic 90 day body transformation what to expect"
   - "before and after abs (real examples / AI examples)"
   - Verify/expand with a keyword tool if available; otherwise Google autocomplete + "People also ask" mining is sufficient at this competition level.
2. **Content template per post:** directly answer the query in the first 150 words → substance (real numbers, honest expectations — reuse the body-fat visibility thresholds from step 4) → an AI-generated example transformation image, clearly labeled → CTA to try it on your own photo. 800–1,500 words, no listicle filler. 2–3 posts/week cadence.
3. **Write in the established voice.** Direct, honest, anti-hype — consistent with Dan's video-outline style (see memory `video-outline-style`: no generic listicles, real specifics). Claude writes these; they are brand-voice work.
4. **Build the calculator** as a WP page (`/abs-calculator/` or similar) using a custom HTML block — self-contained HTML/CSS/JS, no external dependencies, mobile-first.
   - Inputs: sex, current weight, waist measurement (or estimated body-fat range picker with reference images), weekly calorie deficit (with presets: mild/moderate/aggressive).
   - Logic: estimate current BF% → target visibility threshold (men: ~15% faint / 10–12% clearly visible; women: ~22% faint / 19–20% clearly visible) → pounds of fat to lose → weeks at chosen deficit (3,500 kcal/lb; cap aggressive projections and show a healthy-rate warning) → output a date ("Abs visible around March 14, 2027") with a simple timeline graphic.
   - Below the result: (a) "Get the week-by-week plan emailed" → email form into the existing Resend sequence (same `/api/subscribe` endpoint the conversion-layer handoff wires up); (b) primary CTA: "Or skip the wait — see the after photo right now, free" → absbyai.com with UTMs.
   - A "share your date" button (copies a text snippet) — cheap virality.
5. **Internal linking.** Add a link to the calculator from every existing post where it fits (the fat-loss and body-fat posts especially). This can be a one-pass programmatic edit or part of the `the_content` filter from the conversion-layer handoff. Add the calculator to the site nav.
6. **Verify.** Calculator math spot-checked against hand calculations for 6 input combos (both sexes, three deficits); mobile 375px + desktop rendering; email submit works end-to-end; UTM click-throughs land in PostHog.
7. **Close out:** dashboard check-off per AI_COORDINATION.md Rule 9.

## Things to Avoid / Lessons Learned

- **No medical claims.** The calculator gives estimates with a disclaimer line (reuse the tone of absbyai.com's `/disclaimer` page). Aggressive-deficit outputs must carry a caution, not encouragement.
- **Don't gate the calculator result behind email** (settled decision above).
- **Label AI-generated imagery** in posts as such — consistent with the compliance treatment shipped on absbyai.com 2026-07-30.
- Generic fitness content is explicitly deprioritized — if a post idea could appear on any fitness blog, it's the wrong post for this site right now.
- The repo is public; the calculator lives on WordPress, not in the abs-by-ai repo.

## Relevant Files & Locations

- WordPress: sixpackabs.com, blog_id `253647467` (WordPress.com MCP tools have confirmed access)
- Blog-post batch tooling: `anthropic-skills:blog-posts` skill in Claude Code
- Email endpoint + UTM/CORS work: `handoff-20260731-sixpackabs-conversion-layer.md` (ship that first if possible)
- Voice reference: memory `video-outline-style`; disclaimer tone: absbyai.com/disclaimer

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking (posts + calculator both) |
| **If Claude usage is high / approaching a limit** | Posts stay on Claude (Sonnet 5) — brand-voice work, batch them to economize. The calculator alone is well-specified single-page JS: Codex mini-tier, low effort, is fine for it. |

Task-type override: the articles are marketing copy → Always-Claude. Sonnet 5 is sufficient; Opus is not needed for either half.

## Starter Prompt for the Next Task

> Execute `handoff-20260731-sixpackabs-ai-keyword-content.md` in the Abs By AI project root. Goal: pivot sixpackabs.com's new content to AI-transformation search queries (keyword families listed in the doc) and build the self-contained "When will my abs show?" calculator page with email capture + Abs By AI CTA. First action: build the calculator page (it's the highest-leverage single asset), then write the first batch of 5 posts from the keyword list. Voice, thresholds, math rules, and the no-email-gate decision are all settled in the doc.
