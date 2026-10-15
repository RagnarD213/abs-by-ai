import io
import unittest
from unittest.mock import patch
from cover_guard import assert_video_cover, check_image

class CoverGuardTest(unittest.TestCase):
    def setUp(self):
        check_image.cache_clear()

    def post(self, platform, target=None):
        return {'post': {'content': {'platform': platform, 'text': 'Unregistered test', 'mediaUrls': ['https://example.com/video.mp4']}, 'target': target or {}}}

    def test_missing_settings_block_every_video_platform(self):
        for platform in ('youtube', 'instagram', 'tiktok', 'facebook'):
            with self.subTest(platform=platform), self.assertRaises(ValueError):
                assert_video_cover(self.post(platform))

    def test_http_success_with_non_image_body_is_rejected(self):
        with patch('cover_guard.urlopen', return_value=io.BytesIO(b'<html>not a cover</html>')):
            with self.assertRaises(Exception):
                assert_video_cover(self.post('instagram', {'coverImageUrl': 'https://example.com/cover.png'}))

    def test_oversized_youtube_cover_is_rejected(self):
        with patch('cover_guard.urlopen', return_value=io.BytesIO(b'x' * 2_000_001)):
            with self.assertRaisesRegex(ValueError, 'size limit'):
                assert_video_cover(self.post('youtube', {'thumbnailUrl': 'https://example.com/large.jpg'}))

    def test_photo_does_not_need_an_extra_cover(self):
        post = self.post('instagram')
        post['post']['content']['mediaUrls'] = ['https://example.com/photo.jpg']
        assert_video_cover(post)

if __name__ == '__main__':
    unittest.main()
