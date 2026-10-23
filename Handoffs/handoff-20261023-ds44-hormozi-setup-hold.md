# Hormozi Fat Guy SFC Setup (DS-44): covers now, upload and queue ON HOLD until Dan picks the version

**CONTENT (SFC), a dedicated green-screen reaction Short. No ads, no Google Ads, no unlisted upload.**
**Fire now for the covers. Recommended: Claude Opus 5.5, high.**
**Use the Codex subscription to generate the images.**

## What Dan decided (2026-10-23)
- He approved the scripted version, "Alex Hormozi Asks A Fat Guy Why He Isn't 200 Pounds Heavier. He's Right." (DS-44 R2).
- He also wants the off-the-cuff take edited to compare (`handoff-20261023-ds44-hormozi-off-the-cuff-take.md`, DS-44B).
- Dan: *"For the setup handoff, we'll pick the thumbnail that we'll use regardless of the version. Have it hold off on
  installation or adding to the queue until we edit the off-the-cuff take and choose which one we're going to use."*

## Files
- Scripted, approved: `Short-form video content/Hormozi Fat Guy - DS-44/Hormozi Fat Guy SFC R2 - complete Short.mp4`
  (1080x1920, 29.97, 61.228 s, -14.8 LUFS, SHA-256 starts `9d8deb8da3d5eb2b`); captions burned in, SRT beside it.
- Off-the-cuff: will be filed in the same folder by the DS-44B edit, once delivered.
- Contents for the title/description: The Iced Coffee Hour, a caller tells Alex Hormozi he can't stop eating; Hormozi asks
  "Why aren't you 200 pounds heavier?" (YouTube `37mqHjJOS50`, about 2:50 to 3:11). Dan: he's right, you already stop
  somewhere, your stopping point is set too high; set it with the scale (weigh every morning, 2 pounds over, cut back that
  day); Zepbound can make stopping easier; subscribe.
- AI content: the scripted cut contains library AI clip A0197 (man on a bathroom scale, labelled AI-GENERATED on screen), so
  if the scripted version ships the YouTube altered/synthetic flag and TikTok `ai_generated` are **true**; for the off-the-cuff
  version, decide from that cut (true only if it keeps A0197 or any other realistic AI footage).

## Steps
1. Run `/video-setup` for it as a dedicated Short, up to the pick: Edit Queue entry check, five covers made by Codex on the
   subscription (`_shared/codex-image.sh --model gpt-6.1-sol --effort high`): one pool photo, one studio photo, one
   AI-enhanced or AI-generated image of Dan, two of Codex's choice; five unique designs, each in its Instagram and YouTube
   layout. A frame of the reaction layout (Hormozi full screen, Dan small in the corner) is a natural candidate for one of
   Codex's two. The cover is version-independent (Dan's words). **Stop for Dan's pick.**
2. After the pick, prepare but do not apply: export the chosen cover in both layouts, draft the title, description (credit:
   The Iced Coffee Hour), tags and the pinned question comment, and a Blotato config marked HOLD. **Do not upload, do not
   install a cover, do not add anything to Blotato or the waiting list** until Dan picks scripted or off-the-cuff.
3. Once he picks: file and back up that version (Extreme, Drive "anyone with the link"), finish the config for it (AI flag per
   the version), and queue it on the next free **Thursday** dedicated-Short slot at 9 AM CT (`Docs/SHORTS_RELEASE_CALENDAR.md`),
   or the waiting list (`scripts/blotato/video_waitlist.json`) if Blotato is full. Re-read every saved schedule. The other
   version stays filed, unqueued.
4. Edit queue: DS-44 `uploaded` only after the queue read-back. Setup receipt in `Docs/`. Remove the Videos to Review copies
   of both versions when one is queued.

## Starter prompt
> Hormozi Fat Guy SFC Setup. Read `Handoffs/handoff-20261023-ds44-hormozi-setup-hold.md` and execute it: make five Codex covers for my Hormozi reaction Short (use the Codex subscription to generate the images) and stop for my pick. After I pick, prepare everything but hold: no upload, no cover install, nothing in Blotato until I choose the scripted or the off-the-cuff version.
