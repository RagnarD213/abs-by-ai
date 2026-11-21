"""RO-19 round 3 review page (later round: the full film, and only what changed). Order: decisions, the full film, the revision list with exact times and watch
ranges, the first minute, the three new AI clips, the two changed photos, the close, What I decided, the checks stated plainly, one reply box.
Text that depends on the checks comes from round3/page_notes.json (written after the gates and the independent review). Writes round3/index.html.
Serve with _shared/review_server.py 8866 round3."""
import json, os, html, shutil, subprocess
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro19"; O = f"{W}/round3"; e = html.escape; FPS = 30000/1001
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
R = {r["id"]: r for r in json.load(open(f"{W}/plan_resolved.json"))}; S = json.load(open(f"{W}/shots.json")); TOTAL = S[-1]["out_f1"]/FPS
N = json.load(open(f"{O}/page_notes.json")); FILM = f"{O}/film/RO-19 round 3 - full film.mp4"
def mmss(t): return f"{int(t//60)}:{int(t%60):02d}"
def rng(i, pad=0): return f"{mmss(R[i]['t0']-pad)} to {mmss(R[i]['t1']+pad)}"
for d in ("stills", "motion-takes", "frames"): os.makedirs(f"{O}/{d}", exist_ok=True)
def still(name, t):
    p = f"{O}/stills/{name}.jpg"
    subprocess.run([FF, "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", FILM, "-frames:v", "1", "-vf", "scale=960:540", "-q:v", "3", p], check=True); return f"stills/{name}.jpg"
for i in ("A5", "G1", "G3"): shutil.copy(f"{W}/round3/motion/{i}-t1.mp4", f"{O}/motion-takes/{i}-take1.mp4")
for a, b in (("pale2_down", "P04-old-pale-half"), ("pale3_down", "P04-new-pale-half"), ("pale2_single", "P02-old"), ("pale3_single", "P02-new")):
    Image.open(f"{W}/photos/{a}.jpg").resize((600, 750), Image.LANCZOS).save(f"{O}/stills/{b}.jpg", quality=90)
def play(i, label="Play it in context"): return f"<a class='btn' href='review/{i}-context - REVIEW 540p.mp4' onclick=\"return play(this,'{i}')\">{label}</a>"
def seek(t, label=None): return f"<a href='#film' onclick=\"return jump({t:.1f})\">{label or mmss(t)}</a>"
REV = sorted(N["revisions"], key=lambda r: (not r.get("whole"), R[r["id"]]["t0"] if r.get("id") else r["t0"]))          # whole-film rows first, then in film order
css = open(f"{W}/recipe/page20.py").read().split('css = """')[1].split('"""')[0] + ".three{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.rev td{padding:7px 14px 7px 0;border-top:1px solid #26354d}.rev th{text-align:left;color:#9fb2cc;font-weight:600;padding-right:14px}.ok{color:#7be08f}.no{color:#ffb86b}"
h = [f"<!doctype html><meta charset='utf-8'><title>RO-19 round 3</title><style>{css}</style>",
     "<div id='dock'><div class='muted' id='docklabel'>Play any clip in context: press its button</div><video id='player' controls preload='none'></video></div><main>",
     "<h1>My First Spray Tan: round 3, the full film</h1>",
     f"<div class='sub'>Long-form content, 16:9, {mmss(TOTAL)}. Your round 2 notes are in, and this is the first time the whole film exists. Nothing is uploaded or queued.</div>",
     f"<p><b>Already locked and unchanged:</b> {e(N['locked'])}</p>", f"<h2>Your decisions ({len(N['decisions'])})</h2>"]
for k, d in enumerate(N["decisions"], 1):
    h.append(f"<div class='dec'><b>{k}. {e(d['t'])}.</b> {e(d['why'])}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in d['opts'])}</div></div>")
h += ["<h2 id='film'>The full film</h2>", f"<video id='big' class='big' controls preload='none' poster='{still('film-poster', 1.5)}' src='review/full-film - REVIEW 540p.mp4'></video>",
      f"<p class='muted'>This player is the 540p review copy. <a href='film/RO-19 round 3 - full film.mp4'>Full 1080p file</a> &middot; <a href='film/RO-19 audio AB (reference then ours).mp4'>Sound A/B: the reference voice, then this film</a> &middot; <a href='film/RO19.srt'>captions file</a> &middot; <a href='film/RO19.chapters.txt'>chapters</a><br>"
      f"For VLC, in the project folder: <b>Videos to Review / {e(N['vlc_film'])}</b> and <b>{e(N['vlc_first'])}</b></p>",
      "<h2>What changed, and where to look</h2><p class='muted'>Click a time to move the film above to a few seconds before it. You do not need to watch the whole film to check these.</p><table class='rev'><tr><th>Where</th><th>Watch</th><th>What it was</th><th>What it is now</th><th></th></tr>"]
for r in REV:
    if r.get("id"): t0, t1 = R[r["id"]]["t0"], R[r["id"]]["t1"]
    else: t0, t1 = r["t0"], r["t1"]
    a, b = max(0, t0 - r.get("pad", 4)), min(TOTAL, t1 + r.get("pad", 4))
    where = "whole film" if r.get("whole") else f"{mmss(t0)} to {mmss(t1)}"
    btn = play(r["id"], "Play") if r.get("clip") else ""
    h.append(f"<tr><td><b>{where}</b></td><td>{seek(a, mmss(a) + ' to ' + mmss(b))}</td><td class='muted'>{e(r['was'])}</td><td>{e(r['now'])}</td><td>{btn}</td></tr>")
h += ["</table>", f"<p class='muted'>{e(N['unchanged'])}</p>",
      "<h2>The first minute</h2>", f"<video class='big' controls preload='none' poster='{still('first-poster', 51.0)}' src='review/first-minute - REVIEW 540p.mp4' style='max-width:760px'></video>",
      f"<p class='muted'>{e(N['first_note'])}</p>", "<h2>The three new AI clips, finished</h2><p class='muted'>One take each, $0.60 each. Each carries the AI-GENERATED label. The start and end frames are the ones you approved.</p><div class='three'>"]
for m in N["motion"]:
    i = m["id"]
    h.append(f"<div class='card'><img loading='lazy' src='{still(i, R[i]['t0'] + m.get('still', 2.5))}'><div class='b'><span class='id'>{i}</span> <span class='muted'>{e(m['name'])} &middot; {rng(i)}</span><div class='copy'>{e(m['note'])}</div>"
             f"{play(i)} &nbsp; <a class='btn' href='motion-takes/{i}-take1.mp4' onclick=\"return play(this,'{i} whole take')\">Play the whole take</a></div></div>")
h += ["</div><h2>The two changed photos</h2><div class='three'>",
      f"<div class='card'><img loading='lazy' src='{still('P02', R['P02']['t0'] + 3)}'><div class='b'><span class='id'>P02</span> <span class='muted'>{rng('P02')}</span><div class='copy'>{e(N['p02'])}</div>{play('P02')}"
      "<div class='pair'><div><img loading='lazy' src='stills/P02-old.jpg'>the one you turned down</div><div><img loading='lazy' src='stills/P02-new.jpg'>the driveway picture</div></div></div></div>",
      f"<div class='card'><img loading='lazy' src='{still('P04', R['P04']['t0'] + 5)}'><div class='b'><span class='id'>P04</span> <span class='muted'>{rng('P04')}</span><div class='copy'>{e(N['p04'])}</div>{play('P04')}"
      "<div class='pair'><div><img loading='lazy' src='stills/P04-old-pale-half.jpg'>round 2: the filtered copy</div><div><img loading='lazy' src='stills/P04-new-pale-half.jpg'>now: the original</div></div></div></div>",
      "</div><h2>The close: the app tour beside you</h2><div class='three'>"]
for k, (dt, lab) in enumerate(((1.3, "A tap on AI Trainer as you say it"), (3.2, "Workout demo videos on the trainer line"), (8.2, "A tap on Macro Tracker, then the meal photo"), (11.5, "Calorie tracking on the nutritionist line"))):
    h.append(f"<div class='card'><img loading='lazy' src='{still(f'P07-{k}', R['P07']['t0'] + dt)}'><div class='b'><div class='copy'>{e(lab)}</div>{play('P07') if k == 0 else ''}</div></div>")
h += ["</div><h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in N["decided"]] + ["</ol>",
      "<h2>The checks, stated plainly</h2><ul>"] + [f"<li>{e(d)}</li>" for d in N["checks"]] + ["</ul>"]
reply = "RO-19 round 3\n" + "\n".join(f"{k}. {d['t']}: {d['rec']}" for k, d in enumerate(N["decisions"], 1)) + "\nAnything to change in the film (give the time):\nAnything else:\n"
h += ["<h2>Your reply</h2><p class='muted'>My recommendations are filled in. Change any line, add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply' style='height:220px'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function play(a,id){var v=document.getElementById('player');v.src=a.getAttribute('href');document.getElementById('docklabel').textContent=id+' in context';v.play();return false;}"
      "function jump(t){var v=document.getElementById('big');var go=function(){v.currentTime=t;v.play();};if(v.readyState>0){go();}else{v.addEventListener('loadedmetadata',go,{once:true});v.load();}document.getElementById('film').scrollIntoView();return false;}</script></main>"]
txt = "\n".join(h); open(f"{O}/index.html", "w").write(txt); print("page written; em dashes:", txt.count(chr(8212)), "en dashes:", txt.count(chr(8211)))
