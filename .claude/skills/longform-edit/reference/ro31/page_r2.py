"""RO-31 round 2 frames page: every AI idea with its START and END, unlabeled sources (blind test), the line it plays under and
what plays if Dan says no. Only pairs whose gate + fresh reviewer both PASS are shown (framecheck.require_pass)."""
import json, os, sys, random, html, subprocess
from PIL import Image
A = "/Volumes/Expansion/_edit_work/RO-31/round2/aiframes"; OUT = "/Volumes/Expansion/_edit_work/RO-31/round2/review"
P = "/Users/danielrose/Projects/Claude/Projects/Abs By AI"
sys.path.insert(0, f"{P}/.claude/skills/_shared/framecheck"); from gate import require_pass
R1 = {r["id"]: r for r in json.load(open("/Volumes/Expansion/_edit_work/RO-31/round1/plan_resolved.json"))}
WO = [w for w in json.load(open("/Volumes/Expansion/_edit_work/RO-31/round1/words_out.json")) if w["t0"] is not None]
def speech(a, b): return " ".join(w["w"] for w in WO if a <= w["t0"] < b).replace("appsbyai .com", "AbsByAI.com")
def mmss(t): return f"{int(t//60)}:{t%60:04.1f}"
E_ = html.escape
IDEAS = [  # id, name, slot from round 1 plan, candidate sets (src, name), what happens, if no
 ("A1", "The Opener: Self-Conscious About His Chest", "A1", [("google", "O1"), ("google", "O2"), ("google", "O3"), ("google", "O4"), ("google", "O5"), ("google", "O6")],
  "A man with visible man boobs looks down at his chest, self-conscious, then covers or hides it.", "You on camera, as in the first minute you approved."),
 ("A2", "The Pool Shirt", "A2", [("codex", "A2")], "Pool party; he sits in a loose black T-shirt while his friends swim. A friend waves him in; he shakes his head and tugs the shirt down. Slimmer than round 1, as you asked.", "You on camera."),
 ("A6", "The Doctor Visit", "A6", [("codex", "A6"), ("google", "A6")], "A man whose man boobs show through his T-shirt talks to a doctor; the doctor explains, he nods, relieved. No stopwatch.", "You on camera."),
 ("A4", "Juice Down The Drain", "A4", [("codex", "A4"), ("google", "A4")], "He pours a carafe of orange juice down the sink, then drinks a glass of water instead.", "You on camera."),
 ("A5", "T-Shirt Double Take", "A5", [("codex", "A5")], "He smiles at himself in a fitted T-shirt; his girlfriend looks up from her phone and does a double take.", "You on camera."),
 ("A7", "The Locker Room Flex", "A7", [("codex", "A7"), ("google", "A7b"), ("google", "A7c"), ("google", "A7d")], "A bodybuilder flexes at the mirror, glances down at his chest, his smile fades, and he pulls a T-shirt out of his bag. The study line stays over it as a lower third.", "You on camera with the same lower third."),
]
ext = lambda s: "png" if s == "codex" else "jpg"
sec = []; key = {}
rng = random.Random(31)
for iid, name, slot, cands, what, no in IDEAS:
    ok = []
    for s, n in cands:
        st, en = f"{A}/{s}/{n}-start.{ext(s)}", f"{A}/{s}/{n}-end.{ext(s)}"
        try: require_pass(st, en); ok.append((s, n, st, en))
        except BaseException as e: print("not shown:", s, n)
    if not ok: continue
    rng.shuffle(ok); figs = []
    for k, (s, n, st, en) in enumerate(ok, 1):
        lab = f"X{k}"; key[f"{iid}-{lab}"] = {"source": s, "set": n, "start": st, "end": en}
        for which, f in (("start", st), ("end", en)):
            Image.open(f).convert("RGB").resize((1376, 774), Image.LANCZOS).save(f"{OUT}/frames/{iid}-{lab}-{which}.jpg", quality=92)
        figs.append(f"""<div class="set"><h4>{lab}</h4><div class="two"><figure><a href="frames/{iid}-{lab}-start.jpg"><img loading="lazy" src="frames/{iid}-{lab}-start.jpg"></a><figcaption>START</figcaption></figure>
<figure><a href="frames/{iid}-{lab}-end.jpg"><img loading="lazy" src="frames/{iid}-{lab}-end.jpg"></a><figcaption>END</figcaption></figure></div></div>""")
    r = R1[slot]; t0, t1 = r["t0"], r["t1"]
    sec.append(f"""<section><h2>{E_(name)} <span class="tag">{iid}</span> <span class="small">{mmss(t0)} to {mmss(t1)}</span></h2>
<table class="ctx"><tr><td>Just before</td><td>{E_(speech(t0-6, t0))}</td></tr><tr><td>The line it plays under</td><td><b>{E_(speech(t0, t1))}</b></td></tr>
<tr><td>Right after</td><td>{E_(speech(t1, t1+5))}</td></tr><tr><td>What happens</td><td>{E_(what)}</td></tr><tr><td>If you say no</td><td>{E_(no)}</td></tr>
<tr><td>Motion</td><td>One Veo take on your Flow subscription for the set you pick, then the motion check and a fresh reviewer. No paid generation.</td></tr></table>
{''.join(figs)}</section>""")
json.dump(key, open(f"{A}/.page-key.json", "w"), indent=1)
X = json.load(open(f"{A}/page_notes.json"))
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Man Boobs LFC R2</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}body{{margin:0;background:var(--bg);color:var(--ink);font:17px system-ui;line-height:1.55}}
main{{max-width:1240px;margin:0 auto;padding:28px 16px}}h1{{font-size:34px;margin:0 0 8px}}h2{{font-size:24px}}h4{{margin:14px 0 6px;color:var(--acc)}}p,li{{color:var(--mute)}}
section{{margin:26px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:18px}}.two{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}figure{{margin:0}}
figcaption{{font-size:13px;color:#9fb7cf}}img{{width:100%;border-radius:10px}}a{{color:var(--acc)}}.tag{{color:#8ed7ff;font-size:13px;font-weight:700}}.small{{font-size:14px;color:#9fb7cf}}
table{{font-size:15px;color:#cfe0f0;border-collapse:collapse}}td{{padding:3px 12px 3px 0;vertical-align:top}}table.ctx td:first-child{{color:#8ed7ff;white-space:nowrap}}
textarea{{width:100%;box-sizing:border-box;min-height:180px;background:var(--bg);color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer}}@media(max-width:900px){{.two{{grid-template-columns:1fr}}}}</style>
<main><h1>How To Get Rid Of Man Boobs <span class="small">LFC, round 2: AI clip frames</span></h1>
<p>Locked from round 1: colour A, warm bass plus voice, the first minute, every graphic and clip. Killed: Jiggle Belt, Four Straws, Push The Diets Aside.
Each idea below shows its START and END frames. Where there are several sets (X1, X2...), pick one. Motion is made only for the sets you pick.</p>
<section><h2>Your decisions</h2><ol>{''.join('<li>'+d+'</li>' for d in X['decisions'])}</ol></section>
<section><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>'+d+'</li>' for d in X['decided'])}</ul></section>
{''.join(sec)}
<section><h2>One reply</h2><textarea id="r">{E_(X['reply'])}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main></html>"""
open(f"{OUT}/index.html", "w").write(page); print("page ok", len(sec), "ideas")
