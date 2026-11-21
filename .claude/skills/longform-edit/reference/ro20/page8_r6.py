"""RO-20C round 6 review page: the finished film with the three changes, each with its exact timestamps and a short playable
context clip, then "What I decided". Writes /Volumes/Extreme/_edit_work/ro20/round3/index.html (port 8868); the round 5 page is
kept as index-r5.html. usage: python3 page8_r6.py"""
import os, shutil

PAGE = "/Volumes/Extreme/_edit_work/ro20/round3"
STYLE = """<style>body{font:15px/1.45 -apple-system,Helvetica,Arial;margin:0;background:#0d1626;color:#e8eef7}main{max-width:1100px;margin:0 auto 60px;padding:0 24px}
h1{font-size:24px;margin:22px 0 6px}h2{font-size:19px;margin:30px 0 10px;border-top:1px solid #26354d;padding-top:18px}h3{font-size:16px;margin:20px 0 6px;color:#8fd0ff}
.sub{color:#9fb2cc}a{color:#8fd0ff}video{width:100%;border-radius:10px;background:#000;display:block;margin:8px 0}.ch{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:12px 0}
.k{color:#9fb2cc;font-weight:600}li{margin:5px 0}code{color:#cfe2f7}</style>"""
CHANGES = [
    ("The new intro", "0:00.0 to 0:06.9", "0:00 to 0:12", "r6-intro.mp4",
     "Big title over three AI clips that open on your words: Skid Row kettlebell deadlift (now facing the camera, knees bent), "
     "salmon dinner at home, mansion home gym (woman removed). Your locked intro voice is unchanged. The pool clip follows at 0:06.9 as before."),
    ("Hot dog excuse guy", "1:47.3 to 1:51.9", "1:42 to 1:57", "r6-hotdog.mp4",
     "Mouth closed, pouting and shrugging under “I can't afford healthy food, Dan. If I only had money like you, I could afford to eat "
     "healthy,” then back to you on camera for “but I can't, so there's nothing I can do.”"),
    ("Pizza couch excuse guy", "4:13.0 to 4:15.2", "4:08 to 4:20", "r6-pizza.mp4",
     "Lip-synced to your own “Dan, I don't have the money for $30 a pound”; you're on camera for “Oh,” before it and "
     "“on salmon every week” after it."),
]
DECIDED = [
    "Both excuse clips follow your lip-sync rule: the hot dog guy's sync measured too weak, so he keeps his mouth closed; two full-length "
    "mouth-closed takes groaned mid-line, so his clip covers the line up to “eat healthy,” and the film cuts back to you at the comma.",
    "The pizza guy's sync timed well but smeared his beard; I kept the synced lips and put the take's own sharp beard back around them, "
    "and used only the stretch a reviewer passed (your round 2 “use the segment that lined up best” instruction).",
    "Salmon dinner tile: the long takes kept redrawing your hair and face whenever you looked down at the plate, so the tile is two short "
    "clean shots with a cut (smiling at the meal, then cutting the salmon).",
    "Every clip passed the automatic motion check and a separate independent reviewer on the exact seconds used. The full film passed a "
    "fresh frame-by-frame judge (944 images, 0 defects) and the ad-safety image scan.",
    "Everything else is round 4's approved film, copied bit for bit. Same length (29:41).",
    "Known items carried from round 4, unchanged: hair touching the top edge on the kitchen roll, and the audio check's tone row (your locked voice).",
    "Each tile's AI-GENERATED label fades in about a tenth of a second after its clip appears; the template is fixed for next time.",
    "Spend this round: $12.92 ($12.00 paid Veo clips after Flow ran out, $0.92 lip sync). Images were on the Codex subscription.",
]


def main():
    if os.path.exists(f"{PAGE}/index.html") and not os.path.exists(f"{PAGE}/index-r5.html"):
        shutil.copy(f"{PAGE}/index.html", f"{PAGE}/index-r5.html")
    h = ["<!doctype html><meta charset='utf-8'><title>What To Buy For Your Health LFC R6</title>" + STYLE + "<main>",
         "<h1>What To Buy For Your Health At Every Income Level (RO-20C), round 6</h1>",
         "<p class='sub'>The full film with your round 5 changes. Everything else is the round 4 film you approved. "
         "<a href='index-r5.html'>Round 5 frames page</a> · <a href='index-r4.html'>Round 4 page</a></p>",
         "<h2>The full film</h2><video controls preload='metadata' src='r6/r6-full-540p.mp4'></video>",
         "<p class='sub'>Full quality for VLC: <code>Videos to Review/What To Buy For Your Health LFC R6 - full film.mp4</code></p>",
         "<h2>What changed (3 places)</h2>"]
    for name, at, watch, clip, what in CHANGES:
        h.append(f"<div class='ch'><h3>{name}: {at}</h3><div><span class='k'>Watch:</span> {watch}</div><div>{what}</div>"
                 f"<video controls preload='none' src='r6/{clip}'></video></div>")
    h.append("<h2>What I decided (overrule anything)</h2><ul>" + "".join(f"<li>{d}</li>" for d in DECIDED) + "</ul></main>")
    open(f"{PAGE}/index.html", "w").write("\n".join(h))
    print("page ->", f"{PAGE}/index.html")


if __name__ == "__main__":
    main()
