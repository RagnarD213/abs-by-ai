#!/usr/bin/env python3
"""Muhammad Shorts Batch B (DS-06, DS-10, DS-13), organic dedicated Shorts, setup 2026-10-27.
Dan picked A for all three. DS-13 A is unrevised; DS-06 A and DS-10 A were revised (A-r2) and need his OK on the exact
files before this runs for them (VIDEO-RULES, "Revised covers and thumbnails: show Dan before installing").

Per Short, each step skipped when already done:
  1. lock the picked covers (Instagram PNG, YouTube JPEG under 2 MB) into covers/approved-muhammad-batch-b/
  2. TikTok cover-first copy (the Instagram cover as frame 0), frame and audio packets verified
  3. upload master, TikTok copy and both covers to Blotato, hash-check each re-hosted file
  4. write scripts/blotato/configs/<slug>.json, the Facebook cover registry (repo + live) and the shared waiting list

    python3 scripts/blotato/muhammad_shorts/batch_b_setup.py ds13 [ds06 ds10]
State: /Volumes/Expansion/_edit_work/muhammad-batch-b-publish/{manifest,uploads}.json"""
import hashlib, io, json, os, shutil, subprocess, sys, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
from PIL import Image
import tiktok_cover
from danrosefit_migration import api_key, call
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
UP = '/Volumes/Expansion/_edit_work/muhammad-batch-b-publish'
REV = os.path.join(ROOT, 'Short-form video content/covers/review/muhammad-batch-b-20261026')
APP = os.path.join(ROOT, 'Short-form video content/covers/approved-muhammad-batch-b')
CAP = json.load(open(os.path.join(ROOT, 'scripts/covers/muhammad-batch-b-20261026/captions.json')))
S = 'Short-form video content'
V = {
    'ds06': dict(job='DS-06', pick='A-r2', cfg='ds06-what-every-body-fat-percentage-looks-like', main='2027-01-14T15:00:00.000Z',
                 slug='ds-06_what-every-body-fat-percentage-looks-like',
                 video=f'{S}/What Every Body Fat Percentage Looks Like - DS-06/What Every Body Fat Percentage Looks Like | muhammad | 9x16 | V4 HD.mp4'),
    'ds10': dict(job='DS-10', pick='A-r2', cfg='ds10-top-3-non-weight-loss-benefits-of-zepbound', main='2027-01-21T15:00:00.000Z',
                 slug='ds-10_3-unexpected-ways-zepbound-helped-me',
                 video=f'{S}/3 Unexpected Ways Zepbound Helped Me - DS-10/3 Unexpected Ways Zepbound Helped Me | muhammad | 9x16 | V3 HD.mp4'),
    'ds13': dict(job='DS-13', pick='A', cfg='ds13-the-1-change-i-made-to-get-abs-at-40', main='2027-01-07T15:00:00.000Z',
                 slug='ds-13_the-1-change-i-made-to-get-abs-at-40',
                 video=f'{S}/The 1 Change I Made To Get Abs At 40 - DS-13/The 1 Change I Made To Get Abs At 40 | muhammad | 9x16 | V3 HD.mp4'),
}
sha = lambda b: hashlib.sha256(b).hexdigest(); fsha = lambda p: sha(open(p, 'rb').read())
FP = os.path.join(ROOT, 'Media/video_edit/bin/ffprobe')

def packets(f, s):
    return int(subprocess.run([FP, '-v', 'error', '-select_streams', s, '-count_packets', '-show_entries', 'stream=nb_read_packets',
                               '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip())

def run(k):
    v = V[k]; c = CAP[k]; os.makedirs(APP, exist_ok=True)
    video = os.path.join(ROOT, v['video']); pick = v['pick']
    # 1. lock covers
    ig = os.path.join(APP, f"Instagram_{v['slug']}_cover-{pick}.png"); yt = os.path.join(APP, f"YouTube_{v['slug']}_cover-{pick}.jpg")
    shutil.copyfile(os.path.join(REV, k, 'instagram', f"{v['slug']}_cover-{pick}.png"), ig)
    shutil.copyfile(os.path.join(REV, k, 'youtube', f"{v['slug']}_cover-{pick}.jpg"), yt)
    assert os.path.getsize(yt) < 2_000_000 and Image.open(yt).size == (1080, 1920)
    # 2. TikTok cover-first copy
    mp = os.path.join(UP, 'manifest.json'); man = json.load(open(mp)) if os.path.exists(mp) else {}
    tt = os.path.join(UP, f"{v['slug']}_tiktok-coverfirst.mp4")
    if not os.path.exists(tt) or man.get(k, {}).get('ig_cover_sha256') != fsha(ig):
        print(k, 'tiktok build', tiktok_cover.build(video, ig, tt))
        ver = dict(frames_src=packets(video, 'v:0'), frames_out=packets(tt, 'v:0'), audio_src=packets(video, 'a:0'), audio_out=packets(tt, 'a:0'))
        ver['ok'] = ver['frames_out'] == ver['frames_src']+1 and ver['audio_out'] == ver['audio_src']; assert ver['ok'], ver
        man[k] = dict(video=video, video_sha256=fsha(video), tiktok=tt, ig_cover=ig, ig_cover_sha256=fsha(ig), yt_cover=yt, pick=pick, verify=ver)
        json.dump(man, open(mp, 'w'), indent=1); print(k, 'tiktok verified', ver)
    # 3. uploads
    sp = os.path.join(UP, 'uploads.json'); st = json.load(open(sp)) if os.path.exists(sp) else {}
    key = api_key(); CT = {'.mp4': 'video/mp4', '.png': 'image/png', '.jpg': 'image/jpeg'}
    for f in ('video', 'tiktok', 'ig_cover', 'yt_cover'):
        path = man[k][f]; data = open(path, 'rb').read()
        if st.get(f'{k}:{f}', {}).get('sha256') == sha(data): continue
        ext = os.path.splitext(path)[1]; r = call('POST', '/media/uploads', key, {'filename': f'{k}-{f}{ext}'})
        urllib.request.urlopen(urllib.request.Request(r['presignedUrl'], data=data, method='PUT', headers={'Content-Type': CT[ext]})).read()
        back = urllib.request.urlopen(r['publicUrl']).read(); assert sha(back) == sha(data), f'{k}:{f} re-hosted bytes differ'
        st[f'{k}:{f}'] = dict(url=r['publicUrl'], sha256=sha(data), bytes=len(data)); json.dump(st, open(sp, 'w'), indent=1)
        print(k, 'uploaded', f, len(data), flush=True)
    U = lambda f: st[f'{k}:{f}']['url']
    # 4. config
    link = f"https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign={c['campaign']}&utm_content={v['cfg']}"
    cfg = {'content_type': 'organic', 'source': video, 'title': c['title'], 'slug': v['cfg'], 'campaign': c['campaign'],
           'video_url': U('video'), 'tiktok_video_url': U('tiktok'), 'instagram_cover_url': U('ig_cover'), 'youtube_cover_url': U('yt_cover'),
           'main': v['main'], 'keyword': c['keyword'], 'ai_generated': c['ai'], 'hook': c['hook'], 'body': c['body'], 'close': c['close'],
           'tags': c['tags'],
           'youtube_description': f"{c['hook']}\n\nTry your free Abs By AI preview: {link}\n\n{c['points']}\n\n{c['close']}\n\n{c['yt_tags']}",
           'pinned_comment': c['pinned'], 'cover_pick': pick, 'cover_ig_sha256': fsha(ig), 'cover_yt_sha256': fsha(yt)}
    for t in [cfg['title'], cfg['hook'], cfg['body'], cfg['close'], cfg['youtube_description'], cfg['pinned_comment']]:
        assert '—' not in t and '–' not in t
    cp = os.path.join(ROOT, f"scripts/blotato/configs/{v['cfg']}.json"); json.dump(cfg, open(cp, 'w'), indent=1); open(cp, 'a').write('\n')
    # Facebook cover registry: repo copy and live installer copy
    note = f"Dan picked cover {pick} (2026-10-27); Thu {v['main'][:10]} 9 AM Central, all four."
    for reg, cdir in [(os.path.join(ROOT, 'scripts/blotato/fb_reel_covers.json'), os.path.join(ROOT, 'scripts/blotato/fb_covers')),
                      (os.path.expanduser('~/.absbyai/fb-reel-covers/fb_reel_covers.json'), os.path.expanduser('~/.absbyai/fb-reel-covers/covers'))]:
        dst = os.path.join(cdir, f"{v['cfg']}-approved.png"); shutil.copyfile(ig, dst)
        R = json.load(open(reg)); R = [e for e in R if e.get('job') != v['job']]
        R.append(dict(job=v['job'], match=c['hook'], cover=dst, w=1080, h=1920, approved=note, when=v['main']))
        json.dump(R, open(reg, "w"), indent=2)
    # shared waiting list
    wp = os.path.join(ROOT, 'scripts/blotato/video_waitlist.json'); WL = json.load(open(wp))
    rel = f"scripts/blotato/configs/{v['cfg']}.json"
    if not any(e['config'] == rel for e in WL):
        WL.append(dict(config=rel, kind='short', job=v['job'], label=c['title'], added='2026-10-27',
                       note=f"Muhammad HD = approved cut. Cover {pick}. Target Thu {v['main'][:10]}, 9 AM America/Chicago. Four media uploads hash-checked."))
        json.dump(WL, open(wp, 'w'), indent=1)
    print(k, 'config', rel, 'ready')

if __name__ == '__main__':
    for k in sys.argv[1:]:
        run(k)
