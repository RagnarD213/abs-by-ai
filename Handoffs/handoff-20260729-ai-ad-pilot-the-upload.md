# Handoff: "The Upload" — pilot AI-generated video ad

**Date:** 2026-07-29
**Project:** Abs By AI
**Business goal this serves:** Marketing (customer acquisition — building the MadMuscles-style AI ad factory)

## Objective

Produce the first complete AI-generated video ad ("The Upload" concept) end-to-end using the new `/make-ad` skill: script → character sheet → voiceover → AI-generated clips → assembled 9:16 vertical ad with captions → hook variants. The pilot has a second job: **debug the pipeline and write what was learned back into the skill** (`.claude/skills/make-ad/SKILL.md`, Lessons section), so ads 2+ run as a factory.

## Current State

- **Nothing has been generated yet.** This handoff is the starting gun.
- `.claude/skills/make-ad/SKILL.md` exists (v1, written 2026-07-29 before any pilot). It contains the full 11-step workflow with Dan's approval gates, model routing with verified Replicate slugs, cost table, and ⚠️ markers on every assumption the pilot must verify.
- Research is done and saved to memory (`ai-ad-creation-research`, `youtube-ad-competitor-research`): MadMuscles' theme system, their current winners with YouTube IDs (study `youtu.be/lfa71t4RAyw` — their $224.8k/30d ad — before writing the script), and the toolchain rationale.
- All needed models confirmed live on Replicate (2026-07-29): `google/veo-3.1` (+`-fast`, `-lite`), `kwaivgi/kling-v3-video`, `bytedance/seedance-2.0` (accepts up to 9 reference images), `google/nano-banana-pro`, `bytedance/seedream-4.5`. One account: `REPLICATE_API_TOKEN` (Railway env — read it the way the bake-off harnesses did).

## The Concept (approved by Dan)

**"The Upload"** — pure product demo as story. A man unhappy with his reflection uploads a beach photo to Abs By AI; the phone renders his abs version (REAL product output, not a mock); he can't unsee it; gym montage; months later the mirror matches the photo. VO spine: "You can't hit a target you've never seen." End card: "absbyai.com — see your future self free." 9:16, ~60–90s, one character.

Why this one first: it's the ad only we can run (the product's own before/after output is the proof), and it needs just one character — the simplest possible consistency test for the pilot.

## Key Decisions Already Made (do not relitigate)

- **All generation via Replicate API**, not Google's Flow/Gemini web apps and not a Gemini subscription — the point is Claude executes; web UIs would make Dan the operator.
- **Veo 3.1 for dialogue shots, Kling 3/Seedance 2 for B-roll** — Veo is the only one with lip-synced on-camera speech; B-roll on cheaper models cuts cost.
- **Assembly with ffmpeg, not CapCut** — assembly-as-code makes variants a one-line change + re-render. If a cut feels flat, hand the clips + VO to Romeysa for human polish; don't fight ffmpeg for artistry.
- **Voiceover: try MiniMax speech on Replicate first**; only add ElevenLabs (new account, API key from Dan) if the voice quality disappoints.
- **Character consistency = character bible (verbatim in every prompt, outfit never changes) + 3–4 reference stills fed to every clip.**
- **The "after" body imagery goes through the LIVE product pipeline** (memory: `proof-banner-image-gen-process`) — Dan's real-pipeline results beat ad-hoc API prompting, and it makes the ad honest (real product output).
- **Approval gates are Dan's:** script, character sheet, voiceover, assembled ad, variants. Everything between gates is autonomous.
- **Workflow order is locked**: VO approved BEFORE clips are generated (narration length dictates shot durations; script changes after clips = regenerating clips).

## Detailed Plan

Follow `/make-ad` steps 2–11 (step 1, brainstorm, is done — concept chosen):

1. Create `ad-factory/the-upload/` in the project root and **git-ignore `ad-factory/`** (public repo; keep video files out of git).
2. Write `script.md` per the skill's format: 5s hook, ~12 narration lines, 8–12 shot list with per-shot model + full prompt + character bible, end card. Watch the MadMuscles reference ads first for pacing/caption style. **GATE: Dan edits.**
3. Character bible + 3–4 stills (front/profile/close-up) via nano-banana-pro or seedream. Generate the character's fit "after" version through the live absbyai.com pipeline. **GATE: Dan approves.**
4. Voiceover: one continuous MP3. ⚠️ Confirm the MiniMax speech model slug against Replicate's live catalog before calling. **GATE: Dan approves (send the MP3).**
5. Clips: check Replicate balance > $20 first (throttle floor). State estimated batch cost before running. Pull each video model's live OpenAPI schema before first call. QC every clip by extracting frames with ffmpeg and inspecting; retry duds. ⚠️ Record the actual retry rate.
6. Assembly: write `assembly/build.sh` (concat, VO, music bed, burned ASS captions, end card). ⚠️ Define the caption style spec here — study the MadMuscles ads' captions. **GATE: Dan approves the MP4 (send it).**
7. Variants: 3–5 hook swaps, re-render, `the-upload_v1..vN`. **GATE: Dan approves.**
8. **Write the Lessons section of the skill** from everything learned (retry rates, prompt phrasings that worked, actual costs, caption spec, schema gotchas). This is a deliverable, not optional.
9. Check off the dashboard task (`money::Execute handoff: Produce "The Upload" pilot AI video ad` — fetch exact text from `/api/todos` first, per CLAUDE.md mechanism).

**OPEN decisions for the pilot to resolve with Dan:**
- Music: source a royalty-free track (many MadMuscles ads run VO-dominant with minimal music — acceptable to skip music in v1).
- Budget cap: assume ~$50 for the whole pilot including retries; confirm with Dan before the clip batch (the expensive step).

## Things to Avoid / Lessons Learned (inherited from project history)

- **Replicate balance under ~$20 = 6 requests/min throttle.** Top up or enable auto-reload before batch work.
- **Never guess Replicate model input schemas** — pull the live OpenAPI schema (caught Seedream's 4000-char limit and GPT Image's aspect-ratio gap in the bake-off).
- **Costume/wardrobe changes are where AI characters fall apart** — the bible's outfit never varies between shots.
- **iPhone photos carry EXIF orientation tags** that some models honor and others ignore (bake-off gotcha) — normalize with PIL `ImageOps.exif_transpose` if using any real photos as references.
- Generation requests with no `deviceId` skip the app's credit system — but this pilot calls Replicate directly except for the product-pipeline "after" image, which costs one real generation (~8¢); fine.

## Relevant Files & Locations

- Skill: `.claude/skills/make-ad/SKILL.md` (v1 — the workflow authority; update its Lessons section)
- Work dir to create: `ad-factory/the-upload/` (git-ignored)
- Memory: `ai-ad-creation-research.md`, `youtube-ad-competitor-research.md`, `proof-banner-image-gen-process.md`
- Reference ads: youtu.be/lfa71t4RAyw ($224.8k military interview), youtu.be/HZLYJPGi8gI, youtu.be/3-dC0_qRXd0 (tai chi)
- Env: `REPLICATE_API_TOKEN` (Railway); product pipeline at absbyai.com

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Fable 5, high effort** — the pilot is creative brand-voice work + multimodal frame QC + novel API orchestration all at once, and debugging the pipeline well the first time is what makes every later ad cheap. |
| **If Claude usage is high / approaching a limit** | **Claude Opus 5, extended thinking.** Do NOT hand this to Codex — it's marketing/brand-voice creative work with heavy image inspection, both always-Claude categories. |

After the pilot has debugged the skill, subsequent ads are more routine: Sonnet 5 should handle ads 2+ with the skill loaded; escalate only if quality slips.

## Starter Prompt for the Next Task

> Run /make-ad. We're executing the pilot: read `handoff-20260729-ai-ad-pilot-the-upload.md` in the project root and follow it. The concept is "The Upload" (already chosen — don't re-brainstorm). Start with step 1 of the handoff's Detailed Plan: create the git-ignored `ad-factory/the-upload/` folder, then write the script for my review. Remember the approval gates — stop and show me the script before generating anything that costs money.
