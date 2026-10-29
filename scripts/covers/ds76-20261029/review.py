from pathlib import Path
import json,html
LABELS={'A':'Top Of The Rep, Yellow Headline','B':'Back View V-Taper, White And Cyan','C':'Real Studio Photo','D':'Assisted Machine, Large Bottom Title','E':'Backyard Pool Bar, White And Gold','F':'Your Screenshot: Full Rep, Yellow Headline','G':'Your Screenshot: Front Close-Up, White And Cyan','H':'Your Screenshot: Back View, Navy Plaque'}
from build import OUT,ROOT
R=OUT/'ds76';manifest=json.loads((R/'manifest.json').read_text())
labels=LABELS
parts=['''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pull-Ups: Five Cover Choices</title><style>
*{box-sizing:border-box}body{margin:0;background:#101823;color:#f1f5f9;font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1300px;margin:0 auto;padding:32px 22px}h1{font-size:36px;margin:0 0 12px}p{max-width:850px;color:#cbd5e1}.nav{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}a{color:#64e4f3}.nav a{padding:8px 22px;background:#233147;border-radius:8px;text-decoration:none}.notice{padding:18px 22px;border:1px solid #36506a;border-radius:12px;background:#182437}section{margin:28px 0;padding:24px;background:#182230;border:1px solid #344156;border-radius:14px}.pair{display:grid;grid-template-columns:1fr 1fr 0.75fr;gap:22px;align-items:start}.pair img{width:100%;height:auto;border-radius:6px}figure{margin:0}figcaption{font-size:15px;margin:0 0 10px;color:#cbd5e1}h2{margin:0 0 20px}small{color:#b1bfd1}.sheet{max-width:100%;border-radius:10px}.tip{color:#ffd74f} @media(max-width:700px){main{padding:20px 12px}.pair{grid-template-columns:1fr 1fr;gap:12px}.grid{grid-column:1/3;max-width:240px}section{padding:16px}h1{font-size:28px}}
</style></head><body><main><h1>How To Do Pull-Ups</h1><p>Five cover choices. Each option includes a separate Instagram layout and YouTube Shorts layout. Click a picture for its full-size file.</p><div class="notice"><strong>Choose A to H in this chat.</strong><p class="tip">My recommendation: A. The exercise is clear, your face reads well, and the yellow headline is easy to spot on a phone.</p><small>Your approved R2 film is preserved. Nothing has been uploaded or scheduled. C uses your original studio photograph; A, B, D and E use Codex images based on your real identity reference. No paid image API was used.</small></div><div class="nav">''']
for k in 'ABCDEFGH':parts.append(f'<a href="#{k}">{k}</a>')
parts.append('</div><a href="five-cover-choices.jpg"><img class="sheet" src="five-cover-choices.jpg" alt="All five cover choices in both layouts"></a>')
for k in 'ABCDEFGH':
 if k=='F':parts.append('<h2 style="margin-top:44px">New: touched-up screenshots of you (F, G, H)</h2><p>Real frames from your pull-up footage, retouched by Codex for sharper muscle definition and cleaner light. Same face, pose and gym.</p>')
 parts.append(f'<section id="{k}"><h2>{k}. {labels[k]}</h2><div class="pair">')
 for plat in ['instagram','youtube']:
  row=next(q for q in manifest['outputs'] if q['letter']==k and q['platform']==plat);rel=Path(row['path']).relative_to(R.relative_to(ROOT)).as_posix()
  parts.append(f'<figure><figcaption>{"Instagram" if plat=="instagram" else "YouTube Shorts"}</figcaption><a href="{rel}"><img loading="lazy" src="{rel}" alt="{k}, {plat} layout"></a></figure>')
 parts.append(f'<figure class="grid"><figcaption>Instagram profile crop</figcaption><img loading="lazy" src="grid/{k}.jpg" alt="{k}, actual Instagram 3:4 crop"></figure></div></section>')
parts.append('<p>After your pick: complete the Drive backup, upload the approved files, book a January-blitz Short slot and read the live schedules back.</p></main></body></html>')
(R/'index.html').write_text(''.join(parts));print(R/'index.html')
