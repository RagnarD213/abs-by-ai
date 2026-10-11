#!/usr/bin/env python3
"""Builds ro07-work-out-every-day.json from the filed youtube-description.md."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
D = R / "claude edited long form content/14 - Why You MUST Work Out Every Day"
desc = (D / "youtube-description.md").read_text().strip()
P = "https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/"
cfg = {
  "content_type": "organic",
  "source": "claude edited long form content/14 - Why You MUST Work Out Every Day/Why You MUST Work Out Every Day | claude round 3 | 16x9 | RO-07.mp4",
  "slug": "ro07-work-out-every-day",
  "title": "Why You MUST Work Out Every Day (5 Minute Beginner Workout)",
  "main": "2027-01-10T15:00:00.000Z",
  "keyword": "TRAIN",
  "ai_generated": True,
  "hook": "A 5 minute workout done every day gets beginners better results than a one hour workout done twice per week.",
  "body": "You'll barely feel any soreness after 5 minutes, so you won't be dreading your next workout. And there's no decision to make about whether you're working out today, it just becomes who you are, like brushing your teeth. The 5 minute workout is squats, push-ups, lunges and towel rows.",
  "close": "If you're not working out at all right now, start with 5 minutes tomorrow morning, and subscribe.",
  "tags": "#WorkOutEveryDay #HomeWorkout #BeginnerWorkout #AbsByAI",
  "youtube_description": desc,
  "mirror_cta": "More from @danrosefit 👇",
  "video_url": P + "f3b25e96-112a-4837-b710-597a8789a24c.mp4",
  "tiktok_video_url": P + "05e590fb-b538-49dc-9298-552aa4c74df9.mp4",
  "instagram_video_url": P + "16b5e0eb-f9f4-4cdf-b165-fdc2969d559f.mp4",
  "youtube_cover_url": P + "3c566953-7926-4d3a-bea8-fb3cf25ade82.jpg",
  "instagram_cover_url": P + "3c566953-7926-4d3a-bea8-fb3cf25ade82.jpg",
}
out = pathlib.Path(__file__).with_name("ro07-work-out-every-day.json")
out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
print("wrote", out)
