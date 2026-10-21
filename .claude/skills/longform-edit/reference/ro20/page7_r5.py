"""RO-20C round 5 review page: the three intro clip frame pairs, the levels-split intro mockup, the two excuse-clip frame
pairs, "What I decided". Frames and mockup only; no motion, lip sync or film build until Dan approves.

Writes /Volumes/Extreme/_edit_work/ro20/round3/index.html (port 8868 serves that folder); the R4 page is kept as
index-r4.html. Refuses any pair whose frame gate + reviewer stamp does not verify (framecheck.require_pass).
Usage: python3 page7_r5.py
"""
import html, json, os, shutil, subprocess, sys

ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
W5 = "/Volumes/Extreme/_edit_work/ro20/round5"
FR = f"{W5}/frames"
PAGE = "/Volumes/Extreme/_edit_work/ro20/round3"
OUT = f"{PAGE}/r5"
sys.path.insert(0, f"{ROOT}/.claude/skills/_shared/framecheck")
from gate import require_pass  # noqa: E402

E = html.escape

INTRO = [
    dict(id="I1", name="Skid Row deadlift", tier="Dead Broke", word="dead broke", at="0:03",
         see="Homeless Dan, shirtless and ripped, deadlifts a kettlebell in front of his cardboard-box home on Skid Row, downtown LA skyline behind.",
         motion="One rep: from the bottom of the hinge he stands up to lockout, the kettlebell rising to his thighs.",
         crop="The tile crops in on him (a square around his body), so he fills it; the skyline stays behind him."),
    dict(id="I2", name="Salmon dinner at home", tier="Middle Class", word="middle class", at="0:03",
         see="Dan, shirtless and ripped, behind the island of an ordinary suburban kitchen over a restaurant-quality salmon plate.",
         motion="He picks up the fork and knife from the napkin and cuts into the salmon, smiling at the camera.",
         crop="The tile shows the middle of the frame: Dan and the plate."),
    dict(id="I3", name="Mansion home gym", tier="Over $10,000 A Month", word="making over $10,000 a month", at="0:05",
         see="Dan, shirtless and ripped, curls chrome dumbbells in a glass-walled mansion gym at sunset, infinity pool outside; a very fit woman in a sports bra and leggings presses dumbbells right behind him.",
         motion="He curls both dumbbells up; behind him she presses hers overhead.",
         crop="The tile shows the middle of the frame: both of them."),
]
EXCUSE = [
    dict(id="E1", name="Hot dog excuse guy", at="1:47.4 to 1:53.5", clip="ctx-E1-now.mp4",
         before="Now, I hear so many people saying,",
         line="I can't afford healthy food, Dan. If I only had money like you, I could afford to eat healthy, but I can't, so there's nothing I can do.",
         after="Again, ...",
         see="An overweight guy at the dining table of a middle-class house, the table piled with hot dogs, fries, chips, donuts and a soda. He whines the line, holding a half-eaten hot dog, then shrugs with his free hand.",
         no="You stay on camera, as in round 4."),
    dict(id="E2", name="Pizza couch excuse guy", at="4:12.3 to 4:16.0", clip="ctx-E2-now.mp4",
         before="Now, I hear you middle-class people thinking like,",
         line="Oh, Dan, I don't have the money for $30 a pound on salmon every week.",
         after="But you do. Go and review that stuff that we went over before.",
         see="A different guy: heavyset, bald, grey beard, maroon hoodie, on the couch of a middle-class apartment behind a coffee table of pizza, fried chicken, cheese puffs, ice cream and soda. He complains with a pizza slice in one hand and the other palm up.",
         no="You stay on camera, as in round 4."),
]


def jpg(src, dst, w=1280):
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "86", "-Z", str(w), src, "--out", dst],
                   check=True, capture_output=True)


def pair(it):
    s, e = f"{FR}/{it['id']}-start.png", f"{FR}/{it['id']}-end.png"
    require_pass(s, e)
    for k, p in (("start", s), ("end", e)): jpg(p, f"{OUT}/{it['id']}-{k}.jpg")
    return (f"<div class='pair'><figure><img src='r5/{it['id']}-start.jpg'><figcaption>START</figcaption></figure>"
            f"<figure><img src='r5/{it['id']}-end.jpg'><figcaption>END</figcaption></figure></div>")


def row(k, v): return f"<div class='rw'><span class='k'>{E(k)}</span> {v}</div>"


def main():
    os.makedirs(OUT, exist_ok=True)
    if not os.path.exists(f"{PAGE}/index-r4.html"): shutil.copy(f"{PAGE}/index.html", f"{PAGE}/index-r4.html")
    st = json.load(open(f"{W5}/page_state.json"))
    h = ["<!doctype html><meta charset='utf-8'><title>What To Buy For Your Health LFC R5</title>" + STYLE + "<main>"]
    h.append("<h1>What To Buy For Your Health At Every Income Level (RO-20C), round 5</h1>")
    h.append("<p class='sub'>Video 3 of the Invest In Your Health series. Everything else in the round 4 film stays as you approved it. "
             "This round: the new intro (a big title over three AI clips) and two lip-synced excuse clips. "
             "Frames and a mockup only: no motion, lip sync or film build until you approve them. "
             "<a href='index-r4.html'>Round 4 page</a></p>")
    h.append("<h2>Your decisions (2)</h2>")
    h.append("<div class='dec'><b>1. The new intro:</b> approve the three clip frame pairs (Skid Row deadlift, Salmon dinner at home, "
             "Mansion home gym) and the full-screen mockup, or name what to change.</div>")
    h.append("<div class='dec'><b>2. The excuse clips:</b> approve the two frame pairs (Hot dog excuse guy at 1:47, Pizza couch excuse "
             "guy at 4:12), or name what to change.</div>")
    # the mockup
    h.append("<h2>The intro, 0:00 to 0:07: full-screen mockup</h2>")
    h.append("<p class='sub'>Your voice is the locked intro pickup. The title lands first; each clip opens on its word "
             "(&ldquo;dead broke&rdquo; 0:03, &ldquo;middle class&rdquo; 0:03.5, &ldquo;making over $10,000 a month&rdquo; 0:04.7). "
             "In the mockup each tile shows its START frame, then fades to its END frame where the motion will go; the real clips will move. "
             + ("The moving preview runs into the first seconds of the round 4 film so you can judge the hand-off.</p>" if st.get("mock_video") else "The moving preview is rendering and will appear here when the render queue frees up.</p>"))
    h.append(f"<img class='wide' src='r5/{st['mock_still']}'>")
    if st.get("mock_video"):
        h.append(f"<video class='wide' controls preload='metadata' src='r5/{st['mock_video']}'></video>")
    h.append(f"<details><summary>Round 4 intro, for comparison</summary><video class='wide' controls preload='none' src='r5/ctx-intro-r4.mp4'></video></details>")
    # intro pairs
    h.append("<h2>The three intro clips: START and END frames</h2>")
    for it in INTRO:
        h.append(f"<h3>{E(it['name'])} ({it['id']}): tile &ldquo;{E(it['tier'])}&rdquo;</h3>" + pair(it))
        h.append(row("When:", f"opens on &ldquo;{E(it['word'])}&rdquo; (about {it['at']}) and plays until the intro ends at 0:06.9"))
        h.append(row("What you see:", E(it["see"])) + row("The motion:", E(it["motion"])) + row("In the tile:", E(it["crop"])))
        h.append(row("If you say no:", "I regenerate it to your notes; the round 4 photo tile is the fallback."))
    # excuse pairs
    h.append("<h2>The two excuse clips: START and END frames</h2>")
    for it in EXCUSE:
        h.append(f"<h3>{E(it['name'])} ({it['id']}), {it['at']}</h3>" + pair(it))
        h.append(row("Just before:", f"&ldquo;{E(it['before'])}&rdquo;") + row("The line it plays under:", f"<b>&ldquo;{E(it['line'])}&rdquo;</b>"))
        h.append(row("Right after:", f"&ldquo;{E(it['after'])}&rdquo; (back to you on camera)") + row("What you see:", E(it["see"])))
        h.append(row("Lip sync:", "his mouth is synced to your own recording of the line. If the sync fails its check once, he reacts with his mouth closed while your voice does the line (your standing rule)."))
        h.append(row("If you say no:", E(it["no"])))
        if st.get(it["clip"]):
            h.append(f"<details><summary>That spot in the round 4 film now</summary><video class='wide' controls preload='none' src='r5/{it['clip']}'></video></details>")
    # what I decided
    h.append("<h2>What I decided (overrule anything)</h2><ul>")
    for d in st["decided"]: h.append(f"<li>{d}</li>")
    h.append("</ul></main>")
    open(f"{PAGE}/index.html", "w").write("\n".join(h))
    print("page ->", f"{PAGE}/index.html")


STYLE = """<style>body{font:15px/1.45 -apple-system,Helvetica,Arial;margin:0;background:#0d1626;color:#e8eef7}main{max-width:1180px;margin:0 auto 60px;padding:0 24px}
h1{font-size:24px;margin:22px 0 6px}h2{font-size:19px;margin:34px 0 10px;border-top:1px solid #26354d;padding-top:18px}h3{font-size:16px;margin:24px 0 8px;color:#8fd0ff}.sub{color:#9fb2cc}
a{color:#8fd0ff}.dec{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:10px 0}.dec b{color:#8fd0ff}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pair figure{margin:0}.pair img{width:100%;border-radius:8px;display:block}figcaption{color:#9fb2cc;font-size:12px;margin-top:3px}
.wide{width:100%;border-radius:10px;display:block;margin:8px 0;background:#000}.rw{margin:5px 0}.k{color:#9fb2cc;font-weight:600}
details{margin:8px 0}summary{cursor:pointer;color:#9fb2cc}li{margin:5px 0}</style>"""

if __name__ == "__main__":
    main()
