#!/usr/bin/env python3
"""Builds ro08-intermittent-fasting.json from the filed youtube-description.md."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
D = R / "claude edited long form content/15 - Intermittent Fasting The Best Way To Get Abs"
desc = (D / "youtube-description.md").read_text().strip()
P = "https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/"
cfg = {
  "content_type": "organic",
  "source": "claude edited long form content/15 - Intermittent Fasting The Best Way To Get Abs/Intermittent Fasting The Best Way To Get Abs | claude round 3 | 16x9 | RO-08.mp4",
  "slug": "ro08-intermittent-fasting",
  "title": "Intermittent Fasting: The Best Way To Get Abs",
  "main": "2026-11-18T15:00:00.000Z",
  "keyword": "FOOD",
  "ai_generated": True,
  "hook": "Here's the simplest way to do intermittent fasting to get abs.",
  "body": "I've been doing intermittent fasting for about 10 years, and what I personally do is skip breakfast, drink cold brew black coffee, and eat my first meal around 2 PM. That's about a five hour fasting window every morning, and it's a plan you can execute when life punches you in the face. Start by skipping breakfast, break your fast with a salad, and avoid binge eating late at night, eating within two hours of bedtime, and breaking your fast with alcohol.",
  "close": "Try skipping breakfast, and follow for more.",
  "tags": "#IntermittentFasting #SixPackAbs #FatLoss #AbsByAI",
  "tiktok_direct": True,  # 14:40 is over Blotato's TikTok limit; posted in TikTok Studio the Monday after release
  "pinned_comment": "What time do you usually eat your first meal right now?",
  "youtube_description": desc,
  "mirror_cta": "More from @danrosefit 👇",
  "video_url": P + "dbd54f47-5ee0-40a2-94bc-e4b8cfdc7646.mp4",
  "tiktok_video_url": P + "60150af2-3b0f-4076-addc-da008b9a0a1c.mp4",  # cover-first copy, posted by hand (tiktok_direct)
  "instagram_video_url": P + "6549c510-b57d-415a-9391-9d43083e84eb.mp4",
  "youtube_cover_url": P + "8febfe51-afb2-4c3e-81c2-9850ea1f4f1e.jpg",
  "instagram_cover_url": P + "8febfe51-afb2-4c3e-81c2-9850ea1f4f1e.jpg",
}
out = pathlib.Path(__file__).with_name("ro08-intermittent-fasting.json")
out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
print("wrote", out)
