"""Round 6: capture the app's own screens at phone size from a LOCAL copy of the app (launch config abs-by-ai: in-memory database, admin test account
hub@local.test from .claude/launch.json; nothing touches production, no real account). usage: appcap6.py [port]"""
import sys, secrets, json
from playwright.sync_api import sync_playwright
OUT = "/Volumes/Extreme/_edit_work/ro06/round6/phone/cap"; port = sys.argv[1] if len(sys.argv) > 1 else "3000"
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    cx = b.new_context(viewport=dict(width=390, height=844), device_scale_factor=3, is_mobile=True, has_touch=True,
                       user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1")
    pg = cx.new_page(); pg.goto(f"http://localhost:{port}/", wait_until="networkidle")
    pw = secrets.token_urlsafe(12)
    r = pg.evaluate("""async (pw) => { let d; try { d = await authApi('/api/auth/signup', {method:'POST', body: JSON.stringify({email:'hub@local.test', password: pw, deviceId: (typeof getDeviceId==='function'?getDeviceId():'dev-ro06-cap')})}); } catch(e) { return 'ERR '+e.message; }
        setLoggedIn(d); await refreshMembership(); showHub(); return [typeof hasMemberAccess==='function' && hasMemberAccess(), document.getElementById('hubSection').style.display]; }""", pw)
    print("signup:", r); pg.wait_for_timeout(1500)
    # the test account's empty states are not what a member's home looks like: the sign-in line, the empty "Today's brief" card and the join tile are hidden; every feature tile is the app's own
    pg.evaluate("""() => { document.getElementById('hubEmail').style.display='none'; for (const e of document.querySelectorAll('#hubSection .hub-tile')) if (/Become a member/.test(e.innerText)) e.style.display='none';
        const b = [...document.querySelectorAll('#hubSection *')].find(e => /TODAY.S BRIEF/i.test(e.innerText || '') && e.children.length && e.getBoundingClientRect().height < 520 && e.getBoundingClientRect().height > 200); if (b) b.style.display='none'; window.scrollTo(0,0); }""")
    pg.wait_for_timeout(400); pg.screenshot(path=f"{OUT}/hub.png")
    tiles = pg.evaluate("""() => [...document.querySelectorAll('#hubSection .hub-tile')].filter(e => e.offsetParent).map(e => { const r = e.getBoundingClientRect(); return [e.innerText.split(String.fromCharCode(10)).filter(x => x.trim()).join(' | ').slice(0,60), Math.round(r.x), Math.round(r.y + scrollY), Math.round(r.width), Math.round(r.height)]; })""")
    json.dump(tiles, open(f"{OUT}/hub_tiles.json", "w"), indent=1); print(tiles)
    for ex in ("pushup", "reverse-crunch"):
        pg.evaluate("(ex) => { openExerciseSheet(ex, '', ''); }", ex); pg.wait_for_timeout(1200)
        pg.evaluate("() => { const v = document.getElementById('exSheetDemo'); if (v) v.removeAttribute('controls'); }"); pg.wait_for_timeout(300)
        pg.screenshot(path=f"{OUT}/sheet_{ex}.png")
        box = pg.evaluate("""() => { const v = document.getElementById('exSheetDemo'); if (!v) return null; const r = v.getBoundingClientRect(); const c = document.querySelector('.ex-demo-box .ex-ai-chip'); const q = c ? c.getBoundingClientRect() : null; return {video:[r.x, r.y, r.width, r.height], radius: getComputedStyle(v).borderRadius, chip: q ? [q.x, q.y, q.width, q.height] : null}; }""")
        json.dump(box, open(f"{OUT}/sheet_{ex}.json", "w")); print(ex, box)
        pg.evaluate("""() => { const x = [...document.querySelectorAll('button')].find(b => b.offsetParent && /close/i.test(b.getAttribute('aria-label') || b.className || '')); if (x) x.click(); else document.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape'})); }"""); pg.wait_for_timeout(500)
    b.close()
