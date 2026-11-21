#!/usr/bin/env python3
"""SL-03 round 1 review page (standard layout: locks + decisions, what I decided, every item three per row, one reply box)."""
import html, json
E = html.escape; R = '/Volumes/Extreme/_edit_work/sl03/round1'
def card(img, title, lines, tag=''):
    t = f' <span class="tag">{tag}</span>' if tag else ''
    return f'<article><a href="stills/{img}.jpg" target="_blank"><img loading="lazy" src="stills/{img}_sm.jpg"></a><h3>{title}{t}</h3><div class="copy">{"<br>".join(lines)}</div></article>'
def sp(b, d, a): return f'<details><summary>What you are saying</summary><b>before:</b> {E(b)}<br><b>during:</b> {E(d)}<br><b>after:</b> {E(a)}</details>'
items = [
 card('O1_fill', 'O1 Opener, option A: salad fills the frame', ['0:00 to 0:02. The finished salad, full frame, then cut to you.', 'Sharper and bigger on a phone; the bowl rim is cut at the sides.', sp('(start of the short)', "let's talk about why you should be making a daily salad", 'and why I consider this my most important fitness habit.')], 'recommended'),
 card('O1', 'O1 Opener, option B: centre square', ['Same moment as a square on the blue field, so the bowl is shown wider. Your rule for the overhead salad table; this shot is a close-up, so I lean to A.']),
 card('L1', 'L1 Crop: wide level', ['0:02 to 0:06. The full height of the camera frame, steady (no following).', sp("let's talk about why you should be making a daily salad", 'and why I consider this my most important fitness habit.', 'So I practice intermittent fasting')]),
 card('L2', 'L2 Crop: closer level', ['0:06 to 0:17. 1.2x closer, from the top of the frame. The switch hides the cut where a pause was removed.', sp('my most important fitness habit.', "So I practice intermittent fasting which means I'm fasting until about 2pm every day. Scientific research has proven that the way that you break your fast is incredibly, incredibly important.", 'If you break your fast with a ton of carbs or sugar')]),
 card('G1', 'G1 Key point 1', ['0:18 to 0:26. <b>KEY POINT</b>: Break Your Fast With CARBS / And Fasting Barely Works', 'Line 1 lands on "carbs", line 2 on "is not going to be". Back on the wide level because you lean in here. The bar sits under your chin on the lowest frame (33 px clear), captions under the bar.', sp('the way that you break your fast is incredibly, incredibly important.', 'If you break your fast with a ton of carbs or sugar or worst of all alcohol, then intermittent fasting is not going to be anywhere near as effective.', 'However, if your first meal consists of a low carb meal')]),
 card('C2', 'C2 Salad cutaway', ['0:30 to 0:31. The salad again on "like this salad for example", full frame, with key point 2 already up.', sp('However, if your first meal consists of a low carb meal,', 'like this salad for example,', 'then your fast is going to be far more effective for fat loss')]),
 card('G2', 'G2 Key point 2', ['0:27 to 0:36. <b>KEY POINT</b>: A LOW-CARB First Meal / Means Far More FAT LOSS', 'Line 1 lands on "low carb meal", line 2 on "far more effective".', sp('not going to be anywhere near as effective.', 'However, if your first meal consists of a low carb meal, like this salad for example, then your fast is going to be far more effective for fat loss and for supporting your health.', 'So if you really want to lock in')]),
 card('L3', 'L3 Crop: the closing line', ['0:36 to 0:38.5. The camera is very close here and you lean across the frame, so this one shot follows your face gently. Captions drop a little lower to stay off your chin.', sp('for fat loss and for supporting your health.', "So if you really want to lock in, start doing what I'm doing right here.", '(end of the short)')]),
 card('P5_B', 'P5 App short, layout B: phone beside you', ['Phone 20% larger than in the long-form, you tall beside it, captions on the blue under both. Nothing covers the screen or your face.'], 'recommended'),
 card('P5_A', 'P5 App short, layout A: phone stacked over you', ['The stack I described: phone on top at the long-form size, the camera frame under it. Captions have to sit on your chest, in one line.']),
]
T = json.load(open(f'{R}/titles.json'))
trow = ''.join(f'<article><img loading="lazy" src="stills/T{k}.jpg"><h3>Short {k}: {E(v["working"])}</h3><div class="copy">{v["secs"]} s. {E(v["note"])}</div></article>' for k, v in T.items())
reply = """1. Title band (Soft Blue, on screen the whole short, picture under it): approved / changes:
2. Title copy: approved / edits:
   Short 1: INTERMITTENT FASTING / BREAK YOUR FAST WITH THIS
   Short 2: MEAL PREP / THE $20 SALAD YOU CAN MAKE FOR $4
   Short 3: MEAL PREP / KEEP YOUR SALADS FRESH FOR 7 DAYS
   Short 4: DAILY SALAD / STOP BUYING SALAD DRESSING
   Short 5: AI MACRO TRACKING / TRACK A WEEK OF MEALS FROM 1 PHOTO
   Short 6: AI CALORIE TRACKING / THE ONE LINE THAT MAKES IT ACCURATE
3. Key-point bar (look and position, above the captions): approved / changes:
4. Key-point copy: approved / edits:
   G1: Break Your Fast With CARBS / And Fasting Barely Works
   G2: A LOW-CARB First Meal / Means Far More FAT LOSS
5. Salad shots: A fill the frame / B centre square
6. App shorts layout: B phone beside me / A phone stacked over me
7. Hair at the top edge (camera framing): accept, as on the last two batches / other:
8. Small AbsByAI.com in the corner: keep / remove
Other notes (anything in "What I decided"):"""
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Daily Salad SFC R1</title>
<style>:root{{--bg:#050d1c;--panel:#0b1a30;--line:#234a6e;--cy:#68c5ff;--text:#f4faff;--muted:#b4c6d8}}
body{{margin:0;background:var(--bg);color:var(--text);font:17px system-ui,-apple-system,sans-serif;line-height:1.55}}main{{max-width:1500px;margin:auto;padding:28px 16px}}
h1{{font-size:36px;margin:0 0 6px}}h2{{font-size:25px;margin-top:0}}h3{{font-size:17px;margin:10px 0 4px}}p,li{{color:var(--muted)}}li b,p b{{color:var(--text)}}
section{{margin:26px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:16px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}
article{{min-width:0;background:#07142a;padding:12px;border-radius:12px}}img{{width:100%;border-radius:10px;background:#000;display:block}}
a{{color:#9bd6ff}}.tag{{color:#fff;background:#1f6fb0;font-size:12px;font-weight:700;padding:2px 8px;border-radius:9px}}.copy{{font-size:14px;color:#dfe9f2}}.notice{{border-left:4px solid var(--cy);padding:10px 16px;background:#0e2440}}
details{{margin-top:6px;font-size:13px;color:#b4c6d8}}summary{{cursor:pointer;color:#9bd6ff}}
textarea{{width:100%;box-sizing:border-box;min-height:400px;background:#030915;color:#fff;padding:14px;font:15px ui-monospace,monospace;border:1px solid #2c5d8a;border-radius:10px}}
button{{background:#1f6fb0;color:#fff;border:0;border-radius:9px;padding:10px 16px;cursor:pointer;font-size:15px}}nav{{display:flex;gap:14px;flex-wrap:wrap;font-size:15px}}
@media(max-width:820px){{.grid{{grid-template-columns:1fr 1fr}}}}@media(max-width:520px){{.grid{{grid-template-columns:1fr}}h1{{font-size:28px}}}}</style>
<main><h1>Daily Salad shorts / Round 1</h1>
<p>Six shorts from the approved "How I Make My Daily Salad" long-form (the six you picked, A to F). This round is short 1's crop, title and every graphic as stills on its real frames, plus the phone layout for the two app shorts. Nothing is cut yet, nothing uploads, no covers. First batch of shorts in Soft Blue Light.</p>
<p class="notice"><b>Already locked and reused:</b> the long-form's colour (same footage, same grade), its approved sound (cut only, never reprocessed), the title-band layout you finalized on the last two shorts batches (title on screen the whole short, never on you, picture under it), white Arial captions, hard cuts, no AbsByAI.com end mark, no swipe sounds. Every still below is a real frame of the raw kitchen footage in that grade; the captions on the stills are a close mock-up of the burned ones.</p>
<nav><a href="#decide">Your 8 decisions</a><a href="#decided">What I decided</a><a href="#items">Short 1, every item</a><a href="#titles">All six titles</a><a href="#hair">Hair evidence</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions (8)</h2><ol>
<li><b>Title band.</b> The band you finalized, redrawn in Soft Blue Light: blue field, small cyan topic line, white headline, on screen for the whole short. Approve, or say what to change.</li>
<li><b>Title copy</b> for all six (in the reply box). Your working titles, fitted to two lines.</li>
<li><b>Key-point bar.</b> The Soft Blue lower third, each line landing on the word you say. It sits under your face and above the captions. Approve the look and position.</li>
<li><b>Key-point copy</b>, G1 and G2 (two lines each, so the bar never reaches your chin).</li>
<li><b>Salad shots.</b> A (recommended): fill the frame. B: centre square on the blue field.</li>
<li><b>App shorts layout.</b> B (recommended): the phone beside you, both tall, captions underneath. A: the phone stacked over you, as I first described.</li>
<li><b>Hair at the top edge.</b> The camera framed the top of your hair at the very edge of the picture in every one of these kitchen shots (evidence below), so no crop can add room above it. You accepted the same on the last two batches; the title band sits right above, so it reads as the band's edge. Accept?</li>
<li><b>Small AbsByAI.com in the corner.</b> Kept, as on every short so far. This is not the end mark you retired. Keep or remove?</li></ol></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>
<li><b>Cut from the raw kitchen footage, not the finished long-form.</b> The long-form has its title cards, zooms and the phone baked into the picture. Going back to the camera files with the same colour recipe gives a cleaner, sharper vertical.</li>
<li><b>Short 1 opens on "let's talk about why you should be making a daily salad"</b> over the finished salad. I dropped "Alright, so".</li>
<li><b>Short 1 is 38.5 seconds</b> on your ranges (you estimated 42). It ends on "start doing what I'm doing right here."</li>
<li><b>Short 2 starts on "let's talk about why I make it myself"</b> ("But" dropped; a real pause allows it), so the extra "it only costs a few dollars" opener is not needed. 44 s.</li>
<li><b>Short 3 opens on "how to keep these salads fresh for seven days"</b>, dropping "All right, so let's talk about the next part", which points back at the long-form. The silent boxing-up stretch is trimmed to about one second. 49 s.</li>
<li><b>Short 4:</b> your three ranges as picked, 53 s.</li>
<li><b>Short 5 starts its last part at "So scrolling down to the bottom"</b> instead of a few seconds earlier. Your ranges ran 60.2 s and that earlier sentence is already cut off in the long-form. Now 57 s.</li>
<li><b>Short 6's first part ends on "Just a few olives per salad."</b> instead of stopping mid-sentence. 54.5 s.</li>
<li><b>Two crop levels, both steady.</b> The camera does not follow you, except the last 3 seconds of short 1 where the camera is so close that a fixed window would cut your face.</li>
<li><b>Two key points in short 1, not more</b>, each a distilled point, never a repeat of the words.</li>
<li><b>Captions</b> sit under the key-point bar and above the area the apps cover with their own buttons.</li>
<li><b>Audio check passed:</b> the long-form's sound and picture share one clock (no drift at ten points), and every cut lands in a measured pause or on one of the long-form's own cuts. Three cut points get an ear check next round before anything is rendered.</li>
<li><b>Spend so far: $0.</b> No AI clips are planned for this batch.</li></ul></section>
<section id="items"><h2>Short 1, every item in order</h2><p>Tap any still to open it full size.</p><div class="grid">{''.join(items)}</div></section>
<section id="titles"><h2>The title band on all six</h2><div class="grid">{trow}</div></section>
<section id="hair"><h2>Hair evidence</h2><p>Four whole camera frames from short 1's shots. The red line is the top edge of what the camera recorded: your hair is already at it.</p><a href="stills/HAIR.jpg" target="_blank"><img loading="lazy" src="stills/HAIR.jpg" style="max-width:1100px"></a></section>
<section id="reply"><h2>Reply</h2><textarea id="r">{E(reply)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy</button></p></section>
</main></html>"""
open(f'{R}/index.html', 'w').write(page); print('page ok', page.count('—'))
