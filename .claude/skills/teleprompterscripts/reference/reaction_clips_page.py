#!/usr/bin/env python3
"""Review page for reaction clips: my pick and up to two alternates per clip, one shared player (2026-10-12).

    python3 reaction_clips_page.py page.json out_dir
    python3 .claude/skills/_shared/review_server.py PORT out_dir      # serve it (never python -m http.server)

page.json: {"title": "...", "intro": "...", "decided": ["line", ...], "check": ["optional: script lines the clip does not back up"],
            "sections": [{"title": "video title", "set": "Green screen",
                          "slots": [{"slot": "CEL-1", "label": "Sharon Osbourne", "source": "E! News, ...",
                                     "video_id": "oZTHGIoqwI4",
                                     "options": [{"rank": "recommended", "start": 12, "end": 34, "first_words": "...",
                                                  "last_words": "...", "text": "...", "why": "..."}, ...]},   (an option may carry its own "video_id" and "source")
                                    {"info": "Elon Musk's two posts: on-screen text, nothing to choose", "links": [["label", "url"]]}]}]}
Layout follows PRE-RENDER-APPROVAL.md: decisions on top, "What I decided", three cards per row, ONE player in a
fixed panel on the right, one reply box with a Copy button. YouTube clips play in the shared player from start to end.
"""
import json, sys, os, html
E = html.escape
def ts(s):
    s = int(s); return '%d:%02d:%02d' % (s // 3600, s % 3600 // 60, s % 60) if s >= 3600 else '%d:%02d' % (s // 60, s % 60)
NAMES = {'recommended': 'MY PICK', 'alt1': 'ALTERNATE 1', 'alt2': 'ALTERNATE 2'}
CSS = '''
:root{--bg:#f6f7f9;--card:#fff;--ink:#16181d;--mute:#5b6270;--line:#dfe3ea;--pick:#0b6bcb;--pickbg:#eaf3ff;--ok:#12784a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
main{max-width:1180px;margin:0 auto;padding:22px 20px 80px}
@media(min-width:1500px){main{margin:0 500px 0 auto;max-width:none;padding-left:32px}#dock{position:fixed;right:16px;top:16px;width:460px}}
@media(max-width:1499px){#dock{position:sticky;top:0;z-index:5;max-width:640px;margin:0 auto 14px}}
#dock{background:#111;border-radius:10px;padding:10px;color:#fff}#dock .frame{position:relative;padding-top:56.25%;background:#000;border-radius:6px;overflow:hidden}
#dock iframe{position:absolute;inset:0;width:100%;height:100%;border:0}#now{font-size:13px;margin:8px 2px 2px;color:#cfd5df;min-height:36px}
h1{font-size:24px;margin:0 0 6px}h2{font-size:19px;margin:34px 0 4px;padding-top:14px;border-top:2px solid var(--line)}h3{font-size:15px;margin:18px 0 8px}
.set{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mute)}
.box{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:12px 0}.box ul{margin:6px 0 0 18px;padding:0}.box li{margin:3px 0}
.row{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}@media(max-width:900px){.row{grid-template-columns:1fr}}
.card{background:var(--card);border:2px solid var(--line);border-radius:10px;padding:12px;display:flex;flex-direction:column;gap:8px}
.card.sel{border-color:var(--pick);background:var(--pickbg)}.tag{font-size:11px;font-weight:700;letter-spacing:.07em;color:var(--mute)}.card.sel .tag{color:var(--pick)}
.time{font-size:17px;font-weight:650}.why{color:var(--ink)}.q{color:var(--mute);font-size:13.5px}details{font-size:13.5px;color:var(--mute)}summary{cursor:pointer}
.btns{display:flex;gap:8px;flex-wrap:wrap;margin-top:auto}button,a.b{font:inherit;font-size:14px;border-radius:7px;border:1px solid var(--line);background:#fff;padding:7px 11px;cursor:pointer;color:var(--ink);text-decoration:none}
button.play{background:#111;color:#fff;border-color:#111}button.use{border-color:var(--pick);color:var(--pick)}.card.sel button.use{background:var(--pick);color:#fff}
.info{background:#fff;border:1px dashed var(--line);border-radius:10px;padding:10px 14px;margin:8px 0;color:var(--mute)}
textarea{width:100%;min-height:150px;font:14px/1.4 ui-monospace,Menlo,monospace;border:1px solid var(--line);border-radius:8px;padding:10px}
#copied{color:var(--ok);margin-left:10px}
'''
JS = '''
const sel={};const labels={};
function play(id,s,e,what){document.getElementById('player').src='https://www.youtube.com/embed/'+id+'?start='+s+'&end='+e+'&autoplay=1&rel=0';document.getElementById('now').textContent=what;}
function use(slot,rank){sel[slot]=rank;document.querySelectorAll('[data-slot="'+slot+'"]').forEach(c=>c.classList.toggle('sel',c.dataset.rank===rank));try{localStorage.setItem(KEY,JSON.stringify(sel))}catch(e){}reply();}
function reply(){const ch=Object.keys(labels).filter(k=>sel[k]&&sel[k]!=='recommended');const t=document.getElementById('reply');const note=t.dataset.note||'';
 let s=ch.length?('Use my picks for everything except:\\n'+ch.map(k=>'- '+k+' '+labels[k].name+': use '+labels[k][sel[k]]).join('\\n')):'All of your picks are approved.';t.value=s+(note?'\\n\\nNotes: '+note:'\\n\\nNotes: ');}
function copyReply(){const t=document.getElementById('reply');navigator.clipboard.writeText(t.value).then(()=>{document.getElementById('copied').textContent='Copied. Paste it in the chat.'});}
window.addEventListener('DOMContentLoaded',()=>{try{Object.assign(sel,JSON.parse(localStorage.getItem(KEY)||'{}'))}catch(e){}Object.keys(labels).forEach(k=>use(k,sel[k]||'recommended'));});
'''
def build(page):
    labels = {}; n_slots = 0; body = []
    cur_set = None
    for sec in page['sections']:
        if sec.get('set') != cur_set:
            cur_set = sec.get('set'); body.append('<div class="set" style="margin-top:30px">%s</div>' % E(cur_set or ''))
        body.append('<h2>%s</h2>' % E(sec['title']))
        for sl in sec['slots']:
            if 'info' in sl:
                links = ' '.join('<a class="b" target="_blank" href="%s">%s</a>' % (E(u), E(l)) for l, u in sl.get('links', []))
                body.append('<div class="info">%s %s</div>' % (E(sl['info']), links)); continue
            n_slots += 1; slot = sl['slot']
            labels[slot] = {'name': sl['label']}
            body.append('<h3>%s &nbsp;<span class="q">%s. %s</span></h3><div class="row">' % (E(slot), E(sl['label']), E(sl.get('source', ''))))
            for o in sl['options']:
                rng = '%s to %s' % (ts(o['start']), ts(o['end'])); ln = o['end'] - o['start']
                labels[slot][o['rank']] = '%s (%s)' % (NAMES[o['rank']].lower(), rng)
                what = '%s, %s: %s, %d seconds' % (sl['label'], NAMES[o['rank']].lower(), rng, ln)
                vid = o.get('video_id', sl.get('video_id'))   # an option may come from its own video (2026-10-12)
                yt = 'https://www.youtube.com/watch?v=%s&t=%ds' % (vid, o['start'])
                body.append('''<div class="card" data-slot="%s" data-rank="%s"><div class="tag">%s</div><div class="time">%s <span class="q">(%d s)</span></div>
<div class="why">%s</div><div class="q">Starts: "%s"<br>Ends: "%s"</div><details><summary>All the words</summary>%s</details>
<div class="btns"><button class="play" onclick="play('%s',%d,%d,%s)">&#9654; Play</button><button class="use" onclick="use('%s','%s')">Use this one</button><a class="b" target="_blank" href="%s">YouTube</a></div></div>''' % (
                    E(slot), o['rank'], NAMES[o['rank']], rng, ln, E((o['source'] + '. ' if o.get('source') else '') + o.get('why', '')), E(o.get('first_words', '')), E(o.get('last_words', '')), E(o.get('text', '')),
                    vid, o['start'], o['end'], E(json.dumps(what)), E(slot), o['rank'], E(yt)))
            body.append('</div>')
    head = '''<h1>%s</h1><div>%s</div>
<div class="box"><b>Your decisions (%d clips).</b> My pick is first in every row and already selected. Press Play to watch a clip in the player. If you like an alternate better, press "Use this one" on it. When you are done, copy the reply at the bottom into the chat. If you change nothing, my picks go in.</div>
<div class="box"><b>What I decided (overrule anything)</b><ul>%s</ul></div>%s''' % (E(page['title']), E(page['intro']), n_slots, ''.join('<li>%s</li>' % E(x) for x in page['decided']),
        ('<div class="box" style="border-color:#c98a00"><b>%s</b><ul>%s</ul></div>' % (E(page.get('check_title', 'Check before you film')), ''.join('<li>%s</li>' % E(x) for x in page['check']))) if page.get('check') else '')
    foot = '<h2>Your reply</h2><div class="box"><textarea id="reply"></textarea><div style="margin-top:8px"><button class="play" onclick="copyReply()">Copy reply</button><span id="copied"></span></div></div>'
    dock = '<div id="dock"><div class="frame"><iframe id="player" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div><div id="now">Press Play on any clip. It plays here from its first second to its last.</div></div>'
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title><style>%s</style></head><body>%s<main>%s%s%s</main><script>const KEY=%s;%s\nObject.assign(labels,%s);</script></body></html>'
            % (E(page['title']), CSS, dock, head, '\n'.join(body), foot, json.dumps('clips-' + page['title']), JS, json.dumps(labels))), n_slots
if __name__ == '__main__':
    page = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    s, n = build(page); open(os.path.join(out, 'index.html'), 'w').write(s)
    print('wrote', os.path.join(out, 'index.html'), '|', n, 'clips to decide |', len(s) // 1024, 'KB')
