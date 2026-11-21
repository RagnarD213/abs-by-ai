#!/usr/bin/env python3
"""SL-06 R7 page: the five no-face AI intro STILLS for Dan's pick (no motion yet). Each still beside its in-context preview
(the still with the AI-GENERATED chip and the slow push-in the edit will add, over the short's real opening line, then the
approved short). Refuses a still without gate + reviewer PASS.  python3 page_r7.py ; review_server.py 8821 <round7/page>"""
import html, os, shutil, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck")
from gate import require_pass
E = html.escape; R = "/Volumes/Extreme/_edit_work/sl06/round7"; P = f"{R}/page"; os.makedirs(f"{P}/media", exist_ok=True)
def cp(src, dst):
    shutil.copyfile(src, f"{P}/{dst}"); return dst
ITEMS = [
 ("A", "Start At 1 mg Not 2.5 mg", "Here's why you should start Zepbound at 1 milligram to avoid the side effects.",
  "The 1 mg vial in the spot light, the 2.5 mg vial behind it. Motion: dust drifting in the light; slow push-in."),
 ("B", "Use A Needle And Vial Not The Pen", "Here's why you should stop using the pen to inject Zepbound, and why you should use a needle instead.",
  "Plain pen on the left, vial and syringe on the right. Motion: the light over the pen fades out, the light over the vial brightens; slow push-in."),
 ("C", "How To Inject In 10 Seconds", "Here's how to inject Zepbound with a needle, step by step.",
  "The kit laid out: vial, swab, syringe. Motion: almost none; a slow glide, with moving Soft Blue step numbers 1, 2, 3 added beside the items. Then the two real injection clips you approved."),
 ("E2", "How To Come Off Without Regaining It", "Here's how to come off Zepbound without gaining the fat back.",
  "The empty vial set aside next to a packed gym bag and a protein meal-prep box: the medicine is done, the habits stay. (Replaces the belt idea; see What I decided.) Motion: almost none; slow push-in."),
 ("F", "How Much Protein You Need On A GLP-1", "Zepbound reduces your appetite, so eating less calories is easier.",
  "A modest chicken and greens plate, steam rising, the big pasta bowl left alone. Motion: the steam; slow push-in."),
]
cards = []
for S, name, line, how in ITEMS:
    st = f"{R}/frames/{S}_r7.jpg"
    if S == "E2" and not os.path.exists(f"{R}/preview/E2_preview.mp4"): continue
    require_pass(st, st)
    img = cp(st, f"media/{S}_still.jpg"); pv = cp(f"{R}/preview/{S}_preview.mp4", f"media/{S}_preview.mp4")
    cards.append(f"""<article><h3>{S[0]}: {E(name)}</h3><div class="two"><a href="{img}" target="_blank"><img loading="lazy" src="{img}"></a>
<video controls preload="metadata" playsinline src="{pv}"></video></div><div class="small">Left: the picture. Right: how it opens the short (picture, label and push-in over your real first line; no motion yet).</div>
<div class="copy">Line: "{E(line)}"<br>{E(how)}</div></article>""")
DECIDED = [
 "No face and no hands in any of them, so none of the things that ruined the AI clips of you can happen. The video model will only add light, dust or steam; the camera move is done in editing.",
 "Every picture passed an independent reviewer asked: would this pass as a real photo, and does it show the line at a glance? A and C needed redoing first: A had a melted vial cap; C went through four versions (a fake syringe scale, a sharps bin that read as a food tub, impossible sizes) and now shows three real-size items with the syringe's markings facing down.",
 "E changed idea: the belt failed five times. The image model could not draw real worn leather around the holes (every version had painted-on cracks or rings a reviewer could spot), so E is now the empty vial beside a packed gym bag and a protein meal-prep box. Same message: the medicine is done, the habits stay. Say if you want another try at the belt.",
 "Everything is placed clear of the captions at the bottom and the AI-GENERATED label at the top right.",
 "D (Inject On Thursday Evening) is approved and unchanged.",
]
REPLY = "A: approved / changes:\nB: approved / changes:\nC: approved / changes:\nE: approved / changes:\nF: approved / changes:\n\nOther notes:\n"
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 5 Zepbound Tips SFL R7</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--text:#edf5ff;--muted:#bdd0e4}}
body{{margin:0;background:var(--bg);color:var(--text);font:17px system-ui,-apple-system,sans-serif;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:28px 16px}}
h1{{font-size:32px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:24px;margin-top:0}}h3{{font-size:17px;margin:6px 0}}p,li{{color:var(--muted)}}
section{{margin:24px 0;padding:20px;background:var(--panel);border:1px solid var(--line);border-radius:18px}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}
article{{min-width:0;background:#081626;padding:12px;border-radius:12px}}.two{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}img,video{{width:100%;border-radius:10px;background:#000;display:block}}
a{{color:#8cd6ff}}.small{{font-size:13px;color:#9fb7cf;margin-top:6px}}.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}
textarea{{width:100%;box-sizing:border-box;min-height:200px;background:#071221;color:white;padding:14px;font:15px ui-monospace,monospace;border:1px solid #47607b;border-radius:10px}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:7px 11px;cursor:pointer;font-size:14px;margin-top:8px}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}@media(max-width:560px){{h1{{font-size:26px}}}}</style>
<main><h1>Top 5 Zepbound Tips shorts / Round 7: five new intro pictures</h1>
<p>The five no-face ideas you picked, as pictures first. Nothing has been animated yet and no video credits are spent. Approve or change each; then I make the motion (about 250 Flow credits for all five), rebuild the shorts and bring them back.</p>
<section><h2>The five pictures</h2><div class="grid">{''.join(cards)}</div></section>
<section><h2>What I decided (overrule anything)</h2><ul>{''.join(f'<li>{E(x)}</li>' for x in DECIDED)}</ul></section>
<section><h2>One reply</h2><textarea id="r">{E(REPLY)}</textarea><button onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button></section></main></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{P}/index.html", "w").write(page); print("page ok", len(page))
