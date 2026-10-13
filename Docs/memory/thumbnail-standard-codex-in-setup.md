---
name: thumbnail-standard-codex-in-setup
description: "Dan 2026-10-13: thumbnails = 5 unique designs (1 pool, 1 studio, 1 AI-enhanced or AI-generated image of Dan, 2 AI images of Codex's choice), always made by Codex, inside the Claude setup task, GPT-6.1 Sol high"
metadata:
  type: feedback
---

Standard for every upload and setup task unless Dan says otherwise for a video: five thumbnail choices, each a unique design. One pool-shoot photo, one studio-shoot photo, one AI-enhanced or AI-generated image of Dan, and two more AI-generated images of Codex's choice, which may show Dan or not (Codex's judgment). Codex always makes them: the Claude setup task calls Codex in the command line on his subscription (`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`). Show five, stop for his pick, then upload. No Gemini or other outside image model.

**Why:** Dan, 2026-10-13, finalizing RO-19 "My First Spray Tan": "Let's make this a standard way of making thumbnails going forward. We always have one pool, one studio, one AI-enhanced or AI-generated image of me, and two other AI-generated images, which can be me or not. We'll leave the other two up to Codex's judgment, and then we always have five unique designs for thumbnails. Save that to our skill... Make sure that Codex is always the one making these thumbnails." For RO-19 the AI image of him was "me getting a spray tan". It replaces the 2026-10-02 mix (pool, studio, three AI designs of Codex's choice), which replaced the 09-30 mix.

**How to apply:** one Claude handoff per finished video covering thumbnails and setup; it lists the five slots and its starter prompt says "Use the Codex subscription to generate the images." The pool and studio options stay his real cutout over a Codex background; the AI image of him is the one place he may be AI-enhanced or generated (check the face reads as him). My reading, not his words: the AI image of him shows him in the video's subject where one fits, and Shorts covers follow the same five. Rule text: VIDEO-RULES.md first section and AGENTS.md. Related: [[thumbnail-unique-designs]], [[organic-setup-codex-thumbnail-split]], [[cover-photo-selection]], [[thumbnail-design-system]], [[codex-image-gen-from-claude]].
