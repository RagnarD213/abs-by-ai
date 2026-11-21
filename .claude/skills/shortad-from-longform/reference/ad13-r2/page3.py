#!/usr/bin/env python3
"""Ad 13 round 3 review page: the finished vertical, its 59 s cut, the full horizontal, the opener motion and the new
P03 in context, and the square look. Same layout as round 2 (floating side player, What I decided, one reply box).
Serve with `.claude/skills/_shared/review_server.py 8817 review3` (seeking works)."""
import html
import json
import os
import re

B = "/Volumes/Extreme/_edit_work/kit9x16/av11-ad13"
R = B + "/review3"
E = html.escape

style = re.search(r"<style>.*?</style>", open(B + "/review2/index.html").read(), re.S).group(0)


def gate(path):
    try:
        g = json.load(open(path))
    except Exception:
        return None
    rows = g.get("rows", [])
    bad = [r for r in rows if r.get("ok") is not True and not r.get("na_reason")]
    return dict(verdict=g.get("verdict"), passed=sum(1 for r in rows if r.get("ok") is True),
                na=sum(1 for r in rows if r.get("na_reason")), bad=[(r["key"], (r.get("detail") or "")[:220]) for r in bad])


F = json.load(open(R + "/facts.json"))           # written by the session: decisions, decided, notes, file names
V_GATE = gate(B + "/gate_final.json")
C_GATE = gate(F["cut_gate"]) if F.get("cut_gate") else None
H_GATE = gate(B + "/round3/h16x9/gate/deliver_gate_3b_final.json")


def gate_html(name, g):
    if not g:
        return f"<li><b>{E(name)}</b>: gate not run</li>"
    if not g["bad"]:
        return f"<li><b>{E(name)}</b>: quality gate PASS, {g['passed']} of {g['passed']} measured rows.</li>"
    fails = [k for k, d in g["bad"] if "NOT MEASURED" not in d]
    nm = [k for k, d in g["bad"] if "NOT MEASURED" in d]
    return (f"<li><b>{E(name)}</b>: quality gate does not pass yet. {g['passed']} rows pass, {len(fails)} fail"
            f" ({E(', '.join(fails))}), {len(nm)} not measured ({E(', '.join(nm))}). {F.get('h_gate_plain', '')}</li>")


def player(src, poster, label, link=None):
    a = f' <a href="{E(link)}">full size file</a>' if link else ""
    return (f'<article><h3>{E(label)}</h3><video controls preload="none" playsinline poster="{E(poster)}" src="{E(src)}"></video>'
            f'<div class="copy">{a}</div></article>')


sq = json.load(open(R + "/square/items.json"))
sq_cards = []
for it in sq:
    p = f"square/stills/{it['id']}.jpg"
    if not os.path.exists(os.path.join(R, p)):
        continue
    sq_cards.append(f'<article><h3>{E(it["id"])} <span class="tag">{E(it.get("kind", ""))}</span></h3><a href="{p}"><img loading="lazy" src="{p}"></a>'
                    f'<div class="copy">{E(" / ".join(it.get("copy") or []))}</div></article>')
for p in sorted(os.listdir(R + "/square/stills")):
    if p.startswith("P_") and p.endswith(".jpg") and not p.startswith("._"):
        sq_cards.append(f'<article><h3>{E(p[2:-4])} <span class="tag">picture</span></h3><a href="square/stills/{p}"><img loading="lazy" src="square/stills/{p}"></a></article>')

out = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ad 13 "The Cost Of Getting Abs" / round 3: the finished videos</title>{style}
<main><h1>Ad 13 "The Cost Of Getting Abs" / round 3: the finished videos</h1>
<p>{F['intro']}</p>
<p class="notice"><b>Already locked, reused as is:</b> {F['locked']}</p>
<nav><a href="#decide">Your {len(F['decisions'])} decisions</a><a href="#films">The finished videos</a><a href="#decided">What I decided</a><a href="#new">Opener and P03</a><a href="#square">Square look</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(F['decisions'])})</h2><ol>{''.join(f'<li>{d}</li>' for d in F['decisions'])}</ol></section>
<div id="dock"><button id="dockx"></button><div class="small" id="nowp">Pick a clip below to play it here.</div><video id="pv" controls preload="none" playsinline></video></div>
<section id="films"><h2>The finished videos</h2><div class="grid">
{''.join(player(*x) for x in F['films'])}
</div><p class="small">{F['films_note']}</p></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join(f'<li>{d}</li>' for d in F['decided'])}</ul></section>
<section id="new"><h2>The opener motion and the new P03, in context</h2><div class="grid">
{''.join(f'<article><h3>{E(i)}</h3><img loading="lazy" src="{E(st)}"><button onclick="play({json.dumps(c)},{json.dumps(i)})">Play it moving, in context</button><div class="copy">{n}</div></article>' for i, st, c, n in F['new'])}
</div></section>
<section id="square"><h2>The square look (1:1), before any square file is built</h2><p>{F['square_note']}</p>
<div class="grid"><article><h3>Moving sample, 0:00 to 0:35</h3><video controls preload="none" playsinline poster="square/sample.jpg" src="square/sample - REVIEW 540p.mp4"></video></article></div>
<div class="grid">{''.join(sq_cards)}</div></section>
<section id="checks"><h2>Checks (plain)</h2><ul>{gate_html('Vertical, full', V_GATE)}{gate_html('Vertical, 59 second cut', C_GATE)}{gate_html('Horizontal, full', H_GATE)}{''.join(f'<li>{c}</li>' for c in F['checks'])}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(F['reply'])}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id;v.play();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth',block:'nearest'}});}}</script></html>"""
assert chr(8212) not in out, "long dash"
open(R + "/index.html", "w").write(out)
print("wrote", R + "/index.html", len(out))
