# Install approved B3 thumbnail on the jelly-bean Short

Status: ready. Dan approved the finished B3 design on September 20, 2026 and requested installation in a new task.

Recommended model: GPT-5.6 Sol, Medium effort.

## Goal and scope

Replace the thumbnail on the existing YouTube Short at https://www.youtube.com/shorts/JuLnoU9NV28 with the exact approved B3 artwork. Preserve the video, URL, title, description, visibility, analytics, comments and any other settings. Do not redesign the cover, regenerate Dan or change other posts. This handoff does not request Instagram, TikTok or a new video upload.

Dan first preferred thumbnail B's topic background and outlined real studio photo, then requested A's copy. His final revision moved the badge and headline up, removed the `450 CALORIES EACH` pill and its blue outline, and pulled the soda and jelly-bean background upward. He replied, "That looks good. Create a handoff to install this in a new task." The design is approved, so do not ask for another design decision. The standing thumbnail-replacement authorization in `.claude/skills/_shared/VIDEO-RULES.md` applies.

## Exact target and artwork

- Short ID: `JuLnoU9NV28`.
- Studio editor: https://studio.youtube.com/video/JuLnoU9NV28/edit
- Approved master PNG, 1080 x 1920: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/covers/review/jelly-bean-refresh/B3-jelly-beans-beat-soda-tight.png`.
- Master SHA-256: `b4e77ece11d6d6bbf626b61231a465d0681ec470ad5f1d253a789967358c301a`.
- Ready-to-upload JPEG, 1080 x 1920, 566 KB: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/covers/review/jelly-bean-refresh/B3-approved-upload.jpg`.
- Upload JPEG SHA-256: `7133bf0787fc400d26c14a9cee2a0b606013c0f76bfba9c5ded49b67733747a0`.
- Editable builder and history: `Short-form video content/covers/review/jelly-bean-refresh/build.py` and `NOTES.md`. B2 and the original four options are retained for reference, not for upload.

The artwork uses the generated food-and-drink environment as background, plus the original approved `studio-gray-41_CUTOUT.png` photo of Dan. Text clears his face and hair. The master was checked at full resolution and 270 x 480 phone size. No further creative work is needed. These photo files are ignored by Git, so a new worktree must access the absolute paths above in the saved project checkout. Do not assume the artwork is present in the new worktree.

## Installation and proof

1. Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` and `.claude/skills/coverimage/SKILL.md`. Check `AI_COORDINATION.md` for ownership. Confirm the JPEG exists at its absolute path and matches its hash and dimensions. If it is absent, rebuild only from the exact master PNG and compare visually. Do not substitute B2 or a different option.
2. Open the exact Studio editor in Dan's signed-in Chrome session. Confirm the video ID before touching any setting. Note the current thumbnail and save a recoverable copy using **Thumbnail > Options > Download** if available. Capture available A/B test results before replacing or ending a test. Do not delete the video or change its visibility.
3. Use **Thumbnail > Options > Change** (or the live file upload control) and select the ready JPEG. Confirm the preview shows the red `A REAL STUDY` badge near the top, white `JELLY BEANS`, yellow `BEAT SODA?`, Dan's white-outlined studio cutout, soda at left and jelly beans at right, with no calorie pill.
4. Save and wait until Studio's Save button becomes disabled before navigating away. Do not force a navigation through a pending-save warning. Reload the editor and verify the new preview persists, then check the Studio Shorts list. A public thumbnail URL may remain cached after a successful save; distinguish that from an actual failed installation. Preserve the existing visibility even if the Short is already public, since this is not an upload.
5. Record an installation report beside the approved artwork with the prior thumbnail backup path, any test results, installed JPEG hash, video ID, time, Studio verification, and any public propagation delay. Report the live link to Dan. Mark this handoff executed in `Handoffs/README.md` and clear its coordination entry after verified delivery. Do not add a Victory Dashboard row because Dan did not request one.

If the signed-in Studio controls or local artwork are unavailable, investigate the concrete issue. Do not delete or re-upload the Short, alter its visibility, or claim completion without a persisted Studio preview.

## Ready-to-paste starter prompt

Read `Handoffs/handoff-20260920-install-approved-jelly-bean-thumbnail.md` and install the exact approved B3 thumbnail on YouTube Short `JuLnoU9NV28`. The JPEG and its SHA-256 are in the handoff. Preserve the existing video and settings, back up the old thumbnail and available test results, then replace and verify the cover in Studio. Do not redesign or re-upload the Short. Finish with an installation report and live link.
