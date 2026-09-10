# Handoff — finish the thumbnails for the five finished ads and install them on YouTube

Written 2026-09-10 after two rounds with Dan. Everything below is his decision; nothing is left to taste except
the one background design he asked for, which he has NOT seen yet and must approve before install.

## What Dan decided (2026-09-10, verbatim where it matters)

1. **Ad 2 "Stop Wasting Money on Nutritionists" — DECIDED, ready to install.** "Let's use the jeans photo … the
   black and red background one, not the artificial background." That is variant **C** — the jeans photo
   (`studio-blue-173`) on the black ground with the red wash and embers. Both files already exist and passed QC:
   - Muhammad 16:9 `Dtk5knWM7c8` →
     `social media graphics/youtube/thumbnails/Ad 2 Stop Wasting Money On Nutritionists/ad2-muhammad-16x9-Dtk5knWM7c8_C-jeans-black-FINAL.jpg`
   - Vertical `7XgHxn59Tsg` →
     `…/ad2-vertical-7XgHxn59Tsg_C-jeans-black-9x16-FINAL.jpg` (1080×1920)
2. **Ad 1 "How to Use AI to Get in Shape" — REBUILD, then Dan approves.** "Switch that picture to the picture of me
   with my arm behind the head in the Muay Thai shorts" — that is the cutout `studio-blue-89` (arm behind head, black
   and gold Thai shorts, serious face; ruler-measured waistband at 0.57 of the cutout box, clip at 0.60). He first said
   the black-and-red ground, then corrected himself: **"Actually, let's make the background something kind of
   cleaner and more trustable for that one."** So: NOT the Carter black/red/embers ground and NOT the generated
   yacht/rooftop scenes. Copy stays **HOW TO USE AI / TO GET IN SHAPE** (no claims — compliance rule in
   `/youtube-packaging`). Three videos: Muhammad 16:9 `lf46ytHacss`, Zeeshan 16:9 `1oEcwdp21Fg`, vertical `Iz0u8KHRbyE`
   (9:16). The round-2 pool-photo files for Ad 1 are superseded by this decision.
3. Standing rules from the same review, already saved: no claims in ad thumbnail copy; a vertical ad gets a 9:16
   thumbnail; pool photos crop at the waistline. (`/youtube-packaging`, `/coverimage`, memory `thumbnail-no-claims`.)

## The "cleaner, more trustable" background — build two, show him, he picks

Build both as a 16:9 and a 9:16, on the `studio-blue-89` cutout, house type (Manrope ExtraBold white caps, red
accent bar, white wordmark `Media/video_edit/work/logo_white.png` top-left — the banner-derived system Dan approved
2026-08-07 as the trustworthy look). No grunge, no embers, no red wash, no arrows.

- **Option 1 (recommended default): clean dark studio.** Smooth charcoal-to-slate vertical gradient
  (`rgb(5,7,11)` at the edges rising to about `rgb(38,42,50)` behind him), a soft neutral-white spotlight ellipse
  behind his torso (strength ~0.35, no colour), faint grain so it reads as a photo ground. Subject at cx 0.74 (16:9)
  / centred with head top at 0.40 H (9:16), frame clipping him at 0.60 of the cutout box. Type left-stacked (16:9) /
  top band (9:16). This is the ab-wheel "grey-blue" ground with the red taken out and the light turned neutral.
- **Option 2: his own studio backdrop, widened.** Do not cut him out at all — take the ORIGINAL
  `photos/finalized social media photos/studio-blue-89_FINAL_PRIMARY.jpg` and extend its pale blue-grey seamless
  backdrop to 16:9 / 9:16 (programmatic: sample the backdrop gradient column at the frame edge and extrude it, or a
  gen-fill with the widening recipe — the backdrop is a plain gradient, so the extrude is enough and costs nothing).
  Type in **charcoal `rgb(20,22,28)`** with the red bar; wordmark in charcoal too (recolour the white PNG, keep
  alpha). Brightest, most "real photo" of the options; risk is that dark-on-light is off the channel's white-on-dark
  system — that is why Dan sees both.

Assert text clearance on the finished file exactly as `r2/build_bc2.py` / `r2/build_house2.py` do (person mask or the
cutout alpha; ≥ 25 px side clearance for 16:9, ≥ 40 px above his top for 9:16). Send a labelled review sheet
(both options × both aspects) and stop for his pick.

## Install — by API, not Studio

`thumbnails.set` is already called in `scripts/youtube/upload.js` (lines ~222-233) and needs only `youtube.upload`,
which the stored refresh token has. Add a `--set-thumbnail-only <videoId>` mode (or a 30-line
`scripts/youtube/set-thumbnail.js` that reuses the token code) rather than driving Studio's clipboard-paste trick.
Then:

1. Ad 2 now (decided): set `Dtk5knWM7c8` ← the 16:9 C file; `7XgHxn59Tsg` ← the 9:16 C file.
2. Ad 1 after Dan's pick: `lf46ytHacss`, `1oEcwdp21Fg` ← the 16:9 pick; `Iz0u8KHRbyE` ← the 9:16 pick.
3. **Verify by reading back** `videos.list?part=snippet&id=…` → `snippet.thumbnails.maxres.url` fetches and is the
   new image (compare a downscaled hash, not the byte size). Also open each watch page once: a 1080×1920 thumbnail
   on a long vertical video (these are 3:53 and 4:37, not Shorts) is shown pillarboxed in the 16:9 player slot —
   screenshot it for Dan and keep the 16:9 file of the same design beside it as the fallback if he dislikes the
   bars. The Google Ads preview uses the same thumbnail; check it in the ad's preview after the campaign is built.
4. Record the installed file next to each id in `Docs/AD_VIDEO_IDS.md` (new "Thumbnail" column).

## Files and scripts

- Build dir: `social media graphics/youtube/thumbnails/_finished-ads-build-2026-09-10/` — `DELIVERY.md` (both rounds,
  costs, eight traps), `r2/build_bc2.py` (blue-89 Carter builds — copy its layout numbers, swap the ground),
  `r2/build_jeans.py` (jeans set, includes the two generated environments), `r2/build_house2.py` (house type +
  clearance assert, 16:9 and 9:16). The Carter device library is imported from
  `…/The 17 Dollar Ab Wheel Beats Every Crunch/_build-2026-09-01/build.py|build2.py`.
- Delivery folders: `…/thumbnails/Ad 1 This Picture Got Me Abs/` and `…/Ad 2 Stop Wasting Money On Nutritionists/`.
  Park anything superseded in `_finished-ads-build-2026-09-10/_superseded-round1/` (or a `_superseded-round2/`), never
  delete. Both folders are git-ignored (`social media graphics/`).
- Clean environment photos (for Dan's own use, AI backgrounds, label if posted): `photos/ai-environment composites 9-10-26/`.
- Video ids and status: `Docs/AD_VIDEO_IDS.md`.

## Traps (paid for on 2026-09-10)

- `personmask` is `personmask OUTDIR IN...`; the wrong form exits 0 and writes nothing.
- Fit the type to the mask with a 45 px margin and assert 25 px on the finished file, over the SAME rows (the
  running `yy` carries one extra lead after the last line).
- If you gen-fill anything: check the composite IoU, regenerate below 0.9 — the model slid or shrank Dan in 3 of 17
  fills today even with the composition lock. Option 1 above needs no generation at all.
- Ask before spending past the session cap; Option 2's extrude is free and Option 1 is pure PIL.
- No dashboard row exists for this work and Dan has not asked for one — do not add one. When the install is
  verified, delete the "Thumbnails for the 5 finished ads" entry from `AI_COORDINATION.md`, remove this handoff from
  its HANDOFFS list and from `Handoffs/README.md`.

## Recommended model and starter prompt

Fable 5.1, medium effort (PIL compositing, one small Node script, API verification — no video pipeline).

```
Execute Handoffs/handoff-20260910-ad-thumbnails-finish.md. Install the decided Ad 2 thumbnails by API first, then
build the two "cleaner, more trustable" background options for Ad 1 on the arm-behind-head Muay Thai cutout in
16:9 and 9:16, send me one labelled review sheet, and stop for my pick. After I pick, install those three and
verify by reading the thumbnails back.
```
