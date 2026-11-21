# Trial Campaign AD Thumbnails R2

Written 2026-10-01 from Dan's review of round 1. Recommended model: **GPT-6 Astra, High**.
Name the new session **Trial Campaign AD Thumbnails R2**.
**Use the Codex subscription to generate the images.**

## Goal and stopping point

Revise the thumbnails for the six ads in Google Ads campaign `24316364155` using Dan's decisions below. Produce one review page with a recommended pick per ad, then **stop for Dan's picks before final exports or installation**. Nothing is authorized for installation on YouTube or Google Ads. Keep all ad videos Unlisted. Do not publish organically.

The objective remains the highest click-through rate without deceiving viewers. These are creative candidates, not measured CTR winners. This is a targeted revision round, not another batch of five new concepts per ad. The specific directions below override the original five-choice mix.

## Start here

Read project `AGENTS.md`, `AI_COORDINATION.md`, `.claude/skills/_shared/VIDEO-RULES.md` in full, `.claude/skills/_shared/IMAGE-GENERATION.md`, and the imagegen skill. Read the original brief `Handoffs/handoff-20261001-trial-campaign-ad-thumbnails-codex.md` for ad context, plus `Docs/TRIAL_THUMBNAIL_REVIEW_20261001.md` for the first-round receipt. This document supersedes their pending-picks instructions for round 2.

All paths below are relative to the project root `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.

Use these base paths:

- **P:** `social media graphics/youtube/thumbnails/_trial-campaign-20261001/`
- **Photos:** `photos/finalized social media photos/`
- Full photo: `Photos/<photo-id>_FINAL_PRIMARY.jpg`
- Existing studio cutout: `Photos/_cutouts/<photo-id>_CUTOUT.png`
- First-round layout: `P/options/<ad-id>-<letter>-<aspect>.jpg`
- Generated background: `P/generated/<ad-id>-B.png` or `-C.png`

The first-round review is at `http://127.0.0.1:8811/`. If the server has stopped, run:

```bash
python3 -m http.server 8811 --bind 127.0.0.1 --directory "social media graphics/youtube/thumbnails/_trial-campaign-20261001"
```

Inspect `P/manifest.json` for exact photo, text, crop and layout records. `P/build.py` and the tracked copy `scripts/covers/trial-campaign-20261001/build.py` reproduce round 1. Inspect the actual selected JPGs before changing them. Do not run the original builder unchanged, as it would overwrite round 1.

Preserve round 1. Put new code, prompts, generated assets, manifest and review exports in `P/round2/`. Save the reusable round-2 recipe under `scripts/covers/trial-campaign-20261001/round2/`. The copied `generation-reference.py` in the tracked scripts directory is only a reference and has a different working-directory assumption; do not run it blindly.

Round-1 backup, public with the link:
https://drive.google.com/drive/folders/1kaaQ7aqUc3TT7-40p_KesEf0n_EAj5gb

## Exact revisions

### Ad 13: The Cost Of Getting Abs

Dan likes **B's studio design**, but wants **A's pool photo with its background removed** as the person in every variation.

- Person: `photo-10`, taken from the original full photo, not cropped out of the thumbnail.
- Existing removal mask: `P/masks/photo-10_FINAL_PRIMARY.mask.png`. Check the edges before reusing it.
- Design reference: `P/options/ad13-B-16x9.jpg`, background `P/generated/ad13-B.png`.
- Keep B's exact text: **HUMAN TRAINERS / HATE THIS AI**.
- Preserve the bold type, white cutout outline, dark background and yellow accent family. Keep the full head and visible abs; crop the pool swimsuit at the waistband according to the standing rule.

Make three review choices:

1. **13-R2A:** B's existing expense-prop design with the new pool cutout. This is the direct requested photo swap.
2. **13-R2B:** Same person, type and style, with a personal-training robot visibly taking over the human trainer's role. Make the robot and training context understandable at phone size. Generate only the scene/props, then composite the real Dan cutout.
3. **13-R2C:** Same person, type and style with one different background concept of your choosing that fits the cost-saving AI coaching message. Choose a clearly different visual from the robot and existing expense props. Do not change the headline.

The third baseline is included so Dan can compare the requested photo swap with his two requested alternate design directions. Do not add more concepts.

### RA-01: AI Got Me Abs

Dan likes **C's design**, but wants **E's photo**.

- **RA-R2A:** Use `studio-blue-53`, the E photo, in C's existing design.
- Reference: `P/options/ra01-C-16x9.jpg`; background `P/generated/ra01-C.png`.
- Keep C's exact text: **HOW AI / GOT ME ABS**.
- Keep the purple scene and C's styling. Replace the person only, adjusting placement as needed for the different pose.

### Ad 10: Busy Dad Fitness

Dan wants **D's photo with B's design**.

- **10-R2A:** Person `studio-white-25`, the D photo, shirtless in jeans and glasses.
- Reference: `P/options/ad10-B-16x9.jpg`; background `P/generated/ad10-B.png`.
- Keep B's exact text: **HOW BUSY DADS / GET ABS**.
- Keep B's orange home-office and fitness design. Change the person only.

### Ad 4: Stop Wasting Money On Supplements

Dan likes **B**. Retain it unchanged as **4-B-original** and show one additional photo variation beside it.

- **4-R2A:** Same design, background, type and text as B, but a different real photo with a smug, arrogant or mischievous expression. Dan described an "evil or arrogant look" that would make supplement corporations hate him.
- Reference: `P/options/ad4-B-16x9.jpg`; background `P/generated/ad4-B.png`.
- Exact text: **SUPPLEMENT / CORPS / HATE HIM**.
- Original B person is `studio-white-59`; choose another photo from the real library. Inspect candidate photos before choosing. Look for a confident smirk or provocative expression with clear abs.
- Dan's explicit expression request overrides the default no-frowning preference for this one option. It does not authorize AI redrawing his face. Do not generate an evil face or alter his physique.

### Ad 3: Stop Paying Human Trainers

Dan rejected the five current visuals. Keep **Ad 3 B's copy**, but use **RA-01 B's image and design**, including its phone cue.

- **3-R2A:** Reuse `P/generated/ra01-B.png` and RA-01 B's person `studio-blue-173`.
- Visual reference: `P/options/ra01-B-16x9.jpg`, the cyan phone-and-dumbbell design.
- Replace RA-01's headline with Ad 3 B's exact copy: **TRAINERS / HATE THIS / AI APP**.
- Preserve that design; ensure the phone remains obvious at small size after laying out the longer headline. Do not substitute RA-01 C or its new E photo. Dan specifically named RA-01 B for this ad.
- The direct reuse is Dan's request and overrides the usual preference for different hero photos across ads.

### Ad 6: You're Not Too Old

Dan likes **B's design and text** and wants two photo variations. Keep original B available as a comparison, labelled **6-B-original**.

- Reference: `P/options/ad6-B-16x9.jpg`; background `P/generated/ad6-B.png`.
- Exact text for both: **HOW MEN 40+ / GET ABS**.
- **6-R2A, jeans and glasses:** A real shirtless photo of Dan in jeans wearing glasses. Verified available candidates are `studio-blue-171` and `studio-white-25`, including their cutouts. Inspect both. Prefer a suitable different photo from Ad 10's `studio-white-25` if `studio-blue-171` meets the request.
- **6-R2B, older appearance:** AI-age the person from **current Ad 6 B**, `studio-blue-221`, with salt-and-pepper gray hair and visibly older skin. Keep the same identity, expression, pose, body size, physique and clothing. Keep B's background and type unchanged.

Interpretation of Dan's final clarification: the age edit uses the current B person, not automatically the new jeans-and-glasses photo. His last wording was "one of the jeans-with-glasses image" and "one of the current image where I'm looking older".

The explicit AI-aging request is a narrow exception to the standing rule that real Dan photos are never redrawn. It applies only to `6-R2B`. Use Codex on the subscription for the edit. Inspect the input first; constrain the edit to hair and age-related skin changes, and composite the edited areas onto the original where practical so the physique and pose stay intact. Check for unintended changes to face identity, body definition and fingers. Label the review card **AI age edit** so its provenance is clear. Do not add that label as thumbnail headline copy.

## Production and review

Expected work: **9 new visual choices**, plus the two unchanged B comparisons for Ads 4 and 6. This means 11 selectable review cards, not 30 fresh options. Preserve the chosen round-1 references separately wherever useful for comparison.

Plan for **3 Codex generations**: the two new Ad 13 backgrounds and the one Ad 6 age edit. Everything else reuses existing plates and real source photos. State the count before starting; generate no spares. Use `.claude/skills/_shared/codex-image.sh` per the image-generation rules. Do not switch to a paid image API. If a quality repair is necessary, explain it and keep a record of the additional generation.

Composite real cutouts and set all headline type in code. Local background removal is permitted. Keep the established designs, exact text and colours unless Dan explicitly requested a design variation. No em or en dashes in anything written.

Required round-2 layouts:

| Ad | Required aspects |
|---|---|
| Ad 13 | 16:9 |
| RA-01 | 16:9 and 9:16 |
| Ad 10 | 16:9 and 9:16 |
| Ad 4 | 16:9 |
| Ad 3 | 16:9, 9:16 and 1:1 |
| Ad 6 | 16:9 |

That is **13 new review JPGs**, plus the two unchanged horizontal B comparisons. Use 1280x720, 1080x1920 and 1080x1080 respectively, each under 2 MB. Recheck `Docs/AD_VIDEO_IDS.md` for any newly completed formats before delivery; keep the source composition adaptable without taking over another video-editing task.

Build **one review page** at `P/round2/index.html`, reachable as `http://127.0.0.1:8811/round2/` if the existing server is still running. Include:

- A concise "What I decided" section with the six changes above and a recommended choice per ad.
- Clear round-2 IDs, aspect switching, enlarged view, and a phone-size view around 320 pixels wide.
- Source-photo and original-option labels so Dan can verify every swap.
- The two original B comparisons, and the AI age-edit label on the relevant card.
- Pick controls and a copyable reply. Use a new localStorage key so first-round picks cannot appear as second-round choices.

Inspect every layout at full and phone size: all words readable, full hair and head visible, abs uncovered, clean cutout edges, no stretching, and phone/robot cues legible. Verify image URLs and pick controls. Save a manifest of source photos, backgrounds, headline text, aspect layouts and generation prompts. Preserve an offline review copy and back up the new assets to the existing Drive folder with anyone-with-link viewing, following the standing sharing rule.

Save durable code and a receipt, commit only this task's changes using `scripts/git/safe-push.sh`, and verify the resulting deployment status according to project rules. Re-read the coordination board before updating only this task's entry; run `scripts/board-check.sh`. Never include another session's files.

## Campaign identity for later use, not installation authorization

| Ad | YouTube IDs at round 1 |
|---|---|
| Ad 13 | `-SuKGXGcbIg` |
| RA-01 | `OUw788sF1KY`, `rfCsWNxuNV0` |
| Ad 10 | `Sg3vcEY2P_8`, `4nDWFmdjzQQ`, `CR4WAVmSuXY` |
| Ad 4 | `R08TPEtkjuQ` |
| Ad 3 | `86jbUhqBTUQ`, `xlC-tigurnA`, `-wTErCSi640`, `DXRkrfvcJEM` |
| Ad 6 | `Je2yvk00SHE` |

No final `picks.json` exists yet. Do not treat the selected design directions as approval of unseen revisions. Deliver the review page and stop. Only after Dan's later final picks should the selected files be exported and `picks.json` prepared. The existing separate installation handoff is `Handoffs/handoff-20261001-trial-campaign-ad-thumbnails-install-claude.md`; it remains blocked until final picks and exports exist.

## Ready-to-paste starter prompt

Read `Handoffs/handoff-20261001-trial-campaign-ad-thumbnails-round2.md` and execute it. Name this session "Trial Campaign AD Thumbnails R2". Use the Codex subscription to generate the images. Apply my six sets of revisions using the exact photos, designs and text in the handoff. Show all revised choices on one review page with your recommended pick per ad, then stop for my picks before final exports or installing anything.
