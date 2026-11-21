"""DS-36 R2 proposal page: the off-the-cuff transcript with proposed cuts struck through, the time each saves, the speed-up
needed to land under 60 s, and Dan's colour options on matching frames.   python3 r2_proposal.py"""
import json, html
from pathlib import Path
W = Path('/Volumes/Expansion/_edit_work/DS-36/r2/offcuff'); OUT = Path('/Volumes/Expansion/_edit_work/DS-36/r2/page')
w = json.load(open(W/'words_out.json')); FPS = 30000/1001
TOTAL = json.load(open(W/'edl.json'))['total_frames']/FPS; CLIP = 15.682
# (label, first word index, last word index, seconds saved, why) -- seconds = gap from the first cut word to the next kept word
CUTS = [('D1', 68, 77, "A second reason for the same point. 'Because those people aren't going to change anyway' stays."),
        ('D2', 124, 126, "Filler between 'healthy shame' and 'That's what's gonna get you back on track'."),
        ('D4', 172, 184, "Repeats 'get you back on track' from 12 s earlier."),
        ('D5', 189, 192, "Repeats 'shame can be healthy' in the same breath."),
        ('D6', 227, 241, "Third time 'use that shame as motivation' and 'back on track'. Your next line, 'And then you'll start feeling good about yourself', follows 'do anything about it' cleanly.")]
saved = {}
for lab, a, b, _ in CUTS: saved[lab] = round(w[b + 1]['t0'] - w[a]['t0'], 2)
PAUSES = [('P-a', 10, 'Audience murmur after "comeback" inside Bill\'s clip, shortened from 1.9 s to 0.4 s (the layout change hides it)', 1.50),
          ('P-b', 154, 'The drawn-out "and ... then" before "then use that shame", tightened at the zoom cut', 0.45)]
cut_total = sum(saved.values()) + sum(p[3] for p in PAUSES)
after = TOTAL - cut_total; clip_after = CLIP - 1.50; dan_after = after - clip_after
TARGET = 58.5; speed = dan_after/(TARGET - clip_after); SPEED = round(speed + 0.004, 2)
final = clip_after + dan_after/SPEED
OPT = round(w[41]['t0'] - w[28]['t0'], 2)    # optional: Bill's 'We shame them out of littering and most of them out of racism.'
mark = {}
for lab, a, b, _ in CUTS:
    for i in range(a, b + 1): mark[i] = lab
opt = set(range(28, 41)); pause_at = {p[1]: p for p in PAUSES}
def para(lo, hi):
    out = []
    for i in range(lo, hi):
        x = w[i]; t = html.escape(x['w'])
        if i in mark: t = f'<del title="{mark[i]}">{t}</del>' + (f'<sup>{mark[i]}</sup>' if i == max(k for k in mark if mark[k] == mark[i]) else '')
        elif i in opt: t = f'<s class="opt">{t}</s>' + ('<sup>optional</sup>' if i == 40 else '')
        out.append(t)
        if i in pause_at: out.append(f'<span class="pause">[{pause_at[i][0]} pause, -{pause_at[i][3]:.2f} s]</span>')
    return ' '.join(out)
rows = ''.join(f"<tr><td>{lab}</td><td>{html.escape(' '.join(x['w'] for x in w[a:b+1]))}</td><td>-{saved[lab]:.2f} s</td><td>{html.escape(why)}</td></tr>" for lab, a, b, why in CUTS)
rows += ''.join(f"<tr><td>{p[0]}</td><td>{html.escape(p[2])}</td><td>-{p[3]:.2f} s</td><td>Pause only, no words lost.</td></tr>" for p in PAUSES)
looks = [('A', 'Current approved look (Codex R5 warm), as in round 1'), ('B', 'Warmer: more golden skin, a touch more colour'),
         ('C', 'Brighter: lifted and cleaner, softer contrast'), ('D', 'Punchier: deeper contrast, richer colour')]
frames = [('watching', 'Watching Bill'), ('reply', 'Your reply over the panel'), ('wide', 'Wide shot'), ('tight', 'Tight shot')]
col = ''.join(f"<h3>{k}. {html.escape(d)}</h3><div class='row'>" + ''.join(f"<figure><img loading='lazy' src='colour/{k}_{f}.jpg'><figcaption>{n}</figcaption></figure>" for f, n in frames) + '</div>' for k, d in looks)
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fat Shaming R2 Plan</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c;--cut:#ff7b72;--ok:#3ddc97}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1100px;margin:0 auto;padding:16px 16px 80px}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:32px}}.badge{{color:var(--acc);font-weight:600}}
.box{{background:var(--card);border-radius:10px;padding:14px 16px}}.big{{font-size:22px;font-weight:700}}del{{color:var(--cut);text-decoration-thickness:2px}}s.opt{{color:#e3b341}}sup{{color:var(--cut);font-size:11px;margin-left:2px}}
.pause{{color:var(--mut);font-size:13px}}table{{width:100%;border-collapse:collapse;font-size:14px}}td,th{{border-bottom:1px solid #2a3644;padding:6px;text-align:left;vertical-align:top}}
.row{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}}@media(max-width:700px){{.row{{grid-template-columns:1fr 1fr}}}}figure{{margin:0}}figure img{{width:100%;border-radius:6px}}figcaption{{color:var(--mut);font-size:13px}}
.q li{{margin:6px 0}}</style></head><body><main>
<p class="badge">CONTENT · Dedicated Short (SFC) · Round 2 plan · DS-36 · off the cuff</p>
<h1>Bill Maher Says Fat Shaming Should Come Back. He's Right.</h1>
<div class="box"><p class="big">{TOTAL:.1f} s now → {after:.1f} s after cuts → <span style="color:var(--ok)">{final:.1f} s</span> with your reply sped up {SPEED:.2f}x</p>
<p>Cuts save {cut_total:.1f} s (five repeated or filler lines, two pauses). That leaves {after:.1f} s, so your reply also needs a speed-up of <b>{SPEED:.2f}x</b> ({(SPEED-1)*100:.0f}% faster, pitch kept) to land at {final:.1f} s with a little room under 60. Bill's clip stays at normal speed.</p>
<p>Alternative: also cut Bill's line <span style="color:#e3b341">"We shame them out of littering and most of them out of racism."</span> (-{OPT:.2f} s). Then the reply only needs {dan_after/(TARGET - clip_after + OPT):.2f}x. It means a cut inside Bill's single camera, hidden by a zoom cut on you while you watch.</p></div>
<h2>Transcript with the proposed cuts</h2>
<p><del>Red strike</del> = proposed cut. <s class="opt">Yellow strike</s> = optional cut. Grey = pause trimmed.</p>
<div class="box"><p><b>Bill (clip):</b> {para(0, 48)}</p><p><b>You:</b> {para(48, len(w))}</p></div>
<h2>What each cut saves</h2><div class="box"><table><tr><th>Cut</th><th>Words</th><th>Saves</th><th>Why</th></tr>{rows}</table></div>
<p>Every point you make stays: shaming others is pointless, shame yourself instead, weigh in daily, 3 pounds over means act, catch it early, use it to lock in on diet and workouts, shame can save your life, don't wallow, then you feel good. The graphics and cutaways move with the words they sit on ("Shaming Others Changes Nothing" lands on "Because those people..."; the curls cutaway ends at "workouts handled").</p>
<h2>Colour options (your picture only; Bill's clip and the cutaways are unchanged)</h2>
<p>Same four moments in each look. A is what round 1 used.</p>{col}
<h2>Your calls</h2><ol class="q"><li>Approve the cuts (or name any line to keep).</li><li>Speed-up {SPEED:.2f}x on your reply, or also cut Bill's littering/racism line and speed up less.</li><li>Colour: A, B, C or D.</li></ol>
</main></body></html>"""
(OUT/'index.html').write_text(page)
print(json.dumps(dict(total=round(TOTAL, 2), saved=saved, pauses=[p[3] for p in PAUSES], cut_total=round(cut_total, 2), after=round(after, 2),
                      clip_after=round(clip_after, 2), dan_after=round(dan_after, 2), speed=SPEED, final=round(final, 2), optional=OPT,
                      speed_with_optional=round(dan_after/(TARGET - clip_after + OPT), 3))))
