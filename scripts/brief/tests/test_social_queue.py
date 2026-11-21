import unittest
from datetime import datetime, timezone
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from social_queue import normalize


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 2, 18, tzinfo=timezone.utc)
        self.item = {"id": "synthetic", "scheduledAt": "2026-10-03T18:00:00Z", "account": {"name": "Example"},
                     "draft": {"accountId": "fixture-account", "content": {"platform": "facebook", "text": "Example", "mediaUrls": ["https://example.com/video.mp4"]}, "target": {}}}

    def test_missing_is_not_empty_and_facebook_cover_not_inferred_missing(self):
        q = normalize({"checkedAt": self.now.isoformat(), "items": [self.item]}, None, [], self.now)
        self.assertEqual(q["sourceCoverage"]["youtubeStudio"], "missing")
        self.assertEqual(q["rows"][0]["preflight"]["cover"], "unverified")
        self.assertEqual(q["rows"][0]["preflight"]["description"], "not_applicable")

    def test_duplicates_preserve_rows_and_window_excludes_boundary(self):
        other = {**self.item, "id": "synthetic2"}
        boundary = {**self.item, "id": "boundary", "scheduledAt": "2026-10-09T18:00:00Z"}
        q = normalize({"checkedAt": self.now.isoformat(), "items": [self.item, other, boundary]}, None, [], self.now)
        self.assertEqual(len(q["rows"]), 2)
        self.assertTrue(all(row["preflight"]["duplicates"] == "duplicate" for row in q["rows"]))

    def test_stale_and_human_review_flags_are_explicit(self):
        q = normalize({"checkedAt": "2026-09-30T18:00:00Z", "items": [self.item]}, None, [], self.now,
                      {"synthetic": {"notes": ["Crop needs review"], "preflight": {"assetMatch": "unverified"}}})
        self.assertEqual(q["sourceCoverage"]["blotato"], "stale")
        self.assertEqual(q["rows"][0]["notes"], ["Crop needs review"])

    def test_native_youtube_and_broken_links(self):
        v = {"id": "fixture-video", "status": {"publishAt": "2026-10-03T18:00:00Z"},
             "snippet": {"title": "Example", "description": "See https://example.com/missing", "channelId": "fixture-channel", "thumbnails": {"high": {"url": "https://example.com/cover.jpg"}}}}
        q = normalize(None, {"checkedAt": self.now.isoformat(), "videos": [v]}, [{"url": "https://example.com/missing", "status": 404}, {"url": "https://example.com/cover.jpg", "status": 200}], self.now)
        self.assertEqual(q["rows"][0]["preflight"]["links"], "broken")
        self.assertEqual(q["rows"][0]["preflight"]["cover"], "verified")
        self.assertEqual(q["rows"][0]["id"], "youtube:fixture-video")
