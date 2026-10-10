#!/usr/bin/env python3
"""Builds ro06-home-workout-budget.json from the filed youtube-description.md. Refuses while any [LINK_...] placeholder remains."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
D = R / "claude edited long form content/13 - How To Work Out At Home On A Budget"
desc = (D / "youtube-description.md").read_text().strip()
assert "[LINK_" not in desc, "Amazon links still missing in youtube-description.md"
P = "https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/"
cfg = {
  "content_type": "organic",
  "source": "claude edited long form content/13 - How To Work Out At Home On A Budget/How To Work Out At Home On A Budget | claude round 6 | 16x9 | RO-06.mp4",
  "slug": "ro06-home-workout-budget",
  "title": "How To Work Out At Home On A Budget (Full Setup For $58)",
  "main": "2026-12-20T15:00:00.000Z",
  "keyword": "TRAIN",
  "ai_generated": True,
  "hook": "You don't need a gym membership to get in shape. A full home gym costs $58.",
  "body": "A yoga mat, push-up handles, a jump rope and an ab wheel is the whole basic setup. Add a kettlebell, medicine ball and dumbbells and the complete setup is about $150. Every item, what it costs and the cheap version that works just as well.",
  "close": "Save this for when you build your home gym. Subscribe so you don't miss the next one.",
  "tags": "#HomeWorkout #HomeGym #BudgetWorkout #AbsByAI",
  "youtube_description": desc,
  "mirror_cta": "More from @danrosefit 👇",
  "video_url": P + "7a52ff60-894b-491d-8994-7793336c5c9c.mp4",
  "tiktok_video_url": P + "a967e34d-7514-4b2c-b142-ae51290807cd.mp4",
  "youtube_cover_url": P + "65437c3b-1986-451b-aebb-9342c2bcba26.jpg",
  "instagram_cover_url": P + "65437c3b-1986-451b-aebb-9342c2bcba26.jpg",
}
out = pathlib.Path(__file__).with_name("ro06-home-workout-budget.json")
out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
print("wrote", out)
