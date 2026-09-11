---
name: ad-setup
description: Take a FINISHED ad video (usually an editor's HD final shared as a Google Drive link) all the way to running — file it in the project folder, upload it to YouTube unlisted with a description, chapters, tags, the AI-content disclosure and a clean thumbnail, then add it to the Google Ads Demand Gen conversion campaign (one ad group per landing page, its own audience, compliant copy) and record the ids. Use whenever Dan says an ad is "complete", "final", "approved", sends an HD link and asks to "upload it", "set it up", "add it to the campaign", "put it in Google Ads", or adds a new version (a vertical) of an ad already running — even if he doesn't say "/ad-setup". Reviewing a cut is /revisions; filing alone is /editor-deliveries; thumbnails alone are /youtube-packaging.
---

# /ad-setup — finished ad → YouTube → Google Ads

Built 2026-09-11 on Ads 3 + 4 (Muhammad's HD finals, Dan: *"These two ads are complete. Upload them to YouTube,
set them up with descriptions and everything we need, and add these to our campaign in Google Ads."*). Everything
below was run end to end that day; the ids it produced are in `Docs/AD_VIDEO_IDS.md` and
`Docs/DGEN_CONVERSION_CAMPAIGN.md`.

**Scope.** This is the PAID path: an unlisted YouTube video that Google Ads points at. It does NOT publish the
video organically (public YouTube, Blotato to FB / IG / TikTok). Ad 5 got both only because Dan asked for both — if he
wants it public too, that is `scripts/youtube/upload.js --publish-at` for a separate public copy plus a
`scripts/blotato/ad5_queue.py`-style queue script. Ask nothing; just say in the report that organic posting was not done.

All steps are reversible and covered by standing authorizations (analytics/ads config, bias toward action). Do not
stop to ask. The one thing Claude never does here: enable a paused campaign (`ADS_ALLOW_ENABLE_CAMPAIGN=1` is Dan's).

## 0. Preconditions — 2 minutes, never skip

- **It is really final.** The latest `revision docs/adN-revisions-<editor>-roundM-*.md` reads *APPROVED - FINALIZED*,
  and nothing newer exists (the `/editor-deliveries` three-part rule). Drive `get_file_metadata` on the link:
  `video/mp4`, hundreds of MB, 1080p-class. A 30 MB file is a review draft whatever it is called.
- **Nobody else owns it.** Grep `AI_COORDINATION.md` for the ad. Another session building the ad's VERTICAL
  (e.g. `/Volumes/Extreme/_edit_work/ad3-vert/`) is not a conflict — uploads and the campaign are separate.
- **What version is this?** A first 16:9 for an ad → the full run. A new version of an ad already in the campaign
  (a vertical, a re-cut) → steps 1, 3–5, then step 6 with one more `videos` entry (the builder reuses the groups).

## 1. File the master (curl, no browser)

```bash
curl -sL -r 0-1023 "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t" | head -c 12 | xxd -p
#   …667479706d70… = ftyp = real video. HTML = shared only to Dan's account → /editor-deliveries Chrome recipe.
curl -sL -o "<target>.part" "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"
```

Target: `<Editor> Ad Videos/<title> - ad N/<title> | <editor> | 16x9 | ad N.mp4` (title = the script title,
lowercase, no punctuation, the "Use AI Instead" tail dropped — `stop paying human trainers`, `stop wasting money on
supplements`). Rename from `.part` only when `stat -f %z` equals Drive's `fileSize`. Then `ffprobe` it (1920×1080,
duration). Add a `filed` row to `.claude/skills/editor-deliveries/state.json`. The editor's audio is delivered
untouched — no re-encode, upload the file exactly as he exported it. **But measure it and report it:**
`ffmpeg -i <master> -af ebur128=peak=true -f null -` → integrated LUFS and true peak. Dan's rule for editor
exports is −14 LUFS / ≤ −1.0 dBTP; a miss is Dan's call (accept, or ask the editor for a re-export), never a
reason to process his audio and never a reason to hold the upload. Say the numbers in the report. (Ad 4 V4 HD,
09-11: −13.9 LUFS, −0.90 dBTP, 0 clipped samples — flagged by the Ad 4 vertical session after the upload.)
A re-export replaces the video: upload it new, add it as a second `videos` entry in the ad's config, rerun
`dgen-add-ad.js --apply`, pause the old-video ads.

## 2. Title and tags

- Title = the script title as Dan wrote it (`Stop Paying Human Trainers! Use AI Instead`). It is unlisted; SEO
  does not matter, recognisability in Studio does.
- Tags: `ab workout,abs by ai,ai fitness,six pack abs` + two topic tags.

## 3. Transcript → description with chapters

```bash
node .claude/skills/ad-setup/transcribe.js "<master.mp4>" [second.mp4]     # Replicate Whisper, < 1¢, ~10 s
```

Never run local Whisper for this: another session is usually rendering, and it counts against the two-build cap.

Write `<ad folder>/youtube-description.md` — `Muhammad Ad Videos/stop paying human trainers - ad 3/youtube-description.md`
is the template:

1. Two sentences in Dan's voice: the video's argument, first person.
2. `👉 See what YOU would look like with six-pack abs — free AI preview: https://absbyai.com/?utm_source=youtube&utm_medium=video_ad_description&utm_campaign=dgen-conv-adN`
   (homepage, not /start — organic clicks stay out of the /start A/B test).
3. One paragraph: what the viewer learns.
4. `Chapters` — first at `0:00`, at least three, **every chapter ≥ 10 s including the last** (YouTube silently
   drops all chapters otherwise; Ad 4's 0:41 → 0:49 had to be merged). Numbered points as `1. …`.
5. The disclosure: *Some images in this video are AI-generated, including the "future self" picture of me. The
   before picture and the photo-shoot photos are real. AI-generated goal images are illustrations of a possible
   result, not a guarantee.* A supplement / medication topic adds *This video is not medical advice…*.

Never the word "trick" (Dan's rule), never a result promise in the first two lines.

## 4. Thumbnail — the clean look, both grounds

Dan's standing choice for ad thumbnails is the clean look (Manrope caps, red bar, wordmark; O1 dark studio / O2 his
own backdrop). Neither ground is settled (Ad 1 = dark, Ad 5 = light), so build both and install one.

```bash
python3 .claude/skills/ad-setup/ruler.py studio-gray-87 studio-white-57 --out /tmp/ruler.jpg   # then LOOK at it
```

Read where the waistband top sits and use that **+ 0.03** as `waist` (gray-87 0.675 → 0.705, white-57 0.655 → 0.685).
Add a job to `social media graphics/youtube/thumbnails/_ad-setup-2026-09-11/build.py` (`ad`, `folder`, `lines`,
`photo`, `waist`), run it, look at `REVIEW_ad3_ad4.jpg`. It must print ALL PASS (25 px type clearance on the finished
file). It imports the Ad 5 clean builder — never copy that code.

- Copy: a command or topic, never a result or a number (`STOP PAYING / PERSONAL / TRAINERS`). Same wording family
  as the ad title.
- Photo: a hands-on-hips studio frame not already used on another ad (used: blue-89, blue-173 Ad 2; blue-247,
  white-23 Ad 5; gray-87 Ad 3; white-57 Ad 4). A 9:16 video gets a 9:16 thumbnail (/youtube-packaging rules).

## 5. Upload + thumbnail + read back

```bash
node scripts/youtube/upload.js --file "<master>" --title "<title>" --description-file "<folder>/youtube-description.md" \
  --privacy unlisted --category 26 --made-for-kids false --synthetic true --tags "<tags>" > "<folder>/youtube-upload.log" 2>&1
node scripts/youtube/set-thumbnail.js --video <id> --file "<thumb FINAL.jpg>" --out "<build dir>/readback-<id>.jpg"
```

- Check the log's first line says `channel: Abs by AI (UC236gjadarHAhEhOMYNGJ9g)` — the brand-account trap.
- Two uploads in parallel ran at ~2.8 MB/s each (340 MB ≈ 2 min). A re-run makes a SECOND video; only re-run a
  failed one.
- Read back with `videos?part=status,processingDetails` until `processingStatus: succeeded`, `embeddable: true`,
  privacy `unlisted`. Google Ads accepts the id before processing finishes, but check before you report.
- `--synthetic true` is required: the ads show AI goal images of Dan.

## 6. Google Ads — the Demand Gen conversion campaign

Write `scripts/ads/api/dgen-ads/adN.json` (copy `ad3.json`), then:

```bash
node scripts/ads/api/dgen-add-ad.js scripts/ads/api/dgen-ads/adN.json            # plan + Google validateOnly dry run
node scripts/ads/api/dgen-add-ad.js scripts/ads/api/dgen-ads/adN.json --apply    # build + read back → adN.result.json
node scripts/ads/api/client.js policy 24243839443                                # verdicts (re-run next day)
```

What it builds (the shape Ads 1, 2, 5 have): a YouTube video asset, one `Audience` (male + unknown, 25–54 + unknown,
the custom segments), ad groups `<label> | /start` and `<label> | home` (ENABLED, **$30 target CPA on the ad group**
— Dan set every group to $30 on 09-11, US + CA, English, the audience), and one ad per video per group named
`<label> | <version> | <landing>`, final URL `…?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-conv-adN&utm_content=<version>-<start|home>`,
logo `400941168572`, CTA `401407635767`, business name *Abs by AI*. Anything that exists by name is reused, so a
second run is a no-op and a vertical is one more `videos` entry.

**Copy (5 headlines ≤ 40, 3 long headlines ≤ 90, 3 descriptions ≤ 90).** The builder refuses any line that fails
`scripts/ads/ytads/lint.js`, except the lines Dan wrote himself (`DAN_APPROVED` in the builder). Recipe:
- 2 of Dan's shapes: **How I Got Abs At 40**, **How AI Got Me Abs** (approved on every ad that carries them).
- 1–2 of his topic lines if one exists for the subject (headline-style.md: *Fire Your Personal Trainer*, *How AI
  Fixed My Supplements*, *Audit Supplements With AI*, *The Truth About Supplements*).
- The rest plain: what the video shows. Long headlines: *Here's why I…* / *Daniel Rose explains…*. Descriptions:
  *Daniel Rose shows…* / *AI … explained by a guy who did it at 40 years old.*
- **Never "Why My X Kept Failing"** — Google DISAPPROVED it as CLICKBAIT on Ad 5 (09-11). No questions, no reveal,
  no withheld payoff, no "trick", no drug/medication/dose words (lint `medical` catches "dose").

Budget stays at $20/day — adding ad groups does not change it; say in the report that the budget is now shared by
more ad groups. Never enable a campaign.

**Policy, next day:** `client.js policy`. A DISAPPROVED line → rewrite ONLY that line (Dan's rule) with
`scripts/ads/ytads/manual.js`. An ad-level `YOUTUBE_AD_REQUIREMENTS_EXAGERRATED_OR_INACCURATE_CLAIMS` with no line
flagged = the video/thumbnail → the retry rule (memory `ad-retry-rule-and-no-trick`): tamer copy → tamer thumbnail →
remove.

## 7. Record it — same session

- `Docs/AD_VIDEO_IDS.md`: a row per video (ad, version, aspect, length, link, approved, thumbnail).
- `Docs/DGEN_CONVERSION_CAMPAIGN.md`: a dated section — ad group ids, ad ids, asset, audience, copy.
- `state.json` filed row (step 1). Coordination board: update your own entry only.
- Commit the scripts/configs/docs (videos and thumbnails are git-ignored), push to `main`.
- Dashboard: the row *"Add the new finished ads to the Google Ads campaigns…"* lists several ads — check it off only
  when every ad it names is in; otherwise say which part remains.

## Report to Dan (plain language)

Video links, what the description and thumbnail say (send the review sheet with SendUserFile), the ad groups and
what landing pages they point to, that Google is reviewing them, the budget note, anything flagged (policy, other
ads' problems seen in the policy report), and that organic posting was not done unless asked.

## Lessons

- **2026-09-11 (first run, Ads 3 + 4):** Drive direct download worked for Muhammad's HD links (shared "anyone with
  the link") — no Chrome. Local Whisper was skipped: load average 33 with another session rendering Ad 3's vertical;
  Replicate took 5 s per ad. The policy report run at the start showed Ad 5's *Why My Diets Kept Failing* headline
  DISAPPROVED (CLICKBAIT) and its video limited for exaggerated claims — read other ads' verdicts before writing new
  copy; they are the fastest signal of what Google is refusing this week.
