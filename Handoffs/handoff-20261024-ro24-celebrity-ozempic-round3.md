**LFC.** Task name: `Celebrity Ozempic LFC R3`. Supersedes `handoff-20261023-ro24-celebrity-ozempic-round3.md`.

# RO-24 "Reacting To Celebrity Ozempic Transformations": round 3 handoff (2026-10-24)

Round 3 builds a reusable background template for green-screen reaction videos and applies it to this film, with the real
interview clips and before/after photo pairs. Dan's words and decisions are below; follow them exactly.

## Read first
`Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`,
`.claude/skills/_shared/GRAPHICS-STANDARDS.md` + `_shared/hyperframes/README.md`, memory `green-screen-background-cycle` and
`chroma-key-efficiency` (`Docs/memory/`), the round 2 recipe `.claude/skills/longform-edit/reference/ro24/round2/README.md`.

## Dan's round 2 reply (2026-10-23/24), in short
- **Key: good, locked. Graphics: good.** But the key cost far too much: "it wasn't better than what Codex did, and Codex did this in
  much less time... not acceptable." Do NOT re-key anything: all 16 plates for the whole film exist (`round2/key/R*.mkv`); backgrounds
  composite onto them.
- **Background: never plain.** He approved 7 of 8 mockups (`/Volumes/Expansion/_edit_work/RO-24/round3/mock/background_options.jpg`
  and `background_options_2.jpg`), rejected 5 (built TV wall):
  1. the person's clip or photos behind him, softened; 2. their clip full screen, him reacting in a corner (bigger than in reaction
  Shorts), and "occasionally put me to the side while the clip plays in the background"; 3. a scrolling photo wall; 4. side panel:
  their before/after with weight lost and medication, him beside it; 6. floating tilted photo cards drifting behind him; 7. big faint
  type of the number and the drug "when we mention the numbers"; 8. the realistic studio set (Codex plate `round3/mock/set_plate.png`)
  with the person on its wall TV.
  "Cycle through all of these options where it's appropriate... right after the intro clip, the floating cards, or the pictures
  scrolling through... put extra effort into establishing a format for this kind of video... a template for making these visually
  interesting."
- **Intro montage (P0):** each person with weight lost and medication. Approved wording: Sharon Osbourne "42 lb, Ozempic"; Fat Joe
  "200 lb, Ozempic"; Amy Schumer "50 lb, Mounjaro"; Meghan Trainor "60 lb, Mounjaro"; Oprah "Down to 155 lb, GLP-1"; Tracy Morgan
  "On Ozempic, gained 40 lb". (Sources and caveats: the round 2 chat; Meghan's 60 lb is her total since 2021, Oprah never named the brand,
  Tracy's 40 lb was a joke he walked back.)
- **Photos:** before/after pairs with total weight lost and medication on them when known; Sharon's before/after throughout the video;
  different photos or pairs later in the film, no repeats where possible. Download more (standing permission to download anything).
- **Clips:** get the celebrities' interview clips and work them into the film. Available at 1080p (checked 10-24): Sharon E! News
  `oZTHGIoqwI4` (script: 0:00-0:28), Fat Joe Page Six `XkGHIKXLShA` (0:00-0:20), Amy Howard Stern `unx1EuJ8t9s` (1:05-1:27), Meghan ET
  `DNTlfd8Cbk4` (0:28-0:46), Oprah/Serena `g7pw3MJ7QVE` (53:28-53:44). Tracy Morgan's Tonight Show moment (March 2024) is not in the
  script: find it. Downloader: `~/.cache/absbyai/ytdlp/yt-dlp_macos --js-runtimes node`.
- Still open from the round 2 page (re-offer on the round 3 page, defaults in brackets): B-roll at 4:15, AI bench press A or stay on
  camera B [A, in the film now]; AI clip ideas A1-A8 (`round2/ai_ideas.json`) [none until he picks]. Polish from the re-check: G12's last
  row in on "keep losing" (about 3 s on screen); G14's small top lines in CAPITALS.

## Work
1. **The template (reusable, the main deliverable):** a shared module (e.g. `.claude/skills/_shared/greenscreen-bg/`, README + code)
   that renders each approved background type for a keyed presenter: input = presenter plate frame (colour + alpha), section assets
   (clip, photos, before/after pair with weight and drug, numbers), film time; output = the composited frame, with Dan's placement per
   type (centred; shifted for 4/7 and "clip behind, Dan to the side"; corner for 2). Real motion in every type (drift, scroll,
   parallax, the clip playing), Soft Blue Light styling for any text (HyperFrames where text animates). Plus a planner rule set:
   background changes only on cuts, roughly every 8-20 s; type chosen by what is said (intro aftermath 6/3; a clip exists 2 or clip
   behind; a number said 7; a transformation 4; long commentary 8 or 1); no type twice in a row; no photo repeated where avoidable.
   Studio set 8: one plate for the whole film; match Dan's light to it (dimmer, warmer edges, soft floor shadow).
2. **This film's background plan** (`round3/bg_plan.json`, film-time segments on the existing cuts of `round2/edl_film_pic.json`),
   the clips trimmed to the script's cues and graded, the new photos and pairs, P0 with the approved wording.
3. **Show Dan first (round 3 page):** the first ~2 minutes (intro through Sharon into Fat Joe) with the full cycle, a 10-15 s sample of
   every background type in context, the open B2 and AI choices. The complete film is round 4, after he locks the template.

## Efficiency (Dan's rule)
No re-keying. Render through the queue (`renderq.py run --group RO-24`), at most two heavy jobs, `WORKERS=3`; estimate CPU before any
heavy step and say it; stop at once if Dan or the render-line check asks (all steps resumable). Prefer composing at 1080p from the
2880 plates; never re-render the whole film to test a look: test on 10-15 s windows (`assemble16.py --g0 --g1`).

## Where things are (work dir `/Volumes/Expansion/_edit_work/RO-24/`, round 2 in `round2/`)
Plates `round2/key/R*.mkv` (+ `.mkv.json`), timelines `round2/edl_film.json` (audio) / `edl_film_pic.json` (picture, S framing under
side cards, T either side), voice `round2/audio/film_voice_A.wav` (final), graphics + photo scenes + B-roll `round2/film_manifest.json`
(`round2/hf/` with GRAPHICS-REPORT.md; `round2/broll/`), photos `round2/photos/` (20, `photos.json`), assembler `round2/recipe/assemble16.py`
(compose per frame: replace its single static background with the template), page builder `round2/recipe/page_r2.py`, review server
`_shared/review_server.py <port> <dir>` (re-run after every rebuild: it serves a cached copy). Round 2 reviews:
`round2/review/INDEPENDENT-R2.md`, `INDEPENDENT-R2-RECHECK.md`. A fresh `ra-reviewer` checks the round 3 page before Dan.

## Model
Claude: Opus 5.5, high effort.

## Starter prompt
> Celebrity Ozempic LFC R3. Read `Handoffs/handoff-20261024-ro24-celebrity-ozempic-round3.md` and execute round 3 of "Reacting To Celebrity Ozempic Transformations" (RO-24) with /longform-edit: build the reusable green-screen background template Dan approved, apply it to this film with the interview clips and before/after photos, and deliver the round 3 page.
