#!/usr/bin/env python3
"""RA-04 round 5: ONE real generation on the live absbyai.com with the white man's before photo, recorded at B0049's
size (1320x2868): a 1320x2868 viewport at DPR 1 with the page zoomed 3x lays out exactly like a 440x956 phone at DPR 3
(mean difference 3.5 levels on the landing page) and screencasts at full size, about 54 fps (a DPR 3 context screencasts
at 440 px wide in headless Chromium): upload -> Use Photo -> Male / Heavier / Ripped -> Generate -> the real loader
(CDP screencast, JPEG q92, timestamps kept) -> the result.

The result is rendered AFTER-ONLY by the app itself: a style injected before Generate hides the result screen's
"Your photo" column and the body-fat row, so the banned before/after pair is never drawn on any recorded frame
(ad-edit lesson 12 / VIDEO-RULES: never a side-by-side before/after). The chooser screen ("Which future you?") is
handled if it appears but never used in the cut. Saves the generated image full size for the lock-screen card.

Usage: python3 r5_record.py OUT_DIR BEFORE_PHOTO        (spend: one live generation, a few cents)
"""
import base64, json, os, shutil, sys, time
from playwright.sync_api import sync_playwright

OUT, PHOTO = sys.argv[1], sys.argv[2]
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(f'{OUT}/cast'); os.makedirs(f'{OUT}/shots')
W, H, DPR = 440, 956, 3      # the phone it lays out as
Z = 3                        # page zoom
HIDE_PAIR = """
#resultSection .before-after-grid { grid-template-columns: 1fr !important; }
#resultSection .before-after-grid > div:first-child { display: none !important; }
#resultSection .bodyfat-row, #bodyfatNote { display: none !important; }
#resultSection .ba-img { height: 480px !important; }
"""
log, cast = [], []
with sync_playwright() as pw:
    b = pw.chromium.launch(args=['--headless=new'])
    ua = pw.devices['iPhone 15 Pro Max']['user_agent']
    ctx = b.new_context(viewport={'width': W * Z, 'height': H * Z}, device_scale_factor=1, has_touch=True,
                        user_agent=ua, locale='en-US', timezone_id='America/Chicago', color_scheme='light')
    page = ctx.new_page(); T0 = time.time()

    def shot(tag):
        p = f'{OUT}/shots/{len(log):03d}_{tag}.png'; page.screenshot(path=p)
        log.append(dict(tag=tag, t=round(time.time() - T0, 3), path=p)); return p

    page.goto('https://absbyai.com/', wait_until='networkidle', timeout=60000); page.wait_for_timeout(1000)
    shot('landing')
    page.add_style_tag(content=f'html {{ zoom: {Z}; }}' + HIDE_PAIR); page.wait_for_timeout(600)
    cdp = ctx.new_cdp_session(page)

    def on_frame(ev):
        i = len(cast)
        open(f"{OUT}/cast/{i:05d}.jpg", 'wb').write(base64.b64decode(ev['data']))
        cast.append(dict(i=i, t=ev['metadata']['timestamp'], scroll=ev['metadata'].get('scrollOffsetY')))
        try: cdp.send('Page.screencastFrameAck', {'sessionId': ev['sessionId']})
        except Exception: pass
    cdp.on('Page.screencastFrame', on_frame)
    cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 92, 'maxWidth': W * DPR, 'maxHeight': H * DPR,
                                      'everyNthFrame': 1})
    marks = {}
    def mark(k): marks[k] = time.time(); print(f'{k} at {time.time() - T0:.2f} s, frames {len(cast)}', flush=True)

    page.set_input_files('#photoInput', PHOTO); page.wait_for_timeout(1500); mark('uploaded'); shot('crop')
    try:
        page.click('#cropConfirmBtn', timeout=8000); page.wait_for_timeout(1200)
    except Exception as e: print('no crop screen:', str(e)[:80])
    mark('photo_in'); shot('photo_in')
    for label in ('Male', 'Heavier', 'Ripped'):
        try: page.get_by_text(label, exact=True).first.click(timeout=4000); page.wait_for_timeout(450)
        except Exception as e: print('option', label, 'not clicked:', str(e)[:60])
    page.evaluate("() => document.getElementById('generateBtn').scrollIntoView({block:'center', behavior:'smooth'})")
    page.wait_for_timeout(900); shot('options')
    print('generate enabled:', page.evaluate("() => !document.getElementById('generateBtn').disabled"))
    mark('generate_click'); page.click('#generateBtn')
    page.wait_for_timeout(700)
    page.evaluate("() => { const l = document.getElementById('genLoader'); if (l) l.scrollIntoView({block:'center', behavior:'smooth'}); }")
    done = chooser = False; err = None
    while time.time() - marks['generate_click'] < 180:
        page.wait_for_timeout(200)
        st = page.evaluate("""() => ({res: getComputedStyle(document.getElementById('resultSection')).display,
            ch: getComputedStyle(document.getElementById('chooserSection')).display,
            err: ((document.getElementById('errorSection')||{}).innerText||'').trim()})""")
        if st['res'] != 'none': done = True; break
        if st['ch'] != 'none': chooser = True; break
        if st['err']: err = st['err']; print('error shown:', err[:160]); break
    mark('loader_end')
    if chooser:
        page.wait_for_timeout(1500); shot('chooser_RECORD_ONLY')
        page.locator('.chooser-keep-btn').first.click(timeout=8000)
        for _ in range(100):
            page.wait_for_timeout(200)
            if page.evaluate("() => getComputedStyle(document.getElementById('resultSection')).display") != 'none':
                done = True; break
        mark('chooser_kept')
    page.wait_for_timeout(4000); mark('result_settled')
    cdp.send('Page.stopScreencast')
    shot('result_after_only')
    state = page.evaluate("""() => ({lock: getComputedStyle(document.getElementById('afterLockOverlay')).display,
        pay: getComputedStyle(document.getElementById('paywallSection')).display,
        beforeVisible: (() => { const e = document.getElementById('beforeImg'); return !!(e && e.offsetParent); })(),
        weak: getComputedStyle(document.getElementById('weakChangeNudge')).display,
        src: (document.getElementById('afterImg').src || '').slice(0, 80)})""")
    print('result state:', state)
    src = page.evaluate("() => document.getElementById('afterImg').src")
    if src.startswith('data:'):
        data = src
    else:
        data = page.evaluate("""async (u) => { const r = await fetch(u); const bl = await r.blob();
            return await new Promise(res => { const fr = new FileReader(); fr.onload = () => res(fr.result); fr.readAsDataURL(bl); }); }""", src)
    ext = 'jpg' if 'jpeg' in data[:30] else ('webp' if 'webp' in data[:30] else 'png')
    open(f'{OUT}/after_generated.{ext}', 'wb').write(base64.b64decode(data.split(',', 1)[1]))
    json.dump(dict(shots=log, cast=cast, marks={k: v - T0 for k, v in marks.items()}, T0=T0, done=done,
                   chooser=chooser, err=err, state=state, viewport=[W, H, DPR], url='https://absbyai.com/',
                   photo=PHOTO), open(f'{OUT}/log.json', 'w'), indent=1)
    b.close()
print('DONE', len(log), 'shots,', len(cast), 'screencast frames; result', done, 'chooser', chooser)
