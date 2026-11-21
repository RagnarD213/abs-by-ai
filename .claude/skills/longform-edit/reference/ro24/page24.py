"""RO-24 round 1 review page (PRE-RENDER-APPROVAL "The review page"; Dan's scope for this round, 2026-10-20: the chroma key, the
audio, the first minute and the colour, key locked first). Header of locks, your decisions, the first minute on top, the key
(moving comparisons), colour, background, voice auditions, What I decided, the two graphics in context, what is pending, checks,
one reply box. One shared player that floats at the right on a wide screen."""
import json, html, os
W = '/Volumes/Expansion/_edit_work/RO-24/round1'; OUT = f'{W}/review'
X = json.load(open(f'{OUT}/page_extra.json'))
E = html.escape
def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'
def vid(src, poster, label):
    return f"""<button onclick="play('{src}','{E(label)}')">Play: {E(label)}</button>"""
key_html = ''.join(f"""<article><h3>{E(k['title'])}</h3><a href="{k['jpg']}"><img loading="lazy" src="{k['jpg']}"></a>
{vid(k['mp4'], k['jpg'], k['title'])}<p class="small">{E(k['note'])}</p></article>""" for k in X['key'])
col_html = ''.join(f"""<article><h3>{E(c['title'])} <span class="tag">{E(c['id'])}</span></h3>
<div class="two"><figure><a href="{c['W']}"><img loading="lazy" src="{c['W']}"></a><figcaption>Wide</figcaption></figure>
<figure><a href="{c['T']}"><img loading="lazy" src="{c['T']}"></a><figcaption>Tight</figcaption></figure></div>
<p class="small">{E(c['note'])}</p></article>""" for c in X['colour'])
bg_html = ''.join(f"""<article><h3>{E(c['title'])} <span class="tag">{E(c['id'])}</span></h3>
<div class="two"><figure><a href="{c['W']}"><img loading="lazy" src="{c['W']}"></a><figcaption>Wide</figcaption></figure>
<figure><a href="{c['T']}"><img loading="lazy" src="{c['T']}"></a><figcaption>Tight</figcaption></figure></div>
<p class="small">{E(c['note'])}</p></article>""" for c in X['background'])
voice_html = ''.join(f"""<article><h3>{E(v['title'])} <span class="tag">{E(v['id'])}</span></h3>
<audio controls preload="none" src="{v['src']}"></audio><p class="small">{E(v['note'])}</p></article>""" for v in X['voice'])
gfx_html = ''.join(f"""<article><h3>{E(g['name'])} <span class="tag">{g['id']}</span> <span class="small">{mmss(g['t0'])} to {mmss(g['t1'])}</span></h3>
<a href="{g['still']}"><img loading="lazy" src="{g['still']}"></a>{vid(g['ctx'], g['still'], g['id'] + ' in context')}
<div class="copy"><b>topic</b>: {E(g['topic'])}<br><b>point</b>: {E(g['point'])}<br><span class="ok">{E(g['check'])}</span></div>
<details><summary>Speech before / during / after</summary><p class="small"><b>before</b>: {E(g['before'])}<br><b>during</b>: {E(g['during'])}<br><b>after</b>: {E(g['after'])}</p></details></article>""" for g in X['graphics'])
fm = X['first_minute']
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Celebrity Ozempic, round 1</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px system-ui;line-height:1.55}}main{{max-width:1240px;margin:0 auto;padding:28px 16px}}
@media(min-width:1500px){{main{{margin:0 0 0 2vw;max-width:calc(62vw)}}#dock{{position:fixed;right:1.5vw;top:16px;width:33vw;z-index:9}}}}
h1{{font-size:36px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:25px}}p,li{{color:var(--mute)}}section{{margin:30px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}figure{{margin:0}}figcaption{{font-size:13px;color:#9fb7cf}}
img,video{{width:100%;border-radius:10px;background:black}}audio{{width:100%}}a{{color:var(--acc)}}.tag{{color:#8ed7ff;font-size:13px;font-weight:700}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.ok{{color:#9be7b5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}
textarea{{width:100%;box-sizing:border-box;min-height:240px;background:var(--bg);color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
#dock{{background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid var(--line);margin-bottom:16px}}#dock video{{max-height:60vh}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
table{{font-size:14px;color:#cfe0f0;border-collapse:collapse}}td{{padding:3px 10px 3px 0;vertical-align:top}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}h1{{font-size:28px}}}}</style>
<div id="dock"><div class="small" id="nowp">Pick any comparison or graphic below to play it here.</div><video id="pv" controls preload="none" playsinline></video></div>
<main><h1>Reacting To Celebrity Ozempic Transformations <span class="small">LFC, round 1</span></h1>
<p>{X['intro']}</p>
<p class="notice"><b>Already locked, reused as is:</b> {X['locked']}</p>
<nav><a href="#decide">Your {len(X['decisions'])} decisions</a><a href="#minute">First minute</a><a href="#key">Chroma key</a><a href="#colour">Colour</a><a href="#bg">Background</a><a href="#voice">Voice</a><a href="#decided">What I decided</a><a href="#gfx">Graphics in context</a><a href="#pending">Coming next round</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(X['decisions'])})</h2><ol>{''.join('<li>' + d + '</li>' for d in X['decisions'])}</ol></section>
<section id="minute"><h2>The first minute (0:00 to {mmss(fm['end'])})</h2><video controls preload="none" playsinline poster="{fm['poster']}" src="{fm['review']}"></video>
<p class="small"><a href="{fm['master']}">1080p</a> · {fm['links']}</p><p class="small">{fm['note']}</p></section>
<section id="key"><h2>The chroma key</h2><p class="small">{X['key_intro']}</p><div class="grid">{key_html}</div>
<table>{''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>' for a, b, c in X['key_numbers'])}</table></section>
<section id="colour"><h2>Colour (3 options on the same frame)</h2><p class="small">{X['colour_intro']}</p><div class="grid">{col_html}</div></section>
<section id="bg"><h2>What is behind you (3 options)</h2><p class="small">{X['bg_intro']}</p><div class="grid">{bg_html}</div></section>
<section id="voice"><h2>Voice (the same 26 seconds, level matched)</h2><p class="small">{X['voice_intro']}</p><div class="grid">{voice_html}</div></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + d + '</li>' for d in X['decided'])}</ul></section>
<section id="gfx"><h2>The two graphics in the first minute, in context</h2><div class="grid">{gfx_html}</div></section>
<section id="pending"><h2>Coming next round (after the key, colour and voice are locked)</h2><ul>{''.join('<li>' + d + '</li>' for d in X['pending'])}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + d + '</li>' for d in X['checks'])}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(X['reply'])}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id;v.play();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth'}});}}</script></html>"""
open(f'{OUT}/index.html', 'w').write(page); print('page ok')
