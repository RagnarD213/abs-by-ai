#!/usr/bin/env python3
"""REV 6 item 4 -- capture the REAL AI Trainer program for the NUM2 phone PiP (Dan: "scrolling through the workout
program ... only scrolling through a few exercises slowly, where we have the AI demos right there. Don't show any of
the stick figures ... just a little bit of the text showing it's customized").

Same fixture recipe as hub/hub_capture.py (ad-edit lesson 113): LOCAL server, pgmem DB, fixture admin + comp member,
session token in localStorage before load -- never a real login. The program is SEEDED into localStorage
(absbyai_trainer_program, the app's own storage key -- the client renders from it and the server sync only overwrites
when the server has a program, which the fixture does not). Every exercise in it is one of the 33 ids with a live demo
in public/exercise-demos/, so no sheet can ever fall back to the stick-figure SVG; the stick figures on the day-view
cards are switched off for the capture by replacing getExerciseAnim in the page (fixture-only, nothing ships).
Viewport 390x738 CSS at DPR 3 = 1170x2214 -> 433x820 in the phone box (lesson 114).
Writes: day_view.png, day_full.png, sheet_<id>.png + sheet_<id>.json {rect (px), poster}, trainer_state.json.
  python3 trainer_capture.py http://localhost:3000
"""
import json, os, secrets, sys, urllib.request
from playwright.sync_api import sync_playwright
BASE=sys.argv[1].rstrip("/"); OUT=os.path.dirname(os.path.abspath(__file__))
DEMO_OK={'bird-dog','cable-tricep-pushdown','db-bench-press','db-goblet-squat','db-rdl','db-row','dead-bug','face-pull','incline-pushup','leg-press','plank','pushup','reverse-lunge','side-plank','wall-sit','hollow-hold','knee-pushup','pike-pushup','chair-dip','split-squat','glute-bridge','calf-raise','crunch','lying-leg-raise','superman','pullup','lat-pulldown','seated-cable-row','leg-extension','leg-curl','db-shoulder-press','db-curl','db-lateral-raise'}
SHEETS=["db-goblet-squat","pushup","plank"]
def ex(id_,sets,reps,rest,cue): return {"exercise_id":id_,"sets":sets,"reps":reps,"rest_sec":rest,"cue":cue,"common_mistake":""}
def day(n,focus,main,abs_):
    return {"day":n,"focus":focus,"warmup":[],"main":main,"abs_finisher":abs_}
W1=[day(1,"Total-body — upper + arms + abs",
       [ex("db-goblet-squat",3,"12",60,"Sit between your heels, chest tall — your knee felt fine at this depth last block."),
        ex("pushup",3,"12",60,"Hands under shoulders, squeeze your glutes so the hips don't sag."),
        ex("lat-pulldown",3,"12",60,"Pull the elbows to your back pockets, pause at the chest."),
        ex("db-shoulder-press",3,"12",60,"Ribs down, press straight up — no arch to cheat the rep.")],
       [ex("plank",3,"40 sec",45,"Brace like you're about to be poked in the stomach."),
        ex("dead-bug",3,"15",45,"Lower back glued down — shrink the range before it lifts.")]),
    day(3,"Total-body — upper + arms + abs",
       [ex("db-rdl",3,"12",60,"Hips back, soft knees, feel the hamstrings load."),
        ex("db-bench-press",3,"12",60,"Elbows at 45°, touch the chest, drive up."),
        ex("seated-cable-row",3,"12",60,"Squeeze the shoulder blades, don't rock the torso."),
        ex("db-lateral-raise",3,"12",45,"Lead with the elbows, stop at shoulder height.")],
       [ex("lying-leg-raise",3,"15",45,"Press the lower back down, lower the legs slowly."),
        ex("side-plank",3,"30 sec",45,"Push the floor away, stack the hips.")]),
    day(5,"Total-body — upper + arms + abs",
       [ex("leg-press",3,"12",60,"Full foot on the plate, knees track over the toes."),
        ex("incline-pushup",3,"12",60,"Same straight line as the floor version — just easier."),
        ex("db-row",3,"12",60,"Pull to the hip, pause, lower under control."),
        ex("db-curl",3,"12",45,"Elbows pinned, no swing.")],
       [ex("hollow-hold",3,"30 sec",45,"Lower back flat, lift only as high as it stays flat."),
        ex("bird-dog",3,"15",45,"Balance a cup of water on your lower back.")])]
for d in W1:
    for e in d["main"]+d["abs_finisher"]: assert e["exercise_id"] in DEMO_OK, e["exercise_id"]
PROGRAM={"programId":"fixture-rev6","blockNumber":1,"locked":False,"unchanged":False,
 "program":{"stage":4,"equipment_track":"full","start_dow":1,"start_day":1,
   "assessment":{"starting_point":"Solid base from your last block — the abs are showing and the upper body is behind the legs.",
                 "goal_summary":"Your after photo is about 4–5 % body fat away, with more shoulder and arm size.","assigned_level":"Intermediate"},
   "why_this_works":"Three full-body days let you train hard and still recover with a 12-hour workday. Every session opens with 5 minutes of easy cardio, then four compound lifts and an abs finisher.",
   "weeks":[{"week":1,"theme":"Build the base","days":W1},{"week":2,"theme":"Add a set","days":W1},{"week":3,"theme":"Push the load","days":W1},{"week":4,"theme":"Deload + retest","days":W1}]}}
def api(path, body, token=None):
    req=urllib.request.Request(BASE+path, data=json.dumps(body).encode(), headers={"Content-Type":"application/json", **({"Authorization":f"Bearer {token}"} if token else {})})
    with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read())
CRED=f"{OUT}/_fixture_creds.json"   # the pgmem DB lives as long as the local server: reuse the fixture's passwords
if os.path.exists(CRED): c=json.load(open(CRED)); admin_pw,member_pw=c["admin"],c["member"]
else: admin_pw=secrets.token_urlsafe(12); member_pw=secrets.token_urlsafe(12); json.dump({"admin":admin_pw,"member":member_pw},open(CRED,"w"))
try: api("/api/auth/signup", {"email":"hub@local.test","password":admin_pw,"deviceId":"fixture-admin"})
except Exception as e: print("signup (exists?):",e)
adm=api("/api/auth/login", {"email":"hub@local.test","password":admin_pw,"deviceId":"fixture-admin"})
try: r=api("/api/admin/beta-members", {"email":"dan@absbyai.com","password":member_pw}, adm["token"]); print("member fixture", r)
except Exception as e: print("beta-member (exists?):",e)
mem=api("/api/auth/login", {"email":"dan@absbyai.com","password":member_pw,"deviceId":"fixture-member"})
with sync_playwright() as pw:
    b=pw.chromium.launch()
    dev=dict(pw.devices['iPhone 13']); dev['viewport']={'width':390,'height':738}
    ctx=b.new_context(**dev, locale='en-US', timezone_id='America/Chicago', color_scheme='light')
    ctx.add_init_script(f"localStorage.setItem('absbyai_session_token', {json.dumps(mem['token'])}); localStorage.setItem('absbyai_account_email', 'dan@absbyai.com'); localStorage.setItem('absbyai_trainer_program', {json.dumps(json.dumps(PROGRAM))}); localStorage.setItem('absbyai_trainer_progress', '{{}}');")
    page=ctx.new_page(); page.goto(BASE+"/", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(2500)
    print("visible screens:", page.evaluate("() => [...document.querySelectorAll('.screen')].filter(e=>getComputedStyle(e).display!=='none').map(e=>e.id)"))
    # fixture-only: no stick figures anywhere in the capture (every exercise here has a real demo anyway)
    page.evaluate("() => { window.getExerciseAnim = () => ''; }")
    page.evaluate("() => { programView.week=1; programView.day=1; renderProgram(); showScreen('program'); window.scrollTo(0,0); }")
    page.wait_for_timeout(800)
    state=page.evaluate("""() => ({ title: document.getElementById('programNavTitle').textContent,
        cards: [...document.querySelectorAll('#programContent .ex-card .ex-name')].map(e=>e.textContent.trim()),
        anims: document.querySelectorAll('#programContent .ex-anim-wrap, #programContent svg.ex-anim').length,
        h: document.documentElement.scrollHeight })""")
    print(json.dumps(state, indent=1)); assert state["anims"]==0, "stick figures rendered"
    page.screenshot(path=f"{OUT}/day_view.png"); page.screenshot(path=f"{OUT}/day_full.png", full_page=True)
    sheets={}
    for exid in SHEETS:
        cue=next(e["cue"] for d in W1 for e in d["main"]+d["abs_finisher"] if e["exercise_id"]==exid)
        page.evaluate("([id,cue]) => { openExerciseSheet(id, cue, ''); const v=document.getElementById('exSheetDemo'); v.removeAttribute('controls'); }", [exid,cue])
        page.wait_for_timeout(600)
        info=page.evaluate("""() => { const v=document.getElementById('exSheetDemo'); const r=v.getBoundingClientRect();
            return {rect:[r.left,r.top,r.width,r.height], poster:v.getAttribute('poster'), src:v.getAttribute('src'), dpr: window.devicePixelRatio,
                    title: document.querySelector('.ex-sheet-title').textContent, hasSvg: !!document.querySelector('#exSheet svg.ex-anim')} }""")
        assert not info["hasSvg"] and info["src"].endswith(exid+".mp4"), info
        page.screenshot(path=f"{OUT}/sheet_{exid}.png")
        info["rect_px"]=[round(v*info["dpr"]) for v in info["rect"]]
        json.dump(info, open(f"{OUT}/sheet_{exid}.json","w"), indent=1); sheets[exid]=info
        print(exid, info["title"], "rect px", info["rect_px"])
        page.evaluate("() => closeExerciseSheet()"); page.wait_for_timeout(200)
    json.dump({"state":state,"sheets":sheets,"program":PROGRAM}, open(f"{OUT}/trainer_state.json","w"), indent=1)
    b.close()
print("trainer capture written")
