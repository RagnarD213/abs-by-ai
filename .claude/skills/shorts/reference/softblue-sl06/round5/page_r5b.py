#!/usr/bin/env python3
"""SL-06 round 5 final page: the six rebuilt shorts with the moving AI flex intros (band off during the intro) and C's
credited YouTube clips. A later-round page: only what changed, each change with its time and a watch range, one floating
player, what I decided, checks, one reply box. Refuses an intro whose motion take lacks clipcheck + reviewer PASS.
  python3 page_r5b.py ; review_server.py 8821 /Volumes/Extreme/_edit_work/sl06/round5/page"""
import html, json, os, shutil, subprocess, sys
W5 = "/Volumes/Extreme/_edit_work/sl06"; sys.path.insert(0, W5)
import plans as P, batch as Bt
import importlib.util as _iu
_sp = _iu.spec_from_file_location("sl06_deliver", f"{W5}/deliver.py"); Dl = _iu.module_from_spec(_sp); _sp.loader.exec_module(Dl)
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck")
from clipcheck import require_pass
E = html.escape; R = f"{W5}/round5/page"; FF = Bt.lib.FF; FIX = f"{W5}/round5/fix"
os.makedirs(f"{R}/media", exist_ok=True)
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def cp(src, dst):
    if not os.path.exists(f"{R}/{dst}") or os.path.getsize(f"{R}/{dst}") != os.path.getsize(src): shutil.copyfile(src, f"{R}/{dst}")
    return dst
ORDER = ["D", "A", "B", "C", "E", "F"]
HEAD = {"A": 4.14, "B": 4.61, "C": 2.84, "D": 3.28, "E": 3.15, "F": 2.50}
LINE = {"A": "Here's why you should start Zepbound at 1 milligram to avoid the side effects.",
        "B": "Here's why you should stop using the pen to inject Zepbound, and why you should use a needle instead.",
        "C": "Here's how to inject Zepbound with a needle, step by step.",
        "D": "Here's why Thursday evening is the best time to inject Zepbound.",
        "E": "Here's how to come off Zepbound without gaining the fat back.",
        "F": "Zepbound reduces your appetite, so eating less calories is easier."}
HOW = {"A": "Your fingertip stays on the poster's corner while you hold the flex and smile.",
       "B": "Your fingertip stays on the poster's corner while you hold the flex and smile.",
       "C": "Your fingertip stays on the poster's corner, a quick glance at it, smile held.",
       "D": "Double biceps: you squeeze a little harder and the grin grows.",
       "E": "Flexed arm in front, the other hand on the poster's corner, smile held.",
       "F": "Flexed arm in front, the other hand points up at the poster, smile held."}
cards, revs = [], []
for S in ORDER:
    require_pass(f"{FIX}/{S}_intro.mp4")
    base = os.path.basename(Dl.dname(S))[:-4]; name = " ".join(P.TITLE[S][1])
    rv = cp(f"{Dl.REV}/{base} - REVIEW 540p.mp4", f"media/{S} - REVIEW 540p.mp4"); full = cp(Dl.dname(S), f"media/{S} - 1080x1920.mp4")
    poster = f"media/{S}.jpg"
    subprocess.run([FF, "-v", "error", "-y", "-ss", "1.2", "-i", f"{R}/{rv}", "-frames:v", "1", "-q:v", "3", f"{R}/{poster}"], check=True)
    T = json.load(open(f"{Bt.D(S)}/timeline.json")); h = HEAD[S]
    pl = lambda t, lab: f"<button onclick=\"play('{rv}',{E(json.dumps('Short ' + S + ': ' + lab))},{t:.2f})\">{E(lab)}</button>"
    ch = [f"<li><b>0:00 to {mmss(h)}</b>: the moving AI flex intro (was a stock clip). {E(HOW[S])} Title band off, back on the first frame of you on camera at {mmss(h)}. Watch 0:00 to {mmss(h + 4)}. {pl(0, 'Play from 0:00')}</li>"]
    if S == "C":
        ch.append(f"<li><b>0:02.8 to 0:05.8</b>: Seattle Children's self-injection into the front of the thigh (your pick), credited. <b>0:05.8 to 0:09.6</b>: SynergenX pinch and inject, credited, with the Step 1 bar over it. Watch 0:02 to 0:12. {pl(2.0, 'Play from 0:02')}</li>")
    cards.append(f"""<article id="f{S}"><h3>{S}: {E(name)} <span class="small">{mmss(T['total'])}</span></h3>
<a href="{rv}" target="_blank"><img loading="lazy" src="{poster}"></a>{pl(0, 'Play it')}
<div class="copy">Opening line under the intro: "{E(LINE[S])}"<ul>{''.join(ch)}</ul><a href="{full}">1080 x 1920 file</a></div></article>""")
DECIDED = [
 "All six intros move: made on your Google Flow subscription (C, D, E, F) and, after the free credits ran out, on the paid Veo service for A and B ($1.20 for two takes, your OK).",
 "Veo kept turning the pointing hand toward your own chest and kept moving your mouth as if you were talking. So A, B, C and E start from your approved END frame (finger already on the poster's corner) and hold that pose; F keeps the finger pointing up at the poster from below, as in its start frame. D is the double biceps squeeze from its start frame.",
 "Where Veo still moved the lips (C, E, F), the smile is held: the mouth from a clean frame early in the take is kept steady, tracked to the face, so nothing reads as lip sync under your voice.",
 "Veo scribbles small text: the vial labels are restored from your approved frames on every frame, and D's calendar too (Veo wrote FRI with a backwards R).",
 "The title band is off during every intro and returns on the first frame of you on camera. The AI-GENERATED label sits top right (D: top centre); captions, the disclaimer and AbsByAI.com stay on.",
 "Everything after each intro is the round-2 short you approved, unchanged (same cut, audio, graphics, captions); C's 2.8 to 9.6 s uses the clips you approved last round.",
]
CHECKS = [
 "Every intro: the motion check (nothing vanishes or appears, poster and gym hold still, vials stay pinched) and a fresh independent reviewer PASS, after several takes were failed and redone (talking mouth, hand to chest, head duck, backwards R, garbled labels).",
 "Every short: audio gate PASS (your approved mix, untouched), Whisper transcript against the captions, the watch scan (no frozen or black frames, no jump cuts), a watch judge on every boundary strip and contact sheet, and the delivery gate PASS.",
 "One independent reviewer watched all six finished shorts against the plan and the standing rules.",
 "VLC copies of all six are in the Videos to Review folder (the round 2 copies there were replaced).",
]
REPLY = "Six shorts: approved / changes:\n   D:\n   A:\n   B:\n   C:\n   E:\n   F:\n\nOther notes:\n"
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 5 Zepbound Tips SFL R5</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--text:#edf5ff;--muted:#bdd0e4}}
body{{margin:0;background:var(--bg);color:var(--text);font:17px system-ui,-apple-system,sans-serif;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:28px 16px}}
h1{{font-size:34px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:25px;margin-top:0}}h3{{font-size:17px;margin:10px 0 4px}}p,li{{color:var(--muted)}}li b,p b{{color:var(--text)}}
section{{margin:28px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:18px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}
article{{min-width:0;background:#081626;padding:12px;border-radius:12px}}img,video{{width:100%;border-radius:10px;background:#000;display:block}}a{{color:#8cd6ff}}.small{{font-size:14px;color:#9fb7cf;font-weight:400}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}
textarea{{width:100%;box-sizing:border-box;min-height:260px;background:#071221;color:white;padding:14px;font:15px ui-monospace,monospace;border:1px solid #47607b;border-radius:10px}}
#dock{{position:sticky;top:0;z-index:5;background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid var(--line);margin-bottom:16px;text-align:center}}#dock video{{max-height:60vh;width:auto;max-width:100%;margin:auto}}
@media(min-width:1500px){{body{{padding-right:min(30vw,520px)}}#dock{{position:fixed;top:16px;right:16px;width:calc(min(30vw,520px) - 40px);max-height:calc(100vh - 32px);box-sizing:border-box;margin:0;box-shadow:0 8px 40px #000a}}#dock video{{max-height:calc(100vh - 110px)}}}}
@media(max-width:1499px){{#dock video{{max-height:42vh}}}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:7px 11px;cursor:pointer;font-size:14px;margin:6px 4px 0 0}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr 1fr}}}}@media(max-width:560px){{.grid{{grid-template-columns:1fr}}h1{{font-size:27px}}}}</style>
<main><h1>Top 5 Zepbound Tips shorts / Round 5: all six built with the moving intros</h1>
<p>You approved all six intro frame pairs, the gym look and C's clips. Here are the six finished shorts. Only the opening of each changed (and C's first 10 seconds); everything after it is the round-2 short you approved.</p>
<nav><a href="#shorts">The six shorts and what changed</a><a href="#decided">What I decided</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<div id="dock"><div class="small" id="nowp">Pick any Play button: it plays here (at the right on a wide screen). Every player can be scrubbed.</div><video id="pv" controls preload="none" playsinline></video></div>
<section id="shorts"><h2>The six shorts: what changed, with times</h2><div class="grid">{''.join(cards)}</div></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join(f'<li>{E(x)}</li>' for x in DECIDED)}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{''.join(f'<li>{E(x)}</li>' for x in CHECKS)}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(REPLY)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button></p></section></main>
<script>function play(src,id,t){{const v=document.getElementById('pv');const go=()=>{{try{{v.currentTime=t||0}}catch(e){{}};v.play()}};document.getElementById('nowp').textContent=id;
if(v.getAttribute('src')!==src){{v.src=src;v.addEventListener('loadedmetadata',go,{{once:true}});v.load()}}else go();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth',block:'nearest'}});}}</script></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{R}/index.html", "w").write(page); print("page ok", len(page))
