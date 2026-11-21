#!/usr/bin/env python3
"""One page that plays every reaction clip of a shoot in filming order, each in its exact window (2026-11-13).

    python3 clip_player_page.py SOURCE.txt OUT_DIR "Page title" [--no-embed ID,ID,...]

SOURCE.txt is the text export of a filming scripts Doc: a "A15 · Title" line starts a script, a line that starts
with [ and ends with ] is a cue. Every cue that carries a YouTube id followed by times ("0:31 TO 0:37, THEN 0:45
TO 0:53") becomes one clip with one or more windows. Writes OUT_DIR/index.html (one shared YouTube player that plays
each window and stops) and OUT_DIR/clips.json. Serve it with _shared/review_server.py; nothing plays until a click.
Ids given with --no-embed (their owner blocks playing on other sites: the player reports error 150) get an
"Open on YouTube" link, unless OUT_DIR/clips/<id>_<start>_<end>.mp4 exists for every window of the clip: then the
page plays those local files instead (download them with yt-dlp --download-sections; see the skill).
"""
import html, json, os, re, sys

T = r"(?:(\d+):)?(\d+):(\d\d)"


def secs(h, m, s): return (int(h) if h else 0) * 3600 + int(m) * 60 + int(s)
def clock(n): return "%d:%02d" % (n // 60, n % 60)


def parse(path):
    scripts, cur = [], None
    for line in open(path, encoding="utf-8").read().replace("﻿", "").split("\n"):
        t = line.strip()
        m = re.match(r"^([A-Z]+\d*|TESLA) · (.+)$", t)
        if m:
            cur = {"id": m.group(1), "title": m.group(2), "clips": []}; scripts.append(cur); continue
        if not cur or not (t.startswith("[") and t.endswith("]")): continue
        for m in re.finditer(r"(?<![A-Za-z0-9_-])([A-Za-z0-9_-]{11}),\s*(?=\d+:\d\d)", t):
            vid = m.group(1)
            if not (re.search(r"[a-z]", vid) and re.search(r"[A-Z0-9_-]", vid)): continue
            rest = t[m.end():]
            nxt = re.search(r"(?<![A-Za-z0-9_-])[A-Za-z0-9_-]{11},\s*\d+:\d\d", rest)
            if nxt: rest = rest[:nxt.start()]
            wins = [(secs(*p[:3]), secs(*p[3:])) for p in re.findall(T + r"\s+TO\s+" + T, rest)]
            if not wins:
                one = re.search(T, rest); wins = [(secs(*one.groups()), secs(*one.groups()) + 20)]
            label = t.strip("[]")
            label = re.sub(r"^(COLD )?OPEN ON (THE )?CLIP[^:]*:\s*|^PLAY CLIP \d+[^:]*:\s*", "", label)
            cur["clips"].append({"vid": vid, "wins": wins, "label": label})
    return [s for s in scripts if s["clips"]]


PAGE = r"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>__TITLE__</title><style>
:root{--bg:#0f1216;--panel:#181c22;--line:#2a3038;--text:#e9edf2;--mute:#97a1ad;--acc:#4da3ff;--done:#3c8f5a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.45 -apple-system,Helvetica,Arial,sans-serif}
.wrap{display:grid;grid-template-columns:340px 1fr;height:100vh}
.side{overflow:auto;border-right:1px solid var(--line);background:var(--panel);padding:10px 0}
.side h1{font-size:15px;margin:4px 14px 10px}.side .sub{color:var(--mute);font-size:12px;margin:0 14px 10px}
.vid{font-size:12px;color:var(--mute);margin:14px 14px 4px;text-transform:none;font-weight:600}
.clip{display:block;width:100%;text-align:left;background:none;border:0;border-left:3px solid transparent;color:var(--text);padding:7px 14px;font:inherit;font-size:13px;cursor:pointer}
.clip:hover{background:#20262e}.clip.on{border-left-color:var(--acc);background:#1d2530}.clip.seen{color:var(--mute)}.clip.seen:before{content:"\2713  ";color:var(--done)}
.clip small{color:var(--mute);display:block}
.main{display:flex;flex-direction:column;min-width:0;padding:16px 20px;gap:12px;overflow:auto}
.stage{position:relative;width:100%;max-width:1100px;aspect-ratio:16/9;background:#000;border-radius:8px;overflow:hidden}
.stage #player,.stage iframe,.stage video{position:absolute;inset:0;width:100%;height:100%}
.stage video{display:none;background:#000}
.note{position:absolute;inset:0;display:none;align-items:center;justify-content:center;text-align:center;padding:30px;background:#000c;font-size:17px}
.note a{color:var(--acc)}
h2{font-size:19px;margin:0}.lab{color:var(--mute);font-size:13px;margin:0}
.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
button.b{background:#232a33;color:var(--text);border:1px solid var(--line);border-radius:7px;padding:9px 14px;font:inherit;cursor:pointer}
button.b.p{background:var(--acc);border-color:var(--acc);color:#04121f;font-weight:600}
a.yt{color:var(--acc);font-size:13px}.count{color:var(--mute);font-size:13px;margin-left:auto}
@media(max-width:820px){.wrap{grid-template-columns:1fr;height:auto}.side{max-height:38vh;border-right:0;border-bottom:1px solid var(--line)}}
</style></head><body><div class="wrap">
<div class="side"><h1>__TITLE__</h1><p class="sub">__N__ clips in filming order. Click a clip and it plays only its window, then stops. Nothing plays until you click.</p><div id="list"></div></div>
<div class="main"><h2 id="t">Pick a clip on the left</h2><p class="lab" id="l"></p>
<div class="stage"><div id="player"></div><video id="local" playsinline controls preload="none"></video><div class="note" id="note"></div></div>
<div class="bar"><button class="b p" id="play">Play clip</button><button class="b" id="replay">Replay</button><button class="b" id="prev">Previous</button><button class="b" id="next">Next clip</button><a class="yt" id="yt" target="_blank" rel="noopener">Open on YouTube at this second</a><span class="count" id="c"></span></div>
<p class="lab">Keys: N next, P previous, R replay, space play or pause.</p></div></div>
<script>
const DATA=__DATA__, NOEMBED=new Set(__NOEMBED__);
const flat=[];DATA.forEach(s=>s.clips.forEach(c=>flat.push(Object.assign({sid:s.id,title:s.title},c))));
const clock=n=>Math.floor(n/60)+":"+String(n%60).padStart(2,"0");
const list=document.getElementById("list");let cur=-1,win=0,player=null,ready=false,timer=null,pending=false;
const local=document.getElementById("local");
function showLocal(on){local.style.display=on?"block":"none";if(!on){local.pause();}else if(ready){player.stopVideo();}}
local.addEventListener("ended",()=>{const c=flat[cur];if(c&&c.files&&win<c.files.length-1){win++;local.src=c.files[win];local.play();}});
DATA.forEach(s=>{const h=document.createElement("div");h.className="vid";h.textContent=s.title+" ("+s.id+")";list.appendChild(h);});
(function(){let i=0;const heads=[...list.querySelectorAll(".vid")];DATA.forEach((s,k)=>{let after=heads[k];s.clips.forEach(c=>{const b=document.createElement("button");b.className="clip";b.dataset.i=i;
b.innerHTML="";const span=document.createElement("span");span.textContent=c.wins.map(w=>clock(w[0])+" to "+clock(w[1])).join(", then ");const sm=document.createElement("small");sm.textContent=c.label.slice(0,90);b.appendChild(span);b.appendChild(sm);
const n=i;b.onclick=()=>select(n,true);after.after(b);after=b;i++;});});})();
function ytUrl(c,w){return "https://www.youtube.com/watch?v="+c.vid+"&t="+c.wins[w||0][0]+"s";}
function note(msg){const n=document.getElementById("note");if(!msg){n.style.display="none";return;}n.innerHTML=msg;n.style.display="flex";}
function select(i,play){if(i<0||i>=flat.length)return;cur=i;win=0;const c=flat[i];
 document.querySelectorAll(".clip").forEach(b=>b.classList.toggle("on",+b.dataset.i===i));
 const on=document.querySelector(".clip.on");if(on)on.scrollIntoView({block:"nearest"});
 document.getElementById("t").textContent=c.title+" ("+c.sid+")";document.getElementById("l").textContent=c.label;
 document.getElementById("yt").href=ytUrl(c,0);document.getElementById("c").textContent="Clip "+(i+1)+" of "+flat.length;
 clearInterval(timer);
 if(c.files){note("");showLocal(true);local.src=c.files[0];local.load();if(play)start();return;}
 showLocal(false);
 if(NOEMBED.has(c.vid)){if(ready)player.stopVideo();note('This video cannot play inside another page.<br><br><a target="_blank" rel="noopener" href="'+ytUrl(c,0)+'">Open it on YouTube at '+clock(c.wins[0][0])+'</a><br><br>Stop it at '+clock(c.wins[c.wins.length-1][1])+'.');mark(i);return;}
 note("");if(!ready){pending=play;return;}
 if(play)start();else player.cueVideoById({videoId:c.vid,startSeconds:c.wins[0][0]});}
function start(){const c=flat[cur];if(!c)return;
 if(c.files){if(!local.src.endsWith(c.files[win]))local.src=c.files[win];local.currentTime=0;local.play();mark(cur);return;}
 if(NOEMBED.has(c.vid)||!ready)return;const w=c.wins[win];
 player.loadVideoById({videoId:c.vid,startSeconds:w[0]});mark(cur);clearInterval(timer);
 timer=setInterval(()=>{if(!player.getCurrentTime)return;const t=player.getCurrentTime(),w=flat[cur].wins[win];
  if(t>=w[1]){if(win<flat[cur].wins.length-1){win++;player.seekTo(flat[cur].wins[win][0],true);}else{player.pauseVideo();clearInterval(timer);}}},150);}
function mark(i){const b=document.querySelector('.clip[data-i="'+i+'"]');if(b)b.classList.add("seen");}
document.getElementById("play").onclick=()=>{if(cur<0)select(0,true);else{win=0;start();}};
document.getElementById("replay").onclick=()=>{if(cur>=0){win=0;start();}};
document.getElementById("next").onclick=()=>select(cur+1,true);document.getElementById("prev").onclick=()=>select(cur-1,true);
document.addEventListener("keydown",e=>{if(e.target.tagName==="INPUT")return;const k=e.key.toLowerCase();
 if(k==="n")select(cur+1,true);else if(k==="p")select(cur-1,true);else if(k==="r"){win=0;start();}
 else if(k===" "){e.preventDefault();if(cur<0)return;if(flat[cur].files){if(local.paused)local.play();else local.pause();return;}if(!ready)return;const s=player.getPlayerState();if(s===1)player.pauseVideo();else if(s===2)player.playVideo();else{win=0;start();}}});
window.onYouTubeIframeAPIReady=()=>{player=new YT.Player("player",{playerVars:{rel:0,modestbranding:1,playsinline:1},events:{
 onReady:()=>{ready=true;if(cur>=0){if(pending)start();else select(cur,false);}},
 onError:e=>{const c=flat[cur];if(!c)return;clearInterval(timer);note('This video would not play here (YouTube code '+e.data+').<br><br><a target="_blank" rel="noopener" href="'+ytUrl(c,0)+'">Open it on YouTube at '+clock(c.wins[0][0])+'</a><br><br>Stop it at '+clock(c.wins[c.wins.length-1][1])+'.');}}});};
window.__clips={flat:flat,state:()=>({cur:cur,win:win,ready:ready,local:{shown:local.style.display==="block",paused:local.paused,t:local.currentTime,muted:local.muted,src:local.src.split("/").pop()},ps:ready?player.getPlayerState():null,t:ready&&player.getCurrentTime?player.getCurrentTime():null,muted:ready&&player.isMuted?player.isMuted():null})};
const s=document.createElement("script");s.src="https://www.youtube.com/iframe_api";document.head.appendChild(s);
</script></body></html>"""


def main():
    src, out, title = sys.argv[1], sys.argv[2], sys.argv[3]
    noembed = sys.argv[sys.argv.index("--no-embed") + 1].split(",") if "--no-embed" in sys.argv else []
    scripts = parse(src); os.makedirs(out, exist_ok=True); nlocal = 0
    for s in scripts:
        for c in s["clips"]:
            files = ["clips/%s_%d_%d.mp4" % (c["vid"], a, b) for a, b in c["wins"]]
            if all(os.path.getsize(os.path.join(out, f)) > 1000 if os.path.exists(os.path.join(out, f)) else False for f in files):
                if len(files) > 1:   # one file per clip: the review helper allows a play only from the viewer's own click
                    joined = "clips/%s_%s.mp4" % (c["vid"], "__".join("%d_%d" % w for w in c["wins"]))
                    if not os.path.exists(os.path.join(out, joined)):
                        import subprocess
                        ff = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../Media/video_edit/bin/ffmpeg")
                        ff = ff if os.path.exists(ff) else "ffmpeg"
                        cmd = [ff, "-v", "error", "-y"] + sum([["-i", os.path.join(out, f)] for f in files], [])
                        cmd += ["-filter_complex", "".join("[%d:v][%d:a]" % (i, i) for i in range(len(files))) + "concat=n=%d:v=1:a=1[v][a]" % len(files),
                                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", os.path.join(out, joined)]
                        subprocess.run(cmd, check=True)
                    files = [joined]
                c["files"] = files; nlocal += 1
    n = sum(len(s["clips"]) for s in scripts)
    json.dump(scripts, open(os.path.join(out, "clips.json"), "w"), ensure_ascii=False, indent=1)
    page = (PAGE.replace("__TITLE__", html.escape(title)).replace("__N__", str(n))
            .replace("__DATA__", json.dumps(scripts, ensure_ascii=False).replace("</", "<\\/")).replace("__NOEMBED__", json.dumps(noembed)))
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(page)
    for s in scripts:
        print("%-6s %2d clips  %s" % (s["id"], len(s["clips"]), s["title"][:70]))
        for c in s["clips"]:
            if any(b <= a or b - a > 90 for a, b in c["wins"]): print("    CHECK WINDOW", c["vid"], [(clock(a), clock(b)) for a, b in c["wins"]], c["label"][:70])
    blocked = [(s["id"], c["vid"]) for s in scripts for c in s["clips"] if c["vid"] in noembed and "files" not in c]
    print("scripts:", len(scripts), "| clips:", n, "| windows:", sum(len(c["wins"]) for s in scripts for c in s["clips"]),
          "| played from local files:", nlocal, "| still YouTube-only:", len(blocked))


if __name__ == "__main__":
    main()
