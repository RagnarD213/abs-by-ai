#!/usr/bin/env python3
"""SL-10 setup for picked covers: approved files, TikTok cover-first copy, Blotato media with hash read-back, config, Facebook cover row.
    python3 scripts/covers/sl10-20261101/setup_media.py s2=D s1=A
The letter names the built design. Nothing here schedules a post.
"""
import concurrent.futures, hashlib, json, shutil, subprocess, sys, urllib.request
from pathlib import Path
P = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(P/'scripts/blotato')); sys.path.insert(0, str(Path(__file__).parent))
from danrosefit_migration import api_key, call
import tiktok_cover as tc
from build import BUILT, SHORTS
A = P/'Short-form video content/covers/approved-sl10'; A.mkdir(exist_ok=True)
O = Path('/Volumes/Expansion/_edit_work/sl10-publish'); O.mkdir(exist_ok=True)
CAP = json.loads((Path(__file__).parent/'captions.json').read_text())
PARENT = 'scripts/blotato/configs/ro13-alcohol-and-abs.json'; PARENT_TITLE = 'Can You Drink Alcohol And Still Have Abs? (My 6 Rules)'
WORDS = json.loads((Path(__file__).parent/'pick-words.json').read_text())
EXPECT = dict(s1='cf0a7630c904d33d0269a0fb7f084c09591bc9f0c94457cf5fd354cea30974e5', s2='3f4a487f4066fabd24c82bfd2feb2f2bb80e270d9f6d14aebc0fc705b50c8021',
              s3='1d2458deca68b1b65349a4303451b24e2c3389f05aa9d37a7a7c8ec504d40bee', s4='aa2b52111159752370ba434e61694c04564d0b9c99b21f372e598e0bde5fdb9c')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
sp = O/'uploads.json'; state = json.loads(sp.read_text()) if sp.exists() else {}; key = api_key()

def upload(name, p):
    digest = sha(p); old = state.get(name, {})
    if old.get('sha256') == digest and old.get('remote_hash_verified'): return old['url']
    r = call('POST', '/media/uploads', key, {'filename': f'{name}{p.suffix}'})
    ct = {'.mp4': 'video/mp4', '.png': 'image/png', '.jpg': 'image/jpeg'}[p.suffix]
    urllib.request.urlopen(urllib.request.Request(r['presignedUrl'], data=p.read_bytes(), method='PUT', headers={'Content-Type': ct}), timeout=300).read()
    with urllib.request.urlopen(r['publicUrl'], timeout=300) as f: assert hashlib.sha256(f.read()).hexdigest() == digest, name
    state[name] = dict(path=str(p), sha256=digest, bytes=p.stat().st_size, url=r['publicUrl'], remote_hash_verified=True); sp.write_text(json.dumps(state, indent=2))
    print('uploaded and hash-checked', name, flush=True)
    return r['publicUrl']

def audio(path):
    r = subprocess.run([tc.FFMPEG, '-v', 'error', '-i', str(path), '-map', '0:a:0', '-c', 'copy', '-f', 'adts', '-'], capture_output=True, check=True)
    return hashlib.sha256(r.stdout).hexdigest()

def one(s, k):
    spec, c = SHORTS[s], CAP[s]; src = P/c['source']; assert sha(src) == EXPECT[s], s
    ig = A/f"Instagram_{spec['slug']}_cover.png"; yt = A/f"YouTube_{spec['slug']}_cover.jpg"; yp = yt.with_suffix('.png')
    shutil.copy2(BUILT/s/k/'instagram.png', ig); shutil.copy2(BUILT/s/k/'youtube.jpg', yt); shutil.copy2(BUILT/s/k/'youtube.png', yp)
    dst = O/f"{spec['slug']}_tiktok.mp4"
    res = tc.build(str(src), str(ig), str(dst)); assert res.get('ok'), res
    a, b = audio(src), audio(dst); assert a == b, 'audio changed'
    fr = O/f"{spec['slug']}_frame0.png"; subprocess.run([tc.FFMPEG, '-v', 'error', '-y', '-i', str(dst), '-frames:v', '1', str(fr)], check=True)
    urls = {n: upload(f"{c['slug']}-{n}", q) for n, q in [('master', src), ('tiktok', dst), ('instagram', ig), ('youtube', yt)]}
    lede = f"{c['hook']}\n\n{c['body']}\n\n{c['close']}"
    link = lambda m: f"https://absbyai.com/?utm_source={m}&utm_medium=short&utm_campaign=alcohol-and-abs&utm_content={c['slug']}"
    tail = f"Some footage in this video is AI-generated and labeled on screen.\n\n{c['tags']}"
    cfg = dict(content_type='organic', source=c['source'], slug=c['slug'], campaign='alcohol-and-abs', title=c['title'], video_url=urls['master'], tiktok_video_url=urls['tiktok'],
        instagram_cover_url=urls['instagram'], youtube_cover_url=urls['youtube'], main=c['main'], keyword='FOOD', ai_generated=True, hook=c['hook'], body=c['body'], close=c['close'], tags=c['tags'],
        youtube_description=f"{lede}\n\nTry Abs By AI:\n{link('youtube')}\n\nFull video on this channel: {PARENT_TITLE}\n\n{tail}", pinned_comment=c['pinned_comment'],
        instagram_first_comment=f"Try Abs By AI: {link('instagram')}", caption_overrides=dict(
            facebook=f"{lede}\n\nTry Abs By AI:\n{link('facebook')}\n\n{tail}", instagram=f"{lede}\n\nComment FOOD and I'll send you the Abs By AI link.\n\n{tail}",
            tiktok=f"{lede}\n\nAbs By AI, link in bio.\n{link('tiktok')}\n\n{tail}"),
        parent_config=PARENT, kitchen=False, gym=False, filming_set='studio', approved_cover=k, approval_date='2026-11-01',
        media_sha256=dict(master=EXPECT[s], tiktok=sha(dst), ig=sha(ig), yt=sha(yt)))
    name = {'s1': 'sl10-short1-your-drinks-should-taste-bad', 's2': 'sl10-short2-your-nightly-wine-is-killing-your-abs', 's3': 'sl10-short3-stop-drinking-3-hours-before-bed', 's4': 'sl10-short4-what-killed-my-urge-to-drink'}[s]
    (P/f'scripts/blotato/configs/{name}.json').write_text(json.dumps(cfg, indent=2, ensure_ascii=False)+'\n')
    return dict(short=s, title=c['title'], design=k, words=WORDS[s], config=f'scripts/blotato/configs/{name}.json', instagram=str(ig), instagram_sha256=sha(ig), youtube=str(yt), youtube_sha256=sha(yt),
                youtube_png_sha256=sha(yp), film_sha256=EXPECT[s], tiktok=str(dst), tiktok_sha256=sha(dst), tiktok_frames=res, audio_payload_identical=True, frame0=str(fr))

pj = A/'picks.json'; picks = json.loads(pj.read_text()) if pj.exists() else dict(job='SL-10', picked_by='Dan', date='2026-11-01', covers={})
for arg in sys.argv[1:]:
    s, k = arg.split('='); picks['covers'][SHORTS[s]['slug']] = one(s, k); pj.write_text(json.dumps(picks, indent=2)); print('ready', s, k, flush=True)
