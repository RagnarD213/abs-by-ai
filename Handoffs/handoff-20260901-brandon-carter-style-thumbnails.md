# Handoff — Brandon Carter-style thumbnails, built from the REAL studio cutouts on the Mac

- **Date:** 2026-09-01
- **Handing off from:** Claude Code (cloud session, `claude/youtube-thumbnail-concepts-4efv1z`)
- **Handing off to:** Claude Code, fresh session **on Dan's Mac** (needs a browser, the photo
  library and yt-dlp — none of which a cloud session has)
- **Project:** Abs By AI — YouTube channel
- **Business goal:** marketing performance (thumbnail CTR on the long-forms)
- **Skill:** `/youtube-packaging` for the build conventions and delivery paths; `/background-removal`
  only if a needed frame has no cutout yet
- **Spend:** $0.00 expected. No AI generation is needed — the cutouts exist and the rule is never to
  AI-repaint Dan's photos. No production code, no deploy, no native-retest trigger.

---

## Objective

Look at Brandon Carter's actual thumbnails (`https://www.youtube.com/@HighLifeWorkout/videos`),
work out his style from the real images rather than from memory, then build **three finished
1280x720 thumbnails in that style** using the **real studio cutouts** in
`photos/finalized social media photos/_cutouts/` — and show them to Dan beside the Brandon Carter
originals they copy.

## Why this exists — read this before building anything

The cloud session that wrote this could not reach YouTube at all (youtube.com, i.ytimg.com, seven
Invidious/Piped mirrors, image proxies, Bing/Google image search, brandoncarter.com and Instagram
are ALL egress-blocked from cloud sessions). It built three "Brandon Carter style" boards from prior
knowledge of his channel and from his title conventions, using low-resolution pool-shoot stand-ins
(429x640 gallery images keyed with `rembg`) because `photos/` is gitignored and not in the cloud.

**Dan's verdict on those boards, and on the five cutout concepts made the same day: "These all
look very bad."** Do NOT start from them. They are on the canvas at
https://claude.ai/code/artifact/92369b3e-c89c-46b1-b657-afe91ba506b0 only as a record of what was
rejected. The likely reasons they failed, so you avoid them:

1. **Style was guessed, not observed.** Nobody in that session saw a single Brandon Carter
   thumbnail. Step 1 below fixes that: measure his real images first.
2. **Stand-in photos at 500-800 px** instead of the 3368x5056 studio cutouts. Soft, small, wrong
   backdrop light.
3. **Fallback fonts in the preview** (the condensed face never loaded in the headless render) and
   generic type sizing. His type is a specific weight, size and stroke — measure it.
4. **Flat vector backgrounds** (plain gradients, stripes) where his thumbnails carry a real, graded
   photo or a dense composite. A gradient rectangle reads as a template.

## Current State

- **100 studio cutouts exist**: `photos/finalized social media photos/_cutouts/studio-<blue|gray|white>-<n>_CUTOUT.png`,
  full-res RGBA (3368x5056 portrait, a few landscape), 2 px alpha contraction baked in, verified
  clean on all three backdrops (2026-08-31). Every finalized studio pick has one; the pool-shoot
  `photo-N` finals deliberately do NOT.
- **Finalized studio photos** (the sources): `photos/finalized social media photos/studio-<bg>-<n>_FINAL_PRIMARY.jpg`.
- **Logo (white wordmark with alpha):** `Media/video_edit/work/logo_white.png` (360x111). The old
  `logos/03-symbol-left-text.png` path is dead.
- **House thumbnail conventions** (Manrope ExtraBold, red `rgb(201,48,45)` bar, radial scrim,
  two A/B variants per video) are in `/youtube-packaging`. **For THIS job Brandon Carter's style
  overrides the house type treatment** — that is the whole point of the test. Dan's hard rules
  still apply (below).
- **Delivered but still-unpackaged long-forms that could carry these** (pick one, or ask Dan):
  `claude edited long form content/01 - My First Spray Tan`, `02 - My Honest Zepbound Update`,
  `03 - The Supplements I Actually Take`, and the ab-wheel organic video
  (`EDITED LONGFORM 8-20-26/abwheel-17-dollar-ab-wheel/`, "The $17 Ab Wheel Beats Every Crunch").
  Default if Dan does not say: **the ab-wheel video** — its "ab wheel beats crunches" message is
  the closest fit to Carter's STOP-X / DO-THIS format.

## Dan's hard rules (unchanged, all from `/youtube-packaging`)

- **Abs visible in every variation, and text must NEVER overlap them.** Assert on the rendered
  file with a person mask, not on the plan.
- **Never AI-repaint Dan's real photos.** Composite programmatically over the untouched cutout.
  No AI-generated bodies, no video stills unless Dan says so.
- Side-by-side before/after is **banned in paid ads only**; organic thumbnails may show a
  transformation, but the video must deliver it.
- Canvas 1280x720 JPG under 2 MB. Finals go in
  `social media graphics/youtube/thumbnails/<Video Name>/` (own subfolder per video, never loose),
  keep `-nologo` variants alongside the `-FINAL`s.
- `photos/` and `social media graphics/` are gitignored and this repo is PUBLIC — `git check-ignore`
  any new output path before finishing.

## Detailed Plan

### 1. Pull his real thumbnails (15 min)

```bash
cd ~/absbyai-video-work && mkdir -p bc-thumbs && cd bc-thumbs
# top 40 by popularity + the 20 most recent — his style changed between the HighLifeWorkout era
# (2012-2017, gym, "PSYCHO ABS WORKOUT") and the King Keto era (2019+), and Dan should see both.
yt-dlp --flat-playlist --playlist-end 20 --print "%(id)s|%(upload_date)s|%(view_count)s|%(title)s" \
  "https://www.youtube.com/@HighLifeWorkout/videos" > recent.txt
yt-dlp --flat-playlist --playlist-end 40 --print "%(id)s|%(upload_date)s|%(view_count)s|%(title)s" \
  "https://www.youtube.com/@HighLifeWorkout/videos?view=0&sort=p" > popular.txt
cut -d'|' -f1 recent.txt popular.txt | sort -u | while read id; do
  curl -s -o "$id.jpg" "https://i.ytimg.com/vi/$id/maxresdefault.jpg" || true
done
```

If yt-dlp is throttled on the channel listing (it was on one video on 2026-08-28), use the Chrome
MCP in Dan's real Chrome: open the Videos tab sorted by Popular, and read the `ytInitialData`
thumbnail URLs from the page (`find` on `i.ytimg.com/vi/`). `--flat-playlist` needs no video
download and has never been blocked so far. Falls back to `hqdefault.jpg` (480x360) where no
maxres exists — old videos often lack one.

Build two contact sheets (popular, recent), 5 columns, titles and view counts burned under each
tile, and **send both to Dan in chat** — he asked to see them, and it is the only way he can check
the next steps against the source.

### 2. Measure the style — do not describe it from memory (20 min)

On the top ~20 popular thumbnails, measure and write down in `bc-thumbs/STYLE.md`:

- **Palette:** k-means (k=5) over all 20; report the dominant background colour family, the
  text colours (expect white / yellow / red but MEASURE the hex), and stroke colour.
- **Type:** word count per thumbnail (median), cap height as a fraction of frame height, number of
  lines, alignment (left / centred), whether there is a stroke and its width in px at 1280, drop
  shadow yes/no, which words are colour-highlighted. Identify the face by comparison against
  Impact, Anton, Bebas Neue, Montserrat Black and Oswald — Impact ships with macOS
  (`/System/Library/Fonts/Supplemental/Impact.ttf`); Anton/Bebas/Montserrat/Oswald are free
  Google Fonts (download the TTFs, installing fonts needs no permission).
- **Subject:** how big he is (person-mask height as a fraction of frame), where he sits (left /
  right / centre third), shirtless or not, expression register, whether he is cut out on a graphic
  ground or in a real photo, and whether he is looking at the camera or at a prop.
- **Marks and props:** arrows, circles, X marks, food, supplements, before/after splits — count
  how many of the 20 use each.
- **Background:** real photo, darkened photo, flat colour, or gradient — count.
- **Era split:** note which of the above differ between the 2012-2017 videos and the 2019+ ones.
  Dan should pick the era; default to whichever holds more of the top 20 by views.

Use `.claude/skills/shorts/reference/recentre/personmask.swift` (Apple Vision) for the subject
measurements — it is the tool every recent session used and it is calibrated.

### 3. Pick three of HIS thumbnails to copy, one to one (5 min)

Choose three that (a) sit in the top 20 by views, (b) use three clearly different layouts
(e.g. big-body-plus-stacked-type, correction/red-X, arrow-to-prop or before/after), and (c) have a
pose that exists in the studio library. This is the same discipline as `/shortad-from-longform`:
reproduce a specific reference beat for beat, log every deviation with a reason. Vague "in his
style" is what produced the rejected boards.

### 4. Pick the cutouts (10 min)

Build a contact sheet of all 100 `_CUTOUT.png` files on a dark canvas (the 2026-08-31 sheet lived in
a scratchpad and is gone), then choose one cutout per reference thumbnail matching HIS pose
register — a flex for a flex, hands-on-hips serious for a correction, arm-out for a point. Poses
known to be in the library: double-biceps flex (blue-66), boxing guard (blue-84/266, gray-63),
hands on hips (dozens), arms behind head (blue-80 etc.), archer/point (gray-48), several
closed-lip smirks and hard serious faces (blue-221, blue-271, gray-90). ⚠ **Judge a key at usage
scale, not off a 170 px tile** — blue-153 LOOKED headless on a tile and was complete at full size.

### 5. Build (60-90 min)

PIL, 1280x720, one script per thumbnail, kept beside the outputs (`_build-2026-09-xx/` in the
video's thumbnail folder, with every measured number in a config block — copy the pattern of
`social media graphics/youtube/thumbnails/3 Minute Total Body Home Workout/_build-2026-08-30/`).

- **Background:** if his top thumbnails carry a real darkened gym/room photo, use a REAL photo:
  the studio backdrop frames themselves (a `_FINAL_PRIMARY.jpg` with Dan cropped out and the
  backdrop stretched), or the 7-31-26 pool-shoot scenery via the `scene` layout in
  `/youtube-packaging`, or the generative-fill widening recipe from the 2026-08-30 build (that one
  is $0.13 and is the one sanctioned AI use — background only, subject composited back). If his
  top thumbnails are flat colour, match the measured hex, not a guess.
- **Type:** the measured face, size, stroke and colours from step 2. Copy text is Dan's video's
  own hook, in Carter's register (his real titles: "PSYCHO ABS WORKOUT", "ABDOMINAL ASSAULT",
  "How to get a six 6 pack and burn belly fat FAST"). Keep the word count at his median.
- **Cutout:** full-res `_CUTOUT.png`, downscaled ONCE with LANCZOS to its final size — never
  upscale. Match the stroke/glow treatment you measured on him.
- **Logo:** only if his thumbnails carry branding; he generally lets the channel avatar do it.
  Dan's standing rule is to keep a `-nologo` variant either way.

### 6. QC on the rendered files, not the plan (15 min)

- Person-mask the finished 1280x720, take the band between the headline's top and bottom, and
  require **≥25 px clearance** between the text and Dan (the 2026-08-30 assert). Abs inside the
  frame and uncovered on all three.
- **Glance test:** downscale each to 168x94 and put it in a row with his three references at the
  same size. If ours is not the one you would click, fix before sending.
- **His | ours side by side at full size** on one sheet, per thumbnail. This is the deliverable
  Dan judges by — he explicitly asked to see the originals.
- `git check-ignore` the output folder; no personal photo may reach the public repo.

### 7. Deliver

Send Dan: the two channel contact sheets from step 1, the three his|ours comparison sheets, and
the three finals. Say in one line which era you copied and why. Do NOT install anything in YouTube
Studio — that happens only when Dan picks one, per `/youtube-packaging`.

Then: update `AI_COORDINATION.md` (this task's entry is at the top of the Active task section),
and check off the dashboard task `money::Execute handoff: Brandon Carter-style thumbnails from the
real studio cutouts (Mac session)` via `/dashboard-tasks` — the cloud session could not reach
absbyai.com, so the task row was added by editing `todos.json` on the branch instead and only
appears once that branch merges to main.

## Things to Avoid / Lessons Learned

- **Do not reuse the rejected canvas boards' layouts, copy or colours.** Dan: "These all look
  very bad." Start from his real thumbnails.
- **Everything YouTube-shaped is egress-blocked from cloud sessions** — channel pages, image
  host, mirrors, proxies, image search. Thumbnail research is a Mac job; do not burn a cloud
  session on it again.
- **Never ship a headless-render preview whose webfont did not load** — the rejected boards were
  previewed in a fallback face, so the type Dan saw was not the type designed.
- **Low-res stand-ins do not preview a thumbnail** — the softness reads as "bad", not as
  "placeholder". Use the real files or do not show it.
- The general thumbnail research from the same day still stands for the HOUSE style (3 elements,
  2-4 words, real expressions, 4-8 px stroke, centre-70 % safe zone, Test & Compare judges
  watch-time not CTR, don't print "over 40" by default) — but when the brief is "in Carter's
  style", copy Carter; his thumbnails break several of those rules on purpose.
- `sips -Z` sets the LONG edge; on portrait cutouts divide by the real width you read back.
- A Mac session with Dan's Chrome can also just screenshot the Videos tab — 30 seconds, no tooling.

## Relevant Files & Locations

- Cutouts: `photos/finalized social media photos/_cutouts/` (100 files, gitignored)
- Finals (sources): `photos/finalized social media photos/studio-*_FINAL_PRIMARY.jpg`
- Output: `social media graphics/youtube/thumbnails/<Video Name>/` (gitignored; create the subfolder)
- Reference build with measured asserts: `social media graphics/youtube/thumbnails/3 Minute Total Body Home Workout/_build-2026-08-30/`
- Person mask: `.claude/skills/shorts/reference/recentre/personmask.swift`
- Logo: `Media/video_edit/work/logo_white.png`
- Skills: `.claude/skills/youtube-packaging/SKILL.md`, `.claude/skills/background-removal/SKILL.md`
- Rejected mockups (record only): https://claude.ai/code/artifact/92369b3e-c89c-46b1-b657-afe91ba506b0
- His channel: https://www.youtube.com/@HighLifeWorkout/videos (also `@kingketo` on Instagram)

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Opus 5, high effort.** Steps 2-3 are visual judgement on real images and the build is a beat-for-beat copy with measured asserts — the same class of work as `/shortad-from-longform`, where Sonnet-level guessing is what got rejected. |
| **If Claude usage is high / approaching a limit** | **Claude Sonnet 5, standard thinking**, but insist on step 2's measurements being written to `STYLE.md` before any pixel is drawn. Codex is not a fit: this is brand/marketing judgement and it needs to look at images in Dan's Chrome. |

Always-Claude task type (marketing creative), so no Codex branch. Fable is a reasonable middle
option if available at the time; check its pricing then.

## Starter Prompt for the Next Task

> Execute `Handoffs/handoff-20260901-brandon-carter-style-thumbnails.md` with `/youtube-packaging`.
> First pull Brandon Carter's real thumbnails (`https://www.youtube.com/@HighLifeWorkout/videos`,
> top 40 by views plus 20 most recent — yt-dlp `--flat-playlist` then i.ytimg.com maxres) and send
> me two contact sheets. Then MEASURE his style (palette, type, subject size and position, marks,
> background) into `STYLE.md`, pick three of his top thumbnails with different layouts, and rebuild
> each one to one from the real studio cutouts in `photos/finalized social media photos/_cutouts/`
> for the ab-wheel video unless I say otherwise. Deliver his|ours side-by-side sheets plus the three
> finals. Do not reuse anything from the rejected cloud mockups — I said they look very bad.
> $0 AI spend, no deploy, nothing installed in YouTube Studio.
