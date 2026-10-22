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
E = html.escape; R = f"{W5}/round7/page_final"; FF = Bt.lib.FF; FIX = f"{W5}/round7/intro"; FR = f"{W5}/round7/frames"
os.makedirs(f"{R}/media", exist_ok=True)
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def cp(src, dst):
    if not os.path.exists(f"{R}/{dst}") or os.path.getsize(f"{R}/{dst}") != os.path.getsize(src): shutil.copyfile(src, f"{R}/{dst}")
    return dst
ORDER = ["A", "B", "C", "E", "F"]          # R7: the five rebuilt shorts (D approved in R6)
HEAD = {"A": 4.14, "B": 4.61, "C": 2.84, "D": 3.28, "E": 3.15, "F": 1.94}
LINE = {"A": "Here's why you should start Zepbound at 1 milligram to avoid the side effects.",
        "B": "Here's why you should stop using the pen to inject Zepbound, and why you should use a needle instead.",
        "C": "Here's how to inject Zepbound with a needle, step by step.",
        "D": "Here's why Thursday evening is the best time to inject Zepbound.",
        "E": "Here's how to come off Zepbound without gaining the fat back.",
        "F": "Zepbound reduces your appetite, so eating less calories is easier."}
HOW = {"A": "The 1 mg vial in the spot light, the 2.5 mg vial behind it; dust drifts in the light and the camera creeps in (Veo, on your Flow subscription).",
       "B": "Pen on the left, vial and syringe on the right; the light over the pen dims (done in editing, a soft natural fade) and the camera pushes in.",
       "C": "The kit laid out; Soft Blue step numbers 1, 2, 3 land beside the vial, the pad and the syringe; the camera pushes in. Then your two approved injection clips.",
       "E": "The empty vial set aside next to a packed gym bag and a protein meal-prep box; the camera pushes in.",
       "F": "A modest chicken and greens plate, the big pasta bowl behind; the camera pushes in. It ends in the pause after \"appetite,\"."}
cards, revs = [], []
for S in ORDER:
    if S == "A": require_pass(f"{FIX}/A_intro.mp4")      # the only intro with AI motion; B, C, E, F are the reviewed stills
    base = os.path.basename(Dl.dname(S))[:-4]; name = " ".join(P.TITLE[S][1])
    rv = cp(f"{Dl.REV}/{base} - REVIEW 540p.mp4", f"media/{S} - REVIEW 540p.mp4"); full = cp(Dl.dname(S), f"media/{S} - 1080x1920.mp4")
    poster = f"media/{S}.jpg"; frm = cp(f"{FR}/{'E2' if S == 'E' else S}_r7.jpg", f"media/{S}_frame.jpg")
    subprocess.run([FF, "-v", "error", "-y", "-ss", "1.2", "-i", f"{R}/{rv}", "-frames:v", "1", "-q:v", "3", f"{R}/{poster}"], check=True)
    T = json.load(open(f"{Bt.D(S)}/timeline.json")); h = HEAD[S]
    pl = lambda t, lab: f"<button onclick=\"play('{rv}',{E(json.dumps('Short ' + S + ': ' + lab))},{t:.2f})\">{E(lab)}</button>"
    ch = [f"<li><b>0:00 to {mmss(h)}</b>: the new intro (the picture you approved). {E(HOW[S])} Title band off, back on the first frame of you on camera at {mmss(h)}. Watch 0:00 to {mmss(h + 4)}. {pl(0, 'Play from 0:00')}</li>"]
    if S == "C":
        ch.append(f"<li><b>0:02.8 to 0:05.8</b>: Seattle Children's self-injection into the front of the thigh (your pick), credited. <b>0:05.8 to 0:09.6</b>: SynergenX pinch and inject, credited, framed so the needle stays visible above the Step 1 bar. Watch 0:02 to 0:12. {pl(2.0, 'Play from 0:02')}</li>")
    cards.append(f"""<article id="f{S}"><h3>{S}: {E(name)} <span class="small">{mmss(T['total'])}</span></h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><a href="{rv}" target="_blank"><img loading="lazy" src="{poster}"></a><a href="{frm}" target="_blank"><img loading="lazy" src="{frm}"></a></div><div class="small">Left: the short. Right: the new start frame of the intro.</div>{pl(0, 'Play it')}
<div class="copy">Opening line under the intro: "{E(LINE[S])}"<ul>{''.join(ch)}</ul><a href="{full}">1080 x 1920 file</a></div></article>""")
DECIDED = [
 "A moves with AI: Veo added drifting dust and a slow camera creep; an independent reviewer called it real footage. The other AI motion takes did not pass (B's pen was blacked out by a hard-edged shadow, E's vial label came out misspelled with dust bursting from nowhere, F's steam formed floating ghost shapes, C's mat texture shimmered).",
 "So B, C, E and F use the exact pictures you approved, with a smooth slow push-in done in editing. B's light dim is done in editing too, as a soft natural fade. Nothing on screen can look like AI motion.",
 "C's step numbers are a new Soft Blue moving graphic (round glass badges that land one by one and keep gently moving).",
 "Everything after each intro is the short you approved, unchanged. D (Inject On Thursday Evening) was approved last round and is untouched.",
]
CHECKS = [
 "Every picture passed an independent reviewer; A's motion passed the motion gate and a reviewer (real footage).",
 "Every short: audio gate (your approved mix), captions against the transcript, the watch scan (no frozen or black frames, no jump cuts), a watch judge on every boundary, the delivery gate, and one independent reviewer on all five.",
 "VLC copies are in Videos to Review as \"Top 5 Zepbound Tips SFL R7\".",
]
PENDING = []
REPLY = "A: approved / changes:\nB: approved / changes:\nC: approved / changes:\nE: approved / changes:\nF: approved / changes:\n\nOther notes:\n"
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 5 Zepbound Tips SFL R7</title>
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
<main><h1>Top 5 Zepbound Tips shorts / Round 7: the five finished shorts</h1>
<p>The five intro pictures you approved, built into the shorts. Only the opening of each changed; everything after it is the short you already approved. D was approved last round.</p>
<nav><a href="#shorts">The five shorts</a><a href="#decided">What I decided</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<div id="dock"><div class="small" id="nowp">Pick any Play button: it plays here (at the right on a wide screen). Every player can be scrubbed.</div><video id="pv" controls preload="none" playsinline></video></div>
<section id="shorts"><h2>The five shorts with their new intros</h2><div class="grid">{''.join(cards)}</div></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join(f'<li>{E(x)}</li>' for x in DECIDED)}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{''.join(f'<li>{E(x)}</li>' for x in CHECKS)}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(REPLY)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button></p></section></main>
<script>function play(src,id,t){{const v=document.getElementById('pv');const go=()=>{{try{{v.currentTime=t||0}}catch(e){{}};v.play()}};document.getElementById('nowp').textContent=id;
if(v.getAttribute('src')!==src){{v.src=src;v.addEventListener('loadedmetadata',go,{{once:true}});v.load()}}else go();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth',block:'nearest'}});}}</script></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{R}/index.html", "w").write(page); print("page ok", len(page))
