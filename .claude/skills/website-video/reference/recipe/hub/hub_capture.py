#!/usr/bin/env python3
"""Capture the logged-in MEMBER HOME of the real app for the members-home scroll PiP (Dan, rev 3 review: "slowly
scroll through the app members' home screen so they can see all the different features available").

Runs against a LOCAL copy of the site (node server.js with DATABASE_URL=pgmem://local -- an in-memory throwaway DB), so
no real account is touched: the script creates a local admin fixture, grants a complimentary membership to a local
'dan@absbyai.com' fixture through the app's own admin endpoint, and loads the hub through the app's normal auth path.
The hub hero (before/after side by side) does not render because the fixture has no transformation -- lesson 45 / Step 4
(never before+after together, not even inside real app UI). The membership card ("Beta tester", the comp wording), the
member FAQ and the Daily Brief card (needs the live AI) are hidden for the capture; every feature tile is real.
Viewport 390x738 CSS at DPR 3 = 1170x2214 -> 433x820 in the phone box (exact aspect).
  python3 hub_capture.py http://localhost:PORT
"""
import json, os, secrets, sys, urllib.request
from playwright.sync_api import sync_playwright
BASE=sys.argv[1].rstrip("/"); OUT=os.path.dirname(os.path.abspath(__file__))
def api(path, body, token=None):
    req=urllib.request.Request(BASE+path, data=json.dumps(body).encode(), headers={"Content-Type":"application/json", **({"Authorization":f"Bearer {token}"} if token else {})})
    with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read())
admin_pw=secrets.token_urlsafe(12); member_pw=secrets.token_urlsafe(12)
api("/api/auth/signup", {"email":"hub@local.test","password":admin_pw,"deviceId":"fixture-admin"})
adm=api("/api/auth/login", {"email":"hub@local.test","password":admin_pw,"deviceId":"fixture-admin"})
print("admin fixture ok")
r=api("/api/admin/beta-members", {"email":"dan@absbyai.com","password":member_pw}, adm["token"]); print("member fixture", r)
mem=api("/api/auth/login", {"email":"dan@absbyai.com","password":member_pw,"deviceId":"fixture-member"})
with sync_playwright() as pw:
    b=pw.chromium.launch()
    dev=dict(pw.devices['iPhone 13']); dev['viewport']={'width':390,'height':738}
    ctx=b.new_context(**dev, locale='en-US', timezone_id='America/Chicago', color_scheme='light')
    ctx.add_init_script(f"localStorage.setItem('absbyai_session_token', {json.dumps(mem['token'])}); localStorage.setItem('absbyai_account_email', 'dan@absbyai.com');")
    page=ctx.new_page(); page.goto(BASE+"/", wait_until="networkidle", timeout=60000)
    page.wait_for_selector("#hubSection", state="visible", timeout=30000); page.wait_for_timeout(1500)
    state=page.evaluate("""() => { const vis=e=>e && getComputedStyle(e).display!=='none';
        for (const id of ['hubMembershipCard','hubMemberFaq','hubBriefCard','hubPreviewNote','hubPreviewAppNote','hubSoonNote']) { const e=document.getElementById(id); if(e) e.style.display='none'; }
        const tiles=[...document.querySelectorAll('#hubSection .hub-tile')].filter(vis).map(t=>(t.querySelector('.hub-tile-name')||t).textContent.trim());
        return {hero: vis(document.getElementById('hubHeroWrap')), tiles, title: document.getElementById('hubWelcomeTitle').textContent, email: document.getElementById('hubEmail').textContent,
                h: document.documentElement.scrollHeight}; }""")
    print(json.dumps(state, indent=1)); page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/hub_view.png"); page.screenshot(path=f"{OUT}/hub_full.png", full_page=True)
    json.dump(state, open(f"{OUT}/hub_state.json","w"), indent=1); b.close()
print("hub_view.png + hub_full.png written")
