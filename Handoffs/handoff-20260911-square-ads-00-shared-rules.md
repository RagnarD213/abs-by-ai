# Square (1:1) ad versions — the rules shared by every per-ad handoff

**Written 2026-09-11. Dan's instruction from his Google Ads rep meeting: "RE EDIT ALL AD VIDEOS IN SQUARE IN ADDITION TO
VERTICAL" — one handoff per finalized ad video (`handoff-20260911-square-ad*.md`). This doc holds what is common so the
six per-ad docs stay short. Read this first, then the ad's own doc, then `/shortad-from-longform` in full.**

Why the rep asked: a Demand Gen video ad serves across YouTube in-feed, Shorts, Discover and Gmail, and Google fills
each placement from the aspect ratios the ad carries — 16:9, **1:1** and 9:16. We have 16:9 + 9:16; the square fills the
in-feed / Discover / Gmail slots at full size instead of a letterboxed 16:9. Meta feed takes 1:1 too. The square goes
onto the SAME Demand Gen ad as one more `videos` entry (`/ad-setup` step 6), not a new ad.

## What a square build IS — and is not

* **It is a re-layout of the approved VERTICAL build, not a third recovery of the editor's cut.** Every vertical build
  dir already holds the recovered EDL (`edl_*.json`), the editor's grade (`his.cube`), his framing/zoom schedule
  (`fit.json`), the face/torso track (`crop.json`), the beat sheet (`beats.py`), the lifted assets, the caption
  alignment (`words_ctc.json`) and the cut plan (`cut_plan.json`). **Copy the build dir to `<ad>-sq/` and reuse all
  of it; only the geometry and the per-beat renderers change.** Re-deriving the EDL is a day of work for nothing.
* **Frame count = the editor's, to the frame; fps = his** (29.97 for Muhammad, 24 for Zeeshan). The square's
  timeline is identical to the vertical's, so the cutdown plan and the caption timings carry over unchanged.
* **Audio = whatever the approved vertical of that ad carries, bit for bit** (its AAC stream, md5-asserted at mux),
  so Dan hears exactly what he already approved. Where the vertical is not yet approved, the editor's untouched mix
  from his HD (`AGENTS.md` "An editor's finished mix is delivered UNTOUCHED"). Gate: `audio_gate.py --reference-mix
  <his> --verbatim`. Never loudnorm, never mono, never a lift Dan did not ask for.
* **Output: 1080×1080, H.264 High, 8–12 Mbps, BT.709 tagged, AAC 320k**, named per the editor-deliveries convention:
  `<title> | claude | 1x1 | ad N.mp4` and `<title> | claude | 1x1 59s | ad N.mp4`, plus `REVIEW 540p` copies, the
  `.audio_gate.json` stamps, `notes-square.md` and `recipe-square/` beside the vertical in the ad's folder.
* **Standing content rules override the reference** (skill section of that name): AI-GENERATED chip on every AI
  image/clip; **"Real picture of me — not AI-generated"** on every real after picture of Dan (`AGENTS.md`, 09-11);
  the banned email-capture screen never appears; no unbelievable claims in on-screen text; Dan's own headline copy.

## Square translation rules (derived from the vertical rules in Step 5; not yet paid for on a build — the watch pass
## and the audit decide where they bend. Record every deviation in `notes-square.md`.)

1. **The talking head is a 1080×1080 crop of the 1080p source at 1.00× — no upscale at all.** This is the square's one
   free advantage over the vertical (which is a 1.78× upscale). Crop x follows the smoothed face track (rule 11) and
   the editor's punch-in schedule is reproduced as ramps (rule 8, `push_z_expr`); hair-anchored NEAR/FAR framing
   (memory `framing-standard-hair-anchored`, `zhairgate2.py` rebound for 1080 tall).
2. **Two beat families, not one.** *Stacked* (his text-left / Dan-right window screens): Dan in a full-width window at
   the top, height adapting to the wrapped text, clamped **560–700 px**, text on the field below in his tokens.
   *Side-by-side* (portrait media: the phone recording, a portrait photo beside Dan): keep the editor's own left/right
   layout — Dan in a ~520×1080 crop on one side, the media on the other — because a 1:1 frame has the width for it.
   Pick per beat by measuring the wrapped text; never one fixed compromise.
3. **16:9 media never goes full-bleed.** His AI clips and the app recording go in his card at the media's own aspect
   (1080-wide card → 16:9 hole 1080×608, a downscale); the hole matches the file's aspect (rule 4).
4. **Real after pictures (Dan's 09-11 rule: vertical and full screen).** A square cannot show a 2:3 portrait full-bleed
   without cutting head or shorts (rule 12). Default: **two portraits side by side, each 540×1080** (a 2747×4096 pool
   or studio still crops to 1:2 keeping hairline-to-shorts); a lone picture goes **full height, centred on the field**
   with the editor's card margins — never blurred pillars, never mirror padding. Contact-sheet the rendered frames.
5. **Captions:** PIL-rendered word-timed Manrope from `words_ctc.json`, centred at **y≈900**, suppressed under any
   graphic that carries its own words. **Safe area:** nothing that must be read below **y≈980** or above **y≈80**,
   nothing readable in the right-hand 100 px (in-feed UI). Labels (AI / real-picture chips) sit low on the frame
   above the caption band, never over a face.
6. **SFX only on graphic entrances, at HIS count** ([R1]); flashes on his frames from the vertical's beat sheet.
7. **The cutdown reuses the vertical's `cut_plan.json`** frame for frame (same timeline); rebuild only the picture.

## Build order

```
cp -R /Volumes/Extreme/_edit_work/<ad>-vert /Volumes/Extreme/_edit_work/<ad>-sq   # never build inside the vertical's dir
edit the compositor's geometry constants (W=H=1080), the plate/window/card builders, captions y, safe area, hair gate bounds
render → mux (his stream copied, md5 asserted) → cutdown → every gate on the exact delivered files
```
Gates (all mandatory, in the build dir, on the delivered files): `qc.py … --build-dir .` (20/20; `qc.json`'s
per-cut numbers set for 1080×1080 — a qc.py edit for the new dims is a gate change → `python3
.claude/skills/_shared/qc_corpus/run.py` must pass before it is committed), the watch pass (`watch.py` +
`zwatch_sheets.py` + a written `zwatch_mark.py` record), `zhairgate2.py`, `caption_sync_check.py`, `landing_check.py`,
`audio_gate.py --verbatim`, the naked-jump-cut scan (7c), and **the independent Fable subagent audit (7b) — expect a
"does not ship" first time.** Two concurrent video builds max across sessions (`AGENTS.md`); check `ps` first.

## After the build

1. Send Dan the 540p review copies + the audio A/B; **the square is approved only when Dan says so** (verticals rule).
2. On approval: upload unlisted to the Abs by AI channel (`scripts/youtube/upload.js`, 1:1 thumbnail per
   `/youtube-packaging`, AI-content disclosure yes), add a row to `Docs/AD_VIDEO_IDS.md`, then `/ad-setup` step 6 —
   one more `videos` entry on the ad's existing Demand Gen ad groups (`Docs/DGEN_CONVERSION_CAMPAIGN.md` has the
   ids), `client.js policy 24243839443` the next day. Muhammad's/Zeeshan's own 16:9 stays the primary video.
3. Board: delete the ad's square line from `AI_COORDINATION.md` HANDOFFS, `Handoffs/README.md`, and the
   dashboard **Handoffs to fire** list if Dan put it there. No new dashboard row (his 09-08 rule).

## Firing order (what is blocked on what)

| order | doc | fire when |
|---|---|---|
| 1 | `…-square-ad2-muhammad.md` | now — vertical approved 09-08, nothing blocks |
| 2 | `…-square-ad1-muhammad.md` | now — vertical approved 09-10 (attempt 3), older pipeline |
| 3 | `…-square-ad5-muhammad.md` | after `handoff-20260911-ad5-vertical-revisions.md` runs (the square inherits its six picture changes) |
| 4 | `…-square-ad4-muhammad.md` | after the Ad 4 vertical (session running 09-11) is delivered AND Dan approves it |
| 5 | `…-square-ad3-muhammad.md` | after Muhammad re-exports Ad 3 to the approved draft AND the vertical is approved |
| 6 | `…-square-ad1-zeeshan.md` | after Dan approves the re-delivered Zeeshan Ad 1 vertical (his audio untouched) |

Model for every one: **Fable 5.1, effort high** (compositor geometry + the audit loop). Each is one session.
