"""Install Dan's November 9 covers and upload setup assets, without scheduling.

Run with ``prepare`` then ``upload``. State lives outside Git and makes retries
reuse verified assets. This script never calls a post creation endpoint.
"""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts/blotato'))
import tiktok_cover
from danrosefit_migration import api_key, call

WORK = Path('/Volumes/Extreme/_edit_work/SL-12/setup/installed-20261109')
ROUND = WORK.parent / 'round3'
APP = ROOT / 'Short-form video content/covers/approved-sl12'
WORDS = "These look good. Approve the revised A2 covers and B’s Instagram cover, and finish setting up both. Keep publishing on hold until the parent is public on December 6."
JOBS = [('A', 'A2', 'sl12-a-weightlifting', '17286ab36fdc19c69986d217396debbdd8b816ebdc3d6de4bc7a2e3607154ae0'),
        ('B', 'BX2', 'sl12-b-daily-protein', 'dc37c605692b7d8c6bb09a3bc16b2fddf5f85dfd815a1eb3580719087f7b2e38')]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def prepare():
    WORK.mkdir(parents=True, exist_ok=True)
    APP.mkdir(parents=True, exist_ok=True)
    manifest_path = WORK / 'installed.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    approved = json.loads((ROUND / 'manifest.json').read_text())['outputs']
    for letter, pick, slug, master_hash in JOBS:
        cfg_path = ROOT / f'scripts/blotato/configs/{slug}.json'
        cfg = json.loads(cfg_path.read_text())
        assert cfg['release_hold'] and cfg['main'] is None and not cfg['schedule_ids']
        assert sha(cfg['source']) == master_hash, 'Approved master changed'
        covers = {}
        for platform in ['instagram', 'youtube']:
            row = next(r for r in approved if r['label'] == pick and r['platform'] == platform)
            for ext, key in [('png', 'sha256'), ('jpg', 'jpeg_sha256')]:
                src = ROUND / f'covers/{pick}/{platform}.{ext}'
                assert sha(src) == row[key]
                dest = APP / f'{slug}-{platform}-approved.{ext}'
                shutil.copyfile(src, dest)
                assert sha(dest) == row[key]
                covers[platform + '_' + ext] = str(dest)
        tt = WORK / f'{slug}-tiktok-coverfirst.mp4'
        old = manifest.get(letter, {})
        if old.get('tiktok_sha256') != (sha(tt) if tt.exists() else None) or not old.get('verify', {}).get('ok'):
            verification = tiktok_cover.build(cfg['source'], covers['instagram_png'], str(tt))
            assert verification['ok'], verification
        else:
            verification = old['verify']
        manifest[letter] = dict(job='SL-12-' + letter, slug=slug, pick=pick,
            video=cfg['source'], video_sha256=master_hash, tiktok=str(tt),
            tiktok_sha256=sha(tt), ig_cover=covers['instagram_png'],
            yt_cover=covers['youtube_jpg'], covers=covers, verify=verification,
            approved_date='2026-11-09', dan_words=WORDS, release_hold=True)
        save(manifest_path, manifest)
        cfg['cover_approved'] = True
        cfg['cover_selection'].update(revision_approved=True, installed=True,
            approval_date='2026-11-09', dan_words=WORDS)
        if letter == 'B':
            cfg['cover_selection']['instagram_approval'] = 'approved exact revised image November9'
        cfg['cover_local'] = covers
        cfg['setup_stage'] = 'approved_covers_installed_uploading'
        cfg['hold_reason'] = 'Dan: hold publishing until parent RO01 is verified public on or after December 6, 2026. Do not clear from the calendar alone.'
        save(cfg_path, cfg)
        print(letter, 'approved covers installed; TikTok checked', verification, flush=True)


def upload():
    manifest = json.loads((WORK / 'installed.json').read_text())
    state_path = WORK / 'uploads.json'
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    key = api_key()
    for letter, pick, slug, _ in JOBS:
        cfg_path = ROOT / f'scripts/blotato/configs/{slug}.json'
        cfg = json.loads(cfg_path.read_text())
        assert cfg['release_hold'] and cfg['main'] is None and not cfg['schedule_ids']
        for asset in ['video', 'tiktok', 'ig_cover', 'yt_cover']:
            path = Path(manifest[letter][asset])
            data = path.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            token = letter + ':' + asset
            entry = state.get(token)
            if entry and entry.get('sha256') == digest:
                back = urllib.request.urlopen(entry['url'], timeout=90).read()
                assert hashlib.sha256(back).hexdigest() == digest
                print(token, 'existing upload rechecked', flush=True)
                continue
            mime = {'.mp4': 'video/mp4', '.png': 'image/png', '.jpg': 'image/jpeg'}[path.suffix]
            response = call('POST', '/media/uploads', key, {'filename': path.name})
            urllib.request.urlopen(urllib.request.Request(response['presignedUrl'],
                data=data, method='PUT', headers={'Content-Type': mime}), timeout=120).read()
            back = urllib.request.urlopen(response['publicUrl'], timeout=120).read()
            assert len(back) == len(data) and hashlib.sha256(back).hexdigest() == digest
            state[token] = dict(url=response['publicUrl'], path=str(path),
                sha256=digest, bytes=len(data), hash_verified=True)
            save(state_path, state)
            print(token, 'uploaded and full SHA256 verified', len(data), flush=True)
        for asset, field in [('video', 'video_url'), ('tiktok', 'tiktok_video_url'),
                             ('ig_cover', 'instagram_cover_url'), ('yt_cover', 'youtube_cover_url')]:
            cfg[field] = state[letter + ':' + asset]['url']
        cfg['setup_stage'] = 'uploaded_held_for_parent_public'
        save(cfg_path, cfg)
    print('Eight uploaded assets verified. No posts created. Both publishing holds retained.')


if __name__ == '__main__':
    {'prepare': prepare, 'upload': upload}[sys.argv[1]]()
