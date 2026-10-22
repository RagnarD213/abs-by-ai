#!/usr/bin/env python3
"""SL-06 round 6 page (natural AI intros: relaxed pose, closed-mouth smile). Adapted from round 5's final page: the six rebuilt shorts with the moving AI flex intros (band off during the intro) and C's
credited YouTube clips. A later-round page: only what changed, each change with its time and a watch range, one floating
player, what I decided, checks, one reply box. Refuses an intro whose motion take lacks clipcheck + reviewer PASS.
  python3 page_r5b.py ; review_server.py 8821 /Volumes/Extreme/_edit_work/sl06/round6/page"""
import html, json, os, shutil, subprocess, sys
W5 = "/Volumes/Extreme/_edit_work/sl06"; sys.path.insert(0, W5)
import plans as P, batch as Bt
import importlib.util as _iu
_sp = _iu.spec_from_file_location("sl06_deliver", f"{W5}/deliver.py"); Dl = _iu.module_from_spec(_sp); _sp.loader.exec_module(Dl)
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck")
from clipcheck import require_pass
E = html.escape; R = f"{W5}/round6/page"; FF = Bt.lib.FF; FIX = f"{W5}/round6/fix"; FR = f"{W5}/round6/frames"
os.makedirs(f"{R}/media", exist_ok=True)
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def cp(src, dst):
    if not os.path.exists(f"{R}/{dst}") or os.path.getsize(f"{R}/{dst}") != os.path.getsize(src): shutil.copyfile(src, f"{R}/{dst}")
    return dst
ORDER = ["C", "D"]          # the two shorts whose new intro passed every check; A, B, E, F are pending (see PENDING)
HEAD = {"A": 4.14, "B": 4.61, "C": 2.84, "D": 3.28, "E": 3.15, "F": 1.94}
LINE = {"A": "Here's why you should start Zepbound at 1 milligram to avoid the side effects.",
        "B": "Here's why you should stop using the pen to inject Zepbound, and why you should use a needle instead.",
        "C": "Here's how to inject Zepbound with a needle, step by step.",
        "D": "Here's why Thursday evening is the best time to inject Zepbound.",
        "E": "Here's how to come off Zepbound without gaining the fat back.",
        "F": "Zepbound reduces your appetite, so eating less calories is easier."}
HOW = {S: "A calm, relaxed hold: closed-mouth smile, natural blink, a slight settle, the vial held at chest height. No flex, no pointing." for S in "ABCDEF"}
cards, revs = [], []
for S in ORDER:
    require_pass(f"{FIX}/{S}_intro.mp4")
    base = os.path.basename(Dl.dname(S))[:-4]; name = " ".join(P.TITLE[S][1])
    rv = cp(f"{Dl.REV}/{base} - REVIEW 540p.mp4", f"media/{S} - REVIEW 540p.mp4"); full = cp(Dl.dname(S), f"media/{S} - 1080x1920.mp4")
    poster = f"media/{S}.jpg"; frm = cp(f"{FR}/{S}_r6h.jpg", f"media/{S}_frame.jpg"); old = cp(f"{FR}/{S}_r6.jpg", f"media/{S}_pointing.jpg")
    subprocess.run([FF, "-v", "error", "-y", "-ss", "1.2", "-i", f"{R}/{rv}", "-frames:v", "1", "-q:v", "3", f"{R}/{poster}"], check=True)
    T = json.load(open(f"{Bt.D(S)}/timeline.json")); h = HEAD[S]
    pl = lambda t, lab: f"<button onclick=\"play('{rv}',{E(json.dumps('Short ' + S + ': ' + lab))},{t:.2f})\">{E(lab)}</button>"
    ch = [f"<li><b>0:00 to {mmss(h)}</b>: the new AI intro (replaces the rejected R5 flex clip). {E(HOW[S])} Title band off, back on the first frame of you on camera at {mmss(h)}. Watch 0:00 to {mmss(h + 4)}. {pl(0, 'Play from 0:00')}</li>"]
    if S == "C":
        ch.append(f"<li><b>0:02.8 to 0:05.8</b>: Seattle Children's self-injection into the front of the thigh (your pick), credited. <b>0:05.8 to 0:09.6</b>: SynergenX pinch and inject, credited, framed so the needle stays visible above the Step 1 bar. Watch 0:02 to 0:12. {pl(2.0, 'Play from 0:02')}</li>")
    cards.append(f"""<article id="f{S}"><h3>{S}: {E(name)} <span class="small">{mmss(T['total'])}</span></h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><a href="{rv}" target="_blank"><img loading="lazy" src="{poster}"></a><a href="{frm}" target="_blank"><img loading="lazy" src="{frm}"></a></div><div class="small">Left: the short. Right: the new start frame of the intro.</div>{pl(0, 'Play it')}
<div class="copy">Opening line under the intro: "{E(LINE[S])}"<ul>{''.join(ch)}</ul><a href="{full}">1080 x 1920 file</a></div></article>""")
DECIDED = [
 "No flexing at all: the new intros show you relaxed, holding the vial at chest height with the other arm at your side. Veo made every raised fist tremble and kept swinging the pointing hand to your chest, in every wording and both models. The poster behind you still names the tip.",
 "A regular closed-mouth smile on every frame. The start frames were redrawn on the Codex subscription with lips together (no teeth), and the motion prompt never says \"smile\": that word alone made Veo grow a toothy grin in nearly every take.",
 "Nothing on your face or mouth is patched. The only repairs are the tiny vial label (and D's calendar), copied from the approved frame because Veo scrambles small text.",
 "Picky, as you asked: about 110 takes on your Google Flow subscription (the Quality model for most, which holds a face far better), every take measured for mouth, tremor, sway, head nods, blinks and sharpness, then a fresh independent reviewer per finalist asked one question: real footage of a relaxed person, or AI? Only C and D passed. A, B, E and F are not on this page because every take still nodded, rocked, squinted or went soft, and you said slop should never reach you.",
 "Everything after each intro is the short you already approved, unchanged.",
]
CHECKS = [
 "C and D intros: lips closed every frame, one blink, body sway 9 to 18 px (rejected takes rocked 88 to 138 px), hand tremor 0.12 to 0.7 (your rejected R5 clips 0.9 to 2.2), the motion gate and an independent reviewer PASS (verdict: real footage of a relaxed person).",
 "C and D shorts: audio gate PASS (your approved mix, untouched), captions against the transcript, the watch scan (no frozen or black frames, no jump cuts), a watch judge on every boundary and the delivery gate.",
 "VLC copies of C and D are in Videos to Review as \"Top 5 Zepbound Tips SFL R6\"; the six rejected R5 copies were moved out of that folder.",
]
PENDING = [
 ("A", "Start At 1 mg Not 2.5 mg", "closest take nodded three times and squinted"),
 ("B", "Use A Needle And Vial Not The Pen", "closest take snapped its head at the start and closed its eyes at the end"),
 ("E", "How To Come Off Without Regaining It", "closest take dipped its head 63 px and went soft in the first second"),
 ("F", "How Much Protein You Need On A GLP-1", "closest take did a quick chuckle-nod and its sharpness pulsed"),
]
REPLY = "C: approved / changes:\nD: approved / changes:\nA, B, E, F intros: paid Veo up to $16 / spend the last Flow credits / keep R2 openings / other:\n\nOther notes:\n"
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 5 Zepbound Tips SFL R6</title>
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
<main><h1>Top 5 Zepbound Tips shorts / Round 6: natural AI intros</h1>
<p>You rejected all six R5 intros (weird smile, shaking, flexing too hard). Two of six are finished and passed every check: C and D. The other four are not on this page because no take was good enough yet; one decision for you below. Only the intro changed; everything after it is the short you already approved.</p>
<nav><a href="#shorts">C and D, finished</a><a href="#pending">A, B, E, F: your call</a><a href="#decided">What I decided</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<div id="dock"><div class="small" id="nowp">Pick any Play button: it plays here (at the right on a wide screen). Every player can be scrubbed.</div><video id="pv" controls preload="none" playsinline></video></div>
<section id="shorts"><h2>C and D: finished, with the new intro</h2><div class="grid">{''.join(cards)}</div></section>
<section id="pending"><h2>A, B, E, F: not ready, one decision for you</h2><p>About 110 takes on the subscription produced no take for these four that an independent reviewer would call real footage. Their new relaxed start frames passed review (right column below); the motion is the problem. Your Flow balance is down to about 1,000 credits, which other editing jobs share this month, so I stopped spending.</p><div class="grid">{''.join(f'<article><h3>{S}: {E(n)}</h3><img loading="lazy" src="{cp(f"{FR}/{S}_r6h.jpg", f"media/{S}_frame.jpg")}"><div class="copy">Start frame: passed review. Best take: {E(w)}.</div></article>' for S, n, w in PENDING)}</div><p><b>My recommendation:</b> let me try the paid Veo service for these four, about $16 (4 shorts, about 5 takes each at $0.80). It accepts a "do not" list (nodding, squinting, swaying, grinning, talking) that Flow does not, and that is exactly what keeps failing. Other options: spend your last Flow credits, or keep these four on their round-2 openings for now.</p></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join(f'<li>{E(x)}</li>' for x in DECIDED)}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{''.join(f'<li>{E(x)}</li>' for x in CHECKS)}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(REPLY)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button></p></section></main>
<script>function play(src,id,t){{const v=document.getElementById('pv');const go=()=>{{try{{v.currentTime=t||0}}catch(e){{}};v.play()}};document.getElementById('nowp').textContent=id;
if(v.getAttribute('src')!==src){{v.src=src;v.addEventListener('loadedmetadata',go,{{once:true}});v.load()}}else go();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth',block:'nearest'}});}}</script></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{R}/index.html", "w").write(page); print("page ok", len(page))
