#!/usr/bin/env python3
"""Package the isolated graphics proof in the shared review-page format."""
from pathlib import Path
import argparse
import html
import json
import shutil


def main(source, dest):
    receipt = json.loads((source/'proof-receipt.json').read_text())
    words = json.loads((source/'words_out.json').read_text())
    beats = json.loads((source/'hf/beats.json').read_text())
    plan = json.loads((source/'plan_resolved.json').read_text())
    a=receipt['range'][0]
    dest.mkdir(parents=True,exist_ok=True)
    for name in ('old.mp4','new.mp4','original-draft.mp4','proof-receipt.json','new.mp4.edit-sheet.json'):
        shutil.copy2(source/name,dest/name)
    for folder in ('stills','context'):
        shutil.copytree(source/folder,dest/folder,dirs_exist_ok=True)
    shutil.copy2(source/'hf/BEATS.md',dest/'BEATS.md')
    shutil.copy2(source/'checks/checks.json',dest/'checks.json')
    cards=[]
    for it,b in zip(plan,beats):
        title={'alternatives':'Four protein snacks','chipotle':'Chipotle protein cup: $7'}[it['id']]
        copy=it.get('points') or [it['topic'],it['point']]
        speech=[]
        for label,lo,hi in [('Before',it['t0']-3,it['t0']),('During',it['t0'],it['t1']),('After',it['t1'],it['t1']+3)]:
            speech.append('<p><b>'+label+':</b> '+html.escape(' '.join(w['w'] for w in words if lo<=w['t0']<hi))+'</p>')
        rows=''.join(f"<tr><td>{r['t']:.2f}</td><td>{html.escape(r['word'])}</td><td>{html.escape(r['beat'])}</td></tr>" for r in b['rows'])
        cards.append(f'''<article><h3>{html.escape(title)}</h3><p>{it['id']} | film {it['t0']:.2f} to {b['b']:.2f}s | {b['template']}</p><a href="stills/{it['id']}-new.jpg"><img src="stills/{it['id']}-new.jpg" alt="{html.escape(title)} on its real frame"></a><p><b>Exact copy:</b> {html.escape(' / '.join(copy))}</p><p>Source: RO-17 clean graded picture, existing C1713 cut.</p><button onclick="playContext('{it['id']}')">Play it moving, in context</button><details><summary>Speech before / during / after</summary>{''.join(speech)}</details><details><summary>Word-by-word motion plan</summary><table><thead><tr><th>Film seconds</th><th>Spoken words</th><th>What moves</th></tr></thead><tbody>{rows}</tbody></table></details><details><summary>Old graphic treatment</summary><img src="stills/{it['id']}-old.jpg" alt="Old graphic on its frame"><p>Old list still is taken while its original graphic was visible, at 348s. New list still is at 389s after all four foods have been named.</p></details></article>''')
    items={it['id']:it for it in receipt['checks']['items']}
    check=f"Checked every tenth frame. Side-card clearance: {items['alternatives']['min_clear']} px. Face clearance over the lower third: {items['chipotle']['min_face_gap']} px. Shared graphics checks: PASS. Both players carry identical encoded audio. Original RO-17 file hashes are unchanged."
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>RO-17: HyperFrames comparison</title><style>
    *{box-sizing:border-box}body{margin:0;background:#091827;color:#e8f1f7;font:17px/1.5 system-ui}main{max-width:1600px;margin:auto;padding:32px}h1{font-size:32px}h2{color:#85cef0}a{color:#88d6fa}section{margin:28px 0}video,img{width:100%;border-radius:12px}video{background:#000;aspect-ratio:16/9}.comparison{display:grid;grid-template-columns:1fr 1fr;gap:22px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}article,.box{padding:20px;background:#102b43;border:1px solid #285672;border-radius:16px}button{background:#87d7f2;color:#062038;border:0;border-radius:8px;padding:12px 18px;cursor:pointer;font-weight:700;margin:5px 4px 5px 0}details{margin-top:16px}summary{cursor:pointer;color:#a4dcf7}table{font-size:13px;width:100%;border-collapse:collapse}td,th{border-bottom:1px solid #285672;padding:6px;text-align:left}textarea{width:100%;min-height:90px;padding:12px;font:16px system-ui}#dock{position:sticky;top:20px}.subtle{color:#b6c9d7}
    @media(min-width:1800px){main{margin-right:440px;max-width:1450px}#dock{position:fixed;right:24px;top:70px;width:395px}}@media(max-width:900px){main{padding:18px}.comparison{grid-template-columns:1fr}.grid{grid-template-columns:1fr}#dock{position:static}}
    </style><main><header><h1>RO-17: shared HyperFrames graphics</h1><p>One 59.99-second comparison, from 5:38 to 6:38 of the existing Codex draft.</p><p><b>Locked:</b> existing source cuts, grade, spoken wording and audio. No approved video has been replaced or uploaded.</p><div class="box"><b>Your decisions (1)</b><p>Does this implementation look right for future Codex videos? Recommended: approve. Or name the change you want.</p></div></header>
    <section><h2>Old versus new</h2><p>Both players use the same clean presenter picture, fixed side framing and original audio. Existing draft stock placeholders are excluded from both so they do not distract from the graphics comparison. The old graphic keeps its saved copy and timing. The new list waits for each food's spoken name, so it lasts longer.</p><div class="comparison"><div><h3>Old Codex graphics</h3><video id="old" controls preload="none" src="old.mp4"></video><a href="old.mp4">1080p old treatment</a></div><div><h3>Shared HyperFrames graphics</h3><video id="new" controls preload="none" src="new.mp4"></video><a href="new.mp4">1080p new treatment</a></div></div><p><button onclick="pair()">Play both together (new audio only)</button><button onclick="pausePair()">Pause both</button><button onclick="resetPair()">Restart comparison</button></p><p><a href="original-draft.mp4">Original draft excerpt, including its original framing and placeholders</a></p></section>
    <section><h2>What I decided (overrule anything)</h2><ul><li>Keep all four snack names and the exact Chipotle price wording.</li><li>Reveal sardines, eggs, chicken and the protein cup as you name them, rather than showing the complete list early.</li><li>Reveal $7 on your spoken seven. Use the approved glass lower third.</li><li>Keep the list without a new heading, preserving the original copy.</li><li>Give both comparison players the same steady side composition so your arms remain clear of the larger card.</li><li>Use the shared templates and shared colour/blur compositor. No new template, no paid generation and no entrance sound.</li></ul></section><section class="box"><h2>Checks</h2><p>__CHECK__</p><p><a href="checks.json">Graphics measurements</a> | <a href="new.mp4.edit-sheet.json">Validated proof edit sheet</a> | <a href="proof-receipt.json">Proof record</a> | <a href="BEATS.md">Beat sheet</a></p><p class="subtle">This is a graphics-method proof awaiting your review, not a delivery approval for the full film.</p></section>
    <aside id="dock" class="box"><b id="contextTitle">Graphic in context</b><video id="context" controls preload="none"></video><p class="subtle">Use the buttons below. This shared player stays at the side on a wide screen.</p></aside><section><h2>Every graphic, in order</h2><div class="grid">__CARDS__</div></section><section class="box"><h2>Your reply</h2><textarea id="reply">HyperFrames Codex adoption: approve / change:</textarea><button onclick="copyReply()">Copy reply</button><span id="copyStatus"></span></section></main><script>
    const o=document.getElementById('old'),n=document.getElementById('new');
    async function pair(){o.muted=true;n.muted=false;for(const v of [o,n]){v.preload='auto';if(v.readyState===0)v.load()}await Promise.all([o.play(),n.play()]);o.currentTime=n.currentTime;}
    function pausePair(){o.pause();n.pause()}
    function resetPair(){pausePair();o.currentTime=0;n.currentTime=0}
    n.addEventListener('seeked',()=>{if(Math.abs(o.currentTime-n.currentTime)>.12)o.currentTime=n.currentTime});
    const names={'alternatives':'Four protein snacks','chipotle':'Chipotle protein cup'};
    function playContext(id){const v=document.getElementById('context');v.src='context/'+encodeURIComponent(id+'-context - REVIEW 540p.mp4');v.load();document.getElementById('contextTitle').textContent=names[id];v.play()}
    async function copyReply(){try{await navigator.clipboard.writeText(document.getElementById('reply').value);document.getElementById('copyStatus').textContent='Copied'}catch(e){document.getElementById('reply').select();document.execCommand('copy');document.getElementById('copyStatus').textContent='Copied'}}
    </script></html>'''.replace('__CHECK__',html.escape(check)).replace('__CARDS__',''.join(cards))
    assert '\u2014' not in page and '\u2013' not in page
    (dest/'index.html').write_text(page)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('dest',type=Path);a=ap.parse_args();main(a.source,a.dest)
