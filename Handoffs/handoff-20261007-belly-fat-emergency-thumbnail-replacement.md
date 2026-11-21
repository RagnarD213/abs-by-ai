CONTENT | Belly Fat Emergency LFC Thumbnail

# Belly Fat Emergency thumbnail replacement

Written 2026-10-07. This handoff changes the thumbnail for the existing organic long-form video, **Your Belly Fat Is an Emergency: 7 Reasons to Take It Seriously**. Do not edit, re-render or re-upload the video. Public YouTube video: `v2R4QpnURqA`, https://www.youtube.com/watch?v=v2R4QpnURqA. Google Ads also uses this same YouTube video.

**Sidebar name:** `Belly Fat Emergency LFC Thumbnail`.

**Recommended model:** Claude Opus 5.5, high effort for visual direction and review. Use the Codex subscription to generate the images. Run `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high` for the three image edits. No paid image API or other image model.

## Dan's direction

Make **exactly three separate thumbnail choices**. Each shows a recognizable AI-modified image of Dan with **substantial, believable belly fat**. The large word **EMERGENCY** sits in the foreground, across the center of the 16:9 thumbnail and over his body. The text must remain readable at small YouTube sizes. The three images need materially different compositions or visual treatments, not three color swaps. These three choices replace the usual five-choice thumbnail mix for this request.

Dan specifically requests AI modification of his own body. That instruction controls this handoff's image treatment. Preserve his real face, hair, age and recognizable identity as closely as possible while changing the torso. Use source photos of Dan, not a generic AI man. Do not add other words, a website address or a second person. Keep the face and the changed body clearly visible around the headline. Set the final `EMERGENCY` type in code after image generation so its spelling, position and contrast are exact.

Suggested distinct concepts:

1. **Direct portrait:** Dan faces camera with the modified belly visible, against a simple dark red background. `EMERGENCY` crosses his lower chest and upper belly in bold white type.
2. **Pool setting:** Use a suitable real pool-shoot photo of Dan as the source. Keep the outdoor setting recognizable; give his torso substantial belly fat and place red `EMERGENCY` type with a strong light outline across the center of his body.
3. **Studio alert:** Use a different studio photo or pose. Dramatic side lighting and a high-contrast charcoal background, with bright yellow or white `EMERGENCY` centered over his body.

These are starting directions. Change a composition if a source photo makes the body edit or Dan's identity unconvincing. Avoid a belly-only crop: Dan's face and the larger body shape should remain visible. No hands pinching the belly.

## Inputs and baseline

- Current thumbnail, chosen by Dan previously: `social media graphics/youtube/thumbnails/Belly Fat Emergency/belly-fat-emergency_2-pool-photo-172-FINAL.jpg`. Preserve it unchanged as the baseline and rollback asset.
- Find original Dan photos in `photos/finalized social media photos/` and relevant pool-shoot sources. Inspect full-resolution originals before choosing three different poses.
- `Docs/C1652_SETUP_RECEIPT_20260918.md` records the prior thumbnail choice and source.
- YouTube Studio reach data checked 2026-10-07: about **4,200 organic thumbnail impressions**, **1.6% thumbnail click-through rate** and **283 views** since the Oct 4 release. Record exact dates and values again when beginning the test. Traffic source mix matters when comparing CTR later.
- The video and an ad using it are approved in Google Ads, yet the paid ads have zero impressions. A better thumbnail is a packaging test, not a proven fix for paid delivery. Do not change Google Ads bids or budgets in this thumbnail task.

## Build, review and install

1. Read `.claude/skills/_shared/VIDEO-RULES.md` and `.claude/skills/_shared/IMAGE-GENERATION.md`. Confirm the live YouTube video ID and current thumbnail before generating. State the batch size: three images.
2. Generate three distinct edits through the Codex subscription. Use real Dan photos as references. Check that Dan's face is recognizable, the modified belly is substantial and believable, and there are no anatomy errors. Composite the exact word `EMERGENCY` locally in the foreground. Export each as a sharp 1280x720 JPEG or PNG within YouTube's current thumbnail size limits.
3. Put the three final images side by side on one review sheet, at full size and at phone-feed size. Include the source photo and final image for each. Show Dan all three and **stop for his pick**. Do not infer the choice from his prior selection of the current thumbnail.
4. After Dan chooses, replace the thumbnail on `v2R4QpnURqA` in YouTube Studio, then read it back on the live watch page and Studio. Record the installed file, timestamp, hash and a screenshot in a short receipt. Keep the original B thumbnail for rollback.
5. Compare CTR after a meaningful number of new impressions, using a similar traffic-source mix and a clearly stated date range. Report the result as a packaging test. If Google Ads remains at zero impressions, continue its separate delivery investigation rather than claiming the thumbnail change fixed it.

No upload of a new YouTube video, no organic repost, and no ad URL change are part of this handoff.

## Ready-to-paste starter prompt

Name this task `Belly Fat Emergency LFC Thumbnail`. This is CONTENT. Read `Handoffs/handoff-20261007-belly-fat-emergency-thumbnail-replacement.md` and the shared video and image rules. Use the Codex subscription to generate the images. Make exactly three distinct AI-modified thumbnail choices of me with substantial believable belly fat, using my real photos as references. Put the single large word `EMERGENCY` across the center in the foreground over my body. Show all three together at full and phone-feed size, then stop for my pick. After I choose, replace the thumbnail on YouTube video `v2R4QpnURqA`, verify it live, preserve the old thumbnail, and track the new click-through rate. Do not edit or re-upload the video or change Google Ads budgets or bids.
