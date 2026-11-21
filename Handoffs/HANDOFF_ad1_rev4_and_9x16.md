# HANDOFF — Ad 1 rev-4 (2 items) + 9:16 build

**From:** Claude Code (the "First ad batch edit" session, 2026-08-21)
**Recommended model/effort:** Sonnet 5 / medium (execution is recipe-following).
High-usage alternative: Fable 5 / medium only if Dan wants extra judgment on the 9:16 re-layout.
**Read first:** `.claude/skills/ad-edit/SKILL.md` (esp. lessons 7–16) and
`/Volumes/Seagate 4TB/abs by ai 8:14 shoot …/EDITED ADS 8-20-26/ad1-how-ai-got-me-abs/notes.md`.
Invoke `/ad-edit`.

## State

Ad 1 "How AI Got Me Abs" is at **rev-3**, delivered, awaiting Dan's next verdict. Working dir:
`/Volumes/Seagate 4TB/_edit_work/ad1-8-14/` (everything below is relative to it). The finished
chain is: `CUT_v2_graded.mp4` (base cut, don't touch) → `python3 layout2.py layout` (punch pass
is cached as `punched2.mp4`; layout writes `ad1_rev1_nocap.mp4`) → burn captions:
`ffmpeg -i ad1_rev1_nocap.mp4 -vf "subtitles=cap_v2.ass:fontsdir=fonts" -c:a copy ad1_revN_16x9.mp4`.
Review copies: scale to 720p CRF 25 (<30MB) and SendUserFile. Full-res + recipe also copied to the
EDITED ADS delivery folder after each round. Recipe scripts mirrored in git at
`.claude/skills/ad-edit/reference/ad1/`.

## Rev-4 item 1 — replace the tire-flip stock clip (render 46.0–50.0)

Dan: the tire flip isn't relevant. Replace with an AI clip: **overweight dad in his 40s, wearing a
suit, with his family — busy and stressed (work + kids), no motivation to work out.** Suggested
scene (my default, adjust freely): morning kitchen chaos — suit jacket, briefcase, phone wedged at
his ear, two kids demanding attention, visibly overweight and frazzled; start frame mid-chaos,
end frame a tired slump/sigh.

**PROTOCOL (Dan's, mandatory): generate START + END frames first → send to Dan → wait for
approval → only then generate the video.**

- Stills: `node .claude/skills/_shared/gemini-image.js generate --prompt-file p.txt --out f.jpg
  --tier draft --env ~/.absbyai-secrets.env` (~$0.134 each). 16:9 wording in prompt.
  For the end frame, pass `--image start.jpg` and "same exact scene and camera" so the pair stays
  consistent (lesson from rev-2).
- Video: **Replicate is DEAD (402, auto-reload not firing — Dan may fix; re-probe before assuming).**
  Working path = Veo 3.1 Fast on the Gemini API. Exact recipe that works (see
  `aiframes/genclips_veo.js` + the inline python in this session's scripts):
  POST `https://generativelanguage.googleapis.com/v1beta/models/veo-3.1-fast-generate-preview:predictLongRunning?key=$GEMINI_API_KEY`
  body `{"instances":[{"prompt":..., "image":{bytesBase64Encoded,mimeType}}],
  "parameters":{"aspectRatio":"16:9","durationSeconds":4 or 6,"resolution":"720p"}}` → poll the
  operation → download `response.generateVideoResponse.generatedSamples[0].video.uri` + `&key=`.
  TRAPS: `lastFrame` is NOT supported (400 "use case not supported"); flirt/suggestive wording and
  even odd audio hints trip the RAI filter — keep prompts neutral, append "No speech."; failed
  safety attempts are not charged. GEMINI_API_KEY is in `~/.absbyai-secrets.env`.
- Swap into layout: in `layout2.py` VID list, replace the line
  `(STK1[0], STK1[1], STK % "3802827", 2.0, 0, "", False),` with the new clip, e.g.
  `(STK1[0], STK1[1], "aiframes/clip_dad.mp4", 0.3, 0, "", True),` — the `True` gives it the tag
  (see item 2). Window is 4.0s; generate 4–6s and pick the slice-in.

## Rev-4 item 2 — AI-GENERATED tag on full-frame AI clips: upper-left, 50% larger

Dan: at ~2:00 the tag blocks the video. For **full-frame AI video inserts** (clip_a, clip_b,
clip_c, + the new dad clip): move the tag to the **upper-left corner** and make it **50% larger**.
Panel-style inserts (phone clip at 9.3, crude photoshop at 64.0) KEEP the centered tag — nothing
is blocked there (my default; Dan was asked and can override).

Implementation: build `assets_v1/tag_big.png` = the J2 tag rendered at 1.5x (edit `tag_png` call:
Copperplate 51px, box scaled ~1.5x — or simply `Image.resize` the existing tag by 1.5 with
LANCZOS). In `layout2.py` pass2's VID loop, for entries where `wid == 0 and tag` use
`overlay=40:40` with `tag_big.png` instead of `(main_w-overlay_w)/2:40` with `tag.png`.

## Then

1. `python3 layout2.py layout` (~6 min) → burn captions → QC frames (extract stills at 46–49,
   119–129 for tags, spot-check nothing else moved) → 720p review copy → SendUserFile → update
   `notes.md` (append REV-4 section), coordination file, commit skill-reference copies + push.
2. **After Dan approves the 16:9: build the 9:16** per `/ad-edit` Step 8 (NOT a center crop):
   talking head crop tracked on Dan (face anchor ≈ x1099 in the 1920 frame, punch math in
   layout2.py); app/phone clips go full-frame native vertical; stock/AI 16:9 clips center-crop to
   9:16; graphics re-laid-out (captions per /make-ad 1080×1920 spec, CTA bar lower, panels become
   full-width cards); same EDL + audio. Keep both builds in one script so revisions re-render both.
   Remember the 1080p source caveat: the vertical crop is a 608→1080 upscale (flagged to Dan already).
3. Update the two LEARNING sections in the skill with anything Dan's replies teach.

## Money / providers

- Session spend so far on ad 1: ≈ $6 total (well under the $25 cap). State estimates before batches.
- Replicate: 402 since ~08:30 on 2026-08-21; auto-reload configured per Dan but not firing —
  billing page needs his GitHub sign-in (a Chrome tab was left open at it). Re-probe with a cheap
  prediction before relying on it. Veo covers everything meanwhile.

## Starter prompt (paste into a new session)

> /ad-edit Continue ad 1. Read Handoffs/HANDOFF_ad1_rev4_and_9x16.md and execute rev-4:
> (1) the busy-dad AI clip replacing the tire flip at 0:46–0:50 — frames first for my approval,
> (2) AI-GENERATED tags upper-left and 50% larger on the full-frame AI clips. Then deliver the
> 720p review. After I approve the 16:9, build the 9:16.
