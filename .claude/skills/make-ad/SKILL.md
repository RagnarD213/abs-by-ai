---
name: make-ad
description: >
  End-to-end production of an AI-generated video ad for Abs By AI, MadMuscles-style
  (9:16 vertical, 60–110s, AI characters + voiceover, stitched from 5–10s clips).
  Use this skill whenever Dan asks to make an ad, video ad, ad creative, ad variant,
  "MadMuscles-style" content, or to continue ad production at ANY stage (script,
  character sheet, voiceover, clips, assembly, variants) — even if he doesn't say
  "/make-ad". Also use when reviewing or revising a previously produced ad.
---

# Make-Ad: AI Video Ad Production for Abs By AI

**STATUS: v1 — written before the first pilot.** Steps 1–7 are settled process; steps
8–9 contain assumptions marked ⚠️ that the pilot must verify. After the pilot (and
every ad after), update the Lessons section at the bottom — this skill is supposed to
get smarter with every ad.

## The one-paragraph mental model

Nobody generates a 90-second ad in one shot. An ad is ~10 short clips (5–10s each)
stitched in an editor with ONE continuous voiceover carrying the story across cuts —
the unbroken voice is what makes separate clips feel like one film. Characters stay
consistent because every clip is generated from the same written "character bible"
plus the same 3–4 reference photos. Dan approves at fixed gates; everything between
gates is Claude's to execute autonomously.

## Ground rules

- **Dan is non-technical.** Explain each step's result in plain language.
- **Every generation batch costs real money.** Before any batch (images, VO, clips),
  state the estimated cost and get Dan's OK if it exceeds ~$20. Check the Replicate
  balance is comfortably above $20 first — below that, Replicate throttles to
  6 requests/min (bit us during the FLUX work).
- **All models run on Replicate** via `REPLICATE_API_TOKEN` (in Railway env; read it
  the way the bake-off harnesses did). One account, one bill.
- **Work files live in `ad-factory/<ad-slug>/`** in the project root, which must be
  git-ignored (the repo is public; also keeps video files out of git). Layout:
  `script.md`, `character/`, `vo/`, `clips/`, `assembly/`, `final/`.
- **Approval gates are hard stops.** Never proceed past a gate on an old approval —
  a script change after clips exist means regenerating clips.

## Model routing (verified on Replicate 2026-07-29)

| Job | Model (slug) | Notes | Rough cost |
|---|---|---|---|
| Character stills | `google/nano-banana-pro` or `bytedance/seedream-4.5` | Same models as the app; known behavior | ~$0.04–0.13/image |
| Dialogue clips (character speaks on camera) | `google/veo-3.1` (`-fast` for drafts) | Native lip-synced speech, takes reference images, 9:16 | ~$1–4 per 8s clip |
| B-roll clips (no dialogue: montage, walking, scenery) | `kwaivgi/kling-v3-video` or `bytedance/seedance-2.0` | Kling: multi-shot subject consistency. Seedance 2.0: up to 9 reference images | well under Veo |
| Voiceover | MiniMax speech model on Replicate (⚠️ confirm exact slug against live catalog before first use) | One continuous MP3 for the whole ad. ElevenLabs only if quality disappoints (needs new account + API key from Dan) | cents |

⚠️ Pull each model's live OpenAPI schema from Replicate before first use instead of
guessing input fields — this caught real issues in the bake-off (Seedream's 4000-char
limit, GPT Image's missing aspect ratio).

## The 11-step workflow

Steps marked **[GATE]** stop and wait for Dan.

1. **Brainstorm.** Source concepts from memory `ai-ad-creation-research` (10 pitched
   concepts + MadMuscles theme data). Proven themes: military/respect, tai chi
   master, calisthenics elder, podcast story. Our unique angle: the product's own
   before/after output IS the ad's proof — no competitor can copy that.
2. **Script.** Deliverable is `script.md` containing: (a) the hook (first 5s — this
   is what variants will swap); (b) ~12 numbered narration lines; (c) a shot list of
   8–12 shots, each with: duration, dialogue-or-B-roll, which model, and the full
   generation prompt including the character bible verbatim; (d) end card copy
   ("absbyai.com — see your future self free").
3. **[GATE] Dan edits the script.** Lock narration TIMING here too — narration length
   dictates every shot duration.
4. **Character sheet.** Write the character bible: one paragraph, exact face/age/
   build/outfit/setting. THE OUTFIT NEVER CHANGES between shots — costume drift is
   where AI characters fall apart. Generate 3–4 stills (front, profile, close-up)
   with the image models. For "The Upload"-style ads where the character's fit
   version appears: generate the after-body through the LIVE product pipeline
   (per memory `proof-banner-image-gen-process` — Dan's results beat ad-hoc
   prompting).
5. **[GATE] Dan approves the character sheet.**
6. **Voiceover.** One continuous MP3 of all narration lines. Note the duration — it
   is the ad's skeleton.
7. **[GATE] Dan approves the voiceover** (send the MP3 with SendUserFile).
8. **Clips.** Generate per the shot list: Veo for dialogue shots (pass the character
   stills as reference images + the bible in the prompt), Kling/Seedance for B-roll.
   QC each clip by extracting 3–4 frames (ffmpeg) and inspecting them: anatomy,
   outfit match, setting match, no text artifacts. Auto-retry duds — ⚠️ expect
   roughly 1 in 3 to need a retry (pilot to verify). Only surviving clips go to Dan.
9. **Assembly (ffmpeg, NOT CapCut).** Build `assembly/build.sh` per ad: concat clips
   in shot order, trim cuts to narration beats, lay the VO, duck a royalty-free
   music bed under it, burn bold captions (ASS subtitles, MadMuscles style: large,
   centered-low, word-emphasis), append end card. The script IS the timeline —
   any tweak is a one-line change + re-render, which is what makes variants cheap.
   ⚠️ Caption style spec is unwritten; pilot defines it. If a cut feels flat,
   the clips + VO folder can go to a human editor (Romeysa) for polish instead.
10. **[GATE] Dan approves the assembled ad** (send the MP4). He judges motion, lip
    sync, and pacing — frame QC can't catch those.
11. **Variants.** Swap ONLY the hook (new 5s opening clip and/or first narration
    line), re-render via the assembly script. Name `<slug>_v1..vN` like MadMuscles.
    **[GATE] Dan approves variants.** Deliver finals from `final/`.

## MadMuscles reference patterns (why these choices)

Their $488M/yr machine (VidTao, July 2026): all ads 9:16, 60–110s, AI character +
AI VO, themes rotated by performance (tai chi → military), 5–10 hook variants per
script, losers killed at ~$5k spend, winners scaled to $200k+/30d. Reference winners
to study: youtu.be/lfa71t4RAyw ($224.8k/30d military street-interview),
youtu.be/HZLYJPGi8gI, youtu.be/3-dC0_qRXd0 (male tai chi). Full data in memory
`ai-ad-creation-research`.

## Lessons learned (append after every ad)

- (none yet — pilot pending)
