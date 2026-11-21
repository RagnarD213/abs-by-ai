"""RO-08 round 3 review page: Dan's three revisions with their times in the NEW film and a context clip each, the decisions (from
round3/page_extra.json, written after the independent review is read), the full film, the three quality questions answered for every
AI clip by the editor and by the independent reviewer, what I decided, the checks stated plainly, one reply box.
Facts that come from the checks are read from round3/page_facts.json (r3_page_facts.py).
Writes round3/index.html. Serve: python3 .claude/skills/_shared/review_server.py 8872 /Volumes/Extreme/_edit_work/ro08/round3"""
import json, html
W = "/Volumes/Extreme/_edit_work/ro08"; O = f"{W}/round3"; e = html.escape
F = json.load(open(f"{O}/page_facts.json")); X = F["extra"]; R = {r["id"]: r for r in json.load(open(f"{W}/plan_resolved.json"))}
FILM = "RO-08 round 3 - full film"
def mmss(t): return f"{int(t//60)}:{int(t % 60):02d}"
def vid(name, cls=""): return f"<video {cls} controls preload='none' poster='context/{name}-context.jpg' src='context/{name}-context - REVIEW 540p.mp4'></video>"
css = """body{font:15px/1.45 -apple-system,Helvetica,Arial;margin:0;background:#0d1626;color:#e8eef7}main{max-width:1180px;margin:0 auto 60px;padding:0 28px}
h1{font-size:24px;margin:22px 0 6px}h2{font-size:19px;margin:34px 0 10px;border-top:1px solid #26354d;padding-top:18px}.sub{color:#9fb2cc}
.dec{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:10px 0}.dec b{color:#8fd0ff}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}.two video{width:100%;border-radius:10px;background:#000}
.rev{display:grid;grid-template-columns:480px 1fr;gap:16px;background:#14223a;border:1px solid #26354d;border-radius:10px;padding:14px;margin:12px 0}.rev video{width:100%;border-radius:8px;background:#000}
.ts{display:inline-block;background:#1f7a4d;color:#fff;border-radius:5px;padding:1px 8px;font-weight:700;margin-right:6px}.muted{color:#9fb2cc}
table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #26354d;padding:7px 8px;text-align:left;vertical-align:top}th{color:#9fb2cc;font-weight:600}
.v{display:inline-block;border-radius:4px;padding:0 6px;font-weight:700;font-size:12px;margin-right:5px}.vp{background:#1f7a4d}.vb{background:#a8741a}.vf{background:#a33}
textarea{width:100%;height:190px;background:#0b1320;color:#e8eef7;border:1px solid #26354d;border-radius:8px;padding:10px;font:13px/1.4 Menlo,monospace}
video.big{width:100%;border-radius:10px;background:#000}ol li,ul li{margin:5px 0}a{color:#8fd0ff}button{background:#2b6cb0;color:#fff;border:0;border-radius:6px;padding:6px 10px;margin-top:6px;cursor:pointer}
@media(max-width:900px){.rev,.two{grid-template-columns:1fr}}"""
A5 = R["A5"]; A6 = R["A6"]; A8 = R["A8"]
h = [f"<!doctype html><meta charset='utf-8'><title>RO-08 round 3: your three revisions</title><style>{css}</style><main>",
     "<h1>Intermittent Fasting: The Best Way To Get Abs. Round 3, your three revisions</h1>",
     f"<div class='sub'>Long-form content, 16:9, {F['length']}. Your three notes on the round 2 film are done, and your new quality check took the weak second out of two more clips. Everything else is frame for frame the film you reviewed: {F['changed_frames']} of {F['frames']:,} frames differ, all of them inside the five spots below, and the sound is untouched.</div>",
     "<div class='dec'><b>Locked, not reopened:</b> opener A, the time-lapse (your pick). The cut, the colour, voice 1a, the music bed, all 48 lower thirds and every clip you did not name.</div>",
     f"<h2>Your decisions ({len(X['decisions'])})</h2>"]
for k, d in enumerate(X["decisions"], 1):
    h.append(f"<div class='dec'><b>{k}. {e(d['q'])}</b> {e(d['body'])}" + (f"<br><span class='muted'>My recommendation: {e(d['rec'])}</span>" if d.get("rec") else ""))
    if d.get("clips"):
        h.append("<div class='two' style='margin-top:10px'>" + "".join(f"<div><b>{e(t)}</b>{vid(n)}</div>" for n, t in d["clips"]) + "</div>")
    h.append("</div>")
h += ["<h2>The five changes, with where to look in the new film</h2><p class='muted'>Each player is cut from the finished round 3 film with a few seconds of you either side. The green time is where it sits in the full film. The film is the same length as before, so nothing else moved.</p>"]
CH = [("A4-out", "1:58 to 2:04", "watch 1:50 to 2:08", "The office worker and the sandwich: removed",
       "Before: an AI clip of a man who has not eaten all day staring at a coworker's sandwich. Now: you are on camera for the whole line (\"Some people even go entire days without eating...\").",
       "One framing change comes with it. With the clip gone, three shots in a row would have sat at the same close size for 30 seconds, past the 22 second limit I hold every shot to. So the middle one, 1:53 to 2:04, is now the wider camera frame. It is the same take, so it is a size change and not a jump."),
      ("A5", f"{mmss(A5['t0'])} to {mmss(A5['t1'])}", "watch 6:03 to 6:14", "The donut and the food coma: rebuilt so nothing vanishes",
       "Before: one take in which the box emptied in a fast-forward and the donuts faded out. Now: two shots cut from that same take. He bites a donut beside a full box at nine o'clock. Hard cut. Ten o'clock: the box is already down to crumbs, one half-eaten muffin lies on the desk, and he sinks face down onto his keyboard on \"food coma\". No frame of the fast-forward is used.",
       X["a5_note"]),
      ("A3-out", "7:16 to 7:22", "watch 7:10 to 7:32", "The stomach rumble in the meeting: removed",
       "Before: an AI clip where water jumped in the glasses. Now: you are on camera for \"They've done this for the past 40 years and all of a sudden there's no breakfast. Their body really lets them know.\"",
       "The pancake clip before it and the man whining at his empty plate after it are untouched."),
      ("A8-now", f"{mmss(A8['t0'])} to {mmss(A8['t1'])}", "watch 4:52 to 5:06", "The clean-up crew inside the cell: ends before the sweep (my change, decision 2)",
       "Before: it ran to 5:02, and at 5:00 the heaps of junk cleared away by themselves in half a second. Now: it ends on \"for fuel\" while the crew is wheeling the junk to the furnace, and you are on camera for \"renews your cells and makes you younger\".",
       "The clean cell from your approved end frame is not in the film now. Decision 2 has the two ways to get it back."),
      ("A6-now", f"{mmss(A6['t0'])} to {mmss(A6['t1'])}", "watch 12:08 to 12:19", "The midnight fridge raid: ends 1.4 seconds earlier (my change, decision 1)",
       "Before: it ended on him holding one leg out in the air. Now: it ends on the frozen stare with the spoon in his mouth, and you are on camera for \"is not going to work for you\".",
       "Nothing else in the clip changed.")]
for name, ts, watch, title, what, note in CH:
    h.append(f"<div class='rev'>{vid(name)}<div><b>{e(title)}</b><br><span class='ts'>{ts}</span><span class='muted'>{watch}</span><p>{e(what)}</p><p class='muted'>{e(note)}</p></div></div>")
h += ["<h2>The full film</h2>", f"<video class='big' controls preload='none' poster='{FILM}.jpg' src='{FILM} - REVIEW 540p.mp4'></video>",
      f"<p class='muted'><a href='{FILM}.mp4'>Full 1080p file</a> &nbsp; <a href='RO08.srt'>Subtitles</a> &nbsp; <a href='RO08.chapters.txt'>Chapters</a> &nbsp; <a href='RO-08 audio AB (reference then ours).mp4'>Audio A/B against the reference voice</a></p>"]
# ---- the three questions
def badge(v):
    v = (v or "").upper(); c = "vp" if v.startswith("PASS") else ("vf" if v.startswith("FAIL") else "vb"); return f"<span class='v {c}'>{e(v.split()[0] if v else '?')}</span>"
QR = {q.get("id") or q["clip"]: q for q in F["questions_review"]}
def rq(q, k):
    r = X.get("review_map", {}).get(q["id"]); r = QR.get(r) if r else None
    if not r: return "<span class='muted'>not answered</span>"
    a = r[k]; return f"{badge(a['verdict'])}{e(a['why'])}"
def eq(s):
    v = "PASS" if s.lower().startswith("pass") else ("FAIL" if s.lower().startswith("fail") else "BORDERLINE"); return f"{badge(v)}{e(s.split('. ', 1)[1] if '. ' in s else ('' if s.strip().lower() in ('pass.', 'pass') else s))}"
h += ["<h2>The new quality check: three questions asked of every AI clip</h2>",
      "<p class='muted'>Your rule from the round 2 review. Each clip was read frame by frame and judged at playback speed, once by me and once by an independent reviewer who never saw my answers. 1: does everything obey cause and effect (nothing vanishes, appears or moves by itself)? 2: with the sound off, would a stranger say what it shows? 3: does it show the line you are saying, and does the joke land in one viewing?</p>",
      "<table><tr><th style='width:15%'>Clip</th><th>1. Cause and effect</th><th>2. Sound off</th><th>3. Shows the line</th></tr>"]
for q in F["questions_editor"]:
    h.append(f"<tr><td><b>{e(q['clip'])}</b><br><span class='ts'>{e(q['t'])}</span></td>" + "".join(f"<td><span class='muted'>Me:</span> {eq(q[k])}<br><span class='muted'>Reviewer:</span> {rq(q, k)}</td>" for k in ("q1", "q2", "q3")) + "</tr>")
h.append("</table>")
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in X["decided"]] + ["</ol>"]
h += ["<h2>The checks, stated plainly</h2><ul>"] + [f"<li>{e(d)}</li>" for d in X.get("checks_first", []) + F["checks"]] + ["</ul>"]
h += ["<h2>Flags</h2><p class='muted'>The first is newly visible this round. The rest are unchanged from round 2.</p><ul>"] + [f"<li>{e(d)}</li>" for d in X.get("new_flags", []) + F["flags"]] + ["</ul>"]
h += ["<h2>For VLC</h2><p>In the project folder <b>Videos to Review</b> (the three round 2 files are gone):</p><ul>"] + [f"<li>{e(n)}</li>" for n in F["vlc"]] + ["</ul>"]
h += ["<h2>Your reply</h2>", f"<textarea id='reply'>{e(X['reply'])}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button></main>"]
s = "\n".join(h); assert chr(8212) not in s and chr(8211) not in s, "a dash on the page"
open(f"{O}/index.html", "w").write(s); print("page written", len(s))
