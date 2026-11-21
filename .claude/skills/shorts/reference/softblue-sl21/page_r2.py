"""SL-21 round 2 pick page: START and END frame pairs for the two lip-synced excuse clips (Short 1 restaurant,
Short 2 beach). Blind pairs X1/X2 per clip (sources never shown). Refuses any pair without frame gate + reviewer PASS.

Usage: python3 page_r2.py            (reads round2/frames/pairs.json: {"R": {"codex": "codex/R", "google": "google/R2a"}, ...})
Writes review/index.html (port 9621); the round 1 page is kept as review/index-r1.html.
"""
import html, json, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = "/Users/danielrose/Projects/Claude/Projects/Abs By AI"
WORK = "/Users/danielrose/Projects/_edit_work/SL-21"
FR = f"{WORK}/round2/frames"
PAGE = f"{WORK}/review"
OUT = f"{PAGE}/r2"
BLIND = f"{ROOT}/.claude/skills/_shared/blind-image/blind.py"
sys.path.insert(0, f"{ROOT}/.claude/skills/_shared/framecheck")
from gate import require_pass  # noqa: E402

E = html.escape
CLIPS = {
    "R": dict(short="Short 1: Restaurants Don't Care About Your Fitness Goals", name="Restaurant excuse guy",
              at="0:01.5 to 0:05.7", band=f"{WORK}/round2/A_at2.3.png",
              before="A lot of people I know, they're like,",
              line="oh, I don't have the money to get in shape, Dan. I don't have the money for a gym membership.",
              after="But you look at their credit card statement, and they're eating out at restaurants two or three times per week.",
              cap=["I don't have the money", "for a gym membership."],
              see="A fat guy at an expensive steakhouse behind a tomahawk steak, a lobster, a seafood tower and red wine. "
                  "He whines the line with a piece of steak on his fork, then shrugs with both hands.",
              now="Right now you are on camera for this line. The street clip before it and the receipt clip after it stay."),
    "B": dict(short="Short 2: You Don't Deserve A Vacation Until You're Ripped", name="Beach excuse guy",
              at="0:02.6 to 0:05.9", band=f"{WORK}/round2/D_at4.5.png",
              before="Now I know some of you guys aren't gonna like hearing this. You're like,",
              line="I need a vacation. I deserve a break because I work hard.",
              after="But you don't deserve a break. You deserve a break once you're ripped.",
              cap=["I deserve a break", "because I work hard."],
              see="A fat, sunburnt, rough-looking guy on a lounger on a tropical beach with a pineapple cocktail. "
                  "He whines the line, then shrugs with his free hand.",
              now="Right now you are on camera for this line. The beach shot from the air that opens the Short stays, and the "
                  "key point lands on your reply as before."),
}
# crop offset (rows of the 1080-wide scaled frame hidden above the picture area) and caption top, per original file
MOCK = json.load(open(f"{FR}/mock.json")) if os.path.exists(f"{FR}/mock.json") else {}


def norm(src, dst, size):
    Image.open(src).convert("RGB").resize(size, Image.LANCZOS).save(dst, quality=93)


def mock(src, clip, dst, off, cap_y):
    c = CLIPS[clip]
    band = Image.open(c["band"]).convert("RGB")
    im = Image.open(src).convert("RGB")
    h = round(im.height * 1080 / im.width)
    im = im.resize((1080, h), Image.LANCZOS)
    off = max(0, min(off, h - 1610))
    fr = Image.new("RGB", (1080, 1920))
    fr.paste(im.crop((0, off, 1080, off + 1610)), (0, 310))
    fr.paste(band.crop((0, 0, 1080, 310)), (0, 0))
    d = ImageDraw.Draw(fr)
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 86)
    for i, t in enumerate(c["cap"]):
        w = d.textlength(t, font=f)
        d.text(((1080 - w) / 2, cap_y + i * 98), t, font=f, fill="white", stroke_width=7, stroke_fill="black")
    fr.resize((540, 960), Image.LANCZOS).save(dst, quality=90)


def build_clip(clip, pairs):
    setdir = f"{WORK}/round2/blind/{clip}"
    if len(pairs) == 1:          # one pair only (the other source failed twice, logged in frames/google/<clip>-comparison-unavailable.txt):
        key = {"X1": {"source": next(iter(pairs))}}                 # no blind set to build, nothing to score
    else:
        if not os.path.exists(f"{setdir}/.blind-key.json"):
            for src, stem in pairs.items():
                subprocess.run(["python3", BLIND, "add", setdir, "--source", src, "--file", f"{FR}/{stem}-start.png"], check=True,
                               capture_output=True)
            subprocess.run(["python3", BLIND, "build", setdir, "--kind", "start-frame",
                            "--video", "What To Cut Shorts (SL-21)", "--shot", f"{clip} excuse clip frame pair"], check=True,
                           capture_output=True)
        key = json.load(open(f"{setdir}/.blind-key.json"))["labels"]     # never printed
    cards = []
    for label in sorted(key):
        src = key[label]["source"]; stem = pairs[src]
        s, e = f"{FR}/{stem}-start.png", f"{FR}/{stem}-end.png"
        require_pass(s, e)
        if len(pairs) == 1:
            size = (940, 1672); norm(s, f"{OUT}/{clip}-{label}-start.jpg", size)
        else:
            size = Image.open(f"{setdir}/blind/{label}.jpg").size
            shutil.copy(f"{setdir}/blind/{label}.jpg", f"{OUT}/{clip}-{label}-start.jpg")
        norm(e, f"{OUT}/{clip}-{label}-end.jpg", size)
        m = MOCK.get(stem, {})
        mock(s, clip, f"{OUT}/{clip}-{label}-mock.jpg", m.get("off", 150), m.get("cap", 1412))
        cards.append(
            f"<div class='card' data-clip='{clip}' data-label='{label}'><div class='hd'><b>Pair {label}</b>"
            f"<button class='pick' onclick='pick(this)'>Pick {label}</button></div>"
            f"<div class='trio'><figure><img src='r2/{clip}-{label}-start.jpg'><figcaption>START</figcaption></figure>"
            f"<figure><img src='r2/{clip}-{label}-end.jpg'><figcaption>END</figcaption></figure>"
            f"<figure><img src='r2/{clip}-{label}-mock.jpg'><figcaption>Mockup: the START frame in the Short</figcaption></figure></div></div>")
    return "\n".join(cards)


def row(k, v): return f"<div class='rw'><span class='k'>{E(k)}</span> {v}</div>"


def main():
    os.makedirs(OUT, exist_ok=True)
    if not os.path.exists(f"{PAGE}/index-r1.html"): shutil.copy(f"{PAGE}/index.html", f"{PAGE}/index-r1.html")
    pairs = json.load(open(f"{FR}/pairs.json"))
    h = ["<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
         "<title>What To Cut SFL R2</title>" + STYLE + "<main>"]
    h.append("<h1>What To Cut Shorts, round 2: the two excuse clips</h1>")
    h.append("<p class='sub'>Shorts cut from What To Cut To Afford Getting In Shape (RO-20B). Short 3 is final. Shorts 1 and 2 are "
             "approved except for these two new clips. These are frames only: nothing moves and no lips are synced until you "
             "pick a pair for each clip. <a href='index-r1.html'>Round 1 page (the three Shorts)</a></p>")
    h.append("<h2>Your picks (2)</h2><div class='dec'>For each clip, click <b>Pick</b> on the pair you want. A pair is its START "
             "and END frame together. The restaurant clip has one pair that passed its checks; the beach clip has two. "
             "If you want none for a clip, leave it unpicked and say what to change. Your reply text builds "
             "itself at the bottom of the page.</div>")
    for clip, c in CLIPS.items():
        h.append(f"<h2>{E(c['name'])}</h2><p class='sub'>{E(c['short'])}, {c['at']}</p>")
        h.append(row("Just before:", f"&ldquo;{E(c['before'])}&rdquo;"))
        h.append(row("The line his lips sync to:", f"<b>&ldquo;{E(c['line'])}&rdquo;</b> (your own recording)"))
        h.append(row("Right after:", f"&ldquo;{E(c['after'])}&rdquo;"))
        h.append(row("What you see:", E(c["see"])) + row("Now:", E(c["now"])))
        h.append(build_clip(clip, pairs[clip]))
    h.append("<h2>What I decided (overrule anything)</h2><ul>")
    for d in DECIDED: h.append(f"<li>{d}</li>")
    h.append("</ul><h2>Your reply</h2><textarea id='notes' placeholder='Anything to change (optional)' oninput='upd()'></textarea>"
             "<pre id='reply'></pre><button onclick='navigator.clipboard.writeText(document.getElementById(\"reply\").textContent)'>Copy reply</button>")
    h.append(SCRIPT + "</main>")
    open(f"{PAGE}/index.html", "w").write("\n".join(h))
    print("page ->", f"{PAGE}/index.html")


DECIDED = [
    "Each clip plays only under the excuse line. Everything else in Shorts 1 and 2 stays exactly as you approved it.",
    "His mouth is closed in both frames on purpose. The lips are synced to your own recording after the clip is made; a clip "
    "made already talking syncs badly.",
    "The motion is small: he whines the line, then lifts into the shrug you see in the END frame.",
    "Chest-up framing, with the table or the drink in front of him, so no shot is built around his stomach (your standing rule).",
    "The clips carry the AI-GENERATED label, placed off his face.",
    "On the restaurant clip the captions sit lower than usual so they do not cover the steak. The mockups show where the "
    "title and captions land; the caption style in the mockup is approximate.",
    "The picture area of a Short is a little shorter than a full vertical frame, so the mockup shows the crop: a strip of "
    "ceiling or sky at the top is hidden behind the title.",
    "If a lip sync fails its check, he reacts with his mouth closed while your voice does the line (your standing rule).",
]

STYLE = """<style>body{font:16px/1.45 -apple-system,Helvetica,Arial;margin:0;background:#0d1626;color:#e8eef7}main{max-width:1100px;margin:0 auto 60px;padding:0 16px}
h1{font-size:24px;margin:22px 0 6px}h2{font-size:20px;margin:34px 0 8px;border-top:1px solid #26354d;padding-top:18px}.sub{color:#9fb2cc;margin:4px 0 10px}
a{color:#8fd0ff}.dec{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:10px 0}.dec b{color:#8fd0ff}
.card{background:#111c30;border:2px solid #26354d;border-radius:12px;padding:12px;margin:14px 0}.card.on{border-color:#35c26b;background:#10261b}
.hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;font-size:18px}
.trio{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}.trio figure{margin:0}.trio img{width:100%;border-radius:8px;display:block}
figcaption{color:#9fb2cc;font-size:13px;margin-top:4px}.rw{margin:5px 0}.k{color:#9fb2cc;font-weight:600}li{margin:6px 0}
button{font:600 16px -apple-system,Helvetica,Arial;background:#1d4f8f;color:#fff;border:0;border-radius:8px;padding:10px 18px;cursor:pointer}
.card.on .pick{background:#35c26b;color:#04210f}textarea{width:100%;min-height:70px;background:#0a1220;color:#e8eef7;border:1px solid #26354d;border-radius:8px;padding:10px;font:15px -apple-system,Helvetica,Arial;box-sizing:border-box}
pre{background:#0a1220;border:1px solid #26354d;border-radius:8px;padding:12px;white-space:pre-wrap}
@media(max-width:700px){.trio{grid-template-columns:1fr 1fr}.trio figure:last-child{grid-column:1/3}}</style>"""

SCRIPT = """<script>
const names={R:'Restaurant excuse guy (Short 1)',B:'Beach excuse guy (Short 2)'};
function pick(b){const c=b.closest('.card'),was=c.classList.contains('on');
 document.querySelectorAll('.card[data-clip="'+c.dataset.clip+'"]').forEach(x=>{x.classList.remove('on');x.querySelector('.pick').textContent='Pick '+x.dataset.label});
 if(!was){c.classList.add('on');b.textContent='Picked '+c.dataset.label}upd()}
function upd(){let t=[];for(const k in names){const c=document.querySelector('.card.on[data-clip="'+k+'"]');
 t.push(names[k]+': '+(c?'pair '+c.dataset.label:'neither, see my notes'))}
 const n=document.getElementById('notes').value.trim();if(n)t.push('Notes: '+n);document.getElementById('reply').textContent=t.join('\\n')}
upd();</script>"""

if __name__ == "__main__":
    main()
