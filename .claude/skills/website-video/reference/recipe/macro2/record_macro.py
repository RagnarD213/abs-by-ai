#!/usr/bin/env python3
"""Record the REAL Macro Tracker on absbyai.com (public page, no account) with the salmon-plate photo the Ad 2
vertical session used (Pexels 3490368), at the PiP's exact aspect: viewport 390x738 CSS at DPR 3 = 1170x2214 ->
433x820 in the phone box. States captured as screenshots + timestamps (shots.json), plus FULL-PAGE screenshots of
the result and the logged states so the list scroll can be animated smoothly by build_macro_pip.py.
One real analysis call on production (a few cents), no account, no deviceId."""
import json, os, time, shutil
from playwright.sync_api import sync_playwright
OUT='shots'; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
PHOTO=os.path.abspath('meal_photo.jpg'); log=[]; n=[0]; T0=[time.time()]
def shot(page, tag, full=False):
    n[0]+=1; p=f'{OUT}/{n[0]:03d}_{tag}.png'; page.screenshot(path=p, full_page=full)
    log.append(dict(i=n[0], tag=tag, t=round(time.time()-T0[0],3), path=p, full=full)); return p
with sync_playwright() as pw:
    b=pw.chromium.launch()
    dev=dict(pw.devices['iPhone 13']); dev['viewport']={'width':390,'height':738}
    ctx=b.new_context(**dev, locale='en-US', timezone_id='America/Chicago', color_scheme='light')
    page=ctx.new_page()
    page.goto('https://absbyai.com/', wait_until='networkidle', timeout=60000); T0[0]=time.time()
    page.wait_for_timeout(800)
    opened=page.evaluate("""() => { try { if (typeof showMacroScreen === 'function') { showMacroScreen(); return 'showMacroScreen'; }
                                        if (typeof showScreen === 'function') { showScreen('macro'); return 'showScreen'; } } catch(e) { return 'err:'+e.message } return 'none'; }""")
    print('opened via', opened); page.wait_for_timeout(700)
    # scroll so the "Track Your Macros With AI" heading sits at the top (the account link above it is not part of the feature)
    ytop=page.evaluate("""() => { const els=[...document.querySelectorAll('#macroSection h1, #macroSection h2, #macroSection .hero-h1')];
        const h=els.find(e=>/Track Your Macros/i.test(e.textContent)); if(!h) return 0; const r=h.getBoundingClientRect(); return Math.max(0, r.top + window.scrollY - 14); }""")
    print('heading y', ytop); page.evaluate(f"() => window.scrollTo(0,{ytop})"); page.wait_for_timeout(400)
    shot(page,'tracker_empty')
    page.set_input_files('#mealPhotoInput', PHOTO); page.wait_for_timeout(1200)
    page.evaluate(f"() => window.scrollTo(0,{ytop})"); page.wait_for_timeout(300)
    shot(page,'photo_loaded'); shot(page,'photo_loaded_full', full=True)
    # bring the Analyze button into view (it sits under the photo card)
    page.evaluate("() => document.getElementById('mealAnalyzeBtn').scrollIntoView({block:'center'})"); page.wait_for_timeout(350)
    shot(page,'photo_analyzebtn')
    page.click('#mealAnalyzeBtn'); t_click=time.time(); done=False
    while time.time()-t_click<150:
        shot(page,'analyzing')
        st=page.evaluate("() => ({log: getComputedStyle(document.getElementById('mealLogBtn')).display})")
        if st['log']!='none': done=True; break
        page.wait_for_timeout(300)
    print('result after', round(time.time()-t_click,1),'s; done',done); page.wait_for_timeout(700)
    shot(page,'result_full', full=True); shot(page,'result_view')
    page.evaluate("() => document.getElementById('mealLogBtn').scrollIntoView({block:'center'})"); page.wait_for_timeout(400)
    shot(page,'result_logbtn')
    page.click('#mealLogBtn'); page.wait_for_timeout(250); shot(page,'logged_a'); page.wait_for_timeout(700); shot(page,'logged_b')
    shot(page,'logged_full', full=True)
    txt=page.evaluate("() => (document.getElementById('mealLogSuccess')||{}).innerText || ''"); print('log success text:', repr(txt[:90]))
    tot=page.evaluate("() => (document.getElementById('dailyTotalsValues')||{}).innerText || ''"); print('daily totals:', tot)
    json.dump(log, open('shots.json','w'), indent=1); b.close()
print(len(log),'screenshots')
