# Handoff: set up the Social Response Marketing project

**Created:** 2026-11-02 by the SRM Website task (Claude Opus 5.5).
**Recommended:** Claude Opus 5.5, high effort. Task name: `SRM Project Setup`.

## Goal

Dan, 2026-11-02: "we need to create a new project for this in order to have all our context separate from AbsByAI." Build a separate project for Dan's ad agency, Social Response Marketing (SRM): the Upwork client work, cold outreach, the agency website and the agency's videos. Abs By AI keeps fitness content, the app and its ads.

Done means Dan can open the new project in the Claude desktop app and Codex, and a fresh session there has all the context with nothing loaded from Abs By AI's 2,500-word board and instruction files. The Upwork routine keeps running without a missed day. Abs By AI keeps working too.

## Decisions already made (don't ask Dan again)

- **Folder:** `~/Projects/Claude/Projects/Social Response Marketing` (a sibling of `Abs By AI`, `Sell My House` and the others).
- **Git:** its own repo, **private** on GitHub (`gh repo create --private`). The Abs By AI repo is public, and this project will hold prospect names, emails and pipeline data. Never make it public.
- **Copy first, then cut over.** Copy everything into the new project and verify it there. Remove the SRM-only originals from Abs By AI only after Dan confirms the new project works, because that removal is the one step that needs his yes. Moving or renaming a file another live session uses breaks that session.
- **Production skills stay shared, not duplicated.** The skills that make ads (`scriptwriting`, `ad-edit`, `shortad-from-longform`, `dan-voice` and the `dan-voice-writer` agent, `_shared/codex-image.sh`, `revisions`) serve both businesses. Don't fork them. Pick one of these and record which:
  (a) Symlink them into the new project's `.claude/skills/` (recommended: one copy keeps improving for both).
  (b) Point to their Abs By AI paths in the new CLAUDE.md.
  The SRM-only skill, `upwork-pitch`, moves fully into the new project.
- **Standing rules that carry over** (paste them into the new CLAUDE.md/AGENTS.md as rules, not as references back to Abs By AI): Dan's two wrap-up boxes; plain language for a non-technical owner; bias to action on reversible work; no em dashes in anything a client reads; no calls in offers (memory `upwork-no-calls-agentic-income`; Dan's goal is agentic income he is not involved in); official ad-spend numbers (memory `official-ad-spend-numbers`); Upwork only through the official connector; never claim no AI is used; outreach only from dan@socialresponsemarketing.com; nothing goes to clients or prospects without Dan's batch approval; secrets never in the repo; Claude cannot type passwords or payment details; model routing (Opus 5.5 high for writing and design, newest GPT Sol for Codex work); the Codex-subscription rule for generated images. Leave out every fitness, video-release, Blotato and app rule.

## What to bring over

Source paths are relative to `~/Projects/Claude/Projects/Abs By AI` unless shown in full.

**1. Brand and logos**
- The original 99designs logo files (Dan's, 2019, designer "p h i l o s o p h e r"): `sites/srm/brand/logo/srm-logo-stacked-99designs.zip` (stacked logo, 70 files: AI, EPS, PDF, PNG, PSD, every colour) and `sites/srm/brand/logo/srm-logo-horizontal-99designs.zip` (the side-by-side logo "SOCIAL RESPONSE MARKETING 2", which the website header uses). Source page: https://99designs.com/handover/713668/files. Unzip into `brand/logo/stacked/` and `brand/logo/horizontal/`. Brand blue is in the PNGs; sample and record it in `brand/README.md`.
- Dan's photos for the site: `sites/srm/brand/photos/` has his Upwork avatar original (made with Codex, 1384x1136 webp, as Dan sent it in chat 2026-11-02), a 1200 px JPG of it, and the stage photo (old site's `dameet.png`).

**2. Website**
- `sites/srm/` (PLAN.md, COPY.md, mockups/, tools/build.py, public/ = the rejected first draft). → `site/`.
- The design canvas: https://claude.ai/artifact/LDm9v62hh1bBCd8CpU1UG1 (private, version 8). Dan picked **Option C**. R2 shows two boards: today's version (moving ad strip) and the permanent version (Dan's video on top). Older options A and B are still files there but are off the canvas. All images live in that artifact's asset store.
- Reference pages: agency gallery https://claude.ai/artifact/SvJo6ndVJPXgMQ5KpVxUKt (Dan chose Pilothouse), retired blind logo test https://claude.ai/artifact/AZ3KFBfqNcxq4exGGud15q (the old logo won, so the test is dropped), first draft https://claude.ai/artifact/PLdr99pEjRUh1aePA7waei.
- Website handoff: `Handoffs/handoff-20261030-social-response-marketing-website.md` (domain, Cloudflare redirect rule id, email routing, go-live steps). The website task continues in the new project after setup.

**3. Proposal and outreach method**
- Skill `.claude/skills/upwork-pitch/` (SKILL.md, LEARNED.md, TRACKER.md, LAUNCH-CHECKLIST.md, TEMPLATE-outreach-email.md).
- Plans: `Docs/UPWORK_CLIENT_PLAN_MERGED_20261029.md`, `Docs/UPWORK_CLIENT_PLAN_20261029.md`, `Docs/upwork-pipeline/upwork-pipeline.html`.
- Handoffs: `handoff-20261007-upwork-job-applications.md`, `handoff-20261007-upwork-profile-and-portfolio.md`, `handoff-20261029-upwork-client-acquisition.md`, `handoff-20261029-upwork-profile-finish.md`, `upwork-profile-draft.md`, `upwork-profile-working-brief.md`.
- Upwork Pipeline page (live data, stays where it is): https://claude.ai/artifact/8PaJHa8sq1DpB4mf2oU7xT.
- Routine `~/.claude/scheduled-tasks/upwork-proposals-daily/SKILL.md`: its prompt names the Abs By AI folder and skill paths. Update the paths and working folder only after the new project's copy is verified, and make the switch between two daily runs. Then confirm the next run works. Use the scheduled-tasks tools, not hand edits, if they can set the folder.
- Upwork account facts: freelancer org_uid 2107829488368488044, profile https://www.upwork.com/freelancers/~016109a7105ec3bf5d.

**4. Ad library (the proof)**
- `sites/srm/proof/`: every SixPackAbs ad's live YouTube views (`sixpackabs-ad-views-20261102.json`, 1,047 ads, pulled with the YouTube API using `YOUTUBE_REFRESH_TOKEN`), the source tracker spreadsheet, the YouTube frames (`frames/`) and every image on the canvas (`site-assets/`, with `blob-ids.json` mapping canvas asset ids to files). Write `proof/TOP_ADS.md` with the 8 ads on the site (IDs, views, spend, Dan's role).
- `Media/upwork-catalog-covers/` (portfolio and catalog covers).

**5. Videos**
- Planned: generic pitch, 5-second name openings, high-value pitches for the top 3 prospects (LAUNCH-CHECKLIST), the Upwork intro video, and the website's top video ("Why My Ads Sell"). None is filmed yet. Make `videos/README.md` the list, with status and where each will live. Raw footage stays on the external drives. Write only paths.
- Editing still uses the shared production skills and render queue in Abs By AI. Note that link in the new CLAUDE.md.

**6. Memory**
- Copy these from `~/.claude/projects/-Users-danielrose-Projects-Claude-Projects-Abs-By-AI/memory/` into the new project's memory folder (created when the first session opens there; use `Docs/memory/` in the new repo as the copy if it doesn't exist yet): `upwork-no-calls-agentic-income`, `official-ad-spend-numbers`, `socialresponsemarketing-email`, `no-ad-agency-mention`, `google-ads-api-client`, `claude-codex-major-decision-template`, plus any entry whose body mentions Upwork, SRM, Healthy Back Institute, Mind Movies or Spy Briefing (grep). Keep the voice entries (`dan-voice-guide`, `voice-corpus-sources`) linked, not copied. Don't copy private hub entries (`hub-private`, contact info) into a git repo.

**7. Status**
- Board entries to move into the new project's own short `STATUS.md` (and delete from Abs By AI's board once moved): "Upwork Clients", "Upwork client plan PUSH-PENDING" (if still open), "SRM Website".
- Dan's open SRM decisions (pricing after the free ad, "I personally write the scripts" vs. hands-off goal) go in the new project's `DECISIONS.md`.

**8. Secrets**
- No secrets in the repo. Create `~/.srm-secrets.env` (0600) holding only what SRM uses (Cloudflare token for the domain, YouTube read keys if needed), copied from `~/.absbyai-secrets.env`. Record the variable names, never the values, in the new CLAUDE.md.

## Steps

1. Read this file, `sites/srm/PLAN.md` and the upwork-pitch skill. Check that the "Upwork Proposals" session and the SRM Website task are idle. Don't edit files another live session is writing.
2. Create the folder, `git init`, `.gitignore` (secrets, `.DS_Store`, big media), CLAUDE.md (one line: `@AGENTS.md`), AGENTS.md (the carried-over rules above, under 1,200 words), STATUS.md, DECISIONS.md and a README index.
3. Copy items 1 to 6.
4. Set up skills: move `upwork-pitch` and link the shared production skills (pick option a or b and record it).
5. `gh repo create <name> --private --source . --push`; confirm it is private with `gh repo view --json visibility`.
6. Open a test session in the new folder (or read it from a fresh subagent) and check that it can answer: where is the canvas, what are the no-call and ad-spend rules, how does a proposal get drafted. Fix any gaps.
7. Switch the `upwork-proposals-daily` routine to the new folder between runs, then confirm the next run reads the new skill path.
8. Report to Dan with the folder path, the repo link, what moved, and a list of the SRM-only originals still in Abs By AI. Ask once, as a batch with a count, whether to remove them. Then remove them only after his yes.

## Risks

- If the Upwork routine changes folders mid-run, a day of proposals can be lost. Make the switch between runs.
- The Abs By AI repo is public. Nothing copied into it during this work may include prospect data.
- Abs By AI's main folder has 60+ unpushed commits and a live staged file blocking `safe-push.sh`. Don't try to fix that here. Push this handoff with `safe-push.sh` and leave a board note if it is blocked.

## Starter prompt

> Name this task SRM Project Setup. Read Handoffs/handoff-20261102-srm-new-project-setup.md and do what it says: build the separate Social Response Marketing project with its own private repo, bring over the logos, website designs, proposal method, skills, videos list and memory, switch the Upwork routine over between runs, then report and ask me once before removing anything from Abs By AI.
