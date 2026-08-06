# Handoff: Video centerpiece — YouTube launch + SixPackABS.com video integration (post-shoot)

**Date:** 2026-07-31
**Project:** Abs By AI + sixpackabs.com
**Business goal this serves:** Marketing performance (video is the primary traffic engine for fitness) + app adoption

## Objective

Once Dan's video shoot happens (planned ~2026-08-03), make video the centerpiece of the whole traffic strategy: launch the YouTube channel, publish the shoot content with proper SEO packaging, cut vertical clips for Shorts/TikTok/Reels, swap the sixpackabs.com homepage hero to the featured video, and give every video a companion blog post so each upload also creates a search asset. Video out-pulls the blog in fitness by an order of magnitude; the blog's job becomes catching the search demand each video creates.

## Current State

- **PREREQUISITE: the shoot.** Outlines were the focus of the 2026-07-27 content session; shoot target ~2026-08-03. This handoff cannot start until footage exists. If outlines still need finishing, that's the prior task.
- **Raw material already on disk:** `abs by ai gemini clips/` ("6 ways to get abs with AI" intro clips), `B roll/` (ab workout, deadlift, jump rope, m-100s, interview b-roll), `abs by ai images/` + `abs by ai images for future videos/`.
- **A finished AI ad exists:** `ad-factory/the-upload/final/the-upload_v1_9x16.mp4` (70s) and `_v2_firstperson_9x16.mp4` (76s) — Dan-approved, 9:16, captioned. Usable as channel content or pinned product demo, not just as a paid ad.
- **Reusable production tooling from the ad pilot** (all in `ad-factory/` + `.claude/skills/make-ad/SKILL.md` Lessons): ffmpeg-static assembly scripts, the canonical caption spec, and the Whisper word-timestamp caption pipeline (`assembly/captions-from-words.js` — captions that can't drift). This directly serves Shorts/Reels cutdowns.
- **No YouTube channel exists yet** (the VidTao competitor research in memory `youtube-ad-competitor-research` identified MadMuscles' $487M/yr playbook as the model).
- sixpackabs.com homepage hero: the conversion-layer handoff (`handoff-20260731-sixpackabs-conversion-layer.md`) installs a before/after image hero as a placeholder — this task replaces it with the featured video.

## Key Decisions Already Made

- **Dan is the face.** The July 2026 strategic audit settled this (memory `strategic-profile`: launch web-first, be the face). Faceless-channel approaches are out of scope.
- **Every video gets a companion blog post** on sixpackabs.com: embed + written version of the content + the standard Abs By AI CTAs. The embed helps the video (watch time from search traffic) and the post ranks for the query the video targets.
- **Verticals are cutdowns, not separate productions.** Longform first, then 2–4 Shorts/TikTok/Reels clips per video using the existing caption/assembly tooling.
- **Video style follows Dan's outline edits** (memory `video-outline-style`): his real specifics (supplement/Zepbound honesty, Gymboss timed sets), no generic listicle scripts.

## Detailed Plan

1. **OPEN — needs Dan's call before anything else: channel branding.** One channel or two brands? Recommendation: a single channel branded **Abs By AI** with Dan as the face — the product is the business, ad creative and organic content can share the channel, and sixpackabs.com embeds work regardless of channel name. Alternative: personal-name channel if Dan wants broader future scope. Decide, then create the channel (Dan's Google account, ~10 min together: handle, avatar, banner, about text with absbyai.com link).
2. **Channel setup:** handle, branding assets (can be generated from existing product imagery), about section, links to absbyai.com + sixpackabs.com, channel trailer = "The Upload" v1 or the strongest shoot clip.
3. **Publish cadence:** 1 longform/week to start (sustainable > ambitious), 2–4 Shorts per longform. First uploads from the shoot footage; "The Upload" ad can be an early upload/pin.
4. **Per-video packaging (Claude does this for every upload):** title targeting a real query (align with the keyword families in `handoff-20260731-sixpackabs-ai-keyword-content.md` — "AI abs transformation" space is nearly uncontested on YouTube), description with absbyai.com link + UTMs (`utm_source=youtube&utm_medium=video&utm_campaign=<video-slug>`), tags, custom thumbnail (before/after imagery works; label AI examples), end screen + pinned comment pointing at the app.
5. **Cutdowns:** for each longform, pick the 2–4 strongest 30–60s segments; 9:16 crop + burned captions via the ad-factory pipeline (Whisper word timestamps — never estimated timings, per the pilot's lesson). Post natively to Shorts/TikTok/Reels with platform-appropriate copy.
6. **Companion blog post per video** on sixpackabs.com: embed at top, 600–1,000 word written version, calculator + app CTAs. The `anthropic-skills:blog-posts` skill can batch these.
7. **Swap the sixpackabs.com hero** from the placeholder before/after to the featured video + CTA, keeping the app button. Update as new videos land (or feature the best performer, not the newest).
8. **Pinterest (30 min/week):** pin the before/after images and video stills to boards; fitness transformation imagery performs well there and links back to the blog/calculator.
9. **Measure:** YouTube Studio (CTR, retention) + PostHog UTM sessions from youtube. The winners identified here feed the paid-amplification playbook (`handoff-20260731-sixpackabs-paid-amplification.md`).

## Things to Avoid / Lessons Learned

- **Don't script generic listicles** — Dan rejected that style explicitly in the Shoot 3 outline edits; his real specifics are the differentiator.
- **Caption drift:** only generate captions from Whisper word timestamps on the FINAL mixed audio (pilot lesson, paid for twice). The pipeline exists — use it.
- **Label AI-generated imagery** in thumbnails/examples; keep the honesty standard consistent across app, blog, and channel.
- Don't let cutdown production block longform publishing — ship the longform, cut verticals after.
- The abs-by-ai repo is public; raw footage and shoot files stay out of git (follow the existing `.gitignore` patterns for media dirs).

## Relevant Files & Locations

- Footage/materials: `abs by ai gemini clips/`, `B roll/`, `abs by ai images*/` (project root; git-ignored media)
- Finished ads: `ad-factory/the-upload/final/`
- Caption/assembly tooling + lessons: `ad-factory/the-upload/assembly/`, `.claude/skills/make-ad/SKILL.md`
- Competitor playbook: memory `youtube-ad-competitor-research` (MadMuscles model + 10 swipe ads)
- Voice/style: memory `video-outline-style`
- Blog side: `handoff-20260731-sixpackabs-conversion-layer.md` (hero), `handoff-20260731-sixpackabs-ai-keyword-content.md` (keyword alignment)

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking |
| **If Claude usage is high / approaching a limit** | Still Claude, Sonnet 5 — titles, descriptions, thumbnails copy, companion posts are all brand-voice marketing work (Always-Claude). The ffmpeg cutdown runs are mechanical and cheap on any model; batch them into the same sessions rather than splitting tools. |

Task-type override: this is predominantly marketing/copy work → Always-Claude. Opus is not needed.

## Starter Prompt for the Next Task

> The shoot footage exists. Execute `handoff-20260731-sixpackabs-video-centerpiece.md` in the Abs By AI project root. Goal: launch the YouTube channel, publish the first video with full SEO packaging, cut 2–4 captioned 9:16 Shorts using the ad-factory Whisper caption pipeline, write the companion blog post on sixpackabs.com, and swap the sixpackabs.com hero to the featured video. First action: resolve the one OPEN item — channel branding (recommendation in the doc: single "Abs By AI" channel with Dan as the face) — then set up the channel with Dan.
