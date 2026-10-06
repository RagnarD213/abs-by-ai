# YouTube Short thumbnail repair and Blotato queue audit, 2026-10-06

CONTENT: SL-04 short 2, Do This 2 Minute Arm Pump Before You Take Your Shirt Off.

## Live repair

YouTube https://www.youtube.com/shorts/qDvrtKbuhf4 retained its public video and approximately 4,000 views. The approved cover was downloaded from the original setup config. The direct YouTube thumbnails.set request returned success but the downloaded API image remained byte-identical after 60 seconds, and the public Shorts tile still showed a frame. Desktop Studio > Thumbnail > Options > Change > approved JPEG > Save corrected the public portrait tile. Confirmed visually on @danrosefit/shorts. Screenshot: tmp/thumbnail-audit-20261006/channel-fixed.jpg.

## Queue audit

194 scheduled posts: 79 Facebook, 68 Instagram, 30 TikTok, 17 YouTube. Every YouTube post has thumbnailUrl. Every Instagram reel has coverImageUrl. Downloaded and decoded all 47 YouTube and Instagram cover files successfully. All 17 YouTube images are below 2 MB. All 17 match their local setup-config cover bytes. Nine upcoming YouTube Shorts have 1080x1920 covers; eight long-form posts have 1280x720 covers. The nine Shorts are the remaining four SL-04 clips and all five SL-05 clips. No queue changes were needed for missing, broken, oversized or mismatched covers. ad_guard scan clean for all 194 posts.

The queue alone cannot guarantee a correct public Shorts cover: today's failed release had the right URL and valid JPEG. Updated video-setup/SKILL.md to require the actual public portrait tile check after release and the verified Studio repair if necessary. A daily 9:15 AM Central check has been proposed to Dan, pending his schedule confirmation. Never delete/re-upload a posted video for this repair.

## Audit evidence

Local backups: tmp/thumbnail-audit-20261006/queue-before.json, covers.json, approved.jpg and readback.jpg. The readback.jpg is the unchanged API image from the unsuccessful API-only attempt, not proof of the final corrected public cover.

- 5090248: Calories: The Reason You're Not Losing Weight (8 Ways To Eat Less), 1280x720, 208794 bytes.
- 5019229: Make Your Waist Look Smaller With Side Lateral Raises, 1080x1920, 619967 bytes.
- 5019235: How To Do Bicep Curls: One Arm or Both Arms?, 1080x1920, 518871 bytes.
- 4976708: Why I Stopped Deadlifting at 40 (Do These 4 Exercises Instead), 1280x720, 184392 bytes.
- 5019241: Side Lateral Raise Mistake: Raise Your Elbows, Not Your Hands, 1080x1920, 512037 bytes.
- 5095442: My Honest Oura Ring Review After 1.5 Years (The Good, Bad & Ugly), 1280x720, 165416 bytes.
- 5019252: Stop Swinging Your Bicep Curls, 1080x1920, 531818 bytes.
- 5053510: Deadlifts Cause More Injuries Than Every Other Lift, 1080x1920, 1577724 bytes.
- 5014534: How I Make My Daily Salad: 700 Calories, $4 a Bowl, Fresh for 7 Days, 1280x720, 266126 bytes.
- 5053518: 2 Back Exercises To Do Instead Of Deadlifts, 1080x1920, 1624638 bytes.
- 5194487: Can You Drink Alcohol And Still Have Abs? (My 6 Rules), 1280x720, 337062 bytes.
- 5053524: Safer Lifts Build MORE Muscle Long Term, 1080x1920, 1613161 bytes.
- 5053530: Train Legs Without Deadlifts, 1080x1920, 1696663 bytes.
- 5046550: Top 5 Zepbound Tips To Lose Fat And Keep Your Muscle, 1280x720, 516393 bytes.
- 5053539: Deadlifts Build A Powerlifter Body, Not An Aesthetic One, 1080x1920, 1651105 bytes.
- 5211312: The Stomach Vacuum: The Best Ab Exercise For Belly Fat (How To Do It), 1280x720, 216462 bytes.
- 5090110: If I Had Belly Fat, Here's How I'd Lose It In 90 Days, 1280x720, 301155 bytes.
