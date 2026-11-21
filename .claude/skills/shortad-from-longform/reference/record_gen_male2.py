#!/usr/bin/env python3
"""A REAL generation on absbyai.com with the other person's photo (asset library male2-before), recorded
from the live page: upload -> Use Photo -> options -> Generate -> the real scanning loader (CDP screencast,
~20-30 fps) -> the result. The result screen is captured twice: as the app shows it (before/after pair --
for the record only, never used in an ad) and AFTER-ONLY, produced by hiding the before column and the
body-fat row in the live DOM so the app's own rendering makes the compliant screen. Frames -> rev/gen2/."""
import base64, json, os, shutil, time
from playwright.sync_api import sync_playwright
OUT = 'rev/gen2'; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(f'{OUT}/cast'); os.makedirs(f'{OUT}/shots')
PHOTO = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/01 Before and After Images/male2-before.webp"
log = []; cast = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(**pw.devices['iPhone 13'], locale='en-US', timezone_id='America/Chicago', color_scheme='light')
    page = ctx.new_page(); T0 = time.time()
    def shot(tag):
        p = f'{OUT}/shots/{len(log):03d}_{tag}.png'; page.screenshot(path=p); log.append(dict(tag=tag, t=round(time.time()-T0,3), path=p)); return p
    page.goto('https://absbyai.com/', wait_until='networkidle', timeout=60000); page.wait_for_timeout(800)
    shot('landing')
    page.set_input_files('#photoInput', PHOTO); page.wait_for_timeout(1500); shot('crop')
    try:
        page.click('#cropConfirmBtn', timeout=8000); page.wait_for_timeout(1200)
    except Exception as e: print('no crop screen:', str(e)[:80])
    shot('photo_in')
    for label in ('Male', 'Heavier', 'Dramatic'):
        try: page.get_by_text(label, exact=True).first.click(timeout=4000); page.wait_for_timeout(300)
        except Exception as e: print('option', label, 'not clicked:', str(e)[:60])
    page.evaluate("() => document.getElementById('generateBtn').scrollIntoView({block:'center'})"); page.wait_for_timeout(400)
    shot('options')
    print('generate enabled:', page.evaluate("() => !document.getElementById('generateBtn').disabled"))
    # ---- screencast during the real loader
    cdp = ctx.new_cdp_session(page)
    # force the screencast to device pixels (run 2 came back at 390x664 CSS px)
    cdp.send('Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 664, 'deviceScaleFactor': 3, 'mobile': True})
    def on_frame(ev):
        cast.append(dict(t=ev['metadata']['timestamp'], i=len(cast)))
        open(f"{OUT}/cast/{len(cast)-1:05d}.png", 'wb').write(base64.b64decode(ev['data']))
        try: cdp.send('Page.screencastFrameAck', {'sessionId': ev['sessionId']})
        except Exception: pass
    cdp.on('Page.screencastFrame', on_frame)
    cdp.send('Page.startScreencast', {'format': 'png', 'maxWidth': 1170, 'maxHeight': 1992, 'everyNthFrame': 1})
    page.click('#generateBtn'); t_click = time.time()
    done = False; chooser = False; t_loader_end = None
    while time.time() - t_click < 150:
        page.wait_for_timeout(250)
        st = page.evaluate("() => ({res: getComputedStyle(document.getElementById('resultSection')).display, chooser: document.body.innerText.includes('Which future you?'), err: (document.getElementById('errorSection')||{}).innerText})")
        if st['res'] != 'none': done = True; break
        if st['chooser']: chooser = True; break
        if st['err']: print('error shown:', st['err'][:120]); break
    t_loader_end = time.time() - T0
    cdp.send('Page.stopScreencast')
    print(f'loader ended after {time.time()-t_click:.1f} s; result {done} chooser {chooser}; screencast frames {len(cast)}')
    if chooser:
        page.wait_for_timeout(1200); shot('chooser_RECORD_ONLY')
        page.get_by_text('Keep this one', exact=True).first.click(timeout=8000)
        for _ in range(60):
            page.wait_for_timeout(250)
            if page.evaluate("() => getComputedStyle(document.getElementById('resultSection')).display") != 'none': done = True; break
    print('result screen shown:', done)
    page.wait_for_timeout(1500); shot('result_pair_RECORD_ONLY')
    lock = page.evaluate("() => ({lock: getComputedStyle(document.getElementById('afterLockOverlay')).display, pay: getComputedStyle(document.getElementById('paywallSection')).display, src: (document.getElementById('afterImg').src||'').slice(0,60), bf: (document.getElementById('bfAfter')||{}).innerText})")
    print('after lock/paywall/src/bf:', lock)
    # after-only: the app's own rendering with the before column and the body-fat row hidden
    page.evaluate("""() => {
        const g = document.querySelector('.before-after-grid'); g.style.gridTemplateColumns = '1fr';
        const before = document.getElementById('beforeImg').parentElement; before.style.display = 'none';
        document.querySelector('.bodyfat-row').style.display = 'none';
        const n = document.getElementById('bodyfatNote'); if (n) n.style.display = 'none';
        window.scrollTo(0, 0);
    }""")
    page.wait_for_timeout(600); shot('result_after_only')
    page.evaluate("() => document.getElementById('loveItBtn').scrollIntoView({block:'end'})"); page.wait_for_timeout(400); shot('result_after_only_btn')
    # the generated image itself, full size
    src = page.evaluate("() => document.getElementById('afterImg').src")
    if src.startswith('data:'):
        open(f'{OUT}/after_generated.png', 'wb').write(base64.b64decode(src.split(',',1)[1]))
    else:
        data = page.evaluate("async (u) => { const r = await fetch(u); const b = await r.blob(); return await new Promise(res => { const fr = new FileReader(); fr.onload = () => res(fr.result); fr.readAsDataURL(b); }); }", src)
        open(f'{OUT}/after_generated.png', 'wb').write(base64.b64decode(data.split(',',1)[1]))
    json.dump(dict(shots=log, cast=cast, t_click=t_click - T0, t_loader_end=t_loader_end, T0=T0), open(f'{OUT}/log.json','w'), indent=1)
    b.close()
print(len(log), 'shots,', len(cast), 'screencast frames')
