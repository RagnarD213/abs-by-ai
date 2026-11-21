# Install approved breakfast Short thumbnail

Status: ready. Dan approved the revised studio option on 2026-09-22 and asked for installation in a new task.

Recommended model: GPT-5.6 Sol, Medium effort.

## Goal

Replace the thumbnail on the existing YouTube Short **Why I Skip Breakfast Every Single Day** with the exact approved revised studio image. Preserve the video, URL, title, description, visibility, analytics, comments, and all other settings. This is a thumbnail change only. Do not re-upload the Short or change other platforms.

Dan first chose studio option B over the pool option, then asked to raise the breakfast scene so the eggs and food were more visible. The revised image was delivered beside the original B for comparison. Dan replied, "Let's go with B. Make a handoff document to install this in a new task." In context, **B means the revised B2 image below**, not the earlier `B-studio-design.jpg`. The design choice and installation are authorized. Do not ask for another design approval.

## Exact target and file

- Short ID: `UFga137pseM`. Confirmed as the first Short on `https://www.youtube.com/@danrosefit/shorts` on 2026-09-22. Its channel accessibility title was "Why I Skip Breakfast Every Single Day."
- Live Short: https://www.youtube.com/shorts/UFga137pseM
- Studio editor: https://studio.youtube.com/video/UFga137pseM/edit
- **Approved upload file:** `/Users/danielrose/Documents/Claude/Projects/Abs By AI/output/thumbnails/breakfast-short-20260922/B2-studio-breakfast-raised.jpg`
- Approved file SHA-256: `72d840d8b86d684f1354c5b56f483b3b1c37d8a0764285756e65d9b9b87e263e`
- Dimensions: 1080 x 1920 JPEG, about 626 KB.
- Review comparison: `output/thumbnails/breakfast-short-20260922/studio-revision-comparison.jpg`, original B at left and approved revision at right.
- Source and build notes: `output/thumbnails/breakfast-short-20260922/README.md` and `build.py`. The approved JPEG and builder were pushed to `main` in commit `bc9756d`.

The approved cover has `EVERY DAY` in a red badge, `WHY I SKIP` in white, `BREAKFAST` in yellow, and Dan's real studio cutout with a white outline. Eggs, toast, and coffee are visibly placed above and beside him. No text touches his face or hair. There is no small real-photo disclaimer or site URL, per the project's thumbnail rules.

## Install and verify

1. Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, and `.claude/skills/coverimage/SKILL.md`. Check `AI_COORDINATION.md` for ownership. Verify the approved JPEG exists, has the stated dimensions and SHA-256, and visually matches the right side of the comparison. If a worktree does not contain it, retrieve this exact tracked file from `main`. Do not use the older `B-studio-design.jpg` or the pool option.
2. Open the exact Studio editor in Dan's signed-in Chrome session and confirm video ID `UFga137pseM`. Note the current thumbnail. Save a recoverable copy via **Thumbnail > Options > Download** if available. Record any available A/B test results before replacing the old thumbnail or ending a test. The standing thumbnail replacement authorization in `VIDEO-RULES.md` applies.
3. Change the thumbnail to the approved JPEG. Confirm the preview shows the raised eggs, toast, and coffee along with the white-outlined studio portrait and exact headline. Save and wait for Studio's Save button to finish before navigating away. Never force navigation past a pending-save warning.
4. Reload the editor and verify the new thumbnail persists. Check the Studio Shorts list. A public thumbnail URL may be cached, so use Studio's persisted preview as the primary confirmation. Preserve the existing visibility, even if the Short is already public, because this is not a new upload.
5. Write a short installation report beside the approved JPEG with the old thumbnail backup path, available test results, installed file hash, video ID, completion time, and Studio verification. Mark this handoff executed in `Handoffs/README.md` and remove only its own coordination-board entry. Do not add a Victory Dashboard row unless Dan asks.

If Studio controls are unavailable, investigate the specific blocker. Do not delete or re-upload the video, alter its visibility, or claim installation without a saved Studio preview.

## Ready-to-paste starter prompt

Read `Handoffs/handoff-20260922-install-approved-breakfast-short-thumbnail.md` and install the exact approved revised studio thumbnail on YouTube Short `UFga137pseM`. Use `B2-studio-breakfast-raised.jpg` with the SHA-256 recorded in the handoff, not the earlier B image. Back up the current thumbnail and available A/B test results, preserve the existing video and settings, save in Studio, reload to verify, and write an installation report. Do not redesign or re-upload the Short.
