> **EXECUTED 2026-10-25:** Exact Codex R5 and approved cover design 1 R3 installed, media uploaded and verified, one shared-waitlist entry for Thu Dec 31 at 9 AM America/Chicago. Blotato 197/200, no DS-40 schedules yet. Do not rerun this handoff. Existing daily top-up owns queuing. Receipt: `Docs/DS40_CODEX_R5_SETUP_RECEIPT_20261025.md`.

> **SUPERSEDED SOURCE SELECTION, Dan 2026-10-25:** Dan explicitly selected **Codex R5**, shown in his screenshot as approved, 1:04.86. Set up only `/Volumes/Extreme/_edit_work/DS-40-codex/round5/review/media/bill-maher-fat-90-year-old-r5.mp4`, SHA-256 `3808e604f218ad7281865ea74b3cbcf1a740a1bc595d060f1bcb34b8a3f4f720`. Codex R5 approval is recorded in its `dan-approval-20261023.json`. All Claude R6 source directions below are historical and must not be used. Current setup state: `Short-form video content/Fat 90 Year Old - DS-40/Codex R5 setup/SETUP-STATE.json`.

# Fat 90 Year Old SFC Setup (DS-40): "Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right."

**CONTENT (SFC), a dedicated green screen reaction Short edited by Claude (rounds 1 to 6). No ads, no Google Ads work, no unlisted upload.**
**Fire now: Dan approved the round 6 film on 2026-10-23.** Recommended: Claude Opus 5.5, high.
**Use the Codex subscription to generate the images.**

## What Dan decided
- 2026-10-23, on the R6 page (http://127.0.0.1:8940/, now removed): "approved, handoff for setup". The film is final; do not re-edit.
- Final file: `Short-form video content/Fat 90 Year Old - DS-40/Fat 90 Year Old SFC R6 - complete Short.mp4`
  (1080x1920, 29.97, 1:00.3, -14 LUFS, SHA-256 starts `1cc5a8ce8b9e437b`; the approved draft plus the
  independent reviewer's three fixes: watch face solid, captions on the spoken word, BMI cell 35.2. `ROUND-6-REVIEW.md`: SHIP). Beside it: the burned captions as
  `Fat 90 Year Old SFC R6.srt`, the 540p review copy, audio A/B, gate stamps, `ROUND-6-REVIEW.md`, notes and recipe.
- Contents, for the title and description: Bill Maher (Real Time, HBO, "New Rule: Fat Acceptance", YouTube `yfiWjnStE3w`,
  2:14 to 2:34) asks "Have you ever seen a fat 90-year-old?" and calls healthy at any weight "an unchallenged lie". Dan: he
  is right, there is no healthy at any size, treat belly fat as an emergency, here is a BMI table (overweight: health
  improves a lot at a healthy weight; obese: losing fat is the most important thing you can do), subscribe.
- No realistic AI footage in it: the YouTube altered/synthetic flag and TikTok `ai_generated` are **false**.
- No AbsByAI.com end mark (standing rule).

## Steps
1. Run `/video-setup` for it as a dedicated Short: file it (project folder already done; Extreme and Drive copies, Drive
   "anyone with the link"), Edit Queue entry.
2. Five covers made by Codex on the subscription (`_shared/codex-image.sh --model gpt-6.1-sol --effort high`): one pool
   photo, one studio photo, one AI-enhanced or AI-generated image of Dan, two of Codex's choice; five unique designs, each
   in its Instagram and YouTube layout. A frame of the green screen layout (Maher card over Dan) is a natural candidate for
   one of Codex's two. Stop for Dan's pick.
3. After the pick: title, description (credit the clip: Real Time with Bill Maher, HBO), tags, the pinned question comment
   (`"pinned_comment"` in the Blotato config; for example: what BMI category are you in right now?), and the Blotato queue
   on the next free **Thursday** dedicated-Short slot at 9 AM CT (`Docs/SHORTS_RELEASE_CALENDAR.md`), or the waiting list
   (`scripts/blotato/video_waitlist.json`) if Blotato is full. Re-read every saved schedule.
4. Edit queue: DS-40 `uploaded` only after the queue read-back. Write the setup receipt in `Docs/`.

## Note
Codex ran a separate competing DS-40 build (`/Volumes/Extreme/_edit_work/DS-40-codex/`, its own "complete Short" in
Videos to Review). Dan approved Claude's R6, so set up only the file above.

## Starter prompt
> Fat 90 Year Old SFC Setup. Read `Handoffs/handoff-20261023-ds40-fat-90-year-old-sfc-setup.md` and execute it: file the approved R6 Short, make five Codex covers (use the Codex subscription to generate the images), stop for my pick, then queue it in Blotato on the next Thursday dedicated-Short slot.
