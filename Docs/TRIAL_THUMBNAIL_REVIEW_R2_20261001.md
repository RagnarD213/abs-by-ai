# Trial Campaign AD Thumbnails R2, October 1, 2026

Status: reviewed by Dan on October 1, 2026. RA-R2A, 10-R2A, 4-R2A and 3-R2A approved. Ad 13's robot needs the gray background extended to the top. Ad 6 needs a subtle salt-and-pepper age variant of 6-R2A. No final exports, picks.json or installation.

Review: http://127.0.0.1:8811/round2/
Drive backup: https://drive.google.com/file/d/19eXv0-yNXxXdUH6LL15DoO4Eb9NI9a68/view
Shared folder: https://drive.google.com/drive/folders/1kaaQ7aqUc3TT7-40p_KesEf0n_EAj5gb

Nine new choices and two byte-identical original B comparisons for Ads 4 and 6. Thirteen new JPG review layouts plus two comparisons. Dimensions: horizontal 1280x720, vertical 1080x1920, square 1080x1080. Largest JPG: 491,980 bytes.

Recommended: Ad 13 13-R2B; RA-01 RA-R2A; Ad 10 10-R2A; Ad 4 4-R2A; Ad 3 3-R2A; Ad 6 6-R2A. Creative judgments, not measured CTR results.

Photos: Ad 13 photo-10 with original mask and waistband crop; RA-01 studio-blue-53; Ad 10 studio-white-25; Ad 4 studio-gray-55 for the real smirk; Ad 3 studio-blue-173; Ad 6 studio-blue-171 for jeans/glasses and studio-blue-221 for aging. Original B comparisons retain studio-white-59 and studio-blue-221 respectively.

Three generations through codex-image.sh on the Codex subscription, no paid image API calls or spares. Robot background 45,629 tokens, savings background 19,131, age edit 39,670. Total helper-reported tokens 104,430. Prompts and output records preserved. The age edit changes hair, face and neck only; original cutout pixels below 32% of source image height are exactly unchanged, preserving physique, fingers and clothing. Review card labels it AI age edit.

QA: source-photo contact sheets and pool-mask edges inspected. All full-size and phone-size layouts inspected. Robot moved 75 pixels below the headline; square phone scene recomposed to keep the phone visible. Exact headlines retained; zero text/person mask overlap; 21 image URLs returned HTTP 200. Browser pick-to-reply, aspect switching, enlarge and phone-size controls checked; test picks cleared. Docs/AD_VIDEO_IDS.md rechecked with no additional completed formats listed for Ads 13, 4 or 6.

Work directory: social media graphics/youtube/thumbnails/_trial-campaign-20261001/round2/
Durable recipe: scripts/covers/trial-campaign-20261001/round2/
Run build.py, then review.py, from the durable recipe folder using python3. The builder loads only round-1 rendering definitions using AST; it never runs the round-1 build or changes round-1 output files. Review-offline.html embeds the review JPGs and references for use without the local server.

Next: execute `Handoffs/handoff-20261001-trial-campaign-ad-thumbnails-round3.md`. Preserve the four approved choices and stop for Ad 13 confirmation and the Ad 6 choice. Final exports and installation remain pending.
