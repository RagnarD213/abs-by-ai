#!/usr/bin/env python3
"""SL-20 setup for a picked cover: TikTok cover-first copy, Blotato media with full hash read-back, config, Facebook cover row.
    python3 scripts/covers/sl20-20261105/setup_media.py s1
Covers come from Short-form video content/covers/approved-sl20/ (picks.json). Nothing here schedules a post.
"""
import hashlib, json, shutil, subprocess, sys, urllib.request
from pathlib import Path
P = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(P/'scripts/blotato'))
from danrosefit_migration import api_key, call
import tiktok_cover as tc
A = P/'Short-form video content/covers/approved-sl20'
O = Path('/Volumes/Expansion/_edit_work/sl20-publish'); O.mkdir(exist_ok=True)
CAP = json.loads((Path(__file__).parent/'captions.json').read_text())
MAN = json.loads((P/'Short-form video content/invest-SHORTS-final-manifest.json').read_text())
PARENT = 'scripts/blotato/configs/ro20-invest-in-your-health.json'; PARENT_TITLE = 'Why You Should Invest More In Your Health'
CAMPAIGN, KEYWORD = 'invest-in-your-health', 'COACH'
NAMES = {'s1': 'sl20-short1-dont-bother-dating-unless-youre-ripped', 's2': 'sl20-short2-why-being-fat-destroys-your-relationship',
         's3': 'sl20-short3-you-cant-afford-to-not-work-out'}
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
sp = O/'uploads.json'; state = json.loads(sp.read_text()) if sp.exists() else {}; key = api_key()


def upload(name, p):
    digest = sha(p); old = state.get(name, {})
    if old.get('sha256') == digest and old.get('remote_hash_verified'):
        return old['url']
    r = call('POST', '/media/uploads', key, {'filename': f'{name}{p.suffix}'})
    ct = {'.mp4': 'video/mp4', '.png': 'image/png', '.jpg': 'image/jpeg'}[p.suffix]
    urllib.request.urlopen(urllib.request.Request(r['presignedUrl'], data=p.read_bytes(), method='PUT', headers={'Content-Type': ct}), timeout=600).read()
    with urllib.request.urlopen(r['publicUrl'], timeout=600) as f:
        assert hashlib.sha256(f.read()).hexdigest() == digest, name
    state[name] = dict(path=str(p), sha256=digest, bytes=p.stat().st_size, url=r['publicUrl'], remote_hash_verified=True)
    sp.write_text(json.dumps(state, indent=2))
    print('uploaded and hash-checked', name, flush=True)
    return r['publicUrl']


def audio(path):
    r = subprocess.run([tc.FFMPEG, '-v', 'error', '-i', str(path), '-map', '0:a:0', '-c', 'copy', '-f', 'adts', '-'], capture_output=True, check=True)
    return hashlib.sha256(r.stdout).hexdigest()


def one(s):
    c = CAP[s]; n = int(s[1]); m = MAN['shorts'][n-1]
    picks = json.loads((A/'picks.json').read_text())
    pk = next(v for v in picks['covers'].values() if v['short'] == n)
    src = P/c['source']; assert sha(src) == m['sha256'], s
    ig, yt = P/pk['instagram'], P/pk['youtube']
    assert sha(ig) == pk['instagram_sha256'] and sha(yt) == pk['youtube_sha256']
    stem = Path(m['file']).stem
    dst = O/f'{stem}_tiktok.mp4'
    res = tc.build(str(src.resolve()), str(ig.resolve()), str(dst)); assert res.get('ok'), res
    assert audio(src) == audio(dst), 'audio changed'
    fr = O/f'{stem}_frame0.png'
    subprocess.run([tc.FFMPEG, '-v', 'error', '-y', '-i', str(dst), '-frames:v', '1', str(fr)], check=True)
    urls = {k: upload(f"{c['slug']}-{k}", q) for k, q in [('master', src), ('tiktok', dst), ('instagram', ig), ('youtube', yt)]}
    lede = f"{c['hook']}\n\n{c['body']}\n\n{c['close']}"
    link = lambda med: f'https://absbyai.com/?utm_source={med}&utm_medium=short&utm_campaign={CAMPAIGN}&utm_content={c["slug"]}'
    ai = c['ai_generated']
    tail = (f"Some footage in this video is AI-generated and labeled on screen.\n\n{c['tags']}" if ai else c['tags'])
    cfg = dict(content_type='organic', source=c['source'], slug=c['slug'], campaign=CAMPAIGN, title=c['title'], video_url=urls['master'],
               tiktok_video_url=urls['tiktok'], instagram_cover_url=urls['instagram'], youtube_cover_url=urls['youtube'], main=c['main'],
               keyword=KEYWORD, ai_generated=ai, hook=c['hook'], body=c['body'], close=c['close'], tags=c['tags'],
               youtube_description=f"{lede}\n\nTry Abs By AI:\n{link('youtube')}\n\nFull video on this channel: {PARENT_TITLE}\n\n{tail}",
               pinned_comment=c['pinned_comment'], instagram_first_comment=f"Try Abs By AI: {link('instagram')}",
               caption_overrides=dict(facebook=f"{lede}\n\nTry Abs By AI:\n{link('facebook')}\n\n{tail}",
                                      instagram=f"{lede}\n\nComment {KEYWORD} and I'll send you the Abs By AI link.\n\n{tail}",
                                      tiktok=f"{lede}\n\nAbs By AI, link in bio.\n{link('tiktok')}\n\n{tail}"),
               parent_config=PARENT, kitchen=True, gym=False, filming_set='kitchen (Aug 3)', approved_cover=pk['label'],
               approval_date=pk['date'], media_sha256=dict(master=m['sha256'], tiktok=sha(dst), ig=sha(ig), yt=sha(yt)))
    for v in [cfg['youtube_description'], *cfg['caption_overrides'].values(), cfg['pinned_comment']]:
        assert '—' not in v and '–' not in v
    assert len(cfg['pinned_comment']) < 180 and 'http' not in cfg['pinned_comment']
    (P/f'scripts/blotato/configs/{NAMES[s]}.json').write_text(json.dumps(cfg, indent=2, ensure_ascii=False)+'\n')
    # Facebook cover registry: repo copy (committed image) and the live installer copy.
    fbdir = P/'scripts/blotato/fb_covers'; fbdir.mkdir(exist_ok=True)
    fbimg = fbdir/f'{stem}-cover.png'; shutil.copy2(ig, fbimg)
    live = Path.home()/'.absbyai/fb-reel-covers'; (live/'covers').mkdir(parents=True, exist_ok=True)
    liveimg = live/'covers'/ig.name; shutil.copy2(ig, liveimg)
    row = dict(job=f'SL-20 short {n}', match=c['hook'], w=1080, h=1920, approved=(f"Dan picked on {pk['date']}: \"{pk['words']}\"" if pk.get("picked_by", "Dan") == "Dan" else f"{pk['date']}: {pk['words']}"),
               sha256=sha(ig), when=c['main'])
    for regp, img in [(P/'scripts/blotato/fb_reel_covers.json', fbimg), (live/'fb_reel_covers.json', liveimg)]:
        reg = json.loads(regp.read_text()); reg = [r for r in reg if r.get('match') != c['hook']]
        reg.append(dict(row, cover=str(img))); regp.write_text(json.dumps(reg, indent=1, ensure_ascii=False)+'\n')
    pk.update(config=f'scripts/blotato/configs/{NAMES[s]}.json', tiktok=str(dst), tiktok_sha256=sha(dst), tiktok_frames=res,
              audio_payload_identical=True, frame0=str(fr), uploads={k: state[f"{c['slug']}-{k}"] for k in urls})
    (A/'picks.json').write_text(json.dumps(picks, indent=2))
    print('ready', s, NAMES[s], flush=True)


for s in sys.argv[1:]:
    one(s)
