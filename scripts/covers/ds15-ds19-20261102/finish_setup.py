"""Resume the approved DS-15/19 setup uploads, retaining hash receipts."""
import hashlib
import json
import mimetypes
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = Path('/Volumes/Extreme/_edit_work/ds15-ds19-publish')
sys.path.insert(0, str(ROOT / 'scripts/blotato'))
from danrosefit_migration import api_key, call


def digest(path):
    sha = hashlib.sha256()
    with open(path, 'rb') as source:
        while chunk := source.read(1024 * 1024):
            sha.update(chunk)
    return sha.hexdigest()


def remote_digest(url):
    sha = hashlib.sha256()
    size = 0
    with urllib.request.urlopen(url, timeout=120) as response:
        while chunk := response.read(1024 * 1024):
            sha.update(chunk)
            size += len(chunk)
    return sha.hexdigest(), size


def main():
    files = json.loads((WORK / 'files.json').read_text())
    receipt = WORK / 'uploads.json'
    state = json.loads(receipt.read_text()) if receipt.exists() else {}
    for job, info in files.items():
        assets = {
            'master': Path(info['master']),
            'tiktok': WORK / f'{job}-tiktok-cover-first.mp4',
            'instagram_cover': Path(info['instagram_cover']),
            'youtube_cover': Path(info['youtube_cover']),
        }
        for kind, path in assets.items():
            if kind == 'tiktok':
                checked = WORK / f'{job}-tiktok-verification.json'
                if not checked.exists():
                    print('waiting for derivative verification', job, flush=True)
                    continue
                assert json.loads(checked.read_text())['ok']
            key = f'{job}/{kind}'
            sha = digest(path)
            size = path.stat().st_size
            if key in state:
                assert state[key]['sha256'] == sha
                assert remote_digest(state[key]['url']) == (sha, size)
                print('verified existing', key, flush=True)
                continue
            uploaded = call('POST', '/media/uploads', api_key(), {'filename': path.name})
            request = urllib.request.Request(
                uploaded['presignedUrl'], data=path.read_bytes(), method='PUT',
                headers={'Content-Type': mimetypes.guess_type(path.name)[0] or 'application/octet-stream'},
            )
            with urllib.request.urlopen(request, timeout=300) as response:
                response.read()
            assert remote_digest(uploaded['publicUrl']) == (sha, size), key
            state[key] = {'url': uploaded['publicUrl'], 'sha256': sha, 'bytes': size, 'local': str(path)}
            receipt.write_text(json.dumps(state, indent=2) + '\n')
            print('uploaded and downloaded/hash-verified', key, size, flush=True)


if __name__ == '__main__':
    main()
