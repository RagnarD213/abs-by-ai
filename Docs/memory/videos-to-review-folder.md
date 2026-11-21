---
name: videos-to-review-folder
description: Every review video of 45 s or longer is also copied to the project folder "Videos to Review" for VLC; delete the copies when Dan finalizes the video (Dan, 2026-10-08)
metadata:
  type: feedback
---

Every video sent to Dan for review that runs 45 seconds or longer (finished first minute, finished film, short, ad, long graphics-in-motion clip) is copied as the full-quality file to `Videos to Review/` in the Abs By AI project folder, in addition to building the review page. Name it `<task name> - <what it is>.mp4`, open the folder in Finder, and list the file names in chat. When Dan finalizes the video, delete that video's copies from the folder in the same session.

**Why:** Dan, 2026-10-08 (SL-03 round 3): the review page only plays at 2x and its timeline misbehaves when clicked; he watches in VLC at higher speed. He first said Downloads, then changed it the same day to this folder, with deletion at finalize "to stop wasting hard drive space", "for this and every video going forward".

**How to apply:** all video skills, Claude and Codex. Replace the copy after each re-render he will review. The folder is git-ignored. Check the page server answers (200, and 206 on a video range) before sending the link; servers from earlier sessions die on restart. Full rule: `.claude/skills/_shared/VIDEO-RULES.md`, first section. Related: [[review-page-what-i-decided]].
