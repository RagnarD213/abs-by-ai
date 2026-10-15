#!/usr/bin/env python3
"""RA-07 round 3 review page: the whole 9:16 in one docked player, the revision list with watch ranges, the shoulder-fix
frame for Dan's yes, what I decided, the checks. Writes round3/page/index.html; reads round3/page/checks.json if present.
Serve: python3 .claude/skills/_shared/review_server.py 8837 /Volumes/Extreme/_edit_work/ra07/round3/page"""
import html, json, os
E = html.escape
os.chdir("/Volumes/Extreme/_edit_work/ra07/round3/page")
CK = json.load(open("checks.json")) if os.path.exists("checks.json") else {}

def btn(src, poster, label, start=0, on=False):
    return f'<button class="{"on" if on else ""}" data-src="{src}" data-poster="{poster}" data-t="{start}">{E(label)}</button>'

rev = [
 ("0:00 to 0:30.1", "Unchanged. Frame for frame the first 30 seconds you approved.", None),
 ("0:36.5 to 0:37.9", "Tweaked shoulder: re-trimmed so the grab of the shoulder lands inside the clip (it now starts 0.55 s into the take).", 33.5),
 ("0:37.9 to 0:39.2", "Shoulder fix slot: you on camera for now. It becomes the lateral raise clip once you approve the frame below.", 33.5),
 ("0:39.2 to 0:40.4", "Home curls: same clip, its AI label moved off the man's face to the wall beside his head.", 33.5),
 ("0:40.4 to 0:42.1", "NEW: out of order. He walks up to the Smith machine, sees the OUT OF ORDER sign, turns and shrugs.", 33.5),
 ("0:42.1 to 0:44.0", "NEW: the hack squat instead, right after it. He nods at the hack squat, hangs his towel on it and steps on.", 33.5),
 ("0:44.0 to 0:47.0", "Back next week: now 3 seconds (he reads the sign, turns, shrugs); label moved off his hair.", 33.5),
 ("0:47.0 to 0:52.7", "The ending, first time you see it finished: Get Started button, ends on your held smile, music tail smoothed so it no longer dips.", 46.0),
]
rows = "".join(f"<tr><th>{E(t)}</th><td>{E(d)}</td></tr>" for t, d, _ in rev)

decided = [
 "Each fix sits right after its problem: tweaked shoulder, shoulder fix, home curls, out of order, hack squat, back next week. Your words: \"The hack squat goes right after the squat out of order. The side lateral goes right after the tweaked shoulder.\"",
 "I read \"For I5, certain frames look good, but this clip is in the wrong place\" as I4b, because the rest of that sentence is about the hack squat clip. I5 is unchanged apart from its new length.",
 "The shoulder fix is now one shot, the lateral raise, for its whole 1.3 s. The phone half I had planned never actually nodded in its take, and half a second of it read as a still photo.",
 "Your rejected shoulder-fix end frame is redone. Our new frame check rejected twelve versions with his arms up: the image model kept putting the machine's pivots beside his neck, so the pads would have slid off his arms the moment he moved. The frame below is the start of the rep instead, with hands on the handles and pads on the outside of his arms; in the clip he raises both arms out to the sides and back.",
 "The out-of-order end frame you approved had his towel wrapped round his neck, which the clip would have had to morph. I fixed only the towel (it stays on his left shoulder through the turn) and locked the background to the start frame.",
 "The hack squat: replacement frames I made to fix machine faults failed the frame check ten times, so the clip is made from the exact two frames you approved. I use 1.9 s of it, the nod, the towel and the step onto the machine; the take cuts to a different angle after that, which I left out.",
 "I2, I3a and I5 were on your round 2 page moving and drew no change, so they are carried as shown.",
 "Your voice and music are the approved mix, sample for sample, up to the last word. After \"step.\" I evened out a dip in the music and added 1 ms so the sound is exactly as long as the picture.",
 "The Get Started button sits over your upper abs for the last 5.7 s, the same spot as on RA-14. Say if you want it lower.",
]
dec = "".join(f"<li>{E(x)}</li>" for x in decided)
cks = "".join(f"<li>{E(x)}</li>" for x in CK.get("lines", ["Checks are still running; this page updates."]))
ask = CK.get("ask", "")
reply = "1. Shoulder fix frame (I3b): yes / changes:\n2. Budget to $15 for the shoulder fix clip and its retakes: yes / no\n3. Anything in the film to change (give the time):\n"

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fire Your Trainer AD R3</title><style>
:root{{--bg:#0d1420;--panel:#152033;--ink:#eef4fb;--mute:#9db0c7;--line:#27384f;--acc:#68c5ff;--warn:#ffcf6b}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1240px;margin:0 auto;padding:24px 16px 80px}}@media(min-width:1500px){{main{{margin-right:460px}}}}
h1{{font-size:28px;margin:0 0 6px}}h2{{font-size:21px;margin:34px 0 10px;border-top:1px solid var(--line);padding-top:22px}}h3{{font-size:17px;margin:0 0 10px}}
.sub{{color:var(--mute)}}ol,ul{{padding-left:22px}}li{{margin:6px 0}}a{{color:var(--acc)}}
.ask{{background:#2a2410;border:1px solid var(--warn);border-radius:12px;padding:12px 16px;margin:14px 0}}
.player{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}}
@media(min-width:1500px){{.player{{position:fixed;right:18px;top:18px;width:420px}}}}
video{{width:100%;max-height:72vh;border-radius:10px;background:#000}}
.btns button{{display:block;width:100%;text-align:left;background:#1d2c44;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:6px 0 0;font-size:14px;cursor:pointer}}
.btns button.on{{border-color:var(--acc);color:var(--acc)}}
.newpair{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px;margin-bottom:18px}}.pair{{display:flex;gap:10px;max-width:720px}}.pair figure{{margin:0;flex:1}}.pair img{{width:100%;border-radius:8px}}
figcaption{{font-size:12.5px;color:var(--mute);text-align:center}}
table{{border-collapse:collapse;width:100%;font-size:14.5px;margin-top:10px}}th{{text-align:left;vertical-align:top;color:var(--mute);font-weight:600;padding:6px 12px 6px 0;width:24%;white-space:nowrap}}td{{padding:6px 0;vertical-align:top}}
tr+tr th,tr+tr td{{border-top:1px solid var(--line)}}
textarea{{width:100%;height:150px;background:#0a101a;color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:12px;font:15px/1.5 ui-monospace,Menlo,monospace}}
.copy{{background:var(--acc);color:#04121f;border:0;border-radius:8px;padding:10px 16px;font-weight:700;margin-top:8px;cursor:pointer}}
</style></head><body><main>
<h1>Fire Your Trainer! · ad · round 3</h1>
<p class="sub">RA-07, the whole 9:16, 52.7 seconds. Each fix now plays right after its problem. The first 30 seconds are the ones you approved, unchanged.</p>
{f'<div class="ask">{E(ask)}</div>' if ask else ''}
<div class="player"><video id="v" controls preload="none" poster="poster_full.jpg" src="full.mp4"></video>
<div class="btns">{btn("full.mp4","poster_full.jpg","Whole ad (540p)",0,True)}{btn("run.mp4","poster_run.jpg","What changed: 0:33.5 to 0:48.0")}{btn("ending.mp4","poster_end.jpg","The ending: 0:46.0 to the end")}</div>
<p class="sub" style="font-size:13px">Full quality file: Claude Ad Videos/fire your trainer - RA-07/. Review copy: Videos to Review/Fire Your Trainer AD R3 - whole 9x16.mp4.</p></div>
<h2>What changed since round 2 (watch these)</h2>
<table>{rows}</table>
<h2>One frame for your yes: the shoulder fix (I3b)</h2>
<section class="newpair"><div class="pair">
<figure><a href="i3b_end_old.jpg" target="_blank"><img src="i3b_end_old.jpg" alt="rejected end frame"></a><figcaption>Round 2 end frame you rejected</figcaption></figure>
<figure><a href="i3b_end_new.jpg" target="_blank"><img src="i3b_end_new.jpg" alt="new frame"></a><figcaption>NEW: hands on the handles, pads on the outside of his arms, start of the rep</figcaption></figure></div>
<table><tr><th>Plays</th><td>0:37.9 to 0:39.2, right after the tweaked shoulder, under "When you get injured or you can't make it"</td></tr>
<tr><th>In the clip</th><td>He raises both arms out to the sides to shoulder height with the pads riding on his arms, then lowers them: one easy side lateral raise.</td></tr>
<tr><th>Checked</th><td>Passed the frame gate and a fresh independent reviewer (pads, handles, lever reach from behind the shoulder, fingers, calm face).</td></tr>
<tr><th>If yes</th><td>I make the clip next round (about $1, plus a retake if it needs one) and swap it in for the on-camera shot.</td></tr>
<tr><th>If no</th><td>That 1.3 s stays you on camera.</td></tr></table></section>
<h2>What I decided (overrule anything)</h2><ul>{dec}</ul>
<h2>Checks on the exact file</h2><ul>{cks}</ul>
<h2>Your reply</h2>
<textarea id="r">{E(reply)}</textarea><br><button class="copy" onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button>
</main><script>
const v=document.getElementById('v');
document.querySelectorAll('.btns button').forEach(b=>b.onclick=()=>{{v.poster=b.dataset.poster;v.src=b.dataset.src;v.play();
document.querySelectorAll('.btns button').forEach(x=>x.classList.toggle('on',x===b));if(window.innerWidth<1500)v.scrollIntoView({{behavior:'smooth',block:'center'}})}});
</script></body></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash on the page"
open("index.html", "w").write(page)
print("index.html", len(page))
