---
name: shorts-production-style
description: "Locked design system + title formula for Abs By AI short-form video (Shorts/Reels/TikTok), decided 2026-08-06"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a202433e-3302-40c2-ad00-0d901fb83bb8
  modified: 2026-08-06T15:43:27.166Z
---

Dan locked the short-form content system on 2026-08-06 after ~4 rounds of mockups. Apply it to all future shorts.

**Why:** Dan wants shorts that read masculine, clean, and trustworthy at first glance ("men only" audience signal), integrated with the product brand — NOT the teal/pink pill style from the long-form videos, NOT soft/rounded Apple-light looks, and explicitly NO violet/pink gradients. Hazard-tape yellow was considered and beaten by the tactical look for brand meaning + lower fatigue (hazard variant reserved as a future A/B once there's traffic).

**How to apply:**
- **One 9:16 master (1080×1920) per clip, uploaded natively to YouTube/TikTok/Reels/Facebook** — never cross-post watermarked downloads.
- **"J2 tactical" frame system — ONLY for horizontal footage forced into vertical**: near-black bg `#0D0E0B`, faint 90px grid, olive `#8C9858` full-perimeter frame with rangefinder tick marks + white corner brackets; footage sits as a card at (56,590) 968-wide; NO blur-pad fill (Dan rejected it). **Native vertical (9:16-cropped) footage gets NO frame** — just large overlaid title text with drop shadow (Dan 2026-08-06: killed the frame on the vertical anatomy short, wanted bigger text). No static intro title cards — open directly on Dan talking, cut at a sentence start.
- Long eyebrow lines must wrap to two lines rather than shrink below ~50px Copperplate — small letter-spaced text is unreadable at feed size.
- **Type**: headlines in Impact all-caps white; eyebrow/labels in Copperplate letter-spaced olive; chips are square-cornered olive-bordered rects ("TARGET: LOWER ABS" mission framing).
- **Titles must sell the click to someone who never saw the source video** (benefit-first, e.g. "Killer Home Six Pack Abs Exercise: The Toe Touch"), split as eyebrow + big headline. Dan's five examples are in the 2026-08-06 session.
- **URL**: always `AbsByAI.com` camel case (never all-caps, parses/remembers better), small + muted on every short from video #1 (rip protection); wordmark-as-URL instead of a logo while the brand is unknown.
- **Any graphic from the horizontal source that survives a vertical crop must be covered** with a matching tactical chip — measure the ghost's exact pixel box (pink-dot color scan) and cover fully; transparent corners leak slivers, use solid chips.
- Captions: burned word-timed captions from Whisper (Arial 86 bold white, MarginV 690), reuse the ad pipeline spec.
- Pipeline + reusable scripts (overlay gen, caption gen, render): scratchpad `shorts/` dir of session a202433e (gen_j2.py, render_j2.sh); outputs live in git-ignored `ad-factory/shorts-1min-ab-workout/`.
- Clip selection approach approved: soundbite-driven cuts on word timestamps, one idea per short, the "weird cue" / mistake-callout moments as hooks. Related: [[proof-banner-image-gen-process]], [[video-outline-style]].
