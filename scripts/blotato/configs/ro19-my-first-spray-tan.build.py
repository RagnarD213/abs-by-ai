#!/usr/bin/env python3
"""Builds ro19-my-first-spray-tan.json from the filed youtube-description.md."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
D = R / "claude edited long form content/16 - My First Spray Tan (RO-19 re-edit)"
desc = (D / "youtube-description.md").read_text().strip()
P = "https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/"
cfg = {
  "content_type": "organic",
  "source": "claude edited long form content/16 - My First Spray Tan (RO-19 re-edit)/My First Spray Tan | claude round 4 | 16x9 | RO-19.mp4",
  "slug": "ro19-my-first-spray-tan",
  "title": "Spray Tanning Guide: How To Looksmax With A Spray Tan",
  "main": "2027-01-17T15:00:00.000Z",
  "keyword": "TRACK",
  "ai_generated": True,
  "hook": "I just got my first spray tan, and here's why you should consider one if you want to look good in photos.",
  "body": "Cameras flatten your definition, and definition on camera is all about contrast, so the same physique looks much more defined with a tan. It cost me about $100 with the contouring, or about $50 at a cheaper studio without it. I was in and out in about 10 minutes, and it lasts about seven days.",
  "close": "So get your spray tan before your next photo shoot, wedding or big event, and follow for more.",
  "tags": "#SprayTan #SprayTanning #FitnessPhotos #AbsByAI",
  "pinned_comment": "Have you ever had a spray tan? If so, was it professional or do-it-yourself at home?",
  "youtube_description": desc,
  "mirror_cta": "More from @danrosefit 👇",
  "video_url": P + "5c83df9c-c83d-4bc1-af0a-47d844d6339e.mp4",
  "tiktok_video_url": P + "b282de25-c4a3-4816-936a-98865255ba3b.mp4",
  "instagram_video_url": P + "e0661431-a3b4-42cb-ae60-34b7ca16c3a0.mp4",
  "youtube_cover_url": P + "086784b4-c84b-4bce-aecf-7165cd6b06ae.jpg",
  "instagram_cover_url": P + "086784b4-c84b-4bce-aecf-7165cd6b06ae.jpg",
}
out = pathlib.Path(__file__).with_name("ro19-my-first-spray-tan.json")
out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
print("wrote", out)
