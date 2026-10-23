#!/usr/bin/env python3
"""Builds ro14-not-losing-weight.json from the filed youtube-description.md and social-copy.json (RO-14 setup, 2026-10-22)."""
import json, pathlib
MAIN = pathlib.Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI")
D = MAIN / "claude edited long form content/22 - Why You're Not Losing Weight"
desc = (D / "youtube-description.md").read_text().strip()
social = json.loads((D / "social-copy.json").read_text())
P = "https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/"
cfg = {
  "content_type": "organic",
  "source": "claude edited long form content/22 - Why You're Not Losing Weight/Why You're Not Losing Weight | claude round 3 | 16x9 | RO-14.mp4",
  "slug": "ro14-not-losing-weight",
  "title": "Why You're Not Losing Weight (4 Hidden Calorie Leaks)",
  # No 2026 Sunday or Wednesday was left (Docs/LONGFORM_RELEASE_CALENDAR.md); first free 2027 Sunday, Jan 3, 9 AM Central.
  # Socials follow Mon Jan 4 noon (longform_queue.py sets them).
  "main": "2027-01-03T15:00:00.000Z",
  "keyword": "TRACK",
  "ai_generated": True,  # nine realistic AI clips, labelled on screen
  "hook": social["hook"],
  "body": social["body"],
  "close": social["close"],
  "tags": "#WeightLoss #FatLoss #CalorieDeficit #AbsByAI",
  "pinned_comment": social["pinned_comment"],
  "youtube_description": desc,
  "mirror_cta": "More from @danrosefit 👇",
  "video_url": P + "b17af118-b3a5-4867-be2e-1a39bf01d4c1.mp4",
  "tiktok_video_url": P + "800f72fe-8a01-431e-86d6-6df6249794a6.mp4",
  "instagram_video_url": P + "a23478de-539e-4336-a6fa-9aa95d8b6ac2.mp4",
  "youtube_cover_url": P + "b8ae7f31-cf47-4483-87fd-3ba0b2c46261.jpg",
  "instagram_cover_url": P + "b8ae7f31-cf47-4483-87fd-3ba0b2c46261.jpg",
}
out = pathlib.Path(__file__).with_name("ro14-not-losing-weight.json")
out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
print("wrote", out)
