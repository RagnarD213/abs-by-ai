"""Block video scheduling when required cover settings are absent or broken."""
import io
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
from functools import lru_cache
from PIL import Image

HERE = Path(__file__).resolve().parent

@lru_cache(maxsize=128)
def check_image(url, youtube=False):
    if not isinstance(url, str) or not url.startswith('https://'):
        raise ValueError('A public HTTPS cover image is required')
    with urlopen(url, timeout=30) as response:
        data = response.read(10 * 1024 * 1024 + 1)
    if len(data) > 10 * 1024 * 1024 or youtube and len(data) >= 2_000_000:
        raise ValueError('Cover image exceeds the upload size limit')
    with Image.open(io.BytesIO(data)) as image:
        image.verify()


def assert_video_cover(body):
    post = body.get('post', {})
    content = post.get('content', {})
    target = post.get('target', {})
    urls = content.get('mediaUrls', [])
    platform = content.get('platform')
    # Known photo extensions are stills. Unknown extensions must be checked as video.
    if not urls or all(u.split('?')[0].lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')) for u in urls):
        return
    if platform == 'youtube':
        check_image(target.get('thumbnailUrl'), youtube=True)
    elif platform == 'instagram':
        check_image(target.get('coverImageUrl'))
    elif platform == 'tiktok':
        if target.get('videoCoverTimestamp') != 0:
            raise ValueError('TikTok video requires a verified cover-first export and videoCoverTimestamp: 0')
    elif platform == 'facebook':
        registry = json.loads((HERE / 'fb_reel_covers.json').read_text())
        line = content.get('text', '').strip().split('\n')[0].strip()
        hit = next((r for r in registry if r['match'].strip().split('\n')[0].strip() == line), None)
        if not hit or not Path(hit['cover']).is_file():
            raise ValueError('Facebook video requires its approved cover in fb_reel_covers.json and the live installer')
        with Image.open(hit['cover']) as image:
            image.verify()
        live = Path.home() / '.absbyai/fb-reel-covers/fb_reel_covers.json'
        installed = json.loads(live.read_text())
        current = next((r for r in installed if r['match'].strip().split('\n')[0].strip() == line), None)
        if not current or not Path(current['cover']).is_file() or hashlib.sha256(Path(current['cover']).read_bytes()).digest() != hashlib.sha256(Path(hit['cover']).read_bytes()).digest():
            raise ValueError('Facebook approved cover has not been synced to the live installer')
