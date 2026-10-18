#!/usr/bin/env python3
"""Builds ro17-3-healthy-foods.json from the filed youtube-description.md (RO-17 setup, 2026-10-18)."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
MAIN = pathlib.Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI")
D = MAIN / "claude edited long form content/17 - 3 Healthy Foods That Made Me Fat"
desc = (D / "youtube-description.md").read_text().strip()
P = "https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/"
cfg = {
  "content_type": "organic",
  "source": "claude edited long form content/17 - 3 Healthy Foods That Made Me Fat/3 Healthy Foods That Made Me Fat | claude round 5 | 16x9 | RO-17.mp4",
  "slug": "ro17-3-healthy-foods",
  "title": "3 Healthy Foods That Made Me Fat",
  # Docs/LONGFORM_RELEASE_CALENDAR.md: a film finished before December takes RO-22's Sunday (Dec 13). Socials Mon Dec 14 noon.
  "main": "2026-12-13T15:00:00.000Z",
  "keyword": "FOOD",
  "ai_generated": True,  # eight realistic AI clips, labelled on screen
  "hook": "One cup of trail mix is about 700 calories. That's more than a Big Mac.",
  "body": "Trail mix, dried fruit and coconut water are sold as health foods, but they're high in calories and very easy to eat too much of. Cutting them is what finally let me lose the last 10 pounds and see my abs. Now I snack on sardines, hard boiled eggs and chicken, and they fill me up far better.",
  "close": "Save this for your next grocery run, and comment below with the healthy food that was making you fat.",
  "tags": "#HealthyFoods #FatLoss #Snacks #AbsByAI",
  "pinned_comment": "Which one were you eating because you thought it was healthy: trail mix, dried fruit or coconut water?",
  "youtube_description": desc,
  "mirror_cta": "More from @danrosefit 👇",
  "video_url": P + "aebf44fb-534b-4990-b376-f6bdea6c9cd7.mp4",
  "tiktok_video_url": P + "fc720fd7-1f5a-4664-8c29-efe98c821e14.mp4",
  "instagram_video_url": P + "9399e11a-e0a2-4581-a95a-82f98fb2ae51.mp4",
  "youtube_cover_url": P + "e9468e76-4cd7-44cb-a334-4d4b3a2c5451.jpg",
  "instagram_cover_url": P + "e9468e76-4cd7-44cb-a334-4d4b3a2c5451.jpg",
}
out = pathlib.Path(__file__).with_name("ro17-3-healthy-foods.json")
out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
print("wrote", out)
