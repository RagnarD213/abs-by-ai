#!/usr/bin/env python3
"""SL-36 R2 review page (phone first): the three 1080x1920 vertical drafts with their titles and full transcripts, the colour
choices on matching frames, the level-matched voice choices on one continuous passage, every graphic and clip in order, what I
decided, your calls, checks and one reply box. Serve: _shared/review_server.py 9810 <round2>/review"""
import html, json, os, shutil, subprocess, sys, re, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plans as P, batch as Bt
E = html.escape; WK = "/Users/danrrose/Projects/_edit_work/SL-36/round2"; R = f"{WK}/review"; FF = Bt.lib.FF
os.makedirs(f"{R}/media", exist_ok=True)
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
ORDER = [("A", 1), ("B", 2), ("C", 3)]
T_ = json.load(open(f"{WK}/review/page_text.json"))
LOOKS = json.load(open(f"{R}/media/looks.json"))
cards, items = [], {}
for S, n in ORDER:
    d = Bt.D(S); T = json.load(open(f"{d}/timeline.json"))
    src = f"{d}/{P.NAME[S]}.mp4"; dst = f"{R}/media/short{n}.mp4"
    if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src): shutil.copyfile(src, dst)
    subprocess.run([FF, "-v", "error", "-y", "-ss", "1.0", "-i", dst, "-frames:v", "1", "-vf", "scale=540:-1", "-q:v", "3", f"{R}/media/short{n}.jpg"], check=True)
    eb, hl = P.TITLE[S]; title = " ".join(hl)
    words = re.sub(r"\{[^}]*\}", "", P.TEXT[S]).replace(" | ", " ").replace(" / ", " ").replace(" + ", " ").replace("_", " ")
    words = re.sub(r"\s+", " ", words)
    cards.append(f"""<article id="s{n}"><h3>Short {n}: {E(title)} <span class="small">{mmss(T['total'])}</span></h3>
<video controls preload="metadata" playsinline poster="media/short{n}.jpg" src="media/short{n}.mp4"></video>
<p class="small"><button data-review-fullscreen data-target="s{n}">Full screen</button></p>
<h4>Full transcript</h4><p class="tx">{E(words)}</p>
<ul>{''.join('<li>' + E(x) + '</li>' for x in T_['notes'][S])}</ul></article>""")
    shots = json.load(open(f"{d}/shots.json")); man = json.load(open(f"{d}/hf/manifest.json"))
    rows = []
    for sh in shots:
        if sh["kind"] == "talk": continue
        c = sh["cover"]; rows.append((sh["f0"] / Bt.FPS, sh["f1"] / Bt.FPS, T_["what"].get(c["id"], c["id"])))
    for m in man: rows.append((m["a"], m["b"], "Key point bar: " + m["topic"] + ": " + " / ".join(p[0] for p in m["parts"])))
    items[S] = sorted(rows)
def look_rows():
    out = []
    for S, n in ORDER:
        for k in (0, 1):
            figs = []
            for L, name in (("L1", "L1 Parent look (recommended)"), ("L2", "L2 Warmer, richer"), ("L3", "L3 Brighter, crisper")):
                m = LOOKS[f"{S}{k}{L}"]
                figs.append(f'<figure><img loading="lazy" src="media/look_{S}_{k}_{L}.jpg" alt=""><figcaption>{E(name)}<br><span class="small">brightness {m["luma"]:.0f}, colour {m["sat"]:.2f}</span></figcaption></figure>')
            out.append(f'<div class="looks"><p class="small">Short {n}, {"wide" if k == 0 else "close"} shot</p><div class="row3">{"".join(figs)}</div></div>')
    return "".join(out)
V = T_["voice"]
voice = "".join(f'<figure class="vo"><figcaption><b>{E(v["name"])}</b><br><span class="small">{E(v["what"])} ({v["lufs"]} LUFS)</span></figcaption><audio controls preload="metadata" src="media/{v["file"]}"></audio></figure>' for v in V)
ilist = "".join(f'<details><summary>Short {n}: every graphic and clip ({len(items[S])})</summary><ol>' + "".join(f'<li><b>{mmss(a)} to {mmss(b)}</b>: {E(w)}</li>' for a, b, w in items[S]) + '</ol></details>' for S, n in ORDER)
calls = "".join('<li>' + E(x) + '</li>' for x in T_["calls"])
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Man Boobs SFL R2</title>
<style>:root{{color-scheme:dark}}body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:16px}}h1{{font-size:28px;margin:0 0 8px}}h2{{font-size:23px}}h4{{margin:10px 0 2px}}
p,li{{color:#bdd0e4}}section{{margin:20px 0;padding:16px;background:#101f32;border:1px solid #29425b;border-radius:16px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
article{{min-width:0;background:#081626;padding:12px;border-radius:14px}}video{{width:100%;aspect-ratio:9/16;border-radius:10px;background:black}}.small{{font-size:14px;color:#9fb7cf}}.tx{{font-size:15px;color:#e3eefa}}
.row3{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}}figure{{margin:0}}figure img{{width:100%;border-radius:8px}}figcaption{{font-size:14px}}.vo{{margin:10px 0}}audio{{width:100%}}
textarea{{width:100%;box-sizing:border-box;min-height:200px;background:#071221;color:white;padding:12px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;font-size:15px}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}video{{max-height:80vh}}}}</style>
<main><h1>Man Boobs Shorts, round 2: the vertical drafts</h1><p>{E(T_['intro'])}</p>
<section id="picks"><h2>Your picks ({len(T_['questions'])})</h2><ol>{''.join('<li>' + E(x) + '</li>' for x in T_['questions'])}</ol></section>
<section id="shorts"><h2>The three Shorts</h2><div class="grid">{''.join(cards)}</div></section>
<section id="colour"><h2>Colour choices</h2><p>{E(T_['colour_intro'])}</p>{look_rows()}</section>
<section id="voice"><h2>Voice choices</h2><p>{E(T_['voice_intro'])}</p>{voice}</section>
<section id="calls"><h2>Other calls ({len(T_['calls'])})</h2><ol>{calls}</ol></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + E(x) + '</li>' for x in T_['decided'])}</ul></section>
<section id="items"><h2>Every graphic and clip, in order</h2>{ilist}</section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + E(x) + '</li>' for x in T_['checks'])}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">Colour (L1, L2 or L3):
Voice (V1, V2 or V3):
Short 1 (self-check):
Short 2 (spot reduce):
Short 3 (gynecomastia):
Other calls: </textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{R}/index.html", "w").write(page)
man = {f: hashlib.sha256(open(f"{R}/media/{f}", "rb").read()).hexdigest() for f in sorted(os.listdir(f"{R}/media")) if f.endswith((".mp4", ".wav"))}
json.dump(man, open(f"{R}/media_hashes.json", "w"), indent=1); print("page ok", len(page))
