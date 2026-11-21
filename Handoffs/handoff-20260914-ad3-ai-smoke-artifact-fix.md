# Handoff — Ad 3: remove the AI breath-smoke artifact (vertical + 16:9 original), then finish delivery

**Written 2026-09-14 by the Ad 3 vertical session. Not yet executed.**

## Goal

At **1:16** in Ad 3 "Stop Paying Human Trainers", the AI story clip shows a man exhaling at a bathroom mirror, and
**the mirror fogs over with breath smoke**. Dan, 2026-09-14: *"He exhales, and there's smoke coming out when he
exhales. This was also in the original video, so I want you to see if you can fix this both in the vertical and in the
original video. That way, when we make the square, this doesn't carry through to the square as well."*

Deliver:
1. **A clean replacement for that one shot**, same look and same length as the other six shots of the story.
2. **The 9:16 vertical re-rendered** with it. Dan approved everything else about this build on 2026-09-14: *"The color
   correction looks good, and the audio sounds good. I think this is a great reproduction of what Muhammad did."* Change
   nothing else.
3. **A corrected 16:9** — Muhammad's v6 HD with only those frames replaced, his audio bit for bit.
4. **The fixed story clip wherever the square will read it**, so the Ad 3 square (`Handoffs/handoff-20260911-square-ad3-muhammad.md`,
   job J6/J7 in `Handoffs/handoff-20260913-ad-variants-master-queue.md`) cannot inherit the artifact.
5. **Finish Ad 3's delivery**: the ≤0:59 cutdown on the approved colour, every gate, deliver both files, commit the skill work.

## What is known (measured 2026-09-13/14, not assumed)

**Where the artifact is**
- Timeline (the vertical is frame-locked to Muhammad's 16:9, 29.97 fps): the fog appears at about **76.6 s** and
  thickens until the shot cuts at about **78.07 s** (frames ≈ 2296 → 2340). The bathroom shot runs ≈ 73.5 → 78.07 s
  (frames ≈ 2202 → 2340).
- Source: `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/04 AI-Generated Clips/ai-trainer-vs-robot-story-35s.mp4`
  (identical copy at `Media/ad-assets/batch1-ads/clips/`), 1080×1920, 24 fps, 847 frames, no audio. It is **7 shots of
  121 frames each** (5.042 s). The bathroom mirror is **shot 3**, source **10.083 → 15.125 s**; the fog starts about
  **3.4 s into that shot**.
- The raw shot: **`Media/ad-assets/batch1-ads/shots/s3.mp4`** (716×1284, 24 fps, 121 frames). Its start frame:
  **`Media/ad-assets/batch1-ads/frames/s3_no_results_mirror.png`**. How the story was made
  (`Media/ad-assets/batch1-ads/PLACEMENT.md`): `google/nano-banana-pro` start frames, then **`kwaivgi/kling-v3-video`
  image-to-video at 5 s per shot**, stitched with ffmpeg. No prompt file was found on disk.
- The 8 s cutdown `ai-trainer-vs-robot-cutdown-8s.mp4` (Ads 13, 14) uses only the story's first and last beats, so it
  does NOT contain shot 3. Confirm by frame before assuming.

**How the vertical uses it** — build dir `/Volumes/Extreme/_edit_work/ad3-vert/`
- `beats.py`: `('bleedv', 1944, 2845, dict(media=<story clip>, tmap=AI8_MAP-style STORY_MAP, scrim=True))`,
  `STORY_MAP = [(1944, 0.58881, 1.0), (2844, 33.70925, 1.0)]` (source seconds = 0.58881 + (n − 1944) × 0.036800).
  Muhammad's 137-frame shots are the source's 121-frame shots retimed by 1.1029.
- The render: `master13.sh` (three chunks + concat + `zmux.py`). The talking-head colour lives in `grade_post.json`,
  `grade_seg.json`, `grade_final.json`, `his.cube` and `vignette.json` and is applied only to base frames (talk and
  window beats) — **the story clip is not graded by those stages**, so swapping it changes nothing Dan approved.
- Current approved master: `ad3_vertical_9x16.mp4` (render 11, sha256 `405eff4a…`). Already preserved as
  `_approved_r11/ad3_vertical_9x16_r11_APPROVED.mp4`, which the corpus entry `ad3-vertical-r11-approved` points at; the
  colour-rejected render 9 is `_rejected_r9/ad3_vertical_9x16_r9_REJECTED_color.mp4` (entry `ad3-vertical-r9-color`).

**How Muhammad's 16:9 shows it** — `ad3-vert/ref/ad3_v6hd.mp4` (= his "Daniel HQ Ad 3 v6 HD.mp4", Drive
`1qsBpkrm8T7BDaYF67NL1k_x67sTsxsb3`, no colour tags): the portrait clip sits inside his olive card on the dark grid,
with his italic "[AI-generated]" label over it. ⚠ **That file is not his final either** — at 2:14.1–2:23.1 it dropped
"back in my 20s, as a 38 year old dad running a successful ad agency." from a bullet, and Dan was to ask him to
re-export. ⚠ It is live as the unlisted ad video `QWW1oumpNg4` in Demand Gen ad groups 199782847163 / 199360345839.
Replacing a YouTube video changes its id and the ads pointing at it — **do not upload or swap anything on YouTube or in
Google Ads without asking Dan.**

## Plan

### 1. Make a clean shot 3
1. Read every frame of `shots/s3.mp4` at full resolution first, with the AI-artifact checklist now in
   `.claude/skills/revisions/SKILL.md` step 3b. Record every giveaway, not just the fog, so the replacement is judged
   against the full list.
2. **Preferred: regenerate from the same start frame with the same model**, so it matches the other six shots:
   `kwaivgi/kling-v3-video` image-to-video, `frames/s3_no_results_mirror.png`, 5 s, 24 fps if offered. Describe the same
   action (a man in a grey T-shirt lifts his shirt and looks at his belly in the bathroom mirror, disappointed) with the
   mouth closed and breathing through the nose, the mirror staying clear; put "breath, steam, smoke, mist, fog,
   condensation" in the **negative prompt** field rather than as "no smoke" in the positive prompt, which tends to add
   it. Run 3–4 seeds. **State the cost estimate before running** (standing authorization: $25 per session, a single
   batch over $15 needs Dan). Replicate API key: `~/.absbyai-secrets.env` or `railway variables --service abs-by-ai --kv`.
3. Pick the take whose motion best matches the original across the first ~3 s (Muhammad's picture timing and our crop
   were built on it), then read EVERY frame of it with the checklist, including all of its last 2 s. A take with any
   giveaway is rejected, not patched.
4. Fallbacks, only if no take is clean: (a) Veo image-to-video from the same frame; (b) keep s3's clean first ~3.3 s and
   cut to shot 4 early, extending shot 4's head to hold the story's length (changes Muhammad's timing — say so in the
   notes); (c) frame-by-frame removal of the fog — last resort, it tends to smear.
5. Rebuild the story as **`ai-trainer-vs-robot-story-35s_v2.mp4`**: the same 7 shots with only shot 3 replaced, scaled
   and encoded exactly like v1 (1080×1920, 24 fps, 847 frames, no audio). Assert every other shot is pixel-identical to
   v1's frames. Keep v1 untouched. Put v2 next to v1 in the asset library folder and in `Media/ad-assets/batch1-ads/clips/`,
   and add a line to `PLACEMENT.md`. Upload v2 to Drive beside v1 (`/findassets` §6 has the working upload path) so
   Muhammad can use it.

### 2. Vertical
1. Point the `bleedv` beat's `media` in `beats.py` at v2. Nothing else changes.
2. Re-render. Frames 1944–2845 all sit in chunk 0 (0–2845), but re-run the whole `master13.sh` chain unless you prove
   chunks 1 and 2 are untouched; the chain is ~22 min. Check `ps` for the two-build cap first.
3. Verify at full resolution that frames ≈ 2202–2340 show no fog and that the shot boundaries land on the same frames
   as render 11 (diff the two files: every frame outside 2202–2340 should be identical or within encoder noise).
4. Gates on the new file: `gates9.sh` (watch, sheets, caption sync, hair, landing, audio gate `--verbatim`), `qc.py`,
   then review ALL watch sheets and `zwatch_mark.py`, then `plan_build.py --transcribe` + the negative-events scan +
   `_shared/deliver/gate.py --format ad9x16 --plan plan.json`. Known gate limits on this build (record, never tune):
   `compliance:labels` cannot place a per-card chip, the four `framing:*` rows read NOT MEASURED on the window layout
   (our `zhairgate2.py` + `centering.py` do measure it), `captions:graphic_clearance` needs MOVs a Python compositor
   never makes.

### 3. The 16:9 original
1. Build Muhammad's version of the new shot: v2 shot 3 at his 137-frame timing, in his card geometry, carrying his grade
   and his "[AI-generated]" label. Measure all three from his OWN frames on the clean part of the shot (≈ 73.5–76.5 s),
   where his pixels and the original s3 overlap. **Decode his file as BT.709** (`scale=in_color_matrix=bt709:in_range=tv`)
   — it has no colour tags, and the default BT.601 decode is exactly the mistake Dan rejected on 2026-09-13 (memory
   `untagged-video-bt601-trap`). Lift the label, card and grid from a frame where they are static.
2. Replace ONLY his frames ≈ 2202–2340 (confirm his exact shot boundaries first). Re-encode the picture visually
   losslessly (x264 crf ≤ 12, 1920×1080, 29.97, tagged bt709), stream-copy his audio, and assert its md5 equals
   `db408fd0bc0ba2a44245df947cb7e1f3`. Prove every frame outside the patched range matches his within encoder noise.
3. Save it in `Muhammad Ad Videos/stop paying human trainers - ad 3/` as
   `stop paying human trainers | muhammad (smoke shot replaced) | 16x9 | ad 3.mp4`, and write in the folder's notes
   what was replaced and why. It still carries his 2:14 dropped bullet text.
4. Add an item for Muhammad's next Ad 3 round (via `/revisions`, in Dan's voice) with the v2 link, so his re-export
   carries the clean shot. If Dan has already asked him to re-export, the item goes into that request.

### 4. Square
The Ad 3 square is a re-layout of the vertical build. Before it runs, check `beats.py` points at v2 and that the four
grade files and `label_place.json` are in the build dir. Add a line under J6/J7 in the master queue doc.

### 5. Finish Ad 3
1. **Cutdown** on the approved colour: `cut6.sh` (re-selected plan: 57.92 s, 63 % inserts, one CTA). It renders from the
   master dir, so it reads the grade files and v2 automatically. Then the cutdown's watch pass, `qc.py`,
   `plan_build.py --cut --transcribe` and its delivery gate. Its true peak reads −0.90 dBTP because AAC overshoots his
   −1.0 wav by 0.1 dB on every encoder and bitrate tried; Dan accepted exactly that number on Ad 4, but confirm with him
   for Ad 3 — never trim his mix without asking.
2. **Independent audit** of both files (the build's audits caught real defects after every 20/20).
3. **Deliver** with `deliver3.py` into `Muhammad Ad Videos/stop paying human trainers - ad 3/` using the naming in memory
   `ad2-vertical-approved`. Update `notes.md` (colour fix section, smoke shot, label placement) and copy the recipe.
4. **Commit, in this order.** (a) Run `python3 .claude/skills/_shared/qc_corpus/run.py` — it must pass before any of the
   gate-adjacent changes land: `_shared/qc_corpus/corpus.json` (entries `ad3-vertical-r9-color`, `ad3-vertical-r11-approved`),
   `shortad-from-longform/reference/plan_build.py` (cue ends now match the rendered caption), `reference/a6/zlut.py`
   (BT.709 decode). (b) Paste `ad3-vert/a12_draft/LESSONS.md` into `shortad-from-longform/SKILL.md` as **[A12]** (re-read
   the file first — [A9] is Ad 5, [A10] the first square, [A11] the Ad 1 square) and copy the tools to
   `reference/a12_ad3/`, adding the colour pipeline (`zlut.py`, `zgrade2.py`, `zgrade3.py`, `zgrade4.py`, `lift3.py`,
   `zlabelplace.py`, the `render3.py` hooks) and a section on the BT.601 trap and the section-by-section grade.
   ⚠ The repo is public: no personal photos in the commit. Push, then update `AI_COORDINATION.md` (re-read from disk).
5. Dashboard: check off the row for the Ad 3 vertical only once Dan has approved the delivered files.

## Open for Dan
- Whether his two 200 lb BEFORE pictures (2:26–2:33) also get "Real picture of me — not AI-generated" (the vertical
  labels only the four after pictures; the four chips now sit above his head or to the side).
- The cutdown's −0.90 dBTP (above).
- Whether to replace the live unlisted Ad 3 ad video `QWW1oumpNg4` with the corrected 16:9 (new id, ad changes).

## Warnings
- ⚠ **The Ad 4 and Ad 5 vertical builds have the BT.601 colour fault too** (their `zlut.py` decode without
  `in_color_matrix`, their references are untagged). Not part of this job; it is on the coordination board.
- ⚠ Never run a pipeline script inside another session's build dir; cap video builds at two across sessions.
- ⚠ A background session-cleanup job once killed this build's renders; keep long renders in a session that is active.

## Starter prompt

> Execute `Handoffs/handoff-20260914-ad3-ai-smoke-artifact-fix.md` end to end. Read it fully first, then read
> `AI_COORDINATION.md` from disk and the Ad 3 entry. Start with step 1: read every frame of `shots/s3.mp4` with the
> AI-artifact checklist in `.claude/skills/revisions/SKILL.md` step 3b, state the Kling cost estimate, and regenerate
> shot 3. Do not change anything Dan approved in the vertical beyond the story clip. Report with measured proof for each
> deliverable.

**Recommended model / effort:** Claude Opus 5 or Fable 5.1, high effort — it combines AI generation, frame-accurate
video surgery and the full delivery gate. Roughly one long session.
