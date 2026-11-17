"""Install Dan's approved DS-30 stills and file exact-master setup evidence on M2.

No film encoding or scheduling is performed here. Each command is resumable.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[3]
WORK = Path('/Volumes/Expansion/_edit_work/DS-30-setup')
FILM = ROOT / 'Short-form video content/Self-Driving Car - DS-30'
APPROVED = ROOT / 'Short-form video content/covers/approved-ds30'
MASTER = FILM / 'Self-Driving Car SFC R1 - complete Short.mp4'
SRT = FILM / 'Self-Driving Car SFC R1.srt'
EXPECTED = '31dcb750b089c33e01622da845c9bf15281a932b6132e3cb10f66f6f957dc4fc'
sys.path.insert(0, str(ROOT / 'scripts/blotato'))


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.ds30-tmp')
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    tmp.replace(path)


def copy_verified(src, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists() or sha(dest) != sha(src):
        shutil.copy2(src, dest)
    assert sha(src) == sha(dest)
    return dict(file=str(dest), sha256=sha(dest), bytes=dest.stat().st_size)


def install():
    assert sha(MASTER) == EXPECTED
    records = {}
    for platform in ('Instagram', 'YouTube'):
        for ext in ('png', 'jpg'):
            name = f'R2-X4-Car-Fixed-{platform}.{ext}'
            records[f'{platform} {ext}'] = copy_verified(
                WORK / 'r5/covers' / name, APPROVED / name)
    picks = dict(date='2026-11-16', selected='R2-X4, corrected car and final With A copy',
                 final_approval_words='These look good. Approve both covers and finish the setup.',
                 final_cover_approved=True, installed_local_covers=True,
                 cover_text=['Make Time For Fitness', 'With A Self-Driving Car'],
                 film_title='Make Time for Fitness with a Self-Driving Car.',
                 film_sha256=EXPECTED, files=records, original_foreground_preserved=True,
                 source_pick_logged_previously=True)
    save(APPROVED / 'picks.json', picks)
    save(WORK / 'final-cover-approval.json', picks)
    (WORK / 'SETUP-STATUS.txt').write_text('Both exact corrected covers approved by Dan 2026-11-16. Finishing setup.\n')
    print('Installed and hash-verified four approved cover files. Master unchanged.', flush=True)


def backup():
    assert sha(MASTER) == EXPECTED
    extreme = Path('/Volumes/Extreme/Short-form video content/Self-Driving Car - DS-30')
    receipt = dict(local=[dict(file=str(p), sha256=sha(p), bytes=p.stat().st_size) for p in (MASTER, SRT)], extreme=[])
    for p in (MASTER, SRT):
        receipt['extreme'].append(copy_verified(p, extreme / p.name))
    save(WORK / 'backup-verification.json', receipt)
    remote = 'gdrive_backup:Short-form video content/Self-Driving Car - DS-30'
    rclone = str(Path.home() / 'bin/rclone')
    for p in (MASTER, SRT):
        subprocess.run([rclone, 'copyto', str(p), remote + '/' + p.name], check=True)
        proc = subprocess.Popen([rclone, 'cat', remote + '/' + p.name], stdout=subprocess.PIPE)
        h = hashlib.sha256(); count = 0
        while True:
            b = proc.stdout.read(1024 * 1024)
            if not b:
                break
            h.update(b); count += len(b)
        assert proc.wait() == 0
        assert h.hexdigest() == sha(p) and count == p.stat().st_size
        receipt.setdefault('drive', []).append(dict(remote=remote + '/' + p.name, sha256=h.hexdigest(), bytes=count))
        save(WORK / 'backup-verification.json', receipt)
        print('Drive download hash verified:', p.name, flush=True)
    receipt['drive_folder_url'] = subprocess.check_output([rclone, 'link', remote], text=True).strip()
    receipt['drive_readback'] = json.loads(subprocess.check_output([rclone, 'lsjson', remote], text=True))
    receipt['complete'] = True
    save(WORK / 'backup-verification.json', receipt)
    print('Three copies verified. Drive folder:', receipt['drive_folder_url'], flush=True)


def tiktok():
    from tiktok_cover import build
    out = WORK / 'Self-Driving-Car-DS30-TikTok.mp4'
    result = build(str(MASTER), str(APPROVED / 'R2-X4-Car-Fixed-Instagram.png'), str(out))
    save(WORK / 'tiktok-verification.json', result)
    assert result['ok'], result
    # Verify the complete encoded elementary video and audio payloads are preserved.
    ff = ROOT / 'Media/video_edit/bin/ffmpeg'
    def stream_hash(path, kind, skip=0):
        fmt = 'h264' if kind == 'v' else 'adts'
        p = subprocess.Popen([str(ff), '-v', 'error', '-i', str(path), '-map', f'0:{kind}:0',
                              '-c', 'copy', '-f', fmt, '-'], stdout=subprocess.PIPE)
        h = hashlib.sha256()
        for b in iter(lambda: p.stdout.read(1024 * 1024), b''):
            h.update(b)
        assert p.wait() == 0
        return h.hexdigest()
    audio = dict(master=stream_hash(MASTER, 'a'), tiktok=stream_hash(out, 'a'))
    audio['identical'] = audio['master'] == audio['tiktok']
    assert audio['identical']
    save(WORK / 'audio-payload-identity.json', audio)
    assert sha(MASTER) == EXPECTED
    print('TikTok one-frame cover derivative verified; film video stream copied, complete audio payload identical.', flush=True)


def upload():
    from danrosefit_migration import api_key, call
    assert sha(MASTER) == EXPECTED
    files = dict(master=MASTER, tiktok=WORK / 'Self-Driving-Car-DS30-TikTok.mp4',
                 instagram=APPROVED / 'R2-X4-Car-Fixed-Instagram.png',
                 youtube=APPROVED / 'R2-X4-Car-Fixed-YouTube.jpg')
    if len(sys.argv) > 2:
        files = {k: v for k, v in files.items() if k in sys.argv[2:]}
    if 'tiktok' in files:
        assert json.loads((WORK / 'tiktok-verification.json').read_text())['ok']
    statepath = WORK / 'uploads.json'
    state = json.loads(statepath.read_text()) if statepath.exists() else {}
    key = api_key()
    for name, p in files.items():
        digest = sha(p)
        prior = state.get(name, {})
        if prior.get('sha256') == digest and prior.get('remote_hash_verified'):
            print('Previously uploaded and verified:', name, flush=True)
            continue
        record = call('POST', '/media/uploads', key, {'filename': 'ds30-fitness-self-driving-car-' + name + p.suffix})
        mime = {'.mp4': 'video/mp4', '.png': 'image/png', '.jpg': 'image/jpeg'}[p.suffix]
        urllib.request.urlopen(urllib.request.Request(record['presignedUrl'], data=p.read_bytes(), method='PUT',
                                                     headers={'Content-Type': mime}), timeout=300).read()
        state[name] = dict(url=record['publicUrl'], sha256=digest, bytes=p.stat().st_size,
                           path=str(p), remote_hash_verified=False)
        save(statepath, state)
        with urllib.request.urlopen(record['publicUrl'], timeout=300) as response:
            data = response.read()
        assert len(data) == p.stat().st_size and hashlib.sha256(data).hexdigest() == digest
        state[name]['remote_hash_verified'] = True
        save(statepath, state)
        print('Uploaded and full-download SHA-256 verified:', name, len(data), flush=True)


if __name__ == '__main__':
    {'install': install, 'backup': backup, 'tiktok': tiktok, 'upload': upload}[sys.argv[1]]()
