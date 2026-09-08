#!/usr/bin/env python3
"""Record the REAL Macro Tracker on absbyai.com with the new meal photo (Playwright, iPhone emulation, dpr 3):
photo in -> Analyze Meal -> itemized calories -> Log Meal -> 'logged'. Screenshots with timestamps go to
rev/meal/shots/; the clip is assembled from them by build_meal_clip.py."""
import json, os, time, shutil
from playwright.sync_api import sync_playwright
OUT = 'rev/meal/shots'; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
PHOTO = os.path.abspath('rev/meal/meal_photo.jpg')
log = []; n = [0]
def shot(page, tag):
    n[0] += 1; p = f'{OUT}/{n[0]:03d}_{tag}.png'; page.screenshot(path=p); log.append(dict(i=n[0], tag=tag, t=round(time.time()-T0, 3), path=p)); return p
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(**pw.devices['iPhone 13'], locale='en-US', timezone_id='America/Chicago', color_scheme='light')
    page = ctx.new_page()
    page.goto('https://absbyai.com/', wait_until='networkidle', timeout=60000)
    T0 = time.time()
    page.wait_for_timeout(800)
    opened = page.evaluate("""() => { try { if (typeof showMacroScreen === 'function') { showMacroScreen(); return 'showMacroScreen'; }
                                        if (typeof showScreen === 'function') { showScreen('macro'); return 'showScreen'; } } catch(e) { return 'err:'+e.message } return 'none'; }""")
    print('opened via', opened)
    page.wait_for_timeout(700)
    vis = page.evaluate("() => { const s=document.getElementById('macroSection'); return s ? getComputedStyle(s).display : 'missing' }")
    print('macroSection display:', vis)
    shot(page, 'tracker_empty')
    page.set_input_files('#mealPhotoInput', PHOTO)
    page.wait_for_timeout(1200)
    shot(page, 'photo_loaded')
    enabled = page.evaluate("() => !document.getElementById('mealAnalyzeBtn').disabled")
    print('Analyze enabled:', enabled)
    page.click('#mealAnalyzeBtn')
    t_click = time.time()
    # burst while analyzing
    done = False
    while time.time() - t_click < 150:
        shot(page, 'analyzing')
        st = page.evaluate("() => ({log: getComputedStyle(document.getElementById('mealLogBtn')).display, btn: document.getElementById('mealAnalyzeBtn').disabled})")
        if st['log'] != 'none': done = True; break
        page.wait_for_timeout(350)
    print('result after', round(time.time()-t_click, 1), 's; done', done)
    page.wait_for_timeout(600)
    shot(page, 'result_top')
    # scroll the itemized result into view in a few steps (screenshots along the way)
    for k in range(1, 5):
        page.evaluate(f"() => window.scrollBy(0, {220})"); page.wait_for_timeout(350); shot(page, f'result_scroll{k}')
    page.evaluate("() => document.getElementById('mealLogBtn').scrollIntoView({block:'center'})"); page.wait_for_timeout(400)
    shot(page, 'result_logbtn')
    page.click('#mealLogBtn'); page.wait_for_timeout(250); shot(page, 'logged_a'); page.wait_for_timeout(500); shot(page, 'logged_b')
    page.evaluate("() => window.scrollBy(0, -200)"); page.wait_for_timeout(400); shot(page, 'logged_c')
    txt = page.evaluate("() => (document.getElementById('mealLogSuccess')||{}).innerText || ''")
    print('log success text:', repr(txt[:80]))
    tot = page.evaluate("() => (document.getElementById('dailyTotalsValues')||{}).innerText || ''"); print('daily totals:', tot)
    json.dump(log, open('rev/meal/shots.json', 'w'), indent=1)
    b.close()
print(len(log), 'screenshots')
