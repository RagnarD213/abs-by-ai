"""RO-19 round 4 review page (later round: the full film, and only the two things Dan asked for). Order: the one decision, the full film, the revision list with
exact times in THIS film and watch ranges, the photo old and new side by side, the cut at 9:05 (new, and round 3 for comparison), What I decided, the checks
stated plainly, one reply box. Every time comes from the plan and shots the film was rendered from. The words that depend on the gates and the independent
review come from round4/page_checks.json (written by hand from the logs after they ran). Review copies are cut from the MASTER, never a separate render.
usage: page19r4.py [media]   (media: also cut the 540p review copies)  -> round4/index.html. Serve with _shared/review_server.py 8867 round4."""
import json, os, sys, html, subprocess
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro19"; O = f"{W}/round4"; e = html.escape; FPS = 30000/1001
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
R = {r["id"]: r for r in json.load(open(f"{W}/plan_resolved.json"))}; S = json.load(open(f"{W}/shots.json")); SB = {s["id"]: s for s in S}; TOTAL = S[-1]["out_f1"]/FPS
WO = json.load(open(f"{W}/words_out.json")); SH = json.load(open(f"{W}/round4-plan/timeline_shift.json")); X = json.load(open(f"{O}/page_checks.json"))
FILM = f"{O}/film/RO-19 round 4 - full film.mp4"; OLDFILM = f"{W}/round3/film/RO-19 round 3 - full film.mp4"
VLC = "My First Spray Tan LFC R4 - full film.mp4"
def mmss(t): return f"{int(t//60)}:{int(t%60):02d}"
def tenth(t): return f"{int(t//60)}:{t%60:04.1f}"
CUT = SH["at_out_frame"]/FPS; GONE = -SH["frames"]/FPS                                   # the join, and how much came out
w_in = next(w for w in WO if w["shot"] == "water2.1"); w_end = [w for w in WO if w["shot"] == "water2.1"][-1]      # "In" ... "life."
P0, P1 = R["P02"]["t0"], R["P02"]["t1"]
for d in ("stills", "review"): os.makedirs(f"{O}/{d}", exist_ok=True)
def review_copy(src, dst, a=None, b=None, poster_t=1.5):
    cut = [] if a is None else ["-ss", f"{a:.3f}", "-t", f"{b-a:.3f}"]
    subprocess.run([FF, "-v", "error", "-y"] + cut + ["-i", src, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", dst], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-ss", str(poster_t), "-i", dst, "-frames:v", "1", "-q:v", "3", dst[:-4] + ".jpg"], check=True)
CA, CB = CUT - 9.0, w_end["t1"] + 4.0                                                    # the cut in context: from "I sacrificed that this weekend" to the photos line
if len(sys.argv) > 1 and sys.argv[1] == "media":
    review_copy(FILM, f"{O}/review/full-film - REVIEW 540p.mp4", poster_t=1.5)
    review_copy(FILM, f"{O}/review/P02-context - REVIEW 540p.mp4", P0 - 4, P1 + 4, poster_t=7.0)
    review_copy(FILM, f"{O}/review/cut-context - REVIEW 540p.mp4", CA, CB, poster_t=CUT - CA + 4.0)
    review_copy(OLDFILM, f"{O}/review/cut-round3-for-comparison - REVIEW 540p.mp4", CA, CB + GONE, poster_t=CUT - CA + 6.0)
def still(name, t, src=FILM):
    p = f"{O}/stills/{name}.jpg"
    subprocess.run([FF, "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", "scale=960:540", "-q:v", "3", p], check=True); return f"stills/{name}.jpg"
for a, b in (("pale3_single", "P02-old"), ("pale4_single", "P02-new")): Image.open(f"{W}/photos/{a}.jpg").resize((600, 750), Image.LANCZOS).save(f"{O}/stills/{b}.jpg", quality=90)
def play(f, label, name): return f"<a class='btn' href='review/{f}' onclick=\"return play(this,'{name}')\">{label}</a>"
def seek(t, label=None): return f"<a href='#film' onclick=\"return jump({t:.1f})\">{label or mmss(t)}</a>"
REV = [
 dict(where=f"{mmss(P0)} to {mmss(P1)}", a=P0 - 5, b=P1 + 4, was="The driveway photo I picked in round 3 (arms down, straight face)",
      now="The picture you sent: smiling on the driveway, grey shorts, hand at your hip. Same card, same size on screen, same label", btn=play("P02-context - REVIEW 540p.mp4", "Play", "The photo in context")),
 dict(where=f"{tenth(CUT)} to {tenth(w_end['t1'])}", a=CUT - 9, b=w_end["t1"] + 3, was="You said 'In my normal life, I'm', stopped for a second, then said the sentence again from the start",
      now="The first attempt is out. After '...if you're taking care of it.' you say it once: 'In my normal life, I'm in the water all the time, so I'm not entirely sure it would hold up as good as this in my normal life.' The swimmer clip covers the join, so there is no jump in the picture",
      btn=play("cut-context - REVIEW 540p.mp4", "Play", "The cut in context")),
]
DECIDED = [
 "The sentence still ends on 'in my normal life'. That is how you said it, once, at the end of the sentence, and I left it. What came out is the false start at the front. If you want the ending trimmed as well, say so.",
 f"The cut took out {GONE:.1f} seconds ({-SH['frames']} frames). The new start is a tenth of a second before your first word of the restart, measured on the microphone track, so no word is clipped.",
 f"The swimmer clip over that line is the same clip from the same starting point, now {R['Cc11']['t1'] - R['Cc11']['t0']:.1f} seconds instead of 4.5. It still ends after 'all the time', where it ended before.",
 f"Everything after {tenth(CUT)} is {GONE:.1f} seconds earlier than in round 3. Nothing else moved: every shot kept its size and crop, and every lower third, clip and photo is the same and in the same place against your words.",
 "Your picture is used as you sent it. I pulled the full-size copy from your Photos library (it matches your attachment) and cropped it the way the old card was cropped, head to just below the hands, so your abs read at the same size.",
 "One thing about that picture, for your information only: it is a slightly warmer copy of the camera frame taken the same second in your library (chest skin a little more orange than the frame). It still reads clearly pale next to the tanned shots. It is your pick, so it is in as sent.",
 "The music bed and the voice are the same files and settings as round 3.",
 "The doctor clip stays in. When you call the film final I save it to the clip library as the default for 'talk to your doctor' lines, with the other new clips.",
] + X.get("extra_decided", []) + ["Spend this round: $0. No images or AI motion were needed. Total for this video stays $4.80 of the $5.00 limit.", "Nothing is uploaded or queued."]
css = open(f"{W}/recipe/page20.py").read().split('css = """')[1].split('"""')[0] + ".three{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.rev td{padding:7px 14px 7px 0;border-top:1px solid #26354d;vertical-align:top}.rev th{text-align:left;color:#9fb2cc;font-weight:600;padding-right:14px}"
h = [f"<!doctype html><meta charset='utf-8'><title>RO-19 round 4</title><style>{css}</style>",
     "<div id='dock'><div class='muted' id='docklabel'>Play a change in context: press its button</div><video id='player' controls preload='none'></video></div><main>",
     "<h1>My First Spray Tan: round 4, your two final revisions</h1>",
     f"<div class='sub'>Long-form content, 16:9, {mmss(TOTAL)}. Both changes are in and the whole film is rendered again. Nothing is uploaded or queued.</div>",
     "<p><b>Already approved and unchanged:</b> everything else in the film. Same takes, same lower thirds and copy, same stock and AI clips, same sizes, colour, voice and music as the round 3 film you watched.</p>",
     "<h2>Your decision (1)</h2>",
     f"<div class='dec'><b>1. The film.</b> The whole film, {mmss(TOTAL)}, with your two revisions. The list below takes you straight to each one.<div class='opt'>Options: Final (recommended): I file it, save the new clips to the library and write the upload and setup handoff &nbsp;|&nbsp; Changes: give me the time and what you want</div></div>",
     "<h2 id='film'>The full film</h2>", f"<video id='big' class='big' controls preload='none' poster='{still('film-poster', 1.5)}' src='review/full-film - REVIEW 540p.mp4'></video>",
     f"<p class='muted'>This player is the 540p review copy. <a href='film/RO-19 round 4 - full film.mp4'>Full 1080p file</a> &middot; <a href='film/RO-19 audio AB (reference then ours).mp4'>Sound A/B: the reference voice, then this film</a> &middot; <a href='film/RO19.srt'>captions file</a> &middot; <a href='film/RO19.chapters.txt'>chapters</a><br>"
     f"For VLC, in the project folder: <b>Videos to Review / {e(VLC)}</b></p>",
     "<h2>What changed, and where to look</h2><p class='muted'>Times are in this new film. Click a watch range to move the film above to a few seconds before the change. You do not need to watch the whole film again.</p>"
     "<table class='rev'><tr><th>Where</th><th>Watch</th><th>What it was</th><th>What it is now</th><th></th></tr>"]
for r in REV:
    h.append(f"<tr><td><b>{r['where']}</b></td><td>{seek(r['a'], mmss(r['a']) + ' to ' + mmss(r['b']))}</td><td class='muted'>{e(r['was'])}</td><td>{e(r['now'])}</td><td>{r['btn']}</td></tr>")
h += ["</table>", f"<p class='muted'>Every other scene is as you approved it. Because {GONE:.1f} seconds came out, everything after {tenth(CUT)} sits {GONE:.1f} seconds earlier than the times on the round 3 page.</p>",
      "<h2>The photo at 0:48</h2><div class='three'>",
      f"<div class='card'><img loading='lazy' src='{still('P02', P0 + 3)}'><div class='b'><span class='id'>P02</span> <span class='muted'>{mmss(P0)} to {mmss(P1)}, as it is in the film</span><div class='copy'>The picture you sent, on the same card with the same label.</div>{play('P02-context - REVIEW 540p.mp4', 'Play it in context', 'The photo in context')}</div></div>",
      "<div class='card'><div class='b'><div class='pair'><div><img loading='lazy' src='stills/P02-old.jpg'>round 3: the one you replaced</div><div><img loading='lazy' src='stills/P02-new.jpg'>now: your picture</div></div></div></div>",
      "</div><h2>The cut at 9:05</h2><div class='three'>",
      f"<div class='card'><img loading='lazy' src='{still('cut-new', w_in['t0'] + 3.3)}'><div class='b'><span class='id'>NOW</span> <span class='muted'>{tenth(CUT)}: the sentence, said once</span><div class='copy'>{mmss(CA)} to {mmss(CB)} of this film. Listen for one 'In my normal life' at the start of the sentence.</div>{play('cut-context - REVIEW 540p.mp4', 'Play it in context', 'The cut in context')}</div></div>",
      f"<div class='card'><img loading='lazy' src='{still('cut-old', CUT + 1.0, OLDFILM)}'><div class='b'><span class='id'>ROUND 3</span> <span class='muted'>for comparison only</span><div class='copy'>The same stretch of the round 3 film, with the false start you caught.</div>{play('cut-round3-for-comparison - REVIEW 540p.mp4', 'Play round 3', 'Round 3, for comparison')}</div></div>",
      "</div><h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>",
      "<h2>The checks, stated plainly</h2><ul>"] + [f"<li>{e(d)}</li>" for d in X["checks"]] + ["</ul>"]
reply = "RO-19 round 4\n1. The film: final\nAnything to change in the film (give the time):\nAnything else:\n"
h += ["<h2>Your reply</h2><p class='muted'>My recommendation is filled in. Change the line or add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply' style='height:160px'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function play(a,id){var v=document.getElementById('player');v.src=a.getAttribute('href');document.getElementById('docklabel').textContent=id;v.play();return false;}"
      "function jump(t){var v=document.getElementById('big');var go=function(){v.currentTime=t;v.play();};if(v.readyState>0){go();}else{v.addEventListener('loadedmetadata',go,{once:true});v.load();}document.getElementById('film').scrollIntoView();return false;}</script></main>"]
txt = "\n".join(h); open(f"{O}/index.html", "w").write(txt); print("page written; em dashes:", txt.count(chr(8212)), "en dashes:", txt.count(chr(8211)))
print("revision times:", [(r["where"], mmss(r["a"]), mmss(r["b"])) for r in REV], "| total", mmss(TOTAL), "| cut context", round(CA, 1), round(CB, 1))
